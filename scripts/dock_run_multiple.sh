#!/bin/bash

# --- CONFIGURATION ---
RECEPTOR_PDB="1vsn.pdb"              # Your protein file
LIGAND_DIR="ligands_folder"           # Where your .sdf files are
PYTHON_SCRIPT="int_pipeline.py"       # Your PLIP analysis script

# GRID BOX (Based on your report.xml NFT position)
CENTER_X=2.3
CENTER_Y=25.9
CENTER_Z=0.5
SIZE_X=20.0
SIZE_Y=20.0
SIZE_Z=20.0
# ---------------------

# 1. Prepare Receptor for Vina (PDB -> PDBQT)
echo "--- Preparing Receptor ---"
obabel "$RECEPTOR_PDB" -O receptor.pdbqt -xr -p 7.4

for LIG_SDF in "$LIGAND_DIR"/*.sdf; do
    LIG_NAME=$(basename "$LIG_SDF" .sdf)
    echo "========================================"
    echo "DOCKING: $LIG_NAME"
    echo "========================================"

    # 2. Convert SDF to PDBQT for Vina
    # mk_prepare_ligand.py is part of the 'meeko' python package
    python3 -m meeko.cli.mk_prepare_ligand -i "$LIG_SDF" -o "${LIG_NAME}.pdbqt"

    # 3. Run AutoDock Vina
    vina --receptor receptor.pdbqt \
         --ligand "${LIG_NAME}.pdbqt" \
         --center_x $CENTER_X --center_y $CENTER_Y --center_z $CENTER_Z \
         --size_x $SIZE_X --size_y $SIZE_Y --size_z $SIZE_Z \
         --out "${LIG_NAME}_out.pdbqt" --exhaustiveness 8

    # 4. Extract BEST Pose (Pose 1) and convert to PDB
    # -f 1 -l 1 tells obabel to take ONLY the first model
    obabel "${LIG_NAME}_out.pdbqt" -O "${LIG_NAME}_docked.pdb" -f 1 -l 1

    # 5. Create Complex for PLIP (Merging Protein + Docked Ligand)
    grep -v "END" "$RECEPTOR_PDB" > "${LIG_NAME}_complex.pdb"
    cat "${LIG_NAME}_docked.pdb" >> "${LIG_NAME}_complex.pdb"
    echo "END" >> "${LIG_NAME}_complex.pdb"

    # 6. Run Interaction Analysis
    echo "--- Analyzing Interactions ---"
    python3 "$PYTHON_SCRIPT" "${LIG_NAME}_complex.pdb"

    # 7. Cleanup
    rm "${LIG_NAME}.pdbqt" "${LIG_NAME}_out.pdbqt" "${LIG_NAME}_docked.pdb" "${LIG_NAME}_complex.pdb"
done

echo "DONE! All ligands docked and analyzed."

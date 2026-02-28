# Automated-protein-ligand-interaction-pipeline

Automated Protein-Ligand Docking & Interaction Pipeline
This repository contains a high-throughput pipeline designed to automate the process of docking multiple ligands into a protein receptor and performing detailed 2D and 3D interaction analysis.

🚀 Overview
The pipeline automates the following steps:

Receptor Preparation: Converts the protein PDB into PDBQT format using Open Babel.

Ligand Preparation: Batch processes .sdf files into Vina-compatible .pdbqt files using meeko.

Molecular Docking: Runs AutoDock Vina to find the optimal binding poses.

Complex Assembly: Merges the best docking pose with the receptor for analysis.

Interaction Mapping: Uses PLIP (Protein-Ligand Interaction Profiler) to identify chemical bonds.

Visualization: Generates a 2D Hydrogen Bond Network (NetworkX) and an Interactive 3D View (py3Dmol).

🛠️ Prerequisites
Ensure you have the following tools installed on your system:

Software
AutoDock Vina: For the docking engine.

Open Babel: For chemical file format conversion.

PLIP: Protein-Ligand Interaction Profiler.

Python Dependencies
Bash
pip install rdkit meeko py3Dmol networkx matplotlib
📂 File Structure
dock_run_multiple.sh: The master bash script that orchestrates the docking loop.

int_pipeline.py: Python script for interaction analysis and visualization.

1vsn.pdb: Your target protein (Receptor).

ligands_folder/: Directory containing all candidate ligands in .sdf format.

📖 Usage Instructions
1. Configure the Grid Box
Open dock_run_multiple.sh and update the center and size coordinates to match your protein's active site:

Bash
CENTER_X=2.3
CENTER_Y=25.9
CENTER_Z=0.5
SIZE_X=20.0
SIZE_Y=20.0
SIZE_Z=20.0
2. Run the Pipeline
Give execution permissions to the script and run it:

Bash
chmod +x dock_run_multiple.sh
./dock_run_multiple.sh
📊 Outputs
For every ligand in your folder, the script creates an analysis_[LigandName]_complex/ directory containing:

report.xml: Raw PLIP interaction data.

[Ligand]_HBOND_network.png: A 2D circular map of hydrogen bonds between the ligand and specific residues.

[Ligand]_3D.html: An interactive 3D visualization of the binding site with a VDW surface.

🧠 Technical Details
Connectivity Correction
The pipeline uses RDKit to sanitize PDB files. This prevents the "tangled lines" effect often seen in PDB exports by correctly perceiving bond orders before analysis.

Hydrogen Bond Mapping
The 2D network strictly maps residues involved in hydrogen bonding to the central ligand, providing a clean, high-contrast visualization for publications.

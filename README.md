# 🔬 Automated Protein–Ligand Docking & Interaction Analysis Pipeline

## 📌 Project Overview

This project is an **automated end-to-end molecular docking and interaction analysis pipeline** designed to:

* Dock multiple ligands against a target protein
* Extract the best binding pose
* Generate protein–ligand complex structures
* Perform interaction analysis
* Automatically generate:

  * ✅ 2D hydrogen bond interaction network
  * ✅ 3D interactive visualization (HTML)
  * ✅ PLIP reports (XML, TXT)
  * ✅ Organized output folders

The pipeline integrates:

* **AutoDock Vina**
* **Open Babel**
* **PLIP**
* **RDKit**
* **Meeko**
* **py3Dmol**
* **NetworkX**

---

# 🧠 Workflow Architecture

```
Protein (PDB)
      ↓
Receptor Preparation (PDB → PDBQT)
      ↓
Multiple Ligands (.sdf)
      ↓
Ligand Preparation (Meeko)
      ↓
AutoDock Vina Docking
      ↓
Best Pose Extraction
      ↓
Complex Generation
      ↓
PLIP Interaction Analysis
      ↓
2D Network + 3D HTML Visualization + Reports
```

---

# 📂 Project Structure

```
.
├── 1vsn.pdb                  # Receptor protein taken in this study from RCSB PDB
├── ligands_folder/           # Multiple ligand SDF files from Pubchem
├── dock_run_multiple.sh      # Docking automation script
├── interaction_pipeline.py           # Interaction & visualization script
└── analysis_<ligand_name>/   # Auto-generated output folders
```

---

# ⚙️ Features

## 1️⃣ Automated Multi-Ligand Docking

* Loops through all `.sdf` files
* Converts to `.pdbqt`
* Performs docking using AutoDock Vina
* Extracts best binding pose (Pose 1)

## 2️⃣ Complex Generation

* Merges protein + docked ligand
* Creates temporary complex structure
* Ready for interaction profiling

## 3️⃣ Interaction Analysis

Using PLIP engine:

* Hydrogen bonds
* Hydrophobic interactions
* Salt bridges
* π-Stacking
* Water bridges

## 4️⃣ Custom 2D Hydrogen Bond Network

* Parses PLIP XML output
* Generates circular interaction map
* Ligand: Central yellow node
* Residues: Green-bordered nodes
* Hydrogen bonds: Blue dashed edges
* Saved as high-resolution PNG (300 dpi)

## 5️⃣ Interactive 3D Visualization

* Cartoon protein structure
* Stick & sphere ligand representation
* Van der Waals surface
* Exported as interactive HTML file

---

# 📊 Output Example

For each ligand:

```
analysis_LIG1/
│
├── report.xml
├── report.txt
├── LIG1_HBOND_network.png
├── LIG1_3D.html
└── additional PLIP files
```

---

# 🧪 Example Use Case

Protein: `1vsn.pdb`
Ligands: Multiple drug candidates in SDF format

This pipeline enables:

* Virtual screening
* Binding interaction validation
* Drug repurposing studies
* Structure-based drug design analysis

---

# 🚀 How to Run

## Step 1: Install Dependencies

```bash
conda install -c conda-forge openbabel
conda install -c conda-forge plip
pip install rdkit networkx matplotlib py3Dmol meeko
```

Install AutoDock Vina separately.

---

## Step 2: Edit Grid Box Coordinates

In `dock_run_multiple.sh`, modify:

```
CENTER_X
CENTER_Y
CENTER_Z
SIZE_X
SIZE_Y
SIZE_Z
```

---

## Step 3: Run the Pipeline

```bash
chmod +x dock_run_multiple.sh
./dock_run_multiple.sh
```

---

# 🧬 Scientific Significance

This pipeline demonstrates:

* Structure-Based Drug Design (SBDD)
* Molecular docking automation
* Interaction network modeling
* Reproducible computational workflows
* Integration of cheminformatics and structural bioinformatics

---

# 💡 Skills Demonstrated

* Molecular docking automation
* Bash scripting
* Python pipeline development
* XML parsing
* Graph-based interaction modeling
* 3D molecular visualization
* RDKit bond perception correction
* Workflow optimization

---

# 🔮 Future Improvements

* Add binding affinity ranking summary CSV
* Add heatmap of interaction frequencies
* Parallel docking execution
* Integration with molecular dynamics (e.g., GROMACS)
* Web-based dashboard interface

---

# 👩‍💻 Author

**Koka Nikhila Bhavani**
Bioinformatician


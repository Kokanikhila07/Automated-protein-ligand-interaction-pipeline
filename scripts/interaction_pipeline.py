import sys
import os
import subprocess
import py3Dmol
import glob
import shutil
import xml.etree.ElementTree as ET
import networkx as nx
import matplotlib.pyplot as plt
from rdkit import Chem

def fix_ligand_connectivity(pdb_path):
    """Fixes 'tangled lines' by perceiving bonds via RDKit."""
    print(f"--- Sanitizing PDB: {pdb_path} ---")
    mol = Chem.MolFromPDBFile(pdb_path, removeHs=False)
    if mol:
        fixed_path = pdb_path.replace(".pdb", "_fixed.pdb")
        Chem.MolToPDBFile(mol, fixed_path)
        return fixed_path
    return pdb_path

def generate_custom_2d_network(xml_path, output_path):
    """Parses PLIP XML to create a circular network STRICTLY for Hydrogen Bonds."""
    if not os.path.exists(xml_path):
        return
    
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    G = nx.Graph()
    lig_name = "NFT"
    hbond_residues = []

    # Correct path to find hydrogen bonds in your specific XML structure
    for site in root.findall('.//bindingsite'):
        lig_node = site.find('.//identifiers/longname')
        if lig_node is not None:
            lig_name = lig_node.text
        
        # In your XML, bonds are in <interactions><hydrogen_bonds><hydrogen_bond>
        hb_list = site.findall('.//interactions/hydrogen_bonds/hydrogen_bond')
        for hb in hb_list:
            res_num = hb.find('resnr').text
            res_type = hb.find('restype').text
            hbond_residues.append(f"{res_type}{res_num}")

    target_residues = list(set(hbond_residues))
    
    if not target_residues:
        print("Warning: No Hydrogen Bonds found in the nested XML structure.")
        return 

    central_node = lig_name.upper()
    G.add_node(central_node)
    for res in target_residues:
        G.add_edge(central_node, res)

    # Plotting
    plt.figure(figsize=(8, 8))
    pos = nx.circular_layout(G)
    
    # Visual Styling: Blue dashed lines for H-bonds
    nx.draw_networkx_edges(G, pos, style='dashed', edge_color='#4a90e2', width=2.0)
    
    # Central Ligand Node (Yellow)
    nx.draw_networkx_nodes(G, pos, nodelist=[central_node], node_color='#ffcc00', 
                           node_size=10000, node_shape='o')
    
    # Residue Nodes (White squares with green border)
    nx.draw_networkx_nodes(G, pos, nodelist=target_residues, node_color='white', 
                           node_size=2000, edgecolors='#1e7544', node_shape='s')

    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    
    plt.title(f"Hydrogen Bond Network: {central_node}", pad=20)
    plt.axis('off')
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"[SUCCESS] Hydrogen Bond 2D Network created: {output_path}")

def run_full_analysis(pdb_path):
    base_name = os.path.splitext(os.path.basename(pdb_path))[0]
    output_dir = f"analysis_{base_name}"
    
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    processed_pdb = fix_ligand_connectivity(pdb_path)

    print(f"--- Running PLIP Engine ---")
    try:
        subprocess.run([
            'plip', '-f', processed_pdb, 
            '-p', '-y', '-t', '-x', 
            '-o', output_dir
        ], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"PLIP Error:\n{e.stderr}")
        return

    xml_files = glob.glob(f"{output_dir}/**/*.xml", recursive=True)
    if xml_files:
        custom_2d_path = os.path.join(output_dir, f"{base_name}_HBOND_network.png")
        generate_custom_2d_network(xml_files[0], custom_2d_path)

    print("--- Creating 3D View ---")
    with open(processed_pdb, 'r') as f:
        pdb_data = f.read()
    view = py3Dmol.view(width=800, height=600)
    view.addModel(pdb_data, 'pdb')
    view.setStyle({'cartoon': {'color': 'spectrum'}})
    view.setStyle({'hetflag': True}, {'stick': {'radius': 0.2}, 'sphere': {'radius': 0.4}})
    view.addSurface(py3Dmol.VDW, {'opacity': 0.2, 'color': 'white'})
    view.zoomTo({'hetflag': True})
    view.write_html(os.path.join(output_dir, f"{base_name}_3D.html"))

    if "_fixed.pdb" in processed_pdb:
        os.remove(processed_pdb)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 script.py your_complex.pdb")
    else:
        run_full_analysis(sys.argv[1])

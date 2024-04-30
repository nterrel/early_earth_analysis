import networkx as nx
import numpy as np
from networkx.algorithms import isomorphism
import ase
import logging
import pickle

#import pandas as pd
#mol_data = pd.read_parquet('/blue/roitberg/apps/lammps-ani/cumolfind/data/molecule_data.pq')
#serialized_graph = mol_data[mol_data['name'] == 'Alanine']['graph'][0]
#standard_graph = pickle.loads(serialized_graph)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


species_dict = {1: "H", 6: "C", 7: "N", 8: "O"}

bond_data = {
    "HH": 0.75, "HC": 1.09, "HN": 1.01, "HO": 0.96,
    "CC": 1.54, "CN": 1.43, "CO": 1.43,
    "NN": 1.45, "NO": 1.47, "OO": 1.48,
}

stretch_buffer = 0.2
bond_data_stretched = {k: v + stretch_buffer for k, v in bond_data.items()}

def create_networkx_graph(coordinates, atom_types, bond_data_stretched, species_dict, box_lengths):
    G = nx.Graph()
    atomic_nums = [ase.symbols.symbols2numbers(atom)[0] for atom in atom_types]
    
    for i, pos_i in enumerate(coordinates):
        atomic_num_i = atomic_nums[i]
        G.add_node(i, element=species_dict[atomic_num_i], atomic_num=atomic_num_i, pos=pos_i)
    
    for i, pos_i in enumerate(coordinates):
        for j, pos_j in enumerate(coordinates[i+1:], start=i+1):  # Adjusted loop to start from i+1
            dist = pbc_distance(np.array(pos_i), np.array(pos_j), np.array(box_lengths))
            if i == 0 and j == 1:  # Example: Log distance calculation for the first pair as a check
                logging.debug(f"Distance between atoms {i} and {j} under PBC: {dist}")
            pair_key = ''.join(sorted([species_dict[atomic_nums[i]], species_dict[atomic_nums[j]]]))
            if pair_key in bond_data_stretched and dist <= bond_data_stretched[pair_key]:
                G.add_edge(i, j)
    return G

def reorder_structure_to_match_reference(ref_graph, target_graph):
    logging.debug("Starting isomorphism check and reordering process.")
    logging.debug(f"Reference graph nodes: {ref_graph.number_of_nodes()}, edges: {ref_graph.number_of_edges()}")
    logging.debug(f"Target graph nodes: {target_graph.number_of_nodes()}, edges: {target_graph.number_of_edges()}")
    try:
        matcher = isomorphism.GraphMatcher(ref_graph, target_graph,
                                   node_match=isomorphism.categorical_node_match('element', ''))
        if matcher.is_isomorphic():
            mapping = matcher.mapping
            logging.info(f"Isomorphic match found. Mapping: {mapping}")
            # Additional log to verify mapping correctness
            for k, v in mapping.items():
                ref_node = ref_graph.nodes[k]
                target_node = target_graph.nodes[v]
                logging.debug(f"Mapping ref node {k} ({ref_node['element']}) to target node {v} ({target_node['element']})")
        if not matcher.is_isomorphic():
            logging.debug(f"Failed to match structure {index}.")
            logging.debug("Reference graph adjacency list:")
            for line in nx.generate_adjlist(ref_graph):
                logging.debug(line)
            logging.debug("Target graph adjacency list:")
            for line in nx.generate_adjlist(target_graph):
                logging.debug(line)

        else:
            logging.info("No isomorphic match found.")
            # Optionally, log the unmatched elements if the structure is expected to match
            ref_elements = {data['element'] for _, data in ref_graph.nodes(data=True)}
            target_elements = {data['element'] for _, data in target_graph.nodes(data=True)}
            logging.debug(f"Reference elements: {ref_elements}, Target elements: {target_elements}")

    except Exception as e:
        logging.error("Error during reordering: {}".format(e))
        return None

def pbc_distance(pos1, pos2, box_lengths):
    # Calculate distance vector considering periodic boundaries
    delta = np.abs(pos1 - pos2)
    delta = np.where(delta > 0.5 * box_lengths, delta - box_lengths, delta)
    # Compute the Euclidean distance with the adjusted delta
    return np.linalg.norm(delta)


def read_xyz_file(filename):
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]  # Remove empty lines and strip whitespace

    structures = []
    i = 0
    while i < len(lines):
        try:
            num_atoms = int(lines[i])
        except ValueError:
            # If conversion to int fails, skip the line and continue
            print(f"Skipping invalid line at index {i}: '{lines[i]}'")
            i += 1
            continue

        comment = lines[i + 1]  # This line is expected to be a comment
        structure = lines[i + 2:i + 2 + num_atoms]

        atom_types = []
        coordinates = []
        for line in structure:
            parts = line.split()
            if len(parts) < 4:
                print(f"Invalid structure line: {line}")
                continue
            atom_types.append(parts[0])
            coordinates.append(tuple(map(float, parts[1:4])))

        structures.append((atom_types, coordinates))
        i += num_atoms + 2  # Move to the next structure
    return structures

box_lengths = [557, 557, 557]

structures = read_xyz_file('ala_0.1ns.xyz')
standard_atom_types, standard_coordinates = structures[0]
standard_graph = create_networkx_graph(standard_coordinates, standard_atom_types, bond_data_stretched, species_dict, box_lengths)

print('Structures:',len(structures))

reordered_structures = [structures[0]]  # Include the standard as the first structure

for index, (atom_types, coordinates) in enumerate(structures[1:], start=2):  # Start=2 to account for Python indexing and that we skip the first structure
    logging.debug(f"Processing structure {index}/{len(structures)}")
    target_graph = create_networkx_graph(coordinates, atom_types, bond_data_stretched, species_dict, box_lengths)
    reordered_coords = reorder_structure_to_match_reference(standard_graph, target_graph)
    if reordered_coords:
        reordered_structures.append((atom_types, reordered_coords))
        logging.info(f"Structure {index} reordered and added.")
    else:
        logging.warning(f"Structure {index} could not be reordered.")


def write_xyz_file(filename, structures):
    with open(filename, 'w') as file:
        for atom_types, coords in structures:
            file.write(f"{len(atom_types)}\n")
            file.write("Reordered structure\n")
            for atom, (x, y, z) in zip(atom_types, coords):
                file.write(f"{atom} {x} {y} {z}\n")

write_xyz_file('reordered_0.1ns_alanines.xyz', reordered_structures)
print(bond_data_stretched)
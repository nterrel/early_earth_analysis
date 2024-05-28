import networkx as nx
import numpy as np
import ase
import logging
import pickle
import pandas as pd
import glob
import os
import re
import sys

logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# NOTE: To do: if any i,j coordinates are more than n_atoms*max_bond_data apart, set structure aside (with comment line) for manual check


def normalize_name(name):
    """Normalize molecule names to match keys in reference_graphs. Handles special cases and dipeptides."""
    original_name = name
    name = name.lower().replace('all_', '').replace('.xyz', '').replace('_', ' ')
    dipeptide_pattern = re.compile(r"(\w+)yl(\w+)")
    match = dipeptide_pattern.match(name)
    if match:
        normalized_name = match.group(1).capitalize() + " " + match.group(2).capitalize()
    else:
        normalized_name = ' '.join(word.capitalize() for word in name.split(' '))
    logging.debug(f"Normalized name from '{original_name}' to '{normalized_name}'")
    return normalized_name


species_dict = {1: "H", 6: "C", 7: "N", 8: "O"}
bond_data = {
    "HH": 0.75, "HC": 1.09, "HN": 1.01, "HO": 0.96,
    "CC": 1.54, "CN": 1.43, "CO": 1.43,
    "NN": 1.45, "NO": 1.47, "OO": 1.48,
}
stretch_buffer = 0.2
bond_data_stretched = {
    ''.join(sorted(pair)): length + stretch_buffer
    for pair, length in bond_data.items()
}

box_lengths = [557, 557, 557]

mol_data = pd.read_parquet('/red/roitberg/nick_analysis/all_mol_data.pq')
reference_graphs = {row['name']: pickle.loads(
    row['graph']) for index, row in mol_data.iterrows()}
logging.debug(f"Reference graph keys: {reference_graphs.keys()}")

def update_graph_with_elements(graph):
    """Updates reference graph with element symbols based on atomic numbers."""
    for node, data in graph.nodes(data=True):
        data['element'] = species_dict[data['atomic_number']]
    return graph


def add_element_pairs_to_edges(graph):
    """Adds element pair attributes to the edges of the graph for easier comparison."""
    for (node1, node2) in graph.edges():
        element1 = graph.nodes[node1]['element']
        element2 = graph.nodes[node2]['element']
        graph.edges[node1,
                    node2]['element_pair'] = '-'.join(sorted([element1, element2]))


def read_xyz_file(filename: str):
    """Reads XYZ file and extracts atom types and coordinates."""
    logging.info(f"Reading XYZ file: {filename}")
    structures, comments = [], []
    with open(filename, 'r') as file:
        # Remove empty lines and strip whitespace
        lines = [line.strip() for line in file if line.strip()]
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
        comments.append(comment)
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
    logging.info(f"Read {len(structures)} structures from {filename}.")
    return structures, comments


def pbc_distance(pos1, pos2, box_lengths):
    # Calculate distance vector considering periodic boundaries
    delta = np.abs(pos1 - pos2)
    delta = np.where(delta > 0.5 * box_lengths, delta - box_lengths, delta)
    return np.linalg.norm(delta)


def create_networkx_graph(coordinates, atom_types, bond_data_stretched, species_dict, box_lengths):
    G = nx.Graph()
    atomic_nums = [ase.symbols.symbols2numbers(atom)[0] for atom in atom_types]
    for i, pos_i in enumerate(coordinates):
        atomic_num_i = atomic_nums[i]
        G.add_node(
            i, element=species_dict[atomic_num_i], atomic_num=atomic_num_i, pos=pos_i)

    for i, pos_i in enumerate(coordinates):
        for j, pos_j in enumerate(coordinates[i + 1:], start=i + 1):
            dist = pbc_distance(np.array(pos_i), np.array(
                pos_j), np.array(box_lengths))
            elem_i = species_dict[atomic_nums[i]]
            elem_j = species_dict[atomic_nums[j]]
            pair_key = ''.join(sorted([elem_i, elem_j]))
            if pair_key in bond_data_stretched and dist <= bond_data_stretched[pair_key]:
                G.add_edge(i, j)
    return G


def reorder_structure_to_match_reference(ref_graph, target_graph, target_atom_types, target_coordinates):
    if nx.is_isomorphic(ref_graph, target_graph):
        edge_match = nx.isomorphism.categorical_edge_match(
            'element_pair', default='')
        node_match = nx.isomorphism.categorical_node_match('element', '')
        matcher = nx.isomorphism.GraphMatcher(ref_graph, target_graph, node_match=node_match, edge_match=edge_match)

        if matcher.is_isomorphic():
            mapping = matcher.mapping  # Mapping from target to reference
            logging.info(f"Isomorphic match found. Mapping: {mapping}")
            logging.debug(f"Mapping (target:reference): {mapping}")
            # Apply mapping: Reorder target's atoms and coordinates to match reference
            reordered_atom_types = [None] * len(target_atom_types)
            reordered_coordinates = [None] * len(target_coordinates)
            for ref_idx, target_idx in mapping.items():
                target_elem = target_graph.nodes[target_idx]['element']
                ref_elem = ref_graph.nodes[ref_idx]['element']
                logging.debug(
                    f"{target_idx}({target_elem}) -> {ref_idx}({ref_elem})")
                reordered_atom_types[ref_idx] = target_atom_types[target_idx]
                reordered_coordinates[ref_idx] = target_coordinates[target_idx]
            return reordered_atom_types, reordered_coordinates
        else:
            logging.info(
                "Graphs are structurally isomorphic but do not match on specified node attributes.")
            return None, None
    else:
        logging.info("No isomorphic match found for this structure.")
        return None, None


def write_xyz_file(filename, structures_comments):
    with open(filename, 'w') as file:
        for (atom_types, coords, comment) in structures_comments:
            file.write(f"{len(atom_types)}\n")
            file.write(f"Reordered structure from: {comment}\n")
            for atom, (x, y, z) in zip(atom_types, coords):
                file.write(f"{atom} {x:.6f} {y:.6f} {z:.6f}\n")


def write_xyz_file_failed(filename, structures_comments):
    with open(filename, 'w') as file:
        for (atom_types, coords, comment) in structures_comments:
            file.write(f"{len(atom_types)}\n")
            file.write(f"Failed reordering of: {comment}\n")
            for atom, (x, y, z) in zip(atom_types, coords):
                file.write(f"{atom} {x:.6f} {y:.6f} {z:.6f}\n")


def process_files(xyz_directory):
    for xyz_file in glob.glob(os.path.join(xyz_directory, '*.xyz')):
        logging.debug(f"Processing file: {xyz_file}")
        molecule_name = normalize_name(os.path.basename(xyz_file))
        if molecule_name in reference_graphs:
            logging.debug(f"Found reference graph for: {molecule_name}")
            ref_graph = reference_graphs[molecule_name]
            ref_graph = update_graph_with_elements(ref_graph)
            add_element_pairs_to_edges(ref_graph)
            structures, comments = read_xyz_file(xyz_file)

            successful_structures = []
            failed_structures = []

            for index, (atom_types, coordinates) in enumerate(structures):
                target_graph = create_networkx_graph(
                    coordinates, atom_types, bond_data_stretched, species_dict, box_lengths)
                add_element_pairs_to_edges(target_graph)
                reordered_atom_types, reordered_coordinates = reorder_structure_to_match_reference(
                    ref_graph, target_graph, atom_types, coordinates)

                if reordered_atom_types and reordered_coordinates:  # Checks if not None and not empty
                    successful_structures.append(
                        (reordered_atom_types, reordered_coordinates, comments[index]))
                    logging.info(
                        f"Structure {index} reordered and added for {molecule_name}.")
                else:
                    failed_structures.append(
                        (atom_types, coordinates, comments[index]))
                    logging.warning(
                        f"Structure {index} could not be reordered for {molecule_name} and has been set aside for manual inspection.")

            if successful_structures:
                write_xyz_file(
                    f'reordered_{molecule_name}.xyz', successful_structures)
            if failed_structures:
                write_xyz_file_failed(
                    f'Broke/failed_{molecule_name}.xyz', failed_structures)
        else:
            logging.warning(f"No reference graph found for {molecule_name}")


directory = '/red/roitberg/nick_analysis/Extracts/Others/XYZs'
process_files(directory)

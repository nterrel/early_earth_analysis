import networkx as nx
import numpy as np
import ase
import logging
import pickle
import pandas as pd
import sys

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# NOTE: To do: if any i,j coordinates are more than n_atoms*max_bond_data apart, set structure aside (with comment line) for manual check

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

mol_data = pd.read_parquet('molecule_data.pq')
print(mol_data[mol_data['name'] == 'Alanine'])
serialized_graph = mol_data[mol_data['name'] == 'Alanine']['graph'][0]
standard_graph = pickle.loads(serialized_graph)
ref_atom_types = [species_dict[attrs['atomic_number']]
                  for _, attrs in standard_graph.nodes(data=True)]
print(ref_atom_types)
for node, data in standard_graph.nodes(data=True):
    atomic_num = data['atomic_number']
    # Update the node data to include 'element'
    data['element'] = species_dict[atomic_num]
    # Optionally, remove the 'atomic_number' field to avoid confusion
    # del data['atomic_number']

# sys.exit()


def read_xyz_file(filename: str):
    """_summary_

    Args:
        filename (_type_): _description_

    Returns:
        _type_: _description_
    """
    with open(filename, 'r') as file:
        # Remove empty lines and strip whitespace
        lines = [line.strip() for line in file if line.strip()]

    structures = []
    comments = []
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
    return structures, comments


def pbc_distance(pos1, pos2, box_lengths):
    # Calculate distance vector considering periodic boundaries
    delta = np.abs(pos1 - pos2)
    delta = np.where(delta > 0.5 * box_lengths, delta - box_lengths, delta)
    # Compute the Euclidean distance with the adjusted delta
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
            # logging.debug(f"Pre-check bond between atoms {i} ({elem_i}) and {j} ({elem_j}) with distance {dist}. Pair key: {pair_key}")
            if pair_key in bond_data_stretched and dist <= bond_data_stretched[pair_key]:
                # logging.debug(f"Creating bond between {species_dict[atomic_nums[i]]}-{species_dict[atomic_nums[j]]} with distance {dist} and threshold {bond_data_stretched[pair_key]}")
                G.add_edge(i, j)
    return G


# Function to add 'element_pair' attribute to graph edges
def add_element_pairs_to_edges(graph):
    for (node1, node2) in graph.edges():
        element1 = graph.nodes[node1]['element']
        element2 = graph.nodes[node2]['element']
        # Sort the elements alphabetically before creating the label
        edge_label = '-'.join(sorted([element1, element2]))
        graph.edges[node1, node2]['element_pair'] = edge_label


def reorder_structure_to_match_reference(ref_graph, target_graph, target_atom_types, target_coordinates):
    logging.debug("Starting isomorphism check and reordering process.")
    if nx.is_isomorphic(ref_graph, target_graph):
        edge_match = nx.isomorphism.categorical_edge_match(
            'element_pair', default='')
        node_match = nx.isomorphism.categorical_node_match('element', '')
        matcher = nx.isomorphism.GraphMatcher(
            ref_graph,
            target_graph,
            node_match=node_match,
            edge_match=edge_match)

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


def compare_graph_bonds(ref_graph, target_graph, ref_atom_types, target_atom_types):
    # Extracting bonds and their atom types for the reference graph
    ref_bonds = set()
    for u, v in ref_graph.edges():
        atom_u = ref_atom_types[u]
        atom_v = ref_atom_types[v]
        bond = tuple(sorted([atom_u, atom_v]))
        ref_bonds.add(bond)

    # Extracting bonds and their atom types for the target graph
    target_bonds = set()
    for u, v in target_graph.edges():
        atom_u = target_atom_types[u]
        atom_v = target_atom_types[v]
        bond = tuple(sorted([atom_u, atom_v]))
        target_bonds.add(bond)

    # Identifying missing bonds in the target graph
    missing_bonds = ref_bonds - target_bonds

    # Logging the results
    print("Reference Graph Bonds:", ref_bonds)
    print("Target Graph Bonds:", target_bonds)
    print("Missing Bonds in Target Graph:", missing_bonds)


add_element_pairs_to_edges(standard_graph)

structures, comments = read_xyz_file('all_alanines.xyz')

# ref_atom_types, ref_coordinates = structures[0]
# standard_graph = create_networkx_graph(ref_coordinates, ref_atom_types, bond_data_stretched, species_dict, box_lengths)
# add_element_pairs_to_edges(standard_graph)

reordered_structures = []
successful_comments = []
failed_structures = []
failed_comments = []
count = 0

# FIX INDEXING IF YOU FIGURE OUT HOW TO MATCH FIRST STRUCTURE
for index, (atom_types, coordinates) in enumerate(structures[1:], start=1):
    logging.debug(f"Processing structure {index}/{len(structures)}")
    target_graph = create_networkx_graph(
        coordinates, atom_types, bond_data_stretched, species_dict, box_lengths)
    add_element_pairs_to_edges(target_graph)
    # compare_graph_bonds(standard_graph, target_graph, ref_atom_types, atom_types)
    reordered_atom_types, reordered_coordinates = reorder_structure_to_match_reference(
        standard_graph, target_graph, atom_types, coordinates)
    if reordered_atom_types and reordered_coordinates:  # Checks if not None and not empty
        reordered_structures.append(
            (reordered_atom_types, reordered_coordinates, comments[index]))
        logging.info(f"Structure {index} reordered and added.")
    else:
        # Collect failed structures and their comments
        failed_structures.append((atom_types, coordinates, comments[index]))
        logging.warning(
            f"Structure {index} could not be reordered and has been set aside for manual inspection.")
    # break

write_xyz_file('reordered_alanines.xyz', reordered_structures)
write_xyz_file_failed('failed_ala_coord_remap.xyz', failed_structures)

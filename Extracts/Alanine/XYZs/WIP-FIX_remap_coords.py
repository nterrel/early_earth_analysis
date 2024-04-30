import networkx as nx
import numpy as np
from networkx.algorithms import isomorphism
import ase

species_dict = {1: "H", 6: "C", 7: "N", 8: "O"}

bond_data = {
    "HH": 0.75, "HC": 1.09, "HN": 1.01, "HO": 0.96,
    "CC": 1.54, "CN": 1.43, "CO": 1.43,
    "NN": 1.45, "NO": 1.47, "OO": 1.48,
}
stretch_buffer = 0.2
bond_data_stretched = {k: v + stretch_buffer for k, v in bond_data.items()}

def create_networkx_graph(coordinates, atom_types, bond_data_stretched, species_dict):
    G = nx.Graph()
    atomic_nums = [ase.symbols.symbols2numbers(atom)[0] for atom in atom_types]
    
    for i, (x, y, z) in enumerate(coordinates):
        atomic_num = atomic_nums[i]
        G.add_node(i, element=species_dict[atomic_num], atomic_num=atomic_num, pos=(x, y, z))
    
    for i, coord1 in enumerate(coordinates):
        for j, coord2 in enumerate(coordinates):
            if i >= j:
                continue
            dist = np.linalg.norm(np.array(coord1) - np.array(coord2))
            pair_key = ''.join(sorted([species_dict[atomic_nums[i]], species_dict[atomic_nums[j]]]))
            if pair_key in bond_data_stretched and dist <= bond_data_stretched[pair_key]:
                G.add_edge(i, j)
    return G

def reorder_structure_to_match_reference(ref_graph, target_graph):
    matcher = isomorphism.GraphMatcher(ref_graph, target_graph,
                                       node_match=isomorphism.categorical_node_match('element', 'H'))
    if matcher.is_isomorphic():
        mapping = matcher.mapping  # Mapping from target to ref
        reordered = {v: target_graph.nodes[data]['pos'] for v, data in mapping.items()}
        return [reordered[i] for i in range(len(reordered))]  # Reordered coordinates
    return None  # If not isomorphic, return None or handle as needed

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

structures = read_xyz_file('all_alanines.xyz')
standard_atom_types, standard_coordinates = structures[0]
standard_graph = create_networkx_graph(standard_coordinates, standard_atom_types, bond_data_stretched, species_dict)

reordered_structures = [structures[0]]  # Include the standard as the first structure

for atom_types, coordinates in structures[1:]:
    target_graph = create_networkx_graph(coordinates, atom_types, bond_data_stretched, species_dict)  # Add missing arguments here
    reordered_coords = reorder_structure_to_match_reference(standard_graph, target_graph)
    if reordered_coords:
        reordered_structures.append((atom_types, reordered_coords))

def write_xyz_file(filename, structures):
    with open(filename, 'w') as file:
        for atom_types, coords in structures:
            file.write(f"{len(atom_types)}\n")
            file.write("Reordered structure\n")
            for atom, (x, y, z) in zip(atom_types, coords):
                file.write(f"{atom} {x} {y} {z}\n")

write_xyz_file('reordered_alanines.xyz', reordered_structures)

#NOTE: This file doesn't work how i'd like it to, the 'reorganized' coords do not have the same ordering

import numpy as np
import os

bond_data = {
    "HH": 0.75,
    "HC": 1.09,
    "HN": 1.01,
    "HO": 0.96,
    "CC": 1.54,
    "CN": 1.43,
    "CO": 1.43,
    "NN": 1.45,
    "NO": 1.47,
    "OO": 1.48,
}

def read_xyz_file(file_path):
    frames = []
    with open(file_path, 'r') as file:
        while True:
            line = file.readline()
            if not line:
                break  # End of file
            num_atoms = int(line.strip())  # Number of atoms
            comment_line = file.readline().strip()  # Frame comment
            frame_number = int(comment_line.split()[1].rstrip(':'))  # Extract frame number, remove trailing ':'
            
            atoms = []
            coordinates = []
            for _ in range(num_atoms):
                atom_line = file.readline().strip()
                parts = atom_line.split()
                atoms.append(parts[0])
                coordinates.append([float(part) for part in parts[1:]])
                
            frames.append((frame_number, atoms, np.array(coordinates)))
    return frames


def compute_connectivity_matrix(atoms, coordinates, bond_data, buffer=0.15):
    num_atoms = len(atoms)
    connectivity_matrix = np.zeros((num_atoms, num_atoms), dtype=int)

    for i in range(num_atoms):
        for j in range(i+1, num_atoms):
            bond_key = atoms[i] + atoms[j]
            if bond_key in bond_data:
                bond_length = bond_data[bond_key] + buffer
                distance = np.linalg.norm(coordinates[i] - coordinates[j])
                if distance <= bond_length:
                    connectivity_matrix[i][j] = 1
                    connectivity_matrix[j][i] = 1
    return connectivity_matrix

def rearrange_atoms(atoms, coordinates, connectivity_matrix):
    num_atoms = len(atoms)
    visited = [False] * num_atoms
    reordered_atoms = []
    reordered_coord = []
    def dfs(node):
        visited[node] = True
        reordered_atoms.append(atoms[node])
        reordered_coord.append(coordinates[node])

        for neighbor in range(num_atoms):
            if connectivity_matrix[node][neighbor] == 1 and not visited[neighbor]:
                dfs(neighbor)
    
    for i in range(num_atoms):
        if not visited[i]:
            dfs(i)

    return reordered_atoms, np.array(reordered_coord)


def save_xyz_file(file_obj, frame_number, atoms, coordinates):
    num_atoms = len(atoms)
    file_obj.write(f"{num_atoms}\n")
    file_obj.write(f"Frame {frame_number}: XYZ file generated from rearranged coordinates\n")
    for atom, coord in zip(atoms, coordinates):
        file_obj.write(f"{atom} {' '.join(map(str, coord))}\n")


# Define the directory and file name
directory = "/red/roitberg/nick_analysis/Ala_df/XYZs/"

for filename in os.listdir(directory):
    if filename.endswith(".xyz") and filename.startswith("ala_"):
        # Read the XYZ frames from the file
        file_path = os.path.join(directory, filename)
        frames = read_xyz_file(file_path)
        
        # Prepare output file name
        output_filename = f"ordered_{filename}"

        # Open the output file
        output_file_path = os.path.join(directory, output_filename)
        with open(output_file_path, 'w') as output_file:
            # Iterate over frames in the current XYZ file
            for frame_number, atoms, coordinates in frames:
                connectivity_matrix = compute_connectivity_matrix(atoms, coordinates, bond_data)
                reordered_atoms, reordered_coordinates = rearrange_atoms(atoms, coordinates, connectivity_matrix)
                
                save_xyz_file(output_file, frame_number, reordered_atoms, reordered_coordinates)
                output_file.write("\n")  # Separate frames with an empty line
            print(f"Rearranged coordinates saved to {output_file_path}")



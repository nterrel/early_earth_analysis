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
def compute_connectivity_matrix(atoms, coordinates, bond_data, buffer=0.2):
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

def read_xyz_and_compute_connectivity(file_path, bond_data):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    frames = []  # List to hold all frames
    i = 0  # Index to track our position in the file
    while i < len(lines):
        num_atoms = int(lines[i].strip())
        frame_number = int(lines[i+1].split()[1].rstrip(':'))  # Extract frame number
        i += 2  # Move past the atom count and frame number lines

        atoms = []
        coordinates = []
        for _ in range(num_atoms):
            parts = lines[i].split()
            atoms.append(parts[0])
            coordinates.append([float(part) for part in parts[1:4]])
            i += 1  # Move to the next line/atom

        connectivity_matrix = compute_connectivity_matrix(atoms, np.array(coordinates), bond_data)
        frames.append((frame_number, atoms, coordinates, connectivity_matrix))

    return frames


def map_atoms_to_standard(atoms, standard_atoms, connectivity_matrix, standard_connectivity_matrix):
    mapping = [-1] * len(standard_atoms)  # Initialize mapping with -1 to detect unmapped atoms
    
    # Attempt to match based on connectivity patterns, not just direct comparison
    for i, std_atom in enumerate(standard_atoms):
        for j, atom in enumerate(atoms):
            if std_atom == atom:
                # Compare connectivity patterns; more sophisticated than direct np.array_equal
                if np.sum(connectivity_matrix[j] == standard_connectivity_matrix[i]) > 0:
                    if j not in mapping:  # Ensure it's not already mapped
                        mapping[i] = j
                        break
    
    # Check for any unmapped atoms (indicated by -1) and attempt to resolve
    for i, mapped_index in enumerate(mapping):
        if mapped_index == -1:
            print(f"Warning: Unmapped atom {standard_atoms[i]} at index {i}.")
    
    return mapping


def rearrange_atoms(atoms, coordinates, mapping):
    reordered_atoms = [atoms[i] for i in mapping]
    reordered_coordinates = np.array([coordinates[i] for i in mapping])
    return reordered_atoms, reordered_coordinates

def save_xyz_file(file_obj, frame_number, atoms, coordinates):
    num_atoms = len(atoms)
    file_obj.write(f"{num_atoms}\n")
    file_obj.write(f"Frame {frame_number}: XYZ file generated from rearranged coordinates\n")
    for atom, coord in zip(atoms, coordinates):
        file_obj.write(f"{atom} {' '.join(map(str, coord))}\n")


# Main processing
directory = "/red/roitberg/nick_analysis/Ala_df/XYZs"
standard_file = None  # Define the path to your standard file if known, or set to None to use the first file found

for filename in sorted(os.listdir(directory)):
    if filename.endswith(".xyz") and filename.startswith("ala_"):
        file_path = os.path.join(directory, filename)

        # Process the standard file or use the first file as standard
        #if standard_frames is None:
        standard_frames = read_xyz_and_compute_connectivity(file_path, bond_data)
        #    continue  # Skip to the next file after setting the standard

        # For all other files, process each frame
        frames = read_xyz_and_compute_connectivity(file_path, bond_data)
        output_filename = f"ordered_{filename}"
        output_file_path = os.path.join(directory, output_filename)
        with open(output_file_path, 'w') as output_file:
            for frame_number, atoms, coordinates, connectivity_matrix in frames:
                # Assume first frame of standard as reference for simplicity; adjust if needed
                std_frame_number, std_atoms, std_coordinates, std_connectivity_matrix = standard_frames[0]
                mapping = map_atoms_to_standard(atoms, std_atoms, connectivity_matrix, std_connectivity_matrix)
                reordered_atoms, reordered_coordinates = rearrange_atoms(atoms, coordinates, mapping)
                
                save_xyz_file(output_file, frame_number, reordered_atoms, reordered_coordinates)

        print(f"Processed {filename}, reordered coordinates saved to {output_file_path}")



import pandas as pd
import math
import time
from top_loader import load_topology

# Start the timer to measure total runtime
start_timer = time.time()

# Load the molecular topology only once, as it's used for all files
top = load_topology('/red/roitberg/nick_analysis/traj_top_0.0ns.h5')

# Measure the time taken to load topology
top_timer = time.time()
print(f"Topology loaded in {top_timer - start_timer} seconds.")

# Function to get atom types from atom indices using a topology
def get_atom_types(atom_indices, topology):
    return [topology.atom(index).name for index in atom_indices]

# Function to convert coordinates from nanometers to angstroms
def convert_to_angstrom(coordinates):
    return [[x * 10 for x in coordinate] for coordinate in coordinates]

def process_single_file(file_path):
    try:
        df = pd.read_hdf(file_path)
    except FileNotFoundError:
        print(f"File {file_path} does not exist. Exiting...")
        return
    
    print(f"Processing dataframe: {file_path}")
    xyz_file_name = f"/red/roitberg/nick_analysis/96atom.xyz"
    
    # Open the file in append mode to add each new set of coordinates
    with open(xyz_file_name, 'a') as file:
        for index, row in df.iterrows():
            atom_indices = row['atom_indices']
            atom_types = get_atom_types(atom_indices, top)
            coordinates = row['coordinates']
            coordinates_angstrom = convert_to_angstrom(coordinates)
            frame_number = row['frame']

            file.write(f"{len(atom_types)}\n")
            file.write(f"Frame {frame_number}: XYZ file generated from coordinates\n")
            for atom, coord in zip(atom_types, coordinates_angstrom):
                file.write(f"{atom} {coord[0]:.6f} {coord[1]:.6f} {coord[2]:.6f}\n")

# Define the file path directly
file_path = '/red/roitberg/nick_analysis/96_atom_coords.h5'
process_single_file(file_path)

# Record end time and print total runtime
finish_timer = time.time()
print(f"Time to run the whole script: {finish_timer - start_timer} seconds.")

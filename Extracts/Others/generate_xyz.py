import pandas as pd
import os
import glob
import re
import time
from top_loader import load_topology

# Start the timer to measure total runtime
start_timer = time.time()

# Load the molecular topology only once, as it's used for all files
top = load_topology('/red/roitberg/nick_analysis/traj_top_0.0ns.h5')

# Measure the time taken to load topology
top_timer = time.time()
print(f"Topology loaded in {top_timer - start_timer} seconds.")

def get_atom_types(atom_indices, topology):
    return [topology.atom(index).name for index in atom_indices]

def convert_to_angstrom(coordinates):
    return [[x * 10 for x in coordinate] for coordinate in coordinates]

def sort_files(files):
    return sorted(files, key=lambda x: float(re.findall(r"_([\d.]+)ns.h5", x)[0]))

def process_files(directory):
    file_pattern = os.path.join(directory, 'coord_df_*.h5')
    files = glob.glob(file_pattern)
    sorted_files = sort_files(files)
    for file_name in sorted_files:
        try:
            df = pd.read_hdf(file_name)
        except FileNotFoundError:
            print(f"File {file_name} does not exist. Skipping...")
            continue

        print(f"Processing dataframe: {file_name}")
        ns_value = re.findall(r"_([\d.]+)ns", file_name)[0]  # Extract time from filename
        # Group by molecule name and create separate files for each group
        grouped = df.groupby('name')
        for name, group in grouped:
            xyz_file_name = f"/red/roitberg/nick_analysis/XYZs/{name}_{ns_value}ns.xyz"
            with open(xyz_file_name, 'a') as file:
                for index, row in group.iterrows():
                    atom_indices = row['atom_indices']
                    atom_types = get_atom_types(atom_indices, top)
                    coordinates = row['coordinates']
                    coordinates_angstrom = convert_to_angstrom(coordinates)
                    frame_number = row['frame']

                    file.write(f"{len(atom_types)}\n")
                    file.write(f"Frame {frame_number}: XYZ file generated from coordinates\n")
                    for atom, coord in zip(atom_types, coordinates_angstrom):
                        file.write(f"{atom} {coord[0]:.6f} {coord[1]:.6f} {coord[2]:.6f}\n")

directory = '/red/roitberg/nick_analysis/HDF_coord'
process_files(directory)

finish_timer = time.time()
print(f"Time to run the whole script: {finish_timer - start_timer} seconds.")

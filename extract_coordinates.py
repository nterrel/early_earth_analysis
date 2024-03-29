import pandas as pd
import mdtraj as md
import os
import sys
import cProfile
import re
import timeit
import numpy as np
from top_loader import load_topology

"""
This script extracts molecular coordinates from trajectory files for molecules identified in simulations
and stores these coordinates in a pandas DataFrame. The DataFrame is then saved in an HDF5 format.
Each molecule's original and updated indices, along with their coordinates, are maintained for reference.
"""

start_time = timeit.default_timer()

parquet_dir = '/red/roitberg/nick_analysis/split_parquets'
top_file = '/red/roitberg/nick_analysis/traj_top_0.0ns.h5'
print("Loading topology from:", top_file)
topology = load_topology(top_file)

topology_timer = timeit.default_timer()
print(f"Topology loaded in {topology_timer - start_time} seconds")

def extract_coordinates_for_frame(traj_file, topology, frame_num, df):
    """
    Extracts coordinates for all molecules in a given frame from a trajectory file.
    
    Parameters:
    - traj_file: Path to the trajectory file.
    - topology: The topology object associated with the trajectory.
    - frame_num: The frame number to extract coordinates for.
    - df: The pandas DataFrame containing molecule information.
    
    Returns:
    - coord_dict: A dictionary mapping molecule indices to their coordinates.
    """
    frame_time_start = timeit.default_timer()
    frame = md.load_frame(traj_file, index=frame_num, top=topology)
    frame_time_loaded = timeit.default_timer()
    print(f'Time to load frame {frame_num} of trajectory: {frame_time_loaded - frame_time_start}')
    coord_dict = {}
    nan_count = 0
    filtered_df = df[df['local_frame'] == frame_num]
    for index, row in filtered_df.iterrows():
        row_timer_start = timeit.default_timer()
        try:
            print('Row, atom indices', row['atom_indices'])
            coordinates = frame.xyz[0, row['atom_indices']]
            coord_dict[index] = coordinates
        except Exception as e:
            print(f"Error extracting coordinates for index {index}: {e}")
            nan_count += 1
            print(f'NaN count increased to {nan_count}. Coordinates that failed to append:\n', coordinates)
            coord_dict[index] = np.nan
        row_timer_finish = timeit.default_timer()
        print(f"Time taken for looping over one row: {row_timer_finish - row_timer_start} seconds")
    return coord_dict


separate_dfs = {}

for filename in os.listdir(parquet_dir):
    if filename.endswith('.pq'):
        match = re.search(r'df_floor_time_(\d+\.\d+)\.pq', filename)
        if match:
            floor_time = float(match.group(1))
            df = pd.read_parquet(os.path.join(parquet_dir, filename))
            df['original_index'] = df.index
            df.reset_index(inplace=True, drop=True)
            separate_dfs[floor_time] = df

def main():
    global_start = timeit.default_timer()
    for floor_time, df in separate_dfs.items():
        df['coordinates'] = pd.Series(dtype='object')
        unique_frames = df['local_frame'].unique()
        for frame_num in unique_frames:
            traj_file = df[df['local_frame'] == frame_num]['dcd_file'].iloc[0]
            coord_dict = extract_coordinates_for_frame(traj_file, topology, frame_num, df)
            for index, coords in coord_dict.items():
                try:
                    df.at[index, 'coordinates'] = coord_dict[index]
                except Exception as e:
                    print(f"Error inserting coordinates at index {index}: {e}")
                    print(f"Shape of coordinates being inserted: {coord_dict[index].shape if coord_dict[index] is not np.nan else 'NaN'}")
        df.to_hdf(f"/red/roitberg/nick_analysis/split_parquets/coord_df_{floor_time}.h5", key='df', mode='w')
    global_end = timeit.default_timer()
    print(f"Total time for the script: {global_end - global_start}")

if __name__ == "__main__":
    cProfile.run('main()', '/blue/roitberg/nterrel/extract_coord_profiling_results.prof')

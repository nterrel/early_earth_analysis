import pandas as pd
import mdtraj as md
import os
import sys
import cProfile
import re
import timeit
import numpy as np
from top_loader import load_topology

start_time = timeit.default_timer()

parquet_dir = '/red/roitberg/nick_analysis/split_parquets'
top_file = '/red/roitberg/nick_analysis/traj_top_0.0ns.h5'
topology = load_topology(top_file)

topology_timer = timeit.default_timer()
print(f"Topology loaded in {topology_timer - start_time} seconds")

def extract_coordinates_for_frame(traj_file, topology, frame_num, df):
    frame_time_start = timeit.default_timer()
    frame = md.load_frame(traj_file, index=frame_num, top=topology)
    frame_time_loaded = timeit.default_timer()
    print(f'Time to load frame {frame_num} of trajectory: {frame_time_loaded - frame_time_start}')
    coord_dict = {}
    nan_count = 0
    filtered_df = df[df['local_frame'] == frame_num]
    for index, row in filtered_df.iterrows():
        row_timer_start = timeit.default_timer()
        print('index:', index)
        print('row:\n', row)
        try:
            print('Row, atom indices', row['atom_indices'])
            coordinates = frame.xyz[0, row['atom_indices']]
            coord_dict[index] = coordinates
        except Exception as e:
            print(f"Error extracting coordinates for index {index}: {e}")
            nan_count += 1
            print(f'NaN count increased to {nan_count}. Coordinates that failed to append:\n', coordinates)
            coord_dict[index] = np.nan
        # NOTE: The above line caused an error (adding object to dataframe), so i converted to list, trying that? 
        # BUT if that doesn't work, maybe try deleting the below line, and save to a .h5 instead of .pq?
        # Alternatively could flatten the arrays and then reshape later, but that is complex and i'm 100% sure i'd mess it up

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
            df = df.reset_index(inplace=True, drop=False)
            separate_dfs[floor_time] = df

def main():
    global_start = timeit.default_timer()
    for floor_time, df in separate_dfs.items():
        unique_frames = df['local_frame'].unique()
        for frame_num in unique_frames:
            traj_file = df[df['local_frame'] == frame_num]['dcd_file'].iloc[0]
            coord_dict = extract_coordinates_for_frame(traj_file, frame_num, df)
            print(coord_dict)
            for index, coords in coord_dict.items():
                try:
                    breakpoint()
                    df.at[index, 'coordinates'] = coord_dict[index]
                except Exception as e:
                    print(f"Error inserting coordinates at index {index}: {e}")
                    print(f"Shape of coordinates being inserted: {coord_dict[index].shape if coord_dict[index] is not np.nan else 'NaN'}")
            break

        df.to_hdf(f"/red/roitberg/nick_analysis/split_parquets/coord_df_{floor_time}.h5", key='df', mode='w')
        break
    global_end = timeit.default_timer()
    print(f"Total time for the script: {global_end - global_start}")

if __name__ == "__main__":
    cProfile.run('main()', '/blue/roitberg/nterrel/extract_coord_profiling_results.prof')

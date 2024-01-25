import pandas as pd
import mdtraj as md
import os
import sys
import cProfile
import re
import timeit
import numpy as np

start_time = timeit.default_timer()

def extract_coordinates_for_frame(traj_file, frame_num, df):
    frame_time_start = timeit.default_timer()
    frame = md.load_frame(traj_file, index=frame_num, top=top_file)
    frame_time_loaded = timeit.default_timer()
    print(f'Time to load frame {frame_num} of trajectory: {frame_time_loaded - frame_time_start}')
    coord_dict = {}
    nan_count = 0
    for index, row in df[df['local_frame'] == frame_num].iterrows():
        row_timer_start = timeit.default_timer()
        print('index:', index)
        print('row:\n', row)
        try:
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

parquet_dir = '/red/roitberg/nick_analysis/split_parquets'
top_file = '/blue/roitberg/apps/lammps-ani/examples/early_earth/data/mixture_22800000.pdb'

separate_dfs = {}

for filename in os.listdir(parquet_dir):
    if filename.endswith('.pq'):
        match = re.search(r'df_floor_time_(\d+\.\d+)\.pq', filename)
        if match:
            floor_time = float(match.group(1))
            df = pd.read_parquet(os.path.join(parquet_dir, filename))
            separate_dfs[floor_time] = df

def main():
    global_start = timeit.default_timer()
    for floor_time, df in separate_dfs.items():
        unique_frames = df['local_frame'].unique()
        for frame_num in unique_frames:
            traj_file = df[df['local_frame'] == frame_num]['dcd_file'].iloc[0]
            coord_dict = extract_coordinates_for_frame(traj_file, frame_num, df)
            for index in coord_dict:
                try:
                    df.at[index, 'coordinates'] = coord_dict[index]
                except Exception as e:
                    print(f"Error inserting coordinates at index {index}: {e}")
                    print(f"Shape of coordinates being inserted: {coord_dict[index].shape if coord_dict[index] is not np.nan else 'NaN'}")
            break

        # NOTE: If saving to h5 instead of pq, multi-dim NP array can be saved directly
        #   Trying that last today (1/24/24) since I keep hitting errors 

        df.to_hdf(f"/red/roitberg/nick_analysis/split_parquets/coord_df_{floor_time}.h5", key='df', mode='w')
        break
    global_end = timeit.default_timer()
    print(f"Total time for the script: {global_end - global_start}")

if __name__ == "__main__":
    cProfile.run('main()', '/blue/roitberg/nterrel/extract_coord_profiling_results.prof')

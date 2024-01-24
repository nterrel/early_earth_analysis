import pandas as pd
import mdtraj as md
import os
import sys
import cProfile
import re

def extract_coordinates_for_frame(traj_file, frame_num, df):
    frame = md.load_frame(traj_file, index=frame_num, top=top_file)
    coord_data = []

    for index, row in df[df['local_frame'] == frame_num].iterrows():
        coordinates = frame.xyz[0, row['atom_indices']]
        # NOTE: The above line caused an error (adding object to dataframe), so i converted to list, trying that? 
        # BUT if that doesn't work, maybe try deleting the below line, and save to a .h5 instead of .pq?
        # Alternatively could flatten the arrays and then reshape later, but that is complex and i'm 100% sure i'd mess it up
                
        #coord_list = coordinates.tolist()
        
        coord_data.append({'index': index, 'coordinates': coord_list})

    return pd.DataFrame(coord_data).set_index('index')

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
    for floor_time, df in separate_dfs.items():
        unique_frames = df['local_frame'].unique()
        for frame_num in unique_frames:
            traj_file = df[df['local_frame'] == frame_num]['dcd_file'].iloc[0]
            coord_df = extract_coordinates_for_frame(traj_file, frame_num, df)
            df = df.merge(coord_df, left_index=True, right_index=True, how='left')
            break

        # NOTE: If saving to h5 instead of pq, multi-dim NP array can be saved directly
        #   Trying that last today (1/24/24) since I keep hitting errors 

        df.to_hdf(f"/red/roitberg/nick_analysis/split_parquets/coord_df_{floor_time}.h5", key='df', mode='w')
        break

if __name__ == "__main__":
    cProfile.run('main()', '/blue/roitberg/nterrel/extract_coord_profiling_results.prof')

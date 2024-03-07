import pandas as pd
import mdtraj as md
from top_loader import load_topology
import numpy as np
from tqdm.auto import tqdm
import re
import os

def extract_and_assign_coordinates(row, topology):
    if pd.notnull(row['coordinates']):
        return row['coordinates']
    try:
        frame = md.load_frame(row['dcd_file'], index=row['local_frame'], top=topology)
        coordinates = frame.xyz[0, row['atom_indices']]
        return coordinates
    except Exception as e:
        print(f"Error extracting coordinates for molecule at index {row.name}: {e}")
        return np.nan

def process_group(group, topology):
    tqdm.pandas(desc=f"Extracting coordinates for {group.name}")
    group['coordinates'] = group.progress_apply(lambda row: extract_and_assign_coordinates(row, topology), axis=1)
    return group

def main(df, topology):
    grouped = df.groupby('dcd_file')
    for dcd_file, group in tqdm(grouped, desc="DCD Files"):
        ns_timestamp = re.search(r'(\d+\.\d+)ns\.dcd$', dcd_file)
        if ns_timestamp:
            ns_str = ns_timestamp.group(1)
        else:
            ns_str = 'unknown'
        output_file_name = f'/red/roitberg/nick_analysis/Ala_df/ala_coord_{ns_str}ns.h5'
        
        if os.path.exists(output_file_name):
            print(f"File {output_file_name} already exists. Skipping.")
            continue  # Skip to the next group if the file exists
        
        processed_group = process_group(group, topology)
        processed_group.to_hdf(output_file_name, key='df', mode='w')
        print(f"Saved processed group for {dcd_file} to {output_file_name}")

if __name__ == "__main__":
    df = pd.read_parquet('/red/roitberg/nick_analysis/alanine_df_with_dcd.pq')
    if 'coordinates' not in df.columns:
        df['coordinates'] = np.nan
    topology = load_topology('/red/roitberg/nick_analysis/traj_top_0.0ns.h5')
    main(df, topology)


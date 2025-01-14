import pandas as pd
import mdtraj as md
from top_loader import load_topology
import numpy as np
from tqdm.auto import tqdm
import re
import os

dcd_file = '96atom_quench.dcd'

atom_indices = np.array([  121726,   328013,   329333,   333931,   426576,  1069336,
        1104757,  1925833,  2452019,  2936578,  3042479,  3677647,
        3966768,  4203970,  4304990,  4682274,  5703919,  6094422,
        7677038,  7889084,  8008110,  8190732,  8315664,  8379316,
        8410218,  8744796,  9013398,  9175330,  9213388,  9382444,
        9634982,  9659571,  9745826, 10147442, 10190666, 10327701,
       10681733, 10728413, 10781077, 10934138, 11272590, 12231308,
       12312119, 12610587, 13011578, 13066615, 13346330, 13588793,
       13656449, 13699759, 13722718, 14070307, 14304768, 14897392,
       14962768, 15808635, 16075875, 16090790, 16209552, 16418643,
       16611839, 16957440, 17339927, 17430895, 17497280, 17544910,
       17803535, 17887915, 17889200, 18162385, 18635867, 18636205,
       18757550, 18894414, 18903322, 19011181, 19041380, 19121605,
       19212210, 19320956, 20083200, 20164560, 20181060, 20880891,
       21022310, 21097511, 21416546, 21532478, 21571845, 21655051,
       22132837, 22191165, 22221211, 22279758, 22552643, 22777387])

def extract_and_assign_coordinates(row, topology):
    if pd.notnull(row['coordinates']):
        return row['coordinates']
    try:
        frame = md.load_frame(dcd_file, index=0, top=topology)
        #atom_indices_flat = np.concatenate(atom_indices).astype(int)
        coordinates = frame.xyz[0, atom_indices]

        return coordinates
    except Exception as e:
        print(f"Error extracting coordinates for molecule at index {row.name}: {e}")
        return np.nan

def process_group(group, topology):
    tqdm.pandas(desc=f"Extracting coordinates for {group.name}")
    group['coordinates'] = group.progress_apply(lambda row: extract_and_assign_coordinates(row, topology), axis=1)
    return group
def main(df, topology):
    
    output_file_name = f'/red/roitberg/nick_analysis/96_atom_quench_coords.h5'
    
    #if os.path.exists(output_file_name):
    #    print(f"File {output_file_name} already exists. Skipping.")
    #    return  # Exit the function if the file exists

    # Process the single row as if it were a group
    processed_group = process_group(df, topology)
    processed_group.to_hdf(output_file_name, key='df', mode='w')
    print(f"Saved processed group to {output_file_name}")


if __name__ == "__main__":
    df = pd.read_parquet('2024-09-05-173918.390832_256780_quench_seg0020of0021_molecule.pq')
    if 'coordinates' not in df.columns:
        df['coordinates'] = np.nan
    topology = load_topology('/red/roitberg/nick_analysis/traj_top_0.0ns.h5')
    main(df, topology)


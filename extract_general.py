import pandas as pd
import mdtraj as md
from top_loader import load_topology
import numpy as np
from tqdm.auto import tqdm
import re
import os
from multiprocessing import Pool, cpu_count
import psutil


def log_system_usage():
    process = psutil.Process(os.getpid())
    memory_use = process.memory_info().rss / (1024 * 1024)  # memory use in MB
    cpu_percent = process.cpu_percent(interval=1)  # CPU usage percentage
    print(f"Memory usage: {memory_use} MB, CPU usage: {cpu_percent}%")


def extract_and_assign_coordinates(row, topology):
    if pd.notnull(row['coordinates']):
        return row['coordinates']
    try:
        frame = md.load_frame(
            row['dcd_file'], index=row['local_frame'], top=topology)
        coordinates = frame.xyz[0, row['atom_indices']]
        return coordinates
    except Exception as e:
        print(
            f"Error extracting coordinates for molecule at index {row.name}: {e}")
        return np.nan


def process_group(group, topology):
    tqdm.pandas(desc=f"Extracting coordinates for {group.name}")
    group['coordinates'] = group.progress_apply(
        lambda row: extract_and_assign_coordinates(row, topology), axis=1)
    return group


def process_file(group_data):
    dcd_file, molecule_type, group, topology = group_data
    ns_timestamp = re.search(r'(\d+\.\d+)ns\.dcd$', dcd_file)
    ns_str = ns_timestamp.group(1) if ns_timestamp else 'unknown'
    output_file_name = f'/red/roitberg/nick_analysis/{molecule_type}_df/{molecule_type}_coord_{ns_str}ns.h5'

    if not os.path.exists(output_file_name):
        processed_group = process_group(group, topology)
        processed_group.to_hdf(output_file_name, key='df', mode='w')
        print(f"Saved processed group for {dcd_file} to {output_file_name}")
    log_system_usage()


def extract_timestamp(dcd_file):
    ns_timestamp = re.search(r'(\d+\.\d+)ns\.dcd$', dcd_file)
    return ns_timestamp.group(1) if ns_timestamp else 'unknown'


def main(df, topology):
    grouped = df.groupby(['dcd_file', 'name'])
    tasks = [(dcd_file, molecule_type, group, topology) for (dcd_file, molecule_type), group in grouped if not os.path.exists(
        f'/red/roitberg/nick_analysis/{molecule_type}_df/{molecule_type}_coord_{extract_timestamp(dcd_file)}ns.h5')]
    with Pool(processes=cpu_count()) as pool:
        pool.map(process_file, tasks)


if __name__ == "__main__":
    df = pd.read_parquet('/red/roitberg/nick_analysis/merged_mol.pq')
    if 'coordinates' not in df.columns:
        df['coordinates'] = np.nan
    topology = load_topology('/red/roitberg/nick_analysis/traj_top_0.0ns.h5')
    df = df.head(100)
    main(df, topology)

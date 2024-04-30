import pandas as pd
import mdtraj as md
from top_loader import load_topology
import numpy as np
import re
import os
import psutil
import gc
from multiprocessing import Pool, cpu_count


def log_system_usage():
    process = psutil.Process(os.getpid())
    memory_use = process.memory_info().rss / (1024 ** 2)  # memory use in MB
    cpu_percent = process.cpu_percent(interval=1)  # CPU usage percentage
    print(f"Memory usage: {memory_use} MB, CPU usage: {cpu_percent}%")


def setup_dcd_mapping(dcd_path):
    dcd_files = os.listdir(dcd_path)
    return {re.search(r'_(\d+\.\d+)ns\.dcd$', file).group(1): os.path.join(dcd_path, file)
            for file in dcd_files if re.search(r'_(\d+\.\d+)ns\.dcd$', file)}


def extract_coordinates_for_frame(group, topology):
    try:
        traj = md.load_frame(
            group['dcd_file'].iloc[0], index=group['local_frame'].iloc[0], top=topology)
        group['coordinates'] = group['atom_indices'].apply(
            lambda indices: traj.xyz[0, indices])
    except Exception as e:
        print(f"Error loading frame: {e}")
        group['coordinates'] = np.nan
    return group


def process_group(group, topology, output_file):
    processed_data = extract_coordinates_for_frame(group, topology)
    processed_data.to_parquet(output_file, index=False)
    return output_file


def process_file(file_path, topology, dcd_map, checkpoint_dir, test_limit=None):
    df = pd.read_parquet(file_path).head(test_limit)
    output_dir = checkpoint_dir
    for (dcd_file, time), group in df.groupby(['dcd_file', 'floor_time']):
        output_file = os.path.join(output_dir, f"coord_df_{time}ns.h5")
        processed_group = extract_coordinates_for_frame(group, topology)
        processed_group.to_hdf(output_file, key='data', mode='a')

    log_system_usage()
    gc.collect()


def main(topology_path, dcd_path, parquet_dir, checkpoint_dir):
    topology = load_topology(topology_path)
    dcd_map = setup_dcd_mapping(dcd_path)
    parquet_files = [os.path.join(parquet_dir, f) for f in sorted(os.listdir(parquet_dir)) if f.endswith('.pq')][:6]  # Limit to first 2 files

    with Pool(processes=cpu_count()) as pool:
        pool.starmap(process_file, [(f, topology, dcd_map, checkpoint_dir) for f in parquet_files])


if __name__ == "__main__":
    main('/red/roitberg/nick_analysis/traj_top_0.0ns.h5',
         '/red/roitberg/22M_20231222_prodrun',
         '/red/roitberg/nick_analysis/Split_parquets',
         '/red/roitberg/nick_analysis/Checkpoints')

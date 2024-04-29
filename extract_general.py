import pandas as pd
import mdtraj as md
from top_loader import load_topology
import numpy as np
import re
import os
from multiprocessing import Pool, cpu_count
import psutil
import gc
import json


def save_checkpoint(file_path, last_processed_index):
    with open(file_path, 'w') as f:
        json.dump({'last_index': last_processed_index}, f)


def load_checkpoint(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)['last_index']
    except FileNotFoundError:
        return None  # No checkpoint found


def log_system_usage():
    process = psutil.Process(os.getpid())
    memory_use = process.memory_info().rss / (1024 * 1024)  # memory use in MB
    cpu_percent = process.cpu_percent(interval=1)  # CPU usage percentage
    print(f"Memory usage: {memory_use} MB, CPU usage: {cpu_percent}%")


def setup_dcd_mapping():
    dcd_path = '/red/roitberg/22M_20231222_prodrun'
    dcd_files = os.listdir(dcd_path)
    dcd_map = {}
    for file in dcd_files:
        match = re.search(r'_(\d+\.\d+)ns\.dcd$', file)
        if match:
            timestamp = match.group(1)
            dcd_map[timestamp] = os.path.join(dcd_path, file)
    return dcd_map


def extract_and_assign_coordinates(row, topology, dcd_file):
    if pd.notnull(row['coordinates']):
        return row['coordinates']
    try:
        frame = md.load_frame(dcd_file, index=row['local_frame'], top=topology)
        coordinates = frame.xyz[0, row['atom_indices']]
        return coordinates
    except Exception as e:
        print(
            f"Error extracting coordinates for molecule at index {row.name}: {e}")
        return np.nan


def generate_coordinates(df, topology, dcd_file, start_index=0):
    for index, row in df.iloc[start_index:].iterrows():
        coordinates = extract_and_assign_coordinates(row, topology, dcd_file)
        yield index, coordinates


def process_group_with_generator(df, topology, dcd_file, output_file, start_index, checkpoint_path, batch_size=1000):
    batch = []
    for index, coordinates in generate_coordinates(df, topology, dcd_file, start_index):
        batch.append({'index': index, 'coordinates': coordinates})
        if len(batch) >= batch_size:
            pd.DataFrame(batch).to_hdf(output_file, key='df', mode='a', format='table', append=True)
            batch = []  # Reset batch
            save_checkpoint(checkpoint_path, index)  # Save checkpoint after each batch
    if batch:
        pd.DataFrame(batch).to_hdf(output_file, key='df', mode='a', format='table', append=True)  # Save any remaining batch
    gc.collect()


def process_file(file_path, topology, dcd_map, checkpoint_dir):
    try:
        dcd_file = dcd_map[re.search(r'_([\d\.]+)\.pq$', file_path).group(1)]
        checkpoint_path = os.path.join(
            checkpoint_dir, os.path.basename(file_path) + ".checkpoint")
        last_index = load_checkpoint(checkpoint_path)
        start_index = last_index + 1 if last_index is not None else 0

        df = pd.read_parquet(file_path)
        output_file = os.path.join(
            '/red/roitberg/nick_analysis/HDF_coord/', os.path.basename(file_path).replace('.pq', '.h5'))

        process_group_with_generator(
            df, topology, dcd_file, output_file, start_index)

        log_system_usage()
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")
        return None, None


def extract_timestamp(dcd_file):
    ns_timestamp = re.search(r'(\d+\.\d+)ns\.dcd$', dcd_file)
    return ns_timestamp.group(1) if ns_timestamp else 'unknown'


def main(topology, dcd_map, checkpoint_dir):
    parquet_dir = '/red/roitberg/nick_analysis/Split_parquets'
    store_dir = '/red/roitberg/nick_analysis/HDF_coord/'
    os.makedirs(store_dir, exist_ok=True)
    os.makedirs(checkpoint_dir, exist_ok=True)

    parquet_files = [os.path.join(parquet_dir, f)
                     for f in os.listdir(parquet_dir) if f.endswith('.pq')]

    with Pool(processes=cpu_count() // 2) as pool:
        pool.starmap(process_file, [
                     (f, topology, dcd_map, checkpoint_dir) for f in parquet_files])


if __name__ == "__main__":
    topology = load_topology('/red/roitberg/nick_analysis/traj_top_0.0ns.h5')
    dcd_map = setup_dcd_mapping()
    main(topology, dcd_map)

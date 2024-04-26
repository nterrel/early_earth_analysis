import pandas as pd
import mdtraj as md
from top_loader import load_topology
import numpy as np
import re
import os
from multiprocessing import Pool, cpu_count
import psutil
import gc


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


def process_group(group, topology, dcd_file):
    group['coordinates'] = group.apply(
        lambda row: extract_and_assign_coordinates(row, topology, dcd_file), axis=1)
    return group


def process_file(file_path, topology, dcd_map):
    try:
        log_system_usage()  # Log before processing starts
        df = pd.read_parquet(file_path)
        # Limit the DataFrame to the first 100 rows for the test
        # df = df.head(100)
        if 'coordinates' not in df.columns:
            df['coordinates'] = np.nan
        timestamp = re.search(r'_([\d\.]+)\.pq$', file_path).group(1)
        dcd_file = dcd_map[timestamp]
        processed_group = process_group(df, topology, dcd_file)
        log_system_usage()  # Log after processing
        return processed_group, timestamp
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")
        return None, None


def extract_timestamp(dcd_file):
    ns_timestamp = re.search(r'(\d+\.\d+)ns\.dcd$', dcd_file)
    return ns_timestamp.group(1) if ns_timestamp else 'unknown'


def main(topology, dcd_map):
    parquet_dir = '/red/roitberg/nick_analysis/Split_parquets'
    parquet_files = [os.path.join(parquet_dir, f)
                     for f in os.listdir(parquet_dir) if f.endswith('.pq')]
    # parquet_files = parquet_files[:2]
    store_dir = '/red/roitberg/nick_analysis/HDF_coord/'

    # Ensure the storage directory exists
    os.makedirs(store_dir, exist_ok=True)

    # Using multiprocessing to process files
    with Pool(processes=cpu_count() // 2) as pool:
        results = pool.starmap(
            process_file, [(f, topology, dcd_map) for f in parquet_files])

    # Saving results into separate HDF5 files
    for result, ns_str in results:
        if result is not None:
            output_file_name = f'{store_dir}coord_{ns_str}ns.h5'
            result.to_hdf(output_file_name, key='df', mode='w')
            print(f"Saved processed data for {ns_str}ns to {output_file_name}")
            del result  # Delete the DataFrame to free memory
            gc.collect()  # Collect garbage to free up memory


if __name__ == "__main__":
    topology = load_topology('/red/roitberg/nick_analysis/traj_top_0.0ns.h5')
    dcd_map = setup_dcd_mapping()
    main(topology, dcd_map)

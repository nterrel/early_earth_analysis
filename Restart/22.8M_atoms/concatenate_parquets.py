# NOTE: This script iterates over directories to find relevant analysis parquets (from original / quenched frames) and concatenates them to four final pq files (original and quenched molecule and formula parquets)

import os
import pandas as pd
import glob

base_dir = "/red/roitberg/nick_analysis/Restart/22.8M_atoms"
original_formula_ouptut = 'combined_original_formula.pq'
original_molecule_output = 'combined_original_molecule.pq'
quenched_formula_ouptut = 'combined_quenched_formula.pq'
quenched_molecule_output = 'combined_quenched_molecule.pq'


# Helper function to process parquet files
def concatenate_parquet_files(dir_pattern, file_pattern, output_file):
    dataframes = []
    # Iterate over directories matching the pattern (e.g., frame_*/)
    for directory in glob.glob(dir_pattern):
        # Extract the frame number from the directory name (e.g., frame_102584)
        frame_number = os.path.basename(directory).split('_')[1]

        # Find all parquet files matching the pattern in the directory
        for pq_file in glob.glob(os.path.join(directory, file_pattern)):
            # Read parquet file
            df = pd.read_parquet(pq_file)
            # Add frame number as a new column
            df['frame_number'] = frame_number
            # Collect the dataframe
            dataframes.append(df)

    # Concatenate all collected dataframes into one
    if dataframes:
        combined_df = pd.concat(dataframes, ignore_index=True)
        # Save the concatenated dataframe to a parquet file
        combined_df.to_parquet(output_file)
        print(f"Saved combined parquet to {output_file}")
    else:
        print(f"No files found for {dir_pattern}/{file_pattern}")


# Process original_analyze parquet files
concatenate_parquet_files(os.path.join(base_dir, 'frame_*', 'original_analyze'),
                          '*_formula.pq', original_formula_output)
concatenate_parquet_files(os.path.join(base_dir, 'frame_*', 'original_analyze'),
                          '*_molecule.pq', original_molecule_output)

# Process quench_analyze parquet files
concatenate_parquet_files(os.path.join(base_dir, 'frame_*', 'quench_analyze'),
                          '*_formula.pq', quenched_formula_output)
concatenate_parquet_files(os.path.join(base_dir, 'frame_*', 'quench_analyze'),
                          '*_molecule.pq', quenched_molecule_output)

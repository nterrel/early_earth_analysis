import os
import re
import pandas as pd
import glob

# Define paths and output files
base_dir = "/red/roitberg/nick_analysis/Restart/22.8M_atoms/random_400_frames"
original_formula_output = 'combined_original_formula.pq'
original_molecule_output = 'combined_original_molecule.pq'
quenched_formula_output = 'combined_quenched_formula.pq'
quenched_molecule_output = 'combined_quenched_molecule.pq'

# Helper function to extract the frame number using a regular expression
def extract_frame_number(directory):
    match = re.search(r'frame_(\d+)', directory)
    if match:
        return int(match.group(1))
    return None

# Helper function to process parquet files
def concatenate_parquet_files(dir_pattern, file_pattern, output_file):
    dataframes = []
    # Iterate over directories matching the pattern (e.g., frame_*/)
    for directory in glob.glob(dir_pattern):
        # Extract the frame number using the regex-based helper function
        frame_number = extract_frame_number(directory)

        # If we have a valid frame number, proceed
        if frame_number is not None:
            # Find all parquet files matching the pattern in the directory
            for pq_file in glob.glob(os.path.join(directory, file_pattern)):
                # Read parquet file
                df = pd.read_parquet(pq_file)
                # Set the 'frame' column to the extracted frame number
                df['frame'] = frame_number
                # Collect the dataframe
                dataframes.append(df)
        else:
            print(f"Skipping directory: {directory}, no valid frame number found")

    # Concatenate all collected dataframes into one
    if dataframes:
        combined_df = pd.concat(dataframes, ignore_index=True)
        combined_df = combined_df.drop(['time', 'local_frame'], axis=1)
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

import pandas as pd
import os

# Specify the directory containing the trajectory Parquet files
directory = '/red/roitberg/nick_analysis/unique_fragment_analysis'

# List to hold DataFrames
dfs = []

# Loop through files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.pq') and 'formula' in filename:
        print(filename)
        file_path = os.path.join(directory, filename)
        # Read the Parquet file
        df = pd.read_parquet(file_path)
        # Append the DataFrame to the list
        dfs.append(df)

# Concatenate all DataFrames
merged_df = pd.concat(dfs)

# Sort the DataFrame - replace 'column_name' with your specific column
sorted_df = merged_df.sort_values(by='frame')

# Export to a single Parquet file
output_file = '/red/roitberg/nick_analysis/merged_formula.pq'
sorted_df.to_parquet(output_file)

print(f"Merged and sorted data exported to {output_file}")


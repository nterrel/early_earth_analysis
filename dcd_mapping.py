import os
import pandas as pd
import math

dcd_dir = '/red/roitberg/22M_20231222_prodrun/'
dcd_files = [os.path.join(dcd_dir, f) for f in os.listdir(dcd_dir) if f.endswith('.dcd')]

# Function to create a mapping from the floor-divided timestamp to the full filename
def create_dcd_mapping(dcd_filenames):
    mapping = {}
    for filename in dcd_filenames:
        # Extract the timestamp part from the filename (assuming the format before 'ns.dcd')
        timestamp = filename.split('_')[-1].replace('ns.dcd', '')
        mapping[float(timestamp)] = filename
    return mapping
dcd_mapping = create_dcd_mapping(dcd_files)

# Show the created mapping for verification
print(dcd_mapping)

df = pd.read_parquet('/red/roitberg/prod_analysis/merged_mol.pq')
ala_df = df[df['name'] == 'Alanine']

def get_dcd_file(time, dcd_mapping):
    # Calculate the floor-divided timestamp
    dcd_time = math.floor(time * 10) / 10
    
    # Lookup the .dcd file path in the mapping
    if dcd_time in dcd_mapping:
        return dcd_mapping[dcd_time]
    else:
        return "File not found"

# Apply the function to the dataframe
ala_df['dcd_file'] = ala_df['time'].apply(lambda x: get_dcd_file(x, dcd_mapping))

# Display the updated dataframe
print(ala_df)
ala_df.to_parquet('/red/roitberg/nick_analysis/alanine_df_with_dcd.pq')
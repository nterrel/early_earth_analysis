import pandas as pd
import mdtraj as md
import os
import sys
import cProfile
import re

parquet_dir = '/red/roitberg/nick_analysis/split_parquets'

separate_dfs = {}

for filename in os.listdir(parquet_dir):
    if filename.endswith('.pq'):
        match = re.search(r'df_floor_time_(\d+\.\d+)\.pq', filename)
        if match:
            floor_time = float(match.group(1))
            df = pd.read_parquet(os.path.join(parquet_dir, filename))
            separate_dfs[floor_time] = df
print(len(separate_dfs), 'dataframes')
# Rest of your script...

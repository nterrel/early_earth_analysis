from joblib import Parallel, delayed
import pandas as pd
from tqdm import tqdm
import os

# Directory containing the files
directory = "/red/roitberg/nick_analysis/unique_fragment_analysis"

# List all the parquet files
files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith("_formula.pq")]

# Function to extract unique signatures from a file
def process_file(file):
    df = pd.read_parquet(file, columns=["signature"])
    return set(df["signature"].unique())

# Parallel processing
unique_signatures_list = Parallel(n_jobs=-1)(
    delayed(process_file)(file) for file in tqdm(files, desc="Processing files in parallel")
)

# Combine all unique signatures
unique_signatures = set().union(*unique_signatures_list)

# Final unique signatures count
print(f"Total unique signatures: {len(unique_signatures)}")


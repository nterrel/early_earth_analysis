import pandas as pd
import mdtraj as md
from top_loader import load_topology
import timeit
from tqdm import tqdm
import numpy as np

start_timer = timeit.default_timer()


def extract_and_assign_coordinates(row, topology):
    try:
        # Load the specific frame for the molecule
        frame = md.load_frame(row['dcd_file'], index=row['local_frame'], top=topology)
        # Extract coordinates using atom indices from the row
        coordinates = frame.xyz[0, row['atom_indices']]
        return coordinates
    except Exception as e:
        print(f"Error extracting coordinates for molecule at index {row.name}: {e}")
        return np.nan

def main(df, topology):
    # Apply the coordinate extraction function row by row
    tqdm.pandas(desc="Extracting coordinates")
    df['coordinates'] = df.apply(lambda row: extract_and_assign_coordinates(row, topology), axis=1)
    df.to_parquet('/red/roitberg/nick_analysis/alanine_df_coords.pq')

if __name__ == "__main__":
    df = pd.read_parquet('/red/roitberg/nick_analysis/alanine_df_with_dcd.pq')
    topology = load_topology('/red/roitberg/nick_analysis/traj_top_0.0ns.h5')
    topology_timer = timeit.default_timer()
    print(f"Topology loaded in {topology_timer - start_timer} seconds.")
    main(df, topology)

end_timer = timeit.default_timer()
print(f'Time for entire script: {end_timer - start_timer} seconds.')

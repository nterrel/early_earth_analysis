import pandas as pd
import mdtraj as md
from top_loader import load_topology
import timeit

start_timer = timeit.default_timer()

df = pd.read_parquet('/red/roitberg/nick_analysis/alanine_df.pq')
topology = load_topology('/red/roitberg/nick_analysis/traj_top_0.0ns.h5')
topology_timer = timeit.default_timer()
print(f'Topology loaded in {topology_timer - start_timer} seconds.')

def extract_frame_coords(traj_file, topology, frame_num, df):
    """
    traj_file: The dcd file which contains the trajectory frame of interest
    topology: A (pre-loaded) topology -- this is the slow step, load it in at the top of the script
    frame_num: Specific frame that a molecule appeared at
    """
for index, row in df.iterrows():
    print(row.keys())
    break

end_timer = timeit.default_timer()

print(f'Time for entire script: {end_timer - start_timer} seconds.')

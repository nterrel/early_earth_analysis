import pandas as pd
import mdtraj as md
from top_loader import load_topology
import timeit

start_timer = timeit.default_timer()

df = pd.read_parquet('/red/roitberg/nick_analysis/alanine_df.pq')
topology = load_topology('/red/roitberg/nick_analysis/traj_top_0.0ns.h5')
topology_timer = timeit.default_timer()
print(f'Topology loaded in {topology_timer - start_timer} seconds.')



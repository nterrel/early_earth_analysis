import pandas as pd
import mdtraj as md
from .top_loader import get_topology

topology = get_topology('/red/roitberg/nick_analysis/traj_top_0.0ns.h5')
print(topology)

df = pd.read_parquet('/red/roitberg/nick_analysis/alanine_df.pq')
print(df)



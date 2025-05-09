from time import time
from top_loader import load_topology

start = time()

top_file = 'traj_top_0.0ns.h5'
topology = load_topology(top_file)

print(f"Time to load h5 topology file: {time() - start} seconds.")

# When I ran this (5/9/2025 on interactive bash session (hpg-dev, 128gb memory)):
# (rapids-23.10) nterrel@c0712a-s30:/red/roitberg/nick_analysis$ python top_loader_example.py 
# Time to load: 52.998902320861816

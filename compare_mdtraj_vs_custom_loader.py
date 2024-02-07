import mdtraj as md
from top_loader import get_topology
import timeit

start = timeit.default_timer()

file = '/red/roitberg/nick_analysis/traj_top_0.0ns.h5'

topology = md.load(file).topology
md_finish = timeit.default_timer()
print(f'MDTraj time: {md_finish - start} seconds.')

topology = get_topology(file)
custom_finish = timeit.default_timer()
print(f'Custom loader time: {custom_finish - md_finish} seconds.')

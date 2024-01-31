import subprocess
import os
import mdtraj as md
import timeit

start = timeit.default_timer()

topology = md.load('/red/roitberg/nick_analysis/traj0.3ns.h5').topology
print(topology)
finish_top = timeit.default_timer()
print(f'Topology loaded in {finish_top - start} seconds.')

def convert_dcd(dcd_file, output_dir):
    output_h5 = os.path.join(output_dir, os.path.basename(dcd_file).replace('.dcd', '.h5'))
    subprocess.run(['mdconvert', dcd_file, '-o', output_h5, '-t', topology])

dcd_file = '/red/roitberg/22M_20231222_prodrun/2023-12-23-005238.631380_0.0ns.dcd'
output_dir = '/red/roitberg/nick_analysis'
convert_dcd(dcd_file, output_dir)

finish = timeit.default_timer()

print(f'File converted in {finish - start} seconds.')
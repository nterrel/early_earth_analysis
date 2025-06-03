import os, glob, time
import mdtraj as md
from top_loader import load_topology

topology_file   = '/red/roitberg/nick_analysis/traj_top_0.0ns.h5'

temp_dir     = '/red/roitberg/nick_analysis/trimmed_ala_frames'
output_file  = '/red/roitberg/nick_analysis/trimmed_ala_stride50.dcd'
topology = load_topology(topology_file)

# STEP 2: concatenate them in ascending order
t1   = time.time()
dcds = glob.glob(os.path.join(temp_dir, "frame_*.dcd"))
dcds.sort(key=lambda fn: int(os.path.basename(fn).split('_')[1].split('.')[0]))
print(f"STEP 2: concatenating {len(dcds)} files…")

traj = md.load(dcds, top=topology)
traj.save_dcd(output_file)

print(f"STEP 2 done in {time.time()-t1:.1f}s; final DCD has {len(traj)} frames")
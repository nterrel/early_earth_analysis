# NOTE: Here we want to split off 400 randomized frames, 10 per traj file for the 4.0 ns of high temp run

# Copy the protocol for `split_traj.py` but use the random module rather than specify the frame numbers

import mdtraj as md
import random
import glob
import os
from top_loader import load_topology
import time
import re

start_time = time.time()

print('Loading topology...')
# Load the topology file with your custom loader
h5_topology = load_topology('/red/roitberg/nick_analysis/traj_top_0.0ns.h5')
print(f'Time to load topology: {time.time() - start_time} seconds')

# Directory containing all DCD files
dcd_files_dir = '/red/roitberg/22M_20231222_prodrun/'
dcd_files = glob.glob(os.path.join(dcd_files_dir, '*.dcd'))
print('Number of dcd files:', len(dcd_files))

def extract_timestamp_ns(dcd_file):
    # The regex pattern to capture the date, time, and ns part of the file name
    pattern = r'(\d{4}-\d{2}-\d{2})-(\d{6}\.\d{6})_(\d\.\d+)ns\.dcd'
    match = re.search(pattern, dcd_file)
    if match:
        # Return combined date-time and nanoseconds as a tuple
        date = match.group(1)
        time = match.group(2)
        ns = match.group(3)
        return f"{date}-{time}", float(ns)
    return None, None

dcd_files_sorted = sorted(dcd_files, key=lambda x: (extract_timestamp_ns(x)[0], extract_timestamp_ns(x)[1]))
for i in dcd_files_sorted:
    print(i,'\n')

# Output directory for the randomized frames
output_dir = '/red/roitberg/nick_analysis/Restart/22.8M/random_400_frames/'
os.makedirs(output_dir, exist_ok=True)

num_random_frames = 10
total_frames_per_dcd = 8000

for file_idx, dcd_file in enumerate(dcd_files_sorted):
    random_frames = sorted(random.sample(range(total_frames_per_dcd), num_random_frames))

    for local_frame_idx in random_frames:
        global_frame_idx = file_idx * total_frames_per_dcd + local_frame_idx

        frame_dir = os.path.join(output_dir, f"frame_{global_frame_idx}")
        os.makedirs(frame_dir, exist_ok=True)

        traj = md.load(dcd_file, top=h5_topology, frame=local_frame_idx)

        output_frame_file = os.path.join(frame_dir, f"frame_{global_frame_idx}_{os.path.basename(dcd_file)}")

        traj.save_dcd(output_frame_file)

        print(f"Saved frame {global_frame_idx} (local frame {local_frame_idx}) from {os.path.basename(dcd_file)} to {output_frame_file}")

print("All random frames saved.")
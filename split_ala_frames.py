# This script takes a subset of 12 frames which contain alanine molecules,
# and splits the corresponding dcd file in order to run molfind and trace
# the synthesis of a dozen alanine molecules backwards through time.

# Note that the 12 structures were picked using the random module (code to do this was copied onto a OneNote file),
# in order to sample 12 totally random structures.


import mdtraj as md
import pandas as pd
from top_loader import load_topology
import glob
import os

def get_dcd(time, dcd_files):
    floor_time = f"{int(time)}.{int((time*10)%10)}ns"
    for dcd_file in dcd_files:
        if floor_time in dcd_file:
            return dcd_file
    return None

# Define the DataFrame with the random structures (this list was created elsewhere, see notes at top of script)
random_structures = pd.DataFrame({
    'frame': [102584, 127761, 53726, 290169, 164418, 196366, 71744, 48938, 39901, 23406, 166471, 224713],
    'local_frame': [6584, 7761, 5726, 2169, 4418, 4366, 7744, 938, 7901, 7406, 6471, 713],
    'time': [1.282300, 1.597012, 0.671575, 3.627112, 2.055225, 2.454575, 0.896800, 0.611725, 0.498762, 0.292575, 2.080887, 2.808912]
})

# Directory to save individual frames to (create if it doesn't already exist)
individual_frames_dir = "/red/roitberg/nick_analysis/Trimmed_frames/Ala_synthesis/"
os.makedirs(individual_frames_dir, exist_ok=True)

# Load the topology with the custom loader function
h5_topology = load_topology('/red/roitberg/nick_analysis/traj_top_0.0ns.h5')

# Make a list of dcd files to iterate over
dcd_files = glob.glob('/red/roitberg/22M_20231222_prodrun/*.dcd')

# Iterate over the df of randomly selected frames which include alanine molecules
for index, row in random_structures.iterrows():
    dcd_file = get_dcd(row['time'], dcd_files)
    if dcd_file is not None:
        frame = row['frame']
        local_frame = row['local_frame']
        trajectory = md.load(dcd_file, top=h5_topology, frame=local_frame)
        output_frame_file = f"{individual_frames_dir}frame_{frame}_{os.path.basename(dcd_file)}"
        trajectory.save_dcd(output_frame_file)
        print(f"Saved frame {local_frame} from {os.path.basename(dcd_file)} to {output_frame_file}")
    else:
        print(f"No DCD file found for time {row['time']}")

print("All frames saved individually")



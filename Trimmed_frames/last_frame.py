# The purpose of this script is to split the following file:
#  2023-12-24-094959.618385_1.2ns.dcd
# to a small subset of frames for testing on.
# This file contains all Lysine molecules found, so should be a good testing subset.

import mdtraj as md
from top_loader import load_topology

input_dcd = "/red/roitberg/22M_20231222_prodrun/2023-12-30-191515.525761_4.3ns.dcd"
h5_topology = load_topology('traj_top_0.0ns.h5')

# Global frames 97608 - 97629, but using the local frame numbers:
frame = 8000

# Directory where the individual frame will be stored
output_frame_file = f"/red/roitberg/nick_analysis/frame_{frame}.dcd"

# Load the specific frame
trajectory = md.load(input_dcd, top=h5_topology, frame=frame)

# Save the specific frame to a new DCD file
trajectory.save_dcd(output_frame_file)

print(f"Saved frame {frame} to {output_frame_file}")


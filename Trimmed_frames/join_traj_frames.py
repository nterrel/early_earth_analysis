# The purpose of this script is to join the frames split from:
#  2023-12-24-094959.618385_1.2ns.dcd
# to a small subset of frames for testing on.
# This file contains all Lysine molecules found, so should be a good testing subset.

import mdtraj as md
from top_loader import load_topology

h5_topology = load_topology('traj_top_0.0ns.h5')

# Global frames 97608 - 97629, but using the local frame numbers:
start_frame = 1608
end_frame = 1629

individual_frames_dir = "/red/roitberg/nick_analysis/Trimmed_frames/"

# Load all the individual frames and join them into a single trajectory
frames = [md.load_dcd(f"{individual_frames_dir}frame_{frame}.dcd", top=h5_topology)
          for frame in range(start_frame, end_frame + 1)]
joined_trajectory = md.join(frames)

# Save the joined trajectory
output_dcd = "/red/roitberg/nick_analysis/trimmed_1608-1629_1.2ns.dcd"
joined_trajectory.save_dcd(output_dcd)

print(f"Trimmed trajectory saved to {output_dcd}")

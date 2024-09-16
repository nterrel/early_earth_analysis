# NOTE: I think it would be better to just iterate over the directories and automate the creation/submission of molfind scripts for original and quench dcds

import mdtraj as md
import os
import re
import time
from top_loader import load_topology


script_start_time = time.time()

top_load_start_time = time.time()
topology = load_topology('traj_top_0.0ns.h5')
top_load_end_time = time.time()
print(
    f"Time to load topology: {top_load_end_time - top_load_start_time:.2f} seconds")

# Directories where frames are stored, and output file names
base_dir = '/red/roitberg/nick_analysis/Restart/22.8M_atoms/'
output_original_dcd = '/red/roitberg/nick_analysis/Restart/unified_original_trajectory.dcd'
output_quench_dcd = '/red/roitberg/nick_analysis/Restart/unified_quench_trajectory.dcd'
output_frame_numbers_file = '/red/roitberg/nick_analysis/Restart/frame_numbers_list.txt'

# Lists to hold the trajectories and frame numbers
original_traj_list = []
quench_last_frames = []
frame_numbers = []

# Regular expression pattern to extract the frame number from the directory name
frame_number_pattern = re.compile(r'frame_(\d+)')

dir_listing_start_time = time.time()
all_items = os.listdir(base_dir)
frame_dirs = [(item, int(frame_number_pattern.match(item).group(1)))
              for item in all_items if frame_number_pattern.match(item)]
sorted_frame_dirs = sorted(frame_dirs, key=lambda x: x[1])
dir_listing_end_time = time.time()
print(
    f"Time to list and sort directories: {dir_listing_end_time - dir_listing_start_time:.2f} seconds")
print('List of directories / frame numbers\n', sorted_frame_dirs)

# Timestamp for frame processing loop
frame_processing_start_time = time.time()

# Loop over frame directories
for frame_dir, frame_number in sorted_frame_dirs:
    frame_path = os.path.join(base_dir, frame_dir)

    if os.path.isdir(frame_path):
        # Store the frame number in the list
        frame_numbers.append(frame_number)

        # Look for 'frame_*_original.dcd' file
        original_dcd_file = None
        for file in os.listdir(frame_path):
            if file.startswith('frame_') and file.endswith('_original.dcd'):
                original_dcd_file = os.path.join(frame_path, file)
                break

        if original_dcd_file:
            # Load and store the original trajectory, print timing information
            original_load_start_time = time.time()
            original_traj_list.append(md.load(original_dcd_file, top=topology))
            original_load_end_time = time.time()
            print(
                f"Time to load original DCD for frame {frame_number}: {original_load_end_time - original_load_start_time:.2f} seconds")

        # Look for '*_quench.dcd' file in the 'logs' subdirectory
        quench_dcd_file = None
        logs_dir = os.path.join(frame_path, 'logs')
        if os.path.exists(logs_dir):
            for file in os.listdir(logs_dir):
                if file.endswith('_quench.dcd'):
                    quench_dcd_file = os.path.join(logs_dir, file)
                    break

        if quench_dcd_file:
            # Load the quench trajectory, print timing information
            quench_load_start_time = time.time()
            quench_traj = md.load(quench_dcd_file, top=topology)

            # Check if the trajectory contains exactly 21 frames
            if quench_traj.n_frames == 21:
                last_frame = quench_traj[20]  # Get the 21st frame (index 20)
                quench_last_frames.append(last_frame)
            else:
                print(
                    f"Warning: Quench trajectory in {quench_dcd_file} does not contain 21 frames (found {quench_traj.n_frames} frames)")
            quench_load_end_time = time.time()
            print(
                f"Time to load quench DCD for frame {frame_number}: {quench_load_end_time - quench_load_start_time:.2f} seconds")

frame_processing_end_time = time.time()
print(
    f"Total time to process frames: {frame_processing_end_time - frame_processing_start_time:.2f} seconds")

# Concatenate the original trajectories
concatenate_original_start_time = time.time()
if original_traj_list:
    unified_original_traj = md.join(original_traj_list)
    unified_original_traj.save_dcd(output_original_dcd)
concatenate_original_end_time = time.time()
print(
    f"Time to concatenate and save original DCD: {concatenate_original_end_time - concatenate_original_start_time:.2f} seconds")

# Concatenate the last frames of the quench trajectories
concatenate_quench_start_time = time.time()
if quench_last_frames:
    unified_quench_traj = md.join(quench_last_frames)
    unified_quench_traj.save_dcd(output_quench_dcd)
concatenate_quench_end_time = time.time()
print(
    f"Time to concatenate and save quench DCD: {concatenate_quench_end_time - concatenate_quench_start_time:.2f} seconds")

# Save the list of frame numbers to a text file
frame_number_save_start_time = time.time()
with open(output_frame_numbers_file, 'w') as f:
    for frame_number in frame_numbers:
        f.write(f"{frame_number}\n")
print(f"Frame numbers saved to {output_frame_numbers_file}")
frame_number_save_end_time = time.time()
print(
    f"Time to save frame numbers: {frame_number_save_end_time - frame_number_save_start_time:.2f} seconds")

# Total script runtime
script_end_time = time.time()
print(
    f"Total script runtime: {script_end_time - script_start_time:.2f} seconds")

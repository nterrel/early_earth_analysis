import os
import mdtraj as md
import argparse
from top_loader import load_topology
import numpy as np

try:
    topology = load_topology('/red/roitberg/nick_analysis/traj_top_0.0ns.h5')
    print("Topology loaded successfully.")
except Exception as e:
    print(f"Error loading topology: {e}")
    exit(1)

trajectory_files = [
    ('/red/roitberg/22M_20231222_prodrun/2023-12-30-191515.525761_4.1ns.dcd', 328000, 328000),  # 1 frame (328000-328000)
    ('/red/roitberg/22M_20231222_prodrun/2023-12-28-073439.757187_4.0ns.dcd', 320000, 327999),  # 8000 frames (320000-327999)
    ('/red/roitberg/22M_20231222_prodrun/2023-12-28-073439.757187_3.9ns.dcd', 312000, 319999),  # 8000 frames (312000-319999)
    ('/red/roitberg/22M_20231222_prodrun/2023-12-28-073439.757187_3.8ns.dcd', 304000, 311999)   # 8000 frames (304000-311999)
]

def get_trajectory_file_and_local_frame(global_frame_num):
    """
    Determine which trajectory file and local frame index correspond to the global frame number.
    
    :param global_frame_num: Global frame number across all trajectory files
    :return: (trajectory_file, local_frame_num)
    """
    for traj_file, start_frame, end_frame in trajectory_files:
        if start_frame <= global_frame_num <= end_frame:
            local_frame_num = global_frame_num - start_frame
            return traj_file, local_frame_num
    raise ValueError(f"Frame number {global_frame_num} is out of range.")

def get_time_from_filename(filename):
    """
    Extract the time in ns from the trajectory filename.
    
    :param filename: Filename of the trajectory file
    :return: Time in ns
    """
    parts = filename.split('_')
    time_part = parts[-1].replace('.dcd', '')
    return time_part

def slice_and_save_frame(trajectory_path, topology, global_frame_num, atom_indices, output_dir):
    """
    Load a specified frame from a trajectory, slice it based on atom indices,
    and save the sliced atoms to a PDB file.

    :param trajectory_path: Path to the trajectory file
    :param topology: Calls the pre-loaded topology
    :param global_frame_num: Global frame number to load
    :param atom_indices: List of atom indices to include in the slice
    :param output_dir: Directory to save the output files
    """
    # Load the specified frame from the trajectory
    try:
        traj_file, local_frame_num = get_trajectory_file_and_local_frame(global_frame_num)
        print(f"Loading global frame {global_frame_num} from {traj_file} (local frame {local_frame_num})")
        frame = md.load_frame(traj_file, index=local_frame_num, top=topology)
        print(f"Frame {global_frame_num} (local {local_frame_num}) loaded from {traj_file} successfully.")

        # Slice the trajectory based on atom indices
        sliced_traj = frame.atom_slice(atom_indices)
        print(f"Frame {global_frame_num} sliced successfully. Number of atoms: {sliced_traj.n_atoms}")

        # Generate output file name
        time_ns = get_time_from_filename(traj_file)
        output_file_name = os.path.join(output_dir, f"alanine_frame{global_frame_num}_{time_ns}ns.pdb")

        # Save the sliced atoms to a PDB file
        sliced_traj.save_pdb(output_file_name)
        print(f"Output saved to {output_file_name}")
    except Exception as e:
        print(f"Error processing frame {global_frame_num}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Slice a frame from a trajectory and save it as a PDB file.")
    parser.add_argument('trajectory_path', help="Path to the trajectory file")
    parser.add_argument('--start_frame', type=int,
                        help="Frame number to start from")
    parser.add_argument('--end_frame', type=int, help="Frame number to load")
    parser.add_argument(
        '--output_dir', help="Directory to save the output files", default='output_frames')

    args = parser.parse_args()

    # Convert atom_indices from string to list of integers
    ala_indices = np.array([1841346, 2134874, 5220173, 5703624, 7290995, 7646768, 11071642, 11581279, 12069596, 13122725, 15493659, 17220635, 21665985])

    os.makedirs(args.output_dir, exist_ok=True)

    for frame_num in range(args.start_frame, args.end_frame - 1, -1):
        slice_and_save_frame(args.trajectory_path, topology, frame_num, ala_indices, args.output_dir)


if __name__ == "__main__":
    main()

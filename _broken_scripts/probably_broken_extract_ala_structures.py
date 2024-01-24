import pandas as pd
import os
import math
import mdtraj as md
import cProfile
import sys

def slice_and_save_frame(trajectory_path, topology_path, frame_num, atom_indices):
    """
    Load a specified frame from a trajectory, slice it based on atom indices,
    and save the sliced atoms to a PDB file.

    :param trajectory_path: Path to the trajectory file
    :param topology_path: Path to the topology file
    :param frame_num: Frame number to load
    :param atom_indices: List of atom indices to include in the slice
    """
    # Load the specified frame from the trajectory
    frame = md.load_frame(trajectory_path, index=frame_num, top=topology_path)

    # Slice the trajectory based on atom indices
    sliced_traj = frame.atom_slice(atom_indices)
    # breakpoint()

    coordinates = sliced_traj.xyz[0]
    print('Extracted coord:', coordinates)

    # Generate output file name
    traj_file_name = os.path.splitext(os.path.basename(trajectory_path))[0]
    atom_indices_str = '_'.join(map(str, atom_indices))[:20]
    output_file_name = f"{traj_file_name}_frame{frame_num}_atoms{atom_indices_str}.xyz"

    # Save the sliced atoms to a PDB file
    sliced_traj.save_xyz(output_file_name)
    print(f"Output saved to {output_file_name}")
    return coordinates



separate_dfs = {}

for filename in os.listdir(parquet_dir):
    if filename.endswith('.pq'):
        floor_time = float(filename.split('_')[-2])
        df = pd.read_parquet(os.path.join(parquet_dir, filename))
        separate_dfs[floor_time] = df

count = 0

# Function to loop over all the trajectory files
def main(floor_time):
    parquet_dir = '/red/roitberg/nick_analysis/split_parquets'
    traj_dir = '/red/roitberg/22M_20231222_prodrun/'
    top_file = '/blue/roitberg/apps/lammps-ani/examples/early_earth/data/mixture_22800000.pdb'
    for index, row in alanine_df.iterrows():
        count += 1
        frame_time = math.floor(row['time'] * 10) / 10
        atom_indices = row['atom_indices']
        
        traj_file = determine_correct_dcd(frame_time, traj_dir)
        print('Trajectory file path:', traj_file)

        if traj_file is None:
            print(f'No .dcd file found for frame time {frame_time}')
        frame_num = row['local_frame']
        print(frame_num)

        slice_and_save_frame(traj_file, top_file, frame_num, atom_indices)


        if count > 100:
            break

if __name__ == "__main__":
    cProfile.run('main()', 'profiling_results.prof')
    floor_time = sys.argv[1]
    main(float(floor_time))

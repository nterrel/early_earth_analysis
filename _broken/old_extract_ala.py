import pandas as pd
import os
import re
import subprocess
import math
import mdtraj as md
import cProfile

def determine_correct_dcd(frame_time, traj_dir):
    """
    This function checks for the correct simulation timestamp across a directory of
     .dcd trajectory files and returns the path to the correct file (or, if not located,
     returns None).
    :param frame_time: Timestamp (rounded down) of the simulation run
    :param traj_dir: Path to the .dcd files to search through
    """
    dcd_files = [f for f in os.listdir(traj_dir) if f.endswith('.dcd')]
    frame_time_str = "{:.1f}".format(frame_time)

    for file in dcd_files:
        traj_filename = os.path.basename(file)
        match = re.search(r'_(\d+\.\d+)ns\.dcd$', traj_filename)
        if match:
            time_offset = match.group(1)
            if frame_time_str == time_offset:
                return os.path.join(traj_dir, file)
    return None


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
    # Generate output file name
    traj_file_name = os.path.splitext(os.path.basename(trajectory_path))[0]
    atom_indices_str = '_'.join(map(str, atom_indices))[:20]
    output_file_name = f"{traj_file_name}_frame{frame_num}_atoms{atom_indices_str}.pdb"

    # Save the sliced atoms to a PDB file
    sliced_traj.save_pdb(output_file_name)
    print(f"Output saved to {output_file_name}")

alanine_df = pd.read_parquet('/red/roitberg/nick_analysis/alanine_df.pq')
# The above df can be obtained with:
    # df = pd.read_parquet('/red/roitberg/prod_analysis/merged_mol.pq')
    # alanine_df = df[df['name'] == 'Alanine']
    # alanine_df.to_parquet('/red/roitberg/nick_analysis/alanine_df.pq')
    # Then load

#print('Alanine structures:', len(alanine_df))

alanine_df['dcd_file'] = alanine_df['time'].apply(lambda t: math.floor(t * 10) / 10).apply(lambda ft: determine_correct_dcd(ft, '/red/roitberg/22M_20231222_prodrun/'))
#print(alanine_df['dcd_file'].unique()) #NOTE: This does detect there are structures from every .dcd file except 0.0ns

traj_dir = '/red/roitberg/22M_20231222_prodrun/'
top_file = '/blue/roitberg/apps/lammps-ani/examples/early_earth/data/mixture_22800000.pdb'
output_dir = '/blue/roitberg/nterrel/'

count = 0

# Iterate over each row in the alanine dataframe
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
    #command = f"python /red/roitberg/extract_slice.py {traj_file} {top_file} --frame_num={frame_num} --atom_indices=\"{atom_indices}\""
    #subprocess.run(command, shell=True)

    if count > 100:
        break

if __name__ == "__main__":
    cProfile.run('main()', 'profiling_results.prof')
    dcd_filename = sys.argv[1]
    main(dcd_filename)

import mdtraj as md
import os
import timeit
#import cProfile

start_timer = timeit.default_timer()
##
#
#
# DO THIS TOMORROW:
topology = md.load('/red/roitberg/nick_analysis/22M_topology.pdb').topology
save the topology as pickle
see if .pkl loads more quickly than .pdb
#
#
#


def split_trajectory(traj_file, top_file, frame_num, output_dir):
    frame = md.load_frame(traj_file, index=frame_num, top=top_file)
    traj_file_name = os.path.splitext(os.path.basename(traj_file))[0]
    output_file_name = f"{traj_file_name}_frame{frame_num}.dcd"
    output_path = os.path.join(output_dir, output_file_name)
    single_frame_traj = md.Trajectory([frame.xyz], topology=frame.topology)
    single_frame_traj.save_dcd(output_path)
    print(f"Frame {frame_num} saved to {output_path}")

traj_file = '/red/roitberg/22M_20231222_prodrun/2023-12-23-130144.793745_0.3ns.dcd'
top_file = '/red/roitberg/nick_analysis/22M_topology.pdb'
frame_num = 24221
output_dir = '/red/roitberg/nick_analysis/'


if __name__ == "__main__":
    #cProfile.run('split_trajectory()', '/blue/roitberg/nterrel/split_traj_first_frame.prof')
    split_trajectory(traj_file, top_file, frame_num, output_dir)
    end_timer = timeit.default_timer()
    print(f"Open and split trajectory time: {end_timer - start_timer} seconds.")

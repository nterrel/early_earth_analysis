import mdtraj as md
import h5py
import numpy as np

# Load the topology
topology = md.load('/red/roitberg/nick_analysis/22M_topology.pdb').topology

# Initialize an HDF5 file
with h5py.File('/red/roitberg/nick_analysis/test_0.3ns_traj_8_frames.h5', 'w') as h5file:
    # Assuming we know the number of atoms and the number of frames in advance
    atom_count = topology.n_atoms
    frame_count = 8
    coords_dataset = h5file.create_dataset('coordinates', (frame_count, atom_count, 3), dtype='float32')
    
    # Save topology to a separate dataset or attribute (outside the loop)
    topology_json = topology.to_json()
    h5file.attrs['topology'] = topology_json

    count = 0
    # Now iterate through the trajectory, frame by frame
    for frame_num in range(frame_count):
        try:
            # Assuming trajectory file path pattern and loading one frame at a time
            trajectory = md.load_dcd(f'/red/roitberg/22M_20231222_prodrun/2023-12-23-130144.793745_0.3ns.dcd', top=topology, frame=frame_num)
            # Assuming trajectory only contains one frame here
            coords_dataset[frame_num, :, :] = trajectory.xyz[0]
            count += 1
            print(f'Frame {count} added to test_0.3ns_traj_8_frames.h5')
        except Exception as e:
            print(f"Error loading frame {frame_num}: {e}")

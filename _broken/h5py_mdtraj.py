import mdtraj as md
import h5py
import numpy as np
import json

# NOTE: needs lots of updating, but try to mimic the h5 organization -- perhaps save this topology in json so that it can just be appended rather than loaded every time

# Load topology
topology = md.load('/path/to/topology.pdb').topology

# Initialize HDF5 file
with h5py.File('/path/to/output.h5', 'w') as h5file:
    # Create datasets for coordinates, etc.
    atom_count = topology.n_atoms
    coords_dataset = h5file.create_dataset('coordinates', shape=(0, atom_count, 3), maxshape=(None, atom_count, 3), dtype='float32')
    
    # Save topology as JSON in an attribute
    topology_json = json.dumps(topology.to_dict())
    h5file.attrs['topology'] = topology_json

    # Iterate over frames in DCD file
    for frame in md.iterload('/path/to/dcd_file.dcd', top=topology, chunk=1):
        # Append coordinates to dataset
        new_shape = (coords_dataset.shape[0] + 1, atom_count, 3)
        coords_dataset.resize(new_shape)
        coords_dataset[-1, :, :] = frame.xyz[0]

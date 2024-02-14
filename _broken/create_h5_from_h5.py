import h5py
import timeit

start = timeit.default_timer()

# Open the existing HDF5 file
with h5py.File('/red/roitberg/nick_analysis/traj0.3ns.h5', 'r') as existing_file:
    # Access the existing topology dataset
    existing_topology = existing_file['topology']

    # Extract necessary properties
    shape = existing_topology.shape
    dtype = existing_topology.dtype

    # Open a new HDF5 file for the topology data
    with h5py.File('/red/roitberg/nick_analysis/topology_only.h5', 'w') as new_file:
        # Manually create a new dataset with the same shape and dtype
        new_topology = new_file.create_dataset('topology', shape=shape, dtype=dtype)
        
        # If you need to copy the data
        new_topology[:] = existing_topology[:]

finish = timeit.default_timer()
print(f"Time to write new h5: {finish - start} seconds.")


"""
output after:
(/blue/roitberg/apps/torch1121) nterrel@c0710a-s10:/red/roitberg/nick_analysis$ python
Python 3.8.16 | packaged by conda-forge | (default, Feb  1 2023, 16:01:55) 
[GCC 11.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import mdtraj as md
>>> top = md.load('/red/roitberg/nick_analysis/topology_only.h5').topology
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/blue/roitberg/apps/torch1121/lib/python3.8/site-packages/mdtraj/core/trajectory.py", line 396, in load
    kwargs["top"] = _parse_topology(kwargs.get("top", filename_or_filenames[0]), **topkwargs)
  File "/blue/roitberg/apps/torch1121/lib/python3.8/site-packages/mdtraj/core/trajectory.py", line 174, in _parse_topology
    _traj = load_frame(top, 0, **kwargs)
  File "/blue/roitberg/apps/torch1121/lib/python3.8/site-packages/mdtraj/core/trajectory.py", line 314, in load_frame
    return loader(filename, frame=index, **kwargs)
  File "/blue/roitberg/apps/torch1121/lib/python3.8/site-packages/mdtraj/formats/hdf5.py", line 119, in load_hdf5
    return f.read_as_traj(n_frames=n_frames, stride=stride, atom_indices=atom_indices)
  File "/blue/roitberg/apps/torch1121/lib/python3.8/site-packages/mdtraj/formats/hdf5.py", line 518, in read_as_traj
    data = self.read(n_frames=n_frames, stride=stride, atom_indices=atom_indices)
  File "/blue/roitberg/apps/torch1121/lib/python3.8/site-packages/mdtraj/formats/hdf5.py", line 572, in read
    total_n_frames = len(self._handle.root.coordinates)
  File "/blue/roitberg/apps/torch1121/lib/python3.8/site-packages/tables/group.py", line 798, in __getattr__
    return self._f_get_child(name)
  File "/blue/roitberg/apps/torch1121/lib/python3.8/site-packages/tables/group.py", line 682, in _f_get_child
    self._g_check_has_child(childname)
  File "/blue/roitberg/apps/torch1121/lib/python3.8/site-packages/tables/group.py", line 375, in _g_check_has_child
    raise NoSuchNodeError(
tables.exceptions.NoSuchNodeError: group ``/`` does not have a child named ``coordinates``
"""

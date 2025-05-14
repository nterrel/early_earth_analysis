# Some questions we are looking to answer

1. Can we identify every 'formed' molecule with more than 5 atoms?

- UPDATE: Not exactly, but `cumolfind_unique_graphs` gets pretty close -- no graph comparison, but tracks every bond (pair of atoms with a bond between them) in a molecule. This is due to GPU-accelerated graph analysis tools do not have unique comparisons (at present). Migrating all data to CPU to do graph comparisons to determine "have we seen this molecule before" might as well be impossible because it is very slow.

2. Can we demonstrate the path of formation of those 'interesting' molecules?

- UPDATE: YES -- branch `cumolfind_modified` in lammps-ani has a script called `trackmol.py` that can follow a list (or multiple lists) of atom indices backwards through a trajectory. This outputs xyz files per fragment, which can be combined to a single xyz per frame to visualize the formation, over time, of a molecule.


# Script used to create a .data file for lammps input (for quenching system to run molfind before/after cooling to 300 K)

# NOTE: This script produces a .pdb file in a format that is not compatible with the lammps_ani scripts `fix_pdb.py` and `pdb2lmp.py`, so instead save coordinates as xyz, use ASE to save pdb, run `fix_pdb.py` and then `pdb2lmp.py`.

import mdtraj as md
from top_loader import load_topology
from ase.io import read, write

topology = load_topology('traj_top_0.0ns.h5')
trajectory = md.load('/red/roitberg/nick_analysis/Restart/22.8M_atoms/frame_196366/frame_196366_2.4ns_original.dcd', top=topology)

# Correct the unit cell dimensions (converting nm to Å)
#cell_lengths_nm = trajectory.unitcell_lengths
#cell_lengths_angstroms = cell_lengths_nm * 10.0  # Convert nm to Å
#trajectory.unitcell_lengths = cell_lengths_angstroms

frame_index = 0
frame = trajectory[frame_index]

frame.save_pdb('/red/roitberg/nick_analysis/Restart/22.8M_atoms/frame_196366/frame_196366.pdb')


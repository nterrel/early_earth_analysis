# Script used to create a .data file for lammps input (for quenching system to run molfind before/after cooling to 300 K)

# CHECK UNITS

# mdtraj uses different units than ASE, so be sure that the output xyz (which is the important output from this script -- make the pdb using Richard's tool in lammps_ani) has a cell size of 557x557x557 

import mdtraj as md
from top_loader import load_topology
from ase.io import read, write

topology = load_topology('traj_top_0.0ns.h5')
trajectory = md.load('/red/roitberg/nick_analysis/Restart/22.8M_atoms/frame_196366/frame_196366_2.4ns_original.dcd', top=topology)

# Correct the unit cell dimensions (converting nm to Å)
cell_lengths_nm = trajectory.unitcell_lengths
cell_lengths_angstroms = cell_lengths_nm * 10.0  # Convert nm to Å
trajectory.unitcell_lengths = cell_lengths_angstroms

frame_index = 0
frame = trajectory[frame_index]

frame.save('/red/roitberg/nick_analysis/Restart/22.8M_atoms/frame_196366/frame_196366.xyz')

atoms = read('/red/roitberg/nick_analysis/Restart/22.8M_atoms/frame_196366/frame_196366.xyz')
atoms.set_cell(cell_lengths_angstroms[0])

write('/red/roitberg/nick_analysis/Restart/22.8M_atoms/frame_196366/frame_196366.data', atoms, format='lammps-data')

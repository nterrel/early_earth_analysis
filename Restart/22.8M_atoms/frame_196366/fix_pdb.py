# NOTE: Taken from lammps_ani -- used to correct the syntax of pdb files, for use with `pdb2lmp.py`. That file relies on very particular formatting, fails otherwise.

# The xyz input from this script was produced from `convert_dcd_to_pdb.py` located in /red/roitberg/nick_analysis/ -- be sure to check units. 

# This file does produce a pdb which can be used with `pdb2lmp.py`, unlike saving to pdb from mdtraj directly. 
# So take the following process:
# 1. load frame in mdtraj
# 2. convert units to be consistent with Richard's inputs -- can't remember which is in A and which is in nm, but the box length should be 557^3 after the conversion
# 3. save frame as xyz
# 4. input the xyz file name in this script

from ase.io import read, write

mol = read("frame_196366.xyz")
write("frame_196366_ase.pdb", mol)
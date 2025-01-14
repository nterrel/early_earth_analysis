# Minimization and extraction of the largest single molecule found throughout the simulation

This directory contains the structure (and scripts used in minimizing) of the largest molecule produced in the big early earth run, containing 96 atoms, AFTER running a short quench on the system (contained at `/red/roitberg/nick_analysis/Restart/frame_256780`).

## Scripts housed here

- `extract_96atom_quench.py`
  - This python script can be used to extract the coordinates of a specific atomic formula from a simulation frame -- this is really only useful if that formula appears only once in that frame (as is the case with the 96 atom system).

- `submit_96atom_quench_extract.sh`
  - SLURM submission script to run the `extract_96atom_quench.py` python script -- loading the traj requires a lot of memory so I use the scheduler to ask for those resources whenever I need to open a traj for any reason.

## Miscellaneous outputs saved here

- `96_atom_quench_coords.h5`
  - This contains the coordinates of the same atoms after quenching
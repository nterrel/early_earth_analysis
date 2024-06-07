# Early Earth simulation analysis

Source (local) repository housed on HiPerGator at `/red/roitberg/nick_analysis/`

## Usage and some notes

The topology of the 22.8M atom simulation is saved from frame 0 of the 0.0ns .dcd trajectory file

- Loading this topology from the original pdb is very slow (approx 8-10 minutes)
- Loading from a .h5 slice of the first frame of trajectory data takes ~200 sec with the default MDTraj function
- Loading from this .h5 slice with 'top_loader.py' (thanks Ignacio) takes approximately 85 sec

## Scripts found in this directory NOTE: UPDATE SINCE THESE HAVE BEEN MOVED

- `extract_trace_frames.py`
  - This script can extract a specified list of atom indices from a specified number of frames. Left in this directory as `top_loader.py` is a necessary import. Extracts coordinates to the `./Mol_trace/` directory.

- `top_loader.py`
  - This script is used to load a topology in MDTraj from a single-frame slice of the trajectory (Using the zeroth-frame of the 0.0ns traj file, stored in 'traj_top_0.0ns.h5'). The purpose is to load in a massive (22.8M atom) topology more efficiently than the pdb loader

## Other files located here

- `22M_topology.pdb`:
  - Original topology Richard used for his simulation

- `all_mol_data.pq`:
  - Dataframe containing molecules of interest: sugars, amino acids, nucleobases, etc.
  - Also contains all possible dimers of the above molecules of interest (357 total molecules)

- `merged_formula.pq`:
  - A dataframe containing all 'molecules' found in the graph search. No atom_indices are included, but frame#, formula are saved here for every graph found at every frame (~570M rows, big dataframe)

- `traj_top_0.0ns.h5`:
  - The hdf stored topology used with the 'top_loader.py' script

## Some directories and their contents

- `Extracts`:
  - Contains scripts, outputs, analysis related to extracted molecules

- `HDF_coord`:
  - Not saved to remote repo
  - (WIP) Here is where I want to include HDFs with coordinates for ALL 'found' molecules in the EE simulation. Needs work, there's only a few h5 files here, the others have not been generated yet

- `Misc_parquets`:
  - Some analysis of the found molecules, largest molecule over time, largest molecule per frame, counts of all found formulas.

- `Mol_trace`:
  - Directory to dump coordinates for the 'trace' alanine formation used to produce that figure Adrian asked for.

- `Old_outputs`:
  - Not saved to remote repo
  - .txt and .log files from scripts, only keeping for timing/job execution details

- `Restart`
  - Scripts, simulation files related to restarting the EE simulation runs in order to minimize frames and re-run graph analysis.

- `Scripts`:
  - (WIP) Location for general scripts (after adapting from Ala stuff)

- `Split_parquets`:
  - Not saved to remote repo
  - These files are split along the same timestamps as the .dcd trajectory files. Includes the absolute path to a trajectory file in which a molecule can be found/extracted

- `Sync_to_mac`:
  - Not saved to remote repo
  - Used to send files (via sshfs) between my MacBook and this directory on HPG

- `_broken`:
  - Not saved to remote repo
  - Explains itself; where I put scripts and outputs that didn't work as expected, but probably want to hang onto

- `_testing`:
  - Not saved to remote repo
  - Location of scripts that aren't yet ready to run (or things I don't want to delete, timing tests, etc.)

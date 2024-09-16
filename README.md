# Early Earth simulation analysis

Source (local) repository housed on HiPerGator at `/red/roitberg/nick_analysis/`

## Usage and some notes

The topology of the 22.8M atom simulation is saved from frame 0 of the 0.0ns .dcd trajectory file

- Loading this topology from the original pdb is very slow (approx 8-10 minutes)
- Loading from a .h5 slice of the first frame of trajectory data takes ~200 sec with the default MDTraj function
- Loading from this .h5 slice with 'top_loader.py' (thanks Ignacio) takes approximately 85 sec

## Scripts found in this directory NOTE: UPDATE SINCE THESE HAVE BEEN MOVED

- `dcd2data.py`
  - Small script to load a .dcd traj file and create a .data file for use in restarting the simulation run from this frame. Note that the velocities are not preserved, since there are not restart checkpoints.

- `submit_dcd2data_dir.sh`
  - SLURM submission script for the python script which converts a dcd trajectory frame to a .data file for use as a LAMMPS input.

- `top_loader.py`
  - This script is used to load a topology in MDTraj from a single-frame slice of the trajectory (Using the zeroth-frame of the 0.0ns traj file, stored in 'traj_top_0.0ns.h5'). The purpose is to load in a massive (22.8M atom) topology more efficiently than the pdb loader
  - Extrememly useful, this script should be used any time the topology needs to be loaded. 

## Other files located here (not synced through GH since they are too large)

- `22M_topology.pdb`:
  - Original topology Richard used for his simulation

- `all_mol_data.pq`:
  - Dataframe containing molecules of interest: sugars, amino acids, nucleobases, etc.
  - Also contains all possible dimers of the above molecules of interest (357 total molecules)

- `merged_formula.pq`:
  - A dataframe containing all chemical formulas found in the graph search
  - No atom_indices are included, but frame number and formula are saved here for every graph found at every frame (~570M rows, big dataframe)

- `merged_mol.pq`:
  - Dataframe containing all 'molecules' found in the graph search.
  - This df contains atom_indices that can be used to extract the molecular coordinates of any of these molecules of interest.
  - This is an outdated parquet, many of the 'found' molecules are not truly that molecule as the graph search was indiscriminant of bonding patterns. New version of molfind has been adapted to correct this, but the entire trajectory has not been re-analyzed, though 415 frames (found in Restart/22.8M_atoms) have been re-analyzed before and after a cooling quench.

- `rapids_23.10.yml`:
  - Backup of the packages (with correct channel and build) that Richard used to create the original rapids env.

- `traj_top_0.0ns.h5`:
  - The hdf stored topology used with the 'top_loader.py' script
  - This is the first frame (initial starting configuration) used to keep track of atomic indices throughout the simulation. Works as a topology for any trajectory frame loaded into mdtraj, loads much much faster than in pdb format.

## Some directories and their contents

- `Extracts`:
  - Contains scripts, outputs, analysis related to extracted molecules
  - Subdirectories include Alanine, Glycine (not very populated, placeholder for analysis of the bulk of 'found' molecules), and Others (found molecules which are not glycine or alanine)

- `HDF_coord`:
  - Not saved to remote repo
  - (WIP) Here is where I want to include HDFs with coordinates for ALL 'found' molecules in the EE simulation. Needs work, there's only a few h5 files here, the others have not been generated yet

- `Misc_parquets`:
  - Some analysis of the found molecules, largest molecule over time, largest molecule per frame, counts of all found formulas.

- `Mol_trace`:
  - Directory to dump coordinates for the 'trace' alanine formation used to produce that figure Adrian asked for.

- `molfind_modified_timing`:
  - Directory used for timing comparisons before and after making changes to the cumolfind program.
  - Only notable change so far that didn't significantly impact the timing was the addition of a more rigorous 

- `Old_outputs`:
  - Not saved to remote repo
  - .txt and .log files from scripts, only keeping for timing/job execution details

- `Restart`
  - Scripts, simulation files related to restarting the EE simulation runs in order to minimize frames and re-run graph analysis.
  - 228_atoms / 228k_atoms / 22.8M_atoms directories contain files needed for restarting EE sim run for cumolfind analysis of synthesized molecules.
    - Subdir of 22.8M_atoms is `random_400_frames` where I have split off 400 randomly selected frames for quench restarts. 

- `Scripts`:
  - (WIP) Location for general scripts (after adapting from Ala stuff)

- `Split_parquets`:
  - Not saved to remote repo
  - These files are split along the same timestamps as the .dcd trajectory files. Includes the absolute path to a trajectory file in which a molecule can be found/extracted

- `Sync_to_mac`:
  - Not saved to remote repo
  - Used to send files (via sshfs) between my MacBook and this directory on HPG

- `Trimmed_frames`:
  - Spot to dump isolated frames of the trajectory for further analysis of specific frames.

- `_broken`:
  - Not saved to remote repo
  - Explains itself; where I put scripts and outputs that didn't work as expected, but probably want to hang onto

- `_testing`:
  - Not saved to remote repo
  - Location of scripts that aren't yet ready to run (or things I don't want to delete, timing tests, etc.)

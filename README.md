Usage and some notes:

The topology of the 22.8M atom simulation is saved from frame 0 of the 0.0ns .dcd trajectory file
    * Loading this topology from original pdb is very slow (approx 8-10 minutes)
    * Loading from a .h5 slice of the first frame of trajectory data takes ~200 sec with default MDTraj function
    * Loading from this .h5 slice with 'top_loader.py' (thanks Ignacio) takes approximately 85 sec

Scripts found in this directory:
    * batch_submit.sh
        Used to submit extraction script such that different trajectory splits (0.1ns each) are ran in parallel

    * extract_coordinates.py
        This script opens a trajectory file and extracts coordinates of 'found' molecules (from the pubchem dataframe)
    
    * top_loader.py
        This script is used to load a topology in mdtraj from a single-frame slice of the trajectory
        (Using the zeroth-frame of the 0.0ns traj file, stored in 'traj_top_0.0ns.h5')
        The purpose is to load in a massive (22.8M atom) topology more efficiently than the pdb loader

Other files located here:
    * 22M_topology.pdb:
        Original topology Richard used for his simulation 

    * merged_formula.pq:
        A dataframe containing all 'molecules' found in the graph search. No atom_indices are included, but frame#, formula are saved here for every graph found at every frame (~570M rows, big dataframe)

    * traj_top_0.0ns.h5:
        The hdf stored topology used with 'top_loader.py' script

Some directories and their contents: 
    * _broken:
        Explains itself; where I put scripts and outputs that didn't work as expected, but probably want to hang onto

    * _testing:
        Location of scripts that aren't yet ready to run (or things I don't want to delete, timing tests, etc.)

    * Alanine:
        Contains scripts, outputs, analysis related to extracted alanine molecules

    * Coordinate_hdf:
        (WIP) Here is where I want to include HDFs with coordinates for ALL 'found' molecules in the EE simulation
        Needs work, there's only a few h5 files here, the others have not been generated yet

    * Old_outputs:
        .txt and .log files from scripts, only keeping for timing/job execution details 

    * Scripts:
        (WIP) Location for general scripts (after adapting from Ala stuff)

    * Split_parquets:
        These files are split along the same timestamps as the .dcd trajectory files
        Includes the absolute path to a trajectory file in which a molecule can be found/extracted

    * Sync_to_mac:
        Used to send files (via sshfs) between my macbook and this directory on hpg


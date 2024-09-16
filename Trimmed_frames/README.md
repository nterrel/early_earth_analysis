# Directory to dump individual frames split off of the 22.8M trajectory

## Ala_synthesis contains 12 (randomly selected) frames that contain alanine molecules

- Isolated to watch the synthesis of Alanine, and compare before / after the quench restart runs

- Hoping to see multiple paths to synthesizing alanine molecules.


## This directory contains frames 1608-1629 to have a small subset of the overall trajectory for testing things on.

## Other scripts

- `join_traj_frames.py` joins the individual frames saved in this directory into a combined traj file named `trimmed_1608-1629_1.2ns.dcd`.
  - Script to combine single frames into a continuous traj -- created because it is easier to split off one specific frame than it is to split a range of frames. 

- `last_frame.py` is a script used for isolating a single frame from a trajectory

- `split_some_frames.py` was used to split off 3 frames of interest from the original trajectory.

- `split_traj.py` was used to split off the individual frames (1608-1629) into individual dcd files. This script was adapted from `split_ala_frames.py`, which is located in a subdirectory of this dir.
  - Create a small trajectory for testing molfind program on (~20 frames).

- `submit_join_frames.sh` is a SLURM submission script to run `join_traj_frames.py`

- `submit_some_frames.sh` is a SLURM submission script to run `split_some_frames.py`

- `submit_split_traj.sh` is a SLURM submission script to run `split_traj.py`
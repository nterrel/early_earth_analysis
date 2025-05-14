# Some scripts that have limited utility, but may contain some useful snippets

`concatenate_trajectories.py`: Script that I decided against using, in lieu of just running the analyses on one-frame trajectory files and concatenating the pandas dataframes output by the analysis scripts. (This is because loading many frames of the traj quickly occupies RAM and it is difficult to )

`dcd_mapping.py` is used to determine timestamps -- since i ran this once there should be a parquet with all the correct timestamped filenames in `/red/roitberg/nick_analysis`.

`dcd2data.py` makes a .data file for lammps input from an input dcd -- used to make starting configurations for quench runs.

`DONT_USE_convert_dcd_to_pdb.py` this script "works" but not really, it produces a PDB in a format that doesn't play nicely with Richard's pdbfixer, makes all the masses wrong. Rather than just fix it, I created a different script (which can be found in `nick_analysis/Restart`).

`reservation_test.sh` tests the reservation given to us to run last-ditch effort analyses before I graduated.

`sample.sh` is just a basic example of a SLURM submission script.

`submit_concat.sh` is a SLURM script to run the python script `concatenate_trajectories.py`.

`submit_last_frame.sh` is used to submit `last_frame.py` to the SLURM scheduler.

`WORKS_BUT_SLOW_dcd2data.py` is an old version of `dcd2data.py` which reloads the topology each time it writes a data file, so it was too slow to be useful while I was racing against the clock for that week-long reservation of the four nodes. As with `DONT_USE_convert_dcd_to_pdb.py`, the newer (working) version of this script is present in `nick_analysis`.




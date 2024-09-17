# Restarting the 22.8M atom simulation run

* The first frame analyzed was 196366, not for any particular reason, just a good middle point of the simulation. Use this as a starting point for understanding the process used to restart a frame for the quench, and to run the analysis of minimized frames. 

## Subdirectories for specific frames

* Frame 24221
  * Frame containing the most found molecules (that are included in the molfind database)

* Frame 196366
  * Sliced from 2.4ns of original trajectory
  * Alanin-containing frame
  * WIP: Trying to restart simulation with this frame first, eventually edit molfind to trace synthesis backwards

* Frames 23406, 39901, 48938, 53726, 71744, 102584, 127761, 164418, 166471, 224713, 290169, 344041
  * Randomly selected alanine-containing frames, sliced in the same way as 196366
  * Isolated in order to trace alanine synthesis backwards thru the simulation run, to try and identify multiple pathways to synthesize the molecule.

* Frames 256780 and 256786 contain the 96 and 91 atom molecules respectively

* Frame 344041
  * Frame containing the most found formulas

## Scripts located here

* `batch_submit_molfind.sh`:
  * Iterates over directories with the name 'frame_*' and submit both the original and quenched analysis, create subdirectories to place the parquets created, then move on to the next directory. If this works, will run it just like that on the 400 random frames.

* `concatenate_parquets.py`:
  * Iterate over `frame_*` directories and looks for folders named `original_analyze` or `quench_analyze`, then looks for parquets and concatenates them into a single, unified dataframe.
  * Drops the 'time' and 'local_frame' columns, shouldn't need since saving correct absolute frame number. 

* `create_analysis_scripts.sh`:
  * Writes SLURM submission files autonomously for the directories named `frame_NUMBER` which contain a logs directory with a .dcd file.

* `run_22.8M_quench.py`:
  * LAMMPS runner script -- hasn't been edited really at all, except run_steps.

# Analysis of 400 random frames from the 4 nanoseconds of high-temperature run

## Subdirectories

* `frame_NUMBER`:
  * Contain files pertaining to the specified frame number, including LAMMPS restart input files, outputs, and analysis outputs.

* `miscellaneous`:
  * One-off scripts, scripts that didn't prove useful, etc. Dumping grounds for things I probably won't need again.

## Scripts located here

* `batch_submit_molfind.sh`:
  * Iterates over directories with the name 'frame_*' and submit both the original and quenched analysis, create subdirectories to place the parquets created, then move on to the next directory. If this works, will run it just like that on the 400 random frames.

* `batch_submit.sh`:
  * Checks for the existence of .data files in subdirectories, creates a LAMMPS runner shell script, and submits the job with a dependency to only run after the previous job is completed / cancelled.
  * It also iteratively checks for new shell scripts and submits those jobs (within some time limit)

* `concatenate_parquets.py`:
  * Iterate over `frame_*` directories and looks for folders named `original_analyze` or `quench_analyze`, then looks for parquets and concatenates them into a single, unified dataframe.
  * Drops the 'time' and 'local_frame' columns, shouldn't need since saving correct absolute frame number. 

* `create_analysis_scripts.sh`:
  * Writes SLURM submission files autonomously for the directories named `frame_NUMBER` which contain a logs directory with a .dcd file.

* `rename_logs_files.sh`:
  * Didn't edit the `in.22M.quench.lammps` file to have the correct frame number in output file names, but they were placed in the right directories, so this script iterates over the directories and renames the LAMMPS output logs.

* `run_22.8M_quench.py`:
  * LAMMPS runner script -- hasn't been edited really at all, except run_steps.

* `sort_logs.sh`:
  * LAMMPS output is saved to this directory, so this script just pulls the frame_number out of the LAMMPS log and places it in the correct directory.

* `split_400_frames.py`:
  * How the 400 frames were randomly selected and split from the original trajectory.

* `split_random_frames.sh`:
  * SLURM script to accomplish the job set up by `split_400_frames.py`.
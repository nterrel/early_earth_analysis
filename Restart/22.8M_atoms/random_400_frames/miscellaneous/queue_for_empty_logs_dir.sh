#!/bin/bash
#SBATCH --job-name=submit_lammps_jobs
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2gb
#SBATCH --time=01:00:00
#SBATCH --output=submit_lammps_jobs_%j.log

# This script checks for 'frame_*' directories, verifies if their 'logs' subdirectory is empty,
# and submits the corresponding shell scripts for those directories.

parent_dir="/red/roitberg/nick_analysis/Restart/22.8M_atoms/random_400_frames"

for frame_dir in "$parent_dir"/frame_*; do
    logs_dir="${frame_dir}/logs"
    slurm_script="${frame_dir}/submit.32gpu.$(basename "$frame_dir" | sed 's/frame_//').quench.sh"

    # Check if the logs directory exists and is empty, and if the submission script exists
    if [[ -d "$logs_dir" && ! "$(ls -A "$logs_dir")" && -f "$slurm_script" ]]; then
        echo "Logs directory is empty for $frame_dir. Submitting $slurm_script..."
        sbatch "$slurm_script"
    else
        if [[ ! -d "$logs_dir" ]]; then
            echo "Logs directory does not exist for $frame_dir. Skipping..."
        elif [[ "$(ls -A "$logs_dir")" ]]; then
            echo "Logs directory is not empty for $frame_dir. Skipping..."
        elif [[ ! -f "$slurm_script" ]]; then
            echo "Submit script does not exist for $frame_dir. Skipping..."
        fi
    fi
done

echo "Submission complete."

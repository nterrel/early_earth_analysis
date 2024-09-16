#!/bin/bash

# NOTE: This script is intended to iterate over directories with the name 'frame_*' and submit both the original and quenched analysis, create subdirectories to place the parquets created, then move on to the next directory. If this works, will run it just like that on the 400 random frames. 

# Path to directory where frame_NUMBER directories are located
base_dir="/red/roitberg/nick_analysis/Restart/22.8M_atoms/random_400_frames"

# Iterate over each frame dir
for frame_dir in "$base_dir"/frame_*; do
    frame_num=$(basename "$frame_dir" | cut -d'_' -f2)

    # Paths to submission scripts
    original_script="${frame_dir}/submit_original_${frame_num}_analyze.sh"
    quench_script="${frame_dir}/submit_quenched_${frame_num}_analyze.sh"

    # Check if original script exists before submitting
    if [[ -f "$original_script" ]]; then
	echo "Submitting original analysis job for frame_${frame_num}"
	original_job_id=$(sbatch --parsable "$original_script")
	echo "Original analysis job for frame_${frame_num} submitted with the Job ID: $original_job_id"
    else
	echo "Original analysis script not found for frame_${frame_num}, skipping."
    fi

    # Check if quenched analysis script exists and submit it
    if [[ -f "$quench_script" ]]; then
	echo "submitting quenched analysis job for frame_${frame_num}"
	quench_job_id=$(sbatch --parsable "$quench_script")
	echo "Quenched analysis job for frame_${frame_num} submitted with Job ID: $quench_job_id"
    else
	echo "Quenched analysis script not found for frame_${frame_num}, skipping."
    fi
done

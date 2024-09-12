#!/bin/bash

# Using the `missing_log_dir.txt` file, iterate over the directories specified and submit their associated shell script to restart LAMMPS job. 

# Initialize an empty variable to hold the job ID for the dependency chain
prev_job_id=""

# Read each line (directory path) from the file
while IFS= read -r dir; do
    # Check if the directory exists (in case any paths are invalid)
    if [ -d "$dir" ]; then
        # Find the submit.32gpu.*.quench.sh script
        submit_script=$(find "$dir" -name "submit.32gpu.*.quench.sh")

        if [ -n "$submit_script" ]; then
            # Submit the job with a dependency if there's a previous job ID
            if [ -n "$prev_job_id" ]; then
                job_id=$(sbatch --dependency=afterany:$prev_job_id "$submit_script" | awk '{print $4}')
            else
                # First job submission without a dependency
                job_id=$(sbatch "$submit_script" | awk '{print $4}')
            fi

            # Update the prev_job_id to chain the next job
            prev_job_id=$job_id
            echo "Submitted $submit_script with job ID $job_id"
        else
            echo "No submit script found in $dir"
        fi
    else
        echo "$dir is not a valid directory"
    fi
done < missing_log_dirs.txt


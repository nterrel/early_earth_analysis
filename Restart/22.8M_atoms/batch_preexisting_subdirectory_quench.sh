#!/bin/bash

# Define the parent directory with the wildcard pattern for frame directories
parent_dir="/red/roitberg/nick_analysis/Restart/22.8M_atoms/frame*"

# Find all directories that match the pattern "frame_*" and search for submit scripts in those directories
submit_scripts=$(find $parent_dir -type f -name 'submit.32gpu.*.quench.sh' | sort)

# Initialize the job dependency chain
previous_job_id=""

# Loop over each submit script and submit the job with dependency
for script in $submit_scripts; do
    # Submit the first job without any dependency
    if [[ -z "$previous_job_id" ]]; then
        previous_job_id=$(sbatch "$script" | awk '{print $4}')
    else
        # Submit the next job with a dependency on the previous job
        previous_job_id=$(sbatch --dependency=afterany:$previous_job_id "$script" | awk '{print $4}')
    fi
    echo "Submitted job for script $script with Job ID $previous_job_id"
done

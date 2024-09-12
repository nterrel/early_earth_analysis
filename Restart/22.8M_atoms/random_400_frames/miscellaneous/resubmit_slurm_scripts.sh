#!/bin/bash

# File containing the scripts to resubmit
scripts_file="scripts_to_resubmit.txt"

# Set the current running job as the first dependency
job_id="44196625"
echo "Starting with dependency on Job ID $job_id"

# Submit the scripts with the first job dependency
while read script; do
    if [[ ! -z "$script" ]]; then
        # Submit the next job with dependency on the previous job (initially the running job)
        new_job_id=$(sbatch --dependency=afterok:$job_id "$script" | awk '{print $4}')
        echo "Submitted $script with dependency on Job ID $job_id, new Job ID $new_job_id"
        
        # Update job_id to the new one
        job_id=$new_job_id
    fi
done < "$scripts_file"

#!/bin/bash

# I made the mistake of submitting a bunch of duplicate jobs, but didn't set them to run only after a previous job finished, so they have a different 'NODELIST(REASON)' pending statement. I can use that to cancel any jobs with 'QOSGrpGRES' as the reason for not running yet. 

# Get the list of job IDs that are in the 'QOSGrpGRES' state
job_ids=$(squeue --user=$(whoami) --format="%i %r" | grep 'QOSGrpGRES' | awk '{print $1}')

# Check if there are any jobs to cancel
if [[ -z "$job_ids" ]]; then
    echo "No jobs with the 'QOSGrpGRES' reason found."
else
    echo "Cancelling the following jobs with the 'QOSGrpGRES' reason:"
    echo "$job_ids"

    # Cancel each job with the 'QOSGrpGRES' flag
    for job_id in $job_ids; do
        scancel "$job_id"
        echo "Cancelled job $job_id"
    done
fi

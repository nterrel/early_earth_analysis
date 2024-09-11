
#!/bin/bash

# Script to figure out which jobs are not able to run before midnight -- when the `roitberg` reservation ends.

# Write list of scripts to resubmit to some text file
output_file="scripts_to_resubmit.txt"

# Empty output file if it exists
> "$output_file"

job_ids=$(squeue -u nterrel --state=PENDING --format="%i %r" | grep 'Dependency' | awk '{print $1}')

if [[ -z "$job_ids" ]]; then
	echo "No jobs with Dependency found."
	exit 0
fi

for job_id in $job_ids; do
	submit_script=$(scontrol show job "$job_id" | grep -oP '(?<=Command=).+')

    # Check if we found a valid submit script path
    if [[ -n "$submit_script" ]]; then
        echo "Found submit script for job $job_id: $submit_script"
        echo "$submit_script" >> "$output_file"
    else
        echo "No valid submit script found for job $job_id"
    fi
done

echo "Submit scripts saved to $output_file"


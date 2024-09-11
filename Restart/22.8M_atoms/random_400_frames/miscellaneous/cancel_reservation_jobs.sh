#!/bin/bash

# Didn't get to run all my jobs before the reservation ended, so need to cancel those which are sitting on the queue pending for a reservation that no longer exists. 

# Get the list of job IDs where the reason contains "Reservation roitberg was deleted"
job_ids=$(squeue -u nterrel --format="%A %R" | grep "Reservation roitberg was deleted" | awk '{print $1}')

# Cancel each job
for job_id in $job_ids; do
    echo "Cancelling Job ID: $job_id"
    scancel $job_id
done
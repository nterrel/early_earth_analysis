#!/bin/bash
#SBATCH --job-name=resource_monitor
#SBATCH --ntasks=1
#SBATCH --time=01:00:00
#SBATCH --output=resource_monitor_%j.log

# Replace this with your job ID
JOB_ID=22217205

# Time interval for checks (in seconds)
INTERVAL=120

# Monitor until the job is running
while squeue -j $JOB_ID | grep -q $JOB_ID
do
    echo "---- $(date) ----"
    echo "Resource usage for job $JOB_ID:"
    
    # CPU usage
    echo "CPU Usage:"
    sstat -j $JOB_ID --format=AveCPU

    # Memory usage
    echo "Memory Usage:"
    sstat -j $JOB_ID --format=MaxRSS

    # Wait for the next interval
    sleep $INTERVAL
done

echo "Monitoring complete. Job $JOB_ID has finished."


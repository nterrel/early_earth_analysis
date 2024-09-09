#!/bin/bash

# The way I automated writing shell scripts to submit LAMMPS restart jobs makes logs print to this parent directory, so this script is just used to sort those output logs into the proper directories. 

# Loop through all lammps log files in the current directory
for log_file in lammps_ani_*.log; do
    # Extract the frame number from the log file name (assumes format like lammps_ani_<frame_number>_<job_id>.log)
    frame_number=$(echo "$log_file" | cut -d'_' -f3)
    
    # Check if the corresponding frame directory exists
    frame_dir="frame_${frame_number}/"
    if [ -d "$frame_dir" ]; then
        # Move the log file into the corresponding frame directory
        mv "$log_file" "$frame_dir"
        echo "Moved $log_file to $frame_dir"
    else
        echo "Directory $frame_dir not found for log file $log_file"
    fi
done


#!/bin/bash

# This script just looks through subdirectories (move it up one dir if you need to reuse) to look for missing `lammps_ani*log` files and saves them to a text file.

# Find all frame_NUMBER directories that do not contain a file matching 'lammps_ani*log'
for dir in frame_*; do
    if [ -d "$dir" ]; then
        # Check if no files matching 'lammps_ani*log' exist in the directory
        if ! ls "$dir"/lammps_ani*log 1> /dev/null 2>&1; then
            echo "$dir" >> missing_log_dirs.txt
        fi
    fi
done

echo "Directories without lammps_ani*log file have been saved to missing_log_dirs.txt"


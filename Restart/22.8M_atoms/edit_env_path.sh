#!/bin/bash

# Path to the base directory where frame_NUMBER directories are located
base_dir="/red/roitberg/nick_analysis/Restart/22.8M_atoms"

# Find all shell scripts in the frame directories and update the conda activate line
find "$base_dir" -type f -name "submit_*_analyze.sh" | while read -r script; do
    # Use sed to replace the specific line in each script
    sed -i 's|conda activate /blue/roitberg/jinzexue/program/miniconda3/envs/rapids-23.10/|conda activate rapids-23.10|' "$script"
    echo "Updated conda activate line in $script"
done


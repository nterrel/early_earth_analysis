#!/bin/bash

# Define the path to the parent directory where the frame directories are located
parent_dir="/red/roitberg/nick_analysis/Restart/22.8M_atoms/random_400_frames"

# Loop through the directories that match the pattern "frame_*"
for dir in "$parent_dir"/frame_*; do
    # Extract the frame number from the directory name
    frame_num=$(basename "$dir" | sed 's/frame_//')

    # Check if the frame number is between 0-16000 or 336000-352000
    if [[ $frame_num -ge 0 && $frame_num -le 16000 ]] || [[ $frame_num -ge 336000 && $frame_num -le 352000 ]]; then
        # Delete the directory if it matches the criteria
        echo "Deleting $dir..."
        rm -r "$dir"
    else
        echo "Keeping $dir..."
    fi
done

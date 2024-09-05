#!/bin/bash

# Define the parent directory where all frame directories are located
parent_dir="/red/roitberg/nick_analysis/Restart/22.8M_atoms/random_400_frames"

# Find all directories that match the pattern "frame_*"
directories=$(find "$parent_dir" -maxdepth 1 -type d -name "frame_*")

# Loop over each directory
for dir in $directories
do
    echo "Processing $dir..."

    # Find the .dcd file in the current directory
    dcd_file=$(ls "$dir"/*.dcd)

    # Extract the current frame number from the directory name
    frame_number=$(basename "$dir")

    # Extract the timestamp and ns part from the existing file name
    # This looks for the last occurrence of the number before "ns"
    if [[ $dcd_file =~ ([0-9.]+)ns ]]; then
        timestamp=${BASH_REMATCH[1]}
    else
        echo "Could not find timestamp in $dcd_file"
        continue
    fi

    # Create the new file name in the format: frame_x_y.zns_original.dcd
    new_dcd_file="$dir/${frame_number}_${timestamp}ns_original.dcd"

    # Rename the file
    mv "$dcd_file" "$new_dcd_file"

    echo "Renamed $dcd_file to $new_dcd_file"
done

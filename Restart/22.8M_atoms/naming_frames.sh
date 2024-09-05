#!/bin/bash

# Define the directories containing the frames
directories=(
    "frame_127761"
    "frame_166471"
    "frame_224713"
    "frame_24221"
    "frame_256786"
    "frame_48938"
    "frame_71744"
    "frame_102584"
    "frame_164418"
    "frame_196366"
    "frame_23406"
    "frame_256780"
    "frame_290169"
    "frame_39901"
    "frame_53726"
)

# Loop over each directory
for dir in "${directories[@]}"
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

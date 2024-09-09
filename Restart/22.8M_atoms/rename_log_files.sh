#!/bin/bash

parent_dir="/red/roitberg/nick_analysis/Restart/22.8M_atoms"

for frame_dir in "$parent_dir"/frame_*; do
    frame_number=$(basename "$frame_dir" | sed 's/frame_//')
    logs_dir="${frame_dir}/logs"
    if [[ -d "$logs_dir" ]]; then
        echo "Processing logs for frame $frame_number..."
        for file in "$logs_dir"/*196366_quench.*; do
            if [[ -f "$file" ]]; then
                new_file=$(echo "$file" | sed "s/196366/$frame_number/g")
                mv "$file" "$new_file"
                echo "Renamed $file to $new_file"
            fi
        done
    else
        echo "Logs directory does not exist for frame $frame_number, skipping..."
    fi
done

echo "All files renamed successfully."
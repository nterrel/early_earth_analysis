#!/bin/bash

cd /red/roitberg/nick_analysis/unique_fragment_analysis

echo "🧹 Filtering slurm scripts by missing log segments..."

for slurm_file in slurm_scripts/*.slurm; do
    # Extract the segment pattern: e.g., 0.1ns_segment_12_of_20
    segment_key=$(basename "$slurm_file" .slurm | grep -o '[0-9.]\+ns_segment_[0-9]\+_of_[0-9]\+')

    # Check if any log file contains this segment pattern
    if ls logs/*"$segment_key"* &>/dev/null; then
        echo "⏭️  Skipping $slurm_file (log exists for segment $segment_key)"
    else
        echo "🟢 Submitting $slurm_file (no log for $segment_key)"
        sbatch "$slurm_file"
        sleep 0.02
    fi
done
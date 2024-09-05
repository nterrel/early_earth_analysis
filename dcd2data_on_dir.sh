#!/bin/bash
#SBATCH --job-name=dcd2data
#SBATCH --ntasks=1
#SBATCH --mem=120gb
#SBATCH --time=04:00:00
#SBATCH --output=/red/roitberg/nick_analysis/dcd2data_%j.log
#SBATCH --output=dcd2data_%j.out       # Output file

directories=(
    "frame_23406"
    "frame_24221"
    "frame_39901"
    "frame_48938"
    "frame_53726"
    "frame_71744"
    "frame_102584"
    "frame_127761"
    "frame_164418"
    "frame_166471"
    "frame_224713"
    "frame_256780"
    "frame_256786"
    "frame_290169"
)

# Loop over the specified directories
for dir in "${directories[@]}"
do
    echo "Processing $dir..."

    # Define the paths to the DCD, XYZ, PDB, and DATA files
    dcd_file="$dir/${dir}_original.dcd"
    xyz_file="$dir/${dir}.xyz"
    pdb_file="$dir/${dir}.pdb"
    data_file="$dir/${dir}.data"

    # Run the python script to iterate over the directory
    python dcd2data.py "$dcd_file" "$topology_file" "$xyz_file" "$pdb_file" "$data_file"

    echo "Finished processing $dir"
done

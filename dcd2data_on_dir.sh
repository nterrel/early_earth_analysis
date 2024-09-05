#!/bin/bash
#SBATCH --job-name=dcd2data
#SBATCH --ntasks=1
#SBATCH --mem=120gb
#SBATCH --time=04:00:00
#SBATCH --output=/red/roitberg/nick_analysis/dcd2data_%j.log
#SBATCH --output=dcd2data_%j.out       # Output file
#SBATCH --error=dcd2data_%j.err        # Error file

directories=(
    "frame_23406",
    "frame_24221",  # NEED TO CREATE FRAME FOR THIS DIR
    "frame_39901",
    "frame_48938",
    "frame_53726",
    "frame_71744",
    "frame_102584",
    "frame_127761",
    "frame_164418",
    "frame_166471",
    "frame_224713",
    "frame_256780",  # NEED TO CREATE FRAME FOR THIS DIR
    "frame_256786",  # NEED TO CREATE FRAME FOR THIS DIR
    "frame_290169"
)

module load conda
conda activate /blue/roitberg/apps/torch1121


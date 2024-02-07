#!/bin/bash
#SBATCH --job-name=extract_coordinates
#SBATCH --ntasks=1
#SBATCH --mem=128gb
#SBATCH --time=04:00:00
#SBATCH --output=/red/roitberg/nick_analysis/extract_coords_%j.log

module load conda
conda activate /blue/roitberg/apps/torch1121
python /red/roitberg/nick_analysis/extract_coordinates.py &> /red/roitberg/nick_analysis/extract_coords_out.txt

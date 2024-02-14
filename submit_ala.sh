#!/bin/bash
#SBATCH --job-name=extract_coordinates
#SBATCH --ntasks=1
#SBATCH --mem=64gb
#SBATCH --time=01:00:00
#SBATCH --output=/red/roitberg/nick_analysis/extract_ala_%j.log

module load conda
conda activate /blue/roitberg/apps/torch1121
python /red/roitberg/nick_analysis/extract_ala.py &> /red/roitberg/nick_analysis/extract_ala_out.txt

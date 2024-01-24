#!/bin/bash
#SBATCH --job-name=extract_ala_structures
#SBATCH --ntasks=1
#SBATCH --mem=64gb
#SBATCH --time=01:30:00
#SBATCH --output=/blue/roitberg/nterrel/extract_ala.log

module load conda
conda activate /blue/roitberg/apps/torch1121
python /red/roitberg/nick_analysis/extract_ala_structures.py > /blue/roitberg/nterrel/extract_ala_out.txt
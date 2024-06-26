#!/bin/bash
#SBATCH --job-name=extract_coords
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=256gb
#SBATCH --time=48:00:00
#SBATCH --output=/red/roitberg/nick_analysis/extract_coord_%j.log

module load conda
conda activate /blue/roitberg/apps/torch1121
python /red/roitberg/nick_analysis/extract_general.py &> /red/roitberg/nick_analysis/extract_general_out.txt

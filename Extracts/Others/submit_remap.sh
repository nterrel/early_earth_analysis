#!/bin/bash
#SBATCH --job-name=remap_coords
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=64gb
#SBATCH --time=48:00:00
#SBATCH --output=/red/roitberg/nick_analysis/remap_coord_%j.log

module load conda
conda activate nick_earlyearth
python /red/roitberg/nick_analysis/Extracts/Others/remap_general.py &> /red/roitberg/nick_analysis/Extracts/Others/remap_general_out.txt

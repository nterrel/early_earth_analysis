#!/bin/bash
#SBATCH --job-name=split_ala_frames
#SBATCH --ntasks=1
#SBATCH --mem=256gb
#SBATCH --time=04:00:00
#SBATCH --output=/red/roitberg/nick_analysis/split_ala_%j.log
#SBATCH --output=split_ala_%j.out       # Output file
#SBATCH --error=split_ala_%j.err        # Error file

module load conda
conda activate /blue/roitberg/apps/torch1121
cd /red/roitberg/nick_analysis/
python /red/roitberg/nick_analysis/split_ala_frames.py &> /red/roitberg/nick_analysis/split_ala_frames.txt

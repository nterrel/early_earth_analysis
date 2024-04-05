#!/bin/bash
#SBATCH --job-name=mdconvert_traj
#SBATCH --ntasks=1
#SBATCH --mem=128gb
#SBATCH --time=02:00:00
#SBATCH --output=/red/roitberg/nick_analysis/mdconvert_traj_%j.log

module load conda
conda activate /blue/roitberg/apps/torch1121
python /red/roitberg/nick_analysis/mdconvert.py &> /red/roitberg/nick_analysis/mdconvert.txt

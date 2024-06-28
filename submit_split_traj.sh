#!/bin/bash
#SBATCH --job-name=split_big_traj
#SBATCH --ntasks=1
#SBATCH --mem=400gb
#SBATCH --time=02:00:00
#SBATCH --output=/red/roitberg/nick_analysis/split_traj_%j.log
#SBATCH --output=split_traj_%j.out       # Output file
#SBATCH --error=split_traj_%j.err        # Error file

module load conda
conda activate /blue/roitberg/apps/torch1121
python /red/roitberg/nick_analysis/split_traj.py &> /red/roitberg/nick_analysis/split_traj.txt

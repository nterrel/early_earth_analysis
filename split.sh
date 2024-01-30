#!/bin/bash
#SBATCH --job-name=split_trajectory
#SBATCH --ntasks=1
#SBATCH --mem=64gb
#SBATCH --time=01:00:00
#SBATCH --output=/red/roitberg/nick_analysis/split_traj_%j.log

module load conda
conda activate /blue/roitberg/apps/torch1121
python /red/roitberg/nick_analysis/split_traj_testing.py &> /red/roitberg/nick_analysis/split_traj.txt

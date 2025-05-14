#!/bin/bash
#SBATCH --job-name=dcd2data
#SBATCH --ntasks=1
#SBATCH --mem=120gb
#SBATCH --time=60:00:00
#SBATCH --output=dcd2data_%j.out
#SBATCH --error=dcd2data_%j.err

# Define the parent directory where all frame directories are located
parent_dir="/red/roitberg/nick_analysis/Restart/22.8M_atoms/random_400_frames"

module load conda
conda activate /blue/roitberg/apps/torch1121

python dcd2data.py traj_top_0.0ns.h5 "$parent_dir"

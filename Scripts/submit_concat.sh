#!/bin/bash
#SBATCH --job-name=trajectory_concatenation
#SBATCH --output=traj_concat_%j.log
#SBATCH --error=traj_concat_%j.err
#SBATCH --time=16:00:00
#SBATCH --mem=256gb

module load conda
conda activate /blue/roitberg/apps/torch1121

python concatenate_trajectories.py
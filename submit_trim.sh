#!/bin/bash
#SBATCH --job-name=split_ala_traj
#SBATCH --ntasks=1
#SBATCH --mem=128gb
#SBATCH --time=08:00:00
#SBATCH --output=/red/roitberg/nick_analysis/split_traj_%j.log
#SBATCH --output=split_traj_%j.out       # Output file
#SBATCH --error=split_traj_%j.err        # Error file

module load conda
conda activate /red/roitberg/conda-envs/envs/rapids-23.10
python /red/roitberg/nick_analysis/split_ala_traj.py &> /red/roitberg/nick_analysis/split_ala_traj.txt

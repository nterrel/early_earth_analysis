#!/bin/bash
#SBATCH --mem=256G
#SBATCH --cpus-per-task=32
#SBATCH --time=04:00:00
#SBATCH --job-name=count_unique_signatures
source ~/.bashrc
conda activate rapids-23.10
python /red/roitberg/nick_analysis/unique_fragment_analysis/count_signatures.py


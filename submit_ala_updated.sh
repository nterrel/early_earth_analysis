#!/bin/bash
#SBATCH --job-name=extract_ala
#SBATCH --ntasks=1
#SBATCH --mem=32gb
#SBATCH --time=48:00:00
#SBATCH --output=/red/roitberg/nick_analysis/extract_ala_%j.log

module load conda
conda activate /blue/roitberg/apps/torch1121
python /red/roitberg/nick_analysis/extract_ala_updated.py &> /red/roitberg/nick_analysis/extract_ala_updated_out_continued.txt

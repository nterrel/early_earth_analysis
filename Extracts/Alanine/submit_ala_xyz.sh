#!/bin/bash
#SBATCH --job-name=ala_coords
#SBATCH --ntasks=1
#SBATCH --mem=32gb
#SBATCH --time=48:00:00
#SBATCH --output=/red/roitberg/nick_analysis/Ala_df/ala_coords_%j.log

module load conda
conda activate /blue/roitberg/apps/torch1121
python /red/roitberg/nick_analysis/updated_generate_xyz.py &> /red/roitberg/nick_analysis/Ala_df/ala_coord_out.txt

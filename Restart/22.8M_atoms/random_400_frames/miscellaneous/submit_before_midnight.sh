#!/bin/bash
#SBATCH --job-name=gather_submit_scripts
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1gb
#SBATCH --output=gather_submit_scripts_%j.log
#SBATCH --time=01:00:00
#SBATCH --begin=23:58:00 
# Set the job to begin at 11:58 PM HPC time

# Simple script to schedule a tracker for what things aren't able to run before 'roitberg' reservation runs out

# Load necessary modules or activate environments if needed
module activate conda
conda activate /blue/roitberg/apps/torch1121

# Run the gather script
./jobs_to_resubmit.sh


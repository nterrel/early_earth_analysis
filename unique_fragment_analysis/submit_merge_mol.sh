#!/bin/bash
#SBATCH --job-name=merge_molecule
#SBATCH --ntasks=1
#SBATCH --mem=450gb
#SBATCH --time=08:00:00
#SBATCH --output=merge_pq_%j.out
#SBATCH --error=merge_pq_%j.err

python /red/roitberg/nick_analysis/unique_fragment_analysis/merge_mol_pq.py


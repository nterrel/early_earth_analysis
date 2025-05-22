#!/bin/bash
#SBATCH --job-name=write_job_scripts
#SBATCH --output=write_job_scripts_%j.out
#SBATCH --error=write_job_scripts_%j.err
#SBATCH --time=01:00:00
#SBATCH --mem=4gb

# Activate environment
source $(conda info --base)/etc/profile.d/conda.sh
conda activate /red/roitberg/conda-envs/envs/rapids-23.10

# Change to working directory
cd /red/roitberg/nick_analysis/unique_fragment_analysis

# Run job generation script (NO -y)
python /red/roitberg/lammps-ani/cumolfind/restart_submit_analysis.py \
    --traj=/red/roitberg/22M_20231222_prodrun/ \
    --top=/red/roitberg/nick_analysis/traj_top_0.0ns.h5 \
    --num_segments=20 \
    --mol_pq=/red/roitberg/nick_analysis/reduced_all_mol.pq \
    --output_dir=/red/roitberg/nick_analysis/RESTART_new_unique_fragment_analysis

echo "✅ All .slurm job scripts written to slurm_scripts/"
#!/bin/bash
#SBATCH --job-name=re48906311_molfind                 # Job name
#SBATCH --output=/red/roitberg/nick_analysis/re48906311_molfind_%j.out            # Output file
#SBATCH --error=/red/roitberg/nick_analysis/re48906311_molfind_%j.err             # Error file
#SBATCH --partition=gpu                                          # Partition name
#SBATCH --mem=64gb                                              # Memory per node
#SBATCH --time=24:00:00                                          # Time limit
#SBATCH --gres=gpu:a100:1                                        # Number of GPUs
#SBATCH --ntasks=1                                               # Number of tasks (processes)
#SBATCH --cpus-per-task=1                                        # Number of CPU cores per task (adjust as necessary)

echo "Date              = $(date)"
echo "Hostname          = $(hostname -s)"
echo "Working Directory = $(pwd)"
echo ""
echo "Number of Nodes Allocated      = $SLURM_JOB_NUM_NODES"
echo "Number of Tasks Allocated      = $SLURM_NTASKS"
echo "Number of Cores/Task Allocated = $SLURM_CPUS_PER_TASK"

export LAMMPS_ANI_ROOT="/blue/roitberg/nterrel/lammps-ani"
export LAMMPS_ROOT=${LAMMPS_ANI_ROOT}/external/lammps/
export LAMMPS_PLUGIN_PATH=${LAMMPS_ANI_ROOT}/build/

source $(conda info --base)/etc/profile.d/conda.sh
conda activate rapids-23.10
echo using python: $(which python)

cumolfind-molfind /red/roitberg/22M_20231222_prodrun/2023-12-24-094959.618385_1.5ns.dcd \
                  /red/roitberg/nick_analysis/Restart/22.8M_atoms/mixture_22800000.pdb \
                  /red/roitberg/nick_analysis/all_mol_data.pq \
                  --time_offset=1.5 \
                  --dump_interval=50 \
                  --timestep=0.25 \
                  --output_dir=/red/roitberg/nick_analysis/restart_analyze \
                  --num_segments=20 \
                  --segment_index=12

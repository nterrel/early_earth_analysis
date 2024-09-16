#!/bin/bash
#SBATCH --job-name=molfind_297545_original            # Job name
#SBATCH --output=/red/roitberg/nick_analysis/Restart/22.8M_atoms/random_400_frames/frame_297545/molfind_297545_original_%j.out       # Output file
#SBATCH --error=/red/roitberg/nick_analysis/Restart/22.8M_atoms/random_400_frames/frame_297545/molfind_297545_original_%j.err        # Error file
#SBATCH --partition=gpu                                     # Partition name
#SBATCH --mem=128gb                                         # Memory per node
#SBATCH --time=02:00:00                                     # Time limit
#SBATCH --gres=gpu:a100:1                                   # Number of GPUs
#SBATCH --ntasks=1                                          # Number of tasks (processes)
#SBATCH --cpus-per-task=1                                   # Number of CPU cores per task (adjust as necessary)

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
conda activate /blue/roitberg/jinzexue/program/miniconda3/envs/rapids-23.10/  # Specify Richard's env
echo using python: $(which python)

cumolfind-molfind /red/roitberg/nick_analysis/Restart/22.8M_atoms/random_400_frames/frame_297545/frame_297545_3.7ns_original.dcd \
                  /red/roitberg/nick_analysis/Restart/22.8M_atoms/mixture_22800000.pdb \
                  /red/roitberg/nick_analysis/all_mol_data.pq \
                  --dump_interval=50 \
                  --timestep=0.25 \
                  --output_dir=/red/roitberg/nick_analysis/Restart/22.8M_atoms/random_400_frames/frame_297545/original_analyze \
                  --num_segments=1 \
                  --segment_index=0

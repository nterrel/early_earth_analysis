#!/bin/bash
#SBATCH --job-name=lammps_ani_308143
#SBATCH --ntasks=32
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=8
#SBATCH --cpus-per-task=1
#SBATCH --partition=gpu
#SBATCH --gres=gpu:a100:8
#SBATCH --mem=120gb
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=nterrel@ufl.edu
#SBATCH --time=02:00:00
#SBATCH --output=lammps_ani_308143_%j.log

echo "Date              = $(date)"
echo "Hostname          = $(hostname -s)"
echo "Working Directory = $(pwd)"
echo ""
echo "Number of Nodes Allocated      = $SLURM_JOB_NUM_NODES"
echo "Number of Tasks Allocated      = $SLURM_NTASKS"
echo "Number of Cores/Task Allocated = $SLURM_CPUS_PER_TASK"

module load cuda/11.4.3 gcc/9.3.0 openmpi/4.1.5 cmake/3.21.3 git/2.30.1
export LAMMPS_ANI_ROOT="/blue/roitberg/apps/lammps-ani"
export LAMMPS_ROOT=${LAMMPS_ANI_ROOT}/external/lammps/
export LAMMPS_PLUGIN_PATH=${LAMMPS_ANI_ROOT}/build/

source $(conda info --base)/etc/profile.d/conda.sh
conda activate /blue/roitberg/apps/torch1121
echo using python: $(which python)

python /red/roitberg/nick_analysis/Restart/22.8M_atoms/random_400_frames/run_22.8M_quench.py \
    /red/roitberg/nick_analysis/Restart/22.8M_atoms/random_400_frames/frame_308143/frame_308143.data \
    --kokkos \
    --num_gpus=32 \
    --input_file=/red/roitberg/nick_analysis/Restart/22.8M_atoms/random_400_frames/in.22M.quench.lammps \
    --log_dir=/red/roitberg/nick_analysis/Restart/22.8M_atoms/random_400_frames/frame_308143/logs \
    --ani_model_file='ani1x_nr.pt' \
    --run_name=early_earth_22M_308143_quench \
    --ani_num_models=8 \
    --timestep=0.25 \
    --run_steps=1000 \
    --run

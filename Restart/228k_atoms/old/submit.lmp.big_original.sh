#!/bin/bash
#SBATCH --job-name=lammps_ani        # Job name
#SBATCH --ntasks=8                   # Number of MPI tasks (i.e. processes)
#SBATCH --nodes=1                    # Maximum number of nodes to be allocated
#SBATCH --ntasks-per-node=8          # Maximum number of tasks on each node
#SBATCH --cpus-per-task=1            # Number of cores per MPI task
#SBATCH --partition=hpg-ai
#SBATCH --qos=roitberg
#SBATCH --account=roitberg
#SBATCH --gres=gpu:8
#SBATCH --mem=150gb           # Memory (i.e. RAM) per processor
#SBATCH --time=150:00:00              # Wall time limit (days-hrs:min:sec)
#SBATCH --output=lammps_ani_%j_1.log   # Path to the standard output and error files relative to the working dir

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

# python run_one.py mixture_228000.data --kokkos --num_gpus=8 --input_file=in.big.lammps --log_dir=logs-big-blue --ani_model_file='ani1x_nr.pt' --run_name=scale_early_earth_ani1x_nr --ani_num_models=-1 --timestep=0.25 --run

LAMMPS_ANI_PROFILING=1 mpirun -np 8 /blue/roitberg/apps/lammps-ani/external/lammps/build/lmp_mpi -var data_file mixture_228000.data -var timestep 0.25 -var run_steps 1000 -var log_dir logs-big-blue -var replicate '1 1 1' -var ani_model_file /blue/roitberg/apps/lammps-ani/tests/ani1x_nr.pt -var ani_num_models -1 -var ani_aev cuaev -var ani_neighbor full -var ani_precision single -var newton_pair on -var ani_device cuda -var timestamp 2023-10-13-092224.745990 -k on g 8 -sf kk -pk kokkos gpu/aware on -in in.big.lammps -log logs-big-blue/2023-10-13-092224.745990-kokkos-models_-1-gpus_8-mixture_228000-scale_early_earth_ani1x_nr.log

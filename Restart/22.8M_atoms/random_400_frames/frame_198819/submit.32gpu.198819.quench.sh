#!/bin/bash
#SBATCH --job-name=lammps_ani_198819        # Job name
#SBATCH --ntasks=32                  # Number of MPI tasks (i.e. processes)
#SBATCH --nodes=4                    # Maximum number of nodes to be allocated
#SBATCH --ntasks-per-node=8          # Maximum number of tasks on each node
#SBATCH --cpus-per-task=1            # Number of cores per MPI task
#SBATCH --partition=hpg-ai           # Partition   
#SBATCH --qos=roitberg               # QOS for job
#SBATCH --account=roitberg           # 
#SBATCH --reservation=roitberg       # 
#SBATCH --gres=gpu:a100:8            # GPUs per node
#SBATCH --mem=120gb                  # Memory (i.e. RAM) per node
#SBATCH --mail-type=END,FAIL         # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=nterrel@ufl.edu  # Where to send mail
#SBATCH --time=24:00:00              # Wall time limit (days-hrs:min:sec)
#SBATCH --output=lammps_ani_198819_%j.log   # Path to the standard output and error files relative to the working dir

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

python /red/roitberg/nick_analysis/Restart/22.8M_atoms/random_400_frames/run_22.8M_quench.py     /red/roitberg/nick_analysis/Restart/22.8M_atoms/random_400_frames/frame_198819/frame_198819.data     --kokkos     --num_gpus=32     --input_file=/red/roitberg/nick_analysis/Restart/22.8M_atoms/random_400_frames/in.22M.quench.lammps     --log_dir=/red/roitberg/nick_analysis/Restart/22.8M_atoms/random_400_frames/frame_198819/logs     --ani_model_file='ani1x_nr.pt'     --run_name=early_earth_22M_198819_quench     --ani_num_models=8     --timestep=0.25     --run_steps=1000     --run

#!/bin/bash
#SBATCH --job-name=lammps_ani_169206        # Job name
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
#SBATCH --time=24:00:00              # Wall time limit (days-hrs:min:sec)
#SBATCH --output=lammps_ani_169206_%j.log   # Path to the standard output and error files relative to the working dir

module load cuda/11.4.3 gcc/9.3.0 openmpi/4.1.5 cmake/3.21.3 git/2.30.1
source $(conda info --base)/etc/profile.d/conda.sh
conda activate /blue/roitberg/apps/torch1121

python /red/roitberg/nick_analysis/Restart/22.8M_atoms/random_400_frames/run_22.8M_quench.py     /red/roitberg/nick_analysis/Restart/22.8M_atoms/random_400_frames/frame_169206/frame_169206.data     --kokkos     --num_gpus=32     --input_file=/red/roitberg/nick_analysis/Restart/22.8M_atoms/random_400_frames/in.22M.quench.lammps     --log_dir=/red/roitberg/nick_analysis/Restart/22.8M_atoms/random_400_frames/frame_169206/logs     --ani_model_file='ani1x_nr.pt'     --run_name=early_earth_22M_169206_quench     --ani_num_models=8     --timestep=0.25     --run_steps=1000     --run

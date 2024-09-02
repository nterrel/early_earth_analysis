#!/bin/bash
# SBATCH --job-name=lammps_ani        # Job name
# SBATCH --ntasks=32                  # Number of MPI tasks (i.e. processes)
# SBATCH --nodes=4                    # Maximum number of nodes to be allocated
# SBATCH --ntasks-per-node=8          # Maximum number of tasks on each node
# SBATCH --cpus-per-task=1            # Number of cores per MPI task
# SBATCH --partition=hpg-ai           # Partition   
# SBATCH --qos=roitberg               # QOS for job
# SBATCH --account=roitberg           # 
# SBATCH --reservation=roitberg       # 
# SBATCH --gres=gpu:a100:8            # GPUs per node
# SBATCH --mem=120gb                  # Memory (i.e. RAM) per node
# SBATCH --mail-type=END,FAIL         # Mail events (NONE, BEGIN, END, FAIL, ALL)
# SBATCH --mail-user=nterrel@ufl.edu  # Where to send mail
# SBATCH --time=24:00:00             # Wall time limit (days-hrs:min:sec)
# SBATCH --output=lammps_ani_22M_quench_32gpu_%j.log   # Path to the standard output and error files relative to the working dir
# SBATCH --error=lammps_ani_22M_quench_32gpu_%j.err

echo "Testing reservation for LAMMPS_ANI"
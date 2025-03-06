#!/bin/bash
#SBATCH --job-name=melisa_molfind_test               # Job name
#SBATCH --output=nv_molfind_test_%j.out          # Output file
#SBATCH --error=nv_molfind_test_%j.err           # Error file
#SBATCH --partition=gpu
#SBATCH --gres=gpu:a100:1                            # Try to use A100s, large-scale molfind is untested on others
#SBATCH --mem=64gb                   		         # Memory per node
#SBATCH --time=00:60:00               		         # Time limit
#SBATCH --ntasks=1                    		         # Number of tasks (processes)
#SBATCH --cpus-per-task=1             		         # Number of CPU cores per task (adjust as necessary)
#SBATCH --account=mingjieliu-faimm                   # New allocation account
#SBATCH --qos=mingjieliu-faimm                       # Must specify same qos as above, or it will default to roitberg qos


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

cumolfind-molfind /red/roitberg/nick_analysis/Trimmed_frames/trimmed_1608-1629_1.2ns.dcd \
                  /red/roitberg/nick_analysis/traj_top_0.0ns.h5 \
                  /red/roitberg/nick_analysis/all_mol_data.pq \
		  --task="analyze_trajectory" \
                  --dump_interval=50 \
                  --timestep=0.25 \
                  --output_dir=/blue/roitberg/nterrel/melisa_molfind_test \

#!/bin/bash
#SBATCH --job-name=molfind_job        # Job name
#SBATCH --output=molfind_%j.out       # Output file
#SBATCH --error=molfind_%j.err        # Error file
#SBATCH --partition=gpu               # Partition name
#SBATCH --mem=64gb                    # Memory per node
#SBATCH --time=72:00:00               # Time limit
#SBATCH --gres=gpu:a100:8             # Number of GPUs
#SBATCH --ntasks=8                    # Number of tasks (processes)
#SBATCH --cpus-per-task=1             # Number of CPU cores per task (adjust as necessary)

#SBATCH --reservation=roitberg
#SBATCH --account=roitberg
#SBATCH --qos=roitberg

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

# Run the cumolfind-molfind command (NOTE: this is on the new 228 atom run [Feb 14, 2025] )
cumolfind-molfind /red/roitberg/nick_analysis/Restart/228_atoms/logs/2025-02-13-111053.718800.dcd \
                  /red/roitberg/nick_analysis/Restart/228_atoms/228_traj_top_0.0ns.h5 \
                  /red/roitberg/nick_analysis/all_mol_data.pq \
                  --dump_interval=50 \
                  --timestep=0.25 \
                  --output_dir=./test_analyze_new \
		  --num_segments=8 


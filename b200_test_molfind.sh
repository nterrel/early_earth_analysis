#!/bin/bash
#SBATCH --job-name=new_molfind_list      # Job name
#SBATCH --output=new_molfind_list_%j.out          # Output file
#SBATCH --error=new_molfind_list_%j.err           # Error file
#SBATCH --partition=hpg-b200
#SBATCH --gres=gpu:1
#SBATCH --mem=64gb                   		    # Memory per node
#SBATCH --time=02:00:00               		    # Time limit
#SBATCH --ntasks=1                    		    # Number of tasks (processes)
#SBATCH --cpus-per-task=1             		    # Number of CPU cores per task (adjust as necessary)
#SBATCH --account=mingjieliu-faimm
#SBATCH --qos=mingjieliu-faimm
#SBATCH --exclusive

start_time=$(date +%s)

echo "This is testing cumolfind_unique_graphs branch of lammps-ani." 
echo "Date              = $(date)"
echo "Hostname          = $(hostname -s)"
echo "Working Directory = $(pwd)"
echo ""
echo "Number of Nodes Allocated      = $SLURM_JOB_NUM_NODES"
echo "Number of Tasks Allocated      = $SLURM_NTASKS"
echo "Number of Cores/Task Allocated = $SLURM_CPUS_PER_TASK"

export LAMMPS_ANI_ROOT="/red/roitberg/lammps-ani"
export LAMMPS_ROOT=${LAMMPS_ANI_ROOT}/external/lammps/
export LAMMPS_PLUGIN_PATH=${LAMMPS_ANI_ROOT}/build/

source $(conda info --base)/etc/profile.d/conda.sh 
conda activate /red/roitberg/conda-envs/envs/ani-b200
echo using python: $(which python)

cumolfind-molfind /red/roitberg/nick_analysis/Trimmed_frames/trimmed_1608-1629_1.2ns.dcd \
                  /red/roitberg/nick_analysis/traj_top_0.0ns.h5 \
                  /red/roitberg/nick_analysis/reduced_all_mol.pq \
                  --task="analyze_trajectory" \
                  --dump_interval=50 \
                  --timestep=0.25 \
                  --output_dir=/red/roitberg/nick_analysis/b200_small_test \
                  --num_segments=1

end_time=$(date +%s)

# Calculate and print elapsed time
elapsed_time=$((end_time - start_time))
echo ""
echo "Total Runtime: $elapsed_time seconds"


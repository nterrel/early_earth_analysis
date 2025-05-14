#!/bin/bash
#SBATCH --job-name=trackmol_2.4ns      # Job name
#SBATCH --output=trackmol_2.4ns_%j.out          # Output file
#SBATCH --error=trackmol_2.4ns_%j.err           # Error file
#SBATCH --partition=gpu
#SBATCH --gres=gpu:a100:1
#SBATCH --mem=128gb                   		    # Memory per node
#SBATCH --time=06:00:00               		    # Time limit
#SBATCH --ntasks=1                    		    # Number of tasks (processes)
#SBATCH --cpus-per-task=1             		    # Number of CPU cores per task (adjust as necessary)
#SBATCH --account=mingjieliu-faimm
#SBATCH --qos=mingjieliu-faimm

start_time=$(date +%s)

echo "This job tracks Ala formation over 0.1ns, with a 100 frame stride (skip 100 frames)." 
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

module load gcc/9.3.0 openmpi/4.1 cmake/3.21.3 git/2.30.1 singularity

source $(conda info --base)/etc/profile.d/conda.sh 
conda activate rapids-23.10
echo using python: $(which python)

cumolfind-molfind /blue/roitberg/nterrel/trimmed_2.4ns_stride100.dcd \
                  /blue/roitberg/nterrel/traj_top_0.0ns.h5 \
                  /blue/roitberg/nterrel/reduced_all_mol.pq \
                  --task="track_molecules" \
		  --dump_interval=50 \
                  --timestep=0.25 \
                  --output_dir=/blue/roitberg/nterrel/ala_track_2.4ns \
		  --frame_stride=1 \
		  --frame_to_track_mol_origin="/blue/roitberg/nterrel/single_ala_2.4ns.pq"

end_time=$(date +%s)

# Calculate and print elapsed time
elapsed_time=$((end_time - start_time))
echo ""
echo "Total Runtime: $elapsed_time seconds"


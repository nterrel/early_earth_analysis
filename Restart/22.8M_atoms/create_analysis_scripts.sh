#!/bin/bash

# Path to the directory containing the frame directories
base_dir="/red/roitberg/nick_analysis/Restart/22.8M_atoms"

# Iterate over each frame directory
for frame_dir in "$base_dir"/frame_*; do
    # Extract frame number from the directory name
    frame_num=$(basename "$frame_dir" | cut -d'_' -f2)

    # Dynamically find the original DCD file (assumes the original DCD file contains '_original.dcd')
    original_dcd=$(find "$frame_dir" -maxdepth 1 -name "*_original.dcd")

    # Dynamically find the quenched DCD file in the logs directory
    quench_dcd=$(find "$frame_dir/logs" -maxdepth 1 -name "*quench.dcd")

    # Output directories
    original_output_dir="./test_analyze_${frame_num}"
    quench_output_dir="./quench_analyze_${frame_num}"

    # Check if both files are found before creating scripts
    if [[ -n "$original_dcd" && -n "$quench_dcd" ]]; then
        # Create script for the original DCD analysis
        original_script="submit_original_${frame_num}_analyze.sh"
        cat <<EOL > $original_script
#!/bin/bash
#SBATCH --job-name=molfind_job        # Job name
#SBATCH --output=molfind_%j.out       # Output file
#SBATCH --error=molfind_%j.err        # Error file
#SBATCH --partition=gpu               # Partition name
#SBATCH --mem=256gb                   # Memory per node
#SBATCH --time=36:00:00               # Time limit
#SBATCH --gres=gpu:a100:1             # Number of GPUs
#SBATCH --ntasks=1                    # Number of tasks (processes)
#SBATCH --cpus-per-task=1             # Number of CPU cores per task (adjust as necessary)

echo "Date              = \$(date)"
echo "Hostname          = \$(hostname -s)"
echo "Working Directory = \$(pwd)"
echo ""
echo "Number of Nodes Allocated      = \$SLURM_JOB_NUM_NODES"
echo "Number of Tasks Allocated      = \$SLURM_NTASKS"
echo "Number of Cores/Task Allocated = \$SLURM_CPUS_PER_TASK"

export LAMMPS_ANI_ROOT="/blue/roitberg/nterrel/lammps-ani"
export LAMMPS_ROOT=\${LAMMPS_ANI_ROOT}/external/lammps/
export LAMMPS_PLUGIN_PATH=\${LAMMPS_ANI_ROOT}/build/

source \$(conda info --base)/etc/profile.d/conda.sh
conda activate /blue/roitberg/jinzexue/program/miniconda3/envs/rapids-23.10/  # Specify Richard's env
echo using python: \$(which python)

cumolfind-molfind ${original_dcd} \\
                  /red/roitberg/nick_analysis/Restart/22.8M_atoms/mixture_22800000.pdb \\
                  /red/roitberg/nick_analysis/all_mol_data.pq \\
                  --dump_interval=50 \\
                  --timestep=0.25 \\
                  --output_dir=${original_output_dir} \\
                  --num_segments=1 \\
                  --segment_index=0
EOL

        # Create script for the quenched DCD analysis
        quench_script="submit_quenched_${frame_num}_analyze.sh"
        cat <<EOL > $quench_script
#!/bin/bash
#SBATCH --job-name=molfind_job        # Job name
#SBATCH --output=molfind_%j.out       # Output file
#SBATCH --error=molfind_%j.err        # Error file
#SBATCH --partition=gpu               # Partition name
#SBATCH --mem=256gb                   # Memory per node
#SBATCH --time=36:00:00               # Time limit
#SBATCH --gres=gpu:a100:1             # Number of GPUs
#SBATCH --ntasks=1                    # Number of tasks (processes)
#SBATCH --cpus-per-task=1             # Number of CPU cores per task (adjust as necessary)

echo "Date              = \$(date)"
echo "Hostname          = \$(hostname -s)"
echo "Working Directory = \$(pwd)"
echo ""
echo "Number of Nodes Allocated      = \$SLURM_JOB_NUM_NODES"
echo "Number of Tasks Allocated      = \$SLURM_NTASKS"
echo "Number of Cores/Task Allocated = \$SLURM_CPUS_PER_TASK"

export LAMMPS_ANI_ROOT="/blue/roitberg/nterrel/lammps-ani"
export LAMMPS_ROOT=\${LAMMPS_ANI_ROOT}/external/lammps/
export LAMMPS_PLUGIN_PATH=\${LAMMPS_ANI_ROOT}/build/

source \$(conda info --base)/etc/profile.d/conda.sh
conda activate /blue/roitberg/jinzexue/program/miniconda3/envs/rapids-23.10/  # Specify Richard's env
echo using python: \$(which python)

cumolfind-molfind ${quench_dcd} \\
                  /red/roitberg/nick_analysis/Restart/22.8M_atoms/mixture_22800000.pdb \\
                  /red/roitberg/nick_analysis/all_mol_data.pq \\
                  --dump_interval=50 \\
                  --timestep=0.25 \\
                  --output_dir=${quench_output_dir} \\
                  --num_segments=21 \\
                  --segment_index=20
EOL

        echo "Generated scripts for frame_${frame_num}"
    else
        echo "Skipping frame_${frame_num}, DCD files not found."
    fi
done


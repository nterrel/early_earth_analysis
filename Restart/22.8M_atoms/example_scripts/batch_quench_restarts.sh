#!/bin/bash

# NOTE: This script worked to create shell scripts for each of the subdirectories, and individually those shell scripts work, but when trying to batch submit via this script, every job fails with 
# "An ORTE daemon has unexpectedly failed after launch and before communicating back to mpirun. This could be caused by a number of factors, including an inability to create a connection back to mpirun due to a lack of common network interfaces and/or no route found between them. Please check network connectivity (including firewalls and network routing requirements)."
# So, a second script was made to submit each job sequentially, whether the prior job fails or ends.

parent_dir="/red/roitberg/nick_analysis/Restart/22.8M_atoms"

lammps_input="${parent_dir}/in.22M.quench.lammps"
python_script="${parent_dir}/run_22.8M_quench.py"

# Loop over `frame_NUMBER` directories
for frame_dir in "$parent_dir"/frame_*; do
    if [[ ! -d "$frame_dir" ]]; then
        echo "Skipping $frame_dir as it is not a directory."
        continue
    fi

    # Extract frame number from directory name
    frame_number=$(basename "$frame_dir" | sed 's/frame_//')

    # Define file paths specific to this frame
    data_file="${frame_dir}/frame_${frame_number}.data"
    
    log_dir="${frame_dir}/logs"
    slurm_script="${frame_dir}/submit.32gpu.${frame_number}.quench.sh"

    # Dynamically find correct DCD file
    dcd_file=$(find "$frame_dir" -type f -name "frame_${frame_number}_*.dcd" | head -n 1)

    # Check if the necessary data and DCD files exist before proceeding
    if [[ ! -f "$data_file" ]]; then
        echo "Data file not found for frame $frame_number. Skipping..."
        continue
    fi

    if [[ -z "$dcd_file" ]]; then
        echo "DCD file not found for frame $frame_number. Skipping..."
        continue
    fi

    # Create the logs directory if it doesn't exist
    mkdir -p "$log_dir"

    # Create a new SLURM script for this frame
    cat > "$slurm_script" <<EOL
#!/bin/bash
#SBATCH --job-name=lammps_ani_${frame_number}        # Job name
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
#SBATCH --output=lammps_ani_${frame_number}_%j.log   # Path to the standard output and error files relative to the working dir

echo "Date              = \$(date)"
echo "Hostname          = \$(hostname -s)"
echo "Working Directory = \$(pwd)"
echo ""
echo "Number of Nodes Allocated      = \$SLURM_JOB_NUM_NODES"
echo "Number of Tasks Allocated      = \$SLURM_NTASKS"
echo "Number of Cores/Task Allocated = \$SLURM_CPUS_PER_TASK"

module load cuda/11.4.3 gcc/9.3.0 openmpi/4.1.5 cmake/3.21.3 git/2.30.1
export LAMMPS_ANI_ROOT="/blue/roitberg/apps/lammps-ani"
export LAMMPS_ROOT=\${LAMMPS_ANI_ROOT}/external/lammps/
export LAMMPS_PLUGIN_PATH=\${LAMMPS_ANI_ROOT}/build/

source \$(conda info --base)/etc/profile.d/conda.sh
conda activate /blue/roitberg/apps/torch1121
echo using python: \$(which python)

python ${python_script} \
    ${data_file} \
    --kokkos \
    --num_gpus=32 \
    --input_file=${lammps_input} \
    --log_dir=${log_dir} \
    --ani_model_file='ani1x_nr.pt' \
    --run_name=early_earth_22M_${frame_number}_quench \
    --ani_num_models=8 \
    --timestep=0.25 \
    --run_steps=1000 \
    --run

EOL

    # Submit the job for this frame
    sbatch "$slurm_script"

    echo "Submitted job for frame $frame_number"

done

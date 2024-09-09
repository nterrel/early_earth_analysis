#!/bin/bash
#SBATCH --job-name=data_file_tracker
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2gb
#SBATCH --time=36:00:00
#SBATCH --output=data_file_checker_%j.log

# This script checks for the existence of .data files in subdirectories, creates a LAMMPS runner shell script, and submits the job with a dependency to only run after the previous job is completed / cancelled.
# It also iteratively checks for new shell scripts and submits those jobs

module load conda
conda activate /blue/roitberg/apps/torch1121

parent_dir="/red/roitberg/nick_analysis/Restart/22.8M_atoms/random_400_frames"
lammps_input="${parent_dir}/in.22M.quench.lammps"
python_script="${parent_dir}/run_22.8M_quench.py"
data_gen_job_id=43637940    # The job ID of the script (currently running) which creates input .data files

submit_jobs() {
    # Find all directories that match the pattern "frame_*" and check for .data files
    frame_dirs=$(find "$parent_dir" -type d -name "frame_*" | sort)

    previous_job_id=""

    for frame_dir in $frame_dirs; do
        # Extract frame number from directory name
        frame_number=$(basename "$frame_dir" | sed 's/frame_//')

        # Define paths
        data_file="${frame_dir}/frame_${frame_number}.data"
        log_dir="${frame_dir}/logs"
        slurm_script="${frame_dir}/submit.32gpu.${frame_number}.quench.sh"

        # Check if the .data file exists and if the submission script does not exist
        if [[ -f "$data_file" && ! -f "$slurm_script" ]]; then
            echo "Data file found for frame $frame_number, and no submission script exists yet. Creating and submitting the job."

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

            # Submit the job for this frame with dependencies
            if [[ -z "$previous_job_id" ]]; then
                # Submit the first job without any dependency
                previous_job_id=$(sbatch "$slurm_script" | awk '{print $4}')
            else
                # Submit the next job with a dependency on the previous job
                previous_job_id=$(sbatch --dependency=afterany:$previous_job_id "$slurm_script" | awk '{print $4}')
            fi
            echo "Submitted job for frame $frame_number with Job ID $previous_job_id"
        else
            if [[ -f "$slurm_script" ]]; then
                echo "Job already submitted for frame $frame_number. Skipping..."
            else
                echo "Data file not found for frame $frame_number. Skipping..."
            fi
        fi
    done
}

# Function to check if the data generation job is still running
is_data_generation_running() {
    squeue -j "$data_gen_job_id" > /dev/null 2>&1
    if [[ $? -eq 0 ]]; then
        return 0    # Job is still running
    else
        return 1    # Job has completed or failed
    fi
}

# Main loop: check for new .data files while data generation job is running
while is_data_generation_running; do
    echo "Data generation job $data_gen_job_id is still running. Checking for new .data files and submitting jobs..."
    submit_jobs
    echo "Sleeping for 4 hours before checking again..."
    sleep 4h
done

echo "Data generation job $data_gen_job_id has completed. No further checks will be made."

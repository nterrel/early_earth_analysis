#!/bin/bash
#SBATCH --job-name=create_lammps_inputs
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2gb
#SBATCH --time=01:00:00
#SBATCH --output=create_lammps_inputs_%j.log

# This script checks for the existence of .data files in subdirectories, 
# creates a LAMMPS runner shell script if the submission script does not already exist.


module load conda
conda activate /blue/roitberg/apps/torch1121

parent_dir="/red/roitberg/nick_analysis/Restart/22.8M_atoms/random_400_frames"
lammps_input="${parent_dir}/in.22M.quench.lammps"
python_script="${parent_dir}/run_22.8M_quench.py"

# Loop over each "frame_*" directory and check for .data files
for frame_dir in "$parent_dir"/frame_*; do
    # Extract the frame number from the directory name
    frame_number=$(basename "$frame_dir" | sed 's/frame_//')

    # Define paths
    data_file="${frame_dir}/frame_${frame_number}.data"
    log_dir="${frame_dir}/logs"
    slurm_script="${frame_dir}/submit.32gpu.${frame_number}.quench.sh"

    # Check if the .data file exists and the submission script does not exist
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
#SBATCH --time=24:00:00              # Wall time limit (days-hrs:min:sec)
#SBATCH --output=lammps_ani_${frame_number}_%j.log   # Path to the standard output and error files relative to the working dir

module load cuda/11.4.3 gcc/9.3.0 openmpi/4.1.5 cmake/3.21.3 git/2.30.1
source \$(conda info --base)/etc/profile.d/conda.sh
conda activate /blue/roitberg/apps/torch1121

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


        echo "Created submit script: $slurm_script for frame $frame_number"
    else
        if [[ -f "$slurm_script" ]]; then
            echo "Submit script already exists for frame $frame_number. Skipping..."
        else
            echo "Data file not found for frame $frame_number. Skipping..."
        fi
    fi
done

echo "Script generation complete."

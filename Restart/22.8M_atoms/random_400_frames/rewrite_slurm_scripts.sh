#!/bin/bash
#SBATCH --job-name=update_restart_scripts
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2gb
#SBATCH --time=01:00:00
#SBATCH --output=update_restart_scripts_%j.log

# Tried editing restart scripts with python but was having trouble with formatting and missing lines, just going to explicitly write the files in the same way as they were originally produced.

script_list="scripts_to_resubmit.txt"

while IFS= read -r slurm_script; do
    if [[ -f "$slurm_script" ]]; then
        echo "Updating script: $slurm_script"

        # Extract frame_number and set variables for current file
        frame_number=$(basename "$slurm_script" | sed 's/.*\.32gpu\.\([0-9]\+\)\.quench\.sh/\1/')
        frame_dir=$(dirname "$slurm_script")
        log_dir="${frame_dir}/logs"
        data_file="${frame_dir}/frame_${frame_number}.data"
        lammps_input="/red/roitberg/nick_analysis/Restart/22.8M_atoms/random_400_frames/in.22M.quench.lammps"
        python_script="/red/roitberg/nick_analysis/Restart/22.8M_atoms/random_400_frames/run_22.8M_quench.py"

        # Create log dir if it doesn't already exist
        mkdir -p "$log_dir"

        # Backup the original script as 'ORIGINAL_submit.32gpu.FRAME_NUMBER.quench.sh'
        backup_script="${frame_dir}/ORIGINAL_submit.32gpu.${frame_number}.quench.sh"
        if [[ ! -f "$backup_script" ]]; then
            cp "$slurm_script" "$backup_script"
            echo "Saved original script as: $backup_script"
        else
            echo "Backup script already exists for frame $frame_number, skipping backup."
        fi

        # Overwrite the existing SLURM script with the updated configuration

        cat > "$slurm_script" <<EOL
#!/bin/bash
#SBATCH --job-name=lammps_ani_${frame_number}
#SBATCH --ntasks=32
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=8
#SBATCH --cpus-per-task=1
#SBATCH --partition=gpu
#SBATCH --gres=gpu:a100:8
#SBATCH --mem=120gb
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=nterrel@ufl.edu
#SBATCH --time=02:00:00
#SBATCH --output=lammps_ani_${frame_number}_%j.log

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

python ${python_script} \\
    ${data_file} \\
    --kokkos \\
    --num_gpus=32 \\
    --input_file=${lammps_input} \\
    --log_dir=${log_dir} \\
    --ani_model_file='ani1x_nr.pt' \\
    --run_name=early_earth_22M_${frame_number}_quench \\
    --ani_num_models=8 \\
    --timestep=0.25 \\
    --run_steps=1000 \\
    --run
EOL

        echo "Updated submit script: $slurm_script for frame $frame_number"
    else
        echo "Script not found: $slurm_script. Skipping..."
    fi
done < "$script_list"

echo "Script updates complete."

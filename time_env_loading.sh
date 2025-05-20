#!/bin/bash

# === Configuration ===
ENV_BLUE="/blue/roitberg/nterrel/Conda/envs/rapids-23.10"
ENV_RED="/red/roitberg/conda-envs/envs/rapids-23.10"
JOB_TIME="00:05:00"
CPUS=1
MEMORY="2G"
PARTITION="hpg-dev"  # or 'short', 'general', etc.
OUTPUT_DIR="library_import_timings"

# === Create output directory ===
mkdir -p "$OUTPUT_DIR"

# === Modules to test ===
MODULES=(
    os
    re
    pickle
    ast
    time
    collections
    pathlib
    torch
    pytraj
    mdtraj
    pandas
    numpy
    cupy
    cudf
)

# === Helper function to generate and submit a SLURM job ===
generate_job() {
    local module=$1
    local env=$2
    local tag=$3

    local clean_module=$(echo "$module" | tr '.' '_')
    local job_name="import_${clean_module}_${tag}"
    local job_file="${OUTPUT_DIR}/slurm_${job_name}.sh"

    cat <<EOF > "$job_file"
#!/bin/bash
#SBATCH --job-name=$job_name
#SBATCH --output=${OUTPUT_DIR}/${job_name}.out
#SBATCH --error=${OUTPUT_DIR}/${job_name}.err
#SBATCH --time=$JOB_TIME
#SBATCH --cpus-per-task=$CPUS
#SBATCH --mem=$MEMORY
#SBATCH --partition=$PARTITION

source ~/.bashrc
conda activate $env

echo "Timing import of '$module' in $tag..."
/usr/bin/time -f "Wall time: %e seconds" python -c "import time; start = time.time(); import $module; print(f'Import time for $module in $tag: {time.time() - start:.6f} seconds')"
EOF

    sbatch "$job_file"
}

# === Submit jobs for each module in both environments ===
for module in "${MODULES[@]}"; do
    generate_job "$module" "$ENV_BLUE" "blue"
    generate_job "$module" "$ENV_RED" "red"
done

echo "Submitted ${#MODULES[@]} × 2 = $((${#MODULES[@]} * 2)) SLURM jobs."
echo "Output and error files are in: $OUTPUT_DIR/"

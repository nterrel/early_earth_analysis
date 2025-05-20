#!/bin/bash
#SBATCH --job-name=import_pytraj_red
#SBATCH --output=library_import_timings/import_pytraj_red.out
#SBATCH --error=library_import_timings/import_pytraj_red.err
#SBATCH --time=00:05:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --partition=hpg-dev

source ~/.bashrc
conda activate /red/roitberg/conda-envs/envs/rapids-23.10

echo "Timing import of 'pytraj' in red..."
/usr/bin/time -f "Wall time: %e seconds" python -c "import time; start = time.time(); import pytraj; print(f'Import time for pytraj in red: {time.time() - start:.6f} seconds')"

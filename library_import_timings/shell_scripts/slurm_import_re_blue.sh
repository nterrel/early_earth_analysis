#!/bin/bash
#SBATCH --job-name=import_re_blue
#SBATCH --output=library_import_timings/import_re_blue.out
#SBATCH --error=library_import_timings/import_re_blue.err
#SBATCH --time=00:05:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --partition=hpg-dev

source ~/.bashrc
conda activate /blue/roitberg/nterrel/Conda/envs/rapids-23.10

echo "Timing import of 're' in blue..."
/usr/bin/time -f "Wall time: %e seconds" python -c "import time; start = time.time(); import re; print(f'Import time for re in blue: {time.time() - start:.6f} seconds')"

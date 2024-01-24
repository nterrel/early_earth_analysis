#!/bin/bash
# batch_submit.sh

for floor_time in $(seq 0.1 0.1 4.3)  # Adjust range as needed
do
    parquet_file="/red/roitberg/nick_analysis/split_parquets/df_floor_time_${floor_time}.pq"

    sbatch <<EOF
#!/bin/bash
#SBATCH --job-name=extract_${floor_time}ns_structures
#SBATCH --ntasks=1
#SBATCH --mem=128gb
#SBATCH --time=04:00:00
#SBATCH --output=/blue/roitberg/nterrel/extract_coords_%j.log

module load conda
conda activate /path/to/conda/env
python /red/roitberg/nick_analysis/extract_coordinates.py $parquet_file > /blue/roitberg/nterrel/extract_coords_${floor_time}.txt
EOF

done

#!/bin/bash
#SBATCH --job-name=mol_trace
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=128gb
#SBATCH --time=48:00:00
#SBATCH --output=/red/roitberg/nick_analysis/Mol_trace/mol_trace.log
#SBATCH --error=/red/roitberg/nick_analysis/Mol_trace/mol_trace.err

module load conda
conda activate /blue/roitberg/apps/torch1121
python /red/roitberg/nick_analysis/extract_trace_frames.py /red/roitberg/nick_analysis/traj_top_0.0ns.h5 --start_frame 328000 --end_frame 308000 --output_dir /red/roitberg/nick_analysis/Mol_trace

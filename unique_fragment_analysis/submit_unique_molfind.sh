# This calls a python script within the lammps-ani code to write analysis scripts and batch submit them -- if any fail, you'll have to specify the 'segment_index' for the failed segment and restart it with that argument in the molfind command (otherwise it will have incorrect frame / time numbering)

# NOTE (5/22/2025): I re-ran this script to generate the 880 jobs again and then cancelled them with the `grep` and `head` commands at the bottom of the script

python /red/roitberg/lammps-ani/cumolfind/submit_analysis.py \
    --traj=/red/roitberg/22M_20231222_prodrun/ \
    --top=/red/roitberg/nick_analysis/traj_top_0.0ns.h5 \
    --num_segments=20 \
    --mol_pq=/red/roitberg/nick_analysis/reduced_all_mol.pq \
    --output_dir=/red/roitberg/nick_analysis/RESTART_new_unique_fragment_analysis \
    -y | tee all_job_output.txt

# Extract job IDs from the output
grep "Submitted batch job" all_job_output.txt | awk '{print $4}' > all_job_ids.txt

# Cancel the first 589 job IDs (let 291 run)
head -n 585 all_job_ids.txt | xargs scancel


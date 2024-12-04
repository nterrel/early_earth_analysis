# This calls a python script within the lammps-ani code to write analysis scripts and batch submit them -- if any fail, you'll have to specify the 'segment_index' for the failed segment and restart it with that argument in the molfind command (otherwise it will have incorrect frame / time numbering)

python /blue/roitberg/nterrel/lammps-ani/cumolfind/submit_analysis.py \
    --traj=/red/roitberg/22M_20231222_prodrun/ \
    --top=/blue/roitberg/apps/lammps-ani/examples/early_earth/data/mixture_22800000.pdb \
    --num_segments=20 \
    --mol_pq=/red/roitberg/nick_analysis/all_mol_data.pq \
    --output_dir=/red/roitberg/nick_analysis/unique_fragment_analysis \
    -y

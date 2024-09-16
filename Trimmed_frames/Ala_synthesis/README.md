# Directory containing 12 frames which contain Alanine molecules

- `split_ala_frames.py` is a python script used to split those 12 frames out of the original traj. Those 12 frames were randomly selected (literally, using the random python library in an interactive session with the pq containing "found" molecules). `split_ala_frames.txt` is just an output text file that says where the frames were saved from (and where to).
  - Isolate (randomly selected) ala-containing frames into individual dcd files.

- `submit_ala_frames.sh` is a SLURM submission script to run that python script on the queue. 
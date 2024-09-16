# This directory contains a bunch of pdb files that 'trace' the synthesis of an alanine molecule

## Scripts contained here

- `extract_trace_frames.py`
  - This script can extract a specified list of atom indices from a specified number of frames. Left in this directory as `top_loader.py` is a necessary import. Extracts coordinates to the `./Mol_trace/` directory.

- `submit_trace.sh`
  - SLURM submission script to do the same thing.

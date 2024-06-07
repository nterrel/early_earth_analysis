# General extraction scripts

- `extract_general.py`
  - This script opens a trajectory file and extracts coordinates of 'found' molecules (from the pubchem dataframe)

- `generate_xyz.py`
  - Iterates over coordinates stored in HDF and creates a xyz files for each molecule.

- `concatenate_xyz.py`
  - Combines the individual xyz files created by `generate_xyz.py` into a single, unified file for each unique molecule.

- `remap_general.py`
  - This script compares extracted coordinates to a standard reference graph and remaps the coordinates to fit the same ordering as the standard.

- Shell scripts for the `extract_general.py` and `remap_general.py` python scripts, so they run on SLURM.

- `count.sh`
  - Simple shell script for counting the number of successfully remapped / failed structures extracted from the big EE sim.

## Subdirectories

- XYZs
  - Spot to dump all generated xyz files, before remapping. Each unique molecule has its own subdirectory, but the concatenated xyz files are located here.

- Reordered
  - Location of the remapped coordinate files for each unique molecule found in the big EE sim.

- Broke
  - Location of failed remap xyz files, really only used by `count.sh` to determine how many structures were identified as a certain molecule but do not actually have the correct connectivity.

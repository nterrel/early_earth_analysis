# Alanine Extraction and Characterization

The 22.8M ANI-rx Early Earth simulation showed the formation of many molecules, including 450K alanine molecules. This directory includes scripts pertaining to the extraction and characterization of these molecules.

A few files of alanine coordinates exist here:

- `all_alanines.xyz` is a concatenated list of raw output coordinates (ordered arbitrarily by inital graph search)
- `reordered_alanines.xyz` is a slightly smaller set of things that actually match an alanine graph, ordered in an exact format.
- `alanines_final.xyz` is the final set of alanine molecules, filtered, rearranged, unwrapped (pbc conditions) and aligned. 
  - The process to unwrapping and aligning these coordinates was complicated, next set of extracts should be unwrapped when the coordinates are pulled from the trajectory (if possible).
  - Basically:
    - I created a pdb file (with open babel) for the first conformer, which was used for a template topology
    - Ignacio used that pdb to create a mol2 (with amber antechamber)
    - Then used tleap to create a .prmtop
    - Then used cpptraj to unwrap and align the coordinates (this process is detailed better in `ALA_NOTES.md`.)

## Scripts

- `extract_ala.py`
  - Extracts alanine molecules from the simulation data. The extracted coordinates were saved to Pandas DataFrames. 
  - Originally, this was `merged_mol.pq`, I split this df into 0.1ns chunks (to match the trajectory data), which can be found at `/red/roitberg/nick_analysis/Split_parquets`.
  - Each 'found' alanine molecule is saved in its own row of this `merged_mol.pq` (and therefore the split parquets), I iterated over each row to open the correct frame of a dcd trajectory and save the xyz coordinates of that alanine conformer to a new HDF5 file containing all the same data as the split parquet, plus the coordinates of each alanine molecule 'extracted'. 
  - These .h5 dataframes were then used to generate xyz files of the alanine coordinates (more below).

- `generate_ala_xyz.py`
  - Generates .xyz files from extracted coordinates for further analysis.
  - This script outputs an xyz for each 0.1ns split h5 DataFrame.

- `concatenate_xyzs.py`
  - Concatenates multiple .xyz files into a single file.
  - Wanted everything concatenated to a single xyz, so this is just a simple script to combine the 0.1ns splits mentioned above.

- `remap_ala.py`
  - This script looks through the concatenated xyz file and determines which molecules are *actually* alanines, since the initial graph search yielded more isomorphic matches than there should have been.
  - Here, a more stringent graph matching criteria is applied, filtered about 10k conformers from the extracted outputs. 
  - After confirming that a structure truly matches a standard graph of alanine, remap the coordinates to have the exact same ordering as is present in the standard graph.

## Other sub-directories

- `HDF_coord/`
  - Not saved to remote repo
  - This is where the .h5 files containing extracted xyz coordinates for alanine molecules are located.

- `XYZs/`
  - Location of coordinates converted from .h5 stores to .xyz files along 0.1ns splits.

## Notes on the Extraction Process

- Approximately 449,831 alanines were extracted from the simulation. However, about 10,000 of these were not truly alanine molecules; they just met the graph search criteria.

- A more stringent graph search narrowed this down to 438,987 alanine molecules. This refinement was necessary to reorder atomic coordinates to the same ordering for visualization purposes. During this process, it was determined that the graph search criteria were not specific enough to determine the correct connectivity.

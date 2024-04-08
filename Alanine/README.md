# Alanine Extraction and Characterization

The 22.8M Early Earth simulation showed the formation of many molecules, including 450K alanine molecules. This directory includes scripts pertaining to the extraction and characterization of these molecules.

## Scripts:

- `extract_ala.py`
  - Extracts alanine molecules from the simulation data.

- `concatenate_xyzs.py`
  - Concatenates multiple .xyz files into a single file.

- `generate_ala_xyz.py`
  - Generates .xyz files from extracted coordinates for further analysis.

## Other sub-directories:

- `HDF_coord/`
  - This is where the .h5 files containing extracted xyz coordinates for alanine molecules are located.

- `XYZs/`
  - Location of coordinates converted from .h5 stores to .xyz files along 0.1ns splits.

## Notes on the Extraction Process:

- Approximately 450,000 alanines were extracted from the simulation. However, about 10,000 of these were not truly alanine molecules; they just met the graph search criteria.

- A more stringent graph search narrowed this down to 438,987 alanine molecules. This refinement was necessary to reorder atomic coordinates to the same ordering for visualization purposes. During this process, it was determined that the graph search criteria were not specific enough to determine the correct connectivity.

Alanine extraction and characterization

22.8M Early Earth simulation showed the formation of many molecules, including 450K alanine molecules

This directory includes scripts pertaining to the extraction and characterization of these molecules.
Scripts:
* extract_ala.py

* concatenate_xyzs.py

* generate_ala_xyz.py


Other sub-directories:
* HDF_coord/
    This is where the .h5 files containing extracted xyz coordinates for alanine molecules are located
* XYZs/
    Location of coordinates converted from .h5 stores to .xyz files along 0.1ns splits

~450,000 (edit for correct #) alanines were extracted from the simulation
~10,000 were not truly alanine molecules, just met the graph search criteria
A more stringent graph search narrowed this down to 438,987 alanine molecules.
This was done to reorder atomic coordinates to the same ordering for visualization purposes,
 but in the process it was determined that the graph search did not have particular enough criteria to determine the correct connectivity.


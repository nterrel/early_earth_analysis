# Keeping track of small outputs here

This is pretty outdated, the ~1.5% of alanines unable to be labeled are due to molecules along the periodic boundary. 

## Things to do

- After extracting all coordinates, assemble them into a single hdf that is organized like the ANI energies, maybe compute the DFT energies of those things(?) and compare to the ANI energies of those molecules.
- Note that `extract_general.py` is specifically for extracting coordinates that are *NOT* glycine or alanine.

## Things that are done

Assigning stereochemistry with RDKit:
    (ani) nickterrel WIP % python assign_stereochemistry.py

Total runtime for all `stereo_analyses` (438,773 alanines): 147.1323938369751 seconds.

    (ani) nickterrel WIP % grep "Unassigned-" stereo_labeled_alanines.sdf -c

68

    (ani) nickterrel WIP % grep "D-" stereo_labeled_alanines.sdf -c

219007

    (ani) nickterrel WIP % grep "L-" stereo_labeled_alanines.sdf -c

212997

Total = 219007+212997+68 = 432072

## Something happened to ~6700 alanine molecules that isn't one of the three possible outputs

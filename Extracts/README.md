# Files pertaining to extracting coordinates from the large early earth simulation

## Sub-directories

- Alanine
-- First molecules extracted, worked as a template for 'general' extraction scripts contained in `Others`
- Glycine
-- Have not extracted these, probably not worth the time due to the large number of structures. Need to rethink the frame iteration process if looking to extract these.
- Others
-- All other structures found by the initial production analysis (not Ala, Gly). Contains generalized scripts for extracting based on molecules contained in a dataframe with a reference graph. Initial graph search did not verify correct connectivity, so a refined graph comparison is made after coordinates are extracted, allowing them to remap to fit the ordering of the standardized reference graph.

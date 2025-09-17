## This contains scripts / outputs for comparing the original molfind list to a new, larger list

This change makes the analysis take much longer (especially with many very small molecules `new_all_mol.pq`).

So, the comparisons here are really focused on `all_mol_data.pq` (original) vs `reduced_all_mol.pq`, which is `new_all_mol.pq` minus ~9 species of <10 atoms. These species led to a single frame taking several minutes to compute, and all of the molecules removed had a ~90% chance of matching based on formula alone -- for very small molecules we do not necessarily need to do a graph comparison. This trend obviously disappears after chemical complexity increases. 



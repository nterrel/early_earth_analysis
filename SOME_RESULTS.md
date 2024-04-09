Assigning stereochemistry with RDKit:
(ani) nickterrel WIP % python assign_stereochemistry.py
Total runtime for all stereo_analyses (438,773 alanines): 147.1323938369751 seconds.

(ani) nickterrel WIP % grep "Unassigned-" stereo_labeled_alanines.sdf -c
68
(ani) nickterrel WIP % grep "D-" stereo_labeled_alanines.sdf -c
219007
(ani) nickterrel WIP % grep "L-" stereo_labeled_alanines.sdf -c
212997
Total = 219007+212997+68 = 432072
** Something happened to ~6700 alanine molecules that isn't one of the three possible outputs **
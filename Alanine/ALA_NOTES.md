# Notes about alanine reordering and alignment

Created a file `reordered_alanines.xyz` with `remap_ala_test.py` -- Note that I have made some edits to this script and it no longer does EXACTLY what it did when I remapped the coordinates
The changes were an attempt at unwrapping pbc edge-case coordinates by hand, but it was more complicated than I was hoping for. In the end, I asked Ignacio for help with using cpptraj to accomplish this (more below)
Converted this new .xyz to .sdf and .pdb (in that order, pdb made with sdf) via open babel:
`obabel -i xyz reordered_alanines.xyz -o sdf -O reordered_alanines.sdf`
`obabel -isdf reordered_alanines.sdf -opdb -O reordered_alanines.pdb`

Steps Ignacio took to unwrap and align:

1. With the first conformer (in pdb format), use ambertools antechamber to create a mol2
2. Create a topology in tleap
3. Using that topology information, and the following cpptraj code:

```cpp
parm ala.prmtop
trajin alanines.xyz
unwrap
align
trajout alanines.out.xyz
run
```

Output the file `alanines.out.xyz`

The coordinates here are all aligned to some center (which cpptraj decided, either center of mass or center of geometry)

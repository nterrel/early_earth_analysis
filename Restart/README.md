# Files pertaining to quench restarts of LAMMPS-ANI early earth simulations

- `228_atoms` is the small, easy to run system that can be tested on a single GPU
- `228k_atoms` should also be able to run on a single GPU, but tested with Kokkos communicating between 2 gpus
- `22.8M_atoms` is the true system, the one that will give trouble if you try to run on any less than 24 GPUs (estimated), was only able to get it restarted once we got an allocation of 32 GPUs for a little over a week. Ran 415 restarts to quench the system from 2500 K to 300 K. Analysis and miscellaneous scripts pertaining to these restarts are all contained here, but someday may migrate a lot of the analysis files to a different directory.
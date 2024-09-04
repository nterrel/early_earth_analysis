# Before and after quenching frame 196366 (one of the randomly selected ala-containing frames)

* This was the first frame analyzed, so the most detailed errors / logs / scripts are here -- other frames will contain simplified and streamlined scripts to just run the quench and analysis.

## in.22M.quench.lammps edits

* Original input can be found at `/red/roitberg/nick_analysis/Restart/22.8M_atoms/in.22M.lammps`. Modified to `example_submit_quench.sh` located in that same directory.
* Changed 1000 steps to 100 steps
* Deleted a lot of:

    ```text
    dump           2 all dcd 50 ${log_dir}/${timestamp}_4.3ns.dcd
    write_data     ${log_dir}/${timestamp}_4.3ns.final
    write_restart  ${log_dir}/${timestamp}_4.3ns.restart
    run            400000
    undump         2
    ```

  commands, just want to start at 2500K and immediately decrease to 300K

* Changed initial velocities (set/determined at 0.0 K) to:

    ```text
    # Settings: temperature at 0 K
    velocity       all create 2500.0 12345 rot yes mom yes dist gaussian
    timestep       ${timestep}
    ```

* Changed thermo frequency from 50 to 10 since I'm only running 100 steps

### Errors encountered running quench

* Masses not in .data file created by ase, manually added to\ `/red/roitberg/nick_analysis/Restart/22.8M_atoms/frame_196366/lammps_ani_22M_quench_1gpu_41835062.log`\
Will need to do this manually for each frame split off, if using ASE to create data file for input. Not sure how well this will work since velocities are assigned by gaussian distribution.

* INT_MAX error (same as encountered in molfind):\

    ```text
    Exception: nonzero is not supported for tensors with more than INT_MAX elements,   file a support request
    Exception raised from nonzero_out_cuda at /opt/conda/conda-bld/pytorch_1659484683044/work/aten/src/ATen/native/cuda/Nonzero.cu:115 (most recent call first):
    ```

  * Believe this error is due to GPU memory being full. Do not encounter this issue with 32 A100 GPUs.

* GPU memory error (when running on 1, 2, 4, 8, 16 GPUs, but not with 32):

    ```text
    RuntimeError: CUDA out of memory. Tried to allocate 6.59 GiB (GPU 1; 79.14 GiB total capacity; 66.32 GiB already allocated; 4.89 GiB free; 71.29 GiB reserved in total by PyTorch) If reserved memory is >> allocated memory try setting max_split_size_mb to avoid fragmentation.  See documentation for Memory Management and PYTORCH_CUDA_ALLOC_CONF

    ```

  * Solved by using the `Roitberg` reservation from 8-31 (06:00:00) to 9-09 (23:59:59). Richard said (if his memory serves) that the max limit of an a100 gpu is ~1m atoms.

### These errors have been solved, quench runs at approximately 0.55 seconds/step -- after ~7 minutess to load system


## Molfind stuff

* molfind_41492932 files are before quench, these could not run because of the following error:\
`RuntimeError: nonzero is not supported for tensors with more than INT_MAX elements,   file a support request`\
Turns out I was actually using my modified molfind program on the branch `origin/nick`, after switching to `origin/cumolfind_modified` this should work properly.
* molfind_41682856 files are before quench, with the proper branch. Still hit the following error:\
`RuntimeError: nonzero is not supported for tensors with more than INT_MAX elements,   file a support request`

The above 2 errors are (likely) due to a mismatch in environment -- be sure to use Richard's rapids-23.10 env (a .yml file containing the correct package versions is located at `/red/roitberg/nick_analysis/rapids_23.10.yml`). Do not run into this issue with his version of rapids-23.10, I'm not sure where the issue came from when I tried to install my own version, but I've fixed it by specifying his env.

### Issues with molfind have been solved, the analyses can be found in `original_analyze` and `quench_analyze`.

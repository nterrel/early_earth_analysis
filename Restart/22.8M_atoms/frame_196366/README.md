# Before and after quenching frame 196366 (one of the randomly selected ala-containing frames)

## in.22M.quench.lammps edits

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

## Molfind stuff

* molfind_41492932 files are before quench, these could not run because of the following error:\
`RuntimeError: nonzero is not supported for tensors with more than INT_MAX elements,   file a support request`\
Turns out I was actually using my modified molfind program on the branch `origin/nick`, after switching to `origin/cumolfind_modified` this should work properly.
* molfind_41682856 files are before quench, with the proper branch.

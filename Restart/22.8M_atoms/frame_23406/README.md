# Before and after quenching frame 23406 (one of the randomly selected ala-containing frames)

## in.22M.quench.lammps edits:

* changed 1000 steps to 100 steps
* deleted a lot of:
`dump           2 all dcd 50 ${log_dir}/${timestamp}_4.3ns.dcd`
`write_data     ${log_dir}/${timestamp}_4.3ns.final`
`write_restart  ${log_dir}/${timestamp}_4.3ns.restart`
`run            400000`
`undump         2`
"""
  commands, just want to start at 2500K and immediately decrease to 300K
* changed initial velocities (set/determined at 0.0 K) to:
`# Settings: temperature at 0 K`
`velocity       all create 2500.0 12345 rot yes mom yes dist gaussian`
`timestep       ${timestep}`
* changed thermo frequency from 50 to 10 since I'm only running 100 steps

## Molfind stuff: 

* molfind_41492932 files are before quench, these could not run because of the following error:
`RuntimeError: nonzero is not supported for tensors with more than INT_MAX elements,   file a support request`


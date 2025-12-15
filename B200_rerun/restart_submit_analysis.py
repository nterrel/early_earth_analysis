#!/usr/bin/env python3
"""
Restart/redo cumolfind segments listed in missing_segments.txt.

missing_segments.txt format (whitespace-separated):
/full/path/to/traj.dcd 7
/full/path/to/traj.dcd 8
...

Default behavior: WRITE slurm scripts to ./slurm_scripts (no submission).
Add -y to submit via sbatch.
"""

import os
import time
import argparse
import re
from simple_slurm import Slurm


def submit_job(
    traj_file: str,
    top_file: str,
    mol_pq: str,
    task: str,
    time_offset: str,
    num_segments: int,
    segment_index: int,
    output_dir: str,
    log_dir: str,
    submit: bool = False,
):
    job_name = (
        f"cumolfind_{os.path.splitext(os.path.basename(traj_file))[0]}"
        f"_segment_{segment_index:0{len(str(num_segments))}d}_of_{num_segments}"
    )

    os.makedirs(log_dir, exist_ok=True)
    output_filename = os.path.join(log_dir, f"{job_name}_%j.log")

    num_gpus = 1
    nodes = 1
    ntasks_per_node = num_gpus
    gres = "gpu:1"

    slurm = Slurm(
        job_name=job_name,
        ntasks=num_gpus,
        nodes=nodes,
        ntasks_per_node=ntasks_per_node,
        cpus_per_task=1,
        partition="hpg-b200",
        qos="mingjieliu-faimm",
        account="mingjieliu-faimm",
        gres=gres,
        mem_per_gpu="16gb",
        time="10:00:00",
        output=output_filename,
    )

    commands = [
        'echo "Date              = $(date)"',
        'echo "Hostname          = $(hostname -s)"',
        'echo "Working Directory = $(pwd)"',
        'echo ""',
        'echo "Number of Nodes Allocated      = $SLURM_JOB_NUM_NODES"',
        'echo "Nodes Allocated                = $SLURM_JOB_NODELIST"',
        'echo "Number of Tasks Allocated      = $SLURM_NTASKS"',
        'echo "Number of Cores/Task Allocated = $SLURM_CPUS_PER_TASK"',
        "module load cuda/12.9.1",
        'export LAMMPS_ANI_ROOT="/red/roitberg/lammps-ani"',
        "export LAMMPS_ROOT=${LAMMPS_ANI_ROOT}/external/lammps/",
        "export LAMMPS_PLUGIN_PATH=${LAMMPS_ANI_ROOT}/build/",
        "source $(conda info --base)/etc/profile.d/conda.sh",
        "conda activate /blue/roitberg/nterrel/Conda/envs/cumolfind",
        "echo using python: $(which python)",
        (
            f"cumolfind-molfind {traj_file} {top_file} {mol_pq} "
            f"--task={task} --time_offset={time_offset} "
            f"--dump_interval=50 --timestep=0.25 "
            f"--output_dir={output_dir} --num_segments={num_segments} --segment_index={segment_index}"
        ),
    ]

    script_body = "\n".join(commands) + "\n"

    if submit:
        slurm.sbatch(script_body, convert=False)
        # avoid identical timestamps in very fast submission loops
        time.sleep(0.1)
    else:
        script_dir = "slurm_scripts"
        os.makedirs(script_dir, exist_ok=True)
        script_path = os.path.join(script_dir, f"{job_name}.slurm")
        with open(script_path, "w") as f:
            f.write(str(slurm))
            f.write(script_body)
        print(f"Saved job script to {script_path}")


def parse_time_offset_from_traj(traj_file: str) -> str:
    # expects ..._<float>ns.dcd
    name = os.path.basename(traj_file)
    m = re.search(r"_(\d+\.\d+)ns\.dcd$", name)
    if not m:
        raise RuntimeError(
            f"Could not parse time_offset from trajectory filename: {name}")
    return m.group(1)


def main():
    parser = argparse.ArgumentParser(
        description="Resubmit cumolfind segments from missing_segments.txt.")
    parser.add_argument("--missing_txt", required=True,
                        help="Path to missing_segments.txt")
    parser.add_argument("--top", required=True, help="Topology file")
    parser.add_argument("--mol_pq", required=True,
                        help="Molecule database parquet")
    parser.add_argument("--task", choices=["analyze_trajectory",
                        "track_molecules"], required=True, default="analyze_trajectory")
    parser.add_argument("--num_segments", type=int, required=True,
                        help="Number of segments per trajectory (e.g., 10)")
    parser.add_argument("--output_dir", required=True,
                        help="Output directory for cumolfind parquet outputs")
    parser.add_argument("--log_dir", default="logs",
                        help="Directory for SLURM log files (default: ./logs)")
    parser.add_argument("-y", action="store_true",
                        help="If set, submit jobs; otherwise only write slurm scripts")
    args = parser.parse_args()

    # Read missing list
    items = []
    with open(args.missing_txt, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) < 2:
                raise RuntimeError(f"Bad line in {args.missing_txt}: {line!r}")
            traj_file = parts[0]
            seg = int(parts[1])
            items.append((traj_file, seg))

    if not items:
        print("No missing segments found in file; nothing to do.")
        return

    print(f"Found {len(items)} missing segments in {args.missing_txt}")

    # Generate scripts / submit
    for traj_file, seg in items:
        time_offset = parse_time_offset_from_traj(traj_file)
        submit_job(
            traj_file=traj_file,
            top_file=args.top,
            mol_pq=args.mol_pq,
            task=args.task,
            time_offset=time_offset,
            num_segments=args.num_segments,
            segment_index=seg,
            output_dir=args.output_dir,
            log_dir=args.log_dir,
            submit=args.y,
        )


if __name__ == "__main__":
    main()

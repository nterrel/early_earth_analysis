#!/usr/bin/env python3
import os, glob, time
import mdtraj as md
from top_loader import load_topology

# ── USER PARAMETERS ─────────────────────────────────────────────────────────────
trajectory_file = '/red/roitberg/22M_20231222_prodrun/2023-12-23-005238.631380_0.1ns.dcd'
topology_file   = '/red/roitberg/nick_analysis/traj_top_0.0ns.h5'

local_start  = 7319    # mdtraj sees frames 0…7999
global_start = 15319   # “real” index of local_start
stride       = 50
chunk_size   = 100

temp_dir     = '/red/roitberg/nick_analysis/trimmed_ala_frames'
output_file  = '/red/roitberg/nick_analysis/trimmed_ala_stride50.dcd'
# ── END USER PARAMETERS ──────────────────────────────────────────────────────────

os.makedirs(temp_dir, exist_ok=True)
topology = load_topology(topology_file)

file_offset = global_start - local_start          # 8000
desired     = set(range(global_start, file_offset-1, -stride))
print(f"Will extract {len(desired)} frames: {sorted(desired)[:3]} … {sorted(desired)[-3:]}")

t0           = time.time()
global_idx   = file_offset  # maps local 0→global 8000
chunk_count  = 0
saved_frames = 0

# STEP 1: dump one-frame DCDs with timing info
for chunk in md.iterload(trajectory_file, top=topology, chunk=chunk_size):
    chunk_start = time.time()
    start_idx   = global_idx
    end_idx     = global_idx + len(chunk) - 1
    chunk_count += 1

    load_time = time.time() - chunk_start
    print(f"[Chunk {chunk_count}] loaded frames {start_idx}–{end_idx} in {load_time:.2f}s")

    # find which desired globals fall in this chunk
    hits = [g for g in desired if start_idx <= g <= end_idx]
    for g in hits:
        frame_start = time.time()
        local_i = g - start_idx
        chunk[local_i].save_dcd(os.path.join(temp_dir, f"frame_{g}.dcd"))
        frame_time = time.time() - frame_start
        saved_frames += 1
        print(f"  → saved frame {g} in {frame_time:.2f}s (total saved: {saved_frames})")

    global_idx += len(chunk)

print(f"STEP 1 done in {time.time()-t0:.1f}s, dumped {saved_frames} files")

# STEP 2: concatenate them in ascending order
t1   = time.time()
dcds = glob.glob(os.path.join(temp_dir, "frame_*.dcd"))
dcds.sort(key=lambda fn: int(os.path.basename(fn).split('_')[1].split('.')[0]))
print(f"STEP 2: concatenating {len(dcds)} files…")

traj = md.load(dcds, top=topology)
traj.save_dcd(output_file)

print(f"STEP 2 done in {time.time()-t1:.1f}s; final DCD has {len(traj)} frames")
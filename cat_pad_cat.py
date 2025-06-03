# NOTE: This works but does not give a final xyz that is very compatible with visualizing with VMD since atom identities change in every frame (aside from the specified indices that we care about)

import glob
from pathlib import Path
from collections import defaultdict
import numpy as np

def parse_xyz_new_format(filename):
    with open(filename) as f:
        lines = [line.rstrip() for line in f if line.strip()]

    natoms     = int(lines[0])
    atom_lines = lines[2:2 + natoms]

    parsed = []
    for line in atom_lines:
        line = line.lstrip()
        if '# index:' in line:
            parts     = line.split('# index:')
            atom_line = parts[0].rstrip()
            index     = int(parts[1].strip())
        else:
            atom_line = line
            index     = None
        parsed.append((index, atom_line))
    return parsed


# ─── Path setup ────────────────────────────────────────────────────────────────
input_dir  = Path('ala_track_2.4ns_TEST')
output_dir = input_dir / "ordered_combined_xyzs"
output_dir.mkdir(exist_ok=True)

xyz_files    = glob.glob(str(input_dir / "*_frame_*.xyz"))
frame_groups = defaultdict(list)
for fname in xyz_files:
    fname = Path(fname)
    parts = fname.name.split("_frame_")
    if len(parts) != 2:
        continue
    frame_id = parts[1].split(".")[0]
    frame_groups[frame_id].append(fname)


# ─── Tracked indices from alanine ─────────────────────────────────────────────
tracked_set = {
    3056634, 4470849, 8050365, 8928897, 10743359,
    10957096, 13441041, 18074040, 18524165, 19327483,
    20153024, 22045873, 22433880
}


# ─── 1) Pre-pass: compute global centroid & max atom count ────────────────────
sum_xyz     = np.zeros(3, dtype=float)
total_count = 0
frame_counts = {}

for frame_id, files in frame_groups.items():
    count = 0
    for fname in files:
        for _, atom_line in parse_xyz_new_format(fname):
            x, y, z = map(float, atom_line.split()[1:4])
            sum_xyz += (x, y, z)
            total_count += 1
            count += 1
    frame_counts[frame_id] = count

if total_count == 0:
    raise RuntimeError("No atoms found in any frames!")

centroid  = sum_xyz / total_count
max_atoms = max(frame_counts.values())


# ─── 2) Combine, sort, pad, write per-frame & multi-frame ────────────────────
combined_dir = output_dir  / "FINAL_combined_xyzs"
combined_dir.mkdir(exist_ok=True)

multi_path = combined_dir / "all_frames_combined.xyz"
with open(multi_path, "w") as multi_fh:

    # iterate frames in numeric order
    for frame_id, files in sorted(frame_groups.items(), key=lambda kv: int(kv[0])):
        # --- collect & sort real atoms ---
        flat = []
        for fname in files:
            flat.extend(parse_xyz_new_format(fname))

        flat_sorted = sorted(
            flat,
            key=lambda x: (x[0] is None, x[0] if x[0] is not None else 0)
        )

        n_real    = len(flat_sorted)
        n_pad     = max_atoms - n_real

        # --- write individual padded file ---
        out_file = combined_dir / f"frame_{frame_id}_combined.xyz"
        with open(out_file, "w") as out:
            # header
            out.write(f"{n_real + n_pad}\n")
            out.write(
                "Fragments: "
                + " ".join(p.name.split('_target')[0] for p in files)
                + "\n"
            )
            # real atoms + comments
            for idx, atom_line in flat_sorted:
                comment = f"    # Index {idx}" if idx in tracked_set else ""
                out.write(f"{atom_line}{comment}\n")
            # dummy sulfurs at centroid
            cx, cy, cz = centroid
            for _ in range(n_pad):
                out.write(
                    f"S {cx:.6f} {cy:.6f} {cz:.6f}    # dummy sulfur anchor\n"
                )
        print(f"Wrote {out_file}")

        # --- append to multi-frame xyz ---
        with open(out_file) as cf:
            multi_fh.write(cf.read())

print(f"Wrote multi-frame trajectory: {multi_path}")

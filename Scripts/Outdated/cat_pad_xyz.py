import glob
from pathlib import Path
from collections import defaultdict

def parse_xyz_new_format(filename):
    with open(filename) as f:
        lines = [line.rstrip() for line in f if line.strip()]

    natoms = int(lines[0])
    atom_lines = lines[2:2 + natoms]

    parsed = []
    for line in atom_lines:
        line = line.lstrip()
        if '# index:' in line:
            parts = line.split('# index:')
            atom_line = parts[0].rstrip()
            index = int(parts[1].strip())
        else:
            atom_line = line
            index = None
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
sum_x = sum_y = sum_z = 0.0
total_count = 0
frame_counts = {}

for frame_id, files in frame_groups.items():
    count = 0
    for fname in files:
        parsed = parse_xyz_new_format(fname)
        for _, atom_line in parsed:
            # assume atom_line format: "Element x y z [..]"
            x, y, z = map(float, atom_line.split()[1:4])
            sum_x += x
            sum_y += y
            sum_z += z
            total_count += 1
            count += 1
    frame_counts[frame_id] = count

if total_count == 0:
    raise RuntimeError("No atoms found in any frames!")

centroid = (sum_x / total_count,
            sum_y / total_count,
            sum_z / total_count)
max_atoms = max(frame_counts.values())


# ─── 2) Combine, sort, pad, and write each frame ─────────────────────────────
for frame_id, files in frame_groups.items():
    # collect & sort
    flat_data = []
    for fname in files:
        flat_data.extend(parse_xyz_new_format(fname))

    flat_data_sorted = sorted(
        flat_data,
        key=lambda x: (x[0] is None, x[0] if x[0] is not None else 0)
    )

    n_real    = len(flat_data_sorted)
    n_missing = max_atoms - n_real

    # write out
    output_file = output_dir / f"frame_{frame_id}_combined.xyz"
    with open(output_file, "w") as out:
        # updated header
        out.write(f"{n_real + n_missing}\n")
        out.write(
            "Fragments: "
            + " ".join(f.name.split('_target')[0] for f in files)
            + "\n"
        )

        # real atoms (with tracked‐index comments)
        for idx, atom_line in flat_data_sorted:
            comment = f"    # Index {idx}" if idx in tracked_set else ""
            out.write(f"{atom_line}{comment}\n")

        # dummy sulfurs at the global centroid
        cx, cy, cz = centroid
        for _ in range(n_missing):
            out.write(
                f"S {cx:.6f} {cy:.6f} {cz:.6f}    # dummy sulfur anchor\n"
            )

    print(f"Wrote {output_file}")
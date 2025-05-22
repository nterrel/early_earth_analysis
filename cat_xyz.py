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


# Path setup
input_dir = Path('ala_track_2.4ns_TEST')
output_dir = input_dir / "combined_xyzs"
output_dir.mkdir(exist_ok=True)

xyz_files = glob.glob(str(input_dir / "*_frame_*.xyz"))
frame_groups = defaultdict(list)

for fname in xyz_files:
    fname = Path(fname)
    match = fname.name.split("_frame_")
    if len(match) != 2:
        continue
    try:
        frame_id = match[1].split(".")[0]
    except IndexError:
        continue
    frame_groups[frame_id].append(fname)

# Tracked indices from alanine
tracked_set = set([
    3056634, 4470849, 8050365, 8928897, 10743359,
    10957096, 13441041, 18074040, 18524165, 19327483,
    20153024, 22045873, 22433880
])

for frame_id, files in frame_groups.items():
    flat_data = []

    for fname in files:
        fragment_data = parse_xyz_new_format(fname)  # (idx or None, atom_line)
        flat_data.extend(fragment_data)

    # Sort by index where available, otherwise keep original order
    #flat_data_sorted = sorted(flat_data, key=lambda x: (x[0] is None, x[0] if x[0] is not None else 0))

    # above line is commented out to preserve the original order (corresponding to listed fragments in order)
    # rather than listing the tracked indices first
    flat_data_sorted = flat_data

    output_file = output_dir / f"frame_{frame_id}_combined.xyz"
    with open(output_file, "w") as out:
        out.write(f"{len(flat_data_sorted)}\n")
        out.write(f"Fragments: {' '.join([f.name.split('_target')[0] for f in files])}\n")

        for idx, atom_line in flat_data_sorted:
            comment = f"    # Index {idx}" if idx in tracked_set else ""
            out.write(f"{atom_line}{comment}\n")

    print(f"Wrote {output_file}")

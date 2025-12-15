import argparse
import os
from pathlib import Path


def pq_check(p: Path, min_bytes: int = 1024) -> bool:
    #    "Check if the file at path p exists and is larger than min_bytes."
    return p.exists() and p.is_file() and p.stat().st_size >= min_bytes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--traj_dir", required=True,
                    help="Directory containing .dcd files.")
    ap.add_argument("--out_dir", required=True,
                    help="Directory containing output parquet files.")
    ap.add_argument("--num_segments", type=int, default=10,
                    help="Number of segments per trajectory file.")
    ap.add_argument("--min_bytes", type=int, default=1024,
                    help="Minimum size in bytes for a valid parquet file.")
    ap.add_argument("--missing_txt", default="missing_segments.txt",
                    help="Output text file that lists missing segments.")
    args = ap.parse_args()

    traj_dir = Path(args.traj_dir)
    out_dir = Path(args.out_dir)

    traj_files = sorted(traj_dir.glob("*.dcd"))
    if not traj_files:
        raise SystemExit(f"No .dcd files found in {traj_dir}")

    missing_segments = []
    for traj in traj_files:
        stem = traj.stem
        for seg in range(args.num_segments):
            seg_tag = f"seg{seg:04d}of{args.num_segments:04d}"  # seg0000of0010
            f_formula = out_dir / f"{stem}_{seg_tag}_formula.pq"
            f_molecule = out_dir / f"{stem}_{seg_tag}_molecule.pq"

            if traj == traj_files[0] and seg == 0:
                print("DEBUG expected:", f_formula.name, f_molecule.name)
            ok = pq_check(f_formula, args.min_bytes) and pq_check(
                f_molecule, args.min_bytes)
            if not ok:
                missing_segments.append((str(traj), seg))

    with open(args.missing_txt, "w") as f:
        for traj_file, seg_index in missing_segments:
            f.write(f"{traj_file}\t{seg_index}\n")

    print(f"Trajectories: {len(traj_files)}")
    print(f"Missing segments: {len(missing_segments)}")
    print(f"Wrote: {args.missing_txt}")


if __name__ == "__main__":
    main()

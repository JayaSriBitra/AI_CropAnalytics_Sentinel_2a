"""Create a reproducible train/validation/test split without group leakage."""
import argparse
import csv
import random
from collections import defaultdict
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="CSV with sample_id,image_path,mask_path,group_id")
    parser.add_argument("--output", required=True, help="Output CSV path")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--train", type=float, default=0.70)
    parser.add_argument("--validation", type=float, default=0.15)
    parser.add_argument("--test", type=float, default=0.15)
    args = parser.parse_args()

    ratios = [args.train, args.validation, args.test]
    if any(r < 0 for r in ratios) or abs(sum(ratios) - 1.0) > 1e-8:
        parser.error("train, validation and test proportions must be non-negative and sum to 1")

    with open(args.input, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"sample_id", "image_path", "mask_path", "group_id"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            parser.error(f"Input CSV must contain columns: {', '.join(sorted(required))}")
        rows = list(reader)

    if not rows:
        parser.error("Input manifest contains no samples")
    if any(not row["group_id"].strip() for row in rows):
        parser.error("Every row must have a non-empty group_id")

    groups = defaultdict(list)
    for row in rows:
        groups[row["group_id"]].append(row)

    group_ids = list(groups)
    random.Random(args.seed).shuffle(group_ids)

    # Greedy assignment toward target sample counts while keeping each group intact.
    targets = [len(rows) * r for r in ratios]
    assigned = [[], [], []]
    counts = [0, 0, 0]
    # Place largest groups first after seeded shuffle to reduce imbalance.
    group_ids.sort(key=lambda gid: len(groups[gid]), reverse=True)

    for gid in group_ids:
        size = len(groups[gid])
        candidates = []
        for split_idx in range(3):
            projected = counts.copy()
            projected[split_idx] += size
            # Sum of squared normalized deviations from target counts.
            score = sum(
                ((projected[i] - targets[i]) / max(targets[i], 1.0)) ** 2
                for i in range(3)
            )
            candidates.append((score, split_idx))
        _, chosen = min(candidates)
        assigned[chosen].append(gid)
        counts[chosen] += size

    group_to_split = {}
    for idx, name in enumerate(("train", "validation", "test")):
        for gid in assigned[idx]:
            group_to_split[gid] = name

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    if "split" not in fieldnames:
        fieldnames.append("split")
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            out = dict(row)
            out["split"] = group_to_split[row["group_id"]]
            writer.writerow(out)

    print(f"Wrote {len(rows)} samples across {len(group_ids)} groups to {output_path}")
    for name, count in zip(("train", "validation", "test"), counts):
        print(f"{name}: {count} samples")
    print("Review the split and class representation before using it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

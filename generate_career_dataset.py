"""Generate a reproducible synthetic dataset for the Model 2 career quiz."""

import argparse
import random
from pathlib import Path

import pandas as pd

from career_diagnostic import QUESTIONS, calculate_role_scores, TARGET_ROLES


def generate_dataset(rows: int = 10_000, seed: int = 42) -> pd.DataFrame:
    if rows < 1:
        raise ValueError("rows must be positive")
    rng = random.Random(seed)
    records = []
    for _ in range(rows):
        answers = [rng.randrange(5) for _ in QUESTIONS]
        scores = calculate_role_scores(answers)
        target_role = max(TARGET_ROLES, key=lambda role: scores[role])
        records.append({**{f"Q{i + 1}": answer for i, answer in enumerate(answers)}, "target_role": target_role})
    return pd.DataFrame.from_records(records, columns=[*(f"Q{i}" for i in range(1, 11)), "target_role"])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("career_diagnostic_dataset.csv"))
    args = parser.parse_args()
    frame = generate_dataset(args.rows, args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(args.output, index=False)
    print(f"Wrote {len(frame):,} rows to {args.output}")
    print("Role counts:")
    print(frame["target_role"].value_counts().to_string())


if __name__ == "__main__":
    main()

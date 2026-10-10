"""Train and persist the Model 2 career classification pipeline."""

import argparse
import gc
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline


ROOT = Path(__file__).resolve().parent
FEATURES = [f"Q{i}" for i in range(1, 11)]


def train(dataset_path: Path, output_path: Path) -> Pipeline:
    if not dataset_path.is_file():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}. Run generate_career_dataset.py first.")
    frame = pd.read_csv(dataset_path)
    required = set(FEATURES + ["target_role"])
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {', '.join(sorted(missing))}")
    if frame.empty:
        raise ValueError("Dataset has no rows")
    X = frame[FEATURES].astype(int)
    y = frame["target_role"].astype(str)
    pipeline = Pipeline(
        [
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=300,
                    random_state=42,
                    class_weight="balanced",
                    n_jobs=1,
                ),
            )
        ]
    )
    pipeline.fit(X, y)

    training_rows = len(frame)
    learned_roles = sorted(y.unique())
    del X, y, frame
    gc.collect()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, output_path, compress=3)
    print(f"Saved pipeline to {output_path}")
    print(f"Training rows: {training_rows:,}; learned roles: {', '.join(learned_roles)}")
    return pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=ROOT / "career_diagnostic_dataset.csv")
    parser.add_argument("--output", type=Path, default=ROOT / "career_diagnostic_pipeline.joblib")
    args = parser.parse_args()
    train(args.dataset, args.output)


if __name__ == "__main__":
    main()

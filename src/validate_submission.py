"""
Validate FahMai RAG Challenge submission format.

Expected CSV format:
id,answer
1,5
2,3
...
100,2
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd


EXPECTED_ROWS = 100
EXPECTED_COLUMNS = ["id", "answer"]


def validate_submission(path: str | Path) -> None:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Submission file not found: {path}")

    df = pd.read_csv(path)

    if list(df.columns) != EXPECTED_COLUMNS:
        raise ValueError(
            f"Invalid columns. Expected {EXPECTED_COLUMNS}, got {list(df.columns)}"
        )

    if len(df) != EXPECTED_ROWS:
        raise ValueError(f"Expected {EXPECTED_ROWS} rows, got {len(df)} rows")

    if df["id"].duplicated().any():
        duplicated = df.loc[df["id"].duplicated(), "id"].tolist()
        raise ValueError(f"Duplicate IDs found: {duplicated}")

    expected_ids = set(range(1, EXPECTED_ROWS + 1))
    actual_ids = set(df["id"].astype(int).tolist())

    missing_ids = sorted(expected_ids - actual_ids)
    extra_ids = sorted(actual_ids - expected_ids)

    if missing_ids:
        raise ValueError(f"Missing IDs: {missing_ids}")

    if extra_ids:
        raise ValueError(f"Extra IDs: {extra_ids}")

    if not df["answer"].between(1, 10).all():
        invalid = df.loc[~df["answer"].between(1, 10)]
        raise ValueError(f"Invalid answer values found:\n{invalid}")

    print("Submission format is valid.")
    print(f"Rows: {len(df)}")
    print("Columns: id, answer")
    print("Answer range: 1–10")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python src/validate_submission.py <submission.csv>")
        raise SystemExit(1)

    validate_submission(sys.argv[1])


if __name__ == "__main__":
    main()

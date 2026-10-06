"""
CLI entry point.

Usage:
    python src/main.py --fasta data/sample/sample_sequences.fasta \
                        --env data/sample/sample_env.csv \
                        --out data/processed/risk_scores.csv
"""

import argparse
import sys
from pathlib import Path

# Allow running as `python src/main.py` from the project root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.pipeline import run_pipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Coffee batch contamination risk screening pipeline."
    )
    parser.add_argument(
        "--fasta", required=True, type=Path, help="Path to batch sequences FASTA file."
    )
    parser.add_argument(
        "--env", required=True, type=Path, help="Path to environmental metadata CSV."
    )
    parser.add_argument(
        "--out", required=True, type=Path, help="Path to write the risk-score CSV output."
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_pipeline(args.fasta, args.env, args.out)

    high_priority = result[result["high_priority_for_lab_testing"]]
    print(f"\nProcessed {len(result)} batches.")
    print(f"Flagged {len(high_priority)} batch(es) as high priority for lab testing.")
    print(f"Full results written to: {args.out}\n")
    print(result.to_string(index=False))


if __name__ == "__main__":
    main()

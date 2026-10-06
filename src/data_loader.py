"""
Load and validate the two input types the pipeline needs:
  1. FASTA sequences (batch samples to screen, and/or known marker genes)
  2. Environmental metadata CSV (one row per batch)

Keeping this isolated means swapping sample data for real data later
is a one-line change in main.py, not a rewrite.
"""

from pathlib import Path
from typing import Dict
import pandas as pd


def load_fasta(path: Path) -> Dict[str, str]:
    """
    Load a FASTA file into {record_id: sequence_string}.
    Minimal dependency-free parser (no Biopython required) — keeps the
    project installable with just requirements.txt even on a machine
    with a locked-down environment. Good enough for marker-gene /
    short-sequence use cases here; swap for Bio.SeqIO if you later need
    to handle more exotic FASTA edge cases.
    Raises a clear error if the file is missing or empty, rather than
    failing deep inside the pipeline.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"FASTA file not found: {path}")

    records: Dict[str, str] = {}
    current_id = None
    current_seq_parts = []

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if current_id is not None:
                    records[current_id] = "".join(current_seq_parts).upper()
                current_id = line[1:].split()[0]  # first whitespace-delimited token
                current_seq_parts = []
            else:
                current_seq_parts.append(line)
        if current_id is not None:
            records[current_id] = "".join(current_seq_parts).upper()

    if not records:
        raise ValueError(f"No sequences found in {path} — is it a valid FASTA file?")

    return records


def load_environment_csv(path: Path) -> pd.DataFrame:
    """
    Load per-batch environmental metadata.
    Expected columns: batch_id, humidity_pct, storage_days,
    temperature_c, origin_region
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Environmental CSV not found: {path}")

    df = pd.read_csv(path)

    required_cols = {
        "batch_id",
        "humidity_pct",
        "storage_days",
        "temperature_c",
        "origin_region",
    }
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(
            f"Environmental CSV is missing required columns: {sorted(missing)}"
        )

    return df

"""
Sequence and environmental feature extraction for the
coffee OTA screening pipeline.

Sequence evidence is generated using a local NCBI BLAST+
blastn search against the curated OTA reference database.

The k-mer similarity function is retained only for backwards
compatibility/testing. It is NOT used for the production
BLAST-based sequence evidence.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional
import shutil
import subprocess
import tempfile

import pandas as pd

from src.config import (
    KMER_SIZE,
    MARKER_MATCH_THRESHOLD,
)


# ------------------------------------------------------------------
# k-mer compatibility functions
# ------------------------------------------------------------------

def _kmers(sequence: str, k: int) -> set:
    if len(sequence) < k:
        return {sequence}

    return {
        sequence[i:i + k]
        for i in range(len(sequence) - k + 1)
    }


def kmer_similarity(
    sequence: str,
    marker_sequence: str,
    k: int = KMER_SIZE,
) -> float:
    """
    Backwards-compatible Jaccard k-mer similarity.

    This function is retained for legacy tests only.
    Production sequence evidence uses BLAST+.
    """

    set_a = _kmers(sequence, k)
    set_b = _kmers(marker_sequence, k)

    if not set_a or not set_b:
        return 0.0

    intersection = len(set_a & set_b)
    union = len(set_a | set_b)

    return intersection / union if union else 0.0


# ------------------------------------------------------------------
# BLAST helpers
# ------------------------------------------------------------------

BLAST_COLUMNS = [
    "qseqid",
    "sseqid",
    "pident",
    "length",
    "mismatch",
    "gapopen",
    "qstart",
    "qend",
    "sstart",
    "send",
    "evalue",
    "bitscore",
    "qlen",
    "slen",
]


def _clean_sequence(sequence: str) -> str:
    """
    Validate and normalize a DNA sequence.
    """

    sequence = str(sequence).upper().replace(" ", "").replace("\n", "")

    valid = set("ACGTN")

    if not sequence:
        raise ValueError("Empty DNA sequence")

    invalid = set(sequence) - valid

    if invalid:
        raise ValueError(
            f"Invalid DNA bases found: {sorted(invalid)}"
        )

    return sequence


def _query_fasta(
    sequence: str,
    query_id: str,
    output_path: Path,
) -> None:
    """
    Write one query sequence as FASTA.
    """

    output_path.write_text(
        f">{query_id}\n{sequence}\n",
        encoding="utf-8",
    )


def _calculate_query_coverage(row: pd.Series) -> float:
    """
    BLAST query coverage:

        aligned query length / full query length * 100

    For a normal ungapped BLAST alignment this corresponds closely
    to alignment length / query length.
    """

    qlen = float(row["qlen"])

    if qlen <= 0:
        return 0.0

    return (
        float(row["length"]) / qlen
    ) * 100.0


def run_blastn(
    sequence: str,
    query_id: str,
    blast_db: Path,
    runtime_dir: Path,
    evalue: float = 1e-5,
    max_target_seqs: int = 20,
) -> pd.DataFrame:
    """
    Execute real NCBI BLAST+ blastn against the local OTA
    nucleotide reference database.

    Returns one row per BLAST hit.

    This function actually invokes the external blastn executable.
    """

    blastn = shutil.which("blastn")

    if blastn is None:
        raise RuntimeError(
            "blastn executable was not found in PATH."
        )

    blast_db = Path(blast_db)
    runtime_dir = Path(runtime_dir)

    runtime_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    sequence = _clean_sequence(sequence)

    with tempfile.TemporaryDirectory(
        dir=str(runtime_dir),
        prefix="blast_query_",
    ) as tmpdir:

        tmpdir = Path(tmpdir)

        query_file = tmpdir / "query.fasta"
        output_file = tmpdir / "blast.tsv"

        _query_fasta(
            sequence,
            query_id,
            query_file,
        )

        cmd = [
            blastn,
            "-query",
            str(query_file),
            "-db",
            str(blast_db),
            "-out",
            str(output_file),
            "-outfmt",
            "6 " + " ".join(BLAST_COLUMNS),
            "-evalue",
            str(evalue),
            "-max_target_seqs",
            str(max_target_seqs),
            "-task",
            "blastn",
        ]

        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
        )

        if completed.returncode != 0:
            raise RuntimeError(
                "blastn failed.\n"
                f"STDOUT:\n{completed.stdout}\n"
                f"STDERR:\n{completed.stderr}"
            )

        if not output_file.exists():
            raise RuntimeError(
                "blastn completed but produced no output file."
            )

        if output_file.stat().st_size == 0:
            return pd.DataFrame(
                columns=BLAST_COLUMNS + ["query_coverage"]
            )

        hits = pd.read_csv(
            output_file,
            sep="\t",
            header=None,
            names=BLAST_COLUMNS,
        )

        hits["query_coverage"] = hits.apply(
            _calculate_query_coverage,
            axis=1,
        )

        return hits


# ------------------------------------------------------------------
# BLAST evidence classification
# ------------------------------------------------------------------

def classify_blast_hit(
    pident: float,
    query_coverage: float,
    alignment_length: int,
    evalue: float,
) -> str:
    """
    Transparent computational evidence classification.

    IMPORTANT:
    These categories are computational evidence classes,
    not probabilities of OTA contamination.

    Thresholds are kept configurable and should not be described
    as biologically validated until independently revalidated
    using executable BLAST results.
    """

    if (
        pident >= 90.0
        and query_coverage >= 90.0
        and alignment_length >= 150
        and evalue <= 1e-5
    ):
        return "HIGH"

    if (
        pident >= 85.0
        and query_coverage >= 80.0
        and alignment_length >= 100
        and evalue <= 1e-5
    ):
        return "MODERATE"

    if evalue <= 1e-5:
        return "LOW"

    return "NO_SIGNIFICANT_EVIDENCE"


def best_blast_match(
    sequence: str,
    query_id: str,
    blast_db: Path,
    runtime_dir: Path,
) -> Dict[str, object]:
    """
    Run BLAST and return the strongest observed hit.

    Best hit is ranked primarily by:
        1. bit score
        2. percent identity
        3. query coverage
    """

    hits = run_blastn(
        sequence=sequence,
        query_id=query_id,
        blast_db=blast_db,
        runtime_dir=runtime_dir,
    )

    if hits.empty:
        return {
            "best_marker_id": None,
            "best_pident": 0.0,
            "best_query_coverage": 0.0,
            "best_alignment_length": 0,
            "best_evalue": None,
            "best_bitscore": 0.0,
            "blast_hit_count": 0,
            "blast_evidence_class": "NO_SIGNIFICANT_EVIDENCE",
            "blast_executed": True,
        }

    hits = hits.sort_values(
        by=[
            "bitscore",
            "pident",
            "query_coverage",
        ],
        ascending=False,
    )

    best = hits.iloc[0]

    evidence_class = classify_blast_hit(
        pident=float(best["pident"]),
        query_coverage=float(best["query_coverage"]),
        alignment_length=int(best["length"]),
        evalue=float(best["evalue"]),
    )

    return {
        "best_marker_id": str(best["sseqid"]),
        "best_pident": float(best["pident"]),
        "best_query_coverage": float(best["query_coverage"]),
        "best_alignment_length": int(best["length"]),
        "best_evalue": float(best["evalue"]),
        "best_bitscore": float(best["bitscore"]),
        "blast_hit_count": int(len(hits)),
        "blast_evidence_class": evidence_class,
        "blast_executed": True,
    }


# ------------------------------------------------------------------
# Production sequence feature extraction
# ------------------------------------------------------------------

def sequence_features(
    batch_sequences: Dict[str, str],
    marker_genes: Optional[Dict[str, str]] = None,
    blast_db: Optional[Path] = None,
    runtime_dir: Optional[Path] = None,
) -> pd.DataFrame:
    """
    Generate production sequence evidence using real BLAST+.

    marker_genes is retained in the function signature for backwards
    compatibility but is NOT used for production matching.

    Parameters
    ----------
    batch_sequences
        Mapping of batch_id -> DNA sequence.

    marker_genes
        Legacy argument. Not used by the BLAST engine.

    blast_db
        Path/prefix of the BLAST nucleotide database.

    runtime_dir
        Temporary runtime directory for BLAST query/output files.
    """

    if blast_db is None:
        raise ValueError(
            "blast_db must be supplied for real BLAST sequence analysis."
        )

    if runtime_dir is None:
        runtime_dir = Path.cwd() / "blast_runtime"

    rows = []

    for batch_id, sequence in batch_sequences.items():

        result = best_blast_match(
            sequence=sequence,
            query_id=str(batch_id),
            blast_db=Path(blast_db),
            runtime_dir=Path(runtime_dir),
        )

        rows.append(
            {
                "batch_id": batch_id,

                # Legacy-compatible field.
                # This is now derived from BLAST identity rather than
                # k-mer Jaccard similarity.
                "marker_match_score": (
                    result["best_pident"] / 100.0
                ),

                "marker_matched": result["best_marker_id"],

                "has_marker_evidence": (
                    result["blast_evidence_class"]
                    in {"HIGH", "MODERATE", "LOW"}
                ),

                "blast_pident": result["best_pident"],
                "blast_query_coverage": result[
                    "best_query_coverage"
                ],
                "blast_alignment_length": result[
                    "best_alignment_length"
                ],
                "blast_evalue": result["best_evalue"],
                "blast_bitscore": result["best_bitscore"],
                "blast_hit_count": result["blast_hit_count"],
                "blast_evidence_class": result[
                    "blast_evidence_class"
                ],
                "blast_executed": result["blast_executed"],
            }
        )

    return pd.DataFrame(rows)


# ------------------------------------------------------------------
# Environmental features
# ------------------------------------------------------------------

def environmental_risk_features(
    env_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Convert environmental variables into a transparent 0-1 risk score.
    """

    df = env_df.copy()

    def norm(col: pd.Series) -> pd.Series:

        span = col.max() - col.min()

        if span == 0:
            return pd.Series(
                [0.5] * len(col),
                index=col.index,
            )

        return (col - col.min()) / span

    humidity_risk = norm(df["humidity_pct"])
    storage_risk = norm(df["storage_days"])
    temperature_risk = norm(df["temperature_c"])

    df["env_risk_score"] = (
        humidity_risk * 0.4
        + storage_risk * 0.35
        + temperature_risk * 0.25
    )

    return df[
        [
            "batch_id",
            "env_risk_score",
            "origin_region",
        ]
    ]

"""
Turn raw inputs into numeric features the risk model can use.

Two feature sources:
  A) Sequence evidence  — how similar is a batch's sequence to known
     OTA (ochratoxin A) marker genes? Implemented as a lightweight
     k-mer Jaccard-similarity scorer (no external BLAST dependency, so
     it runs anywhere). This is a stand-in for real BLAST+ homology
     search — see the NOTE below for upgrading it.

  B) Environmental evidence — humidity, storage duration, temperature
     and origin region are documented real-world drivers of fungal
     (Aspergillus/Penicillium) growth and OTA production. These are
     normalized into a 0-1 risk-contribution score per batch.

NOTE on upgrading sequence matching to real BLAST+:
  Once you have NCBI BLAST+ installed locally, replace
  `kmer_similarity()` with a call to `blastn` (via Biopython's
  Bio.Blast.Applications.NcbiblastnCommandline) against a local marker
  database, and use percent identity / e-value instead of k-mer
  similarity. Keep the function signature the same
  (sequence, marker_dict) -> float so nothing else in the pipeline
  needs to change.
"""

from typing import Dict
import pandas as pd

from src.config import KMER_SIZE, MARKER_MATCH_THRESHOLD


def _kmers(sequence: str, k: int) -> set:
    if len(sequence) < k:
        return {sequence}
    return {sequence[i : i + k] for i in range(len(sequence) - k + 1)}


def kmer_similarity(sequence: str, marker_sequence: str, k: int = KMER_SIZE) -> float:
    """
    Jaccard similarity between the k-mer sets of two sequences.
    Returns a value in [0, 1]; higher means more similar.
    """
    set_a = _kmers(sequence, k)
    set_b = _kmers(marker_sequence, k)
    if not set_a or not set_b:
        return 0.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union else 0.0


def best_marker_match(sequence: str, marker_genes: Dict[str, str]) -> Dict[str, float]:
    """
    Compare one batch sequence against every known marker gene and
    return the best match's score and which marker it matched.
    """
    best_score = 0.0
    best_marker = None
    for marker_id, marker_seq in marker_genes.items():
        score = kmer_similarity(sequence, marker_seq)
        if score > best_score:
            best_score = score
            best_marker = marker_id
    return {"best_marker_score": best_score, "best_marker_id": best_marker}


def sequence_features(
    batch_sequences: Dict[str, str], marker_genes: Dict[str, str]
) -> pd.DataFrame:
    """
    Build a per-batch dataframe of sequence-evidence features.
    batch_sequences keys are expected to match batch_id values used in
    the environmental CSV (the FASTA record id IS the batch id).
    """
    rows = []
    for batch_id, seq in batch_sequences.items():
        match = best_marker_match(seq, marker_genes)
        rows.append(
            {
                "batch_id": batch_id,
                "marker_match_score": match["best_marker_score"],
                "marker_matched": match["best_marker_id"],
                "has_marker_evidence": match["best_marker_score"]
                >= MARKER_MATCH_THRESHOLD,
            }
        )
    return pd.DataFrame(rows)


def environmental_risk_features(env_df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert raw environmental columns into a normalized 0-1
    env_risk_score per batch. Simple, explainable min-max normalization
    plus domain-informed direction (higher humidity/storage/temp ->
    higher risk). Replace with a learned model once you have labeled
    outcome data (actual lab contamination results).
    """
    df = env_df.copy()

    def norm(col: pd.Series) -> pd.Series:
        span = col.max() - col.min()
        if span == 0:
            return pd.Series([0.5] * len(col), index=col.index)
        return (col - col.min()) / span

    humidity_risk = norm(df["humidity_pct"])
    storage_risk = norm(df["storage_days"])
    temperature_risk = norm(df["temperature_c"])

    df["env_risk_score"] = (
        humidity_risk * 0.4 + storage_risk * 0.35 + temperature_risk * 0.25
    )

    return df[["batch_id", "env_risk_score", "origin_region"]]

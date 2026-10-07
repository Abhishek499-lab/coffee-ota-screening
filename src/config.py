"""
Central config: file paths, thresholds, and tunable constants.
Change values here rather than hunting through the pipeline code.
"""

from pathlib import Path

# --- Paths -------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
SAMPLE_DIR = DATA_DIR / "sample"
PROCESSED_DIR = DATA_DIR / "processed"

# --- Feature extraction --------------------------------------------------
# k-mer length used for the lightweight sequence-similarity scorer.
# Production sequence evidence uses the executable BLAST+ engine implemented in src.feature_extraction.py.
# sensitivity; k-mer similarity is a fast, dependency-free stand-in.
KMER_SIZE = 6

# Similarity score (0-1) above which a sequence is considered a
# plausible match to a known OTA marker gene. Tune this once you have
# real labeled data; this is a placeholder.
MARKER_MATCH_THRESHOLD = 0.35

# --- Risk scoring --------------------------------------------------------
# Weights for combining the two evidence sources into one risk score.
# Must sum to 1.0. Adjust once you know which signal is more reliable
# for your actual data.
SEQUENCE_EVIDENCE_WEIGHT = 0.6
ENVIRONMENT_EVIDENCE_WEIGHT = 0.4

# Risk score (0-1) above which a batch is flagged "high priority" for
# full lab testing.
HIGH_RISK_THRESHOLD = 0.6

RANDOM_SEED = 42

"""
Sanity tests against the synthetic sample data. These confirm the
pipeline runs end-to-end and produces sane output shape — they do NOT
validate real-world contamination-detection accuracy (that requires
real labeled data, see PROGRESS.md).

Run with: python -m pytest tests/
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.pipeline import run_pipeline
from src.feature_extraction import kmer_similarity
from src.risk_model import train_demo_model

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SAMPLE_FASTA = PROJECT_ROOT / "data" / "sample" / "sample_sequences.fasta"
SAMPLE_ENV = PROJECT_ROOT / "data" / "sample" / "sample_env.csv"
TEST_OUTPUT = PROJECT_ROOT / "data" / "processed" / "test_risk_scores.csv"


def test_kmer_similarity_identical_sequences():
    seq = "ATGGCTCGTACCGGTAAGCTTGACC"
    assert kmer_similarity(seq, seq) == 1.0


def test_kmer_similarity_different_sequences():
    score = kmer_similarity("AAAAAAAAAA", "TTTTTTTTTT")
    assert 0.0 <= score < 0.5


def test_pipeline_runs_end_to_end():
    result = run_pipeline(SAMPLE_FASTA, SAMPLE_ENV, TEST_OUTPUT)

    assert len(result) == 5
    assert "final_risk_score" in result.columns
    assert "high_priority_for_lab_testing" in result.columns
    assert result["final_risk_score"].between(0, 1).all()
    assert TEST_OUTPUT.exists()


def test_demo_model_trains_without_error():
    model, accuracy = train_demo_model(n_samples=100)
    assert 0.0 <= accuracy <= 1.0
    assert model is not None


if __name__ == "__main__":
    test_kmer_similarity_identical_sequences()
    test_kmer_similarity_different_sequences()
    test_pipeline_runs_end_to_end()
    test_demo_model_trains_without_error()
    print("All tests passed.")

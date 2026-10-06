"""
Orchestrates the end-to-end run: load data -> extract features ->
score risk -> save output. Kept separate from main.py so this can also
be imported and called directly from a notebook or test file.
"""

from pathlib import Path
import pandas as pd

from src.data_loader import load_fasta, load_environment_csv
from src.feature_extraction import sequence_features, environmental_risk_features
from src.risk_model import combine_scores


# Placeholder marker genes used until real NCBI reference sequences are
# added (see README "Swapping in real data"). Short illustrative
# sequences only — NOT validated real OTA marker genes.
PLACEHOLDER_MARKER_GENES = {
    "placeholder_OTA_marker_1": (
        "ATGGCTCGTACCGGTAAGCTTGACCGTATGCCTAGGTTACGGATCCGTAAGCTTGG"
    ),
    "placeholder_OTA_marker_2": (
        "ATGCCGTACGGATTCCGTAAGGCTTGACCGATCGGTACCGGATCCTTAAGGCTTAC"
    ),
}


def run_pipeline(fasta_path: Path, env_csv_path: Path, output_path: Path) -> pd.DataFrame:
    """
    Run the full pipeline and write the result to output_path.
    Returns the result dataframe as well, for programmatic / test use.
    """
    batch_sequences = load_fasta(fasta_path)
    env_df = load_environment_csv(env_csv_path)

    seq_feat = sequence_features(batch_sequences, PLACEHOLDER_MARKER_GENES)
    env_feat = environmental_risk_features(env_df)

    result = combine_scores(seq_feat, env_feat)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_path, index=False)

    return result

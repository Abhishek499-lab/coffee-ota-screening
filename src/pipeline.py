from pathlib import Path
import csv
import subprocess

from src.data_loader import load_fasta, load_environment_csv
from src.feature_extraction import sequence_features, environmental_risk_features
from src.risk_model import combine_scores


CANONICAL_BLAST_ID_MAP = {
    "AY272043": "OTA001",
    "AY196315": "OTA002",
    "AY534879": "OTA003",
    "AY583209": "OTA004",
    "DQ054596": "OTA005",
}


def _parse_fasta(path):
    records = []

    current_header = None
    current_sequence = []

    with open(path, "r") as fh:
        for line in fh:
            line = line.strip()

            if not line:
                continue

            if line.startswith(">"):
                if current_header is not None:
                    records.append(
                        (
                            current_header,
                            "".join(current_sequence)
                        )
                    )

                current_header = line[1:]
                current_sequence = []

            else:
                current_sequence.append(line)

    if current_header is not None:
        records.append(
            (
                current_header,
                "".join(current_sequence)
            )
        )

    return records


def _prepare_blast_database(reference_fasta, runtime_dir):
    """
    Build a BLAST-compatible runtime database using canonical IDs.

    The original reference FASTA is never modified. Long public
    FASTA headers are converted to OTA001–OTA005 while preserving
    accession-level provenance in a runtime mapping file.
    """

    runtime_dir = Path(runtime_dir)
    runtime_dir.mkdir(parents=True, exist_ok=True)

    normalized_fasta = (
        runtime_dir / "ota_markers_blast_compatible.fasta"
    )

    mapping_csv = runtime_dir / "ota_blast_id_mapping.csv"

    db_dir = runtime_dir / "normalized_db"
    db_dir.mkdir(parents=True, exist_ok=True)

    db_prefix = db_dir / "ota_markers"

    records = _parse_fasta(reference_fasta)

    if len(records) != 5:
        raise ValueError(
            "Expected exactly 5 OTA reference sequences."
        )

    normalized_records = []

    for header, sequence in records:

        accession = header.split("|")[0]

        if accession not in CANONICAL_BLAST_ID_MAP:
            raise ValueError(
                f"Unexpected OTA reference accession: {accession}"
            )

        blast_id = CANONICAL_BLAST_ID_MAP[accession]

        sequence = sequence.upper()

        invalid = sorted(
            set(sequence) - set("ACGTN")
        )

        if invalid:
            raise ValueError(
                f"Invalid DNA bases in {accession}: {invalid}"
            )

        normalized_records.append(
            (
                blast_id,
                accession,
                header,
                sequence
            )
        )

    normalized_records.sort(
        key=lambda x: int(x[0].replace("OTA", ""))
    )

    with open(normalized_fasta, "w") as fh:
        for blast_id, accession, header, sequence in normalized_records:
            fh.write(f">{blast_id}\n")

            for i in range(0, len(sequence), 80):
                fh.write(sequence[i:i + 80] + "\n")

    with open(mapping_csv, "w", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "blast_marker_id",
                "accession",
                "original_fasta_header",
                "length_nt",
            ],
        )

        writer.writeheader()

        for blast_id, accession, header, sequence in normalized_records:
            writer.writerow({
                "blast_marker_id": blast_id,
                "accession": accession,
                "original_fasta_header": header,
                "length_nt": len(sequence),
            })

    # Rebuild DB every time from the current reference FASTA.
    for suffix in [".nhr", ".nin", ".nsq", ".ndb", ".not", ".ntf", ".nto"]:
        path = Path(str(db_prefix) + suffix)

        if path.exists():
            path.unlink()

    result = subprocess.run(
        [
            "makeblastdb",
            "-in",
            str(normalized_fasta),
            "-dbtype",
            "nucl",
            "-parse_seqids",
            "-out",
            str(db_prefix),
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "makeblastdb failed:\n"
            + result.stdout
            + "\n"
            + result.stderr
        )

    required = [
        Path(str(db_prefix) + ".nhr"),
        Path(str(db_prefix) + ".nin"),
        Path(str(db_prefix) + ".nsq"),
    ]

    if not all(path.exists() for path in required):
        raise RuntimeError(
            "BLAST database was not created completely."
        )

    return db_prefix


def run_pipeline(fasta_path, env_csv_path, output_path):
    """
    Execute the complete OTA screening pipeline.

    Sequence evidence is generated by the executable BLAST+
    engine. The bundled reference FASTA is normalized to canonical
    BLAST IDs at runtime so long public FASTA headers do not prevent
    reproducible database construction.
    """

    fasta_path = Path(fasta_path)
    env_csv_path = Path(env_csv_path)
    output_path = Path(output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    batch_sequences = load_fasta(fasta_path)
    environment = load_environment_csv(env_csv_path)

    reference_fasta = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "reference"
        / "ota_reference_markers.fasta"
    )

    if not reference_fasta.exists():
        raise FileNotFoundError(
            f"OTA reference FASTA not found: {reference_fasta}"
        )

    blast_runtime = (
        output_path.parent
        / "blast_runtime"
    )

    blast_db = _prepare_blast_database(
        reference_fasta=reference_fasta,
        runtime_dir=blast_runtime,
    )

    seq_feat = sequence_features(
        batch_sequences=batch_sequences,
        blast_db=blast_db,
        runtime_dir=blast_runtime,
    )

    env_feat = environmental_risk_features(environment)

    result = combine_scores(
        seq_feat,
        env_feat,
    )

    result.to_csv(output_path, index=False)

    return result

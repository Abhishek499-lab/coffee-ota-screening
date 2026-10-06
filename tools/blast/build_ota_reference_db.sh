#!/bin/bash
set -e

# Build the local OTA marker BLAST database.
# Requires BLAST+ to be installed and available as makeblastdb.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

makeblastdb \
    -in "${SCRIPT_DIR}/ota_markers_blast.fasta" \
    -dbtype nucl \
    -parse_seqids \
    -out "${SCRIPT_DIR}/ota_reference_db/ota_markers"

echo "OTA reference BLAST database created."

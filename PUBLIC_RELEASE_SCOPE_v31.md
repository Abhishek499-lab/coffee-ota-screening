# Coffee OTA Screening — Public Release Scope

This repository contains the reproducible computational core and selected
validation/statistical evidence for the Coffee OTA Screening project.

## Intended role

The pipeline is intended for computational pre-screening and triage.

It is NOT a replacement for laboratory confirmation of ochratoxin A (OTA).

Sequence similarity or detection of an OTA-associated reference marker does
not by itself demonstrate OTA toxin production.

## Included

- Core Python pipeline
- Unit/regression tests
- Sample data
- OTA reference sequences and mapping
- Reproducible BLAST database build script
- Verified real OTA contamination dataset
- Final statistical consolidation
- Master computational validation summaries
- Production pipeline evidence

## Excluded

Large intermediate biological challenge datasets, raw GenBank records,
BLAST database binaries, intermediate audit history, temporary files and
large generated query collections are intentionally excluded from the public
source release.

The original complete project remains in the local Google Drive project
directory.

## Validation interpretation

The validation package demonstrates computational control performance and
the tested biological challenge results. It does not establish universal
biological specificity or prove OTA production from sequence evidence alone.

Confirmatory laboratory testing remains required.

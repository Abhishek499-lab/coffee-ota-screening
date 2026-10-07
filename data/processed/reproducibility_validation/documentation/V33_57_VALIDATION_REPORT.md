# Coffee OTA Screening — Executable Validation Evidence

## Purpose

This package contains computational validation evidence for the executable
BLAST-based sequence-screening workflow used in the coffee OTA pre-screening
project.

The package is intended to make the previously generated validation evidence
available in a structured and reproducible form.

## Validation sets

### V33.3 — Fresh executable computational controls

Purpose:
- Positive reference-derived sequence controls
- Computational negative controls
- Verification that the executable BLAST workflow can distinguish these
  predefined controls under the tested conditions

Interpretation:
- Computational control validation only.
- This does not establish biological sensitivity or specificity.

### V33.5 — Executable identity calibration

Purpose:
- Synthetic sequence-divergence calibration across predefined identity levels.

Interpretation:
- Demonstrates computational behavior of the implemented BLAST workflow
  under the tested synthetic sequence perturbations.
- Does not establish an optimal biological detection threshold.

### V33.6 — Biological near-neighbour challenge panel

Purpose:
- Executable testing against the predefined related-sequence challenge panel.

Interpretation:
- Supports discrimination of this specific challenge panel.
- Does not establish universal biological specificity.

### V33.11 — Expanded historical negative controls

Purpose:
- Fresh executable reproduction of the predefined 133-sequence negative-control
  panel using the current public BLAST implementation.

Interpretation:
- Supports computational discrimination of this tested negative-control set.
- Does not establish universal biological specificity.

## Claim boundary

The following claims are supported:

- Computational reproducibility
- Reference-derived positive detection
- Computational negative-control discrimination
- Challenge-panel discrimination

The following claims are NOT established:

- Biological sensitivity
- Biological specificity
- Clinical sensitivity
- Clinical specificity
- OTA production from sequence similarity alone
- Direct sequence-based validation of the 65 Turkish coffee samples

The workflow is a computational pre-screening/triage layer and does not
replace confirmatory laboratory testing.

## Release status

This directory is a release candidate.

No GitHub push or public release is performed by this validation step.


# Project Progress — Coffee OTA Screening Pipeline

## Current stage

Latest consolidated documentation stage: v29


## COMPLETED

- Repository structure
- Modular Python implementation
- Configuration handling
- Input validation
- Sequence quality control
- OTA reference sequence panel
- Local BLAST database
- BLAST-based sequence detection
- Controlled positive validation
- Controlled negative validation
- Expanded computational negative controls
- Biological near-neighbour challenge
- Annotated CDS-level provenance audit
- Production regression testing
- Master sequence-validation consolidation
- Published real OTA contamination dataset integration
- Censored-data statistical analysis
- Two-part contamination analysis
- Nonparametric sensitivity analysis
- Final statistical evidence consolidation
- README documentation update


## SEQUENCE VALIDATION

Current production candidate rule:

Identity >= 80%
Query coverage >= 90%
Alignment length >= 100 nt
E-value <= 1e-5

Validation results:

- Controlled positives: 5/5 detected
- Controlled unrelated negatives: 0/3 false hits
- Expanded computational negatives: 0/133 false hits
- Biological challenge: 0/13 significant false hits

Interpretation:

The sequence workflow has strong computational validation and a limited biological challenge panel.

Universal biological specificity has NOT been established.


## REAL CONTAMINATION DATASET

Published laboratory dataset:

- Total samples: 65
- OTA detected: 53
- Below LOD: 12
- Detection limit: 0.23 microgram/kg
- Sampling years: 2021–2024
- Detected concentration range: 0.26–19.11 microgram/kg


## FINAL STATISTICAL INTERPRETATION

The consolidated analyses do not demonstrate a statistically significant temporal increase in OTA contamination.

Primary results:

- Full censored model: p = 0.678
- Detection component: p = 0.803
- Detected concentration component: p = 0.141
- Nonparametric cross-check: p = 0.142
- Sensitivity excluding 19.11 microgram/kg: p = 0.081

Detected-only exploratory analyses showed some year-specific differences.

These are not treated as proof of a temporal trend.


## IMPORTANT SCIENTIFIC LIMITATION

The real contamination dataset is not sequence-paired.

Therefore:

- no quantitative sequence-to-concentration model is claimed;
- sequence similarity is not interpreted as proof of toxin production;
- laboratory confirmation remains necessary.


## NEXT VALIDATION PRIORITIES

1. Expand independent biological challenge sequences.
2. Obtain sequence-linked laboratory OTA measurements.
3. Evaluate the production detector on independent blinded samples.
4. Perform external validation on an independent dataset.
5. Reassess thresholds after sufficiently large biological validation.


## CURRENT PROJECT STATUS

Repository: COMPLETE
Computational pipeline: COMPLETE
OTA reference database: COMPLETE
Computational validation: COMPLETE
Real contamination dataset: COMPLETE
Statistical consolidation: COMPLETE
Biological validation: LIMITED
External biological benchmarking: PENDING
Sequence-linked laboratory validation: PENDING

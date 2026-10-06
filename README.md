
# Coffee OTA Contamination Pre-Screening Pipeline

A reproducible computational pipeline for pre-screening and triage of potential ochratoxin A (OTA) contamination risk in coffee using sequence evidence and environmental risk factors.

IMPORTANT:
This project is a computational pre-screening / triage framework. It is not a replacement for confirmatory laboratory testing. Sequence similarity alone does not establish OTA toxin production.


## CURRENT PROJECT STATUS

### Repository and software

- Repository structure: COMPLETE
- Modular Python code: COMPLETE
- Configuration handling: COMPLETE
- Data loading and validation: COMPLETE
- Feature extraction: COMPLETE
- Risk scoring: COMPLETE
- Automated tests: PRESENT
- Sample data: PRESENT
- Documentation: UPDATED
- Offline reproducibility: DEMONSTRATED


## OTA SEQUENCE EVIDENCE

- Curated OTA-associated reference sequences: COMPLETE
- Local BLAST database: COMPLETE
- BLAST-based sequence detection: IMPLEMENTED
- Controlled positive validation: 5/5 detected
- Controlled unrelated negatives: 0/3 false hits
- Expanded computational negatives: 0/133 false hits
- Biological challenge panel: LIMITED PANEL COMPLETED
- Universal biological specificity: NOT ESTABLISHED
- OTA toxin production proven by sequence alone: NO


## REAL CONTAMINATION DATA

A published laboratory dataset containing individual OTA measurements has been incorporated for contamination-level analysis.

Dataset:

- Total samples: 65
- OTA detected: 53
- Below LOD: 12
- Detection limit: 0.23 microgram/kg
- Detected concentration range: 0.26–19.11 microgram/kg
- Sampling years: 2021–2024

The concentration dataset is not sequence-paired.

Therefore, it is NOT used to claim a quantitative sequence-to-OTA relationship.


## FINAL STATISTICAL VALIDATION

The real contamination dataset has undergone a consolidated statistical analysis.

Key results:

- Detection prevalence did not differ significantly across years.
- Full-data censored model: p = 0.678
- Two-part detection model: p = 0.803
- Detected-concentration model: p = 0.141
- Nonparametric cross-check: p = 0.142
- Sensitivity analysis excluding the 19.11 microgram/kg observation: p = 0.081

Current interpretation:

The available data do not demonstrate a statistically significant temporal increase in OTA contamination from 2021 to 2024.

Some detected-only exploratory analyses showed year-pair differences. These are treated as exploratory findings and not as proof of a demonstrated temporal trend.


## SEQUENCE VALIDATION

The sequence detection workflow has been tested using:

1. Curated OTA-associated reference sequences
2. Exact internal positive-control sequences
3. Unrelated computational negative controls
4. GC- and length-matched computational negatives
5. Real biological near-neighbour sequences
6. Annotated CDS-level biological challenge sequences
7. Threshold sensitivity analysis
8. Production-style regression testing

Current production candidate rule:

- Identity >= 80%
- Query coverage >= 90%
- Alignment length >= 100 nt
- E-value <= 1e-5

This is a computational evidence threshold.

It is NOT a validated probability of OTA contamination.


## BIOLOGICAL VALIDATION STATUS

The project currently contains a limited biological challenge panel.

Final biological challenge:

- 13 annotated CDS-level sequences
- Related fungal P450, PKS and NRPS sequences
- OTA reference sequences removed from the challenge panel
- 0 significant OTA-reference BLAST hits

Safe interpretation:

"No significant OTA-reference BLAST hit was observed in the tested biological challenge panel."

This does NOT establish universal biological specificity.

Broader independent biological benchmarking remains a future validation step.


## REAL OTA CONTAMINATION ANALYSIS

Overall dataset:

- Total samples: 65
- OTA detected: 53
- Below LOD: 12
- Detection rate: 81.5%
- LOD: 0.23 microgram/kg
- Detected range: 0.26–19.11 microgram/kg
- Detected median: 1.22 microgram/kg
- Detected mean: approximately 1.756 microgram/kg

The below-LOD observations are retained as censored observations.

They are NOT treated as zero.


## REGULATORY SCREENING

The dataset was additionally screened against concentration thresholds.

At 3 microgram/kg:

- 3 samples exceeded the threshold.

At 5 microgram/kg:

- 1 sample exceeded the threshold.

These are screening comparisons only.

Regulatory interpretation depends on the applicable product category and regulatory framework.


## FINAL SCIENTIFIC INTERPRETATION

### Supported

- OTA was detected in 53 of 65 published samples.
- 12 samples were below the reported detection limit.
- The dataset contains substantial variation in OTA concentration.
- Some detected-only analyses showed differences between particular years.
- The 19.11 microgram/kg observation is an influential high concentration.
- Sensitivity analyses were performed to assess its influence.

### Not supported

- A demonstrated monotonic increase in OTA contamination from 2021 to 2024.
- A statistically significant year effect in the primary full-data censored analysis.
- Universal biological specificity of the sequence detector.
- Proof of OTA toxin production from sequence similarity alone.
- A quantitative sequence-to-OTA concentration model from the current published dataset.


## WORKFLOW

Input sequence
    |
    v
Sequence quality control
    |
    v
Local BLAST against OTA reference panel
    |
    v
Molecular evidence classification
    |
    v
Environmental risk features
    |
    v
Transparent weighted risk score
    |
    v
Pre-screen / triage category
    |
    v
Confirmatory laboratory testing


## REPOSITORY STRUCTURE

Company/
    README.md
    PROGRESS.md
    requirements.txt

    src/
        __init__.py
        config.py
        data_loader.py
        feature_extraction.py
        main.py
        pipeline.py
        risk_model.py

    tests/
        test_pipeline.py

    data/
        processed/
        sample/
        reference/


## REPRODUCIBILITY

Major sequence-validation outputs are stored under:

data/processed/blast_validation/

Real contamination analysis outputs are stored under:

data/processed/real_contamination_v20_3/
data/processed/real_contamination_v21_statistics/
data/processed/real_contamination_v22_inferential/
data/processed/real_contamination_v23_effect_sizes/
data/processed/real_contamination_v24_censored_model/
data/processed/real_contamination_v25_2_metadata_corrected/
data/processed/real_contamination_v27_turnbull_npmle/
data/processed/real_contamination_v28_final_statistical_consolidation/

Final statistical consolidation:

data/processed/real_contamination_v28_final_statistical_consolidation/

Key report:

FINAL_STATISTICAL_REPORT_v28.txt


## LIMITATIONS

1. The published contamination dataset is not sequence-paired.
2. It cannot establish a quantitative sequence-to-OTA relationship.
3. Below-LOD concentrations are censored rather than exact measurements.
4. The biological challenge panel is limited in size.
5. Universal biological specificity has not been established.
6. Sequence similarity does not prove OTA toxin production.
7. The environmental risk score is a transparent heuristic and is not a validated probability.
8. Confirmatory laboratory testing remains necessary for actual contamination determination.


## INTENDED USE

This repository is intended for:

- computational pre-screening
- research triage
- sequence-based evidence assessment
- reproducible contamination-risk analysis
- method development and validation

It should NOT be used as a standalone:

- regulatory certification tool
- food-safety certification system
- diagnostic system
- laboratory replacement


## VALIDATION PHILOSOPHY

The project deliberately separates:

Computational validation

from

Biological validation

from

Laboratory confirmation

from

Proof of toxin production

These distinctions are maintained throughout the project to avoid overinterpretation of computational evidence.


## CURRENT DEVELOPMENT STAGE

Research prototype with a validated computational workflow and real published contamination-level analysis.

Main remaining validation needs:

1. Broader independent biological benchmarking
2. Sequence-linked laboratory OTA measurements
3. Independent blinded-sample evaluation
4. External validation
5. Reassessment of thresholds after sufficiently large biological validation


## LAST UPDATED

v29 — Current project documentation and validation status.

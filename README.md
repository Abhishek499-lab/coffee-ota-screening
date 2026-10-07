# Coffee OTA Contamination Pre-Screening Pipeline

A reproducible computational framework for **pre-screening and triage of potential ochratoxin A (OTA) contamination risk in coffee** using molecular sequence evidence and environmental risk factors.

> **Important:** This repository is a computational pre-screening / triage framework. It is **not a replacement for confirmatory laboratory testing**. Sequence similarity alone does not establish OTA toxin production.

---

## Overview

Ochratoxin A (OTA) is a mycotoxin of food-safety interest that can occur in coffee and other agricultural products.

This project combines two evidence streams:

1. **Molecular sequence evidence** from local BLAST comparison against a curated OTA-associated reference panel.
2. **Environmental risk features** related to humidity, storage duration, and temperature.

The outputs are combined into a transparent heuristic risk score intended for **research screening and triage**, not regulatory certification or laboratory diagnosis.

---

## Project Status

| Component | Status |
|---|---|
| Modular Python pipeline | Complete |
| Data validation | Complete |
| Sequence QC | Complete |
| OTA reference panel | Complete |
| Local BLAST workflow | Complete |
| Controlled positive validation | Complete |
| Computational negative controls | Complete |
| Biological challenge panel | Limited panel completed |
| Real published OTA dataset | Integrated |
| Statistical analysis | Complete |
| Automated tests | Passing |
| Public GitHub release | Complete |
| Universal biological specificity | Not established |
| Sequence-only proof of OTA production | Not established |

---

## 1. Workflow

~~~text
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
~~~

---

## 2. Molecular Sequence Evidence

The sequence workflow uses a curated set of five OTA-associated reference sequences and a local BLAST database.

The reference panel includes OTA-associated:

- polyketide synthase (PKS)
- nonribosomal peptide synthetase (NRPS)
- cytochrome P450

sequences from relevant fungal sources.

### Validation results

The current public implementation uses executable BLASTN against the
versioned OTA reference database.

The executable BLAST workflow is implemented in the public source tree.
Detailed validation results are intentionally documented separately until the
corresponding reproducibility artifacts are released.

These computational checks do **not** establish
biological or clinical sensitivity/specificity.

> **No significant OTA-reference BLAST hit was observed in the tested
> biological challenge panel or the 133-sequence expanded negative-control
> panel.**

The challenge and negative-control panels remain limited relative to the
diversity of environmental and biological sequences that may occur in
real-world coffee samples.

This computational screening workflow should therefore be interpreted as a pre-screening or triage tool rather than a laboratory confirmation assay.

---

## 3. Production Sequence-Evidence Rule

The current production candidate rule is:

- Identity >= **80%**
- Query coverage >= **90%**
- Alignment length >= **100 nt**
- E-value <= **1e-5**

This is a **computational evidence threshold**.

It is **not** a validated probability of OTA contamination.

---

## 4. Environmental Risk Features

The environmental component uses three features:

- Relative humidity
- Storage duration
- Temperature

Current environmental weighting:

| Feature | Weight |
|---|---:|
| Relative humidity | 0.40 |
| Storage duration | 0.35 |
| Temperature | 0.25 |

Evidence-stream weighting:

| Evidence stream | Weight |
|---|---:|
| Sequence evidence | 0.60 |
| Environmental evidence | 0.40 |

The resulting score is a **transparent heuristic triage score**, not a calibrated probability of contamination.

---

## 5. Real Published OTA Contamination Dataset

The project incorporates a published laboratory dataset containing OTA measurements from commercially available Turkish coffee.

### Dataset summary

- Total samples: **65**
- OTA detected: **53**
- Below LOD: **12**
- Detection rate: **81.5%**
- Detection limit: **0.23 µg/kg**
- Detected concentration range: **0.26–19.11 µg/kg**
- Sampling years: **2021–2024**

The published contamination dataset is **not sequence-paired** and therefore is not used to train a quantitative sequence-to-OTA concentration model.

---

## 6. Statistical Analysis

The real contamination dataset was analysed using complementary statistical approaches.

- Primary full-data censored model: **p = 0.678**
- Two-part detection component: **p = 0.803**
- Detected-concentration component: **p = 0.141**
- Nonparametric cross-check: **p = 0.142**
- Sensitivity analysis excluding the 19.11 µg/kg observation: **p = 0.081**

The available data do **not** demonstrate a statistically significant temporal increase in OTA contamination from 2021 to 2024.

---

## 7. Regulatory Screening

At **3 µg/kg**, 3 samples exceeded the threshold.

At **5 µg/kg**, 1 sample exceeded the threshold.

These comparisons are screening analyses only. Regulatory interpretation depends on the applicable product category, jurisdiction, sampling framework, and regulatory standard.

---

## 8. Scientific Interpretation

### Supported by the current analysis

- OTA was detected in **53 of 65** published samples.
- **12 samples** were below the reported detection limit.
- The dataset shows substantial variation in OTA concentration.
- Controlled positive sequences were successfully detected.
- No significant OTA-reference hit was observed in the tested biological challenge panel.

### Not supported by the current evidence

The current evidence does **not** establish:

- a demonstrated monotonic increase in OTA contamination from 2021 to 2024
- universal biological specificity
- proof of OTA toxin production from sequence similarity alone
- a quantitative sequence-to-OTA concentration relationship
- a validated probability of contamination from the heuristic risk score

---

## 9. Validation Philosophy

~~~text
Computational validation
          |
          v
Biological validation
          |
          v
Laboratory confirmation
          |
          v
Proof of toxin production
~~~

A computational sequence match is treated as **screening evidence**, not direct proof that a coffee sample contains OTA.

---

## 10. Reproducibility

### Installation

~~~bash
git clone https://github.com/Abhishek499-lab/coffee-ota-screening.git
cd coffee-ota-screening
pip install -r requirements.txt
~~~

### Run tests

~~~bash
pytest -q
~~~

### Build the local OTA BLAST database

~~~bash
bash tools/blast/build_ota_reference_db.sh
~~~

---

## 11. Repository Structure

~~~text
coffee-ota-screening/
├── README.md
├── PROGRESS.md
├── requirements.txt
├── LICENSE
├── src/
├── tests/
├── data/
└── tools/
    └── blast/
~~~

---

## 12. Key Validation Outputs

Sequence validation:

`data/processed/blast_validation/`

Master validation:

`data/processed/blast_validation/MASTER_VALIDATION/`

`data/processed/blast_validation/MASTER_VALIDATION_v18/`

Real contamination dataset:

`data/processed/real_contamination_v20_3/`

Final statistical consolidation:

`data/processed/real_contamination_v28_final_statistical_consolidation/`

---

## 13. Limitations

1. The published contamination dataset is not sequence-paired.
2. It cannot establish a quantitative sequence-to-OTA relationship.
3. Below-LOD concentrations are censored rather than exact measurements.
4. The biological challenge panel is limited in size.
5. Universal biological specificity has not been established.
6. Sequence similarity does not prove OTA toxin production.
7. The environmental risk score is a transparent heuristic.
8. The production sequence threshold is not a universal biological cutoff.
9. Independent blinded-sample validation remains necessary.
10. Confirmatory laboratory testing remains necessary for actual contamination determination.

---

## 14. Intended Use

This repository is intended for:

- computational pre-screening
- research triage
- sequence-based evidence assessment
- reproducible contamination-risk analysis
- method development
- computational validation

It should **not** be used as a standalone regulatory certification, food-safety certification, diagnostic, or laboratory-replacement system.

---

## 15. Current Development Stage

**Research prototype with a validated computational workflow and real published contamination-level analysis.**

Remaining validation needs include:

1. Broader independent biological benchmarking
2. Sequence-linked laboratory OTA measurements
3. Independent blinded-sample evaluation
4. External validation
5. Reassessment of thresholds after sufficiently large biological validation

---

## 16. Citation and Data Source

The real contamination dataset incorporated in this project is derived from:

**Investigation of Ochratoxin A Levels in Commercially Available Turkish Coffee and Risk Assessment.**

DOI:

https://doi.org/10.3390/toxins18020084

The original publication should be cited when reusing the processed dataset or findings derived from it.

---

## 17. License

This project is distributed under the license included in the repository.

See:

`LICENSE`

---

## 18. Current Public Release

**V31.6 — Public release and audit verified**

Verified properties:

- Public GitHub repository
- `main` branch
- 48 tracked release files
- 5 OTA reference markers
- 65 published contamination samples
- 53 OTA-detected samples
- 12 below-LOD samples
- Validation evidence included
- No high-confidence secret patterns detected

---

## Final Note

This project is designed to make computational screening **reproducible, transparent, and appropriately bounded**.

A computational risk signal should be treated as a reason for further investigation—not as proof that a food sample contains OTA.

**Repository:**  
https://github.com/Abhishek499-lab/coffee-ota-screening


## Data provenance and independent re-analysis

The real-contamination dataset used in this repository was reconstructed
from Table 1 of the published study:

**Investigation of Ochratoxin A Levels in Commercially Available Turkish Coffee and Risk Assessment**

- Journal: *Toxins*
- DOI: `10.3390/toxins18020084`
- Published source: PMC article [PMC12944870]
- Source table: Table 1 — Amounts of OTA in Turkish coffee samples
- Detection method reported by the study: HPLC fluorescence detection
- Published dataset size: 65 Turkish coffee samples
- OTA detected: 53 samples
- Below LOD: 12 samples
- LOD: 0.23 ng/g

A row-level audit against the official PMC article reproduced all 65 sample
observations exactly, including the year-wise sample counts, `<LOD` records,
and the full detected concentration range (0.26–19.11 ng/g).

The statistical analyses in this repository are **independent re-analyses**
of the published observations. Their p-values and model results should not
be interpreted as statistics reported by the original publication.

This dataset is used here for reproducible computational analysis and does
not represent newly generated laboratory measurements.

## Validation status

The repository contains an executable BLAST+ sequence-screening implementation using
`blastn` and runtime construction of the bundled OTA reference database.

The implementation has been exercised in controlled and fresh-clone environments.
However, detailed V33 validation output artifacts are not currently committed to this
public repository. Therefore, specific V33.x PASS metrics are intentionally not presented
here as independently verifiable public evidence.

**Current public status: BLAST integration implemented; full validation evidence release
pending — see `PROGRESS.md`.**

The workflow is intended for computational pre-screening/triage and does not replace
confirmatory laboratory testing. Sequence similarity alone does not establish OTA toxin
production, and biological sensitivity/specificity have not been established by this
repository.

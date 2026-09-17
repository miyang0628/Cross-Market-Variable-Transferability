# Cross-Market Variable Transferability: A Multi-Country Validation and Two-Dimensional Extension

> **Anonymous repository for double-blind peer review.**
> All author, institutional, and identifying information has been removed.
> Please do not attempt to de-anonymize the authors.

This repository contains the analysis code, derived data references, and figures
for an extension study of the Cross-Market Variable Transferability Score (CMVTS).
The study validates the transferability framework across nine Asian target markets
using real demand-side microdata, breaks the circularity of the original
single-pair design by using an independent outcome measure, and extends the
one-dimensional transfer tier into a two-dimensional decision framework.

---

## Overview

The original CMVTS framework assessed whether alternative credit-scoring variables
developed in a source market can be transferred to a target market **before** any
target-market data are collected, using a composite of distributional, rank-order,
and structural similarity measures. That framework rested on a single, structurally
comparable market pair, leaving open whether its verdict reflected genuine market
similarity or favourable pair selection.

This extension addresses that gap in four ways:

1. **Multi-country validation.** The macro-structural predictor is computed for a
   source market against nine target markets and correlated with an independently
   measured outcome (realized behavioural divergence from demand-side microdata).
2. **Circularity break.** The predictor and the outcome are drawn from disjoint
   variable groups and different data sources, so the validation does not reuse the
   same inputs on both sides.
3. **Component re-derivation.** The rank-order component is redefined on a
   cross-country basis after the original within-pair formulation is shown to be
   unstable when the source market is extremal on most indicators.
4. **Two-dimensional decision framework.** Transferability and local absorptive
   capacity (bank-sector efficiency) are shown to be independent axes; the original
   one-dimensional tier is extended into a four-quadrant decision grid.

---

## Repository structure

```
.
├── data/                # input data references and small derived tables
├── notebooks/           # analysis notebooks (numbered by execution order)
├── results/
│   ├── figures/         # generated figures (PNG + PDF, 600 dpi, greyscale)
│   └── tables/          # generated result tables (CSV)
└── README.md
```

> **Note on data.** Large primary datasets are **not** redistributed in this
> repository because of source licensing and size. `data/` holds only small derived
> lookup tables and pointers to the public sources below. See **Data access**.

---

## Notebooks

Notebooks are numbered by execution order. Earlier notebooks (01–02) are exploratory
and document methodological pitfalls that motivated the final design; the settled
pipeline begins at 03.

| # | Notebook | Purpose |
|---|----------|---------|
| 01 | predictor–outcome pilot | First predictor–outcome check; surfaces a source-distribution contamination pitfall. |
| 02 | source-distribution construction | Builds the source behavioural distribution; identifies a binning artifact. |
| 03 | outcome robustness | Confirms the outcome is invariant to distribution construction (rank cross-check). |
| 04 | macro-indicator extraction | Pulls open macro indicators (nine countries × two vintages). |
| 05 | macro components C2/C3 | Computes the redefined rank-order and cosine components (normalization-corrected). |
| 06 | component diagnosis | Diagnoses and fixes the rank-order component; motivates the cross-country redefinition. |
| 07 | macro-CMVTS validation | Headline predictor–outcome validation, weight insensitivity, vintage sensitivity. |
| 08 | two-dimensional framework | Independent-label check, four-quadrant grid, placement sensitivity, figures. |
| 09 | figures (spectrum, validation) | Generates the penetration-spectrum and predictor–outcome figures. |
| 10 | figures (weights, vintage) | Generates the weight-insensitivity and vintage-stability figures. |

**Reproducibility notes.** Notebook 05 supersedes an earlier buggy version in which
a min–max normalization broke rank order; the current notebook computes the
rank-order component on raw values. The threshold-calibration analysis originally
attempted a one-dimensional ROC calibration; it was superseded by the
two-dimensional framework in notebook 08 after the outcome label was found to be
independent of the transferability axis.

---

## Results

Generated artifacts are written to `results/`.

**Figures** (`results/figures/`, PNG + PDF, 600 dpi, greyscale, legends at bottom):

| File | Content |
|------|---------|
| `fig_5_1_penetration_spectrum` | Target-market proxy-penetration spectrum across nine countries. |
| `fig_5_2_predictor_outcome` | Macro-CMVTS vs realized behavioural divergence (headline validation). |
| `fig_5_2b_outcome_vs_penetration` | Outcome vs card-activity penetration (illustrates the penetration-driven outcome). |
| `fig_5_4_weight_insensitivity` | Predictor–outcome correlation across macro weight combinations. |
| `fig_5_5_vintage_stability` | Macro-CMVTS at two indicator vintages per country. |
| `fig_2d_decision_grid` | Two-dimensional transferability × absorptive-capacity decision grid. |
| `fig_label_independence` | Independence of the efficiency label from the transferability axis. |
| `fig_sensitivity_fliprate` | Quadrant-placement stability under split-rule variation and jitter. |

**Tables** (`results/tables/`, CSV):

| File | Content |
|------|---------|
| `wdi_macro_2021`, `wdi_macro_latest` | Macro-indicator matrices by vintage. |
| `cmvts_C2C3_2021`, `cmvts_C2C3_latest` | Rank-order and cosine components by vintage. |
| `macro_cmvts_headline` | Headline macro-CMVTS and outcome per country. |
| `cmvts_2d_grid` | Two-dimensional grid coordinates and quadrant assignments. |
| `imf_fdi_label` | Financial-development sub-indices used as the absorptive-capacity label. |

---

## Data access

All primary data come from public sources. None are redistributed here; obtain them
directly and place them under `data/` (or adjust the path constants at the top of
each notebook).

- **Source-market credit bureau microdata** — a synthetic personal credit-bureau
  dataset from a national open-data platform. Registration/login required on the
  provider's portal.
- **Target-market demand-side microdata** — a cross-country financial-inclusion
  survey (2024 collection wave), individual-level labelled CSV. Available from the
  publisher's microdata catalog after free registration.
- **Macro indicators** — a public development-indicators database, retrieved via its
  open API (no key required). The extraction notebook queries it directly.
- **Financial-development sub-indices** — a public financial-development index
  dataset from an international financial institution, downloadable as CSV.

Exact indicator codes, the predictor/outcome variable separation, and the mapping
from source-market scorecard variables to survey proxies are documented in the
notebooks and in the indicator-design note included with the analysis.

---

## Requirements

```
python >= 3.10
numpy
pandas
scipy
matplotlib
seaborn
```

Install with:

```bash
pip install numpy pandas scipy matplotlib seaborn
```

---

## Reproduction

1. Obtain the primary datasets (see **Data access**) and place them under `data/`,
   updating the path constants at the top of each notebook if needed.
2. Run the notebooks in order. `04` requires network access to the public
   development-indicators API; all other notebooks run offline once the input files
   are present.
3. Figures and tables are written to `results/figures/` and `results/tables/`.

Notebooks 01–02 are not required for the final results; they are retained to
document the methodological decisions. The minimal path to the headline results is
`03 → 04 → 05 → 06 → 07 → 08`, followed by `09 → 10` for the remaining figures.

---

## Method summary

- **Predictor (transferability).** A macro-structural similarity score between the
  source and each target market, combining a cross-country rank-order component and
  a cosine-similarity component over open macro indicators. Outcome-linked
  behavioural indicators are excluded from the predictor to preserve independence.
- **Outcome (realized divergence).** An information-theoretic divergence between the
  source behavioural distribution (from source-market credit data) and each target
  market's observed activity distribution (from demand-side survey microdata).
- **Absorptive-capacity label.** A bank-sector efficiency sub-index from a
  prior-literature financial-development index, independent of the transferability
  axis and used only for the two-dimensional decision framework.
- **Decision framework.** A four-quadrant grid over transferability and absorptive
  capacity, extending the original one-dimensional transfer tier.

---

## License

Code in this repository is released for review purposes. A license will be attached
on de-anonymized release. Primary datasets remain under their respective providers'
licenses and are not redistributed here.

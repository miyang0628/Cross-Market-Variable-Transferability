# Cross-Market Variable Transferability — Multi-Country Validation and Two-Dimensional Extension

Analysis code and results for a study that extends the Cross-Market Variable
Transferability Score (CMVTS) — a pre-entry framework for judging whether
alternative credit-scoring variables developed in one market can be deployed in
another — from a single market pair to nine Asian target markets.

The study makes four contributions:

1. **Multi-country validation.** The macro predictor is computed for a source
   market (Republic of Korea) against nine target markets and correlated with an
   independently measured outcome.
2. **Circularity-free design.** The predictor and the outcome are **disjoint by
   data source**: the predictor uses only infrastructure and macroeconomic
   indicators from the World Bank WDI, while the outcome is measured from a separate
   demand-side survey (Global Findex). The predictor is shown to anticipate the
   behavioural-activity **penetration gap** between markets — the first-order
   constraint on a transferred card-based scorecard — rather than realised transfer
   performance.
3. **Corrected rank-order component.** The original rank-order component is unstable
   when the source market is extremal on most indicators; it is redefined on a
   cross-country basis.
4. **Two-dimensional decision framework.** Transferability and local absorptive
   capacity (bank-sector efficiency) are shown to be independent axes, extending the
   one-dimensional transfer tier into a four-quadrant decision grid.

---

## Repository structure

```
.
├── data/                       raw data (NOT redistributed — see data/README.txt)
├── notebooks/                  analysis scripts, numbered by execution order
├── results/
│   ├── figures/                generated figures (PNG + PDF, 600 dpi, greyscale)
│   └── tables/                 result tables (CSV) and the IMF FDI label
├── requirements.txt
└── README.md
```

---

## Notebooks

Run in order from the `notebooks/` folder. Scripts read raw data from `../data/`
and derived CSVs from `../results/`, and write outputs to `../results/tables/` and
`../results/figures/`.

| Script | Purpose |
|--------|---------|
| `01_source_scorecard_and_outcome.py` | Build the Korean source behavioural distribution (from credit-bureau records) and the realized-divergence **outcome** from Findex card-activity penetration. |
| `02_wdi_extraction.py` | Fetch the **predictor** indicators (WDI infrastructure + macro scale only) from the World Bank API for two vintages. |
| `03_cmvts_components.py` | Compute the macro predictor: `C2` (cross-country rank), `C3` (cosine), and equal-weight `macro-CMVTS`. |
| `04_validation.py` | Headline predictor–outcome association, leave-one-out, and weight-insensitivity checks. |
| `05_two_dimensional_framework.py` | FIE independence check, quadrant assignment, and jitter stability. |
| `06_figures.py` | Regenerate figures from the result tables. |

**Circularity note.** The predictor (`02`/`03`) draws only on WDI infrastructure and
macro-scale indicators; the outcome (`01`) draws only on the Findex survey. No
variable and no data source is shared between them. This is the design that makes
the validation free of the circularity discussed in the paper.

---

## Key results (WDI-only predictor)

| Quantity | Value |
|----------|-------|
| Predictor–outcome association (equal weight) | Spearman **−0.73** (p = 0.025) |
| Cosine component alone (`C3`) | Spearman −0.88 |
| Leave-one-out range | −0.64 to −0.83 |
| Weight-grid range | −0.73 to −0.88 (always significant) |
| FIE label independence | Spearman **+0.30** (p = 0.43; weak, non-significant) |
| Vintage stability (mean abs. shift) | 0.025 |

**Two-dimensional quadrants** (median split): Q1 direct transfer — Thailand, Viet Nam,
Philippines; Q3 transfer with monitoring — Indonesia, Cambodia; Q2 redevelop on
functioning base — Bangladesh, Pakistan; Q4 local redevelopment — Nepal, Lao PDR.
Indonesia (the target of the original single-pair study) moves from an unqualified
high-transferability verdict to transfer-with-monitoring.

Result tables are in `results/tables/`:
`outcome_realized_divergence.csv`, `cmvts_components.csv`,
`two_dimensional_grid.csv`, `imf_fdi_label.csv`.

---

## Data access

Raw data are not redistributed here (licensing and size). See `data/README.txt`.

- **Findex 2025 microdata** (2024 wave) — World Bank Global Findex microdata
  catalog, free registration.
- **Korean synthetic personal credit-bureau data** — AI-Hub open-data platform
  (`dataSetSn = 71792`), login required.
- **WDI indicators** — World Bank open API, fetched by `02_wdi_extraction.py`
  (no key needed).
- **IMF Financial Development Index** — public CSV from the IMF; the derived
  `FIE` label is included at `results/tables/imf_fdi_label.csv`.

---

## Requirements

```
python >= 3.10
numpy, pandas, scipy, matplotlib, seaborn
```

```bash
pip install -r requirements.txt
```

---

## Reproduction

1. Obtain the raw datasets and place them under `data/` (see `data/README.txt`).
2. From `notebooks/`, run `01 → 02 → 03 → 04 → 05 → 06` in order.
   `02` requires network access to the World Bank API; the rest run offline once the
   inputs are present.
3. Tables appear in `results/tables/`, figures in `results/figures/`.

---

## License

Code is released for review and reproduction. Primary datasets remain under their
respective providers' licenses and are not redistributed here.

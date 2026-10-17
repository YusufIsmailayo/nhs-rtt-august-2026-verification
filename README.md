# August 2026 RTT and Cancer Waiting Times: verification before writing

A Bronze → Silver → Gold pipeline (Python, pandas, Parquet, Jupyter) built to
test a claim *before* I write about it. Every figure I had for the August 2026
release came from secondary sources (the BMA's compilation and Healthcare
Management). This pipeline rebuilds them from NHS England's own files.

**Status: reconciliation gate PASSES (51 of 51 checks). Notebooks 00–09 built; the findings table is `data/gold/08_findings/findings.csv` (readable copy: `findings.md`). No article has been written.**

## Run order

```
pip install -r requirements.txt
cd notebooks
jupyter nbconvert --to notebook --execute --inplace 00_sources.ipynb 01_bronze.ipynb 02_silver_rtt.ipynb 03_silver_cwt.ipynb 04_reconciliation_gate.ipynb 05_gold_divergence.ipynb 06_gold_pathways_patients.ipynb 07_gold_cancer.ipynb 08_findings.ipynb 09_charts.ipynb
```

`04_reconciliation_gate.ipynb` raises on any failed check, so a scripted run exits non-zero.

Bronze (about 175 MB of NHS England files) and Silver are not in git. `01_bronze` re-downloads
every file from the URLs in `src/sources.py`, and each `data/bronze/*/metadata.json` written
there records the SHA-256 I got, so you can tell whether NHS England still serves the same bytes.
NHS England rotates its file URLs; if one 404s, find the file on the page named in `source_page`.

| Notebook | Layer | What it does |
|---|---|---|
| `00_sources` | — | catalogue of every file (all primary NHS England outputs), the claims under test, the measure |
| `01_bronze` | Bronze | downloads unmodified files with SHA-256; reuses Two Maps' Apr–Jul 2026 RTT extracts only after URL, hash and server size checks |
| `02_silver_rtt` | Silver | 17 months (Apr 2025 – Aug 2026), provider grain, NONC excluded, measures from weekly bands |
| `03_silver_cwt` | Silver | provider basis, FDS / 31D / 62D headline slices with waiting-time bands, trusts proven to sum to the England row; August 2025 as first published (old layout) |
| `04_reconciliation_gate` | Gold 00 | rebuilds NHS England's published figures on both measures; writes `reconciliation.csv`, `claims_vs_primary.csv`, `headline_rebuilt.csv` |
| `05_gold_divergence` | Gold 05 | list vs tail indexed to April 2025 and March 2026, on reported / constant-panel / headline bases; the three-row table; the March 2026 investigation (revision, breadth, tail-cohort exits, flows, targets) |
| `06_gold_pathways_patients` | Gold 06 | WLMDS ratio, estimated patients and surplus pathways for 17 months; bounds on people with 2+ pathways; ratio sensitivity; people-vs-pathway decomposition; WLMDS vs monthly RTT coherence |
| `07_gold_cancer` | Gold 07 | 62-day and FDS vs the 85% / 80% standards in points and people; year on year like for like (provisional) and vs final; breach depth; provider spread with Wilson intervals |
| `08_findings` | Gold 08 | every BMA / Healthcare Management / brief claim beside the rebuilt figure, its basis, a verdict and the source files |
| `09_charts` | Gold 09 | the article's chart (March 2026 = 100, list vs over 18 vs over 52, target deadline marked), the three-row table as an image, and alt text generated from the same numbers |

## The measure

The primary measure is the same one as in Two Maps: **reported-provider** incomplete
pathways, `NONC` commissioner rows excluded. The July 2026 figure reproduces Two Maps'
7,131,685 / 108,263 exactly. NHS England's **headline** adds estimates for
trusts that did not submit (carry-forward of the last submitted position). The gate
rebuilds that too, and every figure in `claims_vs_primary.csv` is labelled with its basis.

**Decision for the August 2026 article (17 Oct 2026):** national England figures are quoted on
NHS England's **headline** basis (7,370,100 pathways; 113,339 over 52 weeks). Two Maps used the
reported basis because it joined provider-level data, where estimates for missing trusts can't be
allocated. The finding the article rests on, that the over-52 tail has grown faster than the list
since March 2026, holds on all three bases (`data/gold/05_divergence/divergence_summary.csv`):
headline +20.1% vs +3.7%, constant panel +20.9% vs +3.7%, reported +18.7% vs +2.0%.

## Sources

NHS England RTT full CSV extracts and published workbooks (RTT 2025-26 and 2026-27 pages),
the August 2026 RTT statistical press notice, and Cancer Waiting Times Combined CSVs,
statistical release and national time series. URLs and hashes are in `src/sources.py` and
each `data/bronze/*/metadata.json`. Crown copyright, Open Government Licence v3.

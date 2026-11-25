# Credit Early-Warning Monitor - Portfolio Summary

- Generated: 24-Nov-2026 16:08
- Panel: `data/real_panel.csv`
- Config applied: `config/thresholds_real_panel.yaml`
- Borrowers: 12 | Latest fiscal year in panel: FY2026
- Bands: 1 red, 3 amber, 8 green

Scoring: each red level signal counts 3, each amber level signal 1, each deterioration flag 0.5. Red band at score >= 12, amber at score >= 4.

## 1. Ranking (worst first)

| Rank | Borrower | Sector | Score | Band | Red | Amber | Deterioration | Top tripped signals |
| ---: | --- | --- | ---: | --- | ---: | ---: | ---: | --- |
| 1 | Piramal Pharma Ltd | Pharma | 12.0 | RED | 3 | 2 | 4 | Gross debt / EBITDA (cash not in source); PAT / net worth; Revenue growth (YoY) |
| 2 | Welspun Living Ltd | Textiles | 10.0 | AMBER | 3 | 0 | 4 | EBITDA margin; PAT / net worth; Revenue growth (YoY) |
| 3 | Gujarat Fluorochemicals Ltd | Chemicals | 5.0 | AMBER | 1 | 2 | 0 | Receivable days; PAT / net worth; Revenue growth (YoY) |
| 4 | Vardhman Textiles Ltd | Textiles | 5.0 | AMBER | 0 | 3 | 4 | EBITDA margin; PAT / net worth; Revenue growth (YoY) |
| 5 | Glenmark Pharmaceuticals Ltd | Pharma | 3.0 | GREEN | 1 | 0 | 1 | Receivable days; Receivable days |
| 6 | Nuvoco Vistas Corporation Ltd | Cement | 3.0 | GREEN | 1 | 0 | 0 | PAT / net worth |
| 7 | Granules India Ltd | Pharma | 2.0 | GREEN | 0 | 1 | 2 | Receivable days; CFO / total debt; Cash interest cover (CFO / interest) |
| 8 | Arvind Ltd | Textiles | 1.0 | GREEN | 0 | 1 | 0 | EBITDA margin |
| 9 | JK Lakshmi Cement Ltd | Cement | 1.0 | GREEN | 0 | 1 | 0 | EBITDA margin |
| 10 | Navin Fluorine International Ltd | Chemicals | 1.0 | GREEN | 0 | 1 | 0 | Receivable days |
| 11 | SRF Ltd | Chemicals | 1.0 | GREEN | 0 | 1 | 0 | Revenue growth (YoY) |
| 12 | Star Cement Ltd | Cement | 0.0 | GREEN | 0 | 0 | 0 | none |

## 2. Top signals by frequency (FY2026)

| # | Signal | Times tripped |
| ---: | --- | ---: |
| 1 | EBITDA margin | 7 |
| 2 | PAT / net worth | 7 |
| 3 | Receivable days | 6 |

Across the whole panel history (all years), the most frequent signals are: PAT / net worth (15), EBITDA margin (12), Receivable days (11).

## 3. Borrower detail

### 1. Piramal Pharma Ltd - RED (score 12.0)

- Sector: Pharma; latest year FY2026
- Level signals: Gross debt / EBITDA (cash not in source) at 6.16x is in the red band (green needs 3.00x); EBITDA margin at 10.4% is in the amber band (green needs 15.0%); Revenue growth (YoY) at -3.1% is in the red band (green needs 8.0%); Receivable days at 89d is in the amber band (green needs 60d); PAT / net worth at -4.0% is in the red band (green needs 10.0%)
- Deterioration (year on year): Gross debt / EBITDA (cash not in source) rose 2.79x year on year (trigger 0.50x) - level already red, no additional weight; Interest coverage (EBITDA / interest) fell 0.72x year on year (trigger 0.50x) but still inside the green band; EBITDA margin fell 5.4pp year on year (trigger 2.0pp) but still inside the amber band; PAT / net worth fell 5.1pp year on year (trigger 3.0pp) - level already red, no additional weight

| Ratio | FY2025 | FY2026 | Band |
| --- | ---: | ---: | --- |
| Gross debt / EBITDA (cash not in source) | 3.36 | 6.16 | RED |
| Interest coverage (EBITDA / interest) | 3.42 | 2.70 | GREEN |
| Cash interest cover (CFO / interest) | 2.11 | 4.85 | GREEN |
| DSCR (CFO / (interest + scheduled principal)) | n/a | n/a | n/a |
| Current ratio | n/a | n/a | n/a |
| Quick ratio | n/a | n/a | n/a |
| Debt / net worth (contingents not in source) | 0.60 | 0.70 | GREEN |
| CFO / total debt | 0.18 | 0.29 | GREEN |
| EBITDA margin | 15.8% | 10.4% | AMBER |
| Revenue growth (YoY) | n/a | -3.1% | RED |
| Receivable days | 94 | 89 | AMBER |
| Inventory days (COGS basis when supplied) | n/a | n/a | n/a |
| PAT / net worth | 1.1% | -4.0% | RED |

### 2. Welspun Living Ltd - AMBER (score 10.0)

- Sector: Textiles; latest year FY2026
- Level signals: EBITDA margin at 8.4% is in the red band (green needs 15.0%); Revenue growth (YoY) at -10.9% is in the red band (green needs 8.0%); PAT / net worth at 4.3% is in the red band (green needs 10.0%)
- Deterioration (year on year): Gross debt / EBITDA (cash not in source) rose 0.79x year on year (trigger 0.50x) but still inside the green band; Interest coverage (EBITDA / interest) fell 1.05x year on year (trigger 0.50x) but still inside the green band; EBITDA margin fell 3.9pp year on year (trigger 2.0pp) - level already red, no additional weight; PAT / net worth fell 9.0pp year on year (trigger 3.0pp) - level already red, no additional weight

| Ratio | FY2025 | FY2026 | Band |
| --- | ---: | ---: | --- |
| Gross debt / EBITDA (cash not in source) | 2.13 | 2.92 | GREEN |
| Interest coverage (EBITDA / interest) | 5.99 | 4.93 | GREEN |
| Cash interest cover (CFO / interest) | 3.17 | 7.30 | GREEN |
| DSCR (CFO / (interest + scheduled principal)) | n/a | n/a | n/a |
| Current ratio | n/a | n/a | n/a |
| Quick ratio | n/a | n/a | n/a |
| Debt / net worth (contingents not in source) | 0.57 | 0.47 | GREEN |
| CFO / total debt | 0.25 | 0.51 | GREEN |
| EBITDA margin | 12.3% | 8.4% | RED |
| Revenue growth (YoY) | n/a | -10.9% | RED |
| Receivable days | 57 | 51 | GREEN |
| Inventory days (COGS basis when supplied) | n/a | n/a | n/a |
| PAT / net worth | 13.4% | 4.3% | RED |

### 3. Gujarat Fluorochemicals Ltd - AMBER (score 5.0)

- Sector: Chemicals; latest year FY2026
- Level signals: Revenue growth (YoY) at 5.5% is in the amber band (green needs 8.0%); Receivable days at 94d is in the red band (green needs 60d); PAT / net worth at 7.3% is in the amber band (green needs 10.0%)

| Ratio | FY2025 | FY2026 | Band |
| --- | ---: | ---: | --- |
| Gross debt / EBITDA (cash not in source) | 1.89 | 2.27 | GREEN |
| Interest coverage (EBITDA / interest) | 7.48 | 8.70 | GREEN |
| Cash interest cover (CFO / interest) | 3.71 | 6.96 | GREEN |
| DSCR (CFO / (interest + scheduled principal)) | n/a | n/a | n/a |
| Current ratio | n/a | n/a | n/a |
| Quick ratio | n/a | n/a | n/a |
| Debt / net worth (contingents not in source) | 0.29 | 0.35 | GREEN |
| CFO / total debt | 0.26 | 0.35 | GREEN |
| EBITDA margin | 23.2% | 24.0% | GREEN |
| Revenue growth (YoY) | n/a | 5.5% | AMBER |
| Receivable days | 92 | 94 | RED |
| Inventory days (COGS basis when supplied) | n/a | n/a | n/a |
| PAT / net worth | 7.5% | 7.3% | AMBER |

### 4. Vardhman Textiles Ltd - AMBER (score 5.0)

- Sector: Textiles; latest year FY2026
- Level signals: EBITDA margin at 12.6% is in the amber band (green needs 15.0%); Revenue growth (YoY) at 0.9% is in the amber band (green needs 8.0%); PAT / net worth at 7.2% is in the amber band (green needs 10.0%)
- Deterioration (year on year): Gross debt / EBITDA (cash not in source) rose 0.52x year on year (trigger 0.50x) but still inside the green band; Interest coverage (EBITDA / interest) fell 2.94x year on year (trigger 0.50x) but still inside the green band; Cash interest cover (CFO / interest) fell 9.31x year on year (trigger 0.25x) but still inside the green band; CFO / total debt fell 0.73x year on year (trigger 0.05x) but still inside the green band

| Ratio | FY2025 | FY2026 | Band |
| --- | ---: | ---: | --- |
| Gross debt / EBITDA (cash not in source) | 0.98 | 1.50 | GREEN |
| Interest coverage (EBITDA / interest) | 16.40 | 13.47 | GREEN |
| Cash interest cover (CFO / interest) | 21.35 | 12.04 | GREEN |
| DSCR (CFO / (interest + scheduled principal)) | n/a | n/a | n/a |
| Current ratio | n/a | n/a | n/a |
| Quick ratio | n/a | n/a | n/a |
| Debt / net worth (contingents not in source) | 0.13 | 0.18 | GREEN |
| CFO / total debt | 1.33 | 0.60 | GREEN |
| EBITDA margin | 12.9% | 12.6% | AMBER |
| Revenue growth (YoY) | n/a | 0.9% | AMBER |
| Receivable days | 48 | 48 | GREEN |
| Inventory days (COGS basis when supplied) | n/a | n/a | n/a |
| PAT / net worth | 9.0% | 7.2% | AMBER |

### 5. Glenmark Pharmaceuticals Ltd - GREEN (score 3.0)

- Sector: Pharma; latest year FY2026
- Level signals: Receivable days at 107d is in the red band (green needs 60d)
- Deterioration (year on year): Receivable days rose 15 days year on year (trigger 10 days) - level already red, no additional weight

| Ratio | FY2025 | FY2026 | Band |
| --- | ---: | ---: | --- |
| Gross debt / EBITDA (cash not in source) | 1.05 | 0.13 | GREEN |
| Interest coverage (EBITDA / interest) | 11.36 | 21.88 | GREEN |
| Cash interest cover (CFO / interest) | -4.00 | 16.48 | GREEN |
| DSCR (CFO / (interest + scheduled principal)) | n/a | n/a | n/a |
| Current ratio | n/a | n/a | n/a |
| Quick ratio | n/a | n/a | n/a |
| Debt / net worth (contingents not in source) | 0.28 | 0.06 | GREEN |
| CFO / total debt | -0.33 | 5.80 | GREEN |
| EBITDA margin | 17.6% | 26.9% | GREEN |
| Revenue growth (YoY) | n/a | 27.5% | GREEN |
| Receivable days | 92 | 107 | RED |
| Inventory days (COGS basis when supplied) | n/a | n/a | n/a |
| PAT / net worth | 11.8% | 13.0% | GREEN |

### 6. Nuvoco Vistas Corporation Ltd - GREEN (score 3.0)

- Sector: Cement; latest year FY2026
- Level signals: PAT / net worth at 3.9% is in the red band (green needs 10.0%)

| Ratio | FY2025 | FY2026 | Band |
| --- | ---: | ---: | --- |
| Gross debt / EBITDA (cash not in source) | 2.97 | 2.65 | GREEN |
| Interest coverage (EBITDA / interest) | 2.77 | 4.67 | GREEN |
| Cash interest cover (CFO / interest) | 2.68 | 3.73 | GREEN |
| DSCR (CFO / (interest + scheduled principal)) | n/a | n/a | n/a |
| Current ratio | n/a | n/a | n/a |
| Quick ratio | n/a | n/a | n/a |
| Debt / net worth (contingents not in source) | 0.45 | 0.53 | GREEN |
| CFO / total debt | 0.33 | 0.30 | GREEN |
| EBITDA margin | 13.3% | 16.4% | GREEN |
| Revenue growth (YoY) | n/a | 9.5% | GREEN |
| Receivable days | 23 | 24 | GREEN |
| Inventory days (COGS basis when supplied) | n/a | n/a | n/a |
| PAT / net worth | 0.2% | 3.9% | RED |

### 7. Granules India Ltd - GREEN (score 2.0)

- Sector: Pharma; latest year FY2026
- Level signals: Receivable days at 62d is in the amber band (green needs 60d)
- Deterioration (year on year): Cash interest cover (CFO / interest) fell 1.46x year on year (trigger 0.25x) but still inside the green band; CFO / total debt fell 0.07x year on year (trigger 0.05x) but still inside the green band

| Ratio | FY2025 | FY2026 | Band |
| --- | ---: | ---: | --- |
| Gross debt / EBITDA (cash not in source) | 1.53 | 1.27 | GREEN |
| Interest coverage (EBITDA / interest) | 9.20 | 10.42 | GREEN |
| Cash interest cover (CFO / interest) | 8.42 | 6.96 | GREEN |
| DSCR (CFO / (interest + scheduled principal)) | n/a | n/a | n/a |
| Current ratio | n/a | n/a | n/a |
| Quick ratio | n/a | n/a | n/a |
| Debt / net worth (contingents not in source) | 0.39 | 0.30 | GREEN |
| CFO / total debt | 0.60 | 0.52 | GREEN |
| EBITDA margin | 21.2% | 22.1% | GREEN |
| Revenue growth (YoY) | n/a | 19.7% | GREEN |
| Receivable days | 77 | 62 | AMBER |
| Inventory days (COGS basis when supplied) | n/a | n/a | n/a |
| PAT / net worth | 13.5% | 11.7% | GREEN |

### 8. Arvind Ltd - GREEN (score 1.0)

- Sector: Textiles; latest year FY2026
- Level signals: EBITDA margin at 11.4% is in the amber band (green needs 15.0%)

| Ratio | FY2025 | FY2026 | Band |
| --- | ---: | ---: | --- |
| Gross debt / EBITDA (cash not in source) | 1.75 | 1.56 | GREEN |
| Interest coverage (EBITDA / interest) | 4.30 | 4.83 | GREEN |
| Cash interest cover (CFO / interest) | 3.67 | 3.94 | GREEN |
| DSCR (CFO / (interest + scheduled principal)) | n/a | n/a | n/a |
| Current ratio | n/a | n/a | n/a |
| Quick ratio | n/a | n/a | n/a |
| Debt / net worth (contingents not in source) | 0.41 | 0.41 | GREEN |
| CFO / total debt | 0.49 | 0.52 | GREEN |
| EBITDA margin | 10.7% | 11.4% | AMBER |
| Revenue growth (YoY) | n/a | 11.7% | GREEN |
| Receivable days | 52 | 57 | GREEN |
| Inventory days (COGS basis when supplied) | n/a | n/a | n/a |
| PAT / net worth | 9.7% | 10.6% | GREEN |

### 9. JK Lakshmi Cement Ltd - GREEN (score 1.0)

- Sector: Cement; latest year FY2026
- Level signals: EBITDA margin at 14.8% is in the amber band (green needs 15.0%)

| Ratio | FY2025 | FY2026 | Band |
| --- | ---: | ---: | --- |
| Gross debt / EBITDA (cash not in source) | 3.03 | 2.59 | GREEN |
| Interest coverage (EBITDA / interest) | 4.77 | 4.74 | GREEN |
| Cash interest cover (CFO / interest) | 4.33 | 5.13 | GREEN |
| DSCR (CFO / (interest + scheduled principal)) | n/a | n/a | n/a |
| Current ratio | n/a | n/a | n/a |
| Quick ratio | n/a | n/a | n/a |
| Debt / net worth (contingents not in source) | 0.74 | 0.67 | GREEN |
| CFO / total debt | 0.30 | 0.42 | GREEN |
| EBITDA margin | 14.0% | 14.8% | AMBER |
| Revenue growth (YoY) | n/a | 9.2% | GREEN |
| Receivable days | 6 | 6 | GREEN |
| Inventory days (COGS basis when supplied) | n/a | n/a | n/a |
| PAT / net worth | 7.8% | 10.6% | GREEN |

### 10. Navin Fluorine International Ltd - GREEN (score 1.0)

- Sector: Chemicals; latest year FY2026
- Level signals: Receivable days at 83d is in the amber band (green needs 60d)

| Ratio | FY2025 | FY2026 | Band |
| --- | ---: | ---: | --- |
| Gross debt / EBITDA (cash not in source) | 2.75 | 1.18 | GREEN |
| Interest coverage (EBITDA / interest) | 6.85 | 9.17 | GREEN |
| Cash interest cover (CFO / interest) | 7.32 | 7.58 | GREEN |
| DSCR (CFO / (interest + scheduled principal)) | n/a | n/a | n/a |
| Current ratio | n/a | n/a | n/a |
| Quick ratio | n/a | n/a | n/a |
| Debt / net worth (contingents not in source) | 0.56 | 0.32 | GREEN |
| CFO / total debt | 0.39 | 0.70 | GREEN |
| EBITDA margin | 22.7% | 32.6% | GREEN |
| Revenue growth (YoY) | n/a | 41.1% | GREEN |
| Receivable days | 90 | 83 | AMBER |
| Inventory days (COGS basis when supplied) | n/a | n/a | n/a |
| PAT / net worth | 11.0% | 16.7% | GREEN |

### 11. SRF Ltd - GREEN (score 1.0)

- Sector: Chemicals; latest year FY2026
- Level signals: Revenue growth (YoY) at 7.4% is in the amber band (green needs 8.0%)

| Ratio | FY2025 | FY2026 | Band |
| --- | ---: | ---: | --- |
| Gross debt / EBITDA (cash not in source) | 1.74 | 1.49 | GREEN |
| Interest coverage (EBITDA / interest) | 7.23 | 12.27 | GREEN |
| Cash interest cover (CFO / interest) | 6.61 | 9.19 | GREEN |
| DSCR (CFO / (interest + scheduled principal)) | n/a | n/a | n/a |
| Current ratio | n/a | n/a | n/a |
| Quick ratio | n/a | n/a | n/a |
| Debt / net worth (contingents not in source) | 0.37 | 0.36 | GREEN |
| CFO / total debt | 0.53 | 0.50 | GREEN |
| EBITDA margin | 18.5% | 21.6% | GREEN |
| Revenue growth (YoY) | n/a | 7.4% | AMBER |
| Receivable days | 54 | 59 | GREEN |
| Inventory days (COGS basis when supplied) | n/a | n/a | n/a |
| PAT / net worth | 9.9% | 13.1% | GREEN |

### 12. Star Cement Ltd - GREEN (score 0.0)

- Sector: Cement; latest year FY2026
- Level signals: none - every ratio is inside the green band

| Ratio | FY2025 | FY2026 | Band |
| --- | ---: | ---: | --- |
| Gross debt / EBITDA (cash not in source) | 0.70 | 0.64 | GREEN |
| Interest coverage (EBITDA / interest) | 18.09 | 20.35 | GREEN |
| Cash interest cover (CFO / interest) | 9.25 | 16.63 | GREEN |
| DSCR (CFO / (interest + scheduled principal)) | n/a | n/a | n/a |
| Current ratio | n/a | n/a | n/a |
| Quick ratio | n/a | n/a | n/a |
| Debt / net worth (contingents not in source) | 0.14 | 0.19 | GREEN |
| CFO / total debt | 0.73 | 1.27 | GREEN |
| EBITDA margin | 18.3% | 24.8% | GREEN |
| Revenue growth (YoY) | n/a | 19.4% | GREEN |
| Receivable days | 23 | 23 | GREEN |
| Inventory days (COGS basis when supplied) | n/a | n/a | n/a |
| PAT / net worth | 5.9% | 12.2% | GREEN |

## 4. Sector-relative view: where absolute bands and peers disagree

Each borrower's latest ratios against the median of its own sector in this panel (minimum three peers). *Hidden relative weakness*: green on absolute thresholds but the weakest in the sector by at least the deterioration trigger. *Sector-wide level*: amber or red on absolute thresholds but at or better than the sector median.

| Borrower | Sector | Ratio | Value | Absolute band | Sector median | Rank | View |
| --- | --- | --- | ---: | --- | ---: | --- | --- |
| Nuvoco Vistas Corporation Ltd | Cement | CFO / total debt | 0.30 | green | 0.42 | 3 of 3 | hidden relative weakness |
| Nuvoco Vistas Corporation Ltd | Cement | Cash interest cover (CFO / interest) | 3.73 | green | 5.13 | 3 of 3 | hidden relative weakness |
| Gujarat Fluorochemicals Ltd | Chemicals | CFO / total debt | 0.35 | green | 0.50 | 3 of 3 | hidden relative weakness |
| Gujarat Fluorochemicals Ltd | Chemicals | Cash interest cover (CFO / interest) | 6.96 | green | 7.58 | 3 of 3 | hidden relative weakness |
| SRF Ltd | Chemicals | EBITDA margin | 21.6% | green | 24.0% | 3 of 3 | hidden relative weakness |
| Gujarat Fluorochemicals Ltd | Chemicals | Gross debt / EBITDA (cash not in source) | 2.27 | green | 1.49 | 3 of 3 | hidden relative weakness |
| Navin Fluorine International Ltd | Chemicals | Receivable days | 83 | amber | 83 | 2 of 3 | sector-wide level |
| SRF Ltd | Chemicals | Revenue growth (YoY) | 7.4% | amber | 7.4% | 2 of 3 | sector-wide level |
| Piramal Pharma Ltd | Pharma | CFO / total debt | 0.29 | green | 0.52 | 3 of 3 | hidden relative weakness |
| Piramal Pharma Ltd | Pharma | Cash interest cover (CFO / interest) | 4.85 | green | 6.96 | 3 of 3 | hidden relative weakness |
| Piramal Pharma Ltd | Pharma | Interest coverage (EBITDA / interest) | 2.70 | green | 10.42 | 3 of 3 | hidden relative weakness |
| Granules India Ltd | Pharma | Receivable days | 62 | amber | 89 | 1 of 3 | sector-wide level |
| Piramal Pharma Ltd | Pharma | Receivable days | 89 | amber | 89 | 2 of 3 | sector-wide level |
| Piramal Pharma Ltd | Pharma | Debt / net worth (contingents not in source) | 0.70 | green | 0.30 | 3 of 3 | hidden relative weakness |
| Arvind Ltd | Textiles | Cash interest cover (CFO / interest) | 3.94 | green | 7.30 | 3 of 3 | hidden relative weakness |
| Arvind Ltd | Textiles | EBITDA margin | 11.4% | amber | 11.4% | 2 of 3 | sector-wide level |
| Vardhman Textiles Ltd | Textiles | EBITDA margin | 12.6% | amber | 11.4% | 1 of 3 | sector-wide level |
| Welspun Living Ltd | Textiles | Gross debt / EBITDA (cash not in source) | 2.92 | green | 1.56 | 3 of 3 | hidden relative weakness |
| Vardhman Textiles Ltd | Textiles | PAT / net worth | 7.2% | amber | 7.2% | 2 of 3 | sector-wide level |
| Vardhman Textiles Ltd | Textiles | Revenue growth (YoY) | 0.9% | amber | 0.9% | 2 of 3 | sector-wide level |

## 5. How to read this report

A level signal means the ratio is outside its green band in the latest year. A deterioration signal means the ratio moved against the borrower by more than the configured trigger in one year, even if the level is still inside a green or amber band - this is the early part of the early-warning system.

Ratios shown as n/a are undefined (zero denominator) or not meaningful (negative EBITDA or non-positive net worth). Those cases raise an explicit data flag instead of an infinity.

See README.md for formulas, threshold defaults and limitations. This report is an analytical screen, not a credit decision.

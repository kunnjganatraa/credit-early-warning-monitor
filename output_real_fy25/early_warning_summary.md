# Credit Early-Warning Monitor - Portfolio Summary

- Generated: 24-Nov-2026 16:08
- Panel: `data/real_panel_fy25.csv`
- Config applied: `config/thresholds_real_panel.yaml`
- Borrowers: 12 | Latest fiscal year in panel: FY2025
- Bands: 0 red, 4 amber, 8 green

Scoring: each red level signal counts 3, each amber level signal 1, each deterioration flag 0.5. Red band at score >= 12, amber at score >= 4.

## 1. Ranking (worst first)

| Rank | Borrower | Sector | Score | Band | Red | Amber | Deterioration | Top tripped signals |
| ---: | --- | --- | ---: | --- | ---: | ---: | ---: | --- |
| 1 | Glenmark Pharmaceuticals Ltd | Pharma | 9.0 | AMBER | 3 | 0 | 0 | CFO / total debt; Cash interest cover (CFO / interest); Receivable days |
| 2 | Piramal Pharma Ltd | Pharma | 8.0 | AMBER | 2 | 2 | 0 | PAT / net worth; Receivable days; CFO / total debt |
| 3 | Gujarat Fluorochemicals Ltd | Chemicals | 4.0 | AMBER | 1 | 1 | 0 | Receivable days; PAT / net worth |
| 4 | Nuvoco Vistas Corporation Ltd | Cement | 4.0 | AMBER | 1 | 1 | 0 | PAT / net worth; EBITDA margin |
| 5 | JK Lakshmi Cement Ltd | Cement | 3.0 | GREEN | 0 | 3 | 0 | EBITDA margin; Gross debt / EBITDA (cash not in source); PAT / net worth |
| 6 | Arvind Ltd | Textiles | 2.0 | GREEN | 0 | 2 | 0 | EBITDA margin; PAT / net worth |
| 7 | Vardhman Textiles Ltd | Textiles | 2.0 | GREEN | 0 | 2 | 0 | EBITDA margin; PAT / net worth |
| 8 | Granules India Ltd | Pharma | 1.0 | GREEN | 0 | 1 | 0 | Receivable days |
| 9 | Navin Fluorine International Ltd | Chemicals | 1.0 | GREEN | 0 | 1 | 0 | Receivable days |
| 10 | SRF Ltd | Chemicals | 1.0 | GREEN | 0 | 1 | 0 | PAT / net worth |
| 11 | Star Cement Ltd | Cement | 1.0 | GREEN | 0 | 1 | 0 | PAT / net worth |
| 12 | Welspun Living Ltd | Textiles | 1.0 | GREEN | 0 | 1 | 0 | EBITDA margin |

## 2. Top signals by frequency (FY2025)

| # | Signal | Times tripped |
| ---: | --- | ---: |
| 1 | PAT / net worth | 8 |
| 2 | EBITDA margin | 5 |
| 3 | Receivable days | 5 |

Across the whole panel history (all years), the most frequent signals are: PAT / net worth (8), EBITDA margin (5), Receivable days (5).

## 3. Borrower detail

### 1. Glenmark Pharmaceuticals Ltd - AMBER (score 9.0)

- Sector: Pharma; latest year FY2025
- Level signals: Cash interest cover (CFO / interest) at -4.00x is in the red band (green needs 1.50x); CFO / total debt at -0.33x is in the red band (green needs 0.20x); Receivable days at 92d is in the red band (green needs 60d)

| Ratio | FY2025 | Band |
| --- | ---: | --- |
| Gross debt / EBITDA (cash not in source) | 1.05 | GREEN |
| Interest coverage (EBITDA / interest) | 11.36 | GREEN |
| Cash interest cover (CFO / interest) | -4.00 | RED |
| DSCR (CFO / (interest + scheduled principal)) | n/a | n/a |
| Current ratio | n/a | n/a |
| Quick ratio | n/a | n/a |
| Debt / net worth (contingents not in source) | 0.28 | GREEN |
| CFO / total debt | -0.33 | RED |
| EBITDA margin | 17.6% | GREEN |
| Revenue growth (YoY) | n/a | n/a |
| Receivable days | 92 | RED |
| Inventory days (COGS basis when supplied) | n/a | n/a |
| PAT / net worth | 11.8% | GREEN |

### 2. Piramal Pharma Ltd - AMBER (score 8.0)

- Sector: Pharma; latest year FY2025
- Level signals: Gross debt / EBITDA (cash not in source) at 3.36x is in the amber band (green needs 3.00x); CFO / total debt at 0.18x is in the amber band (green needs 0.20x); Receivable days at 94d is in the red band (green needs 60d); PAT / net worth at 1.1% is in the red band (green needs 10.0%)

| Ratio | FY2025 | Band |
| --- | ---: | --- |
| Gross debt / EBITDA (cash not in source) | 3.36 | AMBER |
| Interest coverage (EBITDA / interest) | 3.42 | GREEN |
| Cash interest cover (CFO / interest) | 2.11 | GREEN |
| DSCR (CFO / (interest + scheduled principal)) | n/a | n/a |
| Current ratio | n/a | n/a |
| Quick ratio | n/a | n/a |
| Debt / net worth (contingents not in source) | 0.60 | GREEN |
| CFO / total debt | 0.18 | AMBER |
| EBITDA margin | 15.8% | GREEN |
| Revenue growth (YoY) | n/a | n/a |
| Receivable days | 94 | RED |
| Inventory days (COGS basis when supplied) | n/a | n/a |
| PAT / net worth | 1.1% | RED |

### 3. Gujarat Fluorochemicals Ltd - AMBER (score 4.0)

- Sector: Chemicals; latest year FY2025
- Level signals: Receivable days at 92d is in the red band (green needs 60d); PAT / net worth at 7.5% is in the amber band (green needs 10.0%)

| Ratio | FY2025 | Band |
| --- | ---: | --- |
| Gross debt / EBITDA (cash not in source) | 1.89 | GREEN |
| Interest coverage (EBITDA / interest) | 7.48 | GREEN |
| Cash interest cover (CFO / interest) | 3.71 | GREEN |
| DSCR (CFO / (interest + scheduled principal)) | n/a | n/a |
| Current ratio | n/a | n/a |
| Quick ratio | n/a | n/a |
| Debt / net worth (contingents not in source) | 0.29 | GREEN |
| CFO / total debt | 0.26 | GREEN |
| EBITDA margin | 23.2% | GREEN |
| Revenue growth (YoY) | n/a | n/a |
| Receivable days | 92 | RED |
| Inventory days (COGS basis when supplied) | n/a | n/a |
| PAT / net worth | 7.5% | AMBER |

### 4. Nuvoco Vistas Corporation Ltd - AMBER (score 4.0)

- Sector: Cement; latest year FY2025
- Level signals: EBITDA margin at 13.3% is in the amber band (green needs 15.0%); PAT / net worth at 0.2% is in the red band (green needs 10.0%)

| Ratio | FY2025 | Band |
| --- | ---: | --- |
| Gross debt / EBITDA (cash not in source) | 2.97 | GREEN |
| Interest coverage (EBITDA / interest) | 2.77 | GREEN |
| Cash interest cover (CFO / interest) | 2.68 | GREEN |
| DSCR (CFO / (interest + scheduled principal)) | n/a | n/a |
| Current ratio | n/a | n/a |
| Quick ratio | n/a | n/a |
| Debt / net worth (contingents not in source) | 0.45 | GREEN |
| CFO / total debt | 0.33 | GREEN |
| EBITDA margin | 13.3% | AMBER |
| Revenue growth (YoY) | n/a | n/a |
| Receivable days | 23 | GREEN |
| Inventory days (COGS basis when supplied) | n/a | n/a |
| PAT / net worth | 0.2% | RED |

### 5. JK Lakshmi Cement Ltd - GREEN (score 3.0)

- Sector: Cement; latest year FY2025
- Level signals: Gross debt / EBITDA (cash not in source) at 3.03x is in the amber band (green needs 3.00x); EBITDA margin at 14.0% is in the amber band (green needs 15.0%); PAT / net worth at 7.8% is in the amber band (green needs 10.0%)

| Ratio | FY2025 | Band |
| --- | ---: | --- |
| Gross debt / EBITDA (cash not in source) | 3.03 | AMBER |
| Interest coverage (EBITDA / interest) | 4.77 | GREEN |
| Cash interest cover (CFO / interest) | 4.33 | GREEN |
| DSCR (CFO / (interest + scheduled principal)) | n/a | n/a |
| Current ratio | n/a | n/a |
| Quick ratio | n/a | n/a |
| Debt / net worth (contingents not in source) | 0.74 | GREEN |
| CFO / total debt | 0.30 | GREEN |
| EBITDA margin | 14.0% | AMBER |
| Revenue growth (YoY) | n/a | n/a |
| Receivable days | 6 | GREEN |
| Inventory days (COGS basis when supplied) | n/a | n/a |
| PAT / net worth | 7.8% | AMBER |

### 6. Arvind Ltd - GREEN (score 2.0)

- Sector: Textiles; latest year FY2025
- Level signals: EBITDA margin at 10.7% is in the amber band (green needs 15.0%); PAT / net worth at 9.7% is in the amber band (green needs 10.0%)

| Ratio | FY2025 | Band |
| --- | ---: | --- |
| Gross debt / EBITDA (cash not in source) | 1.75 | GREEN |
| Interest coverage (EBITDA / interest) | 4.30 | GREEN |
| Cash interest cover (CFO / interest) | 3.67 | GREEN |
| DSCR (CFO / (interest + scheduled principal)) | n/a | n/a |
| Current ratio | n/a | n/a |
| Quick ratio | n/a | n/a |
| Debt / net worth (contingents not in source) | 0.41 | GREEN |
| CFO / total debt | 0.49 | GREEN |
| EBITDA margin | 10.7% | AMBER |
| Revenue growth (YoY) | n/a | n/a |
| Receivable days | 52 | GREEN |
| Inventory days (COGS basis when supplied) | n/a | n/a |
| PAT / net worth | 9.7% | AMBER |

### 7. Vardhman Textiles Ltd - GREEN (score 2.0)

- Sector: Textiles; latest year FY2025
- Level signals: EBITDA margin at 12.9% is in the amber band (green needs 15.0%); PAT / net worth at 9.0% is in the amber band (green needs 10.0%)

| Ratio | FY2025 | Band |
| --- | ---: | --- |
| Gross debt / EBITDA (cash not in source) | 0.98 | GREEN |
| Interest coverage (EBITDA / interest) | 16.40 | GREEN |
| Cash interest cover (CFO / interest) | 21.35 | GREEN |
| DSCR (CFO / (interest + scheduled principal)) | n/a | n/a |
| Current ratio | n/a | n/a |
| Quick ratio | n/a | n/a |
| Debt / net worth (contingents not in source) | 0.13 | GREEN |
| CFO / total debt | 1.33 | GREEN |
| EBITDA margin | 12.9% | AMBER |
| Revenue growth (YoY) | n/a | n/a |
| Receivable days | 48 | GREEN |
| Inventory days (COGS basis when supplied) | n/a | n/a |
| PAT / net worth | 9.0% | AMBER |

### 8. Granules India Ltd - GREEN (score 1.0)

- Sector: Pharma; latest year FY2025
- Level signals: Receivable days at 77d is in the amber band (green needs 60d)

| Ratio | FY2025 | Band |
| --- | ---: | --- |
| Gross debt / EBITDA (cash not in source) | 1.53 | GREEN |
| Interest coverage (EBITDA / interest) | 9.20 | GREEN |
| Cash interest cover (CFO / interest) | 8.42 | GREEN |
| DSCR (CFO / (interest + scheduled principal)) | n/a | n/a |
| Current ratio | n/a | n/a |
| Quick ratio | n/a | n/a |
| Debt / net worth (contingents not in source) | 0.39 | GREEN |
| CFO / total debt | 0.60 | GREEN |
| EBITDA margin | 21.2% | GREEN |
| Revenue growth (YoY) | n/a | n/a |
| Receivable days | 77 | AMBER |
| Inventory days (COGS basis when supplied) | n/a | n/a |
| PAT / net worth | 13.5% | GREEN |

### 9. Navin Fluorine International Ltd - GREEN (score 1.0)

- Sector: Chemicals; latest year FY2025
- Level signals: Receivable days at 90d is in the amber band (green needs 60d)

| Ratio | FY2025 | Band |
| --- | ---: | --- |
| Gross debt / EBITDA (cash not in source) | 2.75 | GREEN |
| Interest coverage (EBITDA / interest) | 6.85 | GREEN |
| Cash interest cover (CFO / interest) | 7.32 | GREEN |
| DSCR (CFO / (interest + scheduled principal)) | n/a | n/a |
| Current ratio | n/a | n/a |
| Quick ratio | n/a | n/a |
| Debt / net worth (contingents not in source) | 0.56 | GREEN |
| CFO / total debt | 0.39 | GREEN |
| EBITDA margin | 22.7% | GREEN |
| Revenue growth (YoY) | n/a | n/a |
| Receivable days | 90 | AMBER |
| Inventory days (COGS basis when supplied) | n/a | n/a |
| PAT / net worth | 11.0% | GREEN |

### 10. SRF Ltd - GREEN (score 1.0)

- Sector: Chemicals; latest year FY2025
- Level signals: PAT / net worth at 9.9% is in the amber band (green needs 10.0%)

| Ratio | FY2025 | Band |
| --- | ---: | --- |
| Gross debt / EBITDA (cash not in source) | 1.74 | GREEN |
| Interest coverage (EBITDA / interest) | 7.23 | GREEN |
| Cash interest cover (CFO / interest) | 6.61 | GREEN |
| DSCR (CFO / (interest + scheduled principal)) | n/a | n/a |
| Current ratio | n/a | n/a |
| Quick ratio | n/a | n/a |
| Debt / net worth (contingents not in source) | 0.37 | GREEN |
| CFO / total debt | 0.53 | GREEN |
| EBITDA margin | 18.5% | GREEN |
| Revenue growth (YoY) | n/a | n/a |
| Receivable days | 54 | GREEN |
| Inventory days (COGS basis when supplied) | n/a | n/a |
| PAT / net worth | 9.9% | AMBER |

### 11. Star Cement Ltd - GREEN (score 1.0)

- Sector: Cement; latest year FY2025
- Level signals: PAT / net worth at 5.9% is in the amber band (green needs 10.0%)

| Ratio | FY2025 | Band |
| --- | ---: | --- |
| Gross debt / EBITDA (cash not in source) | 0.70 | GREEN |
| Interest coverage (EBITDA / interest) | 18.09 | GREEN |
| Cash interest cover (CFO / interest) | 9.25 | GREEN |
| DSCR (CFO / (interest + scheduled principal)) | n/a | n/a |
| Current ratio | n/a | n/a |
| Quick ratio | n/a | n/a |
| Debt / net worth (contingents not in source) | 0.14 | GREEN |
| CFO / total debt | 0.73 | GREEN |
| EBITDA margin | 18.3% | GREEN |
| Revenue growth (YoY) | n/a | n/a |
| Receivable days | 23 | GREEN |
| Inventory days (COGS basis when supplied) | n/a | n/a |
| PAT / net worth | 5.9% | AMBER |

### 12. Welspun Living Ltd - GREEN (score 1.0)

- Sector: Textiles; latest year FY2025
- Level signals: EBITDA margin at 12.3% is in the amber band (green needs 15.0%)

| Ratio | FY2025 | Band |
| --- | ---: | --- |
| Gross debt / EBITDA (cash not in source) | 2.13 | GREEN |
| Interest coverage (EBITDA / interest) | 5.99 | GREEN |
| Cash interest cover (CFO / interest) | 3.17 | GREEN |
| DSCR (CFO / (interest + scheduled principal)) | n/a | n/a |
| Current ratio | n/a | n/a |
| Quick ratio | n/a | n/a |
| Debt / net worth (contingents not in source) | 0.57 | GREEN |
| CFO / total debt | 0.25 | GREEN |
| EBITDA margin | 12.3% | AMBER |
| Revenue growth (YoY) | n/a | n/a |
| Receivable days | 57 | GREEN |
| Inventory days (COGS basis when supplied) | n/a | n/a |
| PAT / net worth | 13.4% | GREEN |

## 4. Sector-relative view: where absolute bands and peers disagree

Each borrower's latest ratios against the median of its own sector in this panel (minimum three peers). *Hidden relative weakness*: green on absolute thresholds but the weakest in the sector by at least the deterioration trigger. *Sector-wide level*: amber or red on absolute thresholds but at or better than the sector median.

| Borrower | Sector | Ratio | Value | Absolute band | Sector median | Rank | View |
| --- | --- | --- | ---: | --- | ---: | --- | --- |
| Nuvoco Vistas Corporation Ltd | Cement | Cash interest cover (CFO / interest) | 2.68 | green | 4.33 | 3 of 3 | hidden relative weakness |
| JK Lakshmi Cement Ltd | Cement | EBITDA margin | 14.0% | amber | 14.0% | 2 of 3 | sector-wide level |
| Nuvoco Vistas Corporation Ltd | Cement | Interest coverage (EBITDA / interest) | 2.77 | green | 4.77 | 3 of 3 | hidden relative weakness |
| Star Cement Ltd | Cement | PAT / net worth | 5.9% | amber | 5.9% | 2 of 3 | sector-wide level |
| JK Lakshmi Cement Ltd | Cement | PAT / net worth | 7.8% | amber | 5.9% | 1 of 3 | sector-wide level |
| JK Lakshmi Cement Ltd | Cement | Debt / net worth (contingents not in source) | 0.74 | green | 0.45 | 3 of 3 | hidden relative weakness |
| Gujarat Fluorochemicals Ltd | Chemicals | CFO / total debt | 0.26 | green | 0.39 | 3 of 3 | hidden relative weakness |
| Gujarat Fluorochemicals Ltd | Chemicals | Cash interest cover (CFO / interest) | 3.71 | green | 6.61 | 3 of 3 | hidden relative weakness |
| SRF Ltd | Chemicals | EBITDA margin | 18.5% | green | 22.7% | 3 of 3 | hidden relative weakness |
| Navin Fluorine International Ltd | Chemicals | Gross debt / EBITDA (cash not in source) | 2.75 | green | 1.89 | 3 of 3 | hidden relative weakness |
| SRF Ltd | Chemicals | PAT / net worth | 9.9% | amber | 9.9% | 2 of 3 | sector-wide level |
| Navin Fluorine International Ltd | Chemicals | Receivable days | 90 | amber | 90 | 2 of 3 | sector-wide level |
| Piramal Pharma Ltd | Pharma | CFO / total debt | 0.18 | amber | 0.18 | 2 of 3 | sector-wide level |
| Piramal Pharma Ltd | Pharma | Interest coverage (EBITDA / interest) | 3.42 | green | 9.20 | 3 of 3 | hidden relative weakness |
| Granules India Ltd | Pharma | Receivable days | 77 | amber | 92 | 1 of 3 | sector-wide level |
| Glenmark Pharmaceuticals Ltd | Pharma | Receivable days | 92 | red | 92 | 2 of 3 | sector-wide level |
| Welspun Living Ltd | Textiles | CFO / total debt | 0.25 | green | 0.49 | 3 of 3 | hidden relative weakness |
| Welspun Living Ltd | Textiles | Cash interest cover (CFO / interest) | 3.17 | green | 3.67 | 3 of 3 | hidden relative weakness |
| Welspun Living Ltd | Textiles | EBITDA margin | 12.3% | amber | 12.3% | 2 of 3 | sector-wide level |
| Vardhman Textiles Ltd | Textiles | EBITDA margin | 12.9% | amber | 12.3% | 1 of 3 | sector-wide level |
| Arvind Ltd | Textiles | Interest coverage (EBITDA / interest) | 4.30 | green | 5.99 | 3 of 3 | hidden relative weakness |
| Arvind Ltd | Textiles | PAT / net worth | 9.7% | amber | 9.7% | 2 of 3 | sector-wide level |

## 5. How to read this report

A level signal means the ratio is outside its green band in the latest year. A deterioration signal means the ratio moved against the borrower by more than the configured trigger in one year, even if the level is still inside a green or amber band - this is the early part of the early-warning system.

Ratios shown as n/a are undefined (zero denominator) or not meaningful (negative EBITDA or non-positive net worth). Those cases raise an explicit data flag instead of an infinity.

See README.md for formulas, threshold defaults and limitations. This report is an analytical screen, not a credit decision.

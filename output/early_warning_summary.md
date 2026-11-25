# Credit Early-Warning Monitor - Portfolio Summary

- Generated: 20-Nov-2026 20:08
- Panel: `data/borrower_panel.csv`
- Config applied: `config/thresholds.yaml`
- Borrowers: 6 | Latest fiscal year in panel: FY2025
- Bands: 2 red, 2 amber, 2 green

Scoring: each red level signal counts 3, each amber level signal 1, each deterioration flag 0.5. Red band at score >= 12, amber at score >= 4.

## 1. Ranking (worst first)

| Rank | Borrower | Sector | Score | Band | Red | Amber | Deterioration | Top tripped signals |
| ---: | --- | --- | ---: | --- | ---: | ---: | ---: | --- |
| 1 | Deccan Auto Components Pvt Ltd | Auto components | 30.0 | RED | 9 | 3 | 6 | CFO / total debt; Cash interest cover (CFO / interest); EBITDA margin |
| 2 | Sundaram Textiles Ltd | Textiles | 29.0 | RED | 8 | 2 | 6 | EBITDA (input); CFO / total debt; Current ratio |
| 3 | Kalyan Agro Foods Ltd | Food processing | 8.5 | AMBER | 0 | 7 | 3 | CFO / total debt; Cash interest cover (CFO / interest); EBITDA margin |
| 4 | Nirvana Pharma Labs Ltd | Pharmaceuticals | 8.5 | AMBER | 0 | 5 | 7 | CFO / total debt; EBITDA margin; PAT / net worth |
| 5 | Vaigai Engineering Works Ltd | Capital goods | 1.0 | GREEN | 0 | 1 | 0 | Revenue growth (YoY) |
| 6 | Tapti Chemicals Ltd | Specialty chemicals | 0.0 | GREEN | 0 | 0 | 0 | none |

## 2. Top signals by frequency (FY2025)

| # | Signal | Times tripped |
| ---: | --- | ---: |
| 1 | PAT / net worth | 8 |
| 2 | Cash interest cover (CFO / interest) | 7 |
| 3 | CFO / total debt | 7 |

Across the whole panel history (all years), the most frequent signals are: Cash interest cover (CFO / interest) (21), EBITDA margin (19), PAT / net worth (18).

## 3. Borrower detail

### 1. Deccan Auto Components Pvt Ltd - RED (score 30.0)

- Sector: Auto components; latest year FY2025
- Level signals: Net debt / EBITDA at 16.39x is in the red band (green needs 3.00x); Interest coverage (EBITDA / interest) at 0.66x is in the red band (green needs 2.50x); Cash interest cover (CFO / interest) at -0.18x is in the red band (green needs 1.50x); Current ratio at 1.04x is in the amber band (green needs 1.33x); Quick ratio at 0.57x is in the red band (green needs 1.00x); TOL / TNW ((debt + contingent) / net worth) at 3.21x is in the red band (green needs 2.00x); CFO / total debt at -0.02x is in the red band (green needs 0.20x); EBITDA margin at 6.5% is in the red band (green needs 15.0%); Revenue growth (YoY) at -7.4% is in the red band (green needs 8.0%); Receivable days at 90d is in the amber band (green needs 60d); Inventory days (COGS basis when supplied) at 66d is in the amber band (green needs 60d); PAT / net worth at -13.0% is in the red band (green needs 10.0%)
- Deterioration (year on year): Net debt / EBITDA rose 6.13x year on year (trigger 0.50x) - level already red, no additional weight; Cash interest cover (CFO / interest) fell 0.31x year on year (trigger 0.25x) - level already red, no additional weight; Quick ratio fell 0.10x year on year (trigger 0.10x) - level already red, no additional weight; TOL / TNW ((debt + contingent) / net worth) rose 0.48x year on year (trigger 0.25x) - level already red, no additional weight; EBITDA margin fell 2.5pp year on year (trigger 2.0pp) - level already red, no additional weight; PAT / net worth fell 10.2pp year on year (trigger 3.0pp) - level already red, no additional weight

| Ratio | FY2022 | FY2023 | FY2024 | FY2025 | Band |
| --- | ---: | ---: | ---: | ---: | --- |
| Net debt / EBITDA | 6.12 | 7.42 | 10.26 | 16.39 | RED |
| Interest coverage (EBITDA / interest) | 2.05 | 1.58 | 1.08 | 0.66 | RED |
| Cash interest cover (CFO / interest) | 1.29 | 0.73 | 0.13 | -0.18 | RED |
| DSCR (CFO / (interest + scheduled principal)) | n/a | n/a | n/a | n/a | n/a |
| Current ratio | 1.36 | 1.27 | 1.18 | 1.04 | AMBER |
| Quick ratio | 0.84 | 0.76 | 0.67 | 0.57 | RED |
| TOL / TNW ((debt + contingent) / net worth) | 2.19 | 2.39 | 2.73 | 3.21 | RED |
| CFO / total debt | 0.10 | 0.06 | 0.01 | -0.02 | RED |
| EBITDA margin | 12.0% | 11.0% | 9.0% | 6.5% | RED |
| Revenue growth (YoY) | n/a | -3.7% | -5.7% | -7.4% | RED |
| Receivable days | 78 | 83 | 87 | 90 | AMBER |
| Inventory days (COGS basis when supplied) | 58 | 61 | 63 | 66 | AMBER |
| PAT / net worth | 7.1% | 4.9% | -2.8% | -13.0% | RED |

### 2. Sundaram Textiles Ltd - RED (score 29.0)

- Sector: Textiles; latest year FY2025
- Level signals: Cash interest cover (CFO / interest) at -0.61x is in the red band (green needs 1.50x); Current ratio at 0.80x is in the red band (green needs 1.33x); Quick ratio at 0.38x is in the red band (green needs 1.00x); TOL / TNW ((debt + contingent) / net worth) at 3.75x is in the red band (green needs 2.00x); CFO / total debt at -0.05x is in the red band (green needs 0.20x); EBITDA margin at -3.8% is in the red band (green needs 15.0%); Revenue growth (YoY) at -6.9% is in the red band (green needs 8.0%); Receivable days at 76d is in the amber band (green needs 60d); Inventory days (COGS basis when supplied) at 68d is in the amber band (green needs 60d); PAT / net worth at -26.1% is in the red band (green needs 10.0%)
- Deterioration (year on year): Cash interest cover (CFO / interest) fell 0.66x year on year (trigger 0.25x) - level already red, no additional weight; TOL / TNW ((debt + contingent) / net worth) rose 0.85x year on year (trigger 0.25x) - level already red, no additional weight; CFO / total debt fell 0.06x year on year (trigger 0.05x) - level already red, no additional weight; EBITDA margin fell 8.9pp year on year (trigger 2.0pp) - level already red, no additional weight; Revenue growth (YoY) fell 3.1pp year on year (trigger 3.0pp) - level already red, no additional weight; PAT / net worth fell 17.8pp year on year (trigger 3.0pp) - level already red, no additional weight
- Data flags: EBITDA is -18.00 crore

| Ratio | FY2022 | FY2023 | FY2024 | FY2025 | Band |
| --- | ---: | ---: | ---: | ---: | --- |
| Net debt / EBITDA | 7.78 | 9.45 | 16.23 | n/a | n/a |
| Interest coverage (EBITDA / interest) | 1.43 | 1.17 | 0.68 | n/a | n/a |
| Cash interest cover (CFO / interest) | 0.88 | 0.50 | 0.05 | -0.61 | RED |
| DSCR (CFO / (interest + scheduled principal)) | n/a | n/a | n/a | n/a | n/a |
| Current ratio | 1.11 | 1.02 | 0.92 | 0.80 | RED |
| Quick ratio | 0.61 | 0.54 | 0.46 | 0.38 | RED |
| TOL / TNW ((debt + contingent) / net worth) | 2.32 | 2.54 | 2.90 | 3.75 | RED |
| CFO / total debt | 0.07 | 0.04 | 0.00 | -0.05 | RED |
| EBITDA margin | 9.0% | 8.0% | 5.1% | -3.8% | RED |
| Revenue growth (YoY) | n/a | -2.8% | -3.8% | -6.9% | RED |
| Receivable days | 71 | 75 | 75 | 76 | AMBER |
| Inventory days (COGS basis when supplied) | 64 | 65 | 65 | 68 | AMBER |
| PAT / net worth | 6.3% | 2.2% | -8.3% | -26.1% | RED |

### 3. Kalyan Agro Foods Ltd - AMBER (score 8.5)

- Sector: Food processing; latest year FY2025
- Level signals: Net debt / EBITDA at 3.08x is in the amber band (green needs 3.00x); Cash interest cover (CFO / interest) at 1.02x is in the amber band (green needs 1.50x); Quick ratio at 0.87x is in the amber band (green needs 1.00x); CFO / total debt at 0.12x is in the amber band (green needs 0.20x); EBITDA margin at 10.2% is in the amber band (green needs 15.0%); Revenue growth (YoY) at 4.8% is in the amber band (green needs 8.0%); PAT / net worth at 8.5% is in the amber band (green needs 10.0%)
- Deterioration (year on year): Cash interest cover (CFO / interest) fell 0.69x year on year (trigger 0.25x) but still inside the amber band; CFO / total debt fell 0.07x year on year (trigger 0.05x) but still inside the amber band; PAT / net worth fell 3.4pp year on year (trigger 3.0pp) but still inside the amber band

| Ratio | FY2022 | FY2023 | FY2024 | FY2025 | Band |
| --- | ---: | ---: | ---: | ---: | --- |
| Net debt / EBITDA | 2.04 | 2.30 | 2.80 | 3.08 | AMBER |
| Interest coverage (EBITDA / interest) | 3.98 | 3.53 | 2.92 | 2.59 | GREEN |
| Cash interest cover (CFO / interest) | 2.97 | 2.44 | 1.71 | 1.02 | AMBER |
| DSCR (CFO / (interest + scheduled principal)) | n/a | n/a | n/a | n/a | n/a |
| Current ratio | 1.54 | 1.53 | 1.52 | 1.47 | GREEN |
| Quick ratio | 0.90 | 0.90 | 0.90 | 0.87 | AMBER |
| TOL / TNW ((debt + contingent) / net worth) | 0.79 | 0.80 | 0.84 | 0.87 | GREEN |
| CFO / total debt | 0.32 | 0.27 | 0.19 | 0.12 | AMBER |
| EBITDA margin | 13.0% | 12.0% | 10.5% | 10.2% | AMBER |
| Revenue growth (YoY) | n/a | 8.2% | 7.5% | 4.8% | AMBER |
| Receivable days | 56 | 55 | 54 | 54 | GREEN |
| Inventory days (COGS basis when supplied) | 61 | 59 | 57 | 57 | GREEN |
| PAT / net worth | 14.8% | 14.5% | 11.8% | 8.5% | AMBER |

### 4. Nirvana Pharma Labs Ltd - AMBER (score 8.5)

- Sector: Pharmaceuticals; latest year FY2025
- Level signals: CFO / total debt at 0.11x is in the amber band (green needs 0.20x); EBITDA margin at 13.8% is in the amber band (green needs 15.0%); Revenue growth (YoY) at 2.2% is in the amber band (green needs 8.0%); Receivable days at 89d is in the amber band (green needs 60d); PAT / net worth at 9.1% is in the amber band (green needs 10.0%)
- Deterioration (year on year): Net debt / EBITDA rose 0.61x year on year (trigger 0.50x) but still inside the green band; Interest coverage (EBITDA / interest) fell 2.82x year on year (trigger 0.50x) but still inside the green band; Cash interest cover (CFO / interest) fell 2.56x year on year (trigger 0.25x) but still inside the green band; Quick ratio fell 0.13x year on year (trigger 0.10x) but still inside the green band; CFO / total debt fell 0.12x year on year (trigger 0.05x) but still inside the amber band; Revenue growth (YoY) fell 3.2pp year on year (trigger 3.0pp) but still inside the amber band; PAT / net worth fell 5.4pp year on year (trigger 3.0pp) but still inside the amber band

| Ratio | FY2022 | FY2023 | FY2024 | FY2025 | Band |
| --- | ---: | ---: | ---: | ---: | --- |
| Net debt / EBITDA | 1.09 | 1.37 | 1.82 | 2.44 | GREEN |
| Interest coverage (EBITDA / interest) | 13.72 | 11.13 | 8.23 | 5.41 | GREEN |
| Cash interest cover (CFO / interest) | 10.62 | 7.20 | 4.23 | 1.67 | GREEN |
| DSCR (CFO / (interest + scheduled principal)) | n/a | n/a | n/a | n/a | n/a |
| Current ratio | 2.08 | 2.04 | 1.93 | 1.80 | GREEN |
| Quick ratio | 1.50 | 1.44 | 1.32 | 1.20 | GREEN |
| TOL / TNW ((debt + contingent) / net worth) | 0.75 | 0.80 | 0.89 | 0.99 | GREEN |
| CFO / total debt | 0.47 | 0.35 | 0.23 | 0.11 | AMBER |
| EBITDA margin | 18.0% | 17.0% | 15.5% | 13.8% | AMBER |
| Revenue growth (YoY) | n/a | 7.4% | 5.3% | 2.2% | AMBER |
| Receivable days | 78 | 81 | 85 | 89 | AMBER |
| Inventory days (COGS basis when supplied) | 42 | 43 | 47 | 51 | GREEN |
| PAT / net worth | 19.3% | 18.2% | 14.5% | 9.1% | AMBER |

### 5. Vaigai Engineering Works Ltd - GREEN (score 1.0)

- Sector: Capital goods; latest year FY2025
- Level signals: Revenue growth (YoY) at 7.9% is in the amber band (green needs 8.0%)

| Ratio | FY2022 | FY2023 | FY2024 | FY2025 | Band |
| --- | ---: | ---: | ---: | ---: | --- |
| Net debt / EBITDA | 1.66 | 1.56 | 1.45 | 1.32 | GREEN |
| Interest coverage (EBITDA / interest) | 5.47 | 6.20 | 6.31 | 6.99 | GREEN |
| Cash interest cover (CFO / interest) | 3.82 | 4.55 | 4.83 | 5.50 | GREEN |
| DSCR (CFO / (interest + scheduled principal)) | n/a | n/a | n/a | n/a | n/a |
| Current ratio | 1.84 | 1.90 | 1.93 | 1.98 | GREEN |
| Quick ratio | 1.23 | 1.28 | 1.31 | 1.36 | GREEN |
| TOL / TNW ((debt + contingent) / net worth) | 0.90 | 0.84 | 0.78 | 0.72 | GREEN |
| CFO / total debt | 0.32 | 0.36 | 0.39 | 0.43 | GREEN |
| EBITDA margin | 14.0% | 14.5% | 15.0% | 15.4% | GREEN |
| Revenue growth (YoY) | n/a | 9.3% | 7.4% | 7.9% | AMBER |
| Receivable days | 53 | 53 | 52 | 51 | GREEN |
| Inventory days (COGS basis when supplied) | 49 | 48 | 48 | 47 | GREEN |
| PAT / net worth | 23.0% | 23.7% | 24.2% | 24.9% | GREEN |

### 6. Tapti Chemicals Ltd - GREEN (score 0.0)

- Sector: Specialty chemicals; latest year FY2025
- Level signals: none - every ratio is inside the green band

| Ratio | FY2022 | FY2023 | FY2024 | FY2025 | Band |
| --- | ---: | ---: | ---: | ---: | --- |
| Net debt / EBITDA | 0.82 | 0.80 | 0.73 | 0.66 | GREEN |
| Interest coverage (EBITDA / interest) | 8.23 | 8.58 | 8.98 | 9.31 | GREEN |
| Cash interest cover (CFO / interest) | 7.14 | 7.87 | 8.44 | 8.94 | GREEN |
| DSCR (CFO / (interest + scheduled principal)) | n/a | n/a | n/a | n/a | n/a |
| Current ratio | 2.20 | 2.22 | 2.23 | 2.26 | GREEN |
| Quick ratio | 1.47 | 1.49 | 1.51 | 1.56 | GREEN |
| TOL / TNW ((debt + contingent) / net worth) | 0.46 | 0.45 | 0.43 | 0.41 | GREEN |
| CFO / total debt | 0.67 | 0.72 | 0.77 | 0.82 | GREEN |
| EBITDA margin | 16.0% | 16.5% | 17.0% | 17.2% | GREEN |
| Revenue growth (YoY) | n/a | 8.3% | 8.3% | 8.9% | GREEN |
| Receivable days | 53 | 52 | 51 | 50 | GREEN |
| Inventory days (COGS basis when supplied) | 56 | 55 | 54 | 52 | GREEN |
| PAT / net worth | 24.2% | 25.4% | 26.1% | 26.8% | GREEN |

## 4. Sector-relative view: where absolute bands and peers disagree

Each borrower's latest ratios against the median of its own sector in this panel (minimum three peers). *Hidden relative weakness*: green on absolute thresholds but the weakest in the sector by at least the deterioration trigger. *Sector-wide level*: amber or red on absolute thresholds but at or better than the sector median.

No disagreements in the latest year.

## 5. How to read this report

A level signal means the ratio is outside its green band in the latest year. A deterioration signal means the ratio moved against the borrower by more than the configured trigger in one year, even if the level is still inside a green or amber band - this is the early part of the early-warning system.

Ratios shown as n/a are undefined (zero denominator) or not meaningful (negative EBITDA or non-positive net worth). Those cases raise an explicit data flag instead of an infinity.

See README.md for formulas, threshold defaults and limitations. This report is an analytical screen, not a credit decision.

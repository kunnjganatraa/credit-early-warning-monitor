# Credit Early-Warning Monitor

A small, tested Python tool for a credit analyst working on Indian mid-corporate
portfolios. It takes a panel of borrower financials (one row per borrower per
fiscal year, rupee crore), computes thirteen credit ratios, bands each ratio
green / amber / red against thresholds held in a config file, and produces a
ranked watchlist, a per-borrower ratio history, a full signal log and a markdown
summary.

The point of the tool is the second half of the name: it flags **deterioration**,
not only bad levels. A borrower whose interest coverage falls 1.2x in a year is
put on the list even if 2.8x is still a comfortable number, because that is the
part of the curve where a credit analyst can still do something about it.

Runs offline. Standard library plus pandas, openpyxl and (optionally) matplotlib.

## What changed in v2 (21 November 2026)

| Change | Why |
| --- | --- |
| **True DSCR** added: `cfo / (interest + scheduled_principal)`. The old ratio is kept and renamed *cash interest cover* (CFO / interest). | A coverage ratio that ignores principal says nothing about a bullet maturity. A borrower with 4.0x cash interest cover and a principal payment eight times its interest has a DSCR of 0.44x (see `test_bullet_maturity_shows_up_in_dscr_but_not_in_cash_interest_cover`). No principal schedule, no DSCR: it is `n/a` with an explicit flag, never estimated. |
| **COGS-based inventory days** when an optional `cogs` column is supplied; otherwise revenue, with a flag. | Revenue-based days understate the holding period by the gross margin (one third at a 25% margin). |
| **Sector-relative lens** (`ews/sector.py`, `Sector_View` sheet, markdown section 4). | Absolute thresholds judge a cement company and a textile company on the same bars. The lens ranks each ratio against sector peers and reports where the two views disagree. |
| **Run on real borrowers** (`data/real_panel.csv`, `output_real/`): 12 listed companies, 4 sectors, FY25 and FY26 figures from an aggregator, every row sourced in `data/real_panel_sources.csv`. A sanity check, not a validation. | v1 had only been run on a panel built to land 2 red / 2 amber / 2 green. See section 6. |
| 64 tests (was 52). | New cases: true DSCR, bullet maturity, COGS basis, optional columns, every sector-lens branch. |

### Update, 24 November 2026

- The real-borrower run now uses `config/thresholds_real_panel.yaml`: the same thresholds, with two labels corrected. On that panel the source gives no cash or contingent liabilities, so the ratio is **gross** debt / EBITDA and debt / net worth, and the reports now say so instead of printing "Net debt / EBITDA".
- Section 6 is renamed from "Validation" to "Sanity check", and a one-year-ahead test is added (`data/real_panel_fy25.csv`, `output_real_fy25/`). The result is mixed and is reported as it came out.
- Section 6 reconciles the tool's Piramal Pharma figures with the CARE-basis figures in the separate credit memo.
- No change to the ratio or scoring code; the 64 tests are unchanged and pass.

---

## 1. What it does

1. Loads and validates the panel (columns, numeric types, duplicate borrower-year
   rows, blanks).
2. Computes thirteen ratios per borrower-year, returning `NaN` plus an explicit
   flag wherever a ratio is undefined rather than an infinity.
3. Bands every ratio green / amber / red using the thresholds in
   `config/thresholds.yaml` - no thresholds are hard-coded.
4. Detects year-on-year deterioration per ratio against a configured trigger,
   independent of the band.
5. Scores each borrower (weighted count of red, amber and deterioration signals),
   assigns a band, and ranks the portfolio worst first.
6. Writes `early_warning_report.xlsx` (Watchlist, one sheet per borrower,
   Signal_Log, Config), `early_warning_summary.md` and a score chart PNG.

---

## 2. Ratios, formulas and default thresholds

All amounts in rupee crore. `FY` is the fiscal year of the row, `FY-1` the
borrower's previous row in the panel. Thresholds below are the defaults shipped
in `config/thresholds.yaml`; edit that file, not the code.

| # | Ratio (key) | Formula | Better when | Green | Amber | Red | Deterioration trigger |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | Net debt / EBITDA (`net_debt_ebitda`) | `(total_debt - cash) / ebitda` | lower | <= 3.00x | 3.00x - 4.50x | > 4.50x | +0.50x in a year |
| 2 | Interest coverage (`interest_coverage`) | `ebitda / interest_expense` | higher | >= 2.50x | 1.50x - 2.50x | < 1.50x | -0.50x |
| 3 | Cash interest cover (`dscr_proxy`) | `cfo / interest_expense` | higher | >= 1.50x | 1.00x - 1.50x | < 1.00x | -0.25x |
| 3a | DSCR (`dscr`) | `cfo / (interest_expense + scheduled_principal)`; `n/a` + flag if no schedule | higher | >= 1.25x | 1.00x - 1.25x | < 1.00x | -0.20x |
| 4 | Current ratio (`current_ratio`) | `current_assets / current_liabilities` | higher | >= 1.33x | 1.00x - 1.33x | < 1.00x | -0.15x |
| 5 | Quick ratio (`quick_ratio`) | `(current_assets - inventory) / current_liabilities` | higher | >= 1.00x | 0.70x - 1.00x | < 0.70x | -0.10x |
| 6 | TOL / TNW (`tol_tnw`) | `(total_debt + contingent_liabilities) / net_worth` | lower | <= 2.00x | 2.00x - 3.00x | > 3.00x | +0.25x |
| 7 | CFO / total debt (`cfo_to_debt`) | `cfo / total_debt` | higher | >= 0.20x | 0.10x - 0.20x | < 0.10x | -0.05x |
| 8 | EBITDA margin (`ebitda_margin`) | `ebitda / revenue` | higher | >= 15.0% | 10.0% - 15.0% | < 10.0% | -2.0pp |
| 9 | Revenue growth (`revenue_growth`) | `revenue / revenue(FY-1) - 1` | higher | >= 8.0% | 0.0% - 8.0% | < 0.0% | -3.0pp |
| 10 | Receivable days (`receivable_days`) | `receivables / revenue * 365` | lower | <= 60 days | 60 - 90 days | > 90 days | +10 days |
| 11 | Inventory days (`inventory_days`) | `inventory / cogs * 365` if `cogs` supplied, else `inventory / revenue * 365` (flagged) | lower | <= 60 days | 60 - 90 days | > 90 days | +10 days |
| 12 | PAT / net worth (`pat_to_networth`) | `pat / net_worth` | higher | >= 10.0% | 5.0% - 10.0% | < 5.0% | -3.0pp |

Band boundaries are **inclusive**: a value sitting exactly on the green
threshold is green, exactly on the amber threshold is amber.

A deterioration trigger is the minimum move in the ratio's own unit, in the
adverse direction, that counts as deterioration. It is tested with `>=`, so a
fall of exactly 0.50x on interest coverage fires the 0.50x trigger.

### Division by zero, negative EBITDA and negative net worth

Undefined is never represented as `inf`. Every ratio that cannot be computed
returns `NaN` and records a flag, and a `NaN` ratio is never banded (it shows as
`n/a`, is not counted in the score, and is not written to the signal log as a
level signal):

| Case | Behaviour |
| --- | --- |
| `ebitda <= 0` | `net_debt_ebitda` and `interest_coverage` return `NaN` and raise `non_positive_ebitda`. A negative multiple of a negative EBITDA is not a leverage measure and a negative coverage ratio cannot be banded sensibly. The year also raises a **critical red signal** (weight = red weight) so the borrower is still penalised. `ebitda_margin` is still computed and will be negative - that is informative. |
| `net_worth <= 0` | `tol_tnw` and `pat_to_networth` return `NaN` and raise `non_positive_net_worth`, plus a critical red signal. Sign-flipped solvency ratios (negative net worth, negative debt capacity) are worse than useless as bands. |
| any other zero denominator (`interest_expense`, `current_liabilities`, `total_debt`, `revenue`, prior-year `revenue`) | the affected ratio returns `NaN` and raises `zero_denominator` with the offending line item named. |
| first year of a borrower | `revenue_growth` returns `NaN` and raises `no_prior_year`; no deterioration flag can fire for that year. |

So a borrower with negative EBITDA is scored through the critical flag, its
EBITDA margin and its working-capital ratios, not through a fabricated
net-debt/EBITDA number. `tests/test_ratios.py` covers each of these cases.

---

## 3. How the score is weighted

Per borrower, in the latest year in the panel:

```
score = red_weight       * (number of red level signals)
      + amber_weight     * (number of amber level signals)
      + deterioration_weight * (deterioration flags that are not already red)
```

Defaults: `red_weight = 3.0`, `amber_weight = 1.0`, `deterioration_weight = 0.5`.
Critical data flags (negative EBITDA, non-positive net worth) count at the red
weight. Deterioration on a ratio whose level is already red adds **nothing** -
the red level signal has already taken the full weight; set
`deterioration_counts_when_red: true` in the config if you want it counted twice.

Band from score: `red` at `score >= 12`, `amber` at `score >= 4`, otherwise
`green` (both cutoffs configurable). Twelve is roughly "four reds", or "three
reds plus three ambers" - i.e. a borrower needs several independent things wrong
before it is called red.

Worked example (Deccan Auto Components, FY2025): 9 red signals, 3 amber signals,
6 deterioration flags of which 6 are on already-red ratios, so
`9*3.0 + 3*1.0 + 0*0.5 = 30.0` -> red band, rank 1.

The score is ordinal. It is not a probability of default and it has not been
calibrated against any default history.

---

## 4. Install and run

Python 3.12. No network access is needed at runtime.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python cli.py --panel data/borrower_panel.csv \
              --config config/thresholds.yaml \
              --out output/
```

Optional flags: `--no-chart` skips the PNG, `--quiet` suppresses the console
summary. The command exits `0` on success and `2` on a bad panel or config
(with a one-line reason on stderr).

Run the tests:

```bash
pytest -q
```

64 tests, including hand-computed ratio values, the negative-EBITDA and
zero-net-worth cases, band assignment exactly on the threshold boundaries, a
deterioration flag firing on a year-on-year fall inside the green band, a true
DSCR breaking on a bullet maturity, COGS-based inventory days, and every branch
of the sector-relative lens.

Run on the real-borrower panel:

```bash
python cli.py --panel data/real_panel.csv --config config/thresholds_real_panel.yaml --out output_real/
```

Optional panel columns `scheduled_principal` and `cogs` are added as blank if a
CSV does not have them. `--min-peers` (default 3) sets the minimum sector size
for the sector-relative view.

### Layout

```
README.md
requirements.txt
cli.py                     command line entry point
conftest.py                puts the repo on sys.path for pytest, shared fixtures
ews/
  __init__.py
  config.py                config loading/validation, built-in YAML reader
  panel.py                 panel loading and validation
  ratios.py                the thirteen ratio formulas, flags for undefined values
  sector.py                sector-relative lens (peer rank, median, disagreements)
  scoring.py               banding, deterioration, scoring, portfolio analysis
  excel_report.py          the .xlsx workbook
  markdown_report.py       the .md summary
  charts.py                optional PNG score chart
config/thresholds.yaml     every threshold, weight and cutoff
data/borrower_panel.csv    6 borrowers x 4 fiscal years of sample data
data/real_panel.csv        12 listed borrowers x FY25-FY26, reported numbers
data/real_panel_sources.csv  source URL and field mapping for every real borrower
tests/                     pytest suite
output/                    CLI output on the sample panel
output_real/               CLI output on the real-borrower panel
```

### Config format

YAML or JSON, chosen by file extension. YAML is read with PyYAML when it is
installed and otherwise with the small built-in reader in `ews/config.py`
(mappings, scalar lists, comments, quoted strings, numbers, booleans) - so the
tool runs on a bare Python install with no extra dependency. Each ratio needs
`label`, `direction` (`lower_is_better` or `higher_is_better`), `unit`
(`x`, `pct` or `days`), `green`, `amber` and optionally `deterioration`.
Configs are validated on load: a missing key, an unknown direction, or an
inverted band (amber on the wrong side of green) fails with a clear message.

To add a fourteenth ratio: add the formula branch in `ews/ratios.py` and an
entry in the config. Nothing else needs to change.

---

## 5. Sample output

`data/borrower_panel.csv` is engineered so the sample portfolio lands 2 red,
2 amber, 2 green. Console output of the run above:

```
Credit Early-Warning Monitor
================================================================================================
Rank  Band    Score  Borrower                            Red Amber  Det  Top signal
------------------------------------------------------------------------------------------------
   1  RED      30.0  Deccan Auto Components Pvt Ltd        9     3    6  CFO / total debt
   2  RED      29.0  Sundaram Textiles Ltd                 8     2    6  EBITDA (input)
   3  AMBER     8.5  Kalyan Agro Foods Ltd                 0     7    3  CFO / total debt
   4  AMBER     8.5  Nirvana Pharma Labs Ltd               0     5    7  CFO / total debt
   5  GREEN     1.0  Vaigai Engineering Works Ltd          0     1    0  Revenue growth (YoY)
   6  GREEN     0.0  Tapti Chemicals Ltd                   0     0    0  none
------------------------------------------------------------------------------------------------
Bands: 2 red, 2 amber, 2 green | signals logged: 171
Top signals by frequency (latest year): PAT / net worth (8), Cash interest cover (CFO / interest) (7), CFO / total debt (7)
```

Files written to `output/`:

| File | Contents |
| --- | --- |
| `early_warning_report.xlsx` | `Watchlist` (ranked, worst first), one `Borrower_Detail` sheet per borrower with the full ratio history, inputs and latest-year signals, `Signal_Log` (every tripped signal with year, value, prior value, change and weight), `Config` (the thresholds actually applied plus the scoring parameters). Headers use a dark fill with white bold text, panes are frozen and column widths are sized to content. |
| `early_warning_summary.md` | Ranked table, top three signals by frequency, then a per-borrower section with level signals, deterioration and the ratio table. |
| `score_by_borrower.png` | Score per borrower, coloured by band, with the amber and red cutoffs drawn as reference lines. |

Why the two reds are red:

- **Deccan Auto Components** - revenue down 16% over three years while debt rose
  from 620 to 745 crore: net debt/EBITDA 16.4x, interest coverage 0.66x, TOL/TNW
  3.2x, CFO negative, PAT/NW -13%, current ratio 1.04x, quick ratio 0.57x.
  Nine red level signals and six deterioration flags; leverage alone worsened
  6.1x in FY2025.
- **Sundaram Textiles** - EBITDA turned negative in FY2025 (-18 crore), so
  leverage and coverage are `n/a` and raise a critical flag; on top of that
  revenue fell 6.9%, CFO was -25 crore, TOL/TNW reached 3.75x, current ratio
  0.80x, quick ratio 0.38x and PAT/NW -26%.

The two ambers are the interesting cases: **Kalyan Agro Foods** has no red level
signal at all - it is amber because seven ratios sit in the amber band and cash
generation is slipping (cash interest cover 1.71x to 1.02x, CFO/debt 0.19x to 0.12x).
**Nirvana Pharma Labs** is amber on seven deterioration flags: coverage fell
from 8.2x to 5.4x and cash interest cover from 4.2x to 1.7x in one year while leverage climbed
- all still inside green, which is exactly the early warning the tool exists to
surface.

---

## 6. Sanity check on real borrowers

`data/real_panel.csv` holds FY25 and FY26 consolidated figures for twelve listed
companies, three each in chemicals, pharma, textiles and cement, taken from
Screener.in on 21 November 2026 (one URL per borrower in
`data/real_panel_sources.csv`). The source does not split out cash, contingent
liabilities, current assets, inventory or principal schedules, so on this panel
leverage is **gross** debt / EBITDA, TOL/TNW is debt / net worth, receivables
are rebuilt from reported debtor days, and DSCR, current and quick ratios are
`n/a`. That is deliberate: the tool reports what it cannot compute rather than
guessing. Two consequences should be read plainly. The true DSCR, the main v2
feature, is exercised only on the constructed panel and in the tests, because no
principal schedule is available for these twelve. And the figures come from an
aggregator, not from the filings, so they are good enough to exercise the tool
but are not a substitute for spreading the accounts. This run uses
`config/thresholds_real_panel.yaml`, which has the same thresholds and labels the
two affected ratios correctly.

```
Rank  Band    Score  Borrower                            Red Amber  Det  Top signal
   1  RED      12.0  Piramal Pharma Ltd                    3     2    4  Gross debt / EBITDA
   2  AMBER    10.0  Welspun Living Ltd                    3     0    4  EBITDA margin
   3  AMBER     5.0  Gujarat Fluorochemicals Ltd           1     2    0  Receivable days
   4  AMBER     5.0  Vardhman Textiles Ltd                 0     3    4  EBITDA margin
   5  GREEN     3.0  Glenmark Pharmaceuticals Ltd          1     0    1  Receivable days
 ... 7 more green
Bands: 1 red, 3 amber, 8 green
```

What the FY26 run shows. The two borrowers it puts at the top are the two whose
FY26 EBITDA fell most in this set: Piramal Pharma swung to a ₹326 crore loss with
EBITDA down 36% and gross debt/EBITDA of 6.2x; Welspun Living's EBITDA fell 39%
and profit 67%. Both are picked up through deterioration flags as well as
levels, which is the design intent. This is a coincident reading: the tool is
scoring the same FY26 numbers in which the deterioration appears, so it shows
the arithmetic works, not that the tool warns early.

One-year-ahead test. To see whether it would have warned early, the same
thresholds were run on FY25 figures alone (`data/real_panel_fy25.csv`,
`output_real_fy25/`; levels only, because a deterioration flag needs FY24).

| Borrower | FY25 rank of 12 (band) | What happened in FY26 | Verdict |
| --- | --- | --- | --- |
| Piramal Pharma | 2 (amber, score 8.0) | EBITDA down 36%, loss of ₹326 crore | flagged a year early |
| Welspun Living | 12 (green, score 1.0) | EBITDA down 39%, profit down 67% | missed |
| Glenmark Pharmaceuticals | 1 (amber, score 9.0) | EBITDA up 95%, profit up 30% | false alarm |

One hit, one miss and one false alarm in twelve names is not evidence of
predictive power. On this panel the tool is a coincident indicator: useful for
ranking a book on the latest accounts, not yet shown to lead. A real test needs
more years, more borrowers and an outcome the tool does not itself score, such
as later rating actions.

Reconciling Piramal Pharma with the credit memo. The tool shows gross
debt/EBITDA of 6.16x and a 10.4% EBITDA margin for FY26; the separate credit
memo shows 4.28x and 11.4% on CARE's definitions. They are the same accounts on
two bases:

| | Debt (₹ crore) | EBITDA (₹ crore) | Multiple | Margin |
| --- | ---: | ---: | ---: | ---: |
| This tool: borrowings including leases, no cash deducted; EBITDA excluding other income | 5,675 | 922 | 6.16x | 10.4% of ₹8,869 crore |
| Less ₹1,332 crore of cash and liquid funds | 4,343 | 922 | 4.71x | |
| CARE basis: add ₹50 crore of foreign exchange gain and ₹42 crore of other items to EBITDA | 4,343 | 1,014 | 4.28x | 11.4% of ₹8,919 crore |

The aggregator's borrowings of ₹5,675 crore equal the annual report's ₹5,495
crore of borrowings plus ₹179 crore of lease liabilities.

Where the sector lens changes the reading (latest year, minimum three peers):

| Borrower | Ratio | Value | Absolute band | Sector median | View |
| --- | --- | ---: | --- | ---: | --- |
| Piramal Pharma | Interest coverage | 2.70x | green | 10.42x | weakest in pharma by a wide margin; the absolute 2.5x bar lets it through |
| Gujarat Fluorochemicals | Gross debt / EBITDA | 2.27x | green | 1.49x | green absolutely, weakest of three chemicals peers |
| Welspun Living | Gross debt / EBITDA | 2.92x | green | 1.56x | green absolutely, weakest in textiles |
| SRF | EBITDA margin | 21.6% | green | 24.0% | lowest-margin chemicals name in the set |
| Vardhman Textiles | EBITDA margin | 12.6% | amber | 11.4% | amber absolutely but the best in textiles: the 15% bar is too high for the sector |

Twenty disagreements in all (`output_real/early_warning_report.xlsx`, sheet
`Sector_View`). The lesson for calibration is visible: textiles sit below the
15% margin bar as a sector, while a 2.5x coverage bar is far too lenient for
pharma peers running at 10x. A next step would be sector-specific threshold
sets in the config, which the lens makes easy to choose.

What this does not show. Twelve borrowers over two years is a sanity check, not
a back-test. The score is still uncalibrated against defaults (section 3).

---

## 7. Limitations (read these before using it on real borrowers)

- **Ratios are only as good as the accounting inputs.** The panel takes reported
  numbers at face value: no restatement, no IND-AS schedule mapping, no
  adjustment for capitalised items, revenue recognition timing, related-party
  transactions or off-balance-sheet structures. Garbage in, confident-looking
  garbage out.
- **Contingent liabilities need manual tagging.** The model uses one
  `contingent_liabilities` number per year, taken from the notes. Disclosure
  quality varies enormously across Indian mid-corporates, guarantees to group
  companies and disputed tax demands are often under-described, and nothing here
  checks whether the number is complete or comparable year to year.
- **Receivable days use revenue, not credit sales.** Inventory days use COGS
  when it is supplied (v2); receivable days still mix cash sales into the base.
- **DSCR needs a principal schedule.** v2 computes a true DSCR only when
  `scheduled_principal` is supplied, and has no debt-service reserve or
  moratorium logic. CFO is taken before interest paid (the usual Ind AS
  presentation); if a borrower reports interest inside operating cash flow, add
  it back before loading. CFO is lumpy, so one year's DSCR is noisy.
- **Sector thresholds are not yet separate.** The sector lens (v2) ranks within
  sector and flags disagreements, but scoring still uses one set of absolute
  thresholds. Sector-specific threshold sets are the natural next step.
- **Small sectors.** The lens needs at least three peers per sector; with three,
  "weakest" is a crude position. Use larger panels before relying on it.
- **Annual frequency, one lag.** The panel is annual, so a deterioration flag
  needs two years of data and the tool cannot react inside a year. Interim or
  quarterly data would need a different panel and a smaller trigger.
- **n/a is not a pass.** Where a ratio is undefined (negative EBITDA, non-positive
  net worth, zero denominators) the tool refuses to band it and scores a critical
  flag instead. A borrower showing several `n/a` cells should be read as
  "insufficient information", not as "clean".
- **Single entity, single currency.** No group structure, no parent support, no
  consolidation logic, no FX. Amounts are rupee crore throughout.
- **Cash is not restricted-cash adjusted**, so net debt can look better than
  liquidity really is.
- **Ordinal score, no calibration.** The weights and cutoffs are analyst
  judgements, not fitted to a default dataset. Nothing here is a probability of
  default, a rating or a credit decision - it is a screening aid that decides
  what to look at first.

"""Excel workbook writer (openpyxl).

Sheets: Watchlist, one Borrower_Detail sheet per borrower, Signal_Log, Config.
All headers use a dark fill with white bold text, panes are frozen and
column widths are sized to the content.
"""

from __future__ import annotations

import re
from datetime import datetime

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

from .config import config_rows
from .ratios import FINANCIAL_COLUMNS, is_nan
from .scoring import AnalysisResult

DARK = "1F3864"
DARK_FILL = PatternFill("solid", fgColor=DARK)
HEADER_FONT = Font(bold=True, color="FFFFFF", size=10)
TITLE_FONT = Font(bold=True, size=14, color=DARK)
SUB_FONT = Font(italic=True, size=9, color="595959")
BODY_FONT = Font(size=10)
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
SECTION_FILL = PatternFill("solid", fgColor="D9E1F2")

BAND_STYLE = {
    "green": ("C6EFCE", "006100"),
    "amber": ("FFEB9C", "9C6500"),
    "red": ("FFC7CE", "9C0006"),
    "n/a": ("F2F2F2", "808080"),
}

NUM_FORMAT = {"x": "0.00", "pct": "0.0%", "days": "0"}


def _style_header(ws, row: int, ncols: int) -> None:
    for col in range(1, ncols + 1):
        cell = ws.cell(row=row, column=col)
        cell.fill = DARK_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER
    ws.row_dimensions[row].height = 30


def _band_style(cell, band: str | None) -> None:
    fill, font_color = BAND_STYLE.get(str(band).lower(), BAND_STYLE["n/a"])
    cell.fill = PatternFill("solid", fgColor=fill)
    cell.font = Font(size=10, color=font_color, bold=str(band).lower() == "red")


def _autofit(ws, min_width: int = 9, max_width: int = 46) -> None:
    widths: dict[int, int] = {}
    for row in ws.iter_rows():
        for cell in row:
            if cell.value is None:
                continue
            if isinstance(cell.value, float):
                text = f"{cell.value:,.2f}"
            else:
                text = str(cell.value)
            longest = max((len(part) for part in text.split("\n")), default=0)
            widths[cell.column] = max(widths.get(cell.column, 0), longest)
    for col_idx, width in widths.items():
        ws.column_dimensions[get_column_letter(col_idx)].width = max(min_width, min(max_width, width + 2))


def _short_name(borrower: str, max_len: int) -> str:
    """Human-friendly sheet name: drop corporate suffixes, cut on a word boundary."""
    clean = re.sub(r"[^A-Za-z0-9 ]+", " ", borrower)
    clean = re.sub(r"\b(Pvt|Private|Ltd|Limited|LLP|Inc|Co)\b\.?", " ", clean)
    clean = re.sub(r"\s+", " ", clean).strip()
    if len(clean) <= max_len:
        return clean
    cut = clean[:max_len]
    if " " in cut:
        cut = cut.rsplit(" ", 1)[0]
    return cut.strip()


def _sheet_name(borrower: str, index: int, used: set[str]) -> str:
    prefix = f"{index:02d} "
    base = prefix + _short_name(borrower, 31 - len(prefix))
    name = base
    suffix = 1
    while name in used:
        suffix += 1
        tail = f" ({suffix})"
        name = base[: 31 - len(tail)] + tail
    used.add(name)
    return name


def _num_format(unit: str) -> str:
    return NUM_FORMAT.get(unit, "0.00")


def _write_watchlist(ws, result: AnalysisResult, meta: dict) -> None:
    headers = [
        "Rank", "Borrower", "Sector", "Latest FY", "Score", "Band",
        "Red signals", "Amber signals", "Deterioration flags", "Critical data flags",
        "Top tripped signals",
    ]
    ws.append(headers)
    _style_header(ws, 1, len(headers))

    for _, row in result.summary.iterrows():
        ws.append(
            [
                int(row["rank"]),
                row["borrower"],
                row["sector"],
                f"FY{int(row['latest_year'])}",
                float(row["score"]),
                row["band"],
                int(row["red_signals"]),
                int(row["amber_signals"]),
                int(row["deterioration_flags"]),
                int(row["critical_flags"]),
                row["top_signals"],
            ]
        )
        r = ws.max_row
        _band_style(ws.cell(row=r, column=6), row["band"])
        ws.cell(row=r, column=5).number_format = "0.0"
        for col in range(1, len(headers) + 1):
            ws.cell(row=r, column=col).border = BORDER
        ws.cell(row=r, column=11).alignment = Alignment(wrap_text=False)

    ws.freeze_panes = "C2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}{ws.max_row}"

    start = ws.max_row + 3
    ws.cell(row=start, column=1, value="Run metadata").font = TITLE_FONT
    meta_rows = [
        ("Panel", meta.get("panel", "")),
        ("Config applied", meta.get("config", "")),
        ("Generated", meta.get("generated", "")),
        ("Scoring", meta.get("scoring", "")),
        ("Bands", meta.get("bands", "")),
    ]
    for i, (key, value) in enumerate(meta_rows, start=start + 1):
        ws.cell(row=i, column=1, value=key).font = Font(bold=True, size=9)
        cell = ws.cell(row=i, column=2, value=value)
        cell.font = SUB_FONT
        cell.alignment = Alignment(wrap_text=False)

    _autofit(ws)
    ws.column_dimensions["B"].width = 34
    ws.column_dimensions["K"].width = 52


def _write_borrower_detail(ws, result: AnalysisResult, borrower: str, panel=None) -> None:
    cfg = result.cfg
    years = sorted(y for (b, y) in result.records if b == borrower)
    recs = [result.records[(borrower, y)] for y in years]

    ws.cell(row=1, column=1, value=borrower).font = TITLE_FONT
    ws.cell(row=2, column=1, value=f"Sector: {recs[-1].sector}").font = SUB_FONT
    latest = recs[-1]
    ws.cell(
        row=3,
        column=1,
        value=f"Latest score {latest.score:.1f} -> {latest.band.upper()} band "
        f"(FY{years[-1]}). Red {sum(1 for s in latest.signals if s['severity'] == 'red')}, "
        f"amber {sum(1 for s in latest.signals if s['severity'] == 'amber')}, "
        f"deterioration {sum(1 for s in latest.signals if s['signal_type'] == 'deterioration')}.",
    ).font = SUB_FONT

    header_row = 5
    headers = ["Ratio", "Direction"] + [f"FY{y}" for y in years] + ["Latest band", "Latest YoY move", "Deterioration flag"]
    for i, h in enumerate(headers, start=1):
        ws.cell(row=header_row, column=i, value=h)
    _style_header(ws, header_row, len(headers))

    r = header_row + 1
    for key, spec in cfg.ratios.items():
        ws.cell(row=r, column=1, value=spec.label).font = BODY_FONT
        ws.cell(row=r, column=2, value=spec.direction.replace("_", " ")).font = SUB_FONT
        for j, rec in enumerate(recs):
            value = rec.values.get(key)
            cell = ws.cell(row=r, column=3 + j)
            if is_nan(value):
                cell.value = "n/a"
                cell.alignment = Alignment(horizontal="right")
                _band_style(cell, "n/a")
            else:
                cell.value = float(value)
                cell.number_format = _num_format(spec.unit)
                _band_style(cell, rec.bands.get(key))
        band_cell = ws.cell(row=r, column=3 + len(recs), value=latest.bands.get(key) or "n/a")
        _band_style(band_cell, latest.bands.get(key))
        delta = latest.deltas.get(key)
        if is_nan(delta):
            ws.cell(row=r, column=4 + len(recs), value="n/a")
        else:
            dcell = ws.cell(row=r, column=4 + len(recs), value=float(delta))
            dcell.number_format = "+0.00;-0.00;0.00" if spec.unit == "x" else "+0.0%;-0.0%;0.0%"
            if spec.unit == "days":
                dcell.number_format = "+0;-0;0"
        flag = "YES" if latest.deteriorations.get(key) else ""
        fcell = ws.cell(row=r, column=5 + len(recs), value=flag)
        if flag:
            _band_style(fcell, "amber")
            fcell.font = Font(size=10, bold=True, color="9C6500")
        for col in range(1, len(headers) + 1):
            ws.cell(row=r, column=col).border = BORDER
        r += 1

    ws.cell(row=r, column=1, value="Weighted score").font = Font(bold=True, size=10)
    ws.cell(row=r, column=2, value="red 3.0 / amber 1.0 / deterioration 0.5").font = SUB_FONT
    for j, rec in enumerate(recs):
        cell = ws.cell(row=r, column=3 + j, value=float(rec.score))
        cell.number_format = "0.0"
        cell.border = BORDER
    _band_style(ws.cell(row=r, column=3 + len(recs), value=latest.band), latest.band)
    r += 1
    ws.cell(row=r, column=1, value="Borrower band").font = Font(bold=True, size=10)
    for j, rec in enumerate(recs):
        cell = ws.cell(row=r, column=3 + j, value=rec.band)
        _band_style(cell, rec.band)
        cell.border = BORDER

    # ---- inputs
    r += 3
    ws.cell(row=r, column=1, value="Input financials (INR crore)").font = Font(bold=True, size=11, color=DARK)
    r += 1
    input_headers = ["Line item"] + [f"FY{y}" for y in years]
    for i, h in enumerate(input_headers, start=1):
        ws.cell(row=r, column=i, value=h)
    _style_header(ws, r, len(input_headers))
    r += 1
    inputs = {}
    if panel is not None:
        sub = panel[panel["borrower"] == borrower]
        inputs = {int(row["fiscal_year"]): row for _, row in sub.iterrows()}

    for col in FINANCIAL_COLUMNS:
        ws.cell(row=r, column=1, value=col.replace("_", " ").title()).font = BODY_FONT
        for j, year in enumerate(years):
            row = inputs.get(year)
            value = None if row is None else row.get(col)
            cell = ws.cell(row=r, column=2 + j)
            cell.value = None if value is None or is_nan(float(value)) else float(value)
            cell.number_format = "#,##0.00"
            cell.border = BORDER
        ws.cell(row=r, column=1).border = BORDER
        r += 1

    # ---- signals
    r += 2
    ws.cell(row=r, column=1, value="Signals in the latest year").font = Font(bold=True, size=11, color=DARK)
    r += 1
    sig_headers = ["Signal type", "Ratio", "Value", "Prior", "Change", "Severity", "Weight", "Detail"]
    for i, h in enumerate(sig_headers, start=1):
        ws.cell(row=r, column=i, value=h)
    _style_header(ws, r, len(sig_headers))
    r += 1
    for sig in latest.signals:
        ws.cell(row=r, column=1, value=sig["signal_type"]).font = BODY_FONT
        ws.cell(row=r, column=2, value=sig["label"]).font = BODY_FONT
        for col, key in ((3, "value"), (4, "prior_value"), (5, "delta")):
            value = sig[key]
            cell = ws.cell(row=r, column=col)
            cell.value = "n/a" if is_nan(value) else float(value)
            cell.number_format = "0.00"
        _band_style(ws.cell(row=r, column=6, value=sig["severity"]), sig["severity"] if sig["severity"] in BAND_STYLE else "amber")
        ws.cell(row=r, column=7, value=float(sig["weight"])).number_format = "0.0"
        ws.cell(row=r, column=8, value=sig["detail"]).font = BODY_FONT
        for col in range(1, len(sig_headers) + 1):
            ws.cell(row=r, column=col).border = BORDER
        r += 1

    ws.freeze_panes = f"C{header_row + 1}"
    _autofit(ws)
    ws.column_dimensions["A"].width = 40
    ws.column_dimensions[get_column_letter(3 + len(recs))].width = 13


def _write_signal_log(ws, result: AnalysisResult) -> None:
    headers = [
        "Borrower", "Sector", "Fiscal year", "Ratio", "Signal", "Type",
        "Value", "Prior value", "Change", "Band", "Severity", "Weight", "Detail",
    ]
    ws.append(headers)
    _style_header(ws, 1, len(headers))
    for _, row in result.signals.iterrows():
        ws.append(
            [
                row["borrower"],
                row["sector"],
                f"FY{int(row['fiscal_year'])}",
                row["ratio"],
                row["label"],
                row["signal_type"],
                None if is_nan(row["value"]) else float(row["value"]),
                None if is_nan(row["prior_value"]) else float(row["prior_value"]),
                None if is_nan(row["delta"]) else float(row["delta"]),
                row["band"],
                row["severity"],
                float(row["weight"]),
                row["detail"],
            ]
        )
        r = ws.max_row
        _band_style(ws.cell(row=r, column=11), "red" if row["severity"] in ("red", "critical") else "amber")
        _band_style(ws.cell(row=r, column=10), row["band"] if row["band"] in BAND_STYLE else "n/a")
        for col in (7, 8, 9):
            ws.cell(row=r, column=col).number_format = "0.00"
        ws.cell(row=r, column=12).number_format = "0.0"
        for col in range(1, len(headers) + 1):
            ws.cell(row=r, column=col).border = BORDER
    ws.freeze_panes = "C2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}{ws.max_row}"
    _autofit(ws)
    ws.column_dimensions["A"].width = 32
    ws.column_dimensions["E"].width = 38
    ws.column_dimensions["M"].width = 60


def _write_config(ws, result: AnalysisResult, meta: dict) -> None:
    headers = [
        "Ratio", "Label", "Direction", "Unit", "Green threshold", "Amber threshold",
        "Deterioration trigger", "Weight if red", "Weight if amber", "Weight if deterioration",
    ]
    ws.append(headers)
    _style_header(ws, 1, len(headers))
    for row in config_rows(result.cfg):
        ws.append(
            [
                row["ratio"],
                row["label"],
                row["direction"],
                row["unit"],
                row["green_threshold"],
                row["amber_threshold"],
                row["deterioration_trigger"],
                row["weight_if_red"],
                row["weight_if_amber"],
                row["weight_if_deterioration"],
            ]
        )
        r = ws.max_row
        unit = row["unit"]
        for col in (5, 6, 7):
            ws.cell(row=r, column=col).number_format = _num_format(unit)
        for col in (8, 9, 10):
            ws.cell(row=r, column=col).number_format = "0.0"
        for col in range(1, len(headers) + 1):
            ws.cell(row=r, column=col).border = BORDER

    r = ws.max_row + 3
    ws.cell(row=r, column=1, value="Scoring and banding").font = Font(bold=True, size=11, color=DARK)
    score = result.cfg.score
    rows = [
        ("red_weight", score.red_weight),
        ("amber_weight", score.amber_weight),
        ("deterioration_weight", score.deterioration_weight),
        ("deterioration_counts_when_red", str(score.deterioration_counts_when_red)),
        ("red_min_score", score.red_min_score),
        ("amber_min_score", score.amber_min_score),
        ("config_source", meta.get("config", "")),
        ("config_version", str(result.cfg.version)),
    ]
    for key, value in rows:
        r += 1
        ws.cell(row=r, column=1, value=key).font = BODY_FONT
        cell = ws.cell(row=r, column=2, value=value)
        cell.font = BODY_FONT

    ws.freeze_panes = "A2"
    _autofit(ws)
    ws.column_dimensions["B"].width = 44
    ws.column_dimensions["C"].width = 20


def _write_sector_view(ws, view) -> None:
    from .sector import HIDDEN, SECTOR_WIDE
    ws.cell(1, 1, 'Sector-relative view (latest year per borrower)').font = Font(bold=True, size=12)
    ws.cell(2, 1, 'Each ratio against the median of the same sector in this panel. Views: agrees / hidden relative weakness / sector-wide level / too few peers.')
    cols = ['borrower', 'sector', 'fiscal_year', 'label', 'value', 'absolute_band', 'sector_median', 'gap_to_median_adverse', 'peers', 'rank_in_sector', 'view']
    for c, h in enumerate(cols, 1):
        ws.cell(4, c, h.replace('_', ' '))
    _style_header(ws, 4, len(cols))
    for r, (_, row) in enumerate(view.iterrows(), 5):
        for c, k in enumerate(cols, 1):
            val = row[k]
            cell = ws.cell(r, c, None if (isinstance(val, float) and val != val) else val)
            if k in ('value', 'sector_median', 'gap_to_median_adverse') and isinstance(val, float):
                cell.number_format = '0.00'
        if row['view'] in (HIDDEN, SECTOR_WIDE):
            for c in range(1, len(cols) + 1):
                ws.cell(r, c).fill = PatternFill('solid', fgColor='FFF2CC')
    _autofit(ws)


def write_workbook(result: AnalysisResult, path: str, meta: dict | None = None, panel=None, sector=None) -> str:
    meta = dict(meta or {})
    meta.setdefault("generated", datetime.now().strftime("%d-%b-%Y %H:%M"))
    cfg = result.cfg
    meta.setdefault(
        "scoring",
        f"red {cfg.score.red_weight} / amber {cfg.score.amber_weight} / "
        f"deterioration {cfg.score.deterioration_weight}",
    )
    meta.setdefault(
        "bands",
        f"red at score >= {cfg.score.red_min_score}, amber at score >= {cfg.score.amber_min_score}",
    )

    wb = Workbook()
    watch = wb.active
    watch.title = "Watchlist"
    _write_watchlist(watch, result, meta)

    used = {"Watchlist", "Signal_Log", "Config", "Sector_View"}
    for i, borrower in enumerate(result.summary["borrower"].tolist(), start=1):
        name = _sheet_name(borrower, i, used)
        ws = wb.create_sheet(name)
        _write_borrower_detail(ws, result, borrower, panel)

    _write_signal_log(wb.create_sheet("Signal_Log"), result)
    if sector is not None and not sector.empty:
        _write_sector_view(wb.create_sheet("Sector_View"), sector)
    _write_config(wb.create_sheet("Config"), result, meta)

    wb.properties.title = "Credit Early-Warning Monitor"
    wb.properties.creator = "Credit Early-Warning Monitor"
    wb.save(path)
    return path

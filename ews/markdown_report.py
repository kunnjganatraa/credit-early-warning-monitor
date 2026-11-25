"""Markdown summary report."""

from __future__ import annotations

from datetime import datetime

import pandas as pd

from .ratios import is_nan
from .scoring import AnalysisResult, top_signals_by_frequency


def _fmt(value: float, unit: str) -> str:
    if is_nan(value):
        return "n/a"
    if unit == "pct":
        return f"{value * 100:.1f}%"
    if unit == "days":
        return f"{value:.0f}"
    return f"{value:.2f}"


def _band_badge(band: str) -> str:
    return {"red": "RED", "amber": "AMBER", "green": "GREEN"}.get(str(band).lower(), "n/a")


def build_markdown(result: AnalysisResult, meta: dict | None = None, sector=None) -> str:
    meta = dict(meta or {})
    cfg = result.cfg
    summary = result.summary
    latest_year = int(summary["latest_year"].max())
    counts = summary["band"].value_counts().to_dict()

    lines: list[str] = []
    lines.append("# Credit Early-Warning Monitor - Portfolio Summary")
    lines.append("")
    lines.append(f"- Generated: {meta.get('generated', datetime.now().strftime('%d-%b-%Y %H:%M'))}")
    lines.append(f"- Panel: `{meta.get('panel', 'data/borrower_panel.csv')}`")
    lines.append(f"- Config applied: `{meta.get('config', 'config/thresholds.yaml')}`")
    lines.append(f"- Borrowers: {len(summary)} | Latest fiscal year in panel: FY{latest_year}")
    lines.append(
        f"- Bands: {counts.get('red', 0)} red, {counts.get('amber', 0)} amber, {counts.get('green', 0)} green"
    )
    lines.append("")
    lines.append(
        "Scoring: each red level signal counts "
        f"{cfg.score.red_weight:g}, each amber level signal {cfg.score.amber_weight:g}, "
        f"each deterioration flag {cfg.score.deterioration_weight:g}. "
        f"Red band at score >= {cfg.score.red_min_score:g}, amber at score >= {cfg.score.amber_min_score:g}."
    )
    lines.append("")
    lines.append("## 1. Ranking (worst first)")
    lines.append("")
    lines.append("| Rank | Borrower | Sector | Score | Band | Red | Amber | Deterioration | Top tripped signals |")
    lines.append("| ---: | --- | --- | ---: | --- | ---: | ---: | ---: | --- |")
    for _, row in summary.iterrows():
        lines.append(
            f"| {int(row['rank'])} | {row['borrower']} | {row['sector']} | {row['score']:.1f} | "
            f"{_band_badge(row['band'])} | {int(row['red_signals'])} | {int(row['amber_signals'])} | "
            f"{int(row['deterioration_flags'])} | {row['top_signals']} |"
        )
    lines.append("")

    lines.append(f"## 2. Top signals by frequency (FY{latest_year})")
    lines.append("")
    freq = top_signals_by_frequency(result.signals, latest_only=True, n=3)
    if not freq:
        lines.append("No signals tripped in the latest year.")
    else:
        lines.append("| # | Signal | Times tripped |")
        lines.append("| ---: | --- | ---: |")
        for i, (label, count) in enumerate(freq, start=1):
            lines.append(f"| {i} | {label} | {count} |")
    lines.append("")
    all_freq = top_signals_by_frequency(result.signals, latest_only=False, n=3)
    if all_freq:
        lines.append(
            "Across the whole panel history (all years), the most frequent signals are: "
            + ", ".join(f"{label} ({count})" for label, count in all_freq)
            + "."
        )
        lines.append("")

    lines.append("## 3. Borrower detail")
    lines.append("")
    for _, row in summary.iterrows():
        borrower = row["borrower"]
        rec = result.records[(borrower, int(row["latest_year"]))]
        lines.append(f"### {int(row['rank'])}. {borrower} - {_band_badge(row['band'])} (score {row['score']:.1f})")
        lines.append("")
        lines.append(f"- Sector: {row['sector']}; latest year FY{int(row['latest_year'])}")
        level = [s for s in rec.signals if s["signal_type"] == "level"]
        if level:
            lines.append("- Level signals: " + "; ".join(s["detail"] for s in level))
        else:
            lines.append("- Level signals: none - every ratio is inside the green band")
        det = [s for s in rec.signals if s["signal_type"] == "deterioration"]
        if det:
            lines.append("- Deterioration (year on year): " + "; ".join(s["detail"] for s in det))
        crit = [s for s in rec.signals if s["signal_type"] == "data_flag"]
        if crit:
            lines.append("- Data flags: " + "; ".join(s["detail"] for s in crit))
        lines.append("")
        lines.append("| Ratio | " + " | ".join(f"FY{y}" for y in sorted(
            y for (b, y) in result.records if b == borrower)) + " | Band |")
        years = sorted(y for (b, y) in result.records if b == borrower)
        lines.append("| --- | " + " | ".join("---:" for _ in years) + " | --- |")
        for key, spec in cfg.ratios.items():
            cells = [_fmt(result.records[(borrower, y)].values.get(key), spec.unit) for y in years]
            lines.append(
                f"| {spec.label} | " + " | ".join(cells) + f" | {_band_badge(rec.bands.get(key) or 'n/a')} |"
            )
        lines.append("")

    if sector is not None and not sector.empty:
        from .sector import disagreements
        dis = disagreements(sector)
        lines.append("## 4. Sector-relative view: where absolute bands and peers disagree")
        lines.append("")
        lines.append(
            "Each borrower's latest ratios against the median of its own sector in this panel "
            "(minimum three peers). *Hidden relative weakness*: green on absolute thresholds but the weakest in "
            "the sector by at least the deterioration trigger. *Sector-wide level*: amber or red on absolute "
            "thresholds but at or better than the sector median."
        )
        lines.append("")
        if dis.empty:
            lines.append("No disagreements in the latest year.")
        else:
            lines.append("| Borrower | Sector | Ratio | Value | Absolute band | Sector median | Rank | View |")
            lines.append("| --- | --- | --- | ---: | --- | ---: | --- | --- |")
            for _, r in dis.iterrows():
                spec = cfg.spec(r["ratio"])
                lines.append(
                    f"| {r['borrower']} | {r['sector']} | {spec.label} | {_fmt(r['value'], spec.unit)} | "
                    f"{r['absolute_band']} | {_fmt(r['sector_median'], spec.unit)} | {r['rank_in_sector']} | {r['view']} |"
                )
        lines.append("")
    lines.append("## 5. How to read this report" if sector is not None and not sector.empty else "## 4. How to read this report")
    lines.append("")
    lines.append(
        "A level signal means the ratio is outside its green band in the latest year. "
        "A deterioration signal means the ratio moved against the borrower by more than the "
        "configured trigger in one year, even if the level is still inside a green or amber band - "
        "this is the early part of the early-warning system."
    )
    lines.append("")
    lines.append(
        "Ratios shown as n/a are undefined (zero denominator) or not meaningful (negative EBITDA or "
        "non-positive net worth). Those cases raise an explicit data flag instead of an infinity."
    )
    lines.append("")
    lines.append(
        "See README.md for formulas, threshold defaults and limitations. This report is an analytical "
        "screen, not a credit decision."
    )
    lines.append("")
    return "\n".join(lines)


def write_markdown(result: AnalysisResult, path: str, meta: dict | None = None, sector=None) -> str:
    text = build_markdown(result, meta, sector)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path

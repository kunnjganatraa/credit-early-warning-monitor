#!/usr/bin/env python3
"""Command line entry point for the Credit Early-Warning Monitor.

    python cli.py --panel data/borrower_panel.csv \
                  --config config/thresholds.yaml \
                  --out output/
"""

from __future__ import annotations

import argparse
import os
import sys

from ews.config import ConfigError, load_config
from ews.excel_report import write_workbook
from ews.markdown_report import write_markdown
from ews.panel import PanelError, load_panel
from ews.scoring import evaluate, top_signals_by_frequency
from ews.sector import disagreements, sector_view

WORKBOOK_NAME = "early_warning_report.xlsx"
MARKDOWN_NAME = "early_warning_summary.md"
CHART_NAME = "score_by_borrower.png"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="credit-early-warning-monitor",
        description=(
            "Score a borrower panel on credit ratios, band each ratio green/amber/red "
            "and flag year-on-year deterioration."
        ),
    )
    parser.add_argument("--panel", required=True, help="CSV panel of borrower financials (one row per borrower-year)")
    parser.add_argument("--config", required=True, help="threshold config file (.yaml or .json)")
    parser.add_argument("--out", default="output", help="output directory (default: output/)")
    parser.add_argument("--no-chart", action="store_true", help="skip the PNG score chart")
    parser.add_argument("--quiet", action="store_true", help="suppress the console summary")
    parser.add_argument("--min-peers", type=int, default=3, help="minimum borrowers per sector for the sector-relative view (default 3)")
    return parser


def _print_summary(result, out_paths: dict) -> None:
    summary = result.summary
    counts = summary["band"].value_counts().to_dict()
    print("")
    print("Credit Early-Warning Monitor")
    print("=" * 96)
    print(
        f"{'Rank':>4}  {'Band':<6} {'Score':>6}  {'Borrower':<34} {'Red':>4} {'Amber':>5} {'Det':>4}  Top signal"
    )
    print("-" * 96)
    for _, row in summary.iterrows():
        top = row["top_signals"].split(";")[0].strip()
        print(
            f"{int(row['rank']):>4}  {row['band'].upper():<6} {row['score']:>6.1f}  {row['borrower'][:34]:<34} "
            f"{int(row['red_signals']):>4} {int(row['amber_signals']):>5} {int(row['deterioration_flags']):>4}  {top}"
        )
    print("-" * 96)
    print(
        f"Bands: {counts.get('red', 0)} red, {counts.get('amber', 0)} amber, {counts.get('green', 0)} green "
        f"| signals logged: {len(result.signals)}"
    )
    freq = top_signals_by_frequency(result.signals, latest_only=True, n=3)
    if freq:
        print("Top signals by frequency (latest year): " + ", ".join(f"{label} ({count})" for label, count in freq))
    print("")
    for label, path in out_paths.items():
        print(f"  {label:<10} {path}")
    print("")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        cfg = load_config(args.config)
        panel = load_panel(args.panel)
    except (ConfigError, PanelError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    result = evaluate(panel, cfg)
    sector = sector_view(result.ratio_history, cfg, min_peers=args.min_peers)
    os.makedirs(args.out, exist_ok=True)

    meta = {
        "panel": args.panel,
        "config": args.config,
        "scoring": (
            f"red {cfg.score.red_weight:g} / amber {cfg.score.amber_weight:g} / "
            f"deterioration {cfg.score.deterioration_weight:g}"
        ),
        "bands": (
            f"red at score >= {cfg.score.red_min_score:g}, amber at score >= {cfg.score.amber_min_score:g}"
        ),
    }

    out_paths: dict[str, str] = {}
    workbook = write_workbook(result, os.path.join(args.out, WORKBOOK_NAME), meta=meta, panel=panel, sector=sector)
    out_paths["workbook"] = workbook
    out_paths["summary"] = write_markdown(result, os.path.join(args.out, MARKDOWN_NAME), meta=meta, sector=sector)

    if not args.no_chart:
        try:
            from ews.charts import write_score_chart

            out_paths["chart"] = write_score_chart(result, os.path.join(args.out, CHART_NAME))
        except Exception as exc:  # charting must never break the run
            print(f"warning: score chart skipped ({exc})", file=sys.stderr)

    if not args.quiet:
        _print_summary(result, out_paths)
        dis = disagreements(sector)
        if not dis.empty:
            print(f"Sector-relative disagreements (latest year): {len(dis)}")
            for _, r in dis.iterrows():
                print(f"  {r['borrower'][:30]:<30} {r['label'][:36]:<36} {r['absolute_band']:<6} {r['rank_in_sector']:<7} {r['view']}")
            print("")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

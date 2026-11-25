"""Outputs: Excel workbook structure, markdown report and the CLI."""

from __future__ import annotations

import subprocess
import sys

from openpyxl import load_workbook

from conftest import CONFIG_PATH, PANEL_PATH, ROOT
from ews.excel_report import write_workbook
from ews.markdown_report import build_markdown, write_markdown

DARK = "1F3864"


def test_workbook_has_expected_sheets(tmp_path, result, panel):
    path = tmp_path / "book.xlsx"
    write_workbook(result, str(path), panel=panel)
    wb = load_workbook(path)
    names = wb.sheetnames
    assert names[0] == "Watchlist"
    assert "Signal_Log" in names
    assert names[-1] == "Config"
    # one detail sheet per borrower
    detail = [n for n in names if n not in ("Watchlist", "Signal_Log", "Config")]
    assert len(detail) == len(result.summary) == 6
    assert all(len(n) <= 31 for n in names)


def test_workbook_headers_are_dark_with_white_bold_text(tmp_path, result, panel):
    path = tmp_path / "book.xlsx"
    write_workbook(result, str(path), panel=panel)
    wb = load_workbook(path)
    for sheet in ("Watchlist", "Signal_Log", "Config"):
        ws = wb[sheet]
        cell = ws.cell(row=1, column=1)
        assert cell.value is not None
        assert str(cell.fill.fgColor.rgb).upper().endswith(DARK)
        assert cell.font.bold is True
        assert str(cell.font.color.rgb).upper().endswith("FFFFFF")


def test_workbook_panes_frozen_and_widths_set(tmp_path, result, panel):
    path = tmp_path / "book.xlsx"
    write_workbook(result, str(path), panel=panel)
    wb = load_workbook(path)
    for ws in wb.worksheets:
        assert ws.freeze_panes is not None, ws.title
        assert ws.column_dimensions["A"].width >= 9, ws.title


def test_watchlist_is_ranked_worst_first(tmp_path, result, panel):
    path = tmp_path / "book.xlsx"
    write_workbook(result, str(path), panel=panel)
    ws = load_workbook(path)["Watchlist"]
    rows = [[ws.cell(row=r, column=c).value for c in range(1, 7)] for r in range(2, 8)]
    assert [r[0] for r in rows] == [1, 2, 3, 4, 5, 6]
    scores = [r[4] for r in rows]
    assert scores == sorted(scores, reverse=True)
    assert rows[0][5] == "red"
    assert rows[0][1] == "Deccan Auto Components Pvt Ltd"
    assert rows[0][2] == "Auto components"


def test_signal_log_lists_every_signal(tmp_path, result, panel):
    path = tmp_path / "book.xlsx"
    write_workbook(result, str(path), panel=panel)
    ws = load_workbook(path)["Signal_Log"]
    assert ws.max_row - 1 == len(result.signals)
    header = [ws.cell(row=1, column=c).value for c in range(1, 14)]
    for expected in ("Borrower", "Fiscal year", "Signal", "Value", "Severity", "Weight"):
        assert expected in header


def test_config_sheet_shows_applied_thresholds(tmp_path, result, panel):
    path = tmp_path / "book.xlsx"
    write_workbook(result, str(path), panel=panel)
    ws = load_workbook(path)["Config"]
    ratios = {}
    for r in range(2, 14):
        ratios[ws.cell(row=r, column=1).value] = ws.cell(row=r, column=5).value
    assert len(ratios) == 12
    assert ratios["net_debt_ebitda"] == 3.0
    assert ratios["interest_coverage"] == 2.5
    assert ratios["receivable_days"] == 60


def test_borrower_detail_holds_full_ratio_history(tmp_path, result, panel):
    path = tmp_path / "book.xlsx"
    write_workbook(result, str(path), panel=panel)
    wb = load_workbook(path)
    ws = wb["01 Deccan Auto Components"]
    header = [ws.cell(row=5, column=c).value for c in range(1, 10)]
    assert header[2:6] == ["FY2022", "FY2023", "FY2024", "FY2025"]
    labels = [ws.cell(row=r, column=1).value for r in range(6, 18)]
    assert "Net debt / EBITDA" in labels
    assert len(labels) == 12
    # FY2025 interest coverage for Deccan, straight from the panel
    row_idx = 6 + labels.index("Interest coverage (EBITDA / interest)")
    assert round(ws.cell(row=row_idx, column=6).value, 4) == round(44.85 / 68, 4)


def test_markdown_report_ranks_borrowers_and_names_top_signals(result):
    text = build_markdown(result, {"panel": "data/borrower_panel.csv", "config": "config/thresholds.yaml"})
    assert "# Credit Early-Warning Monitor" in text
    assert "## 1. Ranking (worst first)" in text
    assert "## 2. Top signals by frequency" in text
    for borrower in result.summary["borrower"]:
        assert borrower in text
    first = result.summary.iloc[0]["borrower"]
    assert text.index(first) < text.index(result.summary.iloc[-1]["borrower"])
    # guard: generated files must never carry chat citation markers
    assert ("[ci" + "te:") not in text
    assert "2 red, 2 amber, 2 green" in text


def test_markdown_written_to_disk(tmp_path, result):
    path = tmp_path / "summary.md"
    write_markdown(result, str(path))
    assert path.exists()
    assert "Borrower detail" in path.read_text(encoding="utf-8")


def test_cli_end_to_end(tmp_path):
    out = tmp_path / "out"
    proc = subprocess.run(
        [sys.executable, "cli.py", "--panel", str(PANEL_PATH), "--config", str(CONFIG_PATH),
         "--out", str(out)],
        cwd=str(ROOT), capture_output=True, text=True, timeout=180,
    )
    assert proc.returncode == 0, proc.stderr
    assert "2 red, 2 amber, 2 green" in proc.stdout
    assert (out / "early_warning_report.xlsx").exists()
    assert (out / "early_warning_summary.md").exists()
    assert (out / "score_by_borrower.png").exists()


def test_cli_rejects_a_bad_panel(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text("borrower,sector,fiscal_year\nOnly,Three,2025\n", encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, "cli.py", "--panel", str(bad), "--config", str(CONFIG_PATH),
         "--out", str(tmp_path / "out")],
        cwd=str(ROOT), capture_output=True, text=True, timeout=180,
    )
    assert proc.returncode == 2
    assert "error:" in proc.stderr

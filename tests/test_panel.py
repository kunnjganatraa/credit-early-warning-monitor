"""Panel validation."""

from __future__ import annotations

import pandas as pd
import pytest

from conftest import PANEL_PATH
from ews.panel import PanelError, load_panel, validate_panel


def test_shipped_panel_loads_with_expected_shape(panel):
    assert panel.shape == (24, 19)  # 17 required + 2 optional columns added as blank
    assert panel["borrower"].nunique() == 6
    assert sorted(panel["fiscal_year"].unique()) == [2022, 2023, 2024, 2025]
    assert panel.groupby("borrower").size().eq(4).all()


def test_missing_column_raises(tmp_path):
    df = pd.read_csv(PANEL_PATH).drop(columns=["cfo"])
    path = tmp_path / "bad.csv"
    df.to_csv(path, index=False)
    with pytest.raises(PanelError) as exc:
        load_panel(str(path))
    assert "cfo" in str(exc.value)


def test_non_numeric_amount_raises(tmp_path):
    lines = PANEL_PATH.read_text(encoding="utf-8").splitlines()
    cells = lines[1].split(",")
    cells[3] = "not a number"  # revenue of the first row
    lines[1] = ",".join(cells)
    path = tmp_path / "bad.csv"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    with pytest.raises(PanelError) as exc:
        load_panel(str(path))
    assert "non-numeric" in str(exc.value)


def test_duplicate_borrower_year_raises(tmp_path):
    df = pd.read_csv(PANEL_PATH)
    df = pd.concat([df, df.iloc[[0]]], ignore_index=True)
    path = tmp_path / "dup.csv"
    df.to_csv(path, index=False)
    with pytest.raises(PanelError) as exc:
        load_panel(str(path))
    assert "duplicate" in str(exc.value)


def test_extra_columns_are_dropped(panel):
    extra = panel.copy()
    extra["unused_note"] = "x"
    cleaned = validate_panel(extra)
    assert "unused_note" not in cleaned.columns


def test_missing_panel_file_raises():
    with pytest.raises(PanelError):
        load_panel("no/such/panel.csv")


def test_optional_columns_are_added_blank_when_absent():
    df = pd.read_csv(PANEL_PATH)
    assert "scheduled_principal" not in df.columns
    out = validate_panel(df)
    assert out["scheduled_principal"].isna().all()
    assert out["cogs"].isna().all()


def test_optional_columns_are_kept_and_coerced_when_present():
    df = pd.read_csv(PANEL_PATH)
    df["scheduled_principal"] = 25
    df["cogs"] = "600"
    out = validate_panel(df)
    assert (out["scheduled_principal"] == 25.0).all()
    assert (out["cogs"] == 600.0).all()

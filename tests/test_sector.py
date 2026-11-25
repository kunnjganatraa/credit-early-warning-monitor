"""Sector-relative lens."""

from __future__ import annotations

import math

import pandas as pd
import pytest

from conftest import row
from ews.panel import validate_panel
from ews.scoring import evaluate
from ews.sector import AGREES, HIDDEN, SECTOR_WIDE, TOO_FEW, disagreements, sector_view


def _panel(rows):
    return validate_panel(pd.DataFrame(rows))


def _three_peers(debt_a, debt_b, debt_c, sector="Cement"):
    # EBITDA 200 and cash 50 for all, so net debt / EBITDA = (debt - 50) / 200
    return _panel([
        row(borrower="A", sector=sector, total_debt=debt_a),
        row(borrower="B", sector=sector, total_debt=debt_b),
        row(borrower="C", sector=sector, total_debt=debt_c),
    ])


def _view_for(view, borrower, ratio):
    r = view[(view["borrower"] == borrower) & (view["ratio"] == ratio)]
    assert len(r) == 1
    return r.iloc[0]


def test_green_but_weakest_by_more_than_trigger_is_hidden_weakness(cfg):
    # leverage 0.75x, 1.00x, 2.25x: all green (<= 3.0x); C is 1.25x worse than the 1.00x median
    view = sector_view(evaluate(_three_peers(200, 250, 500), cfg).ratio_history, cfg)
    c = _view_for(view, "C", "net_debt_ebitda")
    assert c["absolute_band"] == "green"
    assert c["rank_in_sector"] == "3 of 3"
    assert c["sector_median"] == pytest.approx(1.0)
    assert c["gap_to_median_adverse"] == pytest.approx(1.25)
    assert c["view"] == HIDDEN


def test_weakest_but_within_trigger_of_median_agrees(cfg):
    # 0.75x, 1.00x, 1.25x: C is weakest but only 0.25x worse (trigger is 0.50x)
    view = sector_view(evaluate(_three_peers(200, 250, 300), cfg).ratio_history, cfg)
    assert _view_for(view, "C", "net_debt_ebitda")["view"] == AGREES


def test_amber_at_or_better_than_median_is_sector_wide_level(cfg):
    # 3.25x, 3.50x, 4.00x: all amber; A and B are at or better than the 3.50x median
    view = sector_view(evaluate(_three_peers(700, 750, 850), cfg).ratio_history, cfg)
    assert _view_for(view, "A", "net_debt_ebitda")["view"] == SECTOR_WIDE
    assert _view_for(view, "B", "net_debt_ebitda")["view"] == SECTOR_WIDE
    assert _view_for(view, "C", "net_debt_ebitda")["view"] == AGREES
    assert len(disagreements(view)) >= 2


def test_too_few_peers_takes_no_view(cfg):
    panel = _panel([row(borrower="A", sector="Pharma"), row(borrower="B", sector="Pharma")])
    view = sector_view(evaluate(panel, cfg).ratio_history, cfg)
    assert set(view["view"]) == {TOO_FEW}


def test_uses_latest_year_only(cfg):
    rows = [row(borrower=b, sector="X", fiscal_year=y, total_debt=d)
            for b, d in (("A", 200), ("B", 250), ("C", 500)) for y in (2024, 2025)]
    view = sector_view(evaluate(_panel(rows), cfg).ratio_history, cfg)
    assert set(view["fiscal_year"]) == {2025}


def test_nan_ratio_is_skipped_not_ranked(cfg):
    panel = _three_peers(200, 250, 500)
    panel.loc[panel["borrower"] == "C", "ebitda"] = -10.0  # leverage undefined for C
    view = sector_view(evaluate(panel, cfg).ratio_history, cfg)
    lev = view[view["ratio"] == "net_debt_ebitda"]
    assert "C" not in set(lev["borrower"])
    assert set(lev["view"]) == {TOO_FEW}  # only two valid peers remain

"""Ratio maths: hand-computed values, negative EBITDA, zero denominators."""

from __future__ import annotations

import math

import pytest

from conftest import row
from ews.config import load_config
from ews.ratios import (F_NEG_EBITDA, F_NEG_NET_WORTH, F_NO_PRIOR, F_NO_SCHEDULE, F_REVENUE_BASIS,
                        F_ZERO_DENOMINATOR, compute_ratios)
from ews.scoring import assign_band


def codes(res) -> set[str]:
    return {flag["code"] for flag in res.flags}


def test_hand_computed_ratios_on_clean_row(cfg):
    """Every ratio checked against arithmetic done by hand.

    revenue 1000, ebitda 200, pat 80, interest 50, debt 400, net worth 500,
    current assets 300, current liabilities 200, inventory 100,
    receivables 120, cash 50, cfo 150, contingent 100, prior revenue 800.
    """
    current = row()
    prior = row(fiscal_year=2024, revenue=800.0)
    res = compute_ratios(current, prior, cfg)

    assert res.values["net_debt_ebitda"] == pytest.approx((400 - 50) / 200)  # 1.75
    assert res.values["interest_coverage"] == pytest.approx(200 / 50)  # 4.00
    assert res.values["dscr_proxy"] == pytest.approx(150 / 50)  # 3.00
    assert res.values["current_ratio"] == pytest.approx(300 / 200)  # 1.50
    assert res.values["quick_ratio"] == pytest.approx((300 - 100) / 200)  # 1.00
    assert res.values["tol_tnw"] == pytest.approx((400 + 100) / 500)  # 1.00
    assert res.values["cfo_to_debt"] == pytest.approx(150 / 400)  # 0.375
    assert res.values["ebitda_margin"] == pytest.approx(200 / 1000)  # 0.20
    assert res.values["revenue_growth"] == pytest.approx(200 / 800)  # 0.25
    assert res.values["receivable_days"] == pytest.approx(120 / 1000 * 365)  # 43.8
    assert res.values["inventory_days"] == pytest.approx(100 / 1000 * 365)  # 36.5
    assert res.values["pat_to_networth"] == pytest.approx(80 / 500)  # 0.16
    # no principal schedule and no COGS in the base row: both are flagged, never guessed
    assert codes(res) == {F_NO_SCHEDULE, F_REVENUE_BASIS}
    assert math.isnan(res.values["dscr"])
    assert res.derived["net_debt"] == pytest.approx(350.0)


def test_hand_computed_ratios_from_sample_panel(cfg):
    """Deccan Auto Components FY2025 straight from the shipped CSV."""
    fin = {
        "revenue": 690, "ebitda": 44.85, "pat": -34, "interest_expense": 68,
        "total_debt": 745, "net_worth": 262, "current_assets": 275,
        "current_liabilities": 265, "inventory": 124, "receivables": 170,
        "cash": 10, "cfo": -12, "contingent_liabilities": 95,
    }
    prior = {"revenue": 745, "ebitda": 67.05, "pat": -8, "interest_expense": 62,
             "total_debt": 700, "net_worth": 288, "current_assets": 300,
             "current_liabilities": 255, "inventory": 128, "receivables": 178,
             "cash": 12, "cfo": 8, "contingent_liabilities": 85}
    res = compute_ratios(fin, prior, cfg)

    assert res.values["net_debt_ebitda"] == pytest.approx(735 / 44.85)
    assert res.values["interest_coverage"] == pytest.approx(44.85 / 68)
    assert res.values["dscr_proxy"] == pytest.approx(-12 / 68)
    assert res.values["tol_tnw"] == pytest.approx((745 + 95) / 262)
    assert res.values["receivable_days"] == pytest.approx(170 / 690 * 365)
    assert res.values["pat_to_networth"] == pytest.approx(-34 / 262)
    assert res.values["revenue_growth"] == pytest.approx((690 - 745) / 745)


def test_negative_ebitda_returns_nan_and_flags(cfg):
    """Negative EBITDA must never produce an infinity."""
    res = compute_ratios(row(ebitda=-18.0), row(fiscal_year=2024, revenue=800.0, ebitda=25.0), cfg)

    assert math.isnan(res.values["net_debt_ebitda"])
    assert math.isnan(res.values["interest_coverage"])
    assert F_NEG_EBITDA in codes(res)
    assert all(not math.isinf(v) for v in res.values.values() if v == v)
    # ratios that do not depend on EBITDA are still computed
    assert res.values["current_ratio"] == pytest.approx(1.5)
    assert res.values["pat_to_networth"] == pytest.approx(0.16)


def test_zero_ebitda_is_treated_as_negative(cfg):
    res = compute_ratios(row(ebitda=0.0), None, cfg)
    assert math.isnan(res.values["net_debt_ebitda"])
    assert F_NEG_EBITDA in codes(res)


def test_zero_net_worth_returns_nan_and_flags(cfg):
    res = compute_ratios(row(net_worth=0.0), None, cfg)
    assert math.isnan(res.values["tol_tnw"])
    assert math.isnan(res.values["pat_to_networth"])
    assert F_NEG_NET_WORTH in codes(res)
    assert all(not math.isinf(v) for v in res.values.values() if v == v)


def test_negative_net_worth_returns_nan_and_flags(cfg):
    res = compute_ratios(row(net_worth=-150.0), None, cfg)
    assert math.isnan(res.values["tol_tnw"])
    assert math.isnan(res.values["pat_to_networth"])
    assert F_NEG_NET_WORTH in codes(res)


def test_zero_denominators_flag_instead_of_infinity(cfg):
    res = compute_ratios(row(interest_expense=0.0, current_liabilities=0.0, total_debt=0.0), None, cfg)

    for key in ("interest_coverage", "dscr_proxy", "current_ratio", "quick_ratio", "cfo_to_debt"):
        assert math.isnan(res.values[key]), key
    assert F_ZERO_DENOMINATOR in codes(res)
    flagged = {f["ratio"] for f in res.flags if f["code"] == F_ZERO_DENOMINATOR}
    assert {"interest_coverage", "current_ratio", "cfo_to_debt"} <= flagged


def test_missing_prior_year_flags_growth_as_nan(cfg):
    res = compute_ratios(row(), None, cfg)
    assert math.isnan(res.values["revenue_growth"])
    assert F_NO_PRIOR in codes(res)


def test_true_dscr_includes_scheduled_principal(cfg):
    res = compute_ratios(row(scheduled_principal=100.0), None, cfg)
    assert res.values["dscr"] == pytest.approx(150 / (50 + 100))  # 1.00
    assert F_NO_SCHEDULE not in codes(res)


def test_bullet_maturity_shows_up_in_dscr_but_not_in_cash_interest_cover(cfg):
    """The audit question: 4x cash interest cover, yet a bullet repayment cannot be met."""
    res = compute_ratios(row(cfo=200.0, interest_expense=50.0, scheduled_principal=400.0), None, cfg)
    assert res.values["dscr_proxy"] == pytest.approx(4.0)
    assert assign_band(res.values["dscr_proxy"], cfg.spec("dscr_proxy")) == "green"
    assert res.values["dscr"] == pytest.approx(200 / 450)
    assert assign_band(res.values["dscr"], cfg.spec("dscr")) == "red"


def test_inventory_days_use_cogs_when_supplied(cfg):
    res = compute_ratios(row(cogs=750.0), None, cfg)
    assert res.values["inventory_days"] == pytest.approx(100 / 750 * 365)  # 48.7
    assert res.derived["inventory_days_basis"] == "cogs"
    assert F_REVENUE_BASIS not in codes(res)


def test_revenue_basis_understates_inventory_days_by_the_gross_margin(cfg):
    on_rev = compute_ratios(row(), None, cfg).values["inventory_days"]
    on_cogs = compute_ratios(row(cogs=750.0), None, cfg).values["inventory_days"]
    # COGS = 75% of revenue, so true days are revenue-based days / 0.75 (one third higher)
    assert on_cogs == pytest.approx(on_rev / 0.75)

"""Banding, deterioration detection, scoring and portfolio banding."""

from __future__ import annotations

import math

import pandas as pd
import pytest

from conftest import row
from ews.config import ScoreSpec, build_config
from ews.scoring import (
    assign_band,
    adverse_delta,
    evaluate,
    is_deterioration,
    top_signals_by_frequency,
)


# ---------------------------------------------------------------- banding
def test_band_boundaries_are_inclusive_lower_is_better(cfg):
    spec = cfg.ratios["net_debt_ebitda"]  # green 3.0, amber 4.5, lower is better
    assert assign_band(2.99, spec) == "green"
    assert assign_band(3.0, spec) == "green"  # exactly on the green threshold
    assert assign_band(3.01, spec) == "amber"
    assert assign_band(4.5, spec) == "amber"  # exactly on the amber threshold
    assert assign_band(4.51, spec) == "red"


def test_band_boundaries_are_inclusive_higher_is_better(cfg):
    spec = cfg.ratios["interest_coverage"]  # green 2.5, amber 1.5, higher is better
    assert assign_band(2.51, spec) == "green"
    assert assign_band(2.5, spec) == "green"  # exactly on the green threshold
    assert assign_band(2.49, spec) == "amber"
    assert assign_band(1.5, spec) == "amber"  # exactly on the amber threshold
    assert assign_band(1.49, spec) == "red"


def test_band_of_nan_is_none(cfg):
    assert assign_band(float("nan"), cfg.ratios["quick_ratio"]) is None
    assert assign_band(None, cfg.ratios["quick_ratio"]) is None


# ---------------------------------------------------------- deterioration
def test_deterioration_fires_on_a_fall_inside_the_green_band(cfg):
    """Coverage falls 1.2x in one year but stays green - the flag must still fire."""
    spec = cfg.ratios["interest_coverage"]  # trigger 0.5x
    prior, current = 4.0, 2.8
    assert assign_band(current, spec) == "green"  # level is comfortably inside green
    assert is_deterioration(current, prior, spec) is True
    assert adverse_delta(current, prior, spec) == pytest.approx(1.2)


def test_deterioration_does_not_fire_on_an_improvement(cfg):
    spec = cfg.ratios["interest_coverage"]
    assert is_deterioration(2.6, 2.0, spec) is False


def test_deterioration_does_not_fire_below_the_trigger(cfg):
    spec = cfg.ratios["interest_coverage"]
    assert is_deterioration(3.7, 4.0, spec) is False  # 0.3x fall < 0.5x trigger


def test_deterioration_direction_for_ratio_where_rising_is_worse(cfg):
    spec = cfg.ratios["net_debt_ebitda"]  # trigger 0.5x, rising is adverse
    assert is_deterioration(3.2, 2.6, spec) is True
    assert is_deterioration(2.0, 2.6, spec) is False


def test_deterioration_flag_fires_end_to_end_inside_green(cfg):
    """Interest coverage falls 0.6x in one year and stays green; the flag fires.

    Everything else is held flat on purpose (EBITDA margin, DSCR, leverage,
    working capital) so the score can only come from the coverage fall:
      FY2024: ebitda 160 / interest 50.00 = 3.20x
      FY2025: ebitda 200 / interest 76.92 = 2.60x  (fall of 0.60x, green >= 2.5x)
      DSCR held at 3.00x by moving CFO with interest; revenue up 25% so growth
      is green and improving; EBITDA margin 20% in both years.
    """
    years = [
        row(fiscal_year=2024, revenue=800.0, ebitda=160.0, interest_expense=50.0, cfo=150.0),
        row(fiscal_year=2025, revenue=1000.0, ebitda=200.0, interest_expense=76.9230769, cfo=230.7692308),
    ]
    res = evaluate(pd.DataFrame(years), cfg)
    latest = res.records[("Test Borrower Ltd", 2025)]

    assert latest.values["interest_coverage"] == pytest.approx(2.6)
    assert latest.bands["interest_coverage"] == "green"
    assert latest.deteriorations["interest_coverage"] is True

    det = [s for s in latest.signals if s["signal_type"] == "deterioration"]
    assert any(s["ratio"] == "interest_coverage" for s in det)
    det_signal = next(s for s in det if s["ratio"] == "interest_coverage")
    assert det_signal["band"] == "green"
    assert det_signal["weight"] == pytest.approx(cfg.score.deterioration_weight)
    assert "still inside the green band" in det_signal["detail"]
    # nothing else is tripped, so the score is only the deterioration weight
    assert [s["ratio"] for s in latest.signals] == ["interest_coverage"]
    assert latest.score == pytest.approx(cfg.score.deterioration_weight)
    assert latest.band == "green"


def test_deterioration_on_red_level_carries_no_extra_weight(cfg):
    years = [
        row(fiscal_year=2024, ebitda=60.0, interest_expense=50.0),  # coverage 1.20x -> amber
        row(fiscal_year=2025, ebitda=20.0, interest_expense=50.0),  # coverage 0.40x -> red
    ]
    res = evaluate(pd.DataFrame(years), cfg)
    latest = res.records[("Test Borrower Ltd", 2025)]
    det = [s for s in latest.signals if s["signal_type"] == "deterioration"
           and s["ratio"] == "interest_coverage"]
    assert len(det) == 1
    assert det[0]["weight"] == 0.0
    assert "no additional weight" in det[0]["detail"]


# -------------------------------------------------------------- scoring
def test_score_is_weighted_count_of_red_and_amber(cfg):
    # leverage 2 reds worth: net debt/EBITDA red, coverage red, one amber (quick)
    bad = row(total_debt=900.0, cash=0.0, ebitda=150.0, interest_expense=120.0, inventory=180.0)
    res = evaluate(pd.DataFrame([bad]), cfg)
    rec = res.records[("Test Borrower Ltd", 2025)]

    reds = [s for s in rec.signals if s["signal_type"] == "level" and s["severity"] == "red"]
    ambers = [s for s in rec.signals if s["signal_type"] == "level" and s["severity"] == "amber"]
    expected = cfg.score.red_weight * len(reds) + cfg.score.amber_weight * len(ambers)
    assert rec.score == pytest.approx(expected)
    assert rec.score == pytest.approx(3 * 3 + 1 * 3)  # three reds, three ambers


def test_score_band_cutoffs():
    score = ScoreSpec(red_min_score=12.0, amber_min_score=4.0)
    assert score.band_for_score(0.0) == "green"
    assert score.band_for_score(3.99) == "green"
    assert score.band_for_score(4.0) == "amber"
    assert score.band_for_score(11.99) == "amber"
    assert score.band_for_score(12.0) == "red"
    assert score.band_for_score(40.0) == "red"


def test_weights_come_from_config_not_code():
    data = {
        "score": {"red_weight": 5.0, "amber_weight": 2.0, "deterioration_weight": 0.25,
                  "red_min_score": 20.0, "amber_min_score": 6.0},
        "ratios": {
            "net_debt_ebitda": {"label": "Net debt / EBITDA", "direction": "lower_is_better",
                                "unit": "x", "green": 3.0, "amber": 4.5, "deterioration": 0.5},
        },
    }
    cfg = build_config(data)
    bad = row(total_debt=900.0, cash=0.0, ebitda=100.0)  # 9.0x -> red
    res = evaluate(pd.DataFrame([bad]), cfg)
    rec = res.records[("Test Borrower Ltd", 2025)]
    assert rec.score == pytest.approx(5.0)
    assert rec.band == "green"  # score 5 < amber_min_score 6 with this config


# ------------------------------------------------------------- portfolio
def test_sample_panel_gives_two_red_two_amber_two_green(result):
    bands = result.summary["band"].tolist()
    assert bands.count("red") == 2
    assert bands.count("amber") == 2
    assert bands.count("green") == 2


def test_watchlist_is_ranked_worst_first(result):
    scores = result.summary["score"].tolist()
    assert scores == sorted(scores, reverse=True)
    assert result.summary.iloc[0]["borrower"] == "Deccan Auto Components Pvt Ltd"
    assert result.summary.iloc[0]["band"] == "red"
    assert result.summary["rank"].tolist() == list(range(1, len(scores) + 1))


def test_negative_ebitda_borrower_is_red_with_a_critical_flag(result):
    row_ = result.summary.set_index("borrower").loc["Sundaram Textiles Ltd"]
    assert row_["band"] == "red"
    assert row_["critical_flags"] == 1
    latest = result.records[("Sundaram Textiles Ltd", 2025)]
    assert math.isnan(latest.values["net_debt_ebitda"])
    assert any(s["severity"] == "critical" for s in latest.signals)


def test_signal_log_covers_every_borrower_and_year(result):
    assert not result.signals.empty
    assert set(result.signals["signal_type"]) == {"level", "deterioration", "data_flag"}
    # a clean borrower trips nothing, so it is legitimately absent from the log
    assert set(result.signals["borrower"]) <= set(result.summary["borrower"])
    assert "Tapti Chemicals Ltd" not in set(result.signals["borrower"])
    # the first year of a borrower can only carry level/data signals, never a delta
    first_year = result.signals.groupby("borrower")["fiscal_year"].transform("min")
    first_rows = result.signals[result.signals["fiscal_year"] == first_year]
    assert set(first_rows["signal_type"]) <= {"level", "data_flag"}


def test_top_signals_by_frequency_returns_three(result):
    top = top_signals_by_frequency(result.signals, latest_only=True, n=3)
    assert len(top) == 3
    counts = [c for _, c in top]
    assert counts == sorted(counts, reverse=True)

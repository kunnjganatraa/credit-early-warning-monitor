"""Shared fixtures. Also puts the repo root on sys.path so `pytest -q` works
from a clean checkout without installing the package."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ews.config import load_config  # noqa: E402
from ews.panel import load_panel  # noqa: E402
from ews.scoring import evaluate  # noqa: E402

CONFIG_PATH = ROOT / "config" / "thresholds.yaml"
PANEL_PATH = ROOT / "data" / "borrower_panel.csv"


@pytest.fixture(scope="session")
def cfg():
    return load_config(str(CONFIG_PATH))


@pytest.fixture(scope="session")
def panel():
    return load_panel(str(PANEL_PATH))


@pytest.fixture(scope="session")
def result(cfg, panel):
    return evaluate(panel, cfg)


def row(**overrides) -> dict:
    """A clean baseline borrower-year; override individual line items."""
    base = {
        "borrower": "Test Borrower Ltd",
        "sector": "Testing",
        "fiscal_year": 2025,
        "revenue": 1000.0,
        "ebitda": 200.0,
        "pat": 80.0,
        "interest_expense": 50.0,
        "total_debt": 400.0,
        "net_worth": 500.0,
        "current_assets": 300.0,
        "current_liabilities": 200.0,
        "inventory": 100.0,
        "receivables": 120.0,
        "cash": 50.0,
        "cfo": 150.0,
        "capex": 40.0,
        "contingent_liabilities": 100.0,
    }
    base.update(overrides)
    return base


@pytest.fixture
def base_row():
    return row

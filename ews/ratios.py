"""Ratio computation for the credit early-warning monitor.

Every ratio is computed defensively: a zero or negative denominator returns
NaN plus an explicit flag instead of inf/-inf, so downstream banding can
never be fooled by an infinity.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Mapping

from .config import EwsConfig

INPUT_COLUMNS = [
    "borrower",
    "sector",
    "fiscal_year",
    "revenue",
    "ebitda",
    "pat",
    "interest_expense",
    "total_debt",
    "net_worth",
    "current_assets",
    "current_liabilities",
    "inventory",
    "receivables",
    "cash",
    "cfo",
    "capex",
    "contingent_liabilities",
]

FINANCIAL_COLUMNS = INPUT_COLUMNS[3:]

# Optional columns. If absent from the CSV they are added as blank (NaN).
#   scheduled_principal : contractual principal repayment due in the year (Rs crore).
#                         Needed for a true DSCR; without it DSCR is NaN + flag, never guessed.
#   cogs                : cost of goods sold. When present, inventory days use COGS
#                         (the correct base); otherwise revenue, and the basis is recorded.
OPTIONAL_COLUMNS = ["scheduled_principal", "cogs"]

# flag codes
F_ZERO_DENOMINATOR = "zero_denominator"
F_NEG_EBITDA = "non_positive_ebitda"
F_NEG_NET_WORTH = "non_positive_net_worth"
F_NO_PRIOR = "no_prior_year"
F_NO_SCHEDULE = "no_principal_schedule"
F_REVENUE_BASIS = "inventory_days_on_revenue"

# flags that are treated as red-level signals in their own right
CRITICAL_FLAGS = (F_NEG_EBITDA, F_NEG_NET_WORTH)

FLAG_TEXT = {
    F_ZERO_DENOMINATOR: "denominator is zero - ratio undefined",
    F_NEG_EBITDA: "EBITDA is zero or negative - leverage and coverage are not meaningful",
    F_NEG_NET_WORTH: "net worth is zero or negative - solvency ratios are not meaningful",
    F_NO_PRIOR: "no prior year in panel - growth and deltas not computable",
    F_NO_SCHEDULE: "scheduled principal not supplied - true DSCR not computed",
    F_REVENUE_BASIS: "COGS not supplied - inventory days computed on revenue, which understates holding period",
}

NAN = float("nan")


def is_nan(value: float | None) -> bool:
    return value is None or (isinstance(value, float) and math.isnan(value))


def _num(row: Mapping, key: str) -> float:
    value = row.get(key, NAN)
    if value is None:
        return NAN
    try:
        out = float(value)
    except (TypeError, ValueError):
        return NAN
    return out


@dataclass
class RatioResult:
    values: dict[str, float] = field(default_factory=dict)
    flags: list[dict] = field(default_factory=list)
    derived: dict[str, float] = field(default_factory=dict)

    def add_flag(self, ratio: str, code: str, detail: str = "") -> None:
        message = FLAG_TEXT.get(code, code)
        self.flags.append(
            {
                "ratio": ratio,
                "code": code,
                "detail": detail or message,
                "critical": code in CRITICAL_FLAGS,
            }
        )


def _div(num: float, den: float, res: RatioResult, ratio: str, den_name: str) -> float:
    """Safe division: zero/NaN denominator -> NaN + flag."""
    if is_nan(num) or is_nan(den):
        return NAN
    if den == 0:
        res.add_flag(ratio, F_ZERO_DENOMINATOR, f"{den_name} is zero - {ratio} undefined")
        return NAN
    return num / den


def compute_ratios(fin: Mapping, prior: Mapping | None, cfg: EwsConfig) -> RatioResult:
    """Compute every configured ratio for one borrower-year.

    ``fin`` is the current year row, ``prior`` the same borrower's previous
    fiscal year row (or None).
    """
    res = RatioResult()

    revenue = _num(fin, "revenue")
    ebitda = _num(fin, "ebitda")
    pat = _num(fin, "pat")
    interest = _num(fin, "interest_expense")
    total_debt = _num(fin, "total_debt")
    net_worth = _num(fin, "net_worth")
    current_assets = _num(fin, "current_assets")
    current_liabilities = _num(fin, "current_liabilities")
    inventory = _num(fin, "inventory")
    receivables = _num(fin, "receivables")
    cash = _num(fin, "cash")
    cfo = _num(fin, "cfo")
    contingent = _num(fin, "contingent_liabilities")
    principal = _num(fin, "scheduled_principal")
    cogs = _num(fin, "cogs")

    net_debt = total_debt - cash
    res.derived["net_debt"] = net_debt
    res.derived["quick_assets"] = current_assets - inventory
    res.derived["tol"] = total_debt + contingent

    ebitda_positive = (not is_nan(ebitda)) and ebitda > 0
    net_worth_positive = (not is_nan(net_worth)) and net_worth > 0

    if not ebitda_positive:
        res.add_flag("ebitda", F_NEG_EBITDA, f"EBITDA is {ebitda:.2f} crore")
    if not net_worth_positive:
        res.add_flag("net_worth", F_NEG_NET_WORTH, f"net worth is {net_worth:.2f} crore")

    for key in cfg.ratio_keys:
        res.values[key] = NAN

    for key in cfg.ratio_keys:
        if key == "net_debt_ebitda":
            # negative EBITDA makes this ratio meaningless; flag, do not divide
            res.values[key] = _div(net_debt, ebitda, res, key, "EBITDA") if ebitda_positive else NAN
        elif key == "interest_coverage":
            res.values[key] = _div(ebitda, interest, res, key, "interest expense") if ebitda_positive else NAN
        elif key == "dscr_proxy":
            res.values[key] = _div(cfo, interest, res, key, "interest expense")
        elif key == "dscr":
            # Debt service coverage = cash from operations / (interest + scheduled principal).
            # CFO is taken before interest paid, which is the usual Ind AS presentation
            # (interest paid sits in financing activities). No principal, no ratio.
            if is_nan(principal):
                res.add_flag(key, F_NO_SCHEDULE)
                res.values[key] = NAN
            else:
                res.values[key] = _div(cfo, interest + principal, res, key, "interest + scheduled principal")
        elif key == "current_ratio":
            res.values[key] = _div(current_assets, current_liabilities, res, key, "current liabilities")
        elif key == "quick_ratio":
            res.values[key] = _div(current_assets - inventory, current_liabilities, res, key, "current liabilities")
        elif key == "tol_tnw":
            res.values[key] = (
                _div(total_debt + contingent, net_worth, res, key, "net worth") if net_worth_positive else NAN
            )
        elif key == "cfo_to_debt":
            res.values[key] = _div(cfo, total_debt, res, key, "total debt")
        elif key == "ebitda_margin":
            res.values[key] = _div(ebitda, revenue, res, key, "revenue")
        elif key == "revenue_growth":
            if prior is None:
                res.add_flag(key, F_NO_PRIOR, "no prior year for this borrower")
                res.values[key] = NAN
            else:
                prior_revenue = _num(prior, "revenue")
                growth = _div(revenue - prior_revenue, prior_revenue, res, key, "prior year revenue")
                res.values[key] = NAN if is_nan(growth) else growth
        elif key == "receivable_days":
            days = _div(receivables, revenue, res, key, "revenue")
            res.values[key] = NAN if is_nan(days) else days * 365.0
        elif key == "inventory_days":
            if not is_nan(cogs) and cogs > 0:
                days = _div(inventory, cogs, res, key, "COGS")
                res.derived["inventory_days_basis"] = "cogs"
            else:
                days = _div(inventory, revenue, res, key, "revenue")
                res.derived["inventory_days_basis"] = "revenue"
                if not is_nan(inventory):
                    res.add_flag(key, F_REVENUE_BASIS)
            res.values[key] = NAN if is_nan(days) else days * 365.0
        elif key == "pat_to_networth":
            res.values[key] = _div(pat, net_worth, res, key, "net worth") if net_worth_positive else NAN
        else:  # pragma: no cover - guarded by config validation
            raise KeyError(f"no formula implemented for ratio {key!r}")

    return res

"""Sector-relative lens.

Absolute thresholds judge a cement company and a pharma company on the same
bars. This module places each borrower's latest-year ratios against its own
sector peers in the same panel and reports where the two views disagree:

* hidden relative weakness - the absolute band is green, but the borrower is the
  weakest in its sector and trails the sector median by at least the ratio's
  deterioration trigger. Absolute bands would let it through.
* sector-wide level - the absolute band is amber or red, but the borrower is at
  or better than its sector median. The whole sector sits there, so the absolute
  threshold may be miscalibrated for that sector; it is a prompt to check, not a
  reason to ignore the signal.

A sector needs at least ``min_peers`` borrowers with a valid value for that
ratio; otherwise the borrower is reported as "too few peers" and no view is
taken. Medians, not means, so one outlier cannot move the benchmark.
"""

from __future__ import annotations

import math

import pandas as pd

from .config import EwsConfig
from .ratios import is_nan

AGREES = "agrees"
HIDDEN = "hidden relative weakness"
SECTOR_WIDE = "sector-wide level"
TOO_FEW = "too few peers"


def latest_rows(ratio_history: pd.DataFrame) -> pd.DataFrame:
    idx = ratio_history.groupby("borrower")["fiscal_year"].idxmax()
    return ratio_history.loc[idx].reset_index(drop=True)


def sector_view(ratio_history: pd.DataFrame, cfg: EwsConfig, min_peers: int = 3,
                ratios: list[str] | None = None) -> pd.DataFrame:
    """One row per borrower x ratio for each borrower's latest year."""
    latest = latest_rows(ratio_history)
    keys = ratios or cfg.ratio_keys
    out = []
    for key in keys:
        spec = cfg.spec(key)
        for sector, grp in latest.groupby("sector"):
            vals = grp[["borrower", "fiscal_year", key, f"{key}__band"]].copy()
            valid = vals[vals[key].apply(lambda x: not is_nan(x))]
            n = len(valid)
            median = float(valid[key].median()) if n else math.nan
            # rank 1 = strongest in sector
            ordered = valid.sort_values(key, ascending=not spec.higher_is_better).reset_index(drop=True)
            rank_of = {b: i + 1 for i, b in enumerate(ordered["borrower"])}
            for _, r in vals.iterrows():
                value = r[key]
                band = r[f"{key}__band"]
                if is_nan(value):
                    continue
                if n < min_peers:
                    view, position, rank_txt, gap = TOO_FEW, "n/a", "n/a", math.nan
                else:
                    rank = rank_of[r["borrower"]]
                    rank_txt = f"{rank} of {n}"
                    position = "strongest" if rank == 1 else ("weakest" if rank == n else "middle")
                    # gap > 0 means worse than the sector median
                    gap = (median - value) if spec.higher_is_better else (value - median)
                    if band == "green" and position == "weakest" and gap >= spec.deterioration > 0:
                        view = HIDDEN
                    elif band in ("amber", "red") and gap <= 0:
                        view = SECTOR_WIDE
                    else:
                        view = AGREES
                out.append({
                    "borrower": r["borrower"], "sector": sector, "fiscal_year": int(r["fiscal_year"]),
                    "ratio": key, "label": spec.label, "value": float(value), "absolute_band": band,
                    "sector_median": median, "gap_to_median_adverse": gap, "peers": n,
                    "rank_in_sector": rank_txt, "relative_position": position, "view": view,
                })
    cols = ["borrower", "sector", "fiscal_year", "ratio", "label", "value", "absolute_band", "sector_median",
            "gap_to_median_adverse", "peers", "rank_in_sector", "relative_position", "view"]
    df = pd.DataFrame(out, columns=cols)
    return df.sort_values(["sector", "ratio", "value"]).reset_index(drop=True)


def disagreements(view: pd.DataFrame) -> pd.DataFrame:
    return view[view["view"].isin([HIDDEN, SECTOR_WIDE])].reset_index(drop=True)

"""Banding, deterioration detection, scoring and panel-level analysis."""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from .config import EwsConfig, RatioSpec
from .ratios import CRITICAL_FLAGS, RatioResult, compute_ratios, is_nan

BAND_ORDER = {"green": 0, "amber": 1, "red": 2}
SEVERITY_ORDER = {"deterioration": 0, "amber": 1, "red": 2, "critical": 3}


def assign_band(value: float | None, spec: RatioSpec) -> str | None:
    """Map a ratio value to green/amber/red. Boundaries are inclusive.

    NaN (undefined ratio) returns None - it is never silently banded.
    """
    if is_nan(value):
        return None
    if spec.higher_is_better:
        if value >= spec.green:
            return "green"
        if value >= spec.amber:
            return "amber"
        return "red"
    if value <= spec.green:
        return "green"
    if value <= spec.amber:
        return "amber"
    return "red"


def adverse_delta(value: float | None, prior: float | None, spec: RatioSpec) -> float:
    """Size of the adverse year-on-year move, positive = worse. NaN if not comparable."""
    if is_nan(value) or is_nan(prior):
        return float("nan")
    change = float(value) - float(prior)
    return change if not spec.higher_is_better else -change


def is_deterioration(value: float | None, prior: float | None, spec: RatioSpec) -> bool:
    """True when the adverse move reaches the configured trigger.

    Fires on the level, not the band, so a ratio can deteriorate while still
    sitting comfortably inside green.
    """
    if spec.deterioration <= 0:
        return False
    delta = adverse_delta(value, prior, spec)
    if is_nan(delta):
        return False
    return delta >= spec.deterioration


def format_delta(spec: RatioSpec, delta: float) -> str:
    if is_nan(delta):
        return "n/a"
    if spec.unit == "pct":
        return f"{delta * 100:.1f}pp"
    if spec.unit == "days":
        return f"{delta:.0f} days"
    return f"{delta:.2f}x"


@dataclass
class YearRecord:
    borrower: str
    sector: str
    fiscal_year: int
    values: dict[str, float]
    bands: dict[str, str | None]
    deltas: dict[str, float]
    deteriorations: dict[str, bool]
    flags: list[dict]
    signals: list[dict] = field(default_factory=list)
    score: float = 0.0
    band: str = "green"


@dataclass
class AnalysisResult:
    cfg: EwsConfig
    ratio_history: pd.DataFrame
    delta_history: pd.DataFrame
    signals: pd.DataFrame
    summary: pd.DataFrame
    records: dict[tuple[str, int], YearRecord]

    @property
    def red(self) -> list[str]:
        return self.summary.loc[self.summary["band"] == "red", "borrower"].tolist()

    @property
    def amber(self) -> list[str]:
        return self.summary.loc[self.summary["band"] == "amber", "borrower"].tolist()

    @property
    def green(self) -> list[str]:
        return self.summary.loc[self.summary["band"] == "green", "borrower"].tolist()


def _level_signals(rec: YearRecord, cfg: EwsConfig) -> list[dict]:
    out = []
    for key, spec in cfg.ratios.items():
        band = rec.bands.get(key)
        if band not in ("amber", "red"):
            continue
        value = rec.values.get(key)
        weight = cfg.score.red_weight if band == "red" else cfg.score.amber_weight
        out.append(
            {
                "borrower": rec.borrower,
                "sector": rec.sector,
                "fiscal_year": rec.fiscal_year,
                "ratio": key,
                "label": spec.label,
                "signal_type": "level",
                "value": value,
                "prior_value": float("nan"),
                "delta": float("nan"),
                "band": band,
                "severity": band,
                "weight": weight,
                "detail": f"{spec.label} at {spec.format_value(value)} is in the {band} band "
                f"(green needs {spec.format_value(spec.green)})",
            }
        )
    return out


def _flag_signals(rec: YearRecord, cfg: EwsConfig) -> list[dict]:
    out = []
    for flag in rec.flags:
        if flag["code"] not in CRITICAL_FLAGS:
            continue
        spec = cfg.ratios.get(flag["ratio"])
        labels = {"ebitda": "EBITDA (input)", "net_worth": "Net worth (input)"}
        out.append(
            {
                "borrower": rec.borrower,
                "sector": rec.sector,
                "fiscal_year": rec.fiscal_year,
                "ratio": flag["ratio"],
                "label": spec.label if spec else labels.get(flag["ratio"], flag["ratio"]),
                "signal_type": "data_flag",
                "value": float("nan"),
                "prior_value": float("nan"),
                "delta": float("nan"),
                "band": "red",
                "severity": "critical",
                "weight": cfg.score.red_weight,
                "detail": flag["detail"],
            }
        )
    return out


def _deterioration_signals(rec: YearRecord, cfg: EwsConfig) -> list[dict]:
    out = []
    for key, spec in cfg.ratios.items():
        if not rec.deteriorations.get(key):
            continue
        band = rec.bands.get(key)
        if band == "red" and not cfg.score.deterioration_counts_when_red:
            weight = 0.0  # already fully penalised by the red level signal
        else:
            weight = cfg.score.deterioration_weight
        delta = rec.deltas.get(key, float("nan"))
        value = rec.values.get(key, float("nan"))
        prior_value = float("nan") if is_nan(delta) else value - delta
        verb = "fell" if spec.higher_is_better else "rose"
        out.append(
            {
                "borrower": rec.borrower,
                "sector": rec.sector,
                "fiscal_year": rec.fiscal_year,
                "ratio": key,
                "label": spec.label,
                "signal_type": "deterioration",
                "value": value,
                "prior_value": prior_value,
                "delta": delta,
                "band": band or "n/a",
                "severity": "deterioration",
                "weight": weight,
                "detail": f"{spec.label} {verb} {format_delta(spec, abs(delta))} year on year "
                f"(trigger {format_delta(spec, spec.deterioration)})"
                + (
                    f" - level already red, no additional weight"
                    if weight == 0.0
                    else (f" but still inside the {band} band" if band else "")
                ),
            }
        )
    return out


def evaluate(panel: pd.DataFrame, cfg: EwsConfig) -> AnalysisResult:
    """Run ratios, banding, deterioration detection and scoring over a panel."""
    records: dict[tuple[str, int], YearRecord] = {}
    borrowers = list(dict.fromkeys(panel["borrower"].tolist()))

    for borrower in borrowers:
        sub = panel[panel["borrower"] == borrower].sort_values("fiscal_year")
        rows = [r.to_dict() for _, r in sub.iterrows()]
        results: list[RatioResult] = []
        prior_row = None
        for current in rows:
            results.append(compute_ratios(current, prior_row, cfg))
            prior_row = current

        for idx, (current, res) in enumerate(zip(rows, results)):
            prior_res = results[idx - 1] if idx > 0 else None
            rec = YearRecord(
                borrower=borrower,
                sector=str(current["sector"]),
                fiscal_year=int(current["fiscal_year"]),
                values=dict(res.values),
                bands={},
                deltas={},
                deteriorations={},
                flags=list(res.flags),
            )
            for key, spec in cfg.ratios.items():
                value = res.values.get(key)
                prior_value = None if prior_res is None else prior_res.values.get(key)
                rec.bands[key] = assign_band(value, spec)
                if is_nan(value) or is_nan(prior_value):
                    rec.deltas[key] = float("nan")
                else:
                    rec.deltas[key] = float(value) - float(prior_value)
                rec.deteriorations[key] = is_deterioration(value, prior_value, spec)

            rec.signals = _level_signals(rec, cfg) + _flag_signals(rec, cfg) + _deterioration_signals(rec, cfg)
            rec.score = round(sum(float(s["weight"]) for s in rec.signals), 2)
            rec.band = cfg.score.band_for_score(rec.score)
            records[(borrower, rec.fiscal_year)] = rec

    ratio_rows, delta_rows, signal_rows = [], [], []
    for (borrower, year), rec in records.items():
        rrow = {"borrower": borrower, "sector": rec.sector, "fiscal_year": year}
        drow = {"borrower": borrower, "sector": rec.sector, "fiscal_year": year}
        for key, spec in cfg.ratios.items():
            rrow[key] = rec.values.get(key, float("nan"))
            rrow[f"{key}__band"] = rec.bands.get(key) or "n/a"
            drow[f"{key}__delta"] = rec.deltas.get(key, float("nan"))
            drow[f"{key}__deterioration"] = bool(rec.deteriorations.get(key))
        rrow["score"] = rec.score
        rrow["band"] = rec.band
        drow["deterioration_count"] = int(sum(1 for v in rec.deteriorations.values() if v))
        ratio_rows.append(rrow)
        delta_rows.append(drow)
        signal_rows.extend(rec.signals)

    ratio_history = pd.DataFrame(ratio_rows).sort_values(["borrower", "fiscal_year"]).reset_index(drop=True)
    delta_history = pd.DataFrame(delta_rows).sort_values(["borrower", "fiscal_year"]).reset_index(drop=True)

    signal_cols = [
        "borrower", "sector", "fiscal_year", "ratio", "label", "signal_type",
        "value", "prior_value", "delta", "band", "severity", "weight", "detail",
    ]
    signals = pd.DataFrame(signal_rows, columns=signal_cols)
    if not signals.empty:
        signals["_sev"] = signals["severity"].map(SEVERITY_ORDER).fillna(0).astype(int)
        signals = signals.sort_values(
            ["fiscal_year", "_sev", "weight", "borrower"], ascending=[False, False, False, True]
        ).drop(columns="_sev").reset_index(drop=True)

    summary_rows = []
    for borrower in borrowers:
        latest_year = max(y for (b, y) in records if b == borrower)
        rec = records[(borrower, latest_year)]
        lvl = [s for s in rec.signals if s["signal_type"] == "level"]
        reds = [s for s in lvl if s["severity"] == "red"]
        ambers = [s for s in lvl if s["severity"] == "amber"]
        dets = [s for s in rec.signals if s["signal_type"] == "deterioration"]
        crits = [s for s in rec.signals if s["signal_type"] == "data_flag"]
        ranked = sorted(
            rec.signals,
            key=lambda s: (-SEVERITY_ORDER.get(s["severity"], 0), -float(s["weight"]), s["ratio"]),
        )
        summary_rows.append(
            {
                "borrower": borrower,
                "sector": rec.sector,
                "latest_year": latest_year,
                "score": rec.score,
                "band": rec.band,
                "red_signals": len(reds),
                "amber_signals": len(ambers),
                "deterioration_flags": len(dets),
                "critical_flags": len(crits),
                "signals_total": len(rec.signals),
                "top_signals": "; ".join(s["label"] for s in ranked[:3]) if ranked else "none",
            }
        )

    summary = pd.DataFrame(summary_rows).sort_values(
        ["score", "red_signals", "borrower"], ascending=[False, False, True]
    ).reset_index(drop=True)
    summary.insert(0, "rank", range(1, len(summary) + 1))

    return AnalysisResult(
        cfg=cfg,
        ratio_history=ratio_history,
        delta_history=delta_history,
        signals=signals,
        summary=summary,
        records=records,
    )


def top_signals_by_frequency(signals: pd.DataFrame, latest_only: bool = True, n: int = 3) -> list[tuple[str, int]]:
    """Most frequently tripped signal labels (level + deterioration), worst first."""
    if signals.empty:
        return []
    frame = signals
    if latest_only:
        frame = frame[frame["fiscal_year"] == frame["fiscal_year"].max()]
    counts = frame.groupby("label").size().sort_values(ascending=False)
    return [(str(label), int(count)) for label, count in counts.head(n).items()]

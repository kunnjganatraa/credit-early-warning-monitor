"""Panel loading and validation."""

from __future__ import annotations

import os

import pandas as pd

from .ratios import FINANCIAL_COLUMNS, INPUT_COLUMNS, OPTIONAL_COLUMNS


class PanelError(ValueError):
    """Raised when the input panel is missing columns or is otherwise unusable."""


def load_panel(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise PanelError(f"panel file not found: {path}")
    try:
        df = pd.read_csv(path)
    except Exception as exc:  # pragma: no cover - depends on file contents
        raise PanelError(f"could not read {path}: {exc}") from exc
    return validate_panel(df)


def validate_panel(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]

    missing = [c for c in INPUT_COLUMNS if c not in df.columns]
    if missing:
        raise PanelError(f"panel is missing required column(s): {', '.join(missing)}")
    for col in OPTIONAL_COLUMNS:
        if col not in df.columns:
            df[col] = float("nan")
    keep = INPUT_COLUMNS + OPTIONAL_COLUMNS
    extra = [c for c in df.columns if c not in keep]
    if extra:
        df = df.drop(columns=extra)

    df = df[keep]

    for col in ("borrower", "sector"):
        df[col] = df[col].astype(str).str.strip()
        if (df[col] == "").any():
            raise PanelError(f"column {col!r} contains blank values")

    years = pd.to_numeric(df["fiscal_year"], errors="coerce")
    if years.isna().any():
        bad = df.loc[years.isna(), "fiscal_year"].tolist()[:5]
        raise PanelError(f"fiscal_year must be numeric; bad value(s): {bad}")
    df["fiscal_year"] = years.astype(int)

    for col in FINANCIAL_COLUMNS + OPTIONAL_COLUMNS:
        coerced = pd.to_numeric(df[col], errors="coerce")
        bad = df[col].notna() & coerced.isna()
        if bad.any():
            bad_vals = df.loc[bad, col].tolist()[:5]
            raise PanelError(f"column {col!r} has non-numeric value(s): {bad_vals}")
        df[col] = coerced.astype(float)

    dups = df.duplicated(subset=["borrower", "fiscal_year"], keep=False)
    if dups.any():
        sample = df.loc[dups, ["borrower", "fiscal_year"]].head(5).to_dict("records")
        raise PanelError(f"duplicate borrower/fiscal_year rows: {sample}")

    df = df.sort_values(["borrower", "fiscal_year"]).reset_index(drop=True)
    return df


def borrower_names(df: pd.DataFrame) -> list[str]:
    return list(dict.fromkeys(df["borrower"].tolist()))

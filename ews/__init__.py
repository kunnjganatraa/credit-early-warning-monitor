"""Credit Early-Warning Monitor.

Scores a panel of borrowers on credit ratios, bands each ratio green / amber /
red against configurable thresholds, and flags year-on-year deterioration even
when the level is still inside the band.
"""

from .config import ConfigError, EwsConfig, RatioSpec, ScoreSpec, build_config, load_config
from .panel import PanelError, load_panel, validate_panel
from .ratios import FLAG_TEXT, RatioResult, compute_ratios
from .scoring import (
    AnalysisResult,
    assign_band,
    adverse_delta,
    evaluate,
    is_deterioration,
    top_signals_by_frequency,
)

__version__ = "2.0.0"

__all__ = [
    "AnalysisResult",
    "ConfigError",
    "EwsConfig",
    "FLAG_TEXT",
    "PanelError",
    "RatioResult",
    "RatioSpec",
    "ScoreSpec",
    "adverse_delta",
    "assign_band",
    "build_config",
    "compute_ratios",
    "evaluate",
    "is_deterioration",
    "load_config",
    "load_panel",
    "top_signals_by_frequency",
    "validate_panel",
    "__version__",
]

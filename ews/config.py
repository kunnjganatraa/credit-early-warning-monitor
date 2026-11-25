"""Configuration loading and validation.

Thresholds must never live in code: everything tunable is read from a
config file (YAML or JSON) and validated on load.

YAML is parsed with PyYAML when it is installed, otherwise with the small
built-in reader below. The reader supports the subset this project needs
(nested mappings, scalar lists, comments, quoted strings, ints, floats,
booleans, null) so the tool runs on a bare Python install.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any, Iterable

DIRECTIONS = ("lower_is_better", "higher_is_better")
UNITS = ("x", "pct", "days")
REQUIRED_RATIO_KEYS = ("label", "direction", "green", "amber")


class ConfigError(ValueError):
    """Raised when the threshold config is missing, malformed or inconsistent."""


# --------------------------------------------------------------------------
# minimal YAML reader (subset)
# --------------------------------------------------------------------------

def _split_inline_comment(text: str) -> str:
    quote = None
    for i, ch in enumerate(text):
        if quote:
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch == "#" and (i == 0 or text[i - 1] in " \t"):
            return text[:i]
    return text


def _parse_scalar(token: str) -> Any:
    token = token.strip()
    if not token:
        return ""
    if len(token) >= 2 and token[0] == token[-1] and token[0] in "\"'":
        return token[1:-1]
    low = token.lower()
    if low in ("true", "yes"):
        return True
    if low in ("false", "no"):
        return False
    if low in ("null", "none", "~"):
        return None
    try:
        return int(token)
    except ValueError:
        pass
    try:
        return float(token)
    except ValueError:
        pass
    return token


def _tokenise(text: str) -> list[tuple[int, str]]:
    items: list[tuple[int, str]] = []
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        stripped = raw.lstrip()
        indent = len(raw) - len(stripped)
        if raw[:indent].count("\t"):
            raise ConfigError("tabs are not allowed for indentation; use spaces")
        items.append((indent, stripped.rstrip()))
    return items


def _parse_map(items: list[tuple[int, str]], i: int, indent: int) -> tuple[dict, int]:
    out: dict[str, Any] = {}
    while i < len(items):
        ind, content = items[i]
        if ind < indent:
            break
        if ind > indent:
            raise ConfigError(f"unexpected indentation near: {content!r}")
        if content.startswith("- "):
            raise ConfigError(f"cannot mix list and mapping near: {content!r}")
        key_part, sep, rest = content.partition(":")
        if not sep:
            raise ConfigError(f"expected 'key: value', got: {content!r}")
        key = key_part.strip().strip("\"'")
        rest = _split_inline_comment(rest).strip()
        if rest:
            out[key] = _parse_scalar(rest)
            i += 1
            continue
        if i + 1 < len(items) and items[i + 1][0] > ind:
            child_indent = items[i + 1][0]
            if items[i + 1][1].startswith("- "):
                out[key], i = _parse_list(items, i + 1, child_indent)
            else:
                out[key], i = _parse_map(items, i + 1, child_indent)
        else:
            out[key] = None
            i += 1
    return out, i


def _parse_list(items: list[tuple[int, str]], i: int, indent: int) -> tuple[list, int]:
    out: list[Any] = []
    while i < len(items):
        ind, content = items[i]
        if ind < indent:
            break
        if ind > indent:
            raise ConfigError(f"unexpected indentation near: {content!r}")
        if not content.startswith("- "):
            raise ConfigError(f"cannot mix list and mapping near: {content!r}")
        out.append(_parse_scalar(_split_inline_comment(content[2:])))
        i += 1
    return out, i


def mini_yaml_load(text: str) -> dict:
    """Parse the YAML subset used by this project into a dict."""
    items = _tokenise(text)
    if not items:
        return {}
    if items[0][1].startswith("- "):
        raise ConfigError("top level must be a mapping")
    data, _ = _parse_map(items, 0, items[0][0])
    return data


def _read_mapping(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    suffix = os.path.splitext(path)[1].lower()
    if suffix == ".json":
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise ConfigError(f"{path}: invalid JSON ({exc})") from exc
    else:
        try:
            import yaml  # type: ignore
        except ImportError:
            data = mini_yaml_load(text)
        else:
            try:
                data = yaml.safe_load(text)
            except Exception as exc:  # pragma: no cover - depends on PyYAML
                raise ConfigError(f"{path}: invalid YAML ({exc})") from exc
    if not isinstance(data, dict):
        raise ConfigError(f"{path}: config must be a mapping at the top level")
    return data


# --------------------------------------------------------------------------
# typed config
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class RatioSpec:
    key: str
    label: str
    direction: str
    unit: str
    green: float
    amber: float
    deterioration: float
    decimals: int = 2

    @property
    def higher_is_better(self) -> bool:
        return self.direction == "higher_is_better"

    def format_value(self, value: float | None) -> str:
        if value is None or value != value:  # NaN
            return "n/a"
        if self.unit == "pct":
            return f"{value * 100:.1f}%"
        if self.unit == "days":
            return f"{value:.0f}d"
        return f"{value:.2f}x"


@dataclass(frozen=True)
class ScoreSpec:
    red_weight: float = 3.0
    amber_weight: float = 1.0
    deterioration_weight: float = 0.5
    deterioration_counts_when_red: bool = False
    red_min_score: float = 12.0
    amber_min_score: float = 4.0

    def band_for_score(self, score: float) -> str:
        if score >= self.red_min_score:
            return "red"
        if score >= self.amber_min_score:
            return "amber"
        return "green"


@dataclass(frozen=True)
class EwsConfig:
    ratios: dict[str, RatioSpec]
    score: ScoreSpec
    source_path: str = ""
    version: Any = 1
    raw: dict = field(default_factory=dict, repr=False)

    @property
    def ratio_keys(self) -> list[str]:
        return list(self.ratios.keys())

    def spec(self, key: str) -> RatioSpec:
        return self.ratios[key]


def _as_number(value: Any, where: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ConfigError(f"{where}: expected a number, got {value!r}")
    return float(value)


def build_config(data: dict, source_path: str = "") -> EwsConfig:
    if "ratios" not in data or not isinstance(data["ratios"], dict) or not data["ratios"]:
        raise ConfigError("config must contain a non-empty 'ratios' mapping")

    specs: dict[str, RatioSpec] = {}
    for key, body in data["ratios"].items():
        where = f"ratios.{key}"
        if not isinstance(body, dict):
            raise ConfigError(f"{where}: expected a mapping")
        missing = [k for k in REQUIRED_RATIO_KEYS if k not in body]
        if missing:
            raise ConfigError(f"{where}: missing required key(s) {', '.join(missing)}")
        direction = str(body["direction"])
        if direction not in DIRECTIONS:
            raise ConfigError(f"{where}.direction must be one of {DIRECTIONS}")
        unit = str(body.get("unit", "x"))
        if unit not in UNITS:
            raise ConfigError(f"{where}.unit must be one of {UNITS}")
        green = _as_number(body["green"], f"{where}.green")
        amber = _as_number(body["amber"], f"{where}.amber")
        if direction == "lower_is_better" and amber < green:
            raise ConfigError(f"{where}: for lower_is_better, amber ({amber}) must be >= green ({green})")
        if direction == "higher_is_better" and amber > green:
            raise ConfigError(f"{where}: for higher_is_better, amber ({amber}) must be <= green ({green})")
        det = _as_number(body.get("deterioration", 0.0), f"{where}.deterioration")
        if det < 0:
            raise ConfigError(f"{where}.deterioration must be >= 0")
        specs[key] = RatioSpec(
            key=key,
            label=str(body["label"]),
            direction=direction,
            unit=unit,
            green=green,
            amber=amber,
            deterioration=det,
            decimals=int(body.get("decimals", 2)),
        )

    score_body = data.get("score") or {}
    if not isinstance(score_body, dict):
        raise ConfigError("score: expected a mapping")
    defaults = ScoreSpec()
    score = ScoreSpec(
        red_weight=_as_number(score_body.get("red_weight", defaults.red_weight), "score.red_weight"),
        amber_weight=_as_number(score_body.get("amber_weight", defaults.amber_weight), "score.amber_weight"),
        deterioration_weight=_as_number(
            score_body.get("deterioration_weight", defaults.deterioration_weight),
            "score.deterioration_weight",
        ),
        deterioration_counts_when_red=bool(
            score_body.get("deterioration_counts_when_red", defaults.deterioration_counts_when_red)
        ),
        red_min_score=_as_number(score_body.get("red_min_score", defaults.red_min_score), "score.red_min_score"),
        amber_min_score=_as_number(
            score_body.get("amber_min_score", defaults.amber_min_score), "score.amber_min_score"
        ),
    )
    if score.red_min_score <= score.amber_min_score:
        raise ConfigError("score.red_min_score must be greater than score.amber_min_score")

    return EwsConfig(ratios=specs, score=score, source_path=source_path, version=data.get("version", 1), raw=data)


def load_config(path: str) -> EwsConfig:
    if not os.path.exists(path):
        raise ConfigError(f"config file not found: {path}")
    data = _read_mapping(path)
    return build_config(data, source_path=path)


def config_rows(cfg: EwsConfig) -> Iterable[dict]:
    """Flatten the applied config into rows for the Config worksheet."""
    rows = []
    for spec in cfg.ratios.values():
        rows.append(
            {
                "ratio": spec.key,
                "label": spec.label,
                "direction": spec.direction,
                "unit": spec.unit,
                "green_threshold": spec.green,
                "amber_threshold": spec.amber,
                "deterioration_trigger": spec.deterioration,
                "weight_if_red": cfg.score.red_weight,
                "weight_if_amber": cfg.score.amber_weight,
                "weight_if_deterioration": cfg.score.deterioration_weight,
            }
        )
    return rows

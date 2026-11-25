"""Config loading: YAML, JSON, the built-in reader, and validation."""

from __future__ import annotations

import json

import pytest

from conftest import CONFIG_PATH
from ews.config import ConfigError, build_config, config_rows, load_config, mini_yaml_load


def test_shipped_yaml_config_loads(cfg):
    assert len(cfg.ratios) == 13
    assert cfg.ratio_keys[0] == "net_debt_ebitda"
    spec = cfg.ratios["net_debt_ebitda"]
    assert spec.green == 3.0
    assert spec.amber == 4.5
    assert spec.deterioration == 0.5
    assert spec.direction == "lower_is_better"
    assert cfg.score.red_weight == 3.0
    assert cfg.score.amber_weight == 1.0
    assert cfg.score.deterioration_weight == 0.5
    assert cfg.score.red_min_score == 12.0
    assert cfg.score.amber_min_score == 4.0


def test_mini_yaml_reader_handles_the_shipped_file(cfg):
    """The built-in reader must agree with the config the loader produced."""
    text = CONFIG_PATH.read_text(encoding="utf-8")
    parsed = mini_yaml_load(text)
    assert parsed["version"] == 1
    assert set(parsed["ratios"]) == set(cfg.ratios)
    assert parsed["ratios"]["interest_coverage"]["green"] == 2.5
    assert parsed["score"]["deterioration_counts_when_red"] is False
    assert parsed["ratios"]["receivable_days"]["green"] == 60


def test_mini_yaml_reader_handles_quotes_lists_and_comments():
    text = """
# a comment
name: "quoted: value"   # trailing comment
nested:
  child:
    flag: true
    label: EBITDA / interest
list:
  - one
  - 2
  - 3.5
blank:
"""
    parsed = mini_yaml_load(text)
    assert parsed["name"] == "quoted: value"
    assert parsed["nested"]["child"]["flag"] is True
    assert parsed["nested"]["child"]["label"] == "EBITDA / interest"
    assert parsed["list"] == ["one", 2, 3.5]
    assert parsed["blank"] is None


def test_json_config_is_equivalent(tmp_path):
    data = {
        "version": 1,
        "score": {"red_weight": 3, "amber_weight": 1, "deterioration_weight": 0.5,
                  "red_min_score": 12, "amber_min_score": 4},
        "ratios": {
            "quick_ratio": {"label": "Quick ratio", "direction": "higher_is_better",
                            "unit": "x", "green": 1.0, "amber": 0.7, "deterioration": 0.1},
        },
    }
    path = tmp_path / "thresholds.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    cfg = load_config(str(path))
    assert cfg.ratios["quick_ratio"].green == 1.0
    assert cfg.ratios["quick_ratio"].deterioration == 0.1


def test_missing_config_file_raises():
    with pytest.raises(ConfigError):
        load_config("does/not/exist.yaml")


def test_config_without_ratios_is_rejected():
    with pytest.raises(ConfigError):
        build_config({"score": {}})


def test_config_missing_required_key_is_rejected():
    with pytest.raises(ConfigError) as exc:
        build_config({"ratios": {"current_ratio": {"label": "Current ratio", "direction": "higher_is_better"}}})
    assert "missing required key" in str(exc.value)


def test_config_with_inverted_bands_is_rejected():
    bad = {"ratios": {"tol_tnw": {"label": "TOL/TNW", "direction": "lower_is_better",
                                  "unit": "x", "green": 3.0, "amber": 2.0}}}
    with pytest.raises(ConfigError) as exc:
        build_config(bad)
    assert "amber" in str(exc.value)


def test_config_with_unknown_direction_is_rejected():
    bad = {"ratios": {"tol_tnw": {"label": "TOL/TNW", "direction": "sideways",
                                  "unit": "x", "green": 2.0, "amber": 3.0}}}
    with pytest.raises(ConfigError):
        build_config(bad)


def test_config_rows_expose_applied_thresholds(cfg):
    rows = list(config_rows(cfg))
    assert len(rows) == 13
    assert {r["ratio"] for r in rows} == set(cfg.ratios)
    quick = next(r for r in rows if r["ratio"] == "quick_ratio")
    assert quick["green_threshold"] == 1.0
    assert quick["weight_if_red"] == cfg.score.red_weight

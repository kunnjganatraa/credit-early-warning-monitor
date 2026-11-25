"""Optional score chart (matplotlib, headless)."""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402

from .scoring import AnalysisResult  # noqa: E402

BAND_COLORS = {"red": "#C00000", "amber": "#E8A33D", "green": "#2E7D32"}


def write_score_chart(result: AnalysisResult, path: str) -> str:
    summary = result.summary.sort_values("score", ascending=True)
    labels = [b if len(b) <= 34 else b[:31] + "..." for b in summary["borrower"].tolist()]
    scores = summary["score"].tolist()
    colors = [BAND_COLORS.get(str(b).lower(), "#808080") for b in summary["band"].tolist()]

    fig, ax = plt.subplots(figsize=(9, 0.55 * len(labels) + 1.6), dpi=150)
    bars = ax.barh(labels, scores, color=colors, height=0.62)
    cfg = result.cfg.score
    ax.axvline(cfg.amber_min_score, color="#7F7F7F", linestyle="--", linewidth=1)
    ax.axvline(cfg.red_min_score, color="#404040", linestyle="--", linewidth=1)
    ax.text(cfg.amber_min_score + 0.3, -0.9, "amber cutoff", fontsize=8, color="#7F7F7F", va="center")
    ax.text(cfg.red_min_score + 0.3, -0.9, "red cutoff", fontsize=8, color="#404040", va="center")
    ax.set_ylim(-1.4, len(labels) - 0.4)
    for bar, score in zip(bars, scores):
        ax.text(bar.get_width() + 0.4, bar.get_y() + bar.get_height() / 2, f"{score:.1f}",
                va="center", fontsize=8)
    ax.set_xlabel("Weighted early-warning score")
    ax.set_title("Credit Early-Warning Monitor - score by borrower", fontsize=11, loc="left")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xlim(0, max(max(scores) * 1.15, cfg.red_min_score * 1.25))
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path

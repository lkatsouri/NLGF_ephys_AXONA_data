"""Shared matplotlib/seaborn figure styling for all notebooks in this repo.

Usage, at the top of a notebook's import cell:

    from figure_style import apply_style, set_panel_title, WT, NLGF
    apply_style()

`apply_style()` must be called AFTER any `sns.set_theme()` / `sns.set_style()`
call, since seaborn's theme is what overrides these rcParams in the first
place. If a notebook calls `sns.set_theme()`/`sns.set_style()` again later
(e.g. before a new figure section), call `apply_style()` again right after it.
"""

import matplotlib.pyplot as plt

FIGURE_RCPARAMS = {
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "font.family": "Arial",
    "axes.grid": False,
    "font.size": 6,
    "axes.labelsize": 6,
    "axes.titlesize": 6,
    "xtick.labelsize": 6,
    "ytick.labelsize": 6,
    "legend.fontsize": 6,
    "axes.linewidth": 0.8,
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
    "xtick.major.size": 3,
    "ytick.major.size": 3,
    "ytick.left": True,
    "ytick.direction": "in",
    "savefig.transparent": True,
    "savefig.bbox": "tight",
    # seaborn's default '#262626' dark grey silently overrides these if left
    # unset, so they're pinned explicitly to true black.
    "text.color": "#000000",
    "axes.labelcolor": "#000000",
    "axes.edgecolor": "#000000",
    "xtick.color": "#000000",
    "ytick.color": "#000000",
}

WT = "#5B8DB8"
NLGF = "#E07B54"


def apply_style():
    """Apply FIGURE_RCPARAMS. Call after any sns.set_theme()/sns.set_style()."""
    plt.rcParams.update(FIGURE_RCPARAMS)


def set_panel_title(ax, label):
    """Set a panel title using the shared bold/larger-than-base title style."""
    ax.set_title(label, fontsize=7, fontweight="bold")

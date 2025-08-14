# src/visualizations/tactics_heatmap.py
import os
import plotly.io as pio
import plotly.express as px
from collections import Counter
from typing import List
from src.db.db_filters import get_configs_core_fields
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from src.visualizations.mitre import MITRE_TACTICS, split_tactics, count_tactics


def build_tactics_heatmap_html(
    out_path: str = "output/tactics_heatmap.html",
) -> str:
    """Build an interactive MITRE tactics heatmap and save as a self-contained HTML."""
    rows = get_configs_core_fields()
    counts = count_tactics(rows)

    fig = px.imshow(
        [counts],
        x=MITRE_TACTICS,
        y=["Coverage"],
        text_auto=True,
        aspect="auto",
        labels=dict(x="MITRE ATT&CK Tactics", y="", color="#Configs"),
    )
    fig.update_layout(
        title="MITRE ATT&CK Tactics Coverage (by # of Configs)",
        width=1000,
        height=320,
        margin=dict(l=20, r=20, t=60, b=40),
        xaxis=dict(tickangle=30),
        coloraxis_showscale=True,
    )

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    pio.write_html(fig, file=out_path, include_plotlyjs=True, full_html=True)
    return out_path


def build_tactics_heatmap_png(
    out_path: str = "output/tactics_heatmap.png",
) -> str:
    from matplotlib.colors import LinearSegmentedColormap

    rows = get_configs_core_fields()
    counts = count_tactics(rows)

    df = pd.DataFrame([counts], columns=MITRE_TACTICS, index=["Coverage"])

    # Dark mode + cyan palette
    radar_cyan_cmap = LinearSegmentedColormap.from_list(
        "radar_cyan",
        ["#0b0b0b", "#0e3a3a", "#00ffff"],  # dark → teal → cyan
        N=256,
    )

    plt.figure(figsize=(12, 1.6), facecolor="#121212")
    sns.set_theme(
        style="ticks",
        rc={
            "axes.facecolor": "#121212",
            "figure.facecolor": "#121212",
            "axes.labelcolor": "white",
            "xtick.color": "white",
            "ytick.color": "white",
            "axes.edgecolor": "#333333",
        },
    )
    ax = sns.heatmap(
        df,
        annot=True,
        fmt="d",
        cmap=radar_cyan_cmap,
        cbar_kws={"label": "# Configs", "ticks": [df.min().min(), df.max().max()]},
        linewidths=0.5,
        linecolor="#333333",
        annot_kws={"color": "white"},
    )

    ax.set_title(
        "MITRE ATT&CK Tactics Coverage (by # of Configs)", color="white", pad=12
    )
    ax.tick_params(axis="x", colors="white", rotation=30)
    ax.tick_params(axis="y", colors="white", rotation=0)

    plt.subplots_adjust(
        top=0.80,  # enough room for the title
        bottom=0.40,  # enough room for rotated tactic labels
        left=0.20,  # keep y-axis label visible
        right=0.92,  # keep colorbar visible
    )
    plt.subplots_adjust(bottom=0.50)  # Leave room for tactic labels
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path, dpi=200, facecolor="#121212")
    plt.close()
    return out_path


# def build_tactics_heatmap_png(
#     out_path: str = "output/tactics_heatmap.png",
#     palette: str = "flare",  # You can change: mako, viridis, flare, crest
# ) -> str:
#     import pandas as pd

#     rows = get_configs_core_fields()
#     counts = count_tactics(rows)

#     df = pd.DataFrame([counts], columns=MITRE_TACTICS, index=["Coverage"])

#     # Dark mode style
#     plt.figure(figsize=(12, 1.6), facecolor="#121212")
#     sns.set_theme(style="dark")  # Dark background
#     ax = sns.heatmap(
#         df,
#         annot=True,
#         fmt="d",
#         cmap=palette,
#         cbar_kws={"label": "# Configs"},
#         linewidths=0.5,
#         linecolor="#333333",
#         annot_kws={"color": "white"},  # White text annotations
#     )

#     # Dark mode titles and labels
#     ax.set_title(
#         "MITRE ATT&CK Tactics Coverage (by # of Configs)", color="white", pad=12
#     )
#     ax.tick_params(axis="x", colors="white", rotation=30)
#     ax.tick_params(axis="y", colors="white", rotation=0)
#     ax.figure.set_facecolor("#121212")

#     plt.tight_layout()
#     os.makedirs(os.path.dirname(out_path), exist_ok=True)
#     plt.savefig(out_path, dpi=200, facecolor="#121212")  # Dark background saved
#     plt.close()
#     return out_path

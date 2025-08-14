# src/visualizations/tactics_radar.py
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.projections.polar import PolarAxes
from src.visualizations.mitre import MITRE_TACTICS, count_tactics
from src.db.db_filters import get_configs_core_fields


def build_tactics_radar_png(out_path: str = "output/tactics_radar.png") -> str:
    """
    Generate a MITRE ATT&CK tactics coverage radar chart in dark mode.

    Args:
        out_path (str, optional): Output PNG file path. Defaults to 'output/tactics_radar.png'.

    Returns:
        str: Path to the generated PNG file.
    """
    # Get data from DB and count tactics using shared logic
    rows = get_configs_core_fields()
    counts = count_tactics(rows)
    values = counts + [counts[0]]  # close the radar loop
    angles = np.linspace(0, 2 * np.pi, len(MITRE_TACTICS) + 1)

    # Dark mode figure
    plt.figure(figsize=(8, 8), facecolor="#121212")
    ax: PolarAxes = plt.subplot(111, polar=True)  # type: ignore
    ax.set_facecolor("#121212")

    # Plot data
    ax.plot(angles, values, color="#00FFFF", linewidth=2)
    ax.fill(angles, values, color="#00FFFF", alpha=0.25)

    # Axes styling
    ax.set_theta_offset(np.pi / 2.0)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(
        np.degrees(angles[:-1]), labels=MITRE_TACTICS, fontsize=10, color="white"
    )
    ax.set_rlabel_position(0)
    plt.yticks(color="white")
    ax.tick_params(colors="white")

    # Title
    ax.set_title(
        "MITRE ATT&CK Tactics Coverage Radar", color="white", fontsize=14, pad=20
    )

    # Save
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path, dpi=200, facecolor="#121212")
    plt.close()
    return out_path

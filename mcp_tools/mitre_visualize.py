from fastmcp import FastMCP
from typing import Annotated
from pydantic import Field
from src.visualizations.tactics_heatmap import build_tactics_heatmap_png
from src.visualizations.tactics_radar import build_tactics_radar_png


mcp = FastMCP("MITRE Visualizations")


@mcp.tool()
def tactics_heatmap_png(no_input_required: str) -> str:
    """
    Generate a MITRE ATT&CK tactics coverage heatmap (Seaborn static PNG)
    and return the PNG file path.

    Args:
        blank (str, optional): Dummy param to absorb bad clients that send {"": ""}.
                               Ignored by the tool.
    Returns:
        str: Path to the generated PNG file.
    """
    return build_tactics_heatmap_png()


@mcp.tool()
def tactics_radar_png(no_input_required: str) -> str:
    """
    Generate a MITRE ATT&CK tactics coverage radar chart (dark mode PNG)
    and return the PNG file path.
    """
    return build_tactics_radar_png()

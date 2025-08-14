from fastmcp import FastMCP
from src.stats.basic_stats import build_basic_stats_json, build_recent_changes_json

mcp = FastMCP("Configuration Settings Stats")


@mcp.tool()
def get_basic_stats_json() -> dict:
    """Return baseline statistics in JSON form."""
    return build_basic_stats_json()


@mcp.tool()
def get_recent_changes_json(days: int = 30) -> dict:
    """Return recent changes in JSON form."""
    return build_recent_changes_json(days)


@mcp.tool()
def get_combined_stats(days: int = 30) -> dict:
    """
    Return both basic stats and recent changes in one JSON object.
    Useful for prompts like:
    'tell me the basic stats and recent changes last 30 days in a simple report'
    """
    return {
        "basic_stats": build_basic_stats_json(),
        "recent_changes": build_recent_changes_json(days),
    }

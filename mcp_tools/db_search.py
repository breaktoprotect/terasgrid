from fastmcp import FastMCP
from typing import List, Dict, Any
from src.search import semantic_search
from src.db.db_filters import get_configs_missing_mitre

mcp = FastMCP("Current System Configuration Settings Search")


@mcp.tool()
def semantic_search_configs(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Perform a semantic search across all stored configuration settings.

    Args:
        query (str): Natural-language or keyword search query.
        top_k (int, optional): Max number of matching records to return.

    Returns:
        List[Dict[str, Any]]: Matching records with similarity scores.
    """
    return semantic_search(query=query, top_k=top_k)


@mcp.tool()
def semantic_search_with_filter(
    query: str, top_k: int = 5, status: str = "active"
) -> List[Dict[str, Any]]:
    """
    Semantic search with an optional status filter.

    Args:
        query (str): Natural-language query.
        top_k (int, optional): Max number of results to return.
        status (str, optional): Filter by config status.

    Returns:
        List[Dict[str, Any]]: Filtered matching records with similarity scores.
    """
    return semantic_search(query=query, top_k=top_k, status=status)


@mcp.tool()
def get_missing_records_without_mitre_attack_info() -> list:
    """
    Retrieve configs missing MITRE tactic or technique mapping.

    Returns:
        list: Records with empty MITRE tactic/technique fields.
    """
    rows = get_configs_missing_mitre()
    return [dict(row) for row in rows]

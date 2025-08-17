# src/stats/basic_stats.py
from datetime import datetime, timedelta

from config import CORE_DB_PATH, CSV_COLUMN_MAP
from src.db.schema_map import pk_field
from src.db.db_init import get_db


def build_basic_stats_json() -> dict:
    """Builds basic statistics about configuration settings in the DB."""
    conn = get_db(CORE_DB_PATH)
    cur = conn.cursor()

    pk = pk_field()
    status_col = CSV_COLUMN_MAP["status_mandatory"]

    # Count all configs
    total = cur.execute(f"SELECT COUNT({pk}) FROM configs").fetchone()[0]

    # Count configs with both MITRE fields populated
    mapped_mitre = cur.execute(
        f"""
        SELECT COUNT({pk}) FROM configs
        WHERE TRIM(mitre_tactic) != '' AND TRIM(mitre_technique) != ''
        """
    ).fetchone()[0]

    unmapped_mitre = total - mapped_mitre

    # Status breakdown
    status_counts = dict(
        cur.execute(
            f"SELECT {status_col}, COUNT(*) FROM configs GROUP BY {status_col}"
        ).fetchall()
    )

    conn.close()

    return {
        "total_configs": total,
        "mapped_mitre": mapped_mitre,
        "mapped_percent": round((mapped_mitre / total) * 100, 2) if total else 0.0,
        "unmapped_mitre": unmapped_mitre,
        "unmapped_percent": round((unmapped_mitre / total) * 100, 2) if total else 0.0,
        "status_breakdown": status_counts,
    }


def build_recent_changes_json(days: int = 30) -> dict:
    """Builds statistics of LLM/MCP tool usage in the last N days."""
    conn = get_db(CORE_DB_PATH)
    cur = conn.cursor()

    cutoff = (datetime.now() - timedelta(days=days)).isoformat(timespec="seconds")
    recent_rows = cur.execute(
        """
        SELECT tool, COUNT(*) as cnt
        FROM llm_action_log
        WHERE ts >= ?
        GROUP BY tool
        ORDER BY cnt DESC
        """,
        (cutoff,),
    ).fetchall()

    conn.close()

    return {
        "lookback_days": days,
        "changes": [{"tool": tool, "count": cnt} for tool, cnt in recent_rows],
    }

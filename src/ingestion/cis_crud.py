from typing import Optional, List, Dict
from config import TEMP_DB_PATH
from src.db.db_init import get_db


def list_cis_tables() -> List[str]:
    """Return all table names in TEMP_DB_PATH."""
    with get_db(TEMP_DB_PATH) as conn:
        rows = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()
        return [row["name"] for row in rows]


def get_cis_table(table_name: str) -> List[Dict]:
    """Return all rows from the given CIS table as dicts."""
    with get_db(TEMP_DB_PATH) as conn:
        rows = conn.execute(f"SELECT * FROM {table_name} ORDER BY number").fetchall()
        return [dict(r) for r in rows]


def get_one_unreviewed_record(table_name: str) -> Dict:
    """Return one unreviewed record from the given table."""
    with get_db(TEMP_DB_PATH) as conn:
        row = conn.execute(
            f"""
            SELECT * FROM {table_name}
            WHERE reviewed = 0
            ORDER BY number
            LIMIT 1
            """
        ).fetchone()

        return {} if not row else {k: row[k] for k in row.keys()}


def mark_one_record_reviewed(
    table_name: str, number: str, reviewed: Optional[int] = 1
) -> str:
    """Mark a CIS benchmark record as reviewed/unreviewed."""
    with get_db(TEMP_DB_PATH) as conn:
        cur = conn.execute(
            f"""
            UPDATE {table_name}
            SET reviewed = ?
            WHERE number = ?
            """,
            (reviewed, number),
        )
        conn.commit()

        if cur.rowcount == 0:
            return f"[WARN] No record found for number '{number}'."
        return f"[OK] Record '{number}' updated to reviewed={reviewed}."

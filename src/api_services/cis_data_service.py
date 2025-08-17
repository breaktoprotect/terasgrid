from config import TEMP_DB_PATH
from src.db.db_init import get_db
from src.ingestion.cis_crud import list_cis_tables, get_cis_table


def list_cis_tables_available():
    """
    Return only benchmark-related CIS tables (ignore system/meta tables).
    """
    tables = list_cis_tables()
    return [
        table
        for table in tables
        if table.startswith("cis_")
        and table not in {"sqlite_sequence", "ingestion_meta"}
    ]


def get_cis_table_data(table_name: str):
    """
    Return all columns for a given CIS table.
    The UI will decide which subset of columns to display.
    """
    rows = get_cis_table(table_name)
    return [dict(r) for r in rows]


def get_cis_table_stats(table_name: str):
    with get_db(TEMP_DB_PATH) as conn:
        row = conn.execute(
            f"""
            SELECT
              COUNT(*) as total,
              SUM(CASE WHEN reviewed=1 THEN 1 ELSE 0 END) as reviewed,
              SUM(CASE WHEN reviewed=0 THEN 1 ELSE 0 END) as unreviewed
            FROM {table_name}
        """
        ).fetchone()
        return dict(row)

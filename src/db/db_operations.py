import sqlite3
from typing import Any, List, Tuple, Optional

from config import DB_PATH
from src.db.db_init import get_db
from src.db.schema_map import pk_field


def execute_query(
    query: str, params: Tuple = (), commit: bool = False, db_path: str = DB_PATH
) -> int:
    """Execute INSERT/UPDATE/DELETE without returning results. Returns affected row count."""
    with get_db(db_path) as conn:
        cur = conn.execute(query, params)
        if commit:
            conn.commit()
        return cur.rowcount


def fetch_one(
    query: str, params: Tuple = (), db_path: str = DB_PATH
) -> Optional[sqlite3.Row]:
    """Fetch a single row."""
    with get_db(db_path) as conn:
        return conn.execute(query, params).fetchone()


def fetch_all(
    query: str, params: Tuple = (), db_path: str = DB_PATH
) -> List[sqlite3.Row]:
    """Fetch multiple rows."""
    with get_db(db_path) as conn:
        return conn.execute(query, params).fetchall()


# --- CRUD helpers ---
def insert(table: str, data: dict, db_path: str = DB_PATH) -> int:
    if not data:
        raise ValueError("insert() received empty data dict")
    cols = ", ".join(data.keys())
    placeholders = ", ".join("?" for _ in data)
    sql = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
    return execute_query(sql, tuple(data.values()), commit=True, db_path=db_path)


def update(
    table: str, data: dict, where: str, params: Tuple, db_path: str = DB_PATH
) -> int:
    if not data:
        return 0  # nothing to update
    set_clause = ", ".join(f"{col}=?" for col in data.keys())
    sql = f"UPDATE {table} SET {set_clause} WHERE {where}"
    return execute_query(
        sql, tuple(data.values()) + params, commit=True, db_path=db_path
    )


def delete(table: str, where: str, params: Tuple, db_path: str = DB_PATH) -> int:
    sql = f"DELETE FROM {table} WHERE {where}"
    return execute_query(sql, params, commit=True, db_path=db_path)


def update_by_pk(table: str, pk_value: Any, data: dict, db_path: str = DB_PATH) -> int:
    """
    Update a single record in `table` by its primary key.
    The primary key column name is determined via schema_map.pk_field().
    """
    pk_col = pk_field()
    return update(
        table, data, where=f"{pk_col} = ?", params=(pk_value,), db_path=db_path
    )


def delete_by_pk(table: str, pk_value: Any, db_path: str = DB_PATH) -> int:
    """Delete a record by primary key using schema_map.pk_field()."""
    pk_col = pk_field()
    return delete(table, where=f"{pk_col} = ?", params=(pk_value,), db_path=db_path)

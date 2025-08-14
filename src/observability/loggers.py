# src/observability/writers.py
import json
import sqlite3
from datetime import datetime
from typing import Optional, Dict, Any, Union

from config import DB_PATH, CSV_COLUMN_MAP


def _now_iso() -> str:
    # Local time with offset; ISO is easy to read and sort
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _pk_to_json(pk: Union[str, Dict[str, Any]]) -> str:
    """
    Normalize primary key:
      - If str, wrap with PK field from schema map: {"<pk_field>": "value"}
      - If dict, use as-is
    """
    if isinstance(pk, str):
        pk_field = CSV_COLUMN_MAP["unique_id_mandatory"]
        pk = {pk_field: pk}
    return json.dumps(pk, ensure_ascii=False)


def log_llm_action(
    *,
    tool: str,  # e.g., "insert_config"
    pk: Union[str, Dict[str, Any]],  # "CONF-1" or {"config_id":"CONF-1"}
    reason: Optional[str] = None,  # short justification
    actor: str = "llm",
    request_id: Optional[str] = None
) -> None:
    """Log a single LLM/MCP tool action (non-idempotent only)."""
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            """
            INSERT INTO llm_action_log (ts, tool, pk_json, reason, actor, request_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (_now_iso(), tool, _pk_to_json(pk), reason, actor, request_id),
        )
        conn.commit()
    finally:
        conn.close()


def log_db_op(
    *,
    action: str,  # "insert" | "update" | "delete"
    table_name: str,  # e.g., "configs"
    pk: Union[str, Dict[str, Any]],
    rows_affected: int,
    success: bool = True,
    actor: Optional[str] = None,  # "llm" | "api" | "human" | "system"
    tool: Optional[str] = None,
    error: Optional[str] = None
) -> None:
    """Log a DB operation regardless of origin (MCP/API/CLI)."""
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            """
            INSERT INTO db_op_log (ts, action, table_name, pk_json, rows_affected, success, actor, tool, error)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                _now_iso(),
                action,
                table_name,
                _pk_to_json(pk),
                int(rows_affected),
                1 if success else 0,
                actor,
                tool,
                error,
            ),
        )
        conn.commit()
    finally:
        conn.close()

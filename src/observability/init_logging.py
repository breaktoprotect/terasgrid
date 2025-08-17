# src/observability/init_logging.py
import sqlite3
from config import CORE_DB_PATH


def init_logging() -> None:
    """Create minimal tables for LLM tool logs and DB operation logs."""
    conn = sqlite3.connect(CORE_DB_PATH)
    try:
        # 1) High-level LLM/MCP tool actions (non-idempotent only)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS llm_action_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts TEXT NOT NULL,              -- ISO timestamp
                tool TEXT NOT NULL,            -- e.g., 'insert_config'
                pk_json TEXT NOT NULL,         -- e.g., {"config_id":"CONF-1"}
                reason TEXT,                   -- LLM justification (short)
                actor TEXT NOT NULL DEFAULT 'llm',
                request_id TEXT                -- optional correlation id
            );
        """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_llm_ts ON llm_action_log(ts);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_llm_tool ON llm_action_log(tool);")

        # 2) Low-level DB operations (all origins)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS db_op_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts TEXT NOT NULL,
                action TEXT NOT NULL,          -- insert | update | delete
                table_name TEXT NOT NULL,      -- e.g., 'configs'
                pk_json TEXT NOT NULL,
                rows_affected INTEGER NOT NULL,
                success INTEGER NOT NULL,      -- 1/0
                actor TEXT,                    -- 'llm' | 'api' | 'human' | 'system'
                tool TEXT,                     -- if known; e.g., 'insert_config' or 'api:POST /configs'
                error TEXT                     -- nullable error message
            );
        """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_db_ts ON db_op_log(ts);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_db_action ON db_op_log(action);")
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_db_table ON db_op_log(table_name);"
        )
        conn.commit()
        print("[+] observability: llm_action_log & db_op_log ready.")
    finally:
        conn.close()

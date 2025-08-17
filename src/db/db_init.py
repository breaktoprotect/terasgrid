import sqlite3
import sqlite_vec
from typing import Optional
from config import CORE_DB_PATH, MODEL_ID, TEMP_DB_PATH
from sentence_transformers import SentenceTransformer


def get_db(db_path: str = CORE_DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.enable_load_extension(True)
    sqlite_vec.load(conn)
    conn.enable_load_extension(False)
    conn.row_factory = sqlite3.Row
    return conn


def get_embed_dim() -> int:
    """Load the configured SBERT model and return embedding dimension."""
    model = SentenceTransformer(MODEL_ID)
    # Small dummy encode to determine dimension
    return model.encode(["_"], convert_to_numpy=True, normalize_embeddings=True)[
        0
    ].shape[0]


def init_core_schema(conn: sqlite3.Connection, *, embed_dim: int) -> None:
    conn.execute("DROP TABLE IF EXISTS configs;")
    conn.execute("DROP TABLE IF EXISTS vec_configs;")
    conn.execute(
        """
        CREATE TABLE configs(
            config_id TEXT PRIMARY KEY,
            status TEXT NOT NULL,
            config_name TEXT NOT NULL,
            config_desc TEXT NOT NULL,
            config_settings TEXT NOT NULL,
            role_applicability TEXT NOT NULL DEFAULT '' CHECK (role_applicability IN ('', 'Member Server', 'Domain Controller', 'All Roles')),      
            os_version_applicability TEXT NOT NULL DEFAULT '', 
            mitre_tactic TEXT NOT NULL DEFAULT '',
            mitre_technique TEXT NOT NULL DEFAULT ''
        );
    """
    )
    conn.execute(
        f"""
        CREATE VIRTUAL TABLE vec_configs USING vec0(
            config_id TEXT PRIMARY KEY,
            embedding float[{embed_dim}]
        );
    """
    )


def init_observability(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS llm_action_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL,
            tool TEXT NOT NULL,
            pk_json TEXT NOT NULL,
            reason TEXT,
            actor TEXT NOT NULL DEFAULT 'llm',
            request_id TEXT
        );
    """
    )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_llm_ts ON llm_action_log(ts);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_llm_tool ON llm_action_log(tool);")
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS db_op_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL,
            action TEXT NOT NULL,
            table_name TEXT NOT NULL,
            pk_json TEXT NOT NULL,
            rows_affected INTEGER NOT NULL,
            success INTEGER NOT NULL,
            actor TEXT,
            tool TEXT,
            error TEXT
        );
    """
    )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_db_ts ON db_op_log(ts);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_db_action ON db_op_log(action);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_db_table ON db_op_log(table_name);")


def init_benchmark_db(db_path: str = TEMP_DB_PATH) -> None:
    """Create an empty benchmark DB file with WAL + synchronous settings, no tables yet."""
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.row_factory = sqlite3.Row
    conn.close()


def init_benchmark_meta_table(conn: sqlite3.Connection) -> None:
    """
    Create a simple ingestion_meta table to track ingested files and prevent duplicates.
    """
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS ingestion_meta (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_name TEXT NOT NULL UNIQUE,
            file_hash TEXT NOT NULL UNIQUE,
            filename TEXT NOT NULL,
            standard TEXT NOT NULL,   -- e.g. CIS, STIG, MS-Baseline
            ts TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_ingest_hash ON ingestion_meta(file_hash);"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_ingest_standard ON ingestion_meta(standard);"
    )


def init_all(*, include_observability: bool = True) -> None:
    """Initialize DB with core + optional observability schema, auto-resolving embed_dim."""
    embed_dim = get_embed_dim()

    # * Core DB
    with get_db(CORE_DB_PATH) as conn:
        init_core_schema(conn, embed_dim=embed_dim)
        if include_observability:
            init_observability(conn)
        conn.commit()

    # * Temp DB (e.g. for benchmarks, etc)
    init_benchmark_db()

    # * Benchmark Metadata table
    with get_db(TEMP_DB_PATH) as conn:
        init_benchmark_meta_table(conn)
        conn.commit()

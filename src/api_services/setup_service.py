from src.db.db_reset import destroy_dbs
from src.db.db_init import init_all
from src.ingestion.ingest_core import ingest
from src.observability.loggers import log_db_op


def reset_and_ingest():
    """
    Reset, re-init schema, and ingest baseline configs from CSV_PATH.
    Logs with actor=API for audit.
    """
    destroy_dbs()
    init_all(include_observability=True)
    row_count = ingest()  # <-- now captures the number of rows

    log_db_op(
        action="reset_and_ingest",
        table_name="configs + vec_configs",
        pk="*",
        rows_affected=row_count,
        actor="api",
        success=True,
    )

    return {
        "status": "ok",
        "message": f"Database reset and ingested via API with {row_count} rows",
    }

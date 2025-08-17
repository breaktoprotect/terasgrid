# src/api_services/baseline_automation_service.py
from src.api_services import cis_ingestion_service
from mcp_tools import cis_crud_tool, db_search, db_crud
from src.ingestion.cis_crud import get_cis_table
import threading
import time

progress: dict[str, dict] = {}


def upload_and_ingest(
    pdf_path: str, start_page: int = 36, filename_hint: str | None = None
):
    """
    Wrapper: ingest CIS PDF into temp DB and return ingestion summary.

    Args:
        pdf_path: Path to the CIS benchmark PDF file.
        start_page: Page number to start parsing from.
        filename_hint: Optional safe string (e.g., uploaded filename) used to
                       derive the DB table name instead of a tmp path.

    Returns:
        dict with ingestion summary.
    """
    table_name, title, version, count = cis_ingestion_service.ingest_cis_pdf(
        pdf_path, start_page=start_page, filename_hint=filename_hint
    )
    return {
        "status": "ok",
        "message": f"Ingested {count} CIS recommendations into table '{table_name}'",
        "table": table_name,
        "title": title,
        "version": version,
        "records": count,
    }


def harden(table_name: str, total: int = 5):
    """
    Start a fake hardening workflow in a background thread.
    Returns immediately; progress can be checked via get_progress().
    """
    # initialize progress entry
    progress[table_name] = {"done": 0, "total": total, "status": "running"}

    t = threading.Thread(
        target=_simulate_hardening, args=(table_name, total), daemon=True
    )
    t.start()

    return {"status": "started", "table": table_name, "total": total}


def get_progress(table_name: str):
    """
    Return current hardening progress for a given CIS table.
    """
    return progress.get(table_name, {"done": 0, "total": 0, "status": "not_started"})


# --- Internal helpers ---


def _simulate_hardening(table_name: str, total: int, delay: float = 1.0):
    """
    Worker that simulates record-by-record hardening with time.sleep.
    """
    for reviewed in range(1, total + 1):
        time.sleep(delay)  # simulate processing work
        progress[table_name] = {"done": reviewed, "total": total, "status": "running"}

    progress[table_name]["status"] = "complete"

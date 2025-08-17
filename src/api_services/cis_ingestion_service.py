from pathlib import Path
from src.ingestion.ingest_cis import ingest_cis_pdf


def ingest_cis(pdf_path: str, start_page: int = 2) -> dict:
    """
    Service wrapper for CIS PDF ingestion.
    Calls the ingestion layer and returns a JSON-serializable dict.
    """
    table_name, title, version, count = ingest_cis_pdf(pdf_path, start_page=start_page)

    return {
        "status": "ok",
        "table_name": table_name,
        "title": title,
        "version": version,
        "records_ingested": count,
        "source_file": Path(pdf_path).name,
    }

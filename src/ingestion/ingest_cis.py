# src/ingestion/ingest_cis.py
import re
import hashlib
import sqlite3
from pathlib import Path
import external_tools.cisbenchmarkconverter.cis_benchmark_converter as cbc
from src.ingestion.db.db_ingest_cis import create_cis_table, bulk_insert_cis_records
from src.ingestion.cis_crud import list_cis_tables
from src.db.db_init import get_db, TEMP_DB_PATH


def sanitize_table_name(filename: str) -> str:
    """Sanitize filename into a safe SQLite table name (lowercase, underscores)."""
    base = Path(filename).stem.lower()
    base = re.sub(r"[^a-z0-9_]", "_", base)
    return base[:40]  # enforce max length


def unique_table_name(base_name: str) -> str:
    """Ensure the table name is unique by adding suffix if necessary."""
    existing = set(list_cis_tables())
    candidate = base_name
    counter = 2
    while candidate in existing:
        candidate = f"{base_name}_{counter}"
        counter += 1
    return candidate


def compute_file_hash(path: Path) -> str:
    """Compute SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def ingest_cis_pdf(
    pdf_path: str,
    start_page: int = 2,
    filename_hint: str | None = None,
):
    """
    Ingest a CIS benchmark PDF into the temporary database.

    Args:
        pdf_path (str): Path to the CIS PDF file.
        start_page (int): Page number where recommendations begin.
        filename_hint (str | None): Optional original filename (from upload).

    Returns:
        tuple: (table_name, title, version, record_count)
    """
    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    # --- Hash & dedup check
    file_hash = compute_file_hash(pdf_file)

    with get_db(TEMP_DB_PATH) as conn:
        row = conn.execute(
            "SELECT table_name FROM ingestion_meta WHERE file_hash = ?",
            (file_hash,),
        ).fetchone()

        if row:
            raise ValueError(
                f"Duplicate ingestion prevented. File already ingested as table '{row['table_name']}'."
            )

    # Prefer hint → fall back to actual PDF name
    raw_name = filename_hint if filename_hint else pdf_file.name
    base_name = sanitize_table_name(raw_name)
    table_name = unique_table_name(base_name)

    # --- Extract metadata + recommendations
    title, version = cbc.extract_title_and_version(pdf_file)
    pdf_text = cbc.read_pdf(pdf_file, start_page=start_page)
    recommendations = cbc.extract_recommendations(pdf_text)

    # --- Create staging table + insert records
    create_cis_table(table_name)
    bulk_insert_cis_records(table_name, recommendations)

    # --- Insert ingestion metadata
    with get_db(TEMP_DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO ingestion_meta (table_name, file_hash, filename, standard)
            VALUES (?, ?, ?, ?)
            """,
            (table_name, file_hash, raw_name, "CIS"),
        )
        conn.commit()

    return table_name, title, version, len(recommendations)

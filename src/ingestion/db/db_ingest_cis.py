from typing import List, Dict
from config import TEMP_DB_PATH
from src.db.db_init import get_db


def create_cis_table(table_name: str) -> None:
    """Create (or replace) the CIS table for this benchmark PDF."""
    with get_db(TEMP_DB_PATH) as conn:
        conn.execute(f"DROP TABLE IF EXISTS {table_name}")
        conn.execute(
            f"""
            CREATE TABLE {table_name} (
                reviewed INTEGER DEFAULT 0,
                number TEXT PRIMARY KEY,
                level TEXT,
                title TEXT,
                profile_applicability TEXT,
                description TEXT,
                rationale TEXT,
                impact TEXT,
                audit TEXT,
                remediation TEXT,
                default_value TEXT,
                reference TEXT,
                additional_information TEXT
            );
            """
        )
        conn.commit()


def bulk_insert_cis_records(table_name: str, records: List[Dict]) -> None:
    """Insert multiple CIS recommendation records into the given table."""
    with get_db(TEMP_DB_PATH) as conn:
        for rec in records:
            conn.execute(
                f"""
                INSERT OR IGNORE INTO {table_name} (
                    reviewed, number, level, title,
                    profile_applicability, description, rationale, impact, audit,
                    remediation, default_value, reference, additional_information
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    0,  # reviewed flag (0 = unprocessed)
                    rec.get("Number", ""),
                    rec.get("Level", ""),
                    rec.get("Title", ""),
                    rec.get("Profile Applicability", ""),
                    rec.get("Description", ""),
                    rec.get("Rationale", ""),
                    rec.get("Impact", ""),
                    rec.get("Audit", ""),
                    rec.get("Remediation", ""),
                    rec.get("Default Value", ""),
                    rec.get("References", ""),
                    rec.get("Additional Information", ""),
                ),
            )
        conn.commit()

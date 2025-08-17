import sqlite3
from typing import List, Optional

from config import CORE_DB_PATH, CSV_COLUMN_MAP
from src.db.db_operations import fetch_all, update
from src.db.schema_map import pk_field


def get_configs_missing_mitre(db_path: str = CORE_DB_PATH) -> List[sqlite3.Row]:
    """
    Retrieve configuration records where mitre_tactic or mitre_technique are empty.
    Useful for finding rows that still need enrichment.
    """
    mt_col = CSV_COLUMN_MAP["mitre_tactic_optional"]
    mtech_col = CSV_COLUMN_MAP["mitre_technique_optional"]

    sql = f"""
        SELECT *
        FROM configs
        WHERE ({mt_col} IS NULL OR TRIM({mt_col}) = '')
           OR ({mtech_col} IS NULL OR TRIM({mtech_col}) = '')
    """
    return fetch_all(sql, db_path=db_path)


def update_mitre_fields(
    config_id: str,
    mitre_tactic: Optional[str] = None,
    mitre_technique: Optional[str] = None,
    db_path: str = CORE_DB_PATH,
) -> None:
    """Update exactly one tactic and/or one technique for a given config_id."""
    fields = {}
    if mitre_tactic is not None:
        mt = mitre_tactic.strip()
        if mt:
            fields[CSV_COLUMN_MAP["mitre_tactic_optional"]] = mt
    if mitre_technique is not None:
        mtech = mitre_technique.strip()
        if mtech:
            fields[CSV_COLUMN_MAP["mitre_technique_optional"]] = mtech
    if not fields:
        return

    update(
        "configs",
        fields,
        f"{CSV_COLUMN_MAP['unique_id_mandatory']} = ?",
        (config_id,),
        db_path=db_path,
    )


def get_configs_core_fields(db_path: str = CORE_DB_PATH) -> List[sqlite3.Row]:
    """
    Return the core columns used by visualizations.
    """
    id_col = CSV_COLUMN_MAP["unique_id_mandatory"]
    name_col = CSV_COLUMN_MAP["name_mandatory"]
    desc_col = CSV_COLUMN_MAP["description_mandatory"]
    settings_col = CSV_COLUMN_MAP["settings_optional"]
    status_col = CSV_COLUMN_MAP["status_mandatory"]
    mt_col = CSV_COLUMN_MAP["mitre_tactic_optional"]
    mtech_col = CSV_COLUMN_MAP["mitre_technique_optional"]

    sql = f"""
        SELECT
            {id_col},
            {name_col},
            {desc_col},
            {settings_col},
            {status_col},
            COALESCE({mt_col}, '')    AS {mt_col},
            COALESCE({mtech_col}, '') AS {mtech_col}
        FROM configs
    """
    return fetch_all(sql, db_path=db_path)

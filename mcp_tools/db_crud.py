from fastmcp import FastMCP
from typing import Dict, Any, Optional

from src.db.db_filters import update_mitre_fields
from src.observability.loggers import log_llm_action
from src.db.schema_map import pk_field
from src.db.db_paired_ops import (
    insert_config_with_embedding,
    update_config_with_embedding,
)
from config import CSV_COLUMN_MAP
from src.db.id_utils import generate_unique_id

mcp = FastMCP("Configuration Settings CRUD Operations")


@mcp.tool()
def insert_config_simple(
    config_name: str,
    config_desc: str,
    config_settings: str,
    reason: str,
    request_id: Optional[str] = None,
) -> str:
    """
    Insert a new configuration with only the essential fields:
      - config_name: Name/title of the configuration
      - config_desc: Detailed description
      - config_settings: Registry path(s), GPO setting(s), or command(s)

    All other fields are auto-filled:
      • config_id is auto-generated (NEW_<hash>)
      • status is set to "pending"
      • Any unused columns are set to empty strings.

    Inserts into:
      • Main table (`configs`)
      • Vector table (`vec_configs`)
    """
    pk_col = pk_field()
    status_col = CSV_COLUMN_MAP["status_mandatory"]

    # Auto-generate ID and set status
    new_id = generate_unique_id(
        {
            "config_name": config_name,
            "config_desc": config_desc,
            "config_settings": config_settings,
        }
    )

    record = {
        pk_col: new_id,
        "config_name": config_name.strip(),
        "config_desc": config_desc.strip(),
        "config_settings": config_settings.strip(),
        status_col: "pending",
    }

    # Fill in other expected columns as blanks if they exist in schema
    for col in CSV_COLUMN_MAP.values():
        if col not in record:
            record[col] = ""

    log_llm_action(
        tool="insert_config_simple",
        pk={pk_col: new_id},
        reason=reason,
        request_id=request_id,
        actor="llm",
    )

    insert_config_with_embedding(record)
    return f"Inserted {pk_col}={new_id} with status='pending'."


# @mcp.tool()
# def insert_config(
#     data: Dict[str, Any],
#     reason: str,
#     request_id: Optional[str] = None,
# ) -> str:
#     """
#     Create a new configuration record and generate its embedding.

#     Automatically:
#       • Generates the primary key in the form: NEW_<7-char MD5 hash>
#       • Sets status to "pending"

#     Inserts into:
#       • Main table (`configs`)
#       • Vector table (`vec_configs`)
#     """
#     pk_col = pk_field()
#     status_col = CSV_COLUMN_MAP["status_mandatory"]

#     # Auto-generate PK and enforce pending status
#     data[pk_col] = generate_unique_id(data)
#     data[status_col] = "pending"

#     log_llm_action(
#         tool="insert_config",
#         pk={pk_col: data[pk_col]},
#         reason=reason,
#         request_id=request_id,
#         actor="llm",
#     )

#     insert_config_with_embedding(data)
#     return f"Inserted {pk_col}={data[pk_col]} with status='pending' into configs and vec_configs."


@mcp.tool()
def update_config(
    config_id: str,
    updates: Dict[str, Any],
    reason: Optional[str] = None,
    request_id: Optional[str] = None,
) -> str:
    """
    Update one or more fields for an existing configuration.

    If any embedding-relevant fields change, the corresponding vector in
    `vec_configs` is also updated.

    Args:
        config_id: Primary key of the configuration to update.
        updates: Dict of column names and new values.
        reason: Short, audit-ready explanation for the update.
        request_id: Optional correlation ID for traceability.

    Returns:
        Confirmation message of updated fields.

    Notes:
        • Primary key cannot be changed.
        • No action if `updates` is empty.
        • Logs to `llm_action_log` as a non-idempotent LLM action.
    """
    pk_col = pk_field()

    log_llm_action(
        tool="update_config",
        pk={pk_col: config_id},
        reason=reason,
        request_id=request_id,
        actor="llm",
    )

    if not updates:
        return "No fields provided to update."

    update_config_with_embedding(config_id, updates)
    return f"Updated {pk_col}={config_id} with fields {list(updates.keys())}."


@mcp.tool()
def update_mitre_config(
    config_id: str,
    reason: str,
    mitre_tactic: Optional[str] = None,
    mitre_technique: Optional[str] = None,
    request_id: Optional[str] = None,
) -> str:
    """
    Update MITRE ATT&CK tactic and/or technique fields for a configuration.

    This does not trigger embedding updates.

    Args:
        config_id: Primary key of the configuration to update.
        reason: Short, audit-ready explanation for the change.
        mitre_tactic: Tactic name(s) only (no IDs).
        mitre_technique: Technique(s) in `Txxxx - Name` format.
        request_id: Optional correlation ID for traceability.

    Returns:
        Confirmation message of updated MITRE fields.

    Notes:
        • Tactic must be name only (e.g., "Defense Evasion").
        • Technique must start with T + digits (and optional sub-ID),
          followed by `" - "` and the technique name.
        • Logs to `llm_action_log` as a non-idempotent LLM action.
    """
    pk_col = pk_field()

    log_llm_action(
        tool="update_mitre_config",
        pk={pk_col: config_id},
        reason=reason,
        request_id=request_id,
        actor="llm",
    )

    update_mitre_fields(config_id, mitre_tactic, mitre_technique)
    return f"Updated MITRE fields for {pk_col}={config_id}"

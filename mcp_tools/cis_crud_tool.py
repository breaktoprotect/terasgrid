from fastmcp import FastMCP
from typing import List, Dict, Optional
from src.ingestion import cis_crud as crud

mcp = FastMCP("CIS Benchmark CRUD Tools")


@mcp.tool()
def list_cis_tables() -> List[str]:
    """
    Retrieve all CIS benchmark tables from the temporary database.

    These tables exist only in local_temp.db and correspond to ingested
    CIS Benchmark PDFs. Use this to discover the table name before calling
    get_one_unreviewed_record() or mark_one_record_reviewed().
    """
    return crud.list_cis_tables()


@mcp.tool()
def get_one_unreviewed_record(table_name: str) -> Dict:
    """
    Fetch a single unreviewed CIS benchmark record from the given table.

    Args:
        table_name: The table name from list_cis_tables().

    Returns:
        A dict containing CIS benchmark fields for the record, or {} if none remain.
    """
    return crud.get_one_unreviewed_record(table_name)


@mcp.tool()
def mark_one_record_reviewed(
    table_name: str, number: str, reviewed: Optional[int] = 1
) -> str:
    """
    Update the 'reviewed' flag for a CIS benchmark record.

    Args:
        table_name: The table name from list_cis_tables().
        number: The CIS recommendation number (e.g., "1.1.1").
        reviewed: 1 = reviewed, 0 = unreviewed. Default is 1.
    """
    result = crud.mark_one_record_reviewed(table_name, number, reviewed)

    # ✅ LLM action log (non-idempotent)
    log_llm_action(
        tool="mark_one_record_reviewed",
        pk={"table": table_name, "number": number},
        reason=reason,
        actor="llm",
        request_id=request_id,
    )

    return crud.mark_one_record_reviewed(table_name, number, reviewed)

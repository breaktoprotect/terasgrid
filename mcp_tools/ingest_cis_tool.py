from fastmcp import FastMCP
from typing import Optional
from pathlib import Path

from src.ingestion.ingest_cis import ingest_cis_pdf

mcp = FastMCP("CIS Benchmark Ingestion")


@mcp.tool()
def ingest_cis_benchmark(pdf_path: str, start_page: Optional[int] = 2) -> str:
    """
    Ingest a CIS Benchmark **PDF file from local disk** into the temporary database.

    IMPORTANT:
        • This tool does **not** need the PDF contents in the prompt.
        • Pass the **absolute file path** to `pdf_path`. Do NOT read or upload the file contents.
        • The file must already exist on the MCP server's filesystem.

    Args:
        pdf_path: Full local filesystem path to the PDF file (e.g., "C:/data/benchmark.pdf").
        start_page: Page number to start extraction (default: 2).

    Returns:
        Confirmation message with table name and number of records inserted.
    """
    if not Path(pdf_path).exists():
        return f"[ERROR] File not found: {pdf_path}"

    try:
        ingest_cis_pdf(pdf_path, start_page=start_page)
        return f"[OK] CIS Benchmark PDF '{pdf_path}' ingested successfully."
    except Exception as e:
        return f"[ERROR] {str(e)}"


if __name__ == "__main__":
    mcp.run()

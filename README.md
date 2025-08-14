# TerasGrid

**TerasGrid** is an AI-powered cybersecurity policy and controls baseline management system.  
It focuses on configuration settings first, with future expansion to procedural controls.

## Features

-   Ingestion of CIS, STIG, and Microsoft baseline configurations
-   CRUD operations for configuration settings with vector embeddings
-   AI-driven MITRE ATT&CK mapping
-   Drift detection and enforcement across Windows, Linux, and macOS
-   FastMCP integration for automation
-   Local vector storage with SQLite / libSQL

## Tech Stack

-   **Python 3.11+**
-   **FastMCP**
-   **SQLite** (with `sqlite-vec` for vector search)
-   **Sentence-Transformers** (SBERT)
-   **Pandas / NumPy**

## Status

🚧 **Active development** — early alpha stage.  
Not yet production-ready.

## License

TBD (likely MIT or Apache 2.0)

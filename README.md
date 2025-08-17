# TerasGrid

**TerasGrid** is an AI-powered cybersecurity policy and controls baseline management system.  
It focuses on configuration settings first, with future expansion to procedural controls.

## Key Features

-   ??

## Functionalities

-   Conversion of document baselines (e.g. PDF) to compatible structured format (e.g. CSV)
-   Careful ingestion of baselines based on criteria (i.e. must be security related, must not already exist in CS Policies, etc)
-   End-to-end workflow: ingestion -> semantic matching -> AI curation added “pending” CS -> Review/approval by Cybersecurity Professional
-   Audit-ready logging & traceability (i.e. all actions taken by LLM is logged with reasoning)
-   Semantic search and able to answer questions of including coverage-related or audit-motivated queries based on our configuration policies
-   MITRE ATT&CK enrichment automation
-   Quickly generate statistics for presentation (e.g. How many active/draft/retired/rejected configurations? How many MITRE mapped? How many were updated on recent uplift last 30 days?)
-   Generate useful heatmap, radar chart, etc.

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

from src.db.db_reset import reset_dbs
from src.db.db_init import init_all
from src.ingest import ingest

if __name__ == "__main__":
    print("[*] Resetting databases and output directory...")
    reset_dbs(clear_output=True)  # uses default DB_FILES/DB_PATH
    print("[*] Initializing schema and logging...")
    init_all(include_observability=True)
    print("[*] Starting data ingestion...")
    ingest()
    print("[+] Database reset, initialized, and ingested.")

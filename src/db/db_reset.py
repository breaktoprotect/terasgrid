# src/db/db_reset.py
from __future__ import annotations
import os
import shutil
import sqlite3
from typing import Callable, Iterable, Optional
from config import ALL_DB_FILES

OUTPUT_DIR = "./output"


def destroy_dbs(db_files: Optional[Iterable[str]] = None) -> None:
    """
    Delete the given SQLite database files (if present).
    Default set comes from config.ALL_DB_FILES.
    """
    files = list(db_files) if db_files is not None else list(ALL_DB_FILES)
    for path in files:
        try:
            if os.path.exists(path):
                os.remove(path)
                print(f"[!] Deleted database: {path}")
            else:
                print(f"[!] No database file found at: {path}")
        except Exception as e:
            print(f"[x] Failed to delete {path}: {e}")


def clear_output_dir(path: str = OUTPUT_DIR, recreate: bool = True) -> None:
    if os.path.exists(path) and os.path.isdir(path):
        try:
            shutil.rmtree(path)
            print(f"[!] Cleared output directory: {path}")
        except Exception as e:
            print(f"[x] Failed to clear output directory {path}: {e}")
            return
    else:
        print(f"[!] No output directory found at: {path}")
    if recreate:
        try:
            os.makedirs(path, exist_ok=True)
            print(f"[+] Recreated output directory: {path}")
        except Exception as e:
            print(f"[x] Failed to recreate output directory {path}: {e}")


def reset_dbs(
    db_files: Optional[Iterable[str]] = None,
    init_fn: Optional[Callable[[], None]] = None,
    touch_if_no_init: bool = True,
    clear_output: bool = True,
) -> None:
    """
    Reset databases: destroy them, then optionally re-initialize.
    Also clears output directory if requested.

    - If `init_fn` is provided (e.g., `ingest`), it's called ONCE after destruction.
    - If no `init_fn` is given and `touch_if_no_init` is True, create empty SQLite files.

    Args:
        db_files: DB files to manage (defaults to config.DB_FILES).
        init_fn: a callable like `ingest` to rebuild schema/data.
        touch_if_no_init: create empty SQLite files if no init function is provided.
        clear_output: whether to clear the ./output directory as part of reset.
    """
    files = list(db_files) if db_files is not None else list(ALL_DB_FILES)

    # 0) Clear output if requested
    if clear_output:
        clear_output_dir()

    # 1) Nuke DBs
    destroy_dbs(files)

    # 2) Re-init
    if init_fn is not None:
        try:
            init_fn()
            print("[+] Initialization function executed.")
        except Exception as e:
            print(f"[x] Initialization function failed: {e}")
    elif touch_if_no_init:
        for path in files:
            try:
                conn = sqlite3.connect(path)
                conn.close()
                print(f"[+] Created empty SQLite file: {path}")
            except Exception as e:
                print(f"[x] Failed to create {path}: {e}")

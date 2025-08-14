from config import CSV_COLUMN_MAP


def pk_field() -> str:
    """Return the DB primary key column name from CSV_COLUMN_MAP."""
    return CSV_COLUMN_MAP["unique_id_mandatory"]

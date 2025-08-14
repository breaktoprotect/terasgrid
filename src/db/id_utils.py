import hashlib
from src.db.schema_map import pk_field


def generate_unique_id(data: dict) -> str:
    """
    Generate a unique ID for the primary key column defined in CSV_COLUMN_MAP["unique_id_mandatory"].

    Format: NEW_<7-char MD5 hash>

    The hash is calculated from all key-value pairs except the primary key itself.
    """
    pk_col = pk_field()
    hash_source = "|".join(
        str(data.get(field, "")) for field in sorted(data.keys()) if field != pk_col
    )
    digest = hashlib.md5(hash_source.encode("utf-8")).hexdigest()[:7]
    return f"NEW_{digest}"

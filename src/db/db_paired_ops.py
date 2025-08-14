from config import CSV_COLUMN_MAP
from src.db import db_operations
from src.db.db_embeddings import insert_embedding, update_embedding


def _build_embedding_text(data: dict) -> str:
    """Combine fields into the text representation used for embeddings."""
    return " | ".join(
        [
            str(data.get(CSV_COLUMN_MAP["name_mandatory"], "")),
            str(data.get(CSV_COLUMN_MAP["description_mandatory"], "")),
            str(data.get(CSV_COLUMN_MAP.get("settings_optional", ""), "")),
        ]
    )


def insert_config_with_embedding(data: dict) -> None:
    """
    Insert into configs, then insert into vec_configs with embedding.
    """
    db_operations.insert("configs", data)
    text = _build_embedding_text(data)
    insert_embedding(data[CSV_COLUMN_MAP["unique_id_mandatory"]], text)


def update_config_with_embedding(config_id: str, updates: dict) -> None:
    """
    Update configs, and re-embed if relevant fields changed.
    """
    pk_col = CSV_COLUMN_MAP["unique_id_mandatory"]
    db_operations.update("configs", updates, where=f"{pk_col} = ?", params=(config_id,))

    if any(
        f in updates
        for f in (
            CSV_COLUMN_MAP["name_mandatory"],
            CSV_COLUMN_MAP["description_mandatory"],
            CSV_COLUMN_MAP.get("settings_optional", ""),
        )
    ):
        text = _build_embedding_text(updates)
        update_embedding(config_id, text)

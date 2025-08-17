import numpy as np
from sqlite_vec import serialize_float32
from src.model_loader import get_model
from src.db.db_init import get_db
from config import CORE_DB_PATH


def insert_embedding(config_id: str, text: str, db_path: str = CORE_DB_PATH) -> None:
    model = get_model()
    emb = model.encode([text], convert_to_numpy=True, normalize_embeddings=True)[0]
    with get_db(db_path) as conn:
        conn.execute(
            "INSERT INTO vec_configs(config_id, embedding) VALUES (?, ?)",
            (config_id, serialize_float32(emb.tolist())),
        )
        conn.commit()


def update_embedding(config_id: str, text: str, db_path: str = CORE_DB_PATH) -> None:
    model = get_model()
    emb = model.encode([text], convert_to_numpy=True, normalize_embeddings=True)[0]
    with get_db(db_path) as conn:
        conn.execute(
            "UPDATE vec_configs SET embedding = ? WHERE config_id = ?",
            (serialize_float32(emb.tolist()), config_id),
        )
        conn.commit()

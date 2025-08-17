from config import CORE_DB_PATH, CSV_COLUMN_MAP
from sqlite_vec import serialize_float32
import numpy as np
from src.model_loader import get_model
from src.db.db_init import get_db
from src.db.schema_map import pk_field


def semantic_search(
    query: str, top_k: int = 5, db_path: str = CORE_DB_PATH, status: str | None = None
):
    """Return top-k rows as a list of dicts (for MCP use)."""
    conn = get_db(db_path)
    model = get_model()
    q = model.encode([query], convert_to_numpy=True, normalize_embeddings=True)[
        0
    ].astype(np.float32)

    pk = pk_field()
    name_col = CSV_COLUMN_MAP["name_mandatory"]
    desc_col = CSV_COLUMN_MAP["description_mandatory"]
    settings_col = CSV_COLUMN_MAP["settings_optional"]
    status_col = CSV_COLUMN_MAP["status_mandatory"]

    sql = f"""
        WITH knn AS (
          SELECT {pk} AS pk, distance
          FROM vec_configs
          WHERE embedding MATCH ?
            AND k = ?
        )
        SELECT c.{pk}, c.{name_col}, c.{desc_col}, c.{settings_col}, c.{status_col}, knn.distance
        FROM knn
        JOIN configs c ON c.{pk} = knn.pk
    """
    params = [serialize_float32(q.tolist()), top_k]

    if status:
        sql += f" WHERE c.{status_col} = ?"
        params.append(status)

    sql += " ORDER BY knn.distance ASC;"

    rows = conn.execute(sql, params).fetchall()

    return [
        {
            pk: cid,
            name_col: name,
            desc_col: desc,
            settings_col: settings,
            status_col: st,
            "cosine_similarity": 1.0 - float(dist),
        }
        for (cid, name, desc, settings, st, dist) in rows
    ]

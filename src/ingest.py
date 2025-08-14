import pandas as pd
import numpy as np
from sqlite_vec import serialize_float32
from config import DB_PATH, CSV_PATH, CSV_COLUMN_MAP, CSV_EMBEDDING_COLUMN_MAP
from src.db.db_init import get_db
from src.model_loader import get_model
from sentence_transformers import SentenceTransformer


def validate_mandatory_columns(df: pd.DataFrame) -> None:
    """Ensure all mandatory columns from CSV_COLUMN_MAP exist in the CSV."""
    missing = [
        colname
        for key, colname in CSV_COLUMN_MAP.items()
        if key.endswith("_mandatory") and colname not in df.columns
    ]
    if missing:
        raise ValueError(f"Missing mandatory CSV columns: {missing}")


def embed_rows(df: pd.DataFrame, model: SentenceTransformer) -> np.ndarray:
    parts = []
    for key, colname in CSV_EMBEDDING_COLUMN_MAP.items():
        if colname in df.columns:
            parts.append(df[colname])
        else:
            parts.append(pd.Series([""] * len(df)))  # missing optional column
    texts = (" | ".join(map(str, row)) for row in zip(*parts))
    return model.encode(
        list(texts), convert_to_numpy=True, normalize_embeddings=True
    ).astype(np.float32)


def ingest():
    df = pd.read_csv(CSV_PATH, dtype=str).fillna("")

    # Validate CSV structure
    validate_mandatory_columns(df)

    # Ensure optional columns exist
    for opt_key in [k for k in CSV_COLUMN_MAP if k.endswith("_optional")]:
        colname = CSV_COLUMN_MAP[opt_key]
        if colname not in df.columns:
            df[colname] = ""

    conn = get_db(DB_PATH)
    model = get_model()

    embs = embed_rows(df, model)

    # Prepare insert order according to DB schema, using mapped names
    insert_cols = [
        CSV_COLUMN_MAP["unique_id_mandatory"],
        CSV_COLUMN_MAP["name_mandatory"],
        CSV_COLUMN_MAP["description_mandatory"],
        CSV_COLUMN_MAP.get("settings_optional", ""),
        CSV_COLUMN_MAP["status_mandatory"],
        CSV_COLUMN_MAP.get("mitre_tactic_optional", ""),
        CSV_COLUMN_MAP.get("mitre_technique_optional", ""),
    ]

    conn.executemany(
        """
        INSERT INTO configs(
          config_id, config_name, config_desc, config_settings, status, mitre_tactic, mitre_technique
        ) VALUES (?, ?, ?, ?, ?, ?, ?);
        """,
        df[insert_cols].values.tolist(),
    )

    # Vector table uses the mapped unique ID
    uid_col = CSV_COLUMN_MAP["unique_id_mandatory"]
    conn.executemany(
        """
        INSERT INTO vec_configs(config_id, embedding)
        VALUES (?, ?);
        """,
        [
            (df.iloc[i][uid_col], serialize_float32(embs[i].tolist()))
            for i in range(len(df))
        ],
    )

    conn.commit()
    print(f"[+] Ingested {len(df)} rows into fresh {DB_PATH} with embeddings.")

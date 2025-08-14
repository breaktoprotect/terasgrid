DB_PATH = "local.db"
CSV_PATH = "data.csv"
MODEL_ID = "sentence-transformers/all-mpnet-base-v2"


# List of DB files we manage/reset during development
DB_FILES = ["local.db"]

# ? Must map to your CSV columns
CSV_COLUMN_MAP = {
    # Mandatory mappings
    "unique_id_mandatory": "config_id",  # Primary key
    "name_mandatory": "config_name",  # Human-readable name/title
    "description_mandatory": "config_desc",  # Description/details
    "status_mandatory": "status",  # Status of the record
    # Optional mappings
    "settings_optional": "config_settings",  # Raw settings string
    "mitre_tactic_optional": "mitre_tactic",  # MITRE tactic(s)
    "mitre_technique_optional": "mitre_technique",  # MITRE technique(s)
}

CSV_EMBEDDING_COLUMN_MAP = {
    "name_mandatory": "config_name",
    "description_mandatory": "config_desc",
    "settings_optional": "config_settings",
}

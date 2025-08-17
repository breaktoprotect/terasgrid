# Core (Current configuration settings)
CORE_DB_PATH = "local.db"
CSV_PATH = "data.csv"
MODEL_ID = "sentence-transformers/all-mpnet-base-v2"

# Ingested benchmarks
TEMP_DB_PATH = "local_temp.db"

# List of DB files we manage/reset during development
ALL_DB_FILES = [CORE_DB_PATH, TEMP_DB_PATH]

# Fixed Statuses
STATUSES = ["Active", "Draft", "Retired", "Rejected", "Pending"]

# Fixed allowed values for Windows Server applicability
WINDOWS_SERVER_VERSIONS = ["2012", "2012R2", "2016", "2019", "2022", "2025"]

# Fixed allowed values for status
ROLE_APPLICABILITY = ["Member Server", "Domain Controller", "All Roles"]

# ? Must map to your CSV columns
CSV_COLUMN_MAP = {
    # Mandatory mappings
    "unique_id_mandatory": "config_id",  # Primary key
    "status_mandatory": "status",  # Status of the record
    "name_mandatory": "config_name",  # Human-readable name/title
    "description_mandatory": "config_desc",  # Description/details
    # Optional mappings
    "settings_optional": "config_settings",  # Raw settings string
    "role_applicable_optional": "role_applicability",
    "os_version_optional": "os_version_applicability",
    "mitre_tactic_optional": "mitre_tactic",  # MITRE tactic(s)
    "mitre_technique_optional": "mitre_technique",  # MITRE technique(s)
}

CSV_EMBEDDING_COLUMN_MAP = {
    "name_mandatory": "config_name",
    "description_mandatory": "config_desc",
    "settings_optional": "config_settings",
}

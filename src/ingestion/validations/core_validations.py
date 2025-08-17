import pandas as pd
from config import CSV_COLUMN_MAP, STATUSES, ROLE_APPLICABILITY, WINDOWS_SERVER_VERSIONS


def validate_mandatory_columns(df: pd.DataFrame) -> None:
    """Ensure all mandatory columns from CSV_COLUMN_MAP exist in the CSV."""
    missing = [
        colname
        for key, colname in CSV_COLUMN_MAP.items()
        if key.endswith("_mandatory") and colname not in df.columns
    ]
    if missing:
        raise ValueError(f"Missing mandatory CSV columns: {missing}")


def ensure_optional_columns(df: pd.DataFrame) -> None:
    """Add empty string columns for optional fields that are missing."""
    for opt_key in [k for k in CSV_COLUMN_MAP if k.endswith("_optional")]:
        colname = CSV_COLUMN_MAP[opt_key]
        if colname not in df.columns:
            df[colname] = ""


def validate_allowed_values(df):
    """Validate that CSV values match allowed lists from config.py."""

    # Status validation
    status_col = CSV_COLUMN_MAP["status_mandatory"]
    invalid_statuses = sorted(
        set(v for v in df[status_col].str.strip() if v not in STATUSES)
    )
    if invalid_statuses:
        raise ValueError(f"Invalid status values: {invalid_statuses}")

    # Role applicability validation (optional column)
    role_col = CSV_COLUMN_MAP.get("role_applicable_optional")
    if role_col in df.columns:
        invalid_roles = sorted(
            set(
                v for v in df[role_col].str.strip() if v and v not in ROLE_APPLICABILITY
            )
        )
        if invalid_roles:
            raise ValueError(f"Invalid role applicability values: {invalid_roles}")

    # OS version applicability validation (optional column)
    os_col = CSV_COLUMN_MAP.get("os_version_optional")
    if os_col in df.columns:
        invalid_versions = sorted(
            set(
                part.strip()
                for cell in df[os_col]
                if cell
                for part in cell.replace(",", ";").split(";")  # support both ; and ,
                if part.strip() and part.strip() not in WINDOWS_SERVER_VERSIONS
            )
        )
        if invalid_versions:
            raise ValueError(
                f"Invalid OS version applicability values: {invalid_versions}"
            )

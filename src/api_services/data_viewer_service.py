from src.db.db_filters import get_configs_core_fields


def list_core_configs():
    """
    Return all columns for core configs table.
    The UI decides which columns to display vs. hide.
    """
    rows = get_configs_core_fields()
    return [dict(r) for r in rows]

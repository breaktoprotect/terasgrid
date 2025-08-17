from fastapi import APIRouter
from src.api_services import cis_data_service, data_viewer_service

router = APIRouter(prefix="/data_viewer", tags=["data"])


@router.get("/core")
def list_core_configs():
    return data_viewer_service.list_core_configs()


@router.get("/cis/tables")
def list_cis_tables():
    return cis_data_service.list_cis_tables_available()


@router.get("/cis/{table_name}")
def get_cis_table(table_name: str):
    return cis_data_service.get_cis_table_data(table_name)


@router.get("/cis/{table_name}/stats")
def get_cis_table_stats(table_name: str):
    """
    Return counts for total, reviewed, and unreviewed records.
    """
    return cis_data_service.get_cis_table_stats(table_name)

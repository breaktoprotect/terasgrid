from fastapi import APIRouter
from src.api_services.setup_service import reset_and_ingest

router = APIRouter(prefix="/setup", tags=["setup"])


@router.post("/reset-and-ingest")
def reset_and_ingest_endpoint():
    """
    Reset database schema and ingest baseline configs from CSV_PATH.
    """
    return reset_and_ingest()

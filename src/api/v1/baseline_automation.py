# src/api/v1/baseline_automation.py
from fastapi import APIRouter, BackgroundTasks, UploadFile, File, Form, HTTPException
from src.api_services import baseline_automation_service as baseline_service
import tempfile
import shutil

router = APIRouter(prefix="/baseline", tags=["baseline"])


@router.post("/upload")
async def upload_and_ingest(
    file: UploadFile = File(...),
    start_page: int = Form(36),
):
    """
    Upload a CIS PDF and trigger ingestion into the temp DB.
    The table name will be derived from the uploaded file's original name.
    """
    # Save the uploaded file to a temporary location
    tmp_path = tempfile.mktemp(suffix=".pdf")
    with open(tmp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Pass both temp file path (for reading) and original filename (for table naming)
        return baseline_service.upload_and_ingest(
            pdf_path=tmp_path,
            start_page=start_page,
            filename_hint=file.filename,
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))


@router.post("/harden")
def start_baseline_hardening(background_tasks: BackgroundTasks, table_name: str):
    """
    Start baseline hardening loop as background task.
    """
    background_tasks.add_task(baseline_service.harden, table_name)
    return {"status": "ok", "message": f"Baseline hardening started for {table_name}"}


@router.get("/progress/{table_name}")
def get_baseline_progress(table_name: str):
    """
    Get current progress of baseline hardening.
    """
    return baseline_service.get_progress(table_name)

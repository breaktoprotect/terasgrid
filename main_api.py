from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1 import setup, data_viewer, baseline_automation

app = FastAPI(title="TerasGrid API", version="0.1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <-- allow all origins for now (safe in dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(setup.router, prefix="/api/v1")
app.include_router(data_viewer.router, prefix="/api/v1")
app.include_router(baseline_automation.router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main_api:app", host="127.0.0.1", port=8000, reload=True)

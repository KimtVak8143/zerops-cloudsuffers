from fastapi import FastAPI
from app.api.api_v1.api import router as api_router

app = FastAPI(title="AI Radar API", version="0.1.0")
app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

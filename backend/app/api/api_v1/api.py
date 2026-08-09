from fastapi import APIRouter

from app.api.api_v1.endpoints import trends

router = APIRouter()
router.include_router(trends.router, prefix="/trends", tags=["trends"])

@router.get("/health")
def health() -> dict:
    return {"status": "ok"}

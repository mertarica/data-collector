from fastapi import APIRouter
from app.api.v1.endpoints import datasets, data

api_router = APIRouter()

api_router.include_router(
    datasets.router,
    prefix="/datasets",
    tags=["datasets"]
)

api_router.include_router(
    data.router,
    prefix="/data",
    tags=["data"]
)

@api_router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "augusta-data-collector"}

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from app.models.schemas import DatasetInfo, ErrorResponse
from app.services.ine.database_service import database_service

router = APIRouter()

@router.get("/", response_model=List[DatasetInfo])
async def get_datasets():
    """Get all available datasets from database"""
    try:
        datasets = await database_service.get_ine_datasets()
        
        return [
            DatasetInfo(
                external_id=dataset.get('external_id', ''),
                name=dataset.get('name', ''),
                id=str(dataset.get('id', '')),
                dataset_name=str(dataset.get('dataset_name', '')),
            )
            for dataset in datasets
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch datasets: {str(e)}"
        )

@router.get("/search", response_model=List[DatasetInfo])
async def search_datasets(
    q: str = Query(..., min_length=2, description="Search query"),
    limit: int = Query(20, ge=1, le=100, description="Number of results to return")
):
    """Search datasets by name or code in database"""
    try:
        # Database service'e search metodu ekleyelim
        datasets = await database_service.search_ine_datasets(q, limit)
        
        return [
            DatasetInfo(
                external_id=dataset.get('external_id', ''),
                name=dataset.get('name', ''),
                id=str(dataset.get('id', '')),
                dataset_name=str(dataset.get('dataset_name', '')),
            )
            for dataset in datasets
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )

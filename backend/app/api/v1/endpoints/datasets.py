from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from app.models.schemas import DatasetInfo, ErrorResponse
from app.services.data_ingestion.ine.factory import INEProviderFactory
from app.api.deps import get_ine_factory

router = APIRouter()


@router.get("/", response_model=List[DatasetInfo])
async def get_datasets(
    factory: INEProviderFactory = Depends(get_ine_factory)
):
    """Get all available datasets from INE"""
    try:
        datasets = factory.get_available_datasets()

        return [
            DatasetInfo(
                codigo=item.get('Codigo', ''),
                nombre=item.get('Nombre', ''),
                cod_ioe=item.get('Cod_IOE'),
                url=item.get('Url')
            )
            for item in datasets
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch datasets: {str(e)}"
        )


@router.get("/search", response_model=List[DatasetInfo])
async def search_datasets(
    q: str = Query(..., min_length=2, description="Search query"),
    limit: int = Query(
        20, ge=1, le=100, description="Number of results to return"),
    factory: INEProviderFactory = Depends(get_ine_factory)
):
    """Search datasets by name or code"""
    try:
        results = factory.search_datasets(q, limit=limit)

        return [
            DatasetInfo(
                codigo=item.get('Codigo', ''),
                nombre=item.get('Nombre', ''),
                cod_ioe=item.get('Cod_IOE'),
                url=item.get('Url')
            )
            for item in results
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )


@router.get("/{dataset_code}", response_model=DatasetInfo)
async def get_dataset_info(
    dataset_code: str,
    factory: INEProviderFactory = Depends(get_ine_factory)
):
    """Get information about a specific dataset"""
    try:
        dataset_info = factory.get_dataset_info(dataset_code)

        if not dataset_info:
            raise HTTPException(
                status_code=404,
                detail=f"Dataset '{dataset_code}' not found"
            )

        return DatasetInfo(
            codigo=dataset_info.get('Codigo', ''),
            nombre=dataset_info.get('Nombre', ''),
            cod_ioe=dataset_info.get('Cod_IOE'),
            url=dataset_info.get('Url')
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get dataset info: {str(e)}"
        )

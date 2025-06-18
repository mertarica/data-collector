from fastapi import APIRouter, HTTPException, Depends
from app.services.ine.database_service import database_service
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/raw/{dataset_code}")
async def get_raw_data(dataset_code: str):
    """Get raw data from database (original INE format)"""
    try:
        logger.info(f"Getting raw data for dataset: {dataset_code}")
        
        # DB'den raw data çek (orijinal INE formatında)
        data = await database_service.get_dataset_raw_data(dataset_code)
        
        if not data:
            raise HTTPException(
                status_code=404,
                detail=f"No data found for dataset '{dataset_code}'"
            )
        
        return {
            "status": "success",
            "dataset_code": dataset_code,
            "data": data,
            "total_series": len(data),
            "source": "database"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error for dataset {dataset_code}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/processed/{dataset_code}")
async def get_processed_data(dataset_code: str):
    """Get processed/summarized data from database"""
    try:
        logger.info(f"Getting processed data for dataset: {dataset_code}")
        
        # DB'den processed data çek (summary format)
        data = await database_service.get_dataset_processed_data(dataset_code)
        
        if not data:
            raise HTTPException(
                status_code=404,
                detail=f"No processed data found for dataset '{dataset_code}'"
            )
        
        return {
            "status": "success",
            "dataset_code": dataset_code,
            "summary": data,
            "total_series": len(data),
            "source": "database"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error for dataset {dataset_code}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/metadata/{dataset_code}")
async def get_dataset_metadata(dataset_code: str):
    """Get dataset metadata from database"""
    try:
        logger.info(f"Getting metadata for dataset: {dataset_code}")
        
        # DB'den metadata çek
        metadata = await database_service.get_dataset_metadata(dataset_code)
        
        if not metadata:
            raise HTTPException(
                status_code=404,
                detail=f"No metadata found for dataset '{dataset_code}'"
            )
        
        return {
            "status": "success",
            "dataset_code": dataset_code,
            "metadata": metadata,
            "total_series": len(metadata),
            "source": "database"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error for dataset {dataset_code}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting dataset info for {dataset_code}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
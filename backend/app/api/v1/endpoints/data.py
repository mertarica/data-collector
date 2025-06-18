from fastapi import APIRouter, HTTPException, Depends
from app.services.data_ingestion.ine.factory import INEProviderFactory
from app.api.deps import get_ine_factory
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/raw/{dataset_code}")
async def get_raw_data(dataset_code: str):
    """Get raw INE data"""
    try:
        logger.info(f"Getting raw data for dataset: {dataset_code}")
        factory = INEProviderFactory()
        provider = factory.create_provider(dataset_code)
        
        data = provider.get_data()
        
        if data.get("status") == "error":
            raise HTTPException(
                status_code=400,
                detail=f"Error fetching raw data: {data.get('error')}"
            )
        
        return data
        
    except ValueError as e:
        logger.error(f"ValueError for dataset {dataset_code}: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error for dataset {dataset_code}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/processed/{dataset_code}")
async def get_processed_data(dataset_code: str):
    """Get processed INE data with enriched metadata"""
    try:
        logger.info(f"Getting processed data for dataset: {dataset_code}")
        factory = INEProviderFactory()
        provider = factory.create_provider(dataset_code)
        
        data = provider.get_processed_data()
        
        if data.get("status") == "error":
            raise HTTPException(
                status_code=400,
                detail=f"Error fetching processed data: {data.get('error')}"
            )
        
        return data
        
    except ValueError as e:
        logger.error(f"ValueError for dataset {dataset_code}: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error for dataset {dataset_code}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/info/{dataset_code}")
async def get_dataset_info(dataset_code: str):
    """Get information about a dataset"""
    try:
        factory = INEProviderFactory()
        dataset_info = factory.get_dataset_info(dataset_code)
        
        if not dataset_info:
            raise HTTPException(
                status_code=404,
                detail=f"Dataset '{dataset_code}' not found"
            )
        
        return dataset_info
        
    except Exception as e:
        logger.error(f"Error getting dataset info for {dataset_code}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

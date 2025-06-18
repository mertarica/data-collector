from fastapi import APIRouter, HTTPException
from app.services.ine.data_collector_service import data_collector_service
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/test-ine-connection")
async def test_ine_connection():
    """Test connection to INE API"""
    try:
        connected = await data_collector_service.test_ine_connection()
        return {
            "success": connected,
            "message": "INE connection test completed",
            "connected": connected
        }
    except Exception as error:
        logger.error(f"INE connection test error: {error}")
        return {
            "success": False,
            "message": "INE connection test failed",
            "error": str(error)
        }

@router.post("/run-ine-data-collection")
async def run_ine_data_collection_job():
    """Run INE data collection job"""
    try:
        result = await data_collector_service.collect_ine_data()
        return {
            "success": True,
            "message": "INE data collection completed successfully",
            "data": result
        }
    except Exception as error:
        logger.error(f"INE data collection error: {error}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "message": "INE data collection failed",
                "error": str(error)
            }
        )

@router.get("/health")
async def job_health_check():
    """Health check for job services"""
    return {"status": "healthy", "service": "job-service"}
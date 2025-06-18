import httpx
import logging
import asyncio
from typing import List, Dict, Any
from app.services.ine.database_service import database_service

logger = logging.getLogger(__name__)

class DataCollectorService:
    
    async def collect_ine_data(self):
        """Collect all INE data based on ine_datasets table"""
        try:
            logger.info("Starting INE data collection...")
            
            ine_source = await database_service.get_ine_data_source()
            if not ine_source:
                raise Exception("INE data source not found")
            
            datasets = await database_service.get_ine_datasets()
            logger.info(f"Found {len(datasets)} datasets to collect")
            
            results = []
            async with httpx.AsyncClient(
                timeout=httpx.Timeout(120.0, connect=30.0),
                follow_redirects=True,
                limits=httpx.Limits(max_connections=5)
            ) as client:
                for dataset in datasets:
                    result = await self._process_dataset(client, ine_source['base_url'], dataset)
                    results.append(result)
                    await asyncio.sleep(0.5)
            
            logger.info("INE data collection completed")
            return {"success": True, "total_datasets": len(datasets), "results": results}
            
        except Exception as error:
            logger.error(f"INE data collection failed: {error}")
            raise
    
    async def _process_dataset(self, client: httpx.AsyncClient, base_url: str, dataset: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single dataset"""
        base_result = {
            "dataset_id": dataset['id'],
            "dataset_name": dataset['name'],
            "external_id": dataset['external_id'],
            "record_count": 0
        }
        
        try:
            logger.info(f"Processing dataset: {dataset['name']} ({dataset['external_id']})")
            
            api_url = f"{base_url}/DATOS_TABLA/{dataset['external_id']}"
            data = await self._fetch_dataset_data(client, api_url, dataset)
            
            if not data:
                return {**base_result, "status": "no_data"}
            
            try:
                result = await asyncio.wait_for(
                    database_service.save_dataset_data(dataset['external_id'], data),
                    timeout=300.0
                )
                await database_service.update_dataset_last_collected(dataset['id'])
                
                return {
                    **base_result,
                    "record_count": result.get('records_inserted', 0),
                    "status": "success"
                }
                
            except asyncio.TimeoutError:
                logger.error(f"Database timeout for dataset {dataset['name']}")
                return {**base_result, "status": "timeout_error"}
                
        except Exception as error:
            logger.error(f"Error processing dataset {dataset['name']}: {error}")
            return {**base_result, "status": "error", "error": str(error)}
    
    async def _fetch_dataset_data(self, client: httpx.AsyncClient, api_url: str, dataset: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fetch data for a specific INE dataset"""
        try:
            response = await client.get(api_url)
            
            if response.status_code != 200:
                logger.error(f"HTTP {response.status_code} for dataset {dataset['external_id']}")
                return []
            
            data = response.json()
            
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                return data.get('Data', data.get('datos', [data]))
            else:
                logger.warning(f"Unexpected data type for dataset {dataset['external_id']}: {type(data)}")
                return []
                
        except Exception as error:
            logger.error(f"Error fetching data for dataset {dataset['external_id']}: {error}")
            raise
    
    async def test_ine_connection(self) -> bool:
        """Test connection to INE API"""
        try:
            ine_source = await database_service.get_ine_data_source()
            if not ine_source:
                return False
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(ine_source['base_url'])
                return response.status_code == 200
                
        except Exception as e:
            logger.error(f"INE connection test failed: {e}")
            return False

data_collector_service = DataCollectorService()
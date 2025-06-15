import httpx
import pandas as pd
from typing import Dict, Any, List
from app.services.data_ingestion.base.provider import BaseDataProvider
from app.core.config import settings

class INEProvider(BaseDataProvider):
    """Provider for Spanish National Statistics Institute (INE) data"""
    
    def __init__(self, table_id: str, dataset_code: str, dataset_name: str):
        super().__init__(dataset_code, dataset_name)
        self.table_id = table_id
        self.api_url = f"{settings.INE_API_BASE_URL}/DATOS_TABLA/{self.table_id}"
    
    async def fetch_raw_data(self) -> List[Dict[str, Any]]:
        """Fetch raw data from INE API"""
        print(f"🔗 Fetching from URL: {self.api_url}")  # Debug log
        try:
            async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
                response = await client.get(self.api_url)
                print(f"📊 Response status: {response.status_code}")  # Debug log
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPStatusError as e:
            raise Exception(f"INE API Error {e.response.status_code}: {e.response.text}")
        except httpx.TimeoutException:
            raise Exception("INE API request timed out")
        except Exception as e:
            raise Exception(f"Failed to fetch data from INE: {str(e)}")
    
    def parse_to_dataframe(self, raw_data: List[Dict[str, Any]]) -> pd.DataFrame:
        """Parse INE raw data to DataFrame"""
        if not raw_data:
            return pd.DataFrame()
        
        records = []
        
        for item in raw_data:
            if not isinstance(item, dict) or 'Data' not in item:
                continue
                
            item_name = item.get('Nombre', 'Unknown')
            
            for data_point in item['Data']:
                if isinstance(data_point, dict):
                    records.append({
                        'Dataset_Code': self.dataset_code,
                        'Indicador': item_name,
                        'Valor': data_point.get('Valor'),
                        'Secreto': data_point.get('Secreto', False)
                    })
        
        return pd.DataFrame(records)
    
    def get_api_info(self) -> Dict[str, str]:
        """Get API specific information"""
        info = self.get_info()
        info.update({
            "table_id": self.table_id,
            "api_url": self.api_url
        })
        return info
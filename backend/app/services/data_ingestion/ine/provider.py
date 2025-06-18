import json
import requests
import logging
import pandas as pd
from typing import Dict, Any, List, Optional
from datetime import datetime
from .processor import INEDataProcessor

class INEProvider:
    """Provider for fetching data from INE (Instituto Nacional de Estadística)"""
    
    def __init__(self, table_id: str, dataset_code: str, dataset_name: str):
        self.table_id = table_id
        self.dataset_code = dataset_code
        self.dataset_name = dataset_name
        self.base_url = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA"
        self.logger = logging.getLogger(__name__)
        self.processor = INEDataProcessor()
    
    def get_data(self) -> Dict[str, Any]:
        """Get raw data from INE API"""
        try:
            url = f"{self.base_url}/{self.table_id}"
            self.logger.info(f"Fetching data from INE API: {url}")
            
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Parse JSON response
            raw_data = response.json()
            
            # Count total records
            record_count = 0
            if isinstance(raw_data, list):
                for item in raw_data:
                    if item.get("Data"):
                        record_count += len(item["Data"])
            
            return {
                "status": "success",
                "dataset_info": {
                    "table_id": self.table_id,
                    "dataset_code": self.dataset_code,
                    "dataset_name": self.dataset_name,
                    "source": "INE",
                    "data_type": "raw"
                },
                "raw_data": raw_data,
                "record_count": record_count,
                "retrieved_at": datetime.now().isoformat()
            }
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request error: {e}")
            return {
                "status": "error",
                "error": f"Network error: {str(e)}",
                "dataset_info": {
                    "table_id": self.table_id,
                    "dataset_code": self.dataset_code,
                    "dataset_name": self.dataset_name,
                    "source": "INE",
                    "data_type": "raw"
                }
            }
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON decode error: {e}")
            return {
                "status": "error",
                "error": f"Invalid JSON response: {str(e)}",
                "dataset_info": {
                    "table_id": self.table_id,
                    "dataset_code": self.dataset_code,
                    "dataset_name": self.dataset_name,
                    "source": "INE",
                    "data_type": "raw"
                }
            }
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return {
                "status": "error",
                "error": str(e),
                "dataset_info": {
                    "table_id": self.table_id,
                    "dataset_code": self.dataset_code,
                    "dataset_name": self.dataset_name,
                    "source": "INE",
                    "data_type": "raw"
                }
            }

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

    def get_processed_data(self) -> Dict[str, Any]:
        """Get processed data with enriched metadata"""
        try:
            # First get raw data
            raw_response = self.get_data()
            
            if raw_response.get("status") == "error":
                return {
                    "status": "error",
                    "error": f"Failed to get raw data: {raw_response.get('error')}",
                    "dataset_info": {
                        "table_id": self.table_id,
                        "dataset_code": self.dataset_code,
                        "dataset_name": self.dataset_name,
                        "source": "INE",
                        "data_type": "processed"
                    }
                }
            
            raw_data = raw_response.get("raw_data", [])
            
            # Process the data
            processed_data = self.processor.process_raw_data(raw_data)
            
            response = {
                "status": "success",
                "dataset_info": {
                    "table_id": self.table_id,
                    "dataset_code": self.dataset_code,
                    "dataset_name": self.dataset_name,
                    "source": "INE",
                    "data_type": "processed"
                },
                "processed_data": processed_data,
                "retrieved_at": datetime.now().isoformat(),
            }
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error getting processed data: {e}")
            return {
                "status": "error",
                "error": str(e),
                "dataset_info": {
                    "table_id": self.table_id,
                    "dataset_code": self.dataset_code,
                    "dataset_name": self.dataset_name,
                    "source": "INE",
                    "data_type": "processed"
                }
            }
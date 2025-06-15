import json
import os
from typing import Dict, List, Optional
from app.services.data_ingestion.ine.provider import INEProvider
from app.core.config import settings

class INEProviderFactory:
    """Factory to create INE providers for different datasets"""

    def __init__(self):
        self.table_list = self._load_table_list()
        self.code_to_id = self._create_code_mapping()

    def _load_table_list(self) -> List[Dict]:
        """Load TABLELIST.json from shared directory"""
        try:
            # Try different possible paths
            possible_paths = [
                os.path.join(settings.SHARED_DATA_PATH, "TABLELIST.json"),
                "../../shared/data/TABLELIST.json",
                "../shared/data/TABLELIST.json",
                "shared/data/TABLELIST.json"
            ]

            for path in possible_paths:
                full_path = os.path.abspath(path)
                if os.path.exists(full_path):
                    with open(full_path, 'r', encoding='utf-8') as f:
                        return json.load(f)

            # If not found, return empty list
            print("⚠️  TABLELIST.json not found, using empty dataset list")
            return []

        except Exception as e:
            print(f"❌ Error loading TABLELIST.json: {e}")
            return []

    def _create_code_mapping(self) -> Dict[str, str]:
        """Create mapping from dataset code to IOE table ID"""
        return {
            item['Codigo']: item['Cod_IOE']
            for item in self.table_list
            if item.get('Cod_IOE')
        }

    def create_provider(self, dataset_code: str) -> INEProvider:
        """Create INE provider for given dataset code"""
        table_id = self.code_to_id.get(dataset_code)

        if not table_id:
            available_codes = list(self.code_to_id.keys())[:10]
            raise ValueError(
                f"Dataset code '{dataset_code}' not found. "
                f"Available codes: {available_codes}..."
            )

        # Find dataset name
        dataset_name = "Unknown Dataset"
        for item in self.table_list:
            if item.get('Codigo') == dataset_code:
                dataset_name = item.get('Nombre', 'Unknown Dataset')
                break

        return INEProvider(table_id, dataset_code, dataset_name)

    def get_available_datasets(self, limit: Optional[int] = None) -> List[Dict]:
        """Get all available datasets"""
        datasets = [
            item for item in self.table_list
            if item.get('Cod_IOE')
        ]

        if limit:
            datasets = datasets[:limit]

        return datasets

    def search_datasets(self, query: str, limit: Optional[int] = None) -> List[Dict]:
        """Search datasets by query string"""
        query_lower = query.lower()
        results = []

        for item in self.table_list:
            if item.get('Cod_IOE'):
                codigo = item.get('Codigo', '').lower()
                nombre = item.get('Nombre', '').lower()

                if query_lower in codigo or query_lower in nombre:
                    results.append(item)

        if limit:
            results = results[:limit]

        return results

    def get_dataset_info(self, dataset_code: str) -> Optional[Dict]:
        """Get information about a specific dataset"""
        for item in self.table_list:
            if item.get('Codigo') == dataset_code:
                return item
        return None

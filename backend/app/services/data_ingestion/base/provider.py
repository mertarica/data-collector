from abc import ABC, abstractmethod
from typing import Any, Dict, List
import pandas as pd


class BaseDataProvider(ABC):
    """Base class for all data providers"""

    def __init__(self, dataset_code: str, dataset_name: str):
        self.dataset_code = dataset_code
        self.dataset_name = dataset_name

    @abstractmethod
    async def fetch_raw_data(self) -> Any:
        """Fetch raw data from source"""
        pass

    @abstractmethod
    def parse_to_dataframe(self, raw_data: Any) -> pd.DataFrame:
        """Parse raw data to pandas DataFrame"""
        pass

    def get_info(self) -> Dict[str, str]:
        """Get provider information"""
        return {
            "code": self.dataset_code,
            "name": self.dataset_name,
            "provider": self.__class__.__name__
        }

from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Data Collector"
    VERSION: str = "1.0.0"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # CORS Configuration - String olarak alıp split edeceğiz
    ALLOWED_ORIGINS_STR: str = "http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173"
    
    # INE API Configuration
    INE_API_BASE_URL: str = "https://servicios.ine.es/wstempus/js/ES"
    
    # File Paths
    SHARED_DATA_PATH: str = "../shared/data"
    STORAGE_PATH: str = "./storage"
    
    class Config:
        env_file = ".env"
    
    @property
    def ALLOWED_ORIGINS(self) -> List[str]:
        """Convert comma-separated string to list"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS_STR.split(",")]

# Global settings instance
settings = Settings()
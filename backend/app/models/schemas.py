from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class DatasetInfo(BaseModel):
    codigo: str = Field(..., description="Dataset code (e.g., ICE, IPI)")
    nombre: str = Field(..., description="Dataset name in Spanish")
    cod_ioe: Optional[str] = Field(None, description="INE internal code")
    url: Optional[str] = Field(None, description="Dataset documentation URL")


class DataResponse(BaseModel):
    codigo: str
    dataset_name: str
    record_count: int
    success: bool = True
    message: Optional[str] = None


class RawDataResponse(DataResponse):
    raw_data: List[Dict[str, Any]]


class ProcessedDataResponse(DataResponse):
    processed_data: List[Dict[str, Any]]
    columns: List[str]


class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    code: str
    detail: Optional[str] = None

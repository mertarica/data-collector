from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class DatasetInfo(BaseModel):
    external_id: str = Field(..., description="Dataset code (e.g., ICE, IPI)")
    name: str = Field(..., description="Dataset name in Spanish")
    id: Optional[str] = Field(None, description="INE internal code")
    dataset_name: Optional[str] = Field(None, description="Dataset description")

class DataResponse(BaseModel):
    code: str
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

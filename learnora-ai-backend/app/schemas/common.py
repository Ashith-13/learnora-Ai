from pydantic import BaseModel, Field
from typing import Optional, Any, Dict
from datetime import datetime


class PaginationParams(BaseModel):
    """Pagination parameters"""
    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(default=20, ge=1, le=100, description="Items per page")


class SuccessResponse(BaseModel):
    """Standard success response"""
    success: bool = True
    message: str
    data: Optional[Any] = None


class ErrorResponse(BaseModel):
    """Standard error response"""
    success: bool = False
    error: str
    detail: Optional[str] = None


class TimestampMixin(BaseModel):
    """Mixin for timestamp fields"""
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


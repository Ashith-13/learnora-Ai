from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class DoubtCreate(BaseModel):
    """Schema for creating a doubt"""
    title: str = Field(..., min_length=5, max_length=200)
    question: str = Field(..., min_length=10)
    subject: Optional[str] = Field(None, max_length=100)
    tags: Optional[List[str]] = None
    priority: Optional[str] = Field(default="medium", pattern="^(low|medium|high|urgent)$")
    use_context: bool = Field(default=False, description="Use uploaded documents for context")


class DoubtFollowUpCreate(BaseModel):
    """Schema for follow-up question"""
    doubt_id: int
    question: str = Field(..., min_length=5)


class DoubtSolution(BaseModel):
    """Schema for doubt solution"""
    answer: str
    explanation: str
    examples: Optional[List[str]]
    key_concepts: Optional[List[str]]
    additional_resources: Optional[List[str]]


class DoubtResponse(BaseModel):
    """Schema for doubt response"""
    id: int
    user_id: int
    title: str
    question: str
    subject: Optional[str]
    tags: Optional[List[str]]
    priority: str
    status: str
    solution: Optional[Dict[str, Any]]
    is_resolved: bool
    resolution_time: Optional[int]
    created_at: datetime
    resolved_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class DoubtFollowUpResponse(BaseModel):
    """Schema for follow-up response"""
    id: int
    doubt_id: int
    question: str
    answer: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

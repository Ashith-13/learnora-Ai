from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class MilestoneCreate(BaseModel):
    """Schema for creating a milestone"""
    title: str = Field(..., min_length=3, max_length=200)
    description: str
    duration_weeks: int = Field(..., ge=1)
    topics: List[str]
    resources: List[Dict[str, str]]
    order: int


class MilestoneUpdate(BaseModel):
    """Schema for updating milestone completion"""
    milestone_id: int
    completed: bool


class RoadmapCreate(BaseModel):
    """Schema for creating a roadmap"""
    title: str = Field(..., min_length=3, max_length=200)
    description: str
    category: str = Field(..., min_length=3, max_length=100)
    difficulty: str = Field(default="beginner", pattern="^(beginner|intermediate|advanced)$")
    milestones: List[Dict[str, Any]]
    estimated_duration: int = Field(..., description="Duration in days")
    prerequisites: Optional[List[str]] = []
    tags: Optional[List[str]] = []


class RoadmapResponse(BaseModel):
    """Schema for roadmap response"""
    id: int
    user_id: Optional[int]
    title: str
    description: str
    category: str
    difficulty: str
    milestones: List[Dict[str, Any]]
    estimated_duration: int
    resources: Optional[List[Dict[str, Any]]]
    prerequisites: Optional[List[str]]
    completion_percentage: float
    is_template: bool
    is_public: bool
    tags: Optional[List[str]]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class LearningHistoryCreate(BaseModel):
    """Schema for creating learning history entry"""
    roadmap_id: Optional[int]
    activity_type: str = Field(..., pattern="^(quiz|doubt|video|project|reading)$")
    activity_title: str
    activity_data: Optional[Dict[str, Any]] = {}
    duration: Optional[int] = None
    score: Optional[float] = None


class LearningHistoryResponse(BaseModel):
    """Schema for learning history response"""
    id: int
    user_id: int
    roadmap_id: Optional[int]
    activity_type: str
    activity_title: str
    activity_data: Dict[str, Any]
    duration: Optional[int]
    score: Optional[float]
    created_at: datetime
    
    class Config:
        from_attributes = True


class RoadmapProgressResponse(BaseModel):
    """Schema for roadmap progress"""
    roadmap_id: int
    total_milestones: int
    completed_milestones: int
    completion_percentage: float
    time_spent: int
    current_milestone: Optional[Dict[str, Any]]
    next_milestone: Optional[Dict[str, Any]]
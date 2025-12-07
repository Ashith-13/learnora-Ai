from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class CareerAssessment(BaseModel):
    """Schema for career assessment input"""
    interests: List[str] = Field(..., min_items=1, max_items=10)
    skills: List[str] = Field(..., min_items=1, max_items=15)
    personality_traits: List[str] = Field(..., min_items=1, max_items=10)
    work_preferences: List[str] = Field(..., min_items=1, max_items=10)
    education_level: Optional[str] = None
    experience_years: Optional[int] = Field(None, ge=0, le=50)


class CareerRecommendation(BaseModel):
    """Schema for career recommendation"""
    title: str
    match_score: float = Field(..., ge=0, le=100)
    reasons: List[str]
    growth_outlook: str
    salary_range: str
    required_skills: List[str]
    learning_path: str


class CareerProfileResponse(BaseModel):
    """Schema for career profile response"""
    id: int
    user_id: int
    assessment_completed: bool
    interests: Optional[List[str]]
    skills: Optional[List[str]]
    personality_traits: Optional[List[str]]
    work_preferences: Optional[List[str]]
    career_recommendations: Optional[List[Dict[str, Any]]]
    strength_areas: Optional[List[str]]
    improvement_areas: Optional[List[str]]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class JobResponse(BaseModel):
    """Schema for job listing response"""
    id: int
    title: str
    company: str
    location: str
    job_type: str
    experience_level: str
    salary_range: Optional[str]
    description: str
    requirements: List[str]
    skills_required: List[str]
    application_url: str
    posted_date: datetime
    match_score: Optional[float]
    
    class Config:
        from_attributes = True
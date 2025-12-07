from pydantic import BaseModel, EmailStr, Field, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import datetime, date


class EducationEntry(BaseModel):
    """Schema for education entry"""
    institution: str
    degree: str
    field_of_study: str
    start_date: date
    end_date: Optional[date]
    gpa: Optional[float]
    description: Optional[str]


class ExperienceEntry(BaseModel):
    """Schema for work experience entry"""
    company: str
    position: str
    location: Optional[str]
    start_date: date
    end_date: Optional[date]
    current: bool = False
    description: str
    responsibilities: List[str]


class ProjectEntry(BaseModel):
    """Schema for project entry"""
    name: str
    description: str
    technologies: List[str]
    start_date: Optional[date]
    end_date: Optional[date]
    url: Optional[HttpUrl]


class ResumeCreate(BaseModel):
    """Schema for creating a resume"""
    template: str = Field(default="professional", pattern="^(professional|modern|creative|minimal)$")
    personal_info: Dict[str, Any] = Field(..., description="Name, email, phone, etc.")
    summary: Optional[str] = Field(None, max_length=500)
    education: List[EducationEntry]
    experience: List[ExperienceEntry]
    skills: List[str]
    projects: Optional[List[ProjectEntry]] = []
    certifications: Optional[List[str]] = []
    languages: Optional[List[Dict[str, str]]] = []
    custom_sections: Optional[Dict[str, Any]] = {}


class ResumeUpdate(BaseModel):
    """Schema for updating a resume"""
    template: Optional[str] = None
    personal_info: Optional[Dict[str, Any]] = None
    summary: Optional[str] = None
    education: Optional[List[EducationEntry]] = None
    experience: Optional[List[ExperienceEntry]] = None
    skills: Optional[List[str]] = None
    projects: Optional[List[ProjectEntry]] = None
    certifications: Optional[List[str]] = None
    languages: Optional[List[Dict[str, str]]] = None


class ResumeResponse(BaseModel):
    """Schema for resume response"""
    id: int
    user_id: int
    title: str
    template: str
    content: Dict[str, Any]
    pdf_url: Optional[str]
    is_public: bool
    version: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
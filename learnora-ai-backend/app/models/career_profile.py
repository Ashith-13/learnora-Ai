from sqlalchemy import Column, String, Integer, ForeignKey, JSON, Float, Text, Boolean
from sqlalchemy.orm import relationship
from app.db.base import BaseModel


class CareerProfile(BaseModel):
    __tablename__ = "career_profiles"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Assessment Data
    assessment_responses = Column(JSON, nullable=False)
    
    # Scores
    overall_score = Column(Float, default=0.0)
    technical_score = Column(Float, nullable=True)
    soft_skills_score = Column(Float, nullable=True)
    domain_knowledge_score = Column(Float, nullable=True)
    
    # Career Recommendations
    recommended_careers = Column(JSON, default=list)
    strengths = Column(JSON, default=list)
    areas_for_improvement = Column(JSON, default=list)
    
    # Personality & Preferences
    personality_traits = Column(JSON, default=dict)
    career_interests = Column(JSON, default=list)
    work_values = Column(JSON, default=dict)
    
    # Detailed Report
    report = Column(Text, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="career_profiles")


class Job(BaseModel):
    __tablename__ = "jobs"
    
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    location = Column(String, nullable=True)
    job_type = Column(String, nullable=True)
    
    description = Column(Text, nullable=True)
    requirements = Column(JSON, default=list)
    skills_required = Column(JSON, default=list)
    
    salary_range = Column(String, nullable=True)
    experience_level = Column(String, nullable=True)
    
    application_url = Column(String, nullable=True)
    source = Column(String, nullable=True)
    
    is_active = Column(Boolean, default=True)


from sqlalchemy import Column, String, Integer, ForeignKey, JSON, Text, Boolean
from sqlalchemy.orm import relationship
from app.db.base import BaseModel


class Resume(BaseModel):
    __tablename__ = "resumes"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    title = Column(String, nullable=False)
    template = Column(String, default="modern")
    
    # Personal Info
    personal_info = Column(JSON, default=dict)
    
    # Resume Sections
    professional_summary = Column(Text, nullable=True)
    work_experience = Column(JSON, default=list)
    education = Column(JSON, default=list)
    skills = Column(JSON, default=list)
    projects = Column(JSON, default=list)
    certifications = Column(JSON, default=list)
    languages = Column(JSON, default=list)
    
    # ATS Optimization
    ats_score = Column(Integer, default=0)
    keywords = Column(JSON, default=list)
    suggestions = Column(JSON, default=list)
    
    # File Storage
    file_path = Column(String, nullable=True)
    file_format = Column(String, default="pdf")
    
    is_published = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", back_populates="resumes")

from sqlalchemy import Column, String, Integer, ForeignKey, JSON, Text, Float, Boolean
from sqlalchemy.orm import relationship
from app.db.base import BaseModel


class Roadmap(BaseModel):
    __tablename__ = "roadmaps"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=False)
    difficulty = Column(String, default="beginner")
    
    # Roadmap Structure
    milestones = Column(JSON, nullable=False)
    estimated_duration = Column(Integer, nullable=True)
    
    # Resources
    resources = Column(JSON, default=list)
    prerequisites = Column(JSON, default=list)
    
    # Tracking
    completion_percentage = Column(Float, default=0.0)
    
    is_template = Column(Boolean, default=False)
    is_public = Column(Boolean, default=True)
    
    tags = Column(JSON, default=list)


class LearningHistory(BaseModel):
    __tablename__ = "learning_histories"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    roadmap_id = Column(Integer, ForeignKey("roadmaps.id"), nullable=True)
    
    activity_type = Column(String, nullable=False)
    activity_title = Column(String, nullable=False)
    activity_data = Column(JSON, default=dict)
    
    duration = Column(Integer, nullable=True)
    score = Column(Float, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="learning_histories")

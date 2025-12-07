from sqlalchemy import Column, String, Integer, ForeignKey, JSON, Text, Boolean
from sqlalchemy.orm import relationship
from app.db.base import BaseModel


class Doubt(BaseModel):
    __tablename__ = "doubts"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    question = Column(Text, nullable=False)
    subject = Column(String, nullable=True)
    context = Column(Text, nullable=True)
    
    # AI Response
    answer = Column(Text, nullable=False)
    explanation = Column(Text, nullable=True)
    related_resources = Column(JSON, default=list)
    
    # Uploaded Files
    uploaded_files = Column(JSON, default=list)
    
    # Status
    is_resolved = Column(Boolean, default=False)
    rating = Column(Integer, nullable=True)
    feedback = Column(Text, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="doubts")
    follow_ups = relationship("DoubtFollowUp", back_populates="doubt", cascade="all, delete-orphan")


class DoubtFollowUp(BaseModel):
    __tablename__ = "doubt_follow_ups"
    
    doubt_id = Column(Integer, ForeignKey("doubts.id"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    
    # Relationships
    doubt = relationship("Doubt", back_populates="follow_ups")
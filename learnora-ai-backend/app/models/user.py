from sqlalchemy import Column, String, Boolean, JSON
from sqlalchemy.orm import relationship
from app.db.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"
    
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    
    role = Column(String, default="student")  # student, teacher, admin
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Profile
    bio = Column(String, nullable=True)
    profile_picture = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    
    # Preferences
    preferences = Column(JSON, default=dict)
    learning_goals = Column(JSON, default=list)
    interests = Column(JSON, default=list)
    
    # Relationships - FIXED: Removed job_applications
    quizzes = relationship("Quiz", back_populates="user", cascade="all, delete-orphan")
    doubts = relationship("Doubt", back_populates="user", cascade="all, delete-orphan")
    career_profiles = relationship("CareerProfile", back_populates="user", cascade="all, delete-orphan")
    resumes = relationship("Resume", back_populates="user", cascade="all, delete-orphan")
    learning_histories = relationship("LearningHistory", back_populates="user", cascade="all, delete-orphan")
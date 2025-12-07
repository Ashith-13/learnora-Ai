from sqlalchemy import Column, String, Integer, ForeignKey, JSON, Float, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import enum


class QuizType(str, enum.Enum):
    STANDARD = "standard"
    ADAPTIVE = "adaptive"
    TIMED = "timed"
    PRACTICE = "practice"


class DifficultyLevel(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


class Quiz(BaseModel):
    __tablename__ = "quizzes"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    title = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    quiz_type = Column(SQLEnum(QuizType), default=QuizType.STANDARD)
    difficulty = Column(SQLEnum(DifficultyLevel), default=DifficultyLevel.MEDIUM)
    
    # Quiz Content
    questions = Column(JSON, nullable=False)
    total_questions = Column(Integer, nullable=False)
    
    # Results
    answers = Column(JSON, default=dict)
    score = Column(Integer, default=0)
    percentage = Column(Float, default=0.0)
    time_taken = Column(Integer, nullable=True)
    
    is_completed = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", back_populates="quizzes")

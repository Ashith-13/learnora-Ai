from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class QuizType(str, Enum):
    """Quiz type enumeration"""
    PRACTICE = "practice"
    ASSESSMENT = "assessment"
    MOCK_TEST = "mock_test"
    ADAPTIVE = "adaptive"


class DifficultyLevel(str, Enum):
    """Difficulty level enumeration"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class QuizCreate(BaseModel):
    """Schema for creating a quiz"""
    subject: str = Field(..., min_length=1, max_length=100)
    topic: str = Field(..., min_length=1, max_length=200)
    num_questions: int = Field(..., ge=5, le=50)
    difficulty: DifficultyLevel
    quiz_type: QuizType = QuizType.PRACTICE
    time_limit: Optional[int] = Field(None, ge=60, description="Time limit in seconds")
    use_context: bool = Field(default=False, description="Use uploaded documents as context")
    
    @validator('num_questions')
    def validate_questions(cls, v):
        if v < 5:
            raise ValueError('Minimum 5 questions required')
        if v > 50:
            raise ValueError('Maximum 50 questions allowed')
        return v


class QuestionResponse(BaseModel):
    """Schema for question response"""
    id: int
    question_text: str
    question_type: str
    options: List[str]
    difficulty: DifficultyLevel
    points: int
    order: int
    
    class Config:
        from_attributes = True


class QuizResponse(BaseModel):
    """Schema for quiz response"""
    id: int
    title: str
    description: Optional[str]
    subject: str
    topic: str
    quiz_type: QuizType
    difficulty: DifficultyLevel
    total_questions: int
    time_limit: Optional[int]
    passing_score: float
    questions: List[QuestionResponse]
    created_at: datetime
    
    class Config:
        from_attributes = True


class AnswerSubmission(BaseModel):
    """Schema for submitting an answer"""
    question_id: int
    selected_answer: str


class QuizSubmit(BaseModel):
    """Schema for submitting quiz answers"""
    quiz_id: int
    answers: List[AnswerSubmission]
    time_taken: int = Field(..., description="Time taken in seconds")


class QuestionResult(BaseModel):
    """Schema for individual question result"""
    question_id: int
    question_text: str
    selected_answer: str
    correct_answer: str
    is_correct: bool
    explanation: str
    points_earned: int
    points_possible: int


class QuizResult(BaseModel):
    """Schema for quiz result"""
    quiz_id: int
    score: float
    total_questions: int
    correct_answers: int
    wrong_answers: int
    time_taken: int
    passed: bool
    question_results: List[QuestionResult]
    performance_analysis: Dict[str, Any]
    created_at: datetime
    
    class Config:
        from_attributes = True
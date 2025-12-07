from .user import UserCreate, UserLogin, UserResponse, UserUpdate
from .quiz import QuizCreate, QuizResponse, QuestionResponse, QuizSubmit, QuizResult
from .doubt import DoubtCreate, DoubtResponse, DoubtFollowUpCreate
from .career import CareerAssessment, CareerRecommendation, JobResponse
from .resume import ResumeCreate, ResumeResponse, ResumeUpdate
from .roadmap import RoadmapCreate, RoadmapResponse, MilestoneUpdate
from .common import PaginationParams, SuccessResponse, ErrorResponse

__all__ = [
    # User
    'UserCreate', 'UserLogin', 'UserResponse', 'UserUpdate',
    # Quiz
    'QuizCreate', 'QuizResponse', 'QuestionResponse', 'QuizSubmit', 'QuizResult',
    # Doubt
    'DoubtCreate', 'DoubtResponse', 'DoubtFollowUpCreate',
    # Career
    'CareerAssessment', 'CareerRecommendation', 'JobResponse',
    # Resume
    'ResumeCreate', 'ResumeResponse', 'ResumeUpdate',
    # Roadmap
    'RoadmapCreate', 'RoadmapResponse', 'MilestoneUpdate',
    # Common
    'PaginationParams', 'SuccessResponse', 'ErrorResponse'
]
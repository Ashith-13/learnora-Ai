from fastapi import APIRouter
from app.api.v1.endpoints import auth, quiz, doubt_solver, career_score

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(quiz.router, prefix="/quiz", tags=["Quiz"])
api_router.include_router(doubt_solver.router, prefix="/doubts", tags=["Doubt Solver"])
api_router.include_router(career_score.router, prefix="/career", tags=["Career Assessment"])


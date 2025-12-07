from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.quiz import Quiz, QuizType, DifficultyLevel
from app.services.openai.gpt4_service import gpt4_service
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

router = APIRouter()

class QuizCreate(BaseModel):
    subject: str = Field(..., min_length=1, max_length=100)
    topic: str = Field(..., min_length=1, max_length=200)
    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM
    num_questions: int = Field(10, ge=5, le=50)
    quiz_type: QuizType = QuizType.STANDARD

class QuizSubmit(BaseModel):
    quiz_id: int
    answers: Dict[str, str]

class QuizResponse(BaseModel):
    id: int
    title: str
    subject: str
    topic: str
    difficulty: str
    questions: List[Dict[str, Any]]
    total_questions: int
    is_completed: bool

@router.post("/generate", response_model=QuizResponse)
async def generate_quiz(
    quiz_data: QuizCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Generate adaptive quiz using GPT-4"""
    try:
        questions = await gpt4_service.generate_quiz_questions(
            subject=quiz_data.subject,
            topic=quiz_data.topic,
            difficulty=quiz_data.difficulty.value,
            num_questions=quiz_data.num_questions
        )
        
        quiz = Quiz(
            user_id=current_user.id,
            title=f"{quiz_data.subject} - {quiz_data.topic}",
            subject=quiz_data.subject,
            topic=quiz_data.topic,
            quiz_type=quiz_data.quiz_type,
            difficulty=quiz_data.difficulty,
            total_questions=len(questions),
            questions=questions
        )
        
        db.add(quiz)
        await db.commit()
        await db.refresh(quiz)
        
        return QuizResponse(
            id=quiz.id,
            title=quiz.title,
            subject=quiz.subject,
            topic=quiz.topic,
            difficulty=quiz.difficulty.value,
            questions=questions,
            total_questions=quiz.total_questions,
            is_completed=False
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating quiz: {str(e)}")

@router.post("/submit")
async def submit_quiz(
    submission: QuizSubmit,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Submit quiz answers and calculate score"""
    result = await db.execute(
        select(Quiz).where(
            (Quiz.id == submission.quiz_id) & (Quiz.user_id == current_user.id)
        )
    )
    quiz = result.scalar_one_or_none()
    
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    if quiz.is_completed:
        raise HTTPException(status_code=400, detail="Quiz already submitted")
    
    # Calculate score
    correct_count = 0
    detailed_results = []
    
    for i, question in enumerate(quiz.questions):
        question_id = str(i)
        user_answer = submission.answers.get(question_id)
        correct_answer = question.get("correct_answer")
        is_correct = user_answer == correct_answer
        
        if is_correct:
            correct_count += 1
        
        detailed_results.append({
            "question": question.get("question"),
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "explanation": question.get("explanation")
        })
    
    score = (correct_count / quiz.total_questions) * 100
    
    quiz.answers = submission.answers
    quiz.score = correct_count
    quiz.percentage = score
    quiz.is_completed = True
    
    await db.commit()
    
    return {
        "quiz_id": quiz.id,
        "score": correct_count,
        "total_questions": quiz.total_questions,
        "percentage": round(score, 2),
        "passed": score >= 60,
        "detailed_results": detailed_results
    }

@router.get("/history")
async def get_quiz_history(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's quiz history"""
    result = await db.execute(
        select(Quiz)
        .where(Quiz.user_id == current_user.id)
        .order_by(Quiz.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    quizzes = result.scalars().all()
    
    return [
        {
            "id": quiz.id,
            "title": quiz.title,
            "subject": quiz.subject,
            "topic": quiz.topic,
            "score": quiz.score,
            "percentage": quiz.percentage,
            "total_questions": quiz.total_questions,
            "is_completed": quiz.is_completed,
            "created_at": quiz.created_at.isoformat()
        }
        for quiz in quizzes
    ]

@router.get("/{quiz_id}")
async def get_quiz(
    quiz_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get specific quiz details"""
    result = await db.execute(
        select(Quiz).where(
            (Quiz.id == quiz_id) & (Quiz.user_id == current_user.id)
        )
    )
    quiz = result.scalar_one_or_none()
    
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    return {
        "id": quiz.id,
        "title": quiz.title,
        "subject": quiz.subject,
        "topic": quiz.topic,
        "difficulty": quiz.difficulty.value,
        "questions": quiz.questions,
        "answers": quiz.answers if quiz.is_completed else None,
        "score": quiz.score,
        "percentage": quiz.percentage,
        "is_completed": quiz.is_completed,
        "created_at": quiz.created_at.isoformat()
    }
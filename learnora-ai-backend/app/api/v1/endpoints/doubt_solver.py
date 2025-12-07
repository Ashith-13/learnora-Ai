from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.doubt import Doubt, DoubtFollowUp
from app.services.openai.gpt4_service import gpt4_service
from app.services.pdf_parser import pdf_parser
from pydantic import BaseModel, Field
from typing import Optional, List
import os
import aiofiles

router = APIRouter()

class DoubtCreate(BaseModel):
    question: str = Field(..., min_length=10)
    subject: Optional[str] = None
    context: Optional[str] = None

class DoubtFollowUpCreate(BaseModel):
    doubt_id: int
    question: str = Field(..., min_length=5)

class DoubtRating(BaseModel):
    doubt_id: int
    rating: int = Field(..., ge=1, le=5)
    feedback: Optional[str] = None

@router.post("/ask")
async def ask_doubt(
    doubt_data: DoubtCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Ask a doubt and get AI-powered solution"""
    try:
        solution = await gpt4_service.solve_doubt(
            question=doubt_data.question,
            context=doubt_data.context,
            subject=doubt_data.subject
        )
        
        doubt = Doubt(
            user_id=current_user.id,
            question=doubt_data.question,
            subject=doubt_data.subject,
            context=doubt_data.context,
            answer=solution["answer"],
            explanation=solution["explanation"],
            related_resources=solution.get("related_resources", []),
            is_resolved=True
        )
        
        db.add(doubt)
        await db.commit()
        await db.refresh(doubt)
        
        return {
            "doubt_id": doubt.id,
            "question": doubt.question,
            "answer": doubt.answer,
            "explanation": doubt.explanation,
            "related_resources": doubt.related_resources,
            "created_at": doubt.created_at.isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error solving doubt: {str(e)}")

@router.post("/ask-with-file")
async def ask_doubt_with_file(
    question: str = Form(...),
    subject: Optional[str] = Form(None),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Ask doubt with uploaded PDF/document for context"""
    try:
        # Validate file type
        if not file.filename.endswith(('.pdf', '.txt', '.docx')):
            raise HTTPException(status_code=400, detail="Only PDF, TXT, and DOCX files are supported")
        
        # Save file temporarily
        file_path = f"uploads/temp/{file.filename}"
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Extract text based on file type
        if file.filename.endswith('.pdf'):
            extracted_text = pdf_parser.extract_text(file_path)
        elif file.filename.endswith('.txt'):
            async with aiofiles.open(file_path, 'r') as f:
                extracted_text = await f.read()
        else:
            extracted_text = "Document content analysis pending"
        
        # Limit context to prevent token overflow
        context = extracted_text[:4000] if extracted_text else ""
        
        solution = await gpt4_service.solve_doubt(
            question=question,
            context=context,
            subject=subject
        )
        
        doubt = Doubt(
            user_id=current_user.id,
            question=question,
            subject=subject,
            context=extracted_text[:1000],  # Store first 1000 chars
            answer=solution["answer"],
            explanation=solution["explanation"],
            related_resources=solution.get("related_resources", []),
            uploaded_files=[file.filename],
            is_resolved=True
        )
        
        db.add(doubt)
        await db.commit()
        await db.refresh(doubt)
        
        # Clean up temp file
        try:
            os.remove(file_path)
        except:
            pass
        
        return {
            "doubt_id": doubt.id,
            "question": doubt.question,
            "answer": doubt.answer,
            "explanation": doubt.explanation,
            "related_resources": doubt.related_resources,
            "uploaded_file": file.filename
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@router.post("/follow-up")
async def ask_follow_up(
    follow_up_data: DoubtFollowUpCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Ask follow-up question on existing doubt"""
    result = await db.execute(
        select(Doubt).where(
            (Doubt.id == follow_up_data.doubt_id) & (Doubt.user_id == current_user.id)
        )
    )
    doubt = result.scalar_one_or_none()
    
    if not doubt:
        raise HTTPException(status_code=404, detail="Doubt not found")
    
    context = f"""Previous question: {doubt.question}
Previous answer: {doubt.answer}

Follow-up question: {follow_up_data.question}"""
    
    solution = await gpt4_service.solve_doubt(
        question=follow_up_data.question,
        context=context,
        subject=doubt.subject
    )
    
    follow_up = DoubtFollowUp(
        doubt_id=doubt.id,
        question=follow_up_data.question,
        answer=solution["answer"]
    )
    
    db.add(follow_up)
    await db.commit()
    await db.refresh(follow_up)
    
    return {
        "follow_up_id": follow_up.id,
        "question": follow_up.question,
        "answer": follow_up.answer,
        "created_at": follow_up.created_at.isoformat()
    }

@router.post("/rate")
async def rate_doubt(
    rating_data: DoubtRating,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Rate doubt solution"""
    result = await db.execute(
        select(Doubt).where(
            (Doubt.id == rating_data.doubt_id) & (Doubt.user_id == current_user.id)
        )
    )
    doubt = result.scalar_one_or_none()
    
    if not doubt:
        raise HTTPException(status_code=404, detail="Doubt not found")
    
    doubt.rating = rating_data.rating
    doubt.feedback = rating_data.feedback
    
    await db.commit()
    
    return {
        "message": "Rating submitted successfully",
        "rating": rating_data.rating
    }

@router.get("/history")
async def get_doubt_history(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's doubt history"""
    result = await db.execute(
        select(Doubt)
        .where(Doubt.user_id == current_user.id)
        .order_by(Doubt.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    doubts = result.scalars().all()
    
    return [
        {
            "id": doubt.id,
            "question": doubt.question,
            "subject": doubt.subject,
            "answer": doubt.answer[:200] + "..." if len(doubt.answer) > 200 else doubt.answer,
            "is_resolved": doubt.is_resolved,
            "rating": doubt.rating,
            "created_at": doubt.created_at.isoformat()
        }
        for doubt in doubts
    ]

@router.get("/{doubt_id}")
async def get_doubt(
    doubt_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get specific doubt details"""
    result = await db.execute(
        select(Doubt).where(
            (Doubt.id == doubt_id) & (Doubt.user_id == current_user.id)
        )
    )
    doubt = result.scalar_one_or_none()
    
    if not doubt:
        raise HTTPException(status_code=404, detail="Doubt not found")
    
    # Get follow-ups
    follow_ups_result = await db.execute(
        select(DoubtFollowUp).where(DoubtFollowUp.doubt_id == doubt_id)
    )
    follow_ups = follow_ups_result.scalars().all()
    
    return {
        "id": doubt.id,
        "question": doubt.question,
        "subject": doubt.subject,
        "context": doubt.context,
        "answer": doubt.answer,
        "explanation": doubt.explanation,
        "related_resources": doubt.related_resources,
        "rating": doubt.rating,
        "feedback": doubt.feedback,
        "uploaded_files": doubt.uploaded_files,
        "follow_ups": [
            {
                "id": fu.id,
                "question": fu.question,
                "answer": fu.answer,
                "created_at": fu.created_at.isoformat()
            }
            for fu in follow_ups
        ],
        "created_at": doubt.created_at.isoformat()
    }

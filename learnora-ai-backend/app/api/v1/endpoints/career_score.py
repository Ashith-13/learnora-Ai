from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.career_profile import CareerProfile
from app.services.openai.gpt4_service import gpt4_service
from pydantic import BaseModel
from typing import Dict, Any, List

router = APIRouter()

class CareerAssessment(BaseModel):
    responses: Dict[str, Any]
    skills: List[str]
    interests: List[str]

@router.post("/assess")
async def assess_career(
    assessment_data: CareerAssessment,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Assess career profile and provide recommendations"""
    try:
        analysis = await gpt4_service.assess_career_profile(
            responses=assessment_data.responses,
            user_skills=assessment_data.skills,
            user_interests=assessment_data.interests
        )
        
        career_profile = CareerProfile(
            user_id=current_user.id,
            assessment_responses=assessment_data.responses,
            overall_score=analysis.get("overall_score", 0),
            technical_score=analysis.get("technical_score"),
            soft_skills_score=analysis.get("soft_skills_score"),
            domain_knowledge_score=analysis.get("domain_knowledge_score"),
            recommended_careers=analysis.get("recommended_careers", []),
            strengths=analysis.get("strengths", []),
            areas_for_improvement=analysis.get("areas_for_improvement", []),
            personality_traits=analysis.get("personality_traits", {}),
            career_interests=assessment_data.interests,
            work_values=analysis.get("work_values", {}),
            report=analysis.get("report", "")
        )
        
        db.add(career_profile)
        await db.commit()
        await db.refresh(career_profile)
        
        return {
            "profile_id": career_profile.id,
            "overall_score": career_profile.overall_score,
            "technical_score": career_profile.technical_score,
            "soft_skills_score": career_profile.soft_skills_score,
            "domain_knowledge_score": career_profile.domain_knowledge_score,
            "recommended_careers": career_profile.recommended_careers,
            "strengths": career_profile.strengths,
            "areas_for_improvement": career_profile.areas_for_improvement,
            "personality_traits": career_profile.personality_traits,
            "report": career_profile.report
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error assessing career: {str(e)}")

@router.get("/profile")
async def get_career_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's latest career profile"""
    result = await db.execute(
        select(CareerProfile)
        .where(CareerProfile.user_id == current_user.id)
        .order_by(CareerProfile.created_at.desc())
    )
    profile = result.scalars().first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="No career profile found. Please complete an assessment first.")
    
    return {
        "id": profile.id,
        "overall_score": profile.overall_score,
        "technical_score": profile.technical_score,
        "soft_skills_score": profile.soft_skills_score,
        "domain_knowledge_score": profile.domain_knowledge_score,
        "recommended_careers": profile.recommended_careers,
        "strengths": profile.strengths,
        "areas_for_improvement": profile.areas_for_improvement,
        "personality_traits": profile.personality_traits,
        "career_interests": profile.career_interests,
        "report": profile.report,
        "created_at": profile.created_at.isoformat()
    }

@router.get("/history")
async def get_assessment_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's assessment history"""
    result = await db.execute(
        select(CareerProfile)
        .where(CareerProfile.user_id == current_user.id)
        .order_by(CareerProfile.created_at.desc())
    )
    profiles = result.scalars().all()
    
    return [
        {
            "id": profile.id,
            "overall_score": profile.overall_score,
            "recommended_careers": profile.recommended_careers[:3],
            "created_at": profile.created_at.isoformat()
        }
        for profile in profiles
    ]

"""
Job Model
Stores job recommendations and postings
"""
from sqlalchemy import Column, String, Integer, ForeignKey, JSON, Text, Float, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import BaseModel


class Job(BaseModel):
    """Job model for storing job recommendations and postings"""
    __tablename__ = "jobs"

    # Job Information
    user = relationship("User", back_populates="jobs", overlaps="user")
    title = Column(String, nullable=False, index=True)
    company = Column(String, nullable=False)
    location = Column(String, nullable=True)
    job_type = Column(String, nullable=True)  # full-time, part-time, contract, internship
    work_mode = Column(String, nullable=True)  # remote, hybrid, on-site
    
    # Job Details
    description = Column(Text, nullable=False)
    requirements = Column(JSON, default=list)  # List of requirements
    responsibilities = Column(JSON, default=list)  # List of responsibilities
    skills_required = Column(JSON, default=list)  # Required skills
    skills_preferred = Column(JSON, default=list)  # Preferred skills
    
    # Compensation
    salary_min = Column(Integer, nullable=True)  # Minimum salary
    salary_max = Column(Integer, nullable=True)  # Maximum salary
    salary_currency = Column(String, default="USD")
    benefits = Column(JSON, default=list)  # List of benefits
    
    # Experience & Education
    experience_level = Column(String, nullable=True)  # entry, mid, senior, lead
    experience_years_min = Column(Integer, nullable=True)
    experience_years_max = Column(Integer, nullable=True)
    education_level = Column(String, nullable=True)  # high-school, bachelor, master, phd
    
    # Company Information
    company_size = Column(String, nullable=True)  # startup, small, medium, large, enterprise
    company_industry = Column(String, nullable=True)
    company_description = Column(Text, nullable=True)
    company_website = Column(String, nullable=True)
    company_logo_url = Column(String, nullable=True)
    
    # Application Details
    application_url = Column(String, nullable=True)
    application_email = Column(String, nullable=True)
    application_deadline = Column(DateTime, nullable=True)
    
    # Metadata
    source = Column(String, nullable=True)  # Where the job came from (API, manual, etc.)
    external_id = Column(String, nullable=True, unique=True)  # ID from external source
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    posted_date = Column(DateTime, default=datetime.utcnow)
    
    # Tags and Categories
    tags = Column(JSON, default=list)  # Custom tags
    category = Column(String, nullable=True)  # engineering, design, marketing, etc.
    
    # AI-Generated Fields
    match_score = Column(Float, nullable=True)  # Match score for a specific user (0-100)
    ai_summary = Column(Text, nullable=True)  # AI-generated summary
    
    # Relationships
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # User who posted or saved
    career_profile_id = Column(Integer, ForeignKey("career_profiles.id"), nullable=True)
    
    user = relationship("User", back_populates="jobs")
    career_profile = relationship("CareerProfile", back_populates="jobs")

    def __repr__(self):
        return f"<Job(id={self.id}, title='{self.title}', company='{self.company}')>"

    @property
    def salary_range(self) -> str:
        """Get formatted salary range"""
        if self.salary_min and self.salary_max:
            return f"{self.salary_currency} {self.salary_min:,} - {self.salary_max:,}"
        elif self.salary_min:
            return f"{self.salary_currency} {self.salary_min:,}+"
        elif self.salary_max:
            return f"Up to {self.salary_currency} {self.salary_max:,}"
        return "Not specified"

    @property
    def experience_range(self) -> str:
        """Get formatted experience range"""
        if self.experience_years_min and self.experience_years_max:
            return f"{self.experience_years_min}-{self.experience_years_max} years"
        elif self.experience_years_min:
            return f"{self.experience_years_min}+ years"
        elif self.experience_level:
            return self.experience_level.replace('-', ' ').title()
        return "Not specified"

    @property
    def is_expired(self) -> bool:
        """Check if application deadline has passed"""
        if self.application_deadline:
            return datetime.utcnow() > self.application_deadline
        return False

    def to_dict(self, include_sensitive: bool = False) -> dict:
        """
        Convert job to dictionary
        
        Args:
            include_sensitive: Include sensitive fields
            
        Returns:
            Dictionary representation
        """
        data = {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "job_type": self.job_type,
            "work_mode": self.work_mode,
            "description": self.description,
            "requirements": self.requirements,
            "responsibilities": self.responsibilities,
            "skills_required": self.skills_required,
            "skills_preferred": self.skills_preferred,
            "salary_range": self.salary_range,
            "benefits": self.benefits,
            "experience_range": self.experience_range,
            "experience_level": self.experience_level,
            "education_level": self.education_level,
            "company_size": self.company_size,
            "company_industry": self.company_industry,
            "company_description": self.company_description,
            "company_website": self.company_website,
            "company_logo_url": self.company_logo_url,
            "application_url": self.application_url,
            "is_active": self.is_active,
            "is_featured": self.is_featured,
            "is_expired": self.is_expired,
            "posted_date": self.posted_date.isoformat() if self.posted_date else None,
            "application_deadline": self.application_deadline.isoformat() if self.application_deadline else None,
            "tags": self.tags,
            "category": self.category,
            "match_score": self.match_score,
            "ai_summary": self.ai_summary,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_sensitive:
            data.update({
                "application_email": self.application_email,
                "source": self.source,
                "external_id": self.external_id,
                "user_id": self.user_id,
                "career_profile_id": self.career_profile_id
            })
        
        return data


class JobApplication(BaseModel):
    """Model for tracking user job applications"""
    __tablename__ = "job_applications"

    # References
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    
    # Application Status
    status = Column(String, default="applied")  # applied, reviewed, interview, offer, rejected, withdrawn
    applied_date = Column(DateTime, default=datetime.utcnow)
    status_updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Application Details
    cover_letter = Column(Text, nullable=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=True)
    custom_resume = Column(Boolean, default=False)  # Whether a custom resume was used
    
    # Interview Information
    interview_date = Column(DateTime, nullable=True)
    interview_notes = Column(Text, nullable=True)
    interview_feedback = Column(Text, nullable=True)
    
    # Offer Information
    offer_amount = Column(Integer, nullable=True)
    offer_currency = Column(String, default="USD")
    offer_date = Column(DateTime, nullable=True)
    offer_deadline = Column(DateTime, nullable=True)
    offer_accepted = Column(Boolean, nullable=True)
    
    # Notes and Follow-up
    notes = Column(Text, nullable=True)
    follow_up_date = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="job_applications")
    job = relationship("Job")
    resume = relationship("Resume")

    def __repr__(self):
        return f"<JobApplication(id={self.id}, user_id={self.user_id}, job_id={self.job_id}, status='{self.status}')>"

    @property
    def days_since_applied(self) -> int:
        """Calculate days since application was submitted"""
        if self.applied_date:
            delta = datetime.utcnow() - self.applied_date
            return delta.days
        return 0

    @property
    def is_pending(self) -> bool:
        """Check if application is still pending"""
        return self.status in ["applied", "reviewed", "interview"]

    @property
    def is_successful(self) -> bool:
        """Check if application resulted in an offer"""
        return self.status == "offer" or (self.offer_accepted is True)

    def to_dict(self) -> dict:
        """Convert application to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "job_id": self.job_id,
            "status": self.status,
            "applied_date": self.applied_date.isoformat() if self.applied_date else None,
            "status_updated_at": self.status_updated_at.isoformat() if self.status_updated_at else None,
            "days_since_applied": self.days_since_applied,
            "custom_resume": self.custom_resume,
            "interview_date": self.interview_date.isoformat() if self.interview_date else None,
            "interview_notes": self.interview_notes,
            "offer_amount": self.offer_amount,
            "offer_currency": self.offer_currency,
            "offer_date": self.offer_date.isoformat() if self.offer_date else None,
            "offer_accepted": self.offer_accepted,
            "notes": self.notes,
            "follow_up_date": self.follow_up_date.isoformat() if self.follow_up_date else None,
            "is_pending": self.is_pending,
            "is_successful": self.is_successful,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class SavedJob(BaseModel):
    """Model for users saving jobs for later"""
    __tablename__ = "saved_jobs"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    
    notes = Column(Text, nullable=True)
    reminder_date = Column(DateTime, nullable=True)
    is_archived = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", back_populates="saved_jobs")
    job = relationship("Job")

    def __repr__(self):
        return f"<SavedJob(id={self.id}, user_id={self.user_id}, job_id={self.job_id})>"

    def to_dict(self) -> dict:
        """Convert saved job to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "job_id": self.job_id,
            "notes": self.notes,
            "reminder_date": self.reminder_date.isoformat() if self.reminder_date else None,
            "is_archived": self.is_archived,
            "saved_at": self.created_at.isoformat() if self.created_at else None
        }
    
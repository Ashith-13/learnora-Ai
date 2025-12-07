from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime


class UserCreate(BaseModel):
    """Schema for user registration"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = Field(None, max_length=100)
    
    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.replace('_', '').replace('-', '').isalnum(), 'Username must be alphanumeric'
        return v


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """Schema for updating user profile"""
    full_name: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
    interests: Optional[List[str]] = None
    profile_image: Optional[str] = None
    
    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """Schema for user response"""
    id: int
    email: EmailStr
    username: str
    full_name: Optional[str]
    role: str
    is_active: bool
    is_verified: bool
    bio: Optional[str]
    interests: Optional[List[str]]
    profile_image: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Schema for authentication token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse

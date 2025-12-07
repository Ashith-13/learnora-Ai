import re
from typing import List, Optional
from fastapi import HTTPException, status
from app.core.config import settings


def validate_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, raises HTTPException if invalid
    """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_pattern, email):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid email format"
        )
    return True


def validate_password(password: str) -> bool:
    """
    Validate password strength
    
    Requirements:
    - At least 8 characters
    - Contains uppercase letter
    - Contains lowercase letter
    - Contains number
    - Contains special character
    
    Args:
        password: Password to validate
        
    Returns:
        True if valid, raises HTTPException if invalid
    """
    if len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password must be at least 8 characters long"
        )
    
    if not re.search(r'[A-Z]', password):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password must contain at least one uppercase letter"
        )
    
    if not re.search(r'[a-z]', password):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password must contain at least one lowercase letter"
        )
    
    if not re.search(r'\d', password):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password must contain at least one number"
        )
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password must contain at least one special character"
        )
    
    return True


def validate_file_size(file_size: int, max_size: Optional[int] = None) -> bool:
    """
    Validate file size
    
    Args:
        file_size: Size of file in bytes
        max_size: Maximum allowed size in bytes (default: from settings)
        
    Returns:
        True if valid, raises HTTPException if invalid
    """
    max_allowed = max_size or settings.MAX_UPLOAD_SIZE
    
    if file_size > max_allowed:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds maximum allowed size of {max_allowed / (1024*1024):.2f}MB"
        )
    
    return True


def validate_file_extension(filename: str, allowed_extensions: Optional[List[str]] = None) -> bool:
    """
    Validate file extension
    
    Args:
        filename: Name of the file
        allowed_extensions: List of allowed extensions (default: from settings)
        
    Returns:
        True if valid, raises HTTPException if invalid
    """
    allowed = allowed_extensions or settings.ALLOWED_EXTENSIONS
    extension = filename.split('.')[-1].lower()
    
    if extension not in allowed:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"File type '.{extension}' is not supported. Allowed types: {', '.join(allowed)}"
        )
    
    return True


def validate_quiz_parameters(
    num_questions: int,
    difficulty: str,
    time_limit: Optional[int] = None
) -> bool:
    """
    Validate quiz generation parameters
    
    Args:
        num_questions: Number of questions
        difficulty: Difficulty level
        time_limit: Time limit in seconds
        
    Returns:
        True if valid, raises HTTPException if invalid
    """
    if num_questions < settings.MIN_QUIZ_QUESTIONS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Minimum {settings.MIN_QUIZ_QUESTIONS} questions required"
        )
    
    if num_questions > settings.MAX_QUIZ_QUESTIONS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Maximum {settings.MAX_QUIZ_QUESTIONS} questions allowed"
        )
    
    valid_difficulties = ['easy', 'medium', 'hard']
    if difficulty.lower() not in valid_difficulties:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid difficulty. Must be one of: {', '.join(valid_difficulties)}"
        )
    
    if time_limit and time_limit < 60:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Time limit must be at least 60 seconds"
        )
    
    return True


def validate_url(url: str) -> bool:
    """
    Validate URL format
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid, raises HTTPException if invalid
    """
    url_pattern = r'^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$'
    
    if not re.match(url_pattern, url):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid URL format"
        )
    
    return True

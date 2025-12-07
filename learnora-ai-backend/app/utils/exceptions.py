from fastapi import HTTPException, status


class ValidationError(HTTPException):
    """Custom validation error"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )


class FileUploadError(HTTPException):
    """File upload error"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File upload error: {detail}"
        )


class QuizError(HTTPException):
    """Quiz-related error"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Quiz error: {detail}"
        )


class DoubtError(HTTPException):
    """Doubt-related error"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Doubt error: {detail}"
        )


class AIServiceError(HTTPException):
    """AI service error"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI service error: {detail}"
        )


class DatabaseError(HTTPException):
    """Database error"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {detail}"
        )


class AuthenticationError(HTTPException):
    """Authentication error"""
    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )


class AuthorizationError(HTTPException):
    """Authorization error"""
    def __init__(self, detail: str = "Not enough permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )


class NotFoundError(HTTPException):
    """Resource not found error"""
    def __init__(self, resource: str = "Resource"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} not found"
        )

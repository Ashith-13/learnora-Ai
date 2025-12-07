from fastapi import FastAPI, Request, status
from app.core.config import settings
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pydantic import ValidationError
import logging
import traceback

logger = logging.getLogger(__name__)


def add_exception_handlers(app: FastAPI) -> None:
    """
    Add custom exception handlers to the application
    
    Args:
        app: FastAPI application instance
    """
    
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """Handle HTTP exceptions"""
        logger.error(
            f"HTTP error occurred: {exc.status_code} - {exc.detail} "
            f"| Path: {request.url.path} | Method: {request.method}"
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.status_code,
                    "message": exc.detail,
                    "type": "HTTPException"
                }
            }
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle request validation errors"""
        errors = []
        for error in exc.errors():
            errors.append({
                "field": " -> ".join(str(loc) for loc in error["loc"]),
                "message": error["msg"],
                "type": error["type"]
            })
        
        logger.error(
            f"Validation error: {errors} "
            f"| Path: {request.url.path} | Method: {request.method}"
        )
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "error": {
                    "code": 422,
                    "message": "Validation error",
                    "type": "ValidationError",
                    "details": errors
                }
            }
        )
    
    @app.exception_handler(ValidationError)
    async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
        """Handle Pydantic validation errors"""
        logger.error(
            f"Pydantic validation error: {exc.errors()} "
            f"| Path: {request.url.path} | Method: {request.method}"
        )
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "error": {
                    "code": 422,
                    "message": "Data validation error",
                    "type": "PydanticValidationError",
                    "details": exc.errors()
                }
            }
        )
    
    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        """Handle database integrity errors"""
        logger.error(
            f"Database integrity error: {str(exc)} "
            f"| Path: {request.url.path} | Method: {request.method}"
        )
        
        # Extract meaningful error message
        error_message = "Database constraint violation"
        if "UNIQUE constraint failed" in str(exc):
            error_message = "Duplicate entry: This record already exists"
        elif "FOREIGN KEY constraint failed" in str(exc):
            error_message = "Invalid reference: Related record does not exist"
        elif "NOT NULL constraint failed" in str(exc):
            error_message = "Required field is missing"
        
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "success": False,
                "error": {
                    "code": 409,
                    "message": error_message,
                    "type": "IntegrityError"
                }
            }
        )
    
    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
        """Handle SQLAlchemy errors"""
        logger.error(
            f"Database error: {str(exc)} "
            f"| Path: {request.url.path} | Method: {request.method}",
            exc_info=True
        )
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "code": 500,
                    "message": "Database error occurred",
                    "type": "DatabaseError"
                }
            }
        )
    
    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        """Handle value errors"""
        logger.error(
            f"Value error: {str(exc)} "
            f"| Path: {request.url.path} | Method: {request.method}"
        )
        
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "error": {
                    "code": 400,
                    "message": str(exc),
                    "type": "ValueError"
                }
            }
        )
    
    @app.exception_handler(PermissionError)
    async def permission_error_handler(request: Request, exc: PermissionError):
        """Handle permission errors"""
        logger.error(
            f"Permission error: {str(exc)} "
            f"| Path: {request.url.path} | Method: {request.method}"
        )
        
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "success": False,
                "error": {
                    "code": 403,
                    "message": str(exc) or "You don't have permission to access this resource",
                    "type": "PermissionError"
                }
            }
        )
    
    @app.exception_handler(FileNotFoundError)
    async def file_not_found_error_handler(request: Request, exc: FileNotFoundError):
        """Handle file not found errors"""
        logger.error(
            f"File not found: {str(exc)} "
            f"| Path: {request.url.path} | Method: {request.method}"
        )
        
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "error": {
                    "code": 404,
                    "message": "File not found",
                    "type": "FileNotFoundError"
                }
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle all other unhandled exceptions"""
        # Log full traceback for debugging
        logger.exception(
            f"Unhandled exception: {type(exc).__name__} - {str(exc)} "
            f"| Path: {request.url.path} | Method: {request.method}"
        )
        
        # In production, don't expose internal error details
        error_message = "An unexpected error occurred"
        if settings.DEBUG:
            error_message = f"{type(exc).__name__}: {str(exc)}"
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "code": 500,
                    "message": error_message,
                    "type": type(exc).__name__
                }
            }
        )

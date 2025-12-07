import os
import uuid
import shutil
from pathlib import Path
from typing import Optional
from datetime import datetime, timedelta
from fastapi import UploadFile
from app.core.config import settings


def generate_unique_filename(original_filename: str) -> str:
    """
    Generate unique filename using UUID
    
    Args:
        original_filename: Original file name
        
    Returns:
        Unique filename with original extension
    """
    extension = original_filename.split('.')[-1]
    unique_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    return f"{timestamp}_{unique_id}.{extension}"


async def save_upload_file(
    file: UploadFile,
    destination_dir: str,
    custom_filename: Optional[str] = None
) -> str:
    """
    Save uploaded file to destination directory
    
    Args:
        file: Uploaded file
        destination_dir: Directory to save file
        custom_filename: Optional custom filename
        
    Returns:
        Path to saved file
    """
    # Create destination directory if it doesn't exist
    dest_path = Path(destination_dir)
    dest_path.mkdir(parents=True, exist_ok=True)
    
    # Generate filename
    filename = custom_filename or generate_unique_filename(file.filename)
    file_path = dest_path / filename
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return str(file_path)


def delete_file(file_path: str) -> bool:
    """
    Delete file from filesystem
    
    Args:
        file_path: Path to file
        
    Returns:
        True if deleted, False if file doesn't exist
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        print(f"Error deleting file {file_path}: {str(e)}")
        return False


def get_file_extension(filename: str) -> str:
    """
    Get file extension from filename
    
    Args:
        filename: Name of the file
        
    Returns:
        File extension without dot
    """
    return filename.split('.')[-1].lower()


def format_duration(seconds: int) -> str:
    """
    Format duration in seconds to human-readable string
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string (e.g., "2h 30m", "45m", "30s")
    """
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes}m"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        if minutes > 0:
            return f"{hours}h {minutes}m"
        return f"{hours}h"


def calculate_score(correct_answers: int, total_questions: int) -> float:
    """
    Calculate percentage score
    
    Args:
        correct_answers: Number of correct answers
        total_questions: Total number of questions
        
    Returns:
        Score as percentage (0-100)
    """
    if total_questions == 0:
        return 0.0
    return round((correct_answers / total_questions) * 100, 2)


def paginate(items: list, page: int = 1, page_size: int = 10) -> dict:
    """
    Paginate a list of items
    
    Args:
        items: List of items to paginate
        page: Current page number (1-indexed)
        page_size: Number of items per page
        
    Returns:
        Dictionary with paginated data and metadata
    """
    total_items = len(items)
    total_pages = (total_items + page_size - 1) // page_size
    
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    
    return {
        "items": items[start_idx:end_idx],
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_previous": page > 1
        }
    }


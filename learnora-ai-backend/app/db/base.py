from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime
from datetime import datetime

Base = declarative_base()

class TimestampMixin:
    """Mixin to add timestamp columns to models"""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class BaseModel(Base, TimestampMixin):
    """Base model with common columns"""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)

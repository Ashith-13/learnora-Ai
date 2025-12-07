import asyncio
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings
from app.db.base import Base

# Import all models to ensure they're registered
# FIXED: Removed Question import (doesn't exist in your models)
from app.models.user import User
from app.models.quiz import Quiz, QuizType, DifficultyLevel
from app.models.doubt import Doubt, DoubtFollowUp
from app.models.career_profile import CareerProfile, Job
from app.models.resume import Resume
from app.models.roadmap import Roadmap, LearningHistory


async def init_db():
    """Initialize database tables"""
    print("=" * 50)
    print("🚀 Learnora AI - Database Initialization")
    print("=" * 50)
    
    try:
        # Create async engine
        engine = create_async_engine(
            settings.DATABASE_URL,
            echo=True,
            pool_pre_ping=True
        )
        
        print(f"\n📊 Connecting to database: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'local'}")
        
        async with engine.begin() as conn:
            # Drop all tables (use with caution in production!)
            print("\n⚠️  Dropping existing tables...")
            await conn.run_sync(Base.metadata.drop_all)
            print("✅ Tables dropped successfully")
            
            # Create all tables
            print("\n🔨 Creating new tables...")
            await conn.run_sync(Base.metadata.create_all)
            print("✅ Tables created successfully")
        
        await engine.dispose()
        
        print("\n" + "=" * 50)
        print("✅ Database initialized successfully!")
        print("=" * 50)
        print("\n📝 Tables created:")
        for table_name in sorted(Base.metadata.tables.keys()):
            print(f"   • {table_name}")
        
        print("\n💡 Next steps:")
        print("   1. (Optional) Run seed script: python scripts/seed_data.py")
        print("   2. Start the server: uvicorn app.main:app --reload")
        print("   3. Access API docs: http://localhost:8000/docs")
        
    except Exception as e:
        print(f"\n❌ Error initializing database: {str(e)}")
        print("\n🔍 Troubleshooting:")
        print("   1. Check if PostgreSQL is running: brew services list")
        print("   2. Verify database exists: psql -l | grep learnora")
        print("   3. Check .env file has correct DATABASE_URL")
        print("   4. Ensure all dependencies installed: pip install -r requirements.txt")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(init_db())

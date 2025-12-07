import asyncio
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings
from app.db.base import Base

# Import all models to ensure they're registered
from app.models.user import User
from app.models.quiz import Quiz, Question
from app.models.doubt import Doubt, DoubtFollowUp
from app.models.career_profile import CareerProfile
from app.models.job import Job, JobApplication, SavedJob
from app.models.resume import Resume
from app.models.roadmap import Roadmap, LearningHistory
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init_database():
    """Initialize database tables"""
    
    print("=" * 60)
    print("🚀 Learnora AI - Database Initialization")
    print("=" * 60)
    
    try:
        # Create async engine
        engine = create_async_engine(
            settings.DATABASE_URL,
            echo=True,
            pool_pre_ping=True
        )
        
        logger.info("\n📊 Connecting to database...")
        logger.info(f"Database URL: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'local'}")
        
        async with engine.begin() as conn:
            # Drop all tables (use with caution!)
            logger.warning("\n⚠️  Dropping existing tables...")
            await conn.run_sync(Base.metadata.drop_all)
            logger.info("✅ Existing tables dropped")
            
            # Create all tables
            logger.info("\n🔨 Creating new tables...")
            await conn.run_sync(Base.metadata.create_all)
            logger.info("✅ All tables created successfully")
        
        await engine.dispose()
        
        print("\n" + "=" * 60)
        print("✅ Database Initialized Successfully!")
        print("=" * 60)
        
        print("\n📝 Tables created:")
        tables = [
            "users",
            "quizzes",
            "questions",
            "doubts",
            "doubt_followups",
            "career_profiles",
            "jobs",
            "job_applications",
            "saved_jobs",
            "resumes",
            "roadmaps",
            "learning_histories"
        ]
        
        for table in tables:
            print(f"   ✓ {table}")
        
        print("\n💡 Next steps:")
        print("   1. Seed sample data: python scripts/seed_data.py")
        print("   2. Start the server: uvicorn app.main:app --reload")
        print("   3. View API docs: http://localhost:8000/docs")
        
        return True
        
    except Exception as e:
        logger.error(f"\n❌ Error initializing database: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def check_database_connection():
    """Check if database is accessible"""
    try:
        engine = create_async_engine(
            settings.DATABASE_URL,
            echo=False,
            pool_pre_ping=True
        )
        
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
        
        await engine.dispose()
        logger.info("✅ Database connection successful")
        return True
        
    except Exception as e:
        logger.error(f"❌ Database connection failed: {str(e)}")
        return False


async def list_tables():
    """List all tables in the database"""
    try:
        engine = create_async_engine(
            settings.DATABASE_URL,
            echo=False
        )
        
        async with engine.begin() as conn:
            # Get table names
            result = await conn.run_sync(
                lambda sync_conn: Base.metadata.reflect(sync_conn.engine)
            )
            
            tables = list(Base.metadata.tables.keys())
            
            if tables:
                print("\n📋 Existing tables:")
                for table in sorted(tables):
                    print(f"   • {table}")
            else:
                print("\n⚠️  No tables found in database")
        
        await engine.dispose()
        
    except Exception as e:
        logger.error(f"Error listing tables: {str(e)}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Database initialization utility")
    parser.add_argument(
        "command",
        choices=["init", "check", "list"],
        help="Command to execute"
    )
    
    args = parser.parse_args()
    
    if args.command == "init":
        success = asyncio.run(init_database())
        sys.exit(0 if success else 1)
    
    elif args.command == "check":
        success = asyncio.run(check_database_connection())
        sys.exit(0 if success else 1)
    
    elif args.command == "list":
        asyncio.run(list_tables())
        sys.exit(0)


if __name__ == "__main__":
    # If run without arguments, default to init
    if len(sys.argv) == 1:
        success = asyncio.run(init_database())
        sys.exit(0 if success else 1)
    else:
        main()
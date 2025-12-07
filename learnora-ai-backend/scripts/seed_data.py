"""
Database Seed Script
Populates database with sample data for development
"""
import asyncio
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User
from app.models.roadmap import Roadmap
from app.models.quiz import Quiz, Question, QuizType, DifficultyLevel
from app.models.career_profile import CareerProfile


async def seed_data():
    """Seed database with sample data"""
    print("=" * 50)
    print("🌱 Learnora AI - Database Seeding")
    print("=" * 50)
    
    try:
        # Create async engine and session
        engine = create_async_engine(
            settings.DATABASE_URL,
            echo=False,
            pool_pre_ping=True
        )
        
        async_session = sessionmaker(
            engine, 
            class_=AsyncSession, 
            expire_on_commit=False
        )
        
        async with async_session() as session:
            print("\n👤 Creating users...")
            
            # Create admin user
            admin = User(
                email="admin@learnora.ai",
                username="admin",
                hashed_password=get_password_hash("admin123"),
                full_name="Admin User",
                role="admin",
                is_active=True,
                is_verified=True,
                bio="Platform Administrator"
            )
            session.add(admin)
            print("   ✓ Admin user created")
            
            # Create test students
            students_data = [
                {
                    "email": "student@test.com",
                    "username": "teststudent",
                    "full_name": "Test Student",
                    "interests": ["programming", "data science", "machine learning"],
                    "bio": "Aspiring Data Scientist"
                },
                {
                    "email": "john.doe@example.com",
                    "username": "johndoe",
                    "full_name": "John Doe",
                    "interests": ["web development", "react", "nodejs"],
                    "bio": "Full Stack Developer"
                },
                {
                    "email": "jane.smith@example.com",
                    "username": "janesmith",
                    "full_name": "Jane Smith",
                    "interests": ["ui/ux", "design", "frontend"],
                    "bio": "Creative UI/UX Designer"
                }
            ]
            
            students = []
            for student_data in students_data:
                student = User(
                    email=student_data["email"],
                    username=student_data["username"],
                    hashed_password=get_password_hash("student123"),
                    full_name=student_data["full_name"],
                    role="student",
                    is_active=True,
                    is_verified=True,
                    interests=student_data["interests"],
                    bio=student_data["bio"]
                )
                session.add(student)
                students.append(student)
            
            print(f"   ✓ {len(students)} student users created")
            
            # Commit users first to get IDs
            await session.commit()
            await session.refresh(admin)
            for student in students:
                await session.refresh(student)
            
            print("\n🗺️  Creating roadmap templates...")
            
            # Web Development Roadmap
            web_dev_roadmap = Roadmap(
                title="Full Stack Web Development",
                description="Complete roadmap to become a full-stack web developer from scratch",
                category="Programming",
                difficulty="intermediate",
                milestones=[
                    {
                        "id": 1,
                        "title": "HTML & CSS Fundamentals",
                        "description": "Learn the building blocks of web pages",
                        "duration_weeks": 2,
                        "topics": ["HTML5", "CSS3", "Flexbox", "Grid", "Responsive Design"],
                        "resources": [
                            {"name": "freeCodeCamp", "url": "https://freecodecamp.org", "type": "course"},
                            {"name": "MDN Web Docs", "url": "https://developer.mozilla.org", "type": "documentation"}
                        ],
                        "completed": False
                    },
                    {
                        "id": 2,
                        "title": "JavaScript Basics",
                        "description": "Master the language of the web",
                        "duration_weeks": 3,
                        "topics": ["Variables", "Functions", "Objects", "Arrays", "DOM Manipulation", "ES6+"],
                        "resources": [
                            {"name": "JavaScript.info", "url": "https://javascript.info", "type": "tutorial"},
                            {"name": "Eloquent JavaScript", "url": "https://eloquentjavascript.net", "type": "book"}
                        ],
                        "completed": False
                    },
                    {
                        "id": 3,
                        "title": "React Fundamentals",
                        "description": "Build modern user interfaces",
                        "duration_weeks": 4,
                        "topics": ["Components", "Props", "State", "Hooks", "Context API", "React Router"],
                        "resources": [
                            {"name": "React Official Docs", "url": "https://react.dev", "type": "documentation"},
                            {"name": "Full Stack Open", "url": "https://fullstackopen.com", "type": "course"}
                        ],
                        "completed": False
                    },
                    {
                        "id": 4,
                        "title": "Backend with Node.js",
                        "description": "Build scalable server-side applications",
                        "duration_weeks": 4,
                        "topics": ["Express.js", "REST APIs", "Authentication", "Databases", "Security"],
                        "resources": [
                            {"name": "Node.js Docs", "url": "https://nodejs.org", "type": "documentation"},
                            {"name": "The Odin Project", "url": "https://theodinproject.com", "type": "course"}
                        ],
                        "completed": False
                    },
                    {
                        "id": 5,
                        "title": "Database Management",
                        "description": "Store and manage data efficiently",
                        "duration_weeks": 3,
                        "topics": ["SQL", "PostgreSQL", "MongoDB", "ORMs", "Data Modeling"],
                        "resources": [
                            {"name": "PostgreSQL Tutorial", "url": "https://postgresqltutorial.com", "type": "tutorial"},
                            {"name": "MongoDB University", "url": "https://university.mongodb.com", "type": "course"}
                        ],
                        "completed": False
                    }
                ],
                estimated_duration=16*7,  # 16 weeks in days
                resources=[
                    {"name": "GitHub", "url": "https://github.com", "type": "platform"},
                    {"name": "Stack Overflow", "url": "https://stackoverflow.com", "type": "community"}
                ],
                prerequisites=["Basic computer literacy", "Problem-solving skills"],
                is_template=True,
                is_public=True,
                tags=["web-development", "javascript", "react", "nodejs", "fullstack"]
            )
            session.add(web_dev_roadmap)
            
            # Data Science Roadmap
            data_science_roadmap = Roadmap(
                title="Data Science & Machine Learning",
                description="Comprehensive path to becoming a data scientist",
                category="Data Science",
                difficulty="advanced",
                milestones=[
                    {
                        "id": 1,
                        "title": "Python Programming",
                        "description": "Master Python for data science",
                        "duration_weeks": 3,
                        "topics": ["Python Basics", "NumPy", "Pandas", "Data Structures"],
                        "resources": [
                            {"name": "Python.org Tutorial", "url": "https://python.org", "type": "tutorial"},
                            {"name": "Real Python", "url": "https://realpython.com", "type": "course"}
                        ],
                        "completed": False
                    },
                    {
                        "id": 2,
                        "title": "Statistics & Mathematics",
                        "description": "Build mathematical foundations",
                        "duration_weeks": 4,
                        "topics": ["Probability", "Statistics", "Linear Algebra", "Calculus"],
                        "resources": [
                            {"name": "Khan Academy", "url": "https://khanacademy.org", "type": "course"},
                            {"name": "StatQuest", "url": "https://statquest.org", "type": "video"}
                        ],
                        "completed": False
                    },
                    {
                        "id": 3,
                        "title": "Machine Learning",
                        "description": "Learn ML algorithms and applications",
                        "duration_weeks": 6,
                        "topics": ["Supervised Learning", "Unsupervised Learning", "Scikit-learn", "Model Evaluation"],
                        "resources": [
                            {"name": "Coursera ML", "url": "https://coursera.org", "type": "course"},
                            {"name": "Hands-On ML Book", "url": "https://oreilly.com", "type": "book"}
                        ],
                        "completed": False
                    }
                ],
                estimated_duration=13*7,
                is_template=True,
                is_public=True,
                tags=["data-science", "machine-learning", "python", "statistics"]
            )
            session.add(data_science_roadmap)
            
            # UI/UX Design Roadmap
            design_roadmap = Roadmap(
                title="UI/UX Design Mastery",
                description="Become a skilled UI/UX designer",
                category="Design",
                difficulty="beginner",
                milestones=[
                    {
                        "id": 1,
                        "title": "Design Principles",
                        "description": "Learn fundamental design concepts",
                        "duration_weeks": 2,
                        "topics": ["Color Theory", "Typography", "Layout", "Composition"],
                        "resources": [
                            {"name": "Refactoring UI", "url": "https://refactoringui.com", "type": "book"},
                            {"name": "Design Course", "url": "https://designcourse.com", "type": "video"}
                        ],
                        "completed": False
                    },
                    {
                        "id": 2,
                        "title": "Figma Mastery",
                        "description": "Master the industry-standard design tool",
                        "duration_weeks": 3,
                        "topics": ["Components", "Auto Layout", "Prototyping", "Design Systems"],
                        "resources": [
                            {"name": "Figma Learn", "url": "https://figma.com/learn", "type": "course"},
                            {"name": "Figma Community", "url": "https://figma.com/community", "type": "community"}
                        ],
                        "completed": False
                    }
                ],
                estimated_duration=5*7,
                is_template=True,
                is_public=True,
                tags=["design", "ui", "ux", "figma"]
            )
            session.add(design_roadmap)
            
            print(f"   ✓ 3 roadmap templates created")
            
            print("\n📝 Creating sample quizzes...")
            
            # Python Quiz
            python_quiz = Quiz(
                user_id=students[0].id,
                title="Python Fundamentals",
                description="Test your Python basics knowledge",
                subject="Python Programming",
                topic="Variables and Data Types",
                quiz_type=QuizType.PRACTICE,
                difficulty=DifficultyLevel.BEGINNER,
                total_questions=3,
                time_limit=600,  # 10 minutes
                passing_score=60.0
            )
            session.add(python_quiz)
            await session.flush()
            
            python_questions = [
                Question(
                    quiz_id=python_quiz.id,
                    question_text="What is the output of: print(type([]))?",
                    question_type="multiple_choice",
                    options=["<class 'list'>", "<class 'dict'>", "<class 'tuple'>", "<class 'set'>"],
                    correct_answer="<class 'list'>",
                    explanation="The type() function returns the type of an object. [] is a list.",
                    difficulty=DifficultyLevel.BEGINNER,
                    points=10
                ),
                Question(
                    quiz_id=python_quiz.id,
                    question_text="Which keyword is used to define a function in Python?",
                    question_type="multiple_choice",
                    options=["function", "def", "func", "define"],
                    correct_answer="def",
                    explanation="The 'def' keyword is used to define functions in Python.",
                    difficulty=DifficultyLevel.BEGINNER,
                    points=10
                ),
                Question(
                    quiz_id=python_quiz.id,
                    question_text="What is the result of 2 ** 3 in Python?",
                    question_type="multiple_choice",
                    options=["6", "8", "9", "5"],
                    correct_answer="8",
                    explanation="The ** operator is the exponentiation operator. 2 ** 3 = 2³ = 8",
                    difficulty=DifficultyLevel.BEGINNER,
                    points=10
                )
            ]
            
            for question in python_questions:
                session.add(question)
            
            print(f"   ✓ Python quiz with {len(python_questions)} questions created")
            
            print("\n💼 Creating sample career profiles...")
            
            # Career Profile for student
            career_profile = CareerProfile(
                user_id=students[0].id,
                assessment_completed=True,
                interests=["programming", "data analysis", "problem solving"],
                skills=["Python", "SQL", "Data Analysis"],
                personality_traits=["analytical", "detail-oriented", "curious"],
                work_preferences=["remote", "flexible hours", "continuous learning"],
                career_recommendations=[
                    {
                        "title": "Data Scientist",
                        "match_score": 85,
                        "reasons": ["Strong analytical skills", "Python expertise", "Problem-solving ability"]
                    },
                    {
                        "title": "Backend Developer",
                        "match_score": 78,
                        "reasons": ["Programming skills", "Logical thinking", "Technical aptitude"]
                    }
                ],
                strength_areas=["Technical Skills", "Analytical Thinking", "Problem Solving"],
                improvement_areas=["Communication", "Project Management"]
            )
            session.add(career_profile)
            print("   ✓ Career profile created")
            
            # Commit all data
            await session.commit()
            
        await engine.dispose()
        
        print("\n" + "=" * 50)
        print("✅ Database seeded successfully!")
        print("=" * 50)
        print("\n📊 Summary:")
        print("   • 4 users created (1 admin, 3 students)")
        print("   • 3 roadmap templates created")
        print("   • 1 sample quiz created")
        print("   • 1 career profile created")
        print("\n🔑 Login Credentials:")
        print("   Admin:")
        print("     Email: admin@learnora.ai")
        print("     Password: admin123")
        print("\n   Test Student:")
        print("     Email: student@test.com")
        print("     Password: student123")
        print("\n💡 Next step:")
        print("   Start the server: uvicorn app.main:app --reload")
        
    except Exception as e:
        print(f"\n❌ Error seeding database: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(seed_data())
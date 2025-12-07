# Learnora AI Backend

AI-powered adaptive learning platform with GPT-4 integration for personalized education experiences.

## Features

- 🎯 **Adaptive Quiz Generation** - AI-generated quizzes with difficulty adjustment
- ❓ **Intelligent Doubt Solver** - RAG-powered question answering with context from uploaded documents
- 📊 **Career Assessment** - Comprehensive career scoring and recommendations
- 📄 **AI Resume Builder** - ATS-optimized resume generation
- 🗺️ **Learning Roadmaps** - Personalized learning paths
- 🎥 **Video Content Generator** - Educational video creation
- 🥽 **AR Labs Integration** - Augmented reality learning experiences
- 💼 **Job Recommendations** - AI-powered job matching

## Tech Stack

- **Framework**: FastAPI (Python 3.10+)
- **Database**: PostgreSQL with SQLAlchemy (async)
- **AI**: OpenAI GPT-4, Embeddings, DALL·E
- **Vector DB**: Pinecone for RAG
- **Authentication**: JWT tokens
- **Task Queue**: Celery with Redis
- **Migration**: Alembic

## Quick Start

### 1. Clone and Setup

```bash
cd learnora-ai-backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Generate with `openssl rand -hex 32`
- `OPENAI_API_KEY`: Your OpenAI API key
- `PINECONE_API_KEY`: Your Pinecone API key

### 3. Initialize Database

```bash
# Create database tables
python scripts/init_db.py

# Or use Alembic migrations
alembic upgrade head
```

### 4. Run Server

```bash
# Development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Visit:
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## Project Structure

```
learnora-ai-backend/
├── app/
│   ├── api/v1/endpoints/    # API route handlers
│   ├── core/                # Config, security, celery
│   ├── db/                  # Database setup
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic & AI services
│   ├── crud/                # Database operations
│   ├── utils/               # Helper functions
│   └── middleware/          # CORS, error handling
├── alembic/                 # Database migrations
├── tests/                   # Test suite
├── scripts/                 # Utility scripts
└── uploads/                 # File uploads
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user

### Quiz System
- `POST /api/v1/quiz/generate` - Generate adaptive quiz
- `POST /api/v1/quiz/submit` - Submit quiz answers
- `GET /api/v1/quiz/history` - Get quiz history
- `GET /api/v1/quiz/{quiz_id}` - Get quiz details

### Doubt Solver
- `POST /api/v1/doubts/ask` - Ask a doubt
- `POST /api/v1/doubts/ask-with-file` - Ask with uploaded document
- `POST /api/v1/doubts/follow-up` - Follow-up question
- `POST /api/v1/doubts/rate` - Rate solution
- `GET /api/v1/doubts/history` - Get doubt history

### Career Assessment
- `POST /api/v1/career/assess` - Complete career assessment
- `GET /api/v1/career/profile` - Get career profile
- `GET /api/v1/career/history` - Assessment history

## Database Setup

### PostgreSQL Installation

**macOS:**
```bash
brew install postgresql@14
brew services start postgresql@14
createdb learnora_db
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo -u postgres createdb learnora_db
```

### Redis Installation (for Celery)

**macOS:**
```bash
brew install redis
brew services start redis
```

**Ubuntu/Debian:**
```bash
sudo apt install redis-server
sudo systemctl start redis
```

## Development

### Running Tests

```bash
pytest
pytest --cov=app tests/
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Code Quality

```bash
# Format code
black app/

# Lint
flake8 app/

# Type checking
mypy app/
```

## Docker Deployment (Optional)

```bash
# Development
docker-compose -f docker/docker-compose.dev.yml up

# Production
docker-compose -f docker/docker-compose.yml up -d
```

## Environment Variables

See `.env.example` for all configuration options.

Required:
- `DATABASE_URL`
- `SECRET_KEY`
- `OPENAI_API_KEY`
- `PINECONE_API_KEY`

Optional:
- `REDIS_URL`
- `SMTP_*` (for email)
- API keys for job services

## Production Deployment

1. Set `DEBUG=False` and `ENVIRONMENT=production`
2. Use strong `SECRET_KEY`
3. Configure HTTPS/SSL
4. Set up proper CORS origins
5. Use production database
6. Configure monitoring/logging
7. Set up backups

## Contributing

1. Create feature branch
2. Make changes
3. Write tests
4. Submit pull request

## License

MIT License - see LICENSE file

## Support

For issues and questions:
- GitHub Issues: [repository-url]
- Email: support@learnora.ai

## Roadmap

- [ ] Resume Builder endpoints
- [ ] Learning Roadmaps API
- [ ] Video Generation service
- [ ] AR Labs integration
- [ ] Job Recommendations engine
- [ ] Websocket support for real-time features
- [ ] Advanced analytics dashboard
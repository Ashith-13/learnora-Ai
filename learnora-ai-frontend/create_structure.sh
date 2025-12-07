mkdir -p learnora-ai-backend
cd learnora-ai-backend

touch .env.example .gitignore requirements.txt README.md pytest.ini alembic.ini

mkdir -p docker
touch docker/docker-compose.yml docker/docker-compose.dev.yml docker/Dockerfile docker/Dockerfile.dev docker/.dockerignore

mkdir -p app/api/v1/endpoints app/core app/db app/models app/schemas app/services/openai app/services/rag app/crud app/utils app/middleware

touch app/__init__.py app/main.py app/config.py
touch app/api/__init__.py app/api/deps.py app/api/v1/__init__.py app/api/v1/router.py

touch app/api/v1/endpoints/__init__.py app/api/v1/endpoints/auth.py app/api/v1/endpoints/users.py app/api/v1/endpoints/quiz.py app/api/v1/endpoints/doubt_solver.py app/api/v1/endpoints/career_score.py app/api/v1/endpoints/resume_builder.py app/api/v1/endpoints/roadmaps.py app/api/v1/endpoints/video_generator.py app/api/v1/endpoints/ar_labs.py app/api/v1/endpoints/jobs.py app/api/v1/endpoints/upload.py

touch app/core/__init__.py app/core/security.py app/core/config.py app/core/celery_app.py
touch app/db/__init__.py app/db/base.py app/db/session.py app/db/init_db.py
touch app/models/__init__.py app/models/user.py app/models/quiz.py app/models/doubt.py app/models/career_profile.py app/models/learning_history.py app/models/resume.py app/models/roadmap.py app/models/job.py
touch app/schemas/__init__.py app/schemas/user.py app/schemas/quiz.py app/schemas/doubt.py app/schemas/career.py app/schemas/resume.py app/schemas/roadmap.py app/schemas/common.py

touch app/services/__init__.py app/services/openai/__init__.py app/services/openai/gpt4_service.py app/services/openai/whisper_service.py app/services/openai/dalle_service.py app/services/openai/embeddings_service.py
touch app/services/rag/__init__.py app/services/rag/pinecone_service.py app/services/rag/vector_store.py app/services/rag/retrieval.py
touch app/services/quiz_service.py app/services/doubt_solver_service.py app/services/career_service.py app/services/resume_service.py app/services/video_service.py app/services/pdf_parser.py app/services/file_handler.py

touch app/crud/__init__.py app/crud/base.py app/crud/user.py app/crud/quiz.py app/crud/doubt.py app/crud/career.py app/crud/learning_history.py
touch app/utils/__init__.py app/utils/validators.py app/utils/helpers.py app/utils/logger.py app/utils/exceptions.py
touch app/middleware/__init__.py app/middleware/error_handler.py app/middleware/cors.py app/middleware/rate_limiter.py

mkdir -p alembic/versions
touch alembic/env.py alembic/script.py.mako alembic/README

mkdir -p tests/api tests/services tests/utils
touch tests/__init__.py tests/conftest.py tests/api/__init__.py tests/api/test_auth.py tests/api/test_quiz.py tests/api/test_doubt_solver.py tests/services/__init__.py tests/services/test_gpt4.py tests/services/test_rag.py tests/utils/__init__.py tests/utils/test_helpers.py

mkdir -p scripts
touch scripts/init_db.py scripts/seed_data.py scripts/migrate.py scripts/run_local.sh
chmod +x scripts/run_local.sh

mkdir -p uploads/pdfs uploads/audio uploads/temp
touch uploads/pdfs/.gitkeep uploads/audio/.gitkeep uploads/temp/.gitkeep alembic/versions/.gitkeep

echo "Done!"

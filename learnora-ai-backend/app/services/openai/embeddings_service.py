from openai import AsyncOpenAI
from typing import List
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class EmbeddingsService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_EMBEDDING_MODEL
    
    async def create_embedding(self, text: str) -> List[float]:
        """Create embedding for text"""
        try:
            response = await self.client.embeddings.create(
                model=self.model,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Embedding creation error: {str(e)}")
            raise
    
    async def create_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Create embeddings for multiple texts"""
        try:
            response = await self.client.embeddings.create(
                model=self.model,
                input=texts
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            logger.error(f"Batch embedding creation error: {str(e)}")
            raise

embeddings_service = EmbeddingsService()
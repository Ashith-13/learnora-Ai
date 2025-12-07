from openai import AsyncOpenAI
from typing import Optional
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class DalleService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def generate_image(
        self,
        prompt: str,
        size: str = "1024x1024",
        quality: str = "standard",
        n: int = 1
    ) -> list[str]:
        """Generate images using DALL-E"""
        try:
            response = await self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality=quality,
                n=n
            )
            return [img.url for img in response.data]
        except Exception as e:
            logger.error(f"DALL-E generation error: {str(e)}")
            raise

dalle_service = DalleService()

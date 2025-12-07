from openai import AsyncOpenAI
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class WhisperService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def transcribe_audio(self, audio_file_path: str) -> str:
        """Transcribe audio using Whisper"""
        try:
            with open(audio_file_path, "rb") as audio_file:
                transcript = await self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            return transcript.text
        except Exception as e:
            logger.error(f"Whisper transcription error: {str(e)}")
            raise

whisper_service = WhisperService()
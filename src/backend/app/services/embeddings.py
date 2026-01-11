"""
Embedding Service
Generates vector embeddings for text chunks using OpenAI or local models
"""

from typing import List, Optional
import asyncio

from openai import AsyncOpenAI

from app.config import get_settings

settings = get_settings()


class EmbeddingService:
    """Generate embeddings for text using OpenAI or fallback models"""

    def __init__(self):
        self.openai_client: Optional[AsyncOpenAI] = None
        self.model = "text-embedding-3-small"  # 1536 dims, cheaper than ada-002
        self.dimensions = 768  # Request 768 dims to match our DB schema

        if settings.openai_api_key:
            self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        embeddings = await self.embed_texts([text])
        return embeddings[0]

    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        if not texts:
            return []

        if self.openai_client:
            return await self._embed_openai(texts)
        else:
            # Fallback: return zero vectors (embeddings disabled)
            return [[0.0] * self.dimensions for _ in texts]

    async def _embed_openai(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using OpenAI API"""
        # OpenAI has a limit of ~8000 tokens per request, batch if needed
        batch_size = 100
        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]

            response = await self.openai_client.embeddings.create(
                model=self.model,
                input=batch,
                dimensions=self.dimensions,  # Request specific dimensions
            )

            batch_embeddings = [item.embedding for item in response.data]
            all_embeddings.extend(batch_embeddings)

        return all_embeddings

    def is_available(self) -> bool:
        """Check if embedding service is available"""
        return self.openai_client is not None


# Singleton instance
_embedding_service: Optional[EmbeddingService] = None


def get_embedding_service() -> EmbeddingService:
    """Get or create embedding service instance"""
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service

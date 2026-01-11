"""
Chat Service
Handles Q&A with RAG using Claude or OpenAI
"""

from typing import Optional, List, AsyncGenerator
from uuid import UUID

from anthropic import AsyncAnthropic
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.services.search import SearchService

settings = get_settings()


class ChatService:
    """RAG-powered chat service"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.search_service = SearchService(db)

        # Initialize LLM clients
        self.anthropic_client: Optional[AsyncAnthropic] = None
        self.openai_client: Optional[AsyncOpenAI] = None

        if settings.anthropic_api_key:
            self.anthropic_client = AsyncAnthropic(api_key=settings.anthropic_api_key)
        if settings.openai_api_key:
            self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)

    def _get_system_prompt(self, context: str) -> str:
        """Generate system prompt with context"""
        return f"""You are GrantPilot, an AI assistant helping researchers write grant proposals.

You have access to the following context from the user's documents:

<context>
{context}
</context>

Instructions:
- Answer questions based on the provided context when relevant
- Be helpful and specific with grant writing advice
- If you cite information from the documents, mention the source
- If the context doesn't contain relevant information, say so and provide general guidance
- Be concise but thorough
- Use scientific writing style appropriate for grant proposals"""

    async def chat(
        self,
        message: str,
        project_id: Optional[UUID] = None,
        history: Optional[List[dict]] = None,
    ) -> str:
        """
        Process a chat message with RAG.

        Args:
            message: User's message
            project_id: Optional project for context filtering
            history: Optional conversation history

        Returns:
            Assistant's response
        """
        # Get relevant context
        context = await self.search_service.get_context_for_query(
            message, project_id=project_id
        )

        system_prompt = self._get_system_prompt(context if context else "No documents loaded yet.")

        # Prefer Claude, fallback to OpenAI
        if self.anthropic_client:
            return await self._chat_anthropic(system_prompt, message, history)
        elif self.openai_client:
            return await self._chat_openai(system_prompt, message, history)
        else:
            return "No LLM API key configured. Please set ANTHROPIC_API_KEY or OPENAI_API_KEY."

    async def _chat_anthropic(
        self, system_prompt: str, message: str, history: Optional[List[dict]]
    ) -> str:
        """Chat using Claude"""
        messages = []

        if history:
            for msg in history:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"],
                })

        messages.append({"role": "user", "content": message})

        response = await self.anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            system=system_prompt,
            messages=messages,
        )

        return response.content[0].text

    async def _chat_openai(
        self, system_prompt: str, message: str, history: Optional[List[dict]]
    ) -> str:
        """Chat using OpenAI"""
        messages = [{"role": "system", "content": system_prompt}]

        if history:
            for msg in history:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"],
                })

        messages.append({"role": "user", "content": message})

        response = await self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=2048,
        )

        return response.choices[0].message.content

    async def chat_stream(
        self,
        message: str,
        project_id: Optional[UUID] = None,
        history: Optional[List[dict]] = None,
    ) -> AsyncGenerator[str, None]:
        """
        Stream chat response.

        Yields:
            Chunks of the response text
        """
        context = await self.search_service.get_context_for_query(
            message, project_id=project_id
        )

        system_prompt = self._get_system_prompt(context if context else "No documents loaded yet.")

        if self.anthropic_client:
            async for chunk in self._stream_anthropic(system_prompt, message, history):
                yield chunk
        elif self.openai_client:
            async for chunk in self._stream_openai(system_prompt, message, history):
                yield chunk
        else:
            yield "No LLM API key configured."

    async def _stream_anthropic(
        self, system_prompt: str, message: str, history: Optional[List[dict]]
    ) -> AsyncGenerator[str, None]:
        """Stream using Claude"""
        messages = []

        if history:
            for msg in history:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"],
                })

        messages.append({"role": "user", "content": message})

        async with self.anthropic_client.messages.stream(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            system=system_prompt,
            messages=messages,
        ) as stream:
            async for text in stream.text_stream:
                yield text

    async def _stream_openai(
        self, system_prompt: str, message: str, history: Optional[List[dict]]
    ) -> AsyncGenerator[str, None]:
        """Stream using OpenAI"""
        messages = [{"role": "system", "content": system_prompt}]

        if history:
            for msg in history:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"],
                })

        messages.append({"role": "user", "content": message})

        stream = await self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=2048,
            stream=True,
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    def is_available(self) -> bool:
        """Check if chat service is available"""
        return self.anthropic_client is not None or self.openai_client is not None

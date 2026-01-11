"""
Chat API endpoints
"""

from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.db.database import get_db
from app.services.chat import ChatService
from app.services.search import SearchService

router = APIRouter()


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    project_id: Optional[UUID] = None
    history: Optional[List[ChatMessage]] = None
    stream: bool = False


class ChatResponse(BaseModel):
    response: str
    sources: Optional[List[dict]] = None


class SearchRequest(BaseModel):
    query: str
    project_id: Optional[UUID] = None
    document_ids: Optional[List[UUID]] = None
    limit: int = 5


class SearchResponse(BaseModel):
    results: List[dict]
    query: str


@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Chat with the AI assistant using RAG.
    """
    chat_service = ChatService(db)

    if not chat_service.is_available():
        raise HTTPException(
            status_code=503,
            detail="No LLM API key configured. Set ANTHROPIC_API_KEY or OPENAI_API_KEY.",
        )

    # Convert history to dict format
    history = None
    if request.history:
        history = [{"role": m.role, "content": m.content} for m in request.history]

    if request.stream:
        # Return streaming response
        async def generate():
            async for chunk in chat_service.chat_stream(
                request.message,
                project_id=request.project_id,
                history=history,
            ):
                yield chunk

        return StreamingResponse(generate(), media_type="text/plain")

    # Non-streaming response
    response = await chat_service.chat(
        request.message,
        project_id=request.project_id,
        history=history,
    )

    # Get sources used
    search_service = SearchService(db)
    search_results = await search_service.search(
        request.message,
        project_id=request.project_id,
        limit=3,
    )

    sources = [r.to_dict() for r in search_results] if search_results else None

    return ChatResponse(response=response, sources=sources)


@router.post("/stream")
async def chat_stream(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Stream chat response.
    """
    chat_service = ChatService(db)

    if not chat_service.is_available():
        raise HTTPException(
            status_code=503,
            detail="No LLM API key configured.",
        )

    history = None
    if request.history:
        history = [{"role": m.role, "content": m.content} for m in request.history]

    async def generate():
        async for chunk in chat_service.chat_stream(
            request.message,
            project_id=request.project_id,
            history=history,
        ):
            yield chunk

    return StreamingResponse(generate(), media_type="text/plain")


@router.post("/search", response_model=SearchResponse)
async def search_documents(
    request: SearchRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Search documents using semantic similarity.
    """
    search_service = SearchService(db)

    results = await search_service.search(
        request.query,
        project_id=request.project_id,
        document_ids=request.document_ids,
        limit=request.limit,
    )

    return SearchResponse(
        results=[r.to_dict() for r in results],
        query=request.query,
    )

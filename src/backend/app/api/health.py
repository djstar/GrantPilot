"""
Health check endpoints
"""

import redis.asyncio as redis
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from pydantic import BaseModel
from typing import Optional, Dict, Any

from app.db.database import get_db
from app.config import get_settings
from app.services.embeddings import get_embedding_service

router = APIRouter()
settings = get_settings()


class ServiceStatus(BaseModel):
    status: str  # "healthy", "unhealthy", "unconfigured"
    message: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class FullHealthResponse(BaseModel):
    status: str  # "healthy", "degraded", "unhealthy"
    services: Dict[str, ServiceStatus]
    version: str = "0.1.0"


@router.get("/health")
async def health_check():
    """Basic health check"""
    return {"status": "healthy"}


@router.get("/health/db")
async def database_health(db: AsyncSession = Depends(get_db)):
    """Database connection health check"""
    try:
        result = await db.execute(text("SELECT 1"))
        result.fetchone()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}


@router.get("/health/redis")
async def redis_health():
    """Redis connection health check"""
    try:
        client = redis.from_url(settings.redis_url)
        await client.ping()
        await client.close()
        return {"status": "healthy", "redis": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "redis": "disconnected", "error": str(e)}


@router.get("/health/embeddings")
async def embeddings_health():
    """Embedding service health check"""
    embedding_service = get_embedding_service()

    if not embedding_service.is_available():
        return {
            "status": "unconfigured",
            "message": "OPENAI_API_KEY not set",
            "embeddings_enabled": False,
        }

    try:
        # Test with a small embedding
        test_embedding = await embedding_service.embed_text("test")
        return {
            "status": "healthy",
            "embeddings_enabled": True,
            "model": embedding_service.model,
            "dimensions": len(test_embedding),
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "embeddings_enabled": False,
            "error": str(e),
        }


@router.get("/health/llm")
async def llm_health():
    """LLM service health check"""
    from app.services.chat import ChatService
    from app.db.database import async_session_maker

    async with async_session_maker() as db:
        chat_service = ChatService(db)

        result = {
            "status": "unconfigured",
            "anthropic": "unconfigured",
            "openai": "unconfigured",
        }

        if chat_service.anthropic_client:
            result["anthropic"] = "configured"
            result["status"] = "healthy"

        if chat_service.openai_client:
            result["openai"] = "configured"
            result["status"] = "healthy"

        if result["status"] == "unconfigured":
            result["message"] = "No LLM API keys configured. Set ANTHROPIC_API_KEY or OPENAI_API_KEY."

        return result


@router.get("/health/full", response_model=FullHealthResponse)
async def full_health_check(db: AsyncSession = Depends(get_db)):
    """
    Comprehensive health check of all services.
    Returns detailed status for each component.
    """
    services = {}

    # Database check
    try:
        result = await db.execute(text("SELECT 1"))
        result.fetchone()
        # Check pgvector extension
        await db.execute(text("SELECT '[1,2,3]'::vector(3)"))
        services["database"] = ServiceStatus(
            status="healthy",
            message="PostgreSQL with pgvector",
            details={"extension": "pgvector"}
        )
    except Exception as e:
        services["database"] = ServiceStatus(
            status="unhealthy",
            message=str(e)
        )

    # Redis check
    try:
        client = redis.from_url(settings.redis_url)
        await client.ping()
        info = await client.info("server")
        await client.close()
        services["redis"] = ServiceStatus(
            status="healthy",
            message="Redis connected",
            details={"version": info.get("redis_version")}
        )
    except Exception as e:
        services["redis"] = ServiceStatus(
            status="unhealthy",
            message=str(e)
        )

    # Embeddings check
    embedding_service = get_embedding_service()
    if embedding_service.is_available():
        services["embeddings"] = ServiceStatus(
            status="healthy",
            message=f"OpenAI {embedding_service.model}",
            details={"dimensions": embedding_service.dimensions}
        )
    else:
        services["embeddings"] = ServiceStatus(
            status="unconfigured",
            message="OPENAI_API_KEY not set"
        )

    # LLM check
    anthropic_configured = bool(settings.anthropic_api_key)
    openai_configured = bool(settings.openai_api_key)

    if anthropic_configured or openai_configured:
        llm_providers = []
        if anthropic_configured:
            llm_providers.append("Claude")
        if openai_configured:
            llm_providers.append("OpenAI")
        services["llm"] = ServiceStatus(
            status="healthy",
            message=", ".join(llm_providers),
            details={
                "anthropic": anthropic_configured,
                "openai": openai_configured
            }
        )
    else:
        services["llm"] = ServiceStatus(
            status="unconfigured",
            message="No LLM API keys configured"
        )

    # Determine overall status
    statuses = [s.status for s in services.values()]
    if all(s == "healthy" for s in statuses):
        overall = "healthy"
    elif "unhealthy" in statuses:
        overall = "unhealthy"
    else:
        overall = "degraded"  # Some services unconfigured but core working

    return FullHealthResponse(
        status=overall,
        services=services,
        version="0.1.0"
    )


@router.get("/health/ready")
async def readiness_check(db: AsyncSession = Depends(get_db)):
    """Full readiness check"""
    checks = {
        "api": "healthy",
        "database": "unknown",
    }

    try:
        result = await db.execute(text("SELECT 1"))
        result.fetchone()
        checks["database"] = "healthy"
    except Exception:
        checks["database"] = "unhealthy"

    all_healthy = all(v == "healthy" for v in checks.values())

    return {
        "status": "ready" if all_healthy else "not_ready",
        "checks": checks,
    }

"""
GrantPilot FastAPI Application
Main entry point for the backend server
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.db.database import engine, Base
from app.api import projects, documents, health, chat


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print(f"🚀 Starting {settings.app_name}...")

    # Create database tables (in dev mode)
    if settings.environment == "development":
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✓ Database tables created/verified")

    yield

    # Shutdown
    print(f"👋 Shutting down {settings.app_name}...")
    await engine.dispose()


app = FastAPI(
    title=settings.app_name,
    description="AI-powered grant writing co-pilot",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.app_name,
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs",
    }

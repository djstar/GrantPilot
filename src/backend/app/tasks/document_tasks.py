"""
Document Processing Celery Tasks
"""

import os
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.celery_app import celery_app
from app.config import get_settings
from app.db.models import Document, DocumentChunk
from app.processors.document_processor import process_document
from app.services.embeddings import get_embedding_service

settings = get_settings()

# Sync engine for Celery (Celery doesn't support async well)
sync_engine = create_engine(
    settings.database_url.replace("postgresql://", "postgresql+psycopg2://")
    if "postgresql://" in settings.database_url
    else settings.database_url.replace("postgresql+asyncpg://", "postgresql+psycopg2://")
)
SessionLocal = sessionmaker(bind=sync_engine)


@celery_app.task(bind=True, max_retries=3)
def process_document_task(self, document_id: str, file_path: str):
    """
    Process an uploaded document:
    1. Extract text from file
    2. Split into chunks
    3. Store chunks in database
    4. Update document status
    """
    db = SessionLocal()

    try:
        # Get document record
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise ValueError(f"Document {document_id} not found")

        # Update status to processing
        document.processing_status = "processing"
        db.commit()

        # Process the document
        result = process_document(file_path)

        # Update document metadata
        document.page_count = result["page_count"]
        document.word_count = result["word_count"]

        # Create chunks
        chunk_texts = [chunk_data["text"] for chunk_data in result["chunks"]]
        chunks_created = []

        for chunk_data in result["chunks"]:
            chunk = DocumentChunk(
                document_id=document_id,
                chunk_index=chunk_data["index"],
                content=chunk_data["text"],
                start_char=chunk_data["start_char"],
                end_char=chunk_data["end_char"],
                word_count=chunk_data["word_count"],
            )
            db.add(chunk)
            chunks_created.append(chunk)

        db.flush()  # Get chunk IDs

        # Generate embeddings if service is available
        embedding_service = get_embedding_service()
        embeddings_generated = 0

        if embedding_service.is_available() and chunk_texts:
            # Run async embedding generation in sync context
            loop = asyncio.new_event_loop()
            try:
                embeddings = loop.run_until_complete(
                    embedding_service.embed_texts(chunk_texts)
                )
                for chunk, embedding in zip(chunks_created, embeddings):
                    chunk.embedding = embedding
                    embeddings_generated += 1
            finally:
                loop.close()

        # Mark as completed
        document.processing_status = "completed"
        db.commit()

        return {
            "document_id": document_id,
            "status": "completed",
            "chunks_created": len(result["chunks"]),
            "embeddings_generated": embeddings_generated,
            "word_count": result["word_count"],
            "page_count": result["page_count"],
        }

    except Exception as e:
        db.rollback()

        # Update document with error
        document = db.query(Document).filter(Document.id == document_id).first()
        if document:
            document.processing_status = "failed"
            document.processing_error = str(e)
            db.commit()

        # Retry with exponential backoff
        raise self.retry(exc=e, countdown=60 * (2 ** self.request.retries))

    finally:
        db.close()

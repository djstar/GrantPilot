"""
Document Processing Celery Tasks
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.celery_app import celery_app
from app.config import get_settings
from app.db.models import Document, DocumentChunk
from app.processors.document_processor import process_document

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
        for chunk_data in result["chunks"]:
            chunk = DocumentChunk(
                document_id=document_id,
                chunk_index=chunk_data["index"],
                content=chunk_data["text"],
                start_char=chunk_data["start_char"],
                end_char=chunk_data["end_char"],
                word_count=chunk_data["word_count"],
                # embedding will be added later by embedding task
            )
            db.add(chunk)

        # Mark as completed
        document.processing_status = "completed"
        db.commit()

        return {
            "document_id": document_id,
            "status": "completed",
            "chunks_created": len(result["chunks"]),
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

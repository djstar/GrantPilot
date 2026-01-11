"""
Documents API endpoints
Based on Section 8: API Contracts
"""

import os
import uuid
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from app.db.database import get_db
from app.db.models import Document, DocumentType, ProcessingStatus
from app.config import get_settings

router = APIRouter()
settings = get_settings()


# Pydantic schemas
class DocumentResponse(BaseModel):
    id: UUID
    project_id: Optional[UUID]
    filename: str
    original_filename: str
    file_size: int
    mime_type: str
    document_type: DocumentType
    document_type_confidence: Optional[float]
    processing_status: ProcessingStatus
    processing_error: Optional[str]
    page_count: Optional[int]
    word_count: Optional[int]
    version: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    items: List[DocumentResponse]
    total: int


# Allowed file types
ALLOWED_EXTENSIONS = {
    ".pdf": "application/pdf",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".doc": "application/msword",
    ".txt": "text/plain",
}


def validate_file(file: UploadFile) -> tuple[str, str]:
    """Validate uploaded file and return extension and mime type"""
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Filename is required"
        )

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {ext} not allowed. Allowed: {list(ALLOWED_EXTENSIONS.keys())}",
        )

    return ext, ALLOWED_EXTENSIONS[ext]


@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    project_id: Optional[UUID] = Form(None),
    document_type: DocumentType = Form(DocumentType.OTHER),
    db: AsyncSession = Depends(get_db),
):
    """Upload a new document"""
    # Validate file
    ext, mime_type = validate_file(file)

    # Generate unique filename
    unique_id = uuid.uuid4()
    filename = f"{unique_id}{ext}"
    file_path = os.path.join(settings.upload_dir, filename)

    # Ensure upload directory exists
    os.makedirs(settings.upload_dir, exist_ok=True)

    # Save file
    try:
        content = await file.read()
        file_size = len(content)

        # Check file size
        max_size = settings.max_upload_size_mb * 1024 * 1024
        if file_size > max_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File too large. Max size: {settings.max_upload_size_mb}MB",
            )

        with open(file_path, "wb") as f:
            f.write(content)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}",
        )

    # Create document record
    document = Document(
        project_id=project_id,
        filename=filename,
        original_filename=file.filename,
        file_path=file_path,
        file_size=file_size,
        mime_type=mime_type,
        document_type=document_type,
        processing_status=ProcessingStatus.PENDING,
    )

    db.add(document)
    await db.flush()
    await db.refresh(document)

    # TODO: Trigger async processing task
    # celery_app.send_task("process_document", args=[str(document.id)])

    return DocumentResponse.model_validate(document)


@router.get("", response_model=DocumentListResponse)
async def list_documents(
    project_id: Optional[UUID] = None,
    document_type: Optional[DocumentType] = None,
    db: AsyncSession = Depends(get_db),
):
    """List documents with optional filtering"""
    query = select(Document)

    if project_id:
        query = query.where(Document.project_id == project_id)
    if document_type:
        query = query.where(Document.document_type == document_type)

    query = query.order_by(Document.created_at.desc())

    result = await db.execute(query)
    documents = result.scalars().all()

    return DocumentListResponse(
        items=[DocumentResponse.model_validate(d) for d in documents],
        total=len(documents),
    )


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get a specific document by ID"""
    result = await db.execute(select(Document).where(Document.id == document_id))
    document = result.scalar_one_or_none()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
        )

    return DocumentResponse.model_validate(document)


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Delete a document"""
    result = await db.execute(select(Document).where(Document.id == document_id))
    document = result.scalar_one_or_none()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
        )

    # Delete file from disk
    try:
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
    except Exception:
        pass  # Log but don't fail

    await db.delete(document)
    return None


@router.get("/{document_id}/content")
async def get_document_content(
    document_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get extracted text content of a document"""
    result = await db.execute(select(Document).where(Document.id == document_id))
    document = result.scalar_one_or_none()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
        )

    if document.processing_status != ProcessingStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Document processing status: {document.processing_status.value}",
        )

    return {
        "id": document.id,
        "content": document.extracted_text,
        "page_count": document.page_count,
        "word_count": document.word_count,
    }

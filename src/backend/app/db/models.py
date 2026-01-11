"""
SQLAlchemy Models for GrantPilot
Based on Section 7: Database Schema from specification
"""

import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import (
    String,
    Text,
    Integer,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    JSON,
    Enum as SQLEnum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from pgvector.sqlalchemy import Vector

from app.db.database import Base


# Enums
import enum


class ProjectStatus(str, enum.Enum):
    PLANNING = "planning"
    DRAFTING = "drafting"
    SUBMITTED = "submitted"
    SCORED = "scored"
    FUNDED = "funded"
    NOT_FUNDED = "not_funded"
    ARCHIVED = "archived"


class DocumentType(str, enum.Enum):
    SPECIFIC_AIMS = "specific_aims"
    SIGNIFICANCE = "significance"
    INNOVATION = "innovation"
    APPROACH = "approach"
    BIOSKETCH = "biosketch"
    BUDGET = "budget"
    BUDGET_JUSTIFICATION = "budget_justification"
    FACILITIES = "facilities"
    LETTER_OF_SUPPORT = "letter_of_support"
    RFA = "rfa"
    MANUSCRIPT = "manuscript"
    REVIEW_FEEDBACK = "review_feedback"
    RESEARCH_NOTE = "research_note"
    OTHER = "other"


class ProcessingStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


# Models


class Project(Base):
    """Grant project"""

    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    grant_type: Mapped[Optional[str]] = mapped_column(String(50))  # R01, R21, K99, etc.
    funder: Mapped[Optional[str]] = mapped_column(String(100))  # NIH, NSF, DOD, etc.
    status: Mapped[ProjectStatus] = mapped_column(
        SQLEnum(ProjectStatus), default=ProjectStatus.PLANNING
    )
    deadline: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    budget_limit: Mapped[Optional[float]] = mapped_column(Float)
    budget_used: Mapped[float] = mapped_column(Float, default=0.0)

    # RFA reference
    rfa_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("rfas.id"), nullable=True
    )

    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    documents: Mapped[List["Document"]] = relationship(
        "Document", back_populates="project", cascade="all, delete-orphan"
    )
    rfa: Mapped[Optional["RFA"]] = relationship("RFA", back_populates="projects")


class Document(Base):
    """Uploaded document"""

    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    project_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id"), nullable=True
    )
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer)
    mime_type: Mapped[str] = mapped_column(String(100))
    document_type: Mapped[DocumentType] = mapped_column(
        SQLEnum(DocumentType), default=DocumentType.OTHER
    )
    document_type_confidence: Mapped[Optional[float]] = mapped_column(Float)

    # Processing status
    processing_status: Mapped[ProcessingStatus] = mapped_column(
        SQLEnum(ProcessingStatus), default=ProcessingStatus.PENDING
    )
    processing_error: Mapped[Optional[str]] = mapped_column(Text)

    # Extracted content
    extracted_text: Mapped[Optional[str]] = mapped_column(Text)
    page_count: Mapped[Optional[int]] = mapped_column(Integer)
    word_count: Mapped[Optional[int]] = mapped_column(Integer)
    metadata_json: Mapped[Optional[dict]] = mapped_column(JSON)

    # Version tracking
    version: Mapped[int] = mapped_column(Integer, default=1)
    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documents.id"), nullable=True
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    project: Mapped[Optional["Project"]] = relationship(
        "Project", back_populates="documents"
    )
    chunks: Mapped[List["DocumentChunk"]] = relationship(
        "DocumentChunk", back_populates="document", cascade="all, delete-orphan"
    )


class DocumentChunk(Base):
    """Document chunk for RAG"""

    __tablename__ = "document_chunks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False
    )
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    start_char: Mapped[Optional[int]] = mapped_column(Integer)
    end_char: Mapped[Optional[int]] = mapped_column(Integer)
    word_count: Mapped[Optional[int]] = mapped_column(Integer)
    token_count: Mapped[Optional[int]] = mapped_column(Integer)

    # Vector embeddings (768-dim for PubMedBERT, 1536 for OpenAI)
    embedding: Mapped[Optional[List[float]]] = mapped_column(Vector(768))

    # Metadata
    page_number: Mapped[Optional[int]] = mapped_column(Integer)
    section: Mapped[Optional[str]] = mapped_column(String(100))
    metadata_json: Mapped[Optional[dict]] = mapped_column(JSON)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )

    # Relationships
    document: Mapped["Document"] = relationship("Document", back_populates="chunks")


class RFA(Base):
    """Request for Applications"""

    __tablename__ = "rfas"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    rfa_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    funder: Mapped[str] = mapped_column(String(100))
    mechanism: Mapped[Optional[str]] = mapped_column(String(50))  # R01, R21, etc.
    deadline: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    url: Mapped[Optional[str]] = mapped_column(String(500))

    # Parsed content
    full_text: Mapped[Optional[str]] = mapped_column(Text)
    requirements_json: Mapped[Optional[dict]] = mapped_column(JSON)
    priorities_json: Mapped[Optional[dict]] = mapped_column(JSON)

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    projects: Mapped[List["Project"]] = relationship("Project", back_populates="rfa")

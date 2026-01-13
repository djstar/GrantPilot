"""
Vector Search Service
Semantic search over document chunks using pgvector
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.embeddings import get_embedding_service


class SearchResult:
    """Search result with chunk content and metadata"""

    def __init__(
        self,
        chunk_id: UUID,
        document_id: UUID,
        content: str,
        score: float,
        chunk_index: int,
        document_filename: Optional[str] = None,
    ):
        self.chunk_id = chunk_id
        self.document_id = document_id
        self.content = content
        self.score = score
        self.chunk_index = chunk_index
        self.document_filename = document_filename

    def to_dict(self):
        return {
            "chunk_id": str(self.chunk_id),
            "document_id": str(self.document_id),
            "content": self.content,
            "score": self.score,
            "chunk_index": self.chunk_index,
            "document_filename": self.document_filename,
        }


class SearchService:
    """Semantic search over document chunks"""

    def __init__(self, db: Optional[AsyncSession] = None):
        self.db = db
        self.embedding_service = get_embedding_service()

    async def search(
        self,
        query: str,
        project_id: Optional[UUID] = None,
        document_ids: Optional[List[UUID]] = None,
        limit: int = 5,
        min_score: float = 0.0,
        db: Optional[AsyncSession] = None,
    ) -> List[SearchResult]:
        """
        Search for relevant chunks using semantic similarity.

        Args:
            query: Search query text
            project_id: Optional filter by project
            document_ids: Optional filter by specific documents
            limit: Max number of results
            min_score: Minimum similarity score (0-1)

        Returns:
            List of SearchResult objects sorted by relevance
        """
        if not self.embedding_service.is_available():
            return []

        # Generate query embedding
        query_embedding = await self.embedding_service.embed_text(query)

        # Build the SQL query with vector similarity
        # Using cosine distance: 1 - (embedding <=> query_embedding)
        sql = """
            SELECT
                dc.id as chunk_id,
                dc.document_id,
                dc.content,
                dc.chunk_index,
                d.original_filename,
                1 - (dc.embedding <=> :query_embedding::vector) as score
            FROM document_chunks dc
            JOIN documents d ON d.id = dc.document_id
            WHERE dc.embedding IS NOT NULL
        """

        params = {"query_embedding": str(query_embedding), "limit": limit}

        # Add filters
        if project_id:
            sql += " AND d.project_id = :project_id"
            params["project_id"] = str(project_id)

        if document_ids:
            sql += " AND dc.document_id = ANY(:document_ids)"
            params["document_ids"] = [str(did) for did in document_ids]

        if min_score > 0:
            sql += " AND 1 - (dc.embedding <=> :query_embedding::vector) >= :min_score"
            params["min_score"] = min_score

        sql += " ORDER BY dc.embedding <=> :query_embedding::vector LIMIT :limit"

        # Use provided db or fall back to instance db
        session = db or self.db
        if not session:
            return []

        result = await session.execute(text(sql), params)
        rows = result.fetchall()

        return [
            SearchResult(
                chunk_id=row.chunk_id,
                document_id=row.document_id,
                content=row.content,
                score=float(row.score),
                chunk_index=row.chunk_index,
                document_filename=row.original_filename,
            )
            for row in rows
        ]

    async def get_context_for_query(
        self,
        query: str,
        project_id: Optional[UUID] = None,
        max_tokens: int = 4000,
        limit: int = 10,
    ) -> str:
        """
        Get relevant context for a query, formatted for LLM consumption.

        Args:
            query: User's question
            project_id: Optional project filter
            max_tokens: Approximate max tokens for context
            limit: Max chunks to retrieve

        Returns:
            Formatted context string
        """
        results = await self.search(query, project_id=project_id, limit=limit)

        if not results:
            return ""

        context_parts = []
        total_chars = 0
        char_limit = max_tokens * 4  # Rough estimate: 4 chars per token

        for result in results:
            if total_chars + len(result.content) > char_limit:
                break

            source_info = f"[Source: {result.document_filename}, chunk {result.chunk_index + 1}]"
            context_parts.append(f"{source_info}\n{result.content}")
            total_chars += len(result.content)

        return "\n\n---\n\n".join(context_parts)

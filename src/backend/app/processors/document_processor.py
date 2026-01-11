"""
Document Processing Service
Extracts text from PDF, DOCX, DOC, and TXT files
"""

import os
from pathlib import Path
from typing import Optional
import magic

from pypdf import PdfReader
from docx import Document as DocxDocument


class DocumentProcessor:
    """Extracts text content from various document formats"""

    SUPPORTED_TYPES = {
        "application/pdf": "pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
        "application/msword": "doc",
        "text/plain": "txt",
    }

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.mime_type = self._detect_mime_type()

    def _detect_mime_type(self) -> str:
        """Detect file MIME type using libmagic"""
        mime = magic.Magic(mime=True)
        return mime.from_file(str(self.file_path))

    def extract_text(self) -> str:
        """Extract text based on file type"""
        file_type = self.SUPPORTED_TYPES.get(self.mime_type)

        if file_type == "pdf":
            return self._extract_pdf()
        elif file_type == "docx":
            return self._extract_docx()
        elif file_type == "doc":
            return self._extract_doc()
        elif file_type == "txt":
            return self._extract_txt()
        else:
            raise ValueError(f"Unsupported file type: {self.mime_type}")

    def _extract_pdf(self) -> str:
        """Extract text from PDF"""
        reader = PdfReader(str(self.file_path))
        text_parts = []

        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)

        return "\n\n".join(text_parts)

    def _extract_docx(self) -> str:
        """Extract text from DOCX"""
        doc = DocxDocument(str(self.file_path))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n\n".join(paragraphs)

    def _extract_doc(self) -> str:
        """Extract text from legacy DOC format"""
        # For now, treat as plain text - would need antiword or similar for full support
        # Most modern DOC files are actually DOCX
        try:
            return self._extract_docx()
        except Exception:
            return self._extract_txt()

    def _extract_txt(self) -> str:
        """Extract text from plain text file"""
        with open(self.file_path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()

    def get_page_count(self) -> Optional[int]:
        """Get page count for PDF files"""
        if self.SUPPORTED_TYPES.get(self.mime_type) == "pdf":
            reader = PdfReader(str(self.file_path))
            return len(reader.pages)
        return None

    def get_word_count(self, text: str) -> int:
        """Count words in extracted text"""
        return len(text.split())


class TextChunker:
    """Splits text into chunks for embedding and retrieval"""

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        separators: list[str] = None,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", ". ", " "]

    def split(self, text: str) -> list[dict]:
        """Split text into overlapping chunks with metadata"""
        chunks = []
        current_pos = 0
        chunk_index = 0

        while current_pos < len(text):
            # Find the end of this chunk
            end_pos = min(current_pos + self.chunk_size, len(text))

            # Try to break at a natural boundary
            if end_pos < len(text):
                for sep in self.separators:
                    # Look for separator near the end of chunk
                    search_start = max(current_pos + self.chunk_size - 100, current_pos)
                    sep_pos = text.rfind(sep, search_start, end_pos + 50)
                    if sep_pos > current_pos:
                        end_pos = sep_pos + len(sep)
                        break

            chunk_text = text[current_pos:end_pos].strip()

            if chunk_text:
                chunks.append({
                    "index": chunk_index,
                    "text": chunk_text,
                    "start_char": current_pos,
                    "end_char": end_pos,
                    "word_count": len(chunk_text.split()),
                })
                chunk_index += 1

            # Move position with overlap
            current_pos = end_pos - self.chunk_overlap
            if current_pos <= chunks[-1]["start_char"] if chunks else 0:
                current_pos = end_pos  # Prevent infinite loop

        return chunks


def process_document(file_path: str) -> dict:
    """
    Process a document file and return extracted data.

    Returns:
        dict with keys: text, chunks, page_count, word_count, mime_type
    """
    processor = DocumentProcessor(file_path)
    text = processor.extract_text()
    page_count = processor.get_page_count()
    word_count = processor.get_word_count(text)

    chunker = TextChunker()
    chunks = chunker.split(text)

    return {
        "text": text,
        "chunks": chunks,
        "page_count": page_count,
        "word_count": word_count,
        "mime_type": processor.mime_type,
        "chunk_count": len(chunks),
    }

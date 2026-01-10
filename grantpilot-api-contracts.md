# GrantPilot API Contracts

**Version:** 1.0  
**Last Updated:** January 2025  
**Base URL:** `http://localhost:8000/api/v1`

---

## Table of Contents

1. [Overview](#1-overview)
2. [Authentication](#2-authentication)
3. [Common Patterns](#3-common-patterns)
4. [Projects API](#4-projects-api)
5. [Documents API](#5-documents-api)
6. [RFAs API](#6-rfas-api)
7. [Agents API](#7-agents-api)
8. [Chat API](#8-chat-api)
9. [Knowledge Base API](#9-knowledge-base-api)
10. [References API](#10-references-api)
11. [Settings API](#11-settings-api)
12. [WebSocket Events](#12-websocket-events)
13. [Error Codes Reference](#13-error-codes-reference)

---

## 1. Overview

### 1.1 API Design Principles

- **RESTful:** Resources are nouns, HTTP methods are verbs
- **JSON:** All request/response bodies are JSON
- **Consistent:** Uniform response structure across all endpoints
- **Paginated:** List endpoints support pagination
- **Filterable:** List endpoints support query filters
- **Real-time:** WebSocket for streaming and live updates

### 1.2 Base Response Structure

All API responses follow this structure:

```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "timestamp": "2025-01-10T14:30:00Z",
    "request_id": "req_abc123"
  }
}
```

Error responses:

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable error message",
    "details": { ... }
  },
  "meta": {
    "timestamp": "2025-01-10T14:30:00Z",
    "request_id": "req_abc123"
  }
}
```

### 1.3 HTTP Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful GET, PUT |
| 201 | Created | Successful POST creating resource |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation error, malformed request |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Authenticated but not authorized |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Resource conflict (e.g., duplicate) |
| 422 | Unprocessable Entity | Semantic validation error |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server-side error |
| 503 | Service Unavailable | LLM API unavailable |

---

## 2. Authentication

### 2.1 Approach

Since GrantPilot is a **single-user local application**, authentication is simplified:

- **Local mode:** No authentication required (default)
- **Optional PIN:** User can enable a PIN lock for privacy
- **API keys:** Stored securely for LLM providers (not exposed via API)

### 2.2 Optional PIN Authentication

If PIN is enabled:

**Request Header:**
```
X-GrantPilot-PIN: 1234
```

**Endpoints:**

```
POST /api/v1/auth/verify-pin
```

**Request:**
```json
{
  "pin": "1234"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "verified": true,
    "session_token": "session_xyz789",
    "expires_at": "2025-01-10T18:30:00Z"
  }
}
```

---

## 3. Common Patterns

### 3.1 Pagination

List endpoints support cursor-based pagination:

**Query Parameters:**
- `limit` (integer, default: 20, max: 100) — Items per page
- `cursor` (string, optional) — Cursor for next page
- `sort` (string, optional) — Sort field (prefix with `-` for descending)

**Response includes pagination meta:**
```json
{
  "success": true,
  "data": [ ... ],
  "meta": {
    "pagination": {
      "total": 156,
      "limit": 20,
      "has_more": true,
      "next_cursor": "cursor_abc123",
      "prev_cursor": null
    }
  }
}
```

### 3.2 Filtering

List endpoints support filtering via query parameters:

```
GET /api/v1/projects?status=draft&grant_type=R01
GET /api/v1/documents?document_type=manuscript&project_id=uuid
```

### 3.3 Field Selection

Request specific fields to reduce payload:

```
GET /api/v1/projects?fields=id,name,status,deadline
```

### 3.4 Timestamps

All timestamps are ISO 8601 format in UTC:
```
2025-01-10T14:30:00Z
```

### 3.5 UUIDs

All resource IDs are UUIDs:
```
550e8400-e29b-41d4-a716-446655440000
```

---

## 4. Projects API

### 4.1 List Projects

```
GET /api/v1/projects
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| status | string | Filter by status: draft, in_progress, submitted, funded, not_funded, archived |
| grant_type | string | Filter by grant type: R01, R21, K99, etc. |
| funder | string | Filter by funder |
| search | string | Search in name and description |
| limit | integer | Items per page (default: 20) |
| cursor | string | Pagination cursor |
| sort | string | Sort field: name, created_at, deadline, -updated_at |

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "R01 Cancer Immunotherapy",
      "description": "CAR-T therapy for solid tumors",
      "status": "in_progress",
      "grant_type": "R01",
      "funder": "NIH-NCI",
      "mechanism": "R01",
      "rfa_id": "660e8400-e29b-41d4-a716-446655440001",
      "rfa_number": "RFA-CA-24-001",
      "budget_total": 2500000.00,
      "budget_per_year": 500000.00,
      "deadline": "2025-03-05T17:00:00Z",
      "internal_deadline": "2025-02-28T17:00:00Z",
      "token_budget": 500000,
      "tokens_used": 125000,
      "cost_budget": 25.00,
      "cost_used": 6.25,
      "sections_count": 6,
      "compliance_score": 78,
      "created_at": "2025-01-01T10:00:00Z",
      "updated_at": "2025-01-10T14:30:00Z"
    }
  ],
  "meta": {
    "pagination": {
      "total": 12,
      "limit": 20,
      "has_more": false,
      "next_cursor": null
    }
  }
}
```

---

### 4.2 Create Project

```
POST /api/v1/projects
```

**Request:**
```json
{
  "name": "R01 Cancer Immunotherapy",
  "description": "CAR-T therapy for solid tumors",
  "grant_type": "R01",
  "funder": "NIH-NCI",
  "mechanism": "R01",
  "rfa_id": "660e8400-e29b-41d4-a716-446655440001",
  "budget_total": 2500000.00,
  "budget_per_year": 500000.00,
  "deadline": "2025-03-05T17:00:00Z",
  "internal_deadline": "2025-02-28T17:00:00Z",
  "token_budget": 500000,
  "cost_budget": 25.00
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "R01 Cancer Immunotherapy",
    "status": "draft",
    ...
  }
}
```

---

### 4.3 Get Project

```
GET /api/v1/projects/{project_id}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "R01 Cancer Immunotherapy",
    "description": "CAR-T therapy for solid tumors",
    "status": "in_progress",
    "grant_type": "R01",
    "funder": "NIH-NCI",
    "mechanism": "R01",
    "rfa": {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "title": "Immunotherapy Approaches for Cancer",
      "rfa_number": "RFA-CA-24-001",
      "deadline": "2025-03-05T17:00:00Z"
    },
    "budget_total": 2500000.00,
    "budget_per_year": 500000.00,
    "deadline": "2025-03-05T17:00:00Z",
    "internal_deadline": "2025-02-28T17:00:00Z",
    "token_budget": 500000,
    "tokens_used": 125000,
    "cost_budget": 25.00,
    "cost_used": 6.25,
    "sections": [
      {
        "id": "770e8400-e29b-41d4-a716-446655440002",
        "section_type": "specific_aims",
        "title": "Specific Aims",
        "version": 3,
        "word_count": 487,
        "page_count": 0.95,
        "is_compliant": true,
        "updated_at": "2025-01-10T12:00:00Z"
      }
    ],
    "documents_count": 15,
    "submissions": [],
    "compliance_score": 78,
    "compliance_issues": [
      {
        "section": "innovation",
        "issue": "Only 2 of 3 required points addressed",
        "severity": "warning"
      }
    ],
    "created_at": "2025-01-01T10:00:00Z",
    "updated_at": "2025-01-10T14:30:00Z"
  }
}
```

---

### 4.4 Update Project

```
PUT /api/v1/projects/{project_id}
```

**Request:**
```json
{
  "name": "R01 Cancer Immunotherapy - Updated",
  "status": "in_progress",
  "deadline": "2025-03-10T17:00:00Z",
  "cost_budget": 30.00
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "R01 Cancer Immunotherapy - Updated",
    ...
  }
}
```

---

### 4.5 Delete Project

```
DELETE /api/v1/projects/{project_id}
```

**Query Parameters:**
- `permanent` (boolean, default: false) — If true, permanently delete; otherwise archive

**Response (204 No Content):**
```
(empty body)
```

---

### 4.6 Get Project Sections

```
GET /api/v1/projects/{project_id}/sections
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "770e8400-e29b-41d4-a716-446655440002",
      "project_id": "550e8400-e29b-41d4-a716-446655440000",
      "section_type": "specific_aims",
      "title": "Specific Aims",
      "content": "The long-term goal of this research...",
      "version": 3,
      "word_count": 487,
      "page_count": 0.95,
      "word_limit": null,
      "page_limit": 1.0,
      "is_compliant": true,
      "ai_suggestions": [
        {
          "type": "enhancement",
          "text": "Consider adding preliminary data reference",
          "location": { "start": 245, "end": 312 }
        }
      ],
      "compliance_issues": [],
      "created_at": "2025-01-02T10:00:00Z",
      "updated_at": "2025-01-10T12:00:00Z"
    }
  ]
}
```

---

### 4.7 Create Project Section

```
POST /api/v1/projects/{project_id}/sections
```

**Request:**
```json
{
  "section_type": "significance",
  "title": "Significance",
  "content": "Cancer remains a leading cause of death...",
  "word_limit": null,
  "page_limit": null
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "id": "880e8400-e29b-41d4-a716-446655440003",
    "section_type": "significance",
    "title": "Significance",
    "content": "Cancer remains a leading cause of death...",
    "version": 1,
    "word_count": 156,
    "page_count": 0.31,
    ...
  }
}
```

---

### 4.8 Update Project Section

```
PUT /api/v1/projects/{project_id}/sections/{section_id}
```

**Request:**
```json
{
  "content": "Updated content here...",
  "title": "Significance and Impact"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "880e8400-e29b-41d4-a716-446655440003",
    "version": 2,
    "content": "Updated content here...",
    ...
  }
}
```

---

### 4.9 Get Section Version History

```
GET /api/v1/projects/{project_id}/sections/{section_id}/versions
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "990e8400-e29b-41d4-a716-446655440004",
      "section_id": "880e8400-e29b-41d4-a716-446655440003",
      "version": 2,
      "content": "Updated content here...",
      "change_summary": "Expanded impact statement",
      "created_at": "2025-01-10T14:00:00Z"
    },
    {
      "id": "990e8400-e29b-41d4-a716-446655440005",
      "section_id": "880e8400-e29b-41d4-a716-446655440003",
      "version": 1,
      "content": "Original content...",
      "change_summary": null,
      "created_at": "2025-01-08T10:00:00Z"
    }
  ]
}
```

---

### 4.10 Export Project

```
POST /api/v1/projects/{project_id}/export
```

**Request:**
```json
{
  "format": "docx",
  "sections": ["specific_aims", "significance", "innovation", "approach"],
  "include_comments": false,
  "template": "nih_standard"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "export_id": "exp_abc123",
    "status": "processing",
    "download_url": null,
    "expires_at": null
  }
}
```

After processing (via WebSocket or polling):
```json
{
  "success": true,
  "data": {
    "export_id": "exp_abc123",
    "status": "completed",
    "download_url": "/api/v1/exports/exp_abc123/download",
    "expires_at": "2025-01-10T18:30:00Z"
  }
}
```

---

### 4.11 Get Project Compliance Report

```
GET /api/v1/projects/{project_id}/compliance
```

**Response:**
```json
{
  "success": true,
  "data": {
    "project_id": "550e8400-e29b-41d4-a716-446655440000",
    "overall_score": 78,
    "status": "needs_attention",
    "rfa_id": "660e8400-e29b-41d4-a716-446655440001",
    "checked_at": "2025-01-10T14:30:00Z",
    "sections": [
      {
        "section_type": "specific_aims",
        "status": "pass",
        "checks": [
          { "rule": "page_limit", "status": "pass", "requirement": "1 page", "actual": "0.95 pages" }
        ]
      },
      {
        "section_type": "innovation",
        "status": "warning",
        "checks": [
          { "rule": "content_points", "status": "warning", "requirement": "Address 3 points", "actual": "2 points found" }
        ]
      }
    ],
    "missing_items": [
      { "item": "timeline", "required": true },
      { "item": "letters_of_support", "required": true, "count_required": 2, "count_found": 0 }
    ],
    "rfa_priorities": [
      { "keyword": "health disparities", "rfa_mentions": 12, "your_mentions": 2, "recommendation": "Consider expanding" }
    ],
    "format_issues": [
      { "document": "biosketch_pi.pdf", "issue": "Exceeds 5 page limit", "severity": "warning" }
    ]
  }
}
```

---

## 5. Documents API

### 5.1 List Documents

```
GET /api/v1/documents
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| project_id | uuid | Filter by project |
| document_type | string | Filter by type: manuscript, grant_draft, rfa, biosketch, figure, review, letter |
| processing_status | string | Filter by status: pending, processing, completed, failed |
| source | string | Filter by source: upload, folder_watch, web_download |
| search | string | Full-text search in content |
| limit | integer | Items per page |
| cursor | string | Pagination cursor |

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "doc_550e8400-e29b-41d4-a716-446655440000",
      "filename": "CAR-T_manuscript_2024.pdf",
      "file_path": "/Dropbox/Papers/CAR-T_manuscript_2024.pdf",
      "file_type": "pdf",
      "file_size": 2456789,
      "document_type": "manuscript",
      "document_subtype": null,
      "processing_status": "completed",
      "processed_at": "2025-01-08T12:00:00Z",
      "project_id": null,
      "source": "folder_watch",
      "extracted_metadata": {
        "title": "CAR-T Cell Therapy for Solid Tumors",
        "authors": ["Smith, J.", "Johnson, A."],
        "date": "2024-06-15"
      },
      "chunks_count": 45,
      "created_at": "2025-01-08T11:00:00Z",
      "updated_at": "2025-01-08T12:00:00Z"
    }
  ],
  "meta": {
    "pagination": { ... }
  }
}
```

---

### 5.2 Upload Document

```
POST /api/v1/documents/upload
Content-Type: multipart/form-data
```

**Form Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| file | file | Yes | The file to upload |
| project_id | uuid | No | Associate with project |
| document_type | string | No | Override auto-classification |
| process_immediately | boolean | No | Start processing right away (default: true) |

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "id": "doc_660e8400-e29b-41d4-a716-446655440001",
    "filename": "uploaded_document.pdf",
    "file_type": "pdf",
    "file_size": 1234567,
    "document_type": "manuscript",
    "processing_status": "processing",
    "upload_url": null,
    "created_at": "2025-01-10T14:30:00Z"
  }
}
```

---

### 5.3 Get Document

```
GET /api/v1/documents/{document_id}
```

**Query Parameters:**
- `include_text` (boolean, default: false) — Include full extracted text
- `include_chunks` (boolean, default: false) — Include document chunks

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "doc_550e8400-e29b-41d4-a716-446655440000",
    "filename": "CAR-T_manuscript_2024.pdf",
    "file_path": "/Dropbox/Papers/CAR-T_manuscript_2024.pdf",
    "file_type": "pdf",
    "file_size": 2456789,
    "file_hash": "sha256_abc123...",
    "document_type": "manuscript",
    "document_subtype": null,
    "processing_status": "completed",
    "processed_at": "2025-01-08T12:00:00Z",
    "project_id": null,
    "source": "folder_watch",
    "source_url": null,
    "extracted_text": "Full text here if include_text=true...",
    "extracted_metadata": {
      "title": "CAR-T Cell Therapy for Solid Tumors",
      "authors": ["Smith, J.", "Johnson, A."],
      "date": "2024-06-15",
      "pages": 12,
      "figures": 5,
      "tables": 3
    },
    "image_description": null,
    "chunks": [
      {
        "id": "chunk_001",
        "chunk_index": 0,
        "chunk_text": "Abstract: CAR-T cell therapy...",
        "chunk_metadata": { "page": 1, "section": "abstract" }
      }
    ],
    "created_at": "2025-01-08T11:00:00Z",
    "updated_at": "2025-01-08T12:00:00Z"
  }
}
```

---

### 5.4 Update Document

```
PUT /api/v1/documents/{document_id}
```

**Request:**
```json
{
  "document_type": "grant_draft",
  "document_subtype": "specific_aims",
  "project_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "doc_550e8400-e29b-41d4-a716-446655440000",
    "document_type": "grant_draft",
    "document_subtype": "specific_aims",
    "project_id": "550e8400-e29b-41d4-a716-446655440000",
    ...
  }
}
```

---

### 5.5 Delete Document

```
DELETE /api/v1/documents/{document_id}
```

**Query Parameters:**
- `delete_file` (boolean, default: false) — Also delete the physical file

**Response (204 No Content)**

---

### 5.6 Reprocess Document

```
POST /api/v1/documents/{document_id}/process
```

**Request:**
```json
{
  "force": true,
  "extract_images": true,
  "ocr": false
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "doc_550e8400-e29b-41d4-a716-446655440000",
    "processing_status": "processing",
    "task_id": "task_abc123"
  }
}
```

---

### 5.7 Get Document Preview

```
GET /api/v1/documents/{document_id}/preview
```

**Query Parameters:**
- `page` (integer, default: 1) — Page number for PDFs
- `format` (string, default: "png") — Output format: png, jpg
- `width` (integer, optional) — Max width in pixels

**Response:**
```
Content-Type: image/png
(binary image data)
```

---

### 5.8 Bulk Document Operations

```
POST /api/v1/documents/bulk
```

**Request:**
```json
{
  "operation": "assign_project",
  "document_ids": [
    "doc_550e8400-e29b-41d4-a716-446655440000",
    "doc_660e8400-e29b-41d4-a716-446655440001"
  ],
  "params": {
    "project_id": "proj_123"
  }
}
```

**Operations:**
- `assign_project` — Assign documents to a project
- `set_type` — Set document type
- `reprocess` — Reprocess multiple documents
- `delete` — Delete multiple documents

**Response:**
```json
{
  "success": true,
  "data": {
    "processed": 2,
    "failed": 0,
    "results": [
      { "id": "doc_550e8400...", "status": "success" },
      { "id": "doc_660e8400...", "status": "success" }
    ]
  }
}
```

---

## 6. RFAs API

### 6.1 List RFAs

```
GET /api/v1/rfas
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| status | string | Filter: active, expired, archived |
| funder | string | Filter by funder |
| mechanism | string | Filter by mechanism: R01, R21, etc. |
| deadline_before | datetime | RFAs with deadline before date |
| deadline_after | datetime | RFAs with deadline after date |
| search | string | Search in title and content |

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "rfa_550e8400-e29b-41d4-a716-446655440000",
      "title": "Immunotherapy Approaches for Cancer",
      "funder": "NIH-NCI",
      "mechanism": "R01",
      "rfa_number": "RFA-CA-24-001",
      "source_url": "https://grants.nih.gov/grants/guide/rfa-files/RFA-CA-24-001.html",
      "release_date": "2024-10-15",
      "deadline": "2025-03-05T17:00:00Z",
      "letter_of_intent_date": "2025-02-05",
      "budget_cap_yearly": 500000.00,
      "status": "active",
      "days_until_deadline": 54,
      "projects_count": 2,
      "created_at": "2024-11-01T10:00:00Z"
    }
  ]
}
```

---

### 6.2 Create RFA

```
POST /api/v1/rfas
```

**Request:**
```json
{
  "title": "Immunotherapy Approaches for Cancer",
  "funder": "NIH-NCI",
  "mechanism": "R01",
  "rfa_number": "RFA-CA-24-001",
  "source_url": "https://grants.nih.gov/grants/guide/rfa-files/RFA-CA-24-001.html",
  "deadline": "2025-03-05T17:00:00Z",
  "letter_of_intent_date": "2025-02-05",
  "budget_cap_yearly": 500000.00,
  "full_text": "Optional: paste full RFA text here..."
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "id": "rfa_550e8400-e29b-41d4-a716-446655440000",
    "title": "Immunotherapy Approaches for Cancer",
    "parsing_status": "pending",
    ...
  }
}
```

---

### 6.3 Create RFA from URL

```
POST /api/v1/rfas/from-url
```

**Request:**
```json
{
  "url": "https://grants.nih.gov/grants/guide/rfa-files/RFA-CA-24-001.html"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "id": "rfa_550e8400-e29b-41d4-a716-446655440000",
    "title": "Immunotherapy Approaches for Cancer",
    "parsing_status": "processing",
    "task_id": "task_abc123"
  }
}
```

---

### 6.4 Create RFA from Document

```
POST /api/v1/rfas/from-document
```

**Request:**
```json
{
  "document_id": "doc_550e8400-e29b-41d4-a716-446655440000"
}
```

---

### 6.5 Get RFA

```
GET /api/v1/rfas/{rfa_id}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "rfa_550e8400-e29b-41d4-a716-446655440000",
    "title": "Immunotherapy Approaches for Cancer",
    "funder": "NIH-NCI",
    "mechanism": "R01",
    "rfa_number": "RFA-CA-24-001",
    "source_url": "https://grants.nih.gov/...",
    "release_date": "2024-10-15",
    "deadline": "2025-03-05T17:00:00Z",
    "letter_of_intent_date": "2025-02-05",
    "full_text": "Full RFA text...",
    "budget_cap_total": null,
    "budget_cap_yearly": 500000.00,
    "parsed_requirements": {
      "page_limits": {
        "specific_aims": 1,
        "research_strategy": 12
      },
      "required_sections": ["specific_aims", "significance", "innovation", "approach"],
      "required_attachments": ["biosketch", "budget", "facilities"],
      "eligibility": { ... }
    },
    "parsed_priorities": [
      { "keyword": "health disparities", "mentions": 12, "priority": "high" },
      { "keyword": "preliminary data", "mentions": 8, "priority": "high" },
      { "keyword": "translational", "mentions": 6, "priority": "medium" }
    ],
    "ai_analysis": {
      "summary": "This RFA emphasizes...",
      "key_requirements": [ ... ],
      "implicit_preferences": [ ... ],
      "success_factors": [ ... ],
      "common_pitfalls": [ ... ]
    },
    "keyword_frequencies": {
      "immunotherapy": 45,
      "CAR-T": 12,
      "tumor microenvironment": 8
    },
    "status": "active",
    "projects": [
      { "id": "proj_123", "name": "R01 Cancer Immunotherapy" }
    ],
    "created_at": "2024-11-01T10:00:00Z",
    "updated_at": "2024-11-02T14:00:00Z"
  }
}
```

---

### 6.6 Get RFA Requirements

```
GET /api/v1/rfas/{rfa_id}/requirements
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "req_001",
      "rfa_id": "rfa_550e8400...",
      "requirement_type": "format",
      "category": "specific_aims",
      "description": "Specific Aims must not exceed 1 page",
      "is_mandatory": true,
      "validation_rule": {
        "type": "page_limit",
        "max": 1
      }
    },
    {
      "id": "req_002",
      "requirement_type": "content",
      "category": "innovation",
      "description": "Must address how the proposed research is innovative",
      "is_mandatory": true,
      "validation_rule": {
        "type": "keyword_presence",
        "keywords": ["innovative", "novel", "new approach"]
      }
    },
    {
      "id": "req_003",
      "requirement_type": "attachment",
      "category": "letters_of_support",
      "description": "Letters of support from collaborators",
      "is_mandatory": true,
      "validation_rule": {
        "type": "document_count",
        "min": 2
      }
    }
  ]
}
```

---

### 6.7 Analyze RFA

```
POST /api/v1/rfas/{rfa_id}/analyze
```

**Request:**
```json
{
  "depth": "comprehensive",
  "include_prior_awards": true,
  "include_success_factors": true
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "task_id": "task_abc123",
    "status": "processing",
    "estimated_time": 180
  }
}
```

---

### 6.8 Get RFA Prior Awards

```
GET /api/v1/rfas/{rfa_id}/prior-awards
```

**Query Parameters:**
- `years` (integer, default: 3) — How many years back to search
- `limit` (integer, default: 20) — Number of results

**Response:**
```json
{
  "success": true,
  "data": {
    "rfa_id": "rfa_550e8400...",
    "search_years": 3,
    "total_found": 47,
    "awards": [
      {
        "project_number": "1R01CA234567-01",
        "pi_name": "Dr. Jane Smith",
        "institution": "Harvard Medical School",
        "title": "Novel CAR-T Approaches for Solid Tumors",
        "abstract": "This project aims to...",
        "fiscal_year": 2024,
        "award_amount": 485000,
        "source": "nih_reporter"
      }
    ],
    "patterns": {
      "avg_budget": 467000,
      "common_keywords": ["CAR-T", "immunotherapy", "solid tumors"],
      "top_institutions": ["Harvard", "Stanford", "UCSF"],
      "common_approaches": [ ... ]
    }
  }
}
```

---

## 7. Agents API

### 7.1 Create Agent Task

```
POST /api/v1/agents/tasks
```

**Request:**
```json
{
  "agent_type": "research",
  "project_id": "550e8400-e29b-41d4-a716-446655440000",
  "task_description": "Research competitive landscape for CAR-T R01 grants and identify key gaps",
  "config": {
    "time_limit_minutes": 120,
    "depth_level": "comprehensive",
    "sources": {
      "nih_reporter": true,
      "pubmed": true,
      "web_search": true,
      "my_documents": true,
      "folder_paths": ["/Dropbox/Papers/2023-2024"]
    },
    "focus_keywords": ["CAR-T", "solid tumors", "tumor microenvironment"],
    "exclude_keywords": []
  }
}
```

**Agent Types:**
- `research` — Research Agent
- `writing` — Writing Agent
- `compliance` — Compliance Agent
- `creative` — Creative Agent (image generation)
- `analysis` — Analysis Agent
- `learning` — Learning Agent

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "id": "task_550e8400-e29b-41d4-a716-446655440000",
    "agent_type": "research",
    "project_id": "550e8400-e29b-41d4-a716-446655440000",
    "task_description": "Research competitive landscape...",
    "status": "queued",
    "config": { ... },
    "created_at": "2025-01-10T14:30:00Z",
    "estimated_start": "2025-01-10T14:30:05Z"
  }
}
```

---

### 7.2 Get Agent Task

```
GET /api/v1/agents/tasks/{task_id}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "task_550e8400-e29b-41d4-a716-446655440000",
    "agent_type": "research",
    "project_id": "550e8400-e29b-41d4-a716-446655440000",
    "task_description": "Research competitive landscape...",
    "status": "running",
    "config": { ... },
    "started_at": "2025-01-10T14:30:05Z",
    "completed_at": null,
    "progress": {
      "percent": 45,
      "current_step": "Analyzing NIH Reporter results",
      "steps_completed": 3,
      "steps_total": 7
    },
    "activity_log": [
      {
        "timestamp": "2025-01-10T14:30:05Z",
        "type": "info",
        "message": "Starting research task"
      },
      {
        "timestamp": "2025-01-10T14:30:10Z",
        "type": "action",
        "message": "Querying NIH Reporter for R01 grants in CAR-T space"
      },
      {
        "timestamp": "2025-01-10T14:31:02Z",
        "type": "result",
        "message": "Found 47 funded grants (2021-2024)"
      },
      {
        "timestamp": "2025-01-10T14:31:05Z",
        "type": "action",
        "message": "Analyzing your manuscript: CAR-T_manuscript_2024.pdf"
      },
      {
        "timestamp": "2025-01-10T14:32:30Z",
        "type": "insight",
        "message": "Found strong preliminary data aligning with RFA priority"
      }
    ],
    "interim_results": {
      "nih_grants_found": 47,
      "key_pis_identified": 12,
      "your_relevant_docs": 5
    },
    "tokens_used": 15420,
    "cost_incurred": 0.31,
    "user_injections": [],
    "created_at": "2025-01-10T14:30:00Z"
  }
}
```

---

### 7.3 List Agent Tasks

```
GET /api/v1/agents/tasks
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| project_id | uuid | Filter by project |
| agent_type | string | Filter by agent type |
| status | string | Filter: queued, running, paused, completed, failed, cancelled |
| limit | integer | Items per page |
| cursor | string | Pagination cursor |

---

### 7.4 Inject Context into Running Task

```
POST /api/v1/agents/tasks/{task_id}/inject
```

**Request:**
```json
{
  "type": "context",
  "content": "Also focus on the tumor microenvironment aspects, and check Dr. Smith's recent publications",
  "document_ids": ["doc_abc123"]
}
```

**Injection Types:**
- `context` — Add additional context/instructions
- `document` — Add documents to consider
- `constraint` — Add new constraints
- `redirect` — Redirect focus

**Response:**
```json
{
  "success": true,
  "data": {
    "injection_id": "inj_001",
    "task_id": "task_550e8400...",
    "type": "context",
    "acknowledged": true,
    "acknowledged_at": "2025-01-10T14:35:00Z"
  }
}
```

---

### 7.5 Pause Agent Task

```
POST /api/v1/agents/tasks/{task_id}/pause
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "task_550e8400...",
    "status": "paused",
    "paused_at": "2025-01-10T14:35:00Z",
    "checkpoint": {
      "step": 4,
      "can_resume": true
    }
  }
}
```

---

### 7.6 Resume Agent Task

```
POST /api/v1/agents/tasks/{task_id}/resume
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "task_550e8400...",
    "status": "running",
    "resumed_at": "2025-01-10T14:40:00Z"
  }
}
```

---

### 7.7 Cancel Agent Task

```
POST /api/v1/agents/tasks/{task_id}/cancel
```

**Request:**
```json
{
  "save_partial_results": true
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "task_550e8400...",
    "status": "cancelled",
    "cancelled_at": "2025-01-10T14:40:00Z",
    "partial_results_saved": true
  }
}
```

---

### 7.8 Get Agent Task Results

```
GET /api/v1/agents/tasks/{task_id}/results
```

**Response (for completed research task):**
```json
{
  "success": true,
  "data": {
    "task_id": "task_550e8400...",
    "agent_type": "research",
    "status": "completed",
    "completed_at": "2025-01-10T16:30:00Z",
    "duration_minutes": 120,
    "result": {
      "summary": "Analysis of competitive landscape reveals...",
      "competitive_landscape": {
        "total_grants_analyzed": 47,
        "key_pis": [
          {
            "name": "Dr. Jane Smith",
            "institution": "Harvard",
            "grants": 3,
            "focus": "CAR-T manufacturing",
            "publications_recent": 12
          }
        ],
        "funding_trends": { ... },
        "gaps_identified": [
          "Limited focus on tumor microenvironment remodeling",
          "Few grants addressing solid tumor penetration"
        ]
      },
      "your_positioning": {
        "strengths": [
          "Strong preliminary data on TME remodeling (Fig 3, CAR-T_manuscript_2024.pdf)"
        ],
        "opportunities": [
          "Your work addresses identified gap in TME focus"
        ],
        "recommendations": [
          "Emphasize health disparities angle (RFA mentions 12x)",
          "Consider collaboration with immunology core"
        ]
      },
      "sources_used": [
        { "type": "nih_reporter", "queries": 5, "results": 47 },
        { "type": "pubmed", "queries": 8, "results": 156 },
        { "type": "your_documents", "analyzed": 5 }
      ]
    },
    "result_summary": "Identified 3 key gaps in current funding landscape that align with your preliminary data.",
    "tokens_used": 45230,
    "cost_incurred": 0.91
  }
}
```

---

### 7.9 Writing Agent - Draft Section

Convenience endpoint for common writing task:

```
POST /api/v1/agents/write
```

**Request:**
```json
{
  "project_id": "550e8400-e29b-41d4-a716-446655440000",
  "section_type": "significance",
  "instructions": "Draft the significance section emphasizing health disparities and clinical impact",
  "context": {
    "use_rfa": true,
    "use_preliminary_data": true,
    "reference_documents": ["doc_abc123"],
    "style_profile_id": "style_xyz"
  },
  "constraints": {
    "max_pages": 2,
    "tone": "assertive",
    "include_citations": true
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "task_id": "task_550e8400...",
    "status": "processing",
    "stream_url": "wss://localhost:8000/ws/tasks/task_550e8400..."
  }
}
```

---

### 7.10 Creative Agent - Generate Figure

```
POST /api/v1/agents/create-figure
```

**Request:**
```json
{
  "project_id": "550e8400-e29b-41d4-a716-446655440000",
  "description": "Create a schematic showing CAR-T cell manufacturing process with 4 steps: collection, modification, expansion, and infusion",
  "style": {
    "type": "scientific_schematic",
    "color_scheme": "professional",
    "include_labels": true
  },
  "output": {
    "format": "png",
    "width": 1200,
    "height": 800
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "task_id": "task_550e8400...",
    "status": "processing"
  }
}
```

After completion:
```json
{
  "success": true,
  "data": {
    "task_id": "task_550e8400...",
    "status": "completed",
    "result": {
      "image_url": "/api/v1/files/generated/fig_abc123.png",
      "thumbnail_url": "/api/v1/files/generated/fig_abc123_thumb.png",
      "prompt_used": "Scientific schematic diagram showing...",
      "model": "dall-e-3",
      "iterations": 1
    }
  }
}
```

---

## 8. Chat API

### 8.1 Send Chat Message

```
POST /api/v1/chat
```

**Request:**
```json
{
  "project_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Can you help me strengthen the significance section? The reviewers said it wasn't impactful enough last time.",
  "context": {
    "current_section_id": "sec_abc123",
    "include_rfa": true,
    "include_prior_feedback": true
  },
  "stream": true
}
```

**Response (if stream: false):**
```json
{
  "success": true,
  "data": {
    "id": "msg_550e8400-e29b-41d4-a716-446655440000",
    "role": "assistant",
    "content": "Looking at your draft and the reviewer feedback from your 2023 submission, I see three opportunities...",
    "context_used": [
      { "type": "document", "id": "doc_abc", "excerpt": "..." },
      { "type": "review", "id": "rev_xyz", "excerpt": "..." }
    ],
    "suggestions": [
      {
        "type": "edit",
        "section_id": "sec_abc123",
        "original": "This research is important...",
        "suggested": "This research addresses a critical gap...",
        "rationale": "More assertive language"
      }
    ],
    "tokens_used": 1250,
    "created_at": "2025-01-10T14:30:00Z"
  }
}
```

**Response (if stream: true):**
```json
{
  "success": true,
  "data": {
    "message_id": "msg_550e8400...",
    "stream_url": "wss://localhost:8000/ws/chat/msg_550e8400..."
  }
}
```

---

### 8.2 Get Chat History

```
GET /api/v1/chat/history/{project_id}
```

**Query Parameters:**
- `limit` (integer, default: 50)
- `before` (datetime) — Messages before this time
- `after` (datetime) — Messages after this time

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "msg_001",
      "role": "user",
      "content": "Can you help me strengthen the significance section?",
      "created_at": "2025-01-10T14:30:00Z"
    },
    {
      "id": "msg_002",
      "role": "assistant",
      "content": "Looking at your draft and the reviewer feedback...",
      "context_used": [ ... ],
      "suggestions": [ ... ],
      "created_at": "2025-01-10T14:30:15Z"
    }
  ],
  "meta": {
    "pagination": { ... }
  }
}
```

---

### 8.3 Clear Chat History

```
DELETE /api/v1/chat/history/{project_id}
```

**Response (204 No Content)**

---

### 8.4 Apply Chat Suggestion

```
POST /api/v1/chat/suggestions/{suggestion_id}/apply
```

**Response:**
```json
{
  "success": true,
  "data": {
    "section_id": "sec_abc123",
    "applied": true,
    "new_version": 4
  }
}
```

---

## 9. Knowledge Base API

### 9.1 Search Knowledge Base

```
POST /api/v1/knowledge/search
```

**Request:**
```json
{
  "query": "CAR-T cell manufacturing process preliminary data",
  "filters": {
    "document_types": ["manuscript", "grant_draft"],
    "date_range": {
      "start": "2023-01-01",
      "end": null
    }
  },
  "limit": 10,
  "include_snippets": true
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "results": [
      {
        "id": "doc_550e8400...",
        "document_type": "manuscript",
        "filename": "CAR-T_manuscript_2024.pdf",
        "relevance_score": 0.92,
        "snippets": [
          {
            "text": "Our manufacturing process achieved 95% transduction efficiency...",
            "page": 5,
            "section": "Methods"
          }
        ]
      }
    ],
    "total_results": 8
  }
}
```

---

### 9.2 List Example Grants

```
GET /api/v1/knowledge/examples
```

**Query Parameters:**
- `quality_rating` — Filter: excellent, good, average, poor
- `was_funded` — Filter: true, false
- `grant_type` — Filter by grant type
- `is_own_grant` — Filter: true, false

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "ex_550e8400...",
      "document_id": "doc_abc123",
      "title": "R01 - Novel Immunotherapy Approach",
      "grant_type": "R01",
      "funder": "NIH-NCI",
      "quality_rating": "excellent",
      "was_funded": true,
      "is_own_grant": true,
      "annotations": {
        "specific_aims": "Very clear structure, strong preliminary data integration"
      },
      "strengths": [
        "Clear impact statement",
        "Strong preliminary data"
      ],
      "weaknesses": [],
      "source": "user_upload",
      "created_at": "2025-01-05T10:00:00Z"
    }
  ]
}
```

---

### 9.3 Add Example Grant

```
POST /api/v1/knowledge/examples
```

**Request:**
```json
{
  "document_id": "doc_abc123",
  "title": "R01 - Novel Immunotherapy Approach",
  "grant_type": "R01",
  "funder": "NIH-NCI",
  "quality_rating": "excellent",
  "was_funded": true,
  "is_own_grant": true,
  "annotations": {
    "specific_aims": "Very clear structure"
  },
  "strengths": ["Clear impact statement"],
  "weaknesses": []
}
```

---

### 9.4 Get Learned Patterns

```
GET /api/v1/knowledge/patterns
```

**Query Parameters:**
- `pattern_type` — Filter: writing_style, reviewer_critique, success_factor, failure_pattern
- `category` — Filter by section/category
- `min_confidence` — Minimum confidence threshold (0.0-1.0)

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "pat_001",
      "pattern_type": "reviewer_critique",
      "category": "approach",
      "pattern_description": "Feasibility concerns raised when timeline is not detailed enough",
      "evidence": [
        { "submission_id": "sub_abc", "review_excerpt": "Timeline seems optimistic..." }
      ],
      "confidence": 0.85,
      "occurrence_count": 5,
      "recommendation": "Include detailed milestone table in Approach section",
      "is_active": true,
      "created_at": "2025-01-01T10:00:00Z"
    },
    {
      "id": "pat_002",
      "pattern_type": "success_factor",
      "category": "significance",
      "pattern_description": "Funded grants lead with clinical impact, not mechanism",
      "confidence": 0.78,
      "occurrence_count": 3,
      "is_active": true
    }
  ]
}
```

---

### 9.5 Get Style Profiles

```
GET /api/v1/knowledge/styles
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "style_001",
      "name": "Default",
      "description": "Learned from your successful grants and papers",
      "is_default": true,
      "settings": {
        "formality": 0.7,
        "confidence": 0.8,
        "technical_depth": 0.6,
        "conciseness": 0.5
      },
      "vocabulary_preferences": {
        "preferred": ["novel", "significant", "critical"],
        "avoided": ["interesting", "might", "could potentially"]
      },
      "phrase_patterns": {
        "impact_framing": "addresses a critical gap",
        "preliminary_data": "Our preliminary studies demonstrate"
      },
      "avoided_phrases": [
        "It's important to note that",
        "In conclusion",
        "This is a multifaceted"
      ],
      "source_documents": ["doc_abc", "doc_xyz"],
      "created_at": "2025-01-01T10:00:00Z"
    }
  ]
}
```

---

### 9.6 Create/Update Style Profile

```
POST /api/v1/knowledge/styles
```

**Request:**
```json
{
  "name": "Assertive Technical",
  "description": "More assertive tone for competitive grants",
  "settings": {
    "formality": 0.8,
    "confidence": 0.9,
    "technical_depth": 0.7,
    "conciseness": 0.6
  },
  "source_documents": ["doc_abc", "doc_xyz"],
  "is_default": false
}
```

---

### 9.7 Train Style from Documents

```
POST /api/v1/knowledge/styles/train
```

**Request:**
```json
{
  "style_id": "style_001",
  "document_ids": ["doc_abc", "doc_xyz", "doc_123"],
  "weight": "high"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "style_id": "style_001",
    "training_status": "processing",
    "task_id": "task_abc123",
    "documents_queued": 3
  }
}
```

---

## 10. References API

### 10.1 Search References

```
GET /api/v1/references/search
```

**Query Parameters:**
- `query` — Search in title, authors, abstract
- `pmid` — Search by PMID
- `doi` — Search by DOI
- `year_start` — Filter by year range
- `year_end` — Filter by year range

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "ref_550e8400...",
      "pmid": "12345678",
      "doi": "10.1000/xyz123",
      "title": "CAR-T Cell Therapy: Current Progress and Future Directions",
      "authors": [
        { "name": "Smith, J.", "affiliation": "Harvard" },
        { "name": "Johnson, A.", "affiliation": "MIT" }
      ],
      "journal": "Nature Medicine",
      "year": 2024,
      "volume": "30",
      "pages": "123-135",
      "abstract": "CAR-T cell therapy has revolutionized...",
      "in_knowledge_base": true,
      "citations_in_projects": 3
    }
  ]
}
```

---

### 10.2 Lookup Reference by Identifier

```
GET /api/v1/references/lookup
```

**Query Parameters:**
- `pmid` — PubMed ID
- `doi` — Digital Object Identifier
- `title` — Title for fuzzy search

**Response:**
```json
{
  "success": true,
  "data": {
    "found": true,
    "source": "pubmed",
    "reference": {
      "pmid": "12345678",
      "doi": "10.1000/xyz123",
      "title": "CAR-T Cell Therapy...",
      ...
    },
    "already_in_library": false
  }
}
```

---

### 10.3 Add Reference to Library

```
POST /api/v1/references
```

**Request:**
```json
{
  "pmid": "12345678"
}
```

Or with full details:
```json
{
  "doi": "10.1000/xyz123",
  "title": "CAR-T Cell Therapy...",
  "authors": [...],
  "journal": "Nature Medicine",
  "year": 2024
}
```

---

### 10.4 Sync with ReadCube

```
POST /api/v1/references/sync/readcube
```

**Request:**
```json
{
  "direction": "bidirectional",
  "collections": ["all"]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "task_id": "task_abc123",
    "status": "processing"
  }
}
```

---

### 10.5 Get Citation Suggestions

```
POST /api/v1/references/suggest
```

**Request:**
```json
{
  "text": "CAR-T cell therapy has shown remarkable success in hematological malignancies, but solid tumors remain challenging due to the immunosuppressive tumor microenvironment.",
  "section_type": "significance",
  "limit": 5
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "suggestions": [
      {
        "reference_id": "ref_abc",
        "pmid": "12345678",
        "title": "CAR-T in Solid Tumors: Challenges and Opportunities",
        "relevance_score": 0.94,
        "suggested_position": {
          "after_text": "immunosuppressive tumor microenvironment",
          "rationale": "Supports the claim about TME challenges"
        }
      }
    ]
  }
}
```

---

## 11. Settings API

### 11.1 Get All Settings

```
GET /api/v1/settings
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "name": "Dr. Jane Smith",
      "email": "jane.smith@university.edu",
      "institution": "University Medical Center",
      "department": "Oncology"
    },
    "llm": {
      "primary_provider": "anthropic",
      "primary_model": "claude-3-5-sonnet",
      "fallback_provider": "openai",
      "fallback_model": "gpt-4o",
      "local_provider": "ollama",
      "local_model": "llama3.2",
      "use_local_for_quick_edits": true,
      "api_keys_configured": {
        "anthropic": true,
        "openai": true,
        "ollama": true
      }
    },
    "costs": {
      "global_monthly_budget": 50.00,
      "global_monthly_used": 12.47,
      "alert_thresholds": [80, 90, 100],
      "hard_stop_at_limit": true
    },
    "folders": {
      "watched": [
        {
          "id": "folder_001",
          "path": "/Users/jane/Dropbox/Grants",
          "is_active": true,
          "last_synced": "2025-01-10T12:00:00Z"
        }
      ],
      "backup_path": "/Users/jane/Dropbox/GrantPilot_Backups"
    },
    "notifications": {
      "deadline_reminders": [30, 14, 7, 3, 1],
      "proactive_suggestions": true,
      "compliance_alerts": true
    },
    "ui": {
      "theme": "light",
      "default_mode": "copilot",
      "editor_font_size": 14
    }
  }
}
```

---

### 11.2 Update Settings

```
PUT /api/v1/settings
```

**Request:**
```json
{
  "llm": {
    "primary_provider": "openai",
    "primary_model": "gpt-4o"
  },
  "costs": {
    "global_monthly_budget": 75.00
  }
}
```

---

### 11.3 Update API Keys

```
PUT /api/v1/settings/api-keys
```

**Request:**
```json
{
  "anthropic": "sk-ant-...",
  "openai": "sk-..."
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "anthropic": { "configured": true, "valid": true },
    "openai": { "configured": true, "valid": true }
  }
}
```

---

### 11.4 Get Watched Folders

```
GET /api/v1/settings/folders
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "folder_001",
      "folder_path": "/Users/jane/Dropbox/Grants",
      "folder_name": "Grants",
      "is_active": true,
      "sync_interval_minutes": 60,
      "last_synced": "2025-01-10T12:00:00Z",
      "auto_classify": true,
      "default_document_type": null,
      "total_files": 47,
      "created_at": "2025-01-01T10:00:00Z"
    }
  ]
}
```

---

### 11.5 Add Watched Folder

```
POST /api/v1/settings/folders
```

**Request:**
```json
{
  "folder_path": "/Users/jane/Dropbox/Papers",
  "sync_interval_minutes": 120,
  "auto_classify": true,
  "scan_now": true
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "id": "folder_002",
    "folder_path": "/Users/jane/Dropbox/Papers",
    "is_active": true,
    "scan_task_id": "task_abc123"
  }
}
```

---

### 11.6 Remove Watched Folder

```
DELETE /api/v1/settings/folders/{folder_id}
```

**Query Parameters:**
- `remove_documents` (boolean, default: false) — Also remove indexed documents

---

### 11.7 Trigger Folder Scan

```
POST /api/v1/settings/folders/{folder_id}/scan
```

**Response:**
```json
{
  "success": true,
  "data": {
    "task_id": "task_abc123",
    "status": "scanning"
  }
}
```

---

### 11.8 Get Cost Summary

```
GET /api/v1/settings/costs
```

**Query Parameters:**
- `period` — day, week, month, year, all
- `group_by` — provider, model, project, purpose

**Response:**
```json
{
  "success": true,
  "data": {
    "period": "month",
    "start_date": "2025-01-01",
    "end_date": "2025-01-31",
    "total_cost": 12.47,
    "total_tokens": 2456000,
    "budget": 50.00,
    "budget_remaining": 37.53,
    "breakdown": {
      "by_provider": {
        "anthropic": { "cost": 8.23, "tokens": 1640000 },
        "openai": { "cost": 4.24, "tokens": 816000 }
      },
      "by_project": {
        "R01-Cancer-2024": { "cost": 7.82, "tokens": 1560000 },
        "K99-Neuroscience": { "cost": 3.45, "tokens": 690000 }
      },
      "by_purpose": {
        "drafting": { "cost": 5.12, "tokens": 1024000 },
        "research": { "cost": 4.35, "tokens": 870000 },
        "analysis": { "cost": 2.10, "tokens": 420000 },
        "embedding": { "cost": 0.90, "tokens": 142000 }
      }
    },
    "daily_trend": [
      { "date": "2025-01-01", "cost": 0.85 },
      { "date": "2025-01-02", "cost": 1.20 }
    ]
  }
}
```

---

### 11.9 Update Project Budget

```
PUT /api/v1/settings/budgets/{project_id}
```

**Request:**
```json
{
  "token_budget": 750000,
  "cost_budget": 35.00
}
```

---

### 11.10 Backup Database

```
POST /api/v1/settings/backup
```

**Request:**
```json
{
  "type": "full",
  "destination": "dropbox"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "backup_id": "bak_abc123",
    "status": "processing",
    "task_id": "task_xyz"
  }
}
```

---

### 11.11 List Backups

```
GET /api/v1/settings/backups
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "bak_abc123",
      "backup_type": "full",
      "backup_path": "/Dropbox/GrantPilot_Backups/backup_2025-01-10.sql.gz",
      "file_size": 15678432,
      "status": "completed",
      "created_at": "2025-01-10T02:00:00Z"
    }
  ]
}
```

---

### 11.12 Restore from Backup

```
POST /api/v1/settings/restore
```

**Request:**
```json
{
  "backup_id": "bak_abc123"
}
```

---

## 12. WebSocket Events

### 12.1 Connection

```
WebSocket URL: wss://localhost:8000/ws
```

**Connection Message:**
```json
{
  "type": "connect",
  "client_id": "client_abc123"
}
```

### 12.2 Subscribe to Channels

```json
{
  "type": "subscribe",
  "channels": [
    "project:550e8400-e29b-41d4-a716-446655440000",
    "agent:task_abc123",
    "global"
  ]
}
```

### 12.3 Event Types

#### Agent Activity Events

```json
{
  "type": "agent:activity",
  "task_id": "task_abc123",
  "data": {
    "timestamp": "2025-01-10T14:30:05Z",
    "activity_type": "action",
    "message": "Querying NIH Reporter for R01 grants",
    "progress": {
      "percent": 25,
      "step": 2,
      "total_steps": 8
    }
  }
}
```

#### Agent Status Change

```json
{
  "type": "agent:status",
  "task_id": "task_abc123",
  "data": {
    "previous_status": "running",
    "new_status": "completed",
    "timestamp": "2025-01-10T16:30:00Z"
  }
}
```

#### Agent Result Ready

```json
{
  "type": "agent:result",
  "task_id": "task_abc123",
  "data": {
    "status": "completed",
    "summary": "Analysis complete. Found 47 grants, identified 3 key gaps.",
    "result_url": "/api/v1/agents/tasks/task_abc123/results"
  }
}
```

#### Chat Message Streaming

```json
{
  "type": "chat:token",
  "message_id": "msg_abc123",
  "data": {
    "token": "Looking",
    "index": 0
  }
}
```

```json
{
  "type": "chat:complete",
  "message_id": "msg_abc123",
  "data": {
    "full_content": "Looking at your draft...",
    "suggestions": [...],
    "tokens_used": 1250
  }
}
```

#### Document Processing Events

```json
{
  "type": "document:processing",
  "document_id": "doc_abc123",
  "data": {
    "status": "processing",
    "step": "extracting_text",
    "progress": 50
  }
}
```

```json
{
  "type": "document:ready",
  "document_id": "doc_abc123",
  "data": {
    "status": "completed",
    "document_type": "manuscript",
    "chunks_created": 45
  }
}
```

#### Compliance Update

```json
{
  "type": "compliance:update",
  "project_id": "proj_abc123",
  "data": {
    "score": 85,
    "previous_score": 78,
    "changes": [
      { "requirement": "timeline", "status": "now_complete" }
    ]
  }
}
```

#### Notification Events

```json
{
  "type": "notification",
  "data": {
    "id": "notif_abc123",
    "category": "deadline",
    "severity": "warning",
    "title": "Deadline Approaching",
    "message": "R01-Cancer-2024 deadline in 7 days",
    "project_id": "proj_abc123",
    "action_url": "/projects/proj_abc123",
    "timestamp": "2025-01-10T09:00:00Z"
  }
}
```

#### Cost Alert

```json
{
  "type": "cost:alert",
  "data": {
    "alert_type": "threshold",
    "project_id": "proj_abc123",
    "threshold_percent": 80,
    "current_percent": 82,
    "message": "Project R01-Cancer-2024 has used 82% of its budget"
  }
}
```

#### Folder Sync Events

```json
{
  "type": "folder:sync",
  "folder_id": "folder_001",
  "data": {
    "status": "syncing",
    "files_found": 5,
    "files_processed": 2
  }
}
```

```json
{
  "type": "folder:new_file",
  "folder_id": "folder_001",
  "data": {
    "document_id": "doc_new123",
    "filename": "new_manuscript.pdf",
    "classified_as": "manuscript"
  }
}
```

### 12.4 Unsubscribe

```json
{
  "type": "unsubscribe",
  "channels": ["agent:task_abc123"]
}
```

### 12.5 Heartbeat

Client should send heartbeat every 30 seconds:
```json
{
  "type": "ping"
}
```

Server responds:
```json
{
  "type": "pong",
  "timestamp": "2025-01-10T14:30:00Z"
}
```

---

## 13. Error Codes Reference

### 13.1 General Errors

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Request validation failed |
| `INVALID_JSON` | 400 | Malformed JSON in request body |
| `UNAUTHORIZED` | 401 | Authentication required |
| `FORBIDDEN` | 403 | Not authorized for this action |
| `NOT_FOUND` | 404 | Resource not found |
| `CONFLICT` | 409 | Resource conflict (e.g., duplicate) |
| `RATE_LIMITED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Unexpected server error |

### 13.2 Domain-Specific Errors

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `PROJECT_NOT_FOUND` | 404 | Project does not exist |
| `DOCUMENT_NOT_FOUND` | 404 | Document does not exist |
| `RFA_NOT_FOUND` | 404 | RFA does not exist |
| `TASK_NOT_FOUND` | 404 | Agent task does not exist |
| `DOCUMENT_PROCESSING_FAILED` | 422 | Document could not be processed |
| `UNSUPPORTED_FILE_TYPE` | 422 | File type not supported |
| `FILE_TOO_LARGE` | 422 | File exceeds size limit |
| `TASK_ALREADY_RUNNING` | 409 | Agent task is already running |
| `TASK_NOT_PAUSABLE` | 409 | Task cannot be paused in current state |
| `BUDGET_EXCEEDED` | 402 | Cost budget exceeded |
| `LLM_UNAVAILABLE` | 503 | LLM provider unavailable |
| `LLM_RATE_LIMITED` | 429 | LLM provider rate limited |
| `FOLDER_NOT_ACCESSIBLE` | 422 | Cannot access folder path |
| `BACKUP_FAILED` | 500 | Backup operation failed |
| `RESTORE_FAILED` | 500 | Restore operation failed |

### 13.3 Error Response Examples

**Validation Error:**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": {
      "fields": {
        "deadline": "Must be a future date",
        "budget_total": "Must be a positive number"
      }
    }
  }
}
```

**Budget Exceeded:**
```json
{
  "success": false,
  "error": {
    "code": "BUDGET_EXCEEDED",
    "message": "Project cost budget has been exceeded",
    "details": {
      "project_id": "proj_abc123",
      "budget": 25.00,
      "current_usage": 25.12,
      "action_required": "Increase budget or wait for next billing cycle"
    }
  }
}
```

**LLM Unavailable:**
```json
{
  "success": false,
  "error": {
    "code": "LLM_UNAVAILABLE",
    "message": "Primary LLM provider is unavailable",
    "details": {
      "provider": "anthropic",
      "fallback_attempted": true,
      "fallback_provider": "openai",
      "fallback_status": "also_unavailable"
    }
  }
}
```

---

## Appendix: TypeScript Types

For frontend development, here are the core TypeScript interfaces:

```typescript
// Core types
interface ApiResponse<T> {
  success: boolean;
  data: T;
  meta: {
    timestamp: string;
    request_id: string;
    pagination?: PaginationMeta;
  };
}

interface ApiError {
  success: false;
  error: {
    code: string;
    message: string;
    details?: Record<string, any>;
  };
  meta: {
    timestamp: string;
    request_id: string;
  };
}

interface PaginationMeta {
  total: number;
  limit: number;
  has_more: boolean;
  next_cursor: string | null;
  prev_cursor: string | null;
}

// Project types
interface Project {
  id: string;
  name: string;
  description: string | null;
  status: 'draft' | 'in_progress' | 'submitted' | 'funded' | 'not_funded' | 'archived';
  grant_type: string | null;
  funder: string | null;
  mechanism: string | null;
  rfa_id: string | null;
  budget_total: number | null;
  budget_per_year: number | null;
  deadline: string | null;
  internal_deadline: string | null;
  token_budget: number | null;
  tokens_used: number;
  cost_budget: number | null;
  cost_used: number;
  created_at: string;
  updated_at: string;
}

interface ProjectSection {
  id: string;
  project_id: string;
  section_type: string;
  title: string;
  content: string;
  version: number;
  word_count: number;
  page_count: number;
  word_limit: number | null;
  page_limit: number | null;
  is_compliant: boolean;
  ai_suggestions: AISuggestion[];
  compliance_issues: ComplianceIssue[];
  created_at: string;
  updated_at: string;
}

// Document types
interface Document {
  id: string;
  filename: string;
  file_path: string;
  file_type: string;
  file_size: number;
  document_type: string | null;
  document_subtype: string | null;
  processing_status: 'pending' | 'processing' | 'completed' | 'failed';
  project_id: string | null;
  source: 'upload' | 'folder_watch' | 'web_download';
  extracted_metadata: Record<string, any>;
  created_at: string;
  updated_at: string;
}

// Agent types
interface AgentTask {
  id: string;
  agent_type: 'research' | 'writing' | 'compliance' | 'creative' | 'analysis' | 'learning';
  project_id: string | null;
  task_description: string;
  status: 'queued' | 'running' | 'paused' | 'completed' | 'failed' | 'cancelled';
  config: AgentTaskConfig;
  progress: TaskProgress | null;
  activity_log: ActivityLogEntry[];
  result: Record<string, any> | null;
  tokens_used: number;
  cost_incurred: number;
  created_at: string;
  started_at: string | null;
  completed_at: string | null;
}

interface TaskProgress {
  percent: number;
  current_step: string;
  steps_completed: number;
  steps_total: number;
}

interface ActivityLogEntry {
  timestamp: string;
  type: 'info' | 'action' | 'result' | 'insight' | 'error';
  message: string;
}

// WebSocket event types
type WebSocketEvent = 
  | AgentActivityEvent
  | AgentStatusEvent
  | AgentResultEvent
  | ChatTokenEvent
  | ChatCompleteEvent
  | DocumentProcessingEvent
  | NotificationEvent
  | CostAlertEvent;

interface AgentActivityEvent {
  type: 'agent:activity';
  task_id: string;
  data: {
    timestamp: string;
    activity_type: string;
    message: string;
    progress: TaskProgress;
  };
}

// ... additional types
```

---

*End of API Contracts Document*

# GrantPilot Specification Issues

**Generated:** 2026-01-12
**Review Method:** Adversarial multi-model debate (GPT-4o, Gemini 2.0 Flash, Deepseek Chat) + Claude analysis
**Total Review Cost:** $0.0183

---

## Summary

| Priority | Count | Status |
|----------|-------|--------|
| Critical | 5 | Open |
| High | 4 | Open |
| Medium | 4 | Open |
| Low | 3 | Open |

---

## Critical Issues (Must Fix Before v1)

### SPEC-001: Embedding Dimension Inconsistency
**Status:** Open
**Source:** All models + Claude
**Location:** `grantpilot-specification.md` Section 7, `document_chunks` table

**Problem:**
- Spec shows `vector(1536)` in database schema
- Implementation uses 768-dim (per HANDOFF.md)
- OpenAI `text-embedding-3-small` defaults to 1536, but can output 768
- PubMedBERT outputs 768

**Resolution:**
- [ ] Decide canonical dimension: **768** (matches implementation, PubMedBERT compatible)
- [ ] Update spec Section 7: `embedding vector(768)`
- [ ] Document in spec which embedding model is primary

---

### SPEC-002: Missing Goals and Non-Goals
**Status:** Open
**Source:** All 3 models (unanimous)
**Location:** `grantpilot-specification.md` - missing section

**Problem:**
No explicit statement of what Phase 1b aims to achieve and what is explicitly out of scope.

**Resolution:**
Add section after Overview:

```markdown
## Goals and Non-Goals

### Phase 1b Goals
- G1: Implement WebSocket infrastructure for real-time agent updates
- G2: Develop and integrate the Writing Agent
- G3: Implement Agent Orchestrator for task decomposition and collaboration
- G4: Implement style learning from user's uploaded documents
- G5: Add cost tracking per agent/task

### Phase 1b Non-Goals
- NG1: Full ReadCube API integration (deferred - API may be restricted)
- NG2: Image generation via "Nano Banana API" (service unclear)
- NG3: Cloud deployment (local Docker only)
- NG4: Multi-user collaboration
- NG5: Advanced agent crash recovery beyond basic checkpointing
```

---

### SPEC-003: ReadCube Integration Dependency Risk
**Status:** Open
**Source:** Claude
**Location:** `grantpilot-specification.md` Section 5.3

**Problem:**
ReadCube is marked "critical for v1" but:
- No public API documentation exists
- "API access may be restricted"
- Single point of failure for citation management

**Resolution:**
- [ ] Demote ReadCube to "optional enhancement"
- [ ] Promote fallback methods to primary:
  - RIS/BibTeX import from any reference manager
  - PMID/DOI bulk import
  - Paste title → auto-lookup
- [ ] Update spec to reflect this priority change

---

### SPEC-004: "Nano Banana API" - Undefined Service
**Status:** Open
**Source:** All models + Claude
**Location:** `grantpilot-specification.md` Section 5.4, Creative Agent

**Problem:**
"Nano Banana API" listed as primary for scientific illustrations. No documentation or public API exists for this service.

**Resolution:**
- [ ] Clarify what this service is (internal tool? placeholder?)
- [ ] If unavailable, update spec to use DALL-E 3 as primary
- [ ] Consider Stable Diffusion as local fallback

---

### SPEC-005: No Agent Checkpoint Format
**Status:** Open
**Source:** Deepseek + Claude
**Location:** `grantpilot-specification.md` - missing

**Problem:**
Agent pause/resume/cancel endpoints exist but:
- No checkpoint data format specified
- No recovery mechanism for partial completions
- A 2-hour research task crash loses all work

**Resolution:**
Add to database schema and document format:

```sql
-- In agent_tasks table
checkpoint JSONB DEFAULT '{}'::jsonb,
-- Structure:
-- {
--   "last_step": "string",
--   "completed_items": ["item1", "item2"],
--   "interim_results": {...},
--   "tokens_spent": 1234,
--   "timestamp": "ISO8601"
-- }
```

- [ ] Define checkpoint schema per agent type
- [ ] Implement checkpoint save after each logical work unit
- [ ] Add recovery logic in Orchestrator

---

## High Priority Issues (Should Fix for v1)

### SPEC-006: API URL Inconsistency
**Status:** Open
**Source:** Claude
**Location:** Multiple files

**Problem:**
- API contracts header: `Base URL: http://localhost:8000/api/v1`
- Current implementation: `/api` (fixed in Phase 1a)
- Creates confusion for implementers

**Resolution:**
- [ ] Pick one: recommend `/api/v1` for versioning
- [ ] Update all documentation consistently
- [ ] Update implementation to match

---

### SPEC-007: Missing Security Specification
**Status:** Open
**Source:** All 3 models
**Location:** `grantpilot-specification.md` - inadequate coverage

**Problem:**
Security mentioned superficially. Missing:
- Authentication mechanism details
- Authorization model
- API key storage encryption
- Input validation strategy
- Audit logging

**Resolution:**
Add Security section:

```markdown
## Security Considerations

### Authentication
- Phase 1b: API key-based (single user)
- Future: JWT with 24-hour expiry, OAuth 2.0

### Authorization
- Row-Level Security: All queries filter by user context
- API endpoints validate ownership before operations

### Data Protection
- Passwords: bcrypt with work factor 12
- API keys: Encrypted at rest using system keyring (macOS Keychain)
- PII: User email/name encrypted via PostgreSQL pgcrypto
- Secrets: Environment variables, never in code

### Input Validation
- All API inputs validated via Pydantic models
- File uploads restricted to: .pdf, .docx, .txt
- Max file size: 50MB

### Audit Logging
- All agent tasks logged with user_id, timestamp, cost
- Document uploads tracked
- LLM calls logged (prompt hash, not content)
```

---

### SPEC-008: Missing Performance SLAs
**Status:** Open
**Source:** All 3 models
**Location:** `grantpilot-specification.md` - missing section

**Problem:**
No specific, measurable performance targets.

**Resolution:**
Add Performance Requirements section:

```markdown
## Performance Requirements / SLAs

| Metric | Target | Measurement |
|--------|--------|-------------|
| API Response Time | p95 < 500ms | All non-streaming endpoints |
| Chat First Token | p95 < 1.5s | WebSocket streaming |
| Chat Complete Response | p95 < 30s | Full response delivered |
| Document Processing | p95 < 60s | Per 10-page PDF |
| RAG Query | p95 < 1s | Vector search + context retrieval |
| System Availability | 99.5% | Excluding scheduled maintenance |
| Concurrent Users | 50 | Supported per instance |
```

---

### SPEC-009: Missing Observability Specification
**Status:** Open
**Source:** All 3 models
**Location:** `grantpilot-specification.md` - missing section

**Problem:**
No logging, metrics, or alerting strategy defined.

**Resolution:**
Add Observability section:

```markdown
## Observability

### Logging
- Structured JSON to stdout
- Fields: timestamp, level, service, endpoint, user_id, correlation_id, message
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL

### Metrics (Prometheus)
- `api_request_duration_seconds` (histogram by endpoint)
- `agent_task_duration_seconds` (histogram by agent_type)
- `llm_requests_total` (counter by provider, model)
- `document_processing_seconds` (histogram)
- `active_websocket_connections` (gauge)

### Alerting
- Warning: API p95 > 800ms for 5 minutes
- Warning: Error rate > 2% for 5 minutes
- Critical: Error rate > 5% for 2 minutes
- Critical: Health check fails 3 consecutive times
```

---

## Medium Priority Issues

### SPEC-010: Style Learning Cold Start
**Status:** Open
**Source:** Claude
**Location:** `grantpilot-specification.md` Section 5.6

**Problem:**
- Requires 10+ documents for "confident" tier
- No onboarding guidance for new users
- Users start with "generic" output

**Resolution:**
- [ ] Add onboarding wizard guiding first 5-10 uploads
- [ ] Consider bundling sample funded grants (NIH grants are public)
- [ ] Document expected time to confidence

---

### SPEC-011: Missing Error Handling Strategy
**Status:** Open
**Source:** All 3 models
**Location:** `grantpilot-specification.md` - missing section

**Problem:**
No enumeration of error scenarios or handling strategy.

**Resolution:**
Add Error Handling section:

```markdown
## Error Handling Strategy

### API Errors
| Code | HTTP Status | Description |
|------|-------------|-------------|
| ERR_INVALID_INPUT | 400 | Validation failed |
| ERR_UNAUTHORIZED | 401 | Invalid/missing auth |
| ERR_NOT_FOUND | 404 | Resource doesn't exist |
| ERR_RATE_LIMITED | 429 | Too many requests |
| ERR_TASK_FAILED | 500 | Agent task failed |
| ERR_LLM_UNAVAILABLE | 503 | LLM provider down |

### Retry Logic
- Transient failures: Exponential backoff (1s, 2s, 4s), max 3 retries
- LLM failures: Fallback chain (Claude → OpenAI → Ollama)

### Agent Crash Recovery
- Checkpoint saved after each logical work unit
- On worker restart, Orchestrator resumes from last checkpoint
```

---

### SPEC-012: Cost Tracking Granularity
**Status:** Open
**Source:** Claude
**Location:** `grantpilot-specification.md` Section 4.3

**Problem:**
Token tracking exists per-project, but:
- No per-agent breakdown
- No per-task attribution
- Hard to audit "where did my budget go?"

**Resolution:**
- [ ] Add `cost_cents` and `token_usage` columns to `agent_tasks` table
- [ ] Expose cost breakdown in UI per agent type
- [ ] Add daily/weekly cost summary endpoint

---

### SPEC-013: Missing Testing Strategy
**Status:** Open
**Source:** All 3 models
**Location:** `grantpilot-specification.md` - missing section

**Problem:**
"17 API tests passing" mentioned but no overall strategy.

**Resolution:**
Add Testing Strategy section:

```markdown
## Testing Strategy

### Unit Tests (pytest)
- Target: 80% line coverage for core business logic
- Mock external APIs (OpenAI, Anthropic, PubMed)
- Run on every commit

### Integration Tests
- Test API endpoints with test database
- Verify auth, data persistence, error flows
- Run on PR merge

### End-to-End Tests (Playwright)
- Critical journeys: login, project create, document upload, chat
- Run nightly

### Performance Tests (k6)
- Load test document upload and concurrent chat
- Validate against SLAs
- Run weekly
```

---

## Low Priority Issues

### SPEC-014: Inconsistent Grant Type Terminology
**Status:** Open
**Source:** Claude
**Location:** Throughout spec

**Problem:**
Overlapping terms: `grant_type`, `mechanism`, `funder` used inconsistently.

**Resolution:**
Normalize terminology:
- `funder`: Organization (NIH, NSF, DOD)
- `institute`: Sub-organization (NCI, NIDDK) - NIH only
- `mechanism`: Grant type (R01, R21, K99)
- `rfa_number`: Specific opportunity (RFA-CA-24-001)

---

### SPEC-015: WebSocket Reconnection Strategy
**Status:** Open
**Source:** Claude
**Location:** `grantpilot-api-contracts.md` WebSocket section

**Problem:**
- No client reconnection protocol
- No message queue for missed events
- 30-second heartbeat may timeout on slow networks

**Resolution:**
- [ ] Add exponential backoff reconnection (1s, 2s, 4s, max 30s)
- [ ] Add `last_event_id` for resuming missed events
- [ ] Consider SSE fallback for simpler clients

---

### SPEC-016: Phase 1b Scope Creep Risk
**Status:** Open
**Source:** Claude
**Location:** HANDOFF.md Phase 1b

**Problem:**
Phase 1b includes substantial scope:
- WebSocket infrastructure
- Writing Agent
- Agent Orchestrator
- Style learning
- Cost tracking

**Resolution:**
Consider splitting:
- **Phase 1b:** WebSocket + basic Writing Agent
- **Phase 1c:** Full Orchestrator + Style Learning
- **Phase 1d:** Cost tracking + refinements

---

## Changelog

| Date | Change |
|------|--------|
| 2026-01-12 | Initial issue list from adversarial review |


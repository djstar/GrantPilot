# GrantPilot Project Handoff for Claude Code

## Quick Start for Claude Code

When you start a Claude Code session, share this file first, then say:

```
I'm building GrantPilot, an AI-powered grant writing co-pilot.
I have comprehensive specs ready. Please read the handoff document
and all spec files, then let's continue from where we left off.
```

---

## Project Overview

**GrantPilot** is an AI-powered grant writing assistant with:
- **6 specialized agents** (Research, Writing, Compliance, Creative, Analysis, Learning)
- **Self-learning RAG system** that improves from feedback
- **Web application** (React + FastAPI + PostgreSQL)
- **Local-first deployment** via Docker

**Target User:** Biomedical researcher writing NIH/NSF/foundation grants

---

## Current Status

### ✅ Completed Specifications

| Document | Description | Lines |
|----------|-------------|-------|
| `grantpilot-specification.md` | Master spec document (v1.2) | ~2400 |
| `grantpilot-api-contracts.md` | 70+ REST endpoints, WebSocket events | ~3000 |
| `grantpilot-agent-prompts.md` | 36 Jinja2 prompt templates for all agents | ~2800 |
| `grantpilot-todo.md` | Progress tracker with session log | ~210 |

### Sections Complete
1. ✅ Executive Summary
2. ✅ Vision & Value Proposition
3. ✅ User Experience & Interface (3 modes + **Confidence Indicators**)
4. ✅ Multi-Agent Architecture (6 agents + **Orchestrator Collaboration Protocol**)
5. ✅ Self-Learning RAG System (**+ Style Confidence Tiers, Feedback Parsers**)
6. ✅ Technical Stack (React, FastAPI, PostgreSQL/pgvector, Docker)
7. ✅ Database Schema (complete PostgreSQL with 20+ tables)
8. ✅ API Contracts (70+ endpoints, WebSocket events, TypeScript types)
9. ✅ Agent Prompt Templates (**36 Jinja2 templates for all 6 agents + orchestrator**)
10. ✅ Workflow Diagrams (**4 user journeys + 5 system flows**)
11. ✅ UI Wireframes (**14 screens + design system + component specs**)
12. ✅ Development Phases (**Split Phase 1 into 1a/1b**)
- ✅ Appendix D: Offline/Sync Strategy
- ✅ Appendix E: Security Considerations
- ✅ Appendix F: Error Recovery & Crash Handling

### 🔲 Remaining TODO
- ~~**Section 10:** Workflow Diagrams~~ ✅ COMPLETE
- ~~**Section 11:** UI Wireframes~~ ✅ COMPLETE
- Testing Strategy ← **NEXT PRIORITY**
- Deployment Guide

---

## Technical Decisions Made

### Core Architecture
| Decision | Choice | Rationale |
|----------|--------|-----------|
| Deployment | Local Server + Browser | Simpler dev, Docker-friendly |
| Database | PostgreSQL + pgvector | Robust, vector search in single DB |
| Frontend | React 18 + TypeScript + Tailwind | Modern, well-supported |
| Backend | Python FastAPI + Celery | Good async, task queues |
| LLM Primary | Anthropic Claude / OpenAI | Best quality |
| LLM Fallback | Ollama (local) | Offline capability |
| Citations | PMID priority, then DOI | User preference |
| Reference Manager | ReadCube + RIS/BibTeX fallback | API may be limited |

### Design Session Decisions (January 2025)
| Decision | Choice | Rationale |
|----------|--------|-----------|
| Agent Collaboration | **Orchestrator-mediated** | All cross-agent requests go through orchestrator for visibility, cost control, and context management |
| Style Corpus Size | **10+ documents for high confidence** | With auto-weighting: funded grants 2x, unfunded 0.5x, recent preferred |
| Anti-LLM Detection | **Balanced mode** | Flag obvious AI patterns, but allow common scientific phrasing |
| Budget Limits | **Soft warning** | Complete current task, block new tasks when budget exceeded |
| Feedback Parsing | **Full template system** | NIH structured, NSF semi-structured, Foundation/generic NLP-based |
| Confidence Indicators | **Show everywhere** | All AI inferences show confidence (High/Medium/Low) for transparency |
| Phase 1 | **Split into 1a + 1b** | 1a=Core Foundation, 1b=Agent Foundation for faster time-to-usable |
| Image Generation | **Nano Banana primary** | DALL-E 3 as fallback; better scientific illustration control |
| Self-Learning | **Multi-layer architecture** | SPECTER2/PubMedBERT embeddings, LoRA fine-tuning, prompt evolution |

### ML Models & Self-Learning (January 2025)
| Component | Choice | Rationale |
|-----------|--------|-----------|
| Scientific Embeddings | **SPECTER2** (Allen AI) | Task-specific adapters; trained on 6M triplets across 23 fields |
| Biomedical Embeddings | **PubMedBERT** | 768-dim vectors optimized for medical/life science literature |
| Fallback Embeddings | **SciBERT** | 3.17B token pretraining on biomedical + CS papers |
| Local LLM | **BioMistral 2 / PMC-LLaMA** | Domain-specific, open-source for offline inference |
| Fine-Tuning | **QLoRA/PEFT** | 95%+ parameter reduction; runs on consumer hardware |
| Prompt Learning | **A/B testing + outcome correlation** | Prompts evolve based on acceptance rate and funding outcomes |

---

## Key User Requirements

1. **Web application** (not CLI) — needs visual document handling
2. **Agent mode** for autonomous research with:
   - Time/depth caps
   - Source scoping (checkboxes)
   - Mid-run context injection
   - Pause/resume/cancel
3. **Co-pilot mode** for interactive collaboration
4. **Review & Learn mode** (lower priority) for feedback ingestion
5. **Intelligent folder watching** — auto-ingest from Dropbox
6. **Style learning** — match user's writing voice, anti-LLM detection
7. **Cost tracking** with per-project budgets
8. **Crash recovery** — checkpoint agent tasks, auto-backup
9. **Single user** — no collaboration features needed
10. **Desktop only** — laptop use

---

## File Structure for Development

```
grantpilot/
├── docker-compose.yml
├── start.sh
├── README.md
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── api/           # REST endpoints
│   │   ├── agents/        # 6 agent implementations
│   │   ├── llm/           # LLM integrations
│   │   ├── rag/           # RAG system
│   │   ├── processors/    # Document processing
│   │   ├── services/      # Business logic
│   │   ├── db/            # SQLAlchemy models
│   │   ├── prompts/       # Jinja2 prompt templates
│   │   └── utils/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── stores/
│   │   ├── api/
│   │   └── types/
│   ├── package.json
│   └── Dockerfile
│
└── data/
    ├── postgresql/
    ├── redis/
    └── backups/
```

---

## Next Steps (What to Work On)

### Immediate: Agent Prompt Templates

Need to create Jinja2 prompt templates for each agent:

**Research Agent:**
- Web search query generation
- NIH Reporter query construction
- PubMed search optimization
- Competitive landscape synthesis

**Writing Agent:**
- Section drafting (specific aims, significance, etc.)
- Style matching/calibration
- Anti-LLM detection and rephrasing
- Reviewer perspective critique

**Compliance Agent:**
- RFA parsing and extraction
- Requirement identification
- "Reading between the lines" analysis

**Creative Agent:**
- DALL-E prompts for scientific figures
- Diagram generation

**Analysis Agent:**
- Figure interpretation
- Literature gap analysis

**Learning Agent:**
- Reviewer feedback parsing
- Pattern extraction
- Style profile generation

### Then: Workflow Diagrams & UI Wireframes

---

## Conversation Context

Key discussion points from our conversation:

1. User is inspired by Claude Code's agentic approach
2. Wants full autonomy for agents with guardrails (time caps, source scoping)
3. Emphasized need for organic growth/learning from examples
4. Domain: biomedical/life sciences, systems biology, immunology, AI/tech bio
5. Writes grants across NIH, NSF, DOD, foundations
6. Currently uses Word + Dropbox + ReadCube
7. No privacy concerns with cloud APIs
8. Wants image generation (DALL-E) for figures
9. In-app notifications only (no email)
10. Clean Word export (no track changes for now)

---

## How to Continue

1. Read all three spec files completely
2. Continue with Section 9: Agent Prompt Templates
3. Update `grantpilot-todo.md` as sections are completed
4. Keep `grantpilot-specification.md` as the master document
5. Create new files for each major section as needed

---

## Files to Load

Load these files in order:
1. `HANDOFF.md` (this file)
2. `grantpilot-specification.md`
3. `grantpilot-api-contracts.md`
4. `grantpilot-todo.md`

---

## Design Session Log

### Session: Claude.ai → Claude Code Migration (January 2025)

**What happened:**
- Migrated project from Claude.ai to Claude Code
- Claude Code reviewed full spec and asked clarifying questions
- Made 8 key design decisions based on user preferences
- Added 6 new sections/appendices to spec

**Questions Asked & Answers:**

1. **Agent orchestration model?**
   → Dynamic collaboration, but orchestrator-mediated (not autonomous agent-to-agent calls)

2. **Style corpus size expectation?**
   → 10+ documents including funded grants, papers, drafts across different projects

3. **ReadCube criticality?**
   → Critical for v1, but added RIS/BibTeX/PMID file fallback for reliability

4. **Reviewer feedback format?**
   → Varies by funder (NIH structured, foundations informal) → need parser templates

5. **Cross-agent task spawning?**
   → Through orchestrator for visibility and cost attribution

6. **Style weighting?**
   → Auto-weight with smart defaults (funded=2x, recent=1x, old=0.5x)

7. **Anti-LLM detection aggressiveness?**
   → Balanced (flag obvious, allow scientific phrases)

8. **Budget limit behavior?**
   → Soft warning (complete task, block new)

**Improvements Made:**

| Addition | Location | Description |
|----------|----------|-------------|
| Orchestrator Protocol | Section 4.2 | 6-step collaboration flow with rules table |
| Style Confidence Tiers | Section 5.2 | 3 tiers (Initializing/Learning/Confident) + auto-weighting |
| ReadCube Fallbacks | Section 5.3 | RIS/BibTeX import, PMID/DOI bulk lookup |
| Feedback Parser Templates | Section 5.5 | NIH, NSF, DOD, Foundation, Generic parsers |
| Confidence Indicators | Section 3.6 | System-wide transparency for all AI inferences |
| Phase 1 Split | Section 12 | 1a (core) + 1b (agents) for faster iteration |
| Offline/Sync Strategy | Appendix D | State machine, conflict resolution UI |
| Security Considerations | Appendix E | API key encryption, threat model |
| Error Recovery | Appendix F | Checkpointing, backup system, crash handling |

**Design Philosophy Captured:**
- Transparency over magic (show confidence, explain inferences)
- User control with smart defaults (auto-weight but allow override)
- Graceful degradation (offline mode, fallbacks, soft limits)
- Never lose work (checkpointing, WAL, backups)
- Single-user simplicity (no auth complexity, local-first)

---

### Session: Phase 1a Implementation (January 2026)

**What happened:**
- Built complete Phase 1a scaffold (Core Foundation)
- Created 39 files across backend and frontend
- All TypeScript compiles successfully
- Frontend builds to production

**Files Created:**

| Directory | Key Files |
|-----------|-----------|
| `src/backend/` | FastAPI app, SQLAlchemy models, API routers |
| `src/frontend/` | React + Vite, shadcn/ui components, pages |
| `src/` | docker-compose.yml, start.sh |

**Implementation Notes:**

1. **pgvector for embeddings**: Using 768-dim vectors for PubMedBERT compatibility
   - `DocumentChunk.embedding` uses `Vector(768)` from pgvector-python

2. **Docker service naming**: Service is `db` not `postgres` in docker-compose
   - Update any scripts referencing `postgres` to use `db`

3. **Vite environment types**: Must create `src/vite-env.d.ts` with:
   ```typescript
   /// <reference types="vite/client" />
   interface ImportMetaEnv {
     readonly VITE_API_URL: string
   }
   ```

4. **shadcn/ui setup**: Using CSS variables in `index.css` for theming
   - Light/dark mode via `.dark` class on root element

5. **sonner for toasts**: Added as dependency (not in original package.json)
   - Import `Toaster` from 'sonner' in App.tsx

6. **File upload validation**: Backend validates by extension + MIME type
   - PDF, DOCX, DOC, TXT supported
   - Size limit configurable in settings

**Lessons Learned:**

| Issue | Solution |
|-------|----------|
| Docker Compose `version` attribute deprecated | Remove it, not needed in modern Docker |
| Frontend port should be 5173 for Vite dev | Update docker-compose and start.sh |
| `import.meta.env` TypeScript error | Add vite-env.d.ts with reference types |
| Missing sonner package | Add to package.json dependencies |

**Next Steps:**
1. ~~Test with Docker when available~~ ✅
2. ~~Add document processing worker (Celery task)~~ ✅
3. Implement WebSocket for real-time updates
4. ~~Add LLM integration layer~~ ✅

---

### Session: RAG Chat Implementation (January 2026)

**What happened:**
- Added complete RAG pipeline: embeddings, vector search, chat
- Document processing now generates embeddings
- Chat UI with conversation history

**New Services:**

| Service | File | Description |
|---------|------|-------------|
| EmbeddingService | `services/embeddings.py` | OpenAI embeddings (768-dim) |
| SearchService | `services/search.py` | pgvector cosine similarity search |
| ChatService | `services/chat.py` | RAG chat with Claude/OpenAI |

**API Endpoints:**
- `POST /api/chat` - Chat with RAG context
- `POST /api/chat/stream` - Streaming chat
- `POST /api/chat/search` - Semantic document search

**Environment Variables Required:**
- `ANTHROPIC_API_KEY` - For Claude chat
- `OPENAI_API_KEY` - For embeddings + GPT fallback

**Key Implementation Details:**
1. Embeddings use `text-embedding-3-small` with 768 dims (matches pgvector schema)
2. Search uses cosine distance: `1 - (embedding <=> query_embedding)`
3. Chat context limited to ~4000 tokens to leave room for response
4. Streaming supported for both Claude and OpenAI

---

*Last updated: January 2026 (v1.4)*
*Generated from Claude.ai + Claude Code sessions*

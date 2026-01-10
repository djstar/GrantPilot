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
12. ✅ Development Phases (**Split Phase 1 into 1a/1b**)
- ✅ Appendix D: Offline/Sync Strategy
- ✅ Appendix E: Security Considerations
- ✅ Appendix F: Error Recovery & Crash Handling

### 🔲 Remaining TODO
- **Section 9:** Agent Prompt Templates ← **NEXT PRIORITY**
- **Section 10:** Workflow Diagrams
- **Section 11:** UI Wireframes
- Testing Strategy
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

*Last updated: January 2025 (v1.2)*
*Generated from Claude.ai + Claude Code sessions*

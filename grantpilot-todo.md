# GrantPilot Development TODO Tracker

**Last Updated:** January 2025 (v1.2)

---

## Specification Status

### ✅ Completed Sections

| Section | Status | Notes |
|---------|--------|-------|
| 1. Executive Summary | ✅ Complete | Vision, differentiators, target user |
| 2. Vision & Value Proposition | ✅ Complete | Problem/solution, success metrics |
| 3. User Experience & Interface | ✅ Complete | 3 modes, info arch, **+ Confidence indicators (3.6)** |
| 4. Multi-Agent Architecture | ✅ Complete | 6 agents, **+ Orchestrator collaboration protocol (4.2)** |
| 5. Self-Learning RAG System | ✅ Complete | Architecture, **+ Style confidence tiers (5.2), ReadCube fallbacks (5.3), Feedback parser templates (5.5), Advanced Self-Learning (5.6)** |
| 6. Technical Stack | ✅ Complete | Full stack defined |
| 7. Database Schema | ✅ Complete | PostgreSQL with pgvector, all tables |
| 8. API Contracts | ✅ Complete | 70+ endpoints, WebSocket events, TypeScript types |
| 9. Agent Prompt Templates | ✅ Complete | 36 Jinja2 templates for all agents |
| 10. Workflow Diagrams | ✅ Complete | 4 user journeys + 5 system flows |
| 12. Development Phases | ✅ Complete | **Split Phase 1 into 1a/1b** for faster iteration |
| Appendix D | ✅ Complete | Offline/Sync Strategy |
| Appendix E | ✅ Complete | Security Considerations |
| Appendix F | ✅ Complete | Error Recovery & Crash Handling |

### 🔲 TODO Sections

| Section | Priority | Dependencies |
|---------|----------|--------------|
| ~~9. Agent Prompt Templates~~ | ~~HIGH~~ | ✅ COMPLETE |
| ~~10. Workflow Diagrams~~ | ~~MEDIUM~~ | ✅ COMPLETE |
| 11. UI Wireframes | **NEXT** | Section 3 |
| Testing Strategy | LOW | All sections |
| Deployment Guide | LOW | Section 6 |

---

## Detailed TODO Items

### ~~Section 8: API Contracts~~ ✅ COMPLETE

**Completed on:** January 2025
**File:** `grantpilot-api-contracts.md`
**Contents:**
- ✅ 70+ REST endpoints defined with request/response schemas
- ✅ Projects API (11 endpoints)
- ✅ Documents API (8 endpoints)
- ✅ RFAs API (8 endpoints)
- ✅ Agents API (10 endpoints)
- ✅ Chat API (4 endpoints)
- ✅ Knowledge Base API (7 endpoints)
- ✅ References API (5 endpoints)
- ✅ Settings API (12 endpoints)
- ✅ WebSocket events (12 event types)
- ✅ Error codes reference (20+ error codes)
- ✅ TypeScript type definitions

---

### ~~Section 9: Agent Prompt Templates~~ ✅ COMPLETE

**Completed on:** January 2025
**File:** `grantpilot-agent-prompts.md`
**Contents:**
- ✅ Research Agent (6 prompts): web search, NIH Reporter, PubMed, prior awardee, competitive landscape, summarization
- ✅ Writing Agent (9 prompts): Specific Aims, Significance, Innovation, Approach, style calibration, anti-LLM, reviewer critique, persuasion, tone
- ✅ Compliance Agent (6 prompts): RFA parsing, requirements, hidden priorities, format check, content check, pre-submission audit
- ✅ Creative Agent (4 prompts): figure concepts, DALL-E prompts, diagram specs, style consistency
- ✅ Analysis Agent (4 prompts): figure interpretation, data synthesis, literature gaps, grant strategy
- ✅ Learning Agent (4 prompts): feedback parsing, pattern extraction, style profile, success factors
- ✅ Orchestrator (3 prompts): task routing, collaboration handling, result merging
- ✅ Shared components: error handling, confidence framework, citation formatting

---

### ~~Section 10: Workflow Diagrams~~ ✅ COMPLETE

**Completed on:** January 2025
**Location:** `grantpilot-specification.md` Section 10

**User Journey Maps:**
- [x] New user onboarding flow (10.1.1)
- [x] Create new project flow (10.1.2)
- [x] Agent mode task flow (10.1.3)
- [x] Co-pilot mode interaction flow (10.1.4)

**System Flows:**
- [x] Document ingestion pipeline (10.2.1)
- [x] Agent orchestration flow (10.2.2)
- [x] RAG retrieval flow (10.2.3)
- [x] Self-learning feedback loop (10.2.4)
- [x] Submission tracking & review flow (10.2.5)

---

### Section 11: UI Wireframes

**Screens to Design:**
- [ ] Dashboard / Home
- [ ] Project list view
- [ ] Project detail view
- [ ] Agent mode panel
- [ ] Co-pilot mode (split view)
- [ ] Document viewer
- [ ] RFA analysis view
- [ ] Compliance checker (with confidence indicators)
- [ ] Knowledge base manager
- [ ] Settings / Configuration
- [ ] Cost tracking dashboard
- [ ] Review & Learn mode
- [ ] Sync conflict resolution dialog
- [ ] Style confidence display

---

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| Jan 2025 | Local Server + Browser deployment | Simpler development, better debugging, Docker-friendly |
| Jan 2025 | PostgreSQL with pgvector | Robust, complex queries, vector search in single DB |
| Jan 2025 | React + FastAPI stack | Modern, well-supported, good async support |
| Jan 2025 | Anthropic/OpenAI primary, Ollama fallback | Best quality with offline option |
| Jan 2025 | PMID priority for citations | User preference, PubMed-indexed literature |
| Jan 2025 | **Dynamic agent collaboration via orchestrator** | Maintains visibility and cost control while enabling agent-to-agent handoffs |
| Jan 2025 | **10+ documents for confident style learning** | With auto-weighting based on funding outcomes and recency |
| Jan 2025 | **ReadCube primary, RIS/BibTeX/PMID fallback** | ReadCube API may be limited; file-based import ensures reliability |
| Jan 2025 | **Full funder-specific feedback parser templates** | NIH structured, NSF semi-structured, Foundation/generic NLP-based |
| Jan 2025 | **Confidence indicators everywhere** | Transparency builds trust; shows when to verify AI output |
| Jan 2025 | **Split Phase 1 into 1a (core) + 1b (agents)** | Faster time to usable product, iterative development |
| Jan 2025 | **Balanced anti-LLM detection** | Flag obvious AI patterns, but allow common scientific phrasing |
| Jan 2025 | **Soft budget warnings** | Complete current task, block new tasks when budget exceeded |

---

## Open Questions

1. ~~**ReadCube Integration:** What API access is available?~~ → Fallback strategy defined (RIS/BibTeX)
2. **NIH Reporter Rate Limits:** What are the constraints for bulk queries?
3. **Ollama Model Selection:** Which models work best for grant writing?
4. ~~**Backup Location:** Confirm Dropbox path structure.~~ → Offline/sync strategy defined

---

## Next Session Agenda

1. ~~Define API contracts (Section 8)~~ ✅ DONE
2. ~~Spec improvements (orchestrator, confidence, security, etc.)~~ ✅ DONE
3. ~~Create agent prompt templates (Section 9)~~ ✅ DONE
4. Design workflow diagrams (Section 10) ← **NEXT**
5. Create UI wireframes (Section 11)

---

## Session Log

### Session: January 2025 (Spec Refinement)

**Completed:**
- Added orchestrator collaboration protocol (Section 4.2)
- Added style learning confidence tiers with auto-weighting (Section 5.2)
- Updated reference management with RIS/BibTeX/PMID fallback (Section 5.3)
- Added reviewer feedback parser templates for multiple funders (Section 5.5)
- Added system-wide confidence indicators (Section 3.6)
- Split Phase 1 into 1a (Core Foundation) and 1b (Agent Foundation)
- Added Appendix D: Offline/Sync Strategy
- Added Appendix E: Security Considerations
- Added Appendix F: Error Recovery & Crash Handling

**Key Decisions Made:**
- Orchestrator-mediated agent collaboration (not autonomous)
- Auto-weighting for style corpus (funded grants weighted 2x)
- Balanced anti-LLM detection
- Soft budget warnings (complete task, block new)
- Full parser template system for feedback

---

### Session: January 2025 (Advanced Self-Learning)

**Completed:**
- Added Section 5.6: Advanced Self-Learning Architecture
- Specified pretrained models to leverage (SPECTER2, PubMedBERT, SciBERT, BioMistral 2, PMC-LLaMA)
- Designed LoRA/PEFT fine-tuning strategy for style adapters, classifiers, critique extractors
- Added agent performance tracking system
- Designed prompt evolution system with A/B testing and outcome correlation
- Added proactive knowledge expansion (literature monitoring, funder intelligence, gap analysis)
- Created 5 new database tables: `agent_performance`, `prompt_versions`, `knowledge_suggestions`, `finetune_jobs`, `literature_monitors`
- Updated HANDOFF.md with ML model decisions
- Updated Creative Agent prompts for Nano Banana API as primary image generation

**Key Decisions Made:**
- SPECTER2 for scientific embeddings (task-specific adapters)
- PubMedBERT for biomedical RAG retrieval
- QLoRA for fine-tuning (runs on consumer hardware)
- Prompt versioning with A/B testing
- Automated literature and funder monitoring
- Nano Banana API as primary image generation backend

**Models Selected:**
| Purpose | Model | Source |
|---------|-------|--------|
| Scientific embeddings | SPECTER2 | allenai/specter2 (HuggingFace) |
| Biomedical embeddings | PubMedBERT | NeuML/pubmedbert-base-embeddings |
| General scientific | SciBERT | allenai/scibert |
| Offline LLM | BioMistral 2 / PMC-LLaMA | Open-source |
| Fine-tuning | HuggingFace PEFT | LoRA/QLoRA |

---

*This file should be updated after each working session*

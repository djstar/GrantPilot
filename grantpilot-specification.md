# GrantPilot: AI-Powered Grant Writing Co-Pilot

## Complete Technical Specification

**Version:** 1.0  
**Last Updated:** January 2025  
**Status:** In Development  

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Vision & Core Value Proposition](#2-vision--core-value-proposition)
3. [User Experience & Interface Model](#3-user-experience--interface-model)
4. [Multi-Agent Architecture](#4-multi-agent-architecture)
5. [Self-Learning RAG System](#5-self-learning-rag-system)
6. [Technical Stack](#6-technical-stack)
7. [Database Schema](#7-database-schema)
8. [API Contracts](#8-api-contracts)
9. [Agent Prompt Templates](#9-agent-prompt-templates)
10. [Workflow Diagrams](#10-workflow-diagrams)
11. [UI Wireframes](#11-ui-wireframes)
12. [Development Phases](#12-development-phases)
13. [Appendices](#13-appendices)

---

## 1. Executive Summary

### 1.1 What is GrantPilot?

GrantPilot is an AI-powered grant writing assistant that functions as both a **co-pilot** (interactive collaboration) and **agent** (autonomous research/tasks), with continuous learning from user feedback and outcomes. It is designed specifically for biomedical/life science researchers working with NIH, NSF, DOD, and foundation grants.

### 1.2 Key Differentiators

| Feature | Description |
|---------|-------------|
| **Institutional Memory** | Learns from your specific grant history, successes, failures, and reviewer feedback |
| **RFA Intelligence** | Deeply parses funding announcements to understand explicit requirements AND implicit preferences |
| **Research Integration** | Ingests and synthesizes your manuscripts, preliminary data, and research context |
| **Agentic Research** | Autonomously investigates funders, prior awardees, trends, and competitive landscape |
| **Voice Matching** | Learns your writing style and ensures output doesn't sound like AI-generated text |
| **Compliance Automation** | Real-time format checking and requirement validation |

### 1.3 Target User Profile

- **Domain:** Biomedical/life sciences with AI, tech bio, computational, translational, systems biology/immunology focus
- **Grant Types:** NIH (R01, R21, K-awards), NSF, DOD, foundation grants
- **Usage:** Solo researcher on single laptop
- **Current Workflow:** Word documents, Dropbox folder organization, ReadCube for references

---

## 2. Vision & Core Value Proposition

### 2.1 Problem Statement

Grant writing is a time-intensive, high-stakes process where:
- Researchers spend 25-40% of their time writing grants
- Success rates are typically 10-25%
- Knowledge from previous submissions (especially reviewer feedback) is often lost
- RFA requirements are complex and easy to miss
- Competitive landscape research is manual and incomplete

### 2.2 Solution

GrantPilot addresses these challenges by:

1. **Reducing time spent on research** — Autonomous agents gather competitive intelligence, analyze prior awardees, and synthesize literature

2. **Improving quality through learning** — System learns from your successful grants, reviewer feedback, and iterates to improve

3. **Ensuring compliance** — Automated checking of all RFA requirements, formats, and implicit preferences

4. **Maintaining your voice** — AI output is calibrated to match your writing style, not generic LLM output

5. **Building institutional memory** — All grants, reviews, and outcomes are tracked and analyzed for patterns

### 2.3 Success Metrics

- Reduction in grant preparation time
- Improvement in compliance (fewer desk rejections)
- Improvement in review scores over iterations
- User satisfaction with AI-generated content quality

---

## 3. User Experience & Interface Model

### 3.1 Deployment Model

**Local Server + Browser** architecture:
- Python FastAPI server running locally
- React web application accessed via `http://localhost:3000`
- PostgreSQL database for persistent storage
- Docker containerization for easy setup

```
┌─────────────────────────────────────────────────────────────────────────────┐
│   Your Laptop                                                               │
│   ┌─────────────────────────────┐                                           │
│   │   Your Browser              │                                           │
│   │   (Chrome/Firefox/Safari)   │                                           │
│   │   http://localhost:3000     │                                           │
│   └──────────────┬──────────────┘                                           │
│                  │ HTTP/WebSocket                                           │
│                  ▼                                                          │
│   ┌─────────────────────────────┐                                           │
│   │   GrantPilot Server         │                                           │
│   │   (Python/FastAPI)          │                                           │
│   └──────────────┬──────────────┘                                           │
│                  ▼                                                          │
│   ┌─────────────────────────────────────────────────────────────┐           │
│   │  PostgreSQL Database    │    Your Dropbox/Files             │           │
│   └─────────────────────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Startup Flow:**
1. Double-click "Start GrantPilot" script
2. Script starts Docker containers (server, database, Redis)
3. Browser automatically opens to localhost:3000

### 3.2 Three Primary Modes

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 🧬 GrantPilot                              [Projects ▾]  [Knowledge]  [⚙️]  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Mode Toggle:  [ 🤖 Agent ]  [ 👤 Co-pilot ]  [ 📝 Review & Learn ]         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 3.2.1 Agent Mode (Autonomous Research & Implementation)

For autonomous tasks like research, drafting, and analysis.

**Key Features:**
- **Mission Definition:** Natural language task description
- **Time/Depth Caps:** User-configurable limits (e.g., "2 hours", "comprehensive")
- **Source Scoping:** Checkbox control over what the agent can access
- **Mid-Run Injection:** Add context, redirect, or upload new docs while running
- **Live Activity Feed:** See reasoning and progress in real-time
- **Pause/Stop with Save:** Never lose work

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 🤖 AGENT MODE                                          R01-Cancer-2024      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ ┌─ Mission Definition ─────────────────────────────────────────────────────┐│
│ │                                                                          ││
│ │ Task: [Research competitive landscape and draft Significance section   ] ││
│ │                                                                          ││
│ │ ┌─ Constraints ────────────────────────────────────────────────────────┐ ││
│ │ │ ⏱️ Time cap:    [2 hours ▾]     🔍 Depth:    [Comprehensive ▾]       │ ││
│ │ │                                                                      │ ││
│ │ │ 📂 Scope to these sources:                                           │ ││
│ │ │ ☑ My manuscripts (folder: /Dropbox/Papers/2023-2024)                 │ ││
│ │ │ ☑ This RFA: NIH-RFA-CA-24-001                                        │ ││
│ │ │ ☑ NIH Reporter (prior awards)                                        │ ││
│ │ │ ☐ PubMed (recent literature)                                         │ ││
│ │ │ ☐ Example grants (my knowledge base)                                 │ ││
│ │ │ ☑ Web search (general)                                               │ ││
│ │ └──────────────────────────────────────────────────────────────────────┘ ││
│ │                                                                          ││
│ │ [▶ Launch Agent]                                                         ││
│ └──────────────────────────────────────────────────────────────────────────┘│
│                                                                             │
│ ┌─ Agent Activity (Live) ──────────────────────────────────────────────────┐│
│ │                                                                          ││
│ │ 14:23:01  🔍 Parsing RFA for significance criteria...                    ││
│ │ 14:23:15  ✓  Found 8 key evaluation points for significance              ││
│ │ 14:23:18  🔍 Querying NIH Reporter for R01s in CAR-T space...            ││
│ │ 14:24:02  ✓  Found 34 funded grants (2021-2024)                          ││
│ │ 14:24:05  📄 Analyzing your manuscript: "CAR-T_tumor_micro_2024.pdf"     ││
│ │ 14:24:30  💡 Found strong preliminary data aligns with RFA priority      ││
│ │ 14:24:45  🔍 Researching top 5 funded PIs in this space...               ││
│ │                                                                          ││
│ │ ┌─ Inject Context (add info mid-run) ──────────────────────────────────┐ ││
│ │ │ [Type additional guidance or upload document...]              [Send] │ ││
│ │ └──────────────────────────────────────────────────────────────────────┘ ││
│ │                                                                          ││
│ │           [⏸ Pause]  [🛑 Stop & Save Progress]  [📊 View Interim]        ││
│ └──────────────────────────────────────────────────────────────────────────┘│
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 3.2.2 Co-pilot Mode (Interactive Collaboration)

For interactive drafting, editing, and refinement.

**Key Features:**
- **Split View:** Document + chat side-by-side
- **Proactive Alerts:** AI notices things without you asking
- **Word Export:** Clean export for Word workflow
- **Version History:** Track iterations
- **Inline AI Annotations:** Suggestions directly in document context

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 👤 CO-PILOT MODE                                       R01-Cancer-2024      │
├───────────────────────────────────┬─────────────────────────────────────────┤
│                                   │                                         │
│  📄 Document Workspace            │  💬 Co-pilot Chat                       │
│  ───────────────────────          │  ─────────────────                      │
│                                   │                                         │
│  [Specific Aims ▾] v3 - Draft     │  🤖 I notice your Aim 2 doesn't         │
│                                   │     reference the preliminary data      │
│  ┌─────────────────────────────┐  │     from your 2024 paper. The RFA       │
│  │                             │  │     emphasizes "strong rationale" —     │
│  │  [Document content with     │  │     adding Fig 3 data here would        │
│  │   inline suggestions,       │  │     strengthen this significantly.      │
│  │   highlights, and           │  │                                         │
│  │   margin comments from AI]  │  │  ─────────────────────────────────      │
│  │                             │  │                                         │
│  └─────────────────────────────┘  │  You: Can you show me how other         │
│                                   │       funded grants positioned          │
│  [Export to Word]  [Version Hx]   │       similar preliminary data?         │
│                                   │                                         │
├───────────────────────────────────┴─────────────────────────────────────────┤
│ 📊 Proactive Alerts                                            [Dismiss All]│
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ ⚠️ Deadline in 18 days │ 🔍 New R01 in your area posted │ ✓ Compliant   │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 3.2.3 Review & Learn Mode (Phase 3 Feature)

For ingesting feedback and tracking patterns across submissions.

**Key Features:**
- **Submission Tracker:** Track all submissions and outcomes
- **Feedback Ingestion:** Parse and analyze reviewer comments
- **Pattern Discovery:** AI identifies trends across your submissions
- **Iteration Comparison:** Compare versions to see what improved

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 📝 REVIEW & LEARN MODE                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ ┌─ Submission Tracker ─────────────────────────────────────────────────────┐│
│ │ Grant              │ Submitted │ Outcome   │ Score │ Iteration │ Learned ││
│ │────────────────────│───────────│───────────│───────│───────────│─────────││
│ │ R01-Cancer-2024    │ Mar 2024  │ Pending   │ —     │ 1st       │ —       ││
│ │ R01-Cancer-2023    │ Mar 2023  │ Not Fund  │ 32    │ 2nd       │ ✓       ││
│ │ R21-Pilot-2023     │ Jun 2023  │ Funded    │ 18    │ 1st       │ ✓       ││
│ └──────────────────────────────────────────────────────────────────────────┘│
│                                                                             │
│ ┌─ AI-Discovered Patterns ─────────────────────────────────────────────────┐│
│ │                                                                          ││
│ │ From your 8 submissions, I've identified:                                ││
│ │                                                                          ││
│ │ ✓ Strengths: Innovation sections score consistently well                 ││
│ │ ⚠ Pattern: Feasibility concerns raised in 5/8 reviews                    ││
│ │   → Recommendation: Add more timeline detail, preliminary data           ││
│ │                                                                          ││
│ └──────────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.3 Information Architecture

```
GrantPilot
├── 🗂️ Projects (individual grant applications)
│   ├── R01-Cancer-2024
│   │   ├── RFA (linked)
│   │   ├── Drafts (versioned)
│   │   ├── Supporting docs (biosketches, letters, etc.)
│   │   ├── Research notes (agent outputs)
│   │   └── Submission history (reviews, scores, iterations)
│   └── ...
│
├── 📋 RFA Library (parsed funding announcements)
│   ├── Active RFAs (with deadlines)
│   └── Archived RFAs (for pattern analysis)
│
├── 📚 Knowledge Base (institutional memory)
│   ├── My Papers & Manuscripts
│   ├── Example Grants (good/bad, annotated)
│   ├── Reviewer Feedback History
│   ├── Funder Intelligence (patterns, preferences)
│   └── Writing Style References
│
└── ⚙️ Configuration
    ├── LLM settings (API keys, model preferences)
    ├── User profile (institution, field, CV)
    ├── Budget limits per project
    └── Templates & defaults
```

### 3.4 Intelligent Document Ingestion

The system watches designated folders and automatically:
- Detects document types (aims, biosketches, RFAs, figures, reviews)
- Groups related files into projects
- Extracts text, figures, tables for AI analysis
- Identifies submission iterations (v1, v2, resubmission)
- Links reviews to corresponding submissions
- Re-indexes on file changes

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 📂 KNOWLEDGE BASE — Document Ingestion                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ ┌─ Connect Local Folders ──────────────────────────────────────────────────┐│
│ │                                                                          ││
│ │ Watched Folders:                                                         ││
│ │ ┌──────────────────────────────────────────────────────────────────────┐ ││
│ │ │ 📁 /Dropbox/Grants/                                    [Scan Now]    │ ││
│ │ │    Last scan: 2 hours ago | 47 documents | 12 projects detected      │ ││
│ │ └──────────────────────────────────────────────────────────────────────┘ ││
│ │                                                                          ││
│ │ [+ Add Folder]                                                           ││
│ └──────────────────────────────────────────────────────────────────────────┘│
│                                                                             │
│ ┌─ Auto-Detected Structure ────────────────────────────────────────────────┐│
│ │                                                                          ││
│ │ 📁 R01_Cancer_2024/                     → Classified as: Grant Project   ││
│ │    ├─ Specific_Aims_v3.docx             → Specific Aims (draft)          ││
│ │    ├─ Research_Strategy_v2.docx         → Research Strategy (draft)      ││
│ │    ├─ Biosketch_Smith.pdf               → Biosketch                      ││
│ │    ├─ Budget_justification.xlsx         → Budget                         ││
│ │    ├─ Preliminary_data/                 → Figures/Data folder            ││
│ │    │   └─ Fig1_western_blot.png         → Figure (experimental)          ││
│ │    ├─ RFA_NIH-CA-24-001.pdf             → RFA document                   ││
│ │    └─ Reviews_2023/                     → Previous submission feedback   ││
│ │        └─ Summary_statement.pdf         → Reviewer comments              ││
│ │                                                                          ││
│ │ [✓ Accept Classification]  [✏️ Edit]  [Ignore this folder]               ││
│ └──────────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.5 Interaction Style

- **Both Pull and Push:** User can ask specific questions AND AI proactively suggests/warns
- **Full Agent Autonomy:** Agents run autonomously with ability to inject details mid-run
- **Configurable Constraints:** Time caps, depth levels, source scoping
- **In-App Notifications Only:** No email or desktop notifications

### 3.6 Confidence Indicators (System-Wide Transparency)

GrantPilot displays confidence scores for all AI-driven inferences, helping users know when to trust vs. verify outputs:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CONFIDENCE INDICATOR SYSTEM                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  DISPLAY FORMAT                                                             │
│  ══════════════                                                             │
│                                                                             │
│  ✓ High (85-100%)    Green checkmark     Trust this inference               │
│  ◐ Medium (60-84%)   Yellow half-circle  Review recommended                 │
│  ○ Low (< 60%)       Gray circle         Manual verification needed         │
│                                                                             │
│  AREAS WITH CONFIDENCE DISPLAY                                              │
│  ══════════════════════════════                                             │
│                                                                             │
│  Document Classification:                                                   │
│  ┌────────────────────────────────────────────────────────────────┐        │
│  │ 📄 new_paper_2024.pdf                                          │        │
│  │    Type: Manuscript ✓ (94%)                                    │        │
│  │    Auto-detected from: Title page, abstract structure          │        │
│  └────────────────────────────────────────────────────────────────┘        │
│                                                                             │
│  RFA Priority Inference:                                                    │
│  ┌────────────────────────────────────────────────────────────────┐        │
│  │ 🎯 Inferred Priority: "Health Disparities"                     │        │
│  │    Confidence: ✓ High (mentioned 12x in RFA)                   │        │
│  │    Your draft mentions: 2x → Recommendation: Expand            │        │
│  └────────────────────────────────────────────────────────────────┘        │
│                                                                             │
│  Style Match:                                                               │
│  ┌────────────────────────────────────────────────────────────────┐        │
│  │ ✍️ Style Match Score: 78% ◐                                    │        │
│  │    Voice alignment: Good                                       │        │
│  │    Technical depth: Slightly lower than your samples           │        │
│  │    [Adjust] [See comparison]                                   │        │
│  └────────────────────────────────────────────────────────────────┘        │
│                                                                             │
│  Compliance Check:                                                          │
│  ┌────────────────────────────────────────────────────────────────┐        │
│  │ ✅ Page limit: 0.95/1.0 pages ✓ (exact measurement)            │        │
│  │ ⚠️ Innovation points: 2 of 3 addressed ◐ (NLP detection)       │        │
│  │ ❓ Timeline present: ○ Low confidence (couldn't locate)        │        │
│  └────────────────────────────────────────────────────────────────┘        │
│                                                                             │
│  Research Agent Findings:                                                   │
│  ┌────────────────────────────────────────────────────────────────┐        │
│  │ 🔬 "47 grants found in CAR-T space" ✓ (NIH Reporter query)     │        │
│  │ 🔬 "Gap identified: TME focus" ◐ (inferred from abstracts)     │        │
│  │ 🔬 "Top competitor: Dr. Smith" ○ (limited data, verify)        │        │
│  └────────────────────────────────────────────────────────────────┘        │
│                                                                             │
│  Anti-LLM Detection:                                                        │
│  ┌────────────────────────────────────────────────────────────────┐        │
│  │ 🤖 "It's important to note" flagged ✓ (known AI pattern)       │        │
│  │ 🤖 "multifaceted approach" flagged ◐ (sometimes legitimate)    │        │
│  │    [Keep] [Rephrase] [Add to allowlist]                        │        │
│  └────────────────────────────────────────────────────────────────┘        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Confidence Sources:**

| Inference Type | How Confidence is Calculated |
|----------------|------------------------------|
| **Document classification** | ML model probability + heuristic signals (file structure, keywords) |
| **RFA priorities** | Keyword frequency + context analysis + comparison to funded grants |
| **Style match** | Embedding similarity to corpus + feature comparison (vocab, structure) |
| **Compliance (format)** | Exact measurement (page count, word count) = High confidence |
| **Compliance (content)** | NLP detection of required topics = Medium confidence |
| **Research findings** | Source reliability × extraction method (API = High, scraping = Medium) |
| **Anti-LLM detection** | Pattern match strength + false positive history |

**User Controls:**

- **Hide low-confidence items:** Option to only show high-confidence results
- **Threshold adjustment:** User can set minimum confidence for auto-actions
- **Feedback loop:** User corrections improve future confidence calibration

---

## 4. Multi-Agent Architecture

### 4.1 Agent System Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           GRANTPILOT AGENT SYSTEM                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐    ┌─────────────────────────────────────────────────┐     │
│  │             │    │              ORCHESTRATOR                       │     │
│  │    USER     │◄──►│  (Routes tasks, manages agent collaboration)    │     │
│  │             │    │                                                 │     │
│  └─────────────┘    └─────────────────────────────────────────────────┘     │
│                                        │                                    │
│         ┌──────────────────────────────┼──────────────────────────────┐     │
│         ▼                              ▼                              ▼     │
│  ┌─────────────┐                ┌─────────────┐                ┌─────────────┐
│  │ 🔬 RESEARCH │                │ ✍️ WRITING  │                │ ✅ COMPLIANCE│
│  │    AGENT    │                │    AGENT    │                │    AGENT    │
│  └─────────────┘                └─────────────┘                └─────────────┘
│         │                              │                              │     │
│         ▼                              ▼                              ▼     │
│  ┌─────────────┐                ┌─────────────┐                ┌─────────────┐
│  │ 🎨 CREATIVE │                │ 📊 ANALYSIS │                │ 🧠 LEARNING │
│  │    AGENT    │                │    AGENT    │                │    AGENT    │
│  └─────────────┘                └─────────────┘                └─────────────┘
│         │                              │                              │     │
│         └──────────────────────────────┼──────────────────────────────┘     │
│                                        ▼                                    │
│                     ┌─────────────────────────────────────┐                 │
│                     │      📚 KNOWLEDGE BASE (RAG)        │                 │
│                     └─────────────────────────────────────┘                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Orchestrator Collaboration Protocol

Agents collaborate dynamically through the orchestrator, which provides visibility, cost control, and context management.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    AGENT COLLABORATION PROTOCOL                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. COLLABORATION REQUEST                                                   │
│     ─────────────────────                                                   │
│     Agent A (e.g., Writing) identifies need for help:                       │
│     → "I need competitive landscape data to strengthen this section"        │
│     → Sends structured request to Orchestrator                              │
│                                                                             │
│  2. ORCHESTRATOR VALIDATION                                                 │
│     ────────────────────────                                                │
│     Orchestrator checks:                                                    │
│     → Budget availability (will this exceed project/global limits?)         │
│     → Permission scope (is Research Agent enabled for this task?)           │
│     → Context relevance (does request align with original mission?)         │
│     → Priority queue (are other urgent tasks waiting?)                      │
│                                                                             │
│  3. CONTEXT SUMMARIZATION                                                   │
│     ──────────────────────                                                  │
│     Orchestrator prepares context for Agent B:                              │
│     → Task summary (not full history—reduces tokens/cost)                   │
│     → Relevant constraints from original task                               │
│     → Specific deliverable expected                                         │
│     → Time/depth limits for sub-task                                        │
│                                                                             │
│  4. SUB-TASK EXECUTION                                                      │
│     ────────────────────                                                    │
│     Agent B (e.g., Research) executes with:                                 │
│     → Awareness it's a collaboration (not standalone task)                  │
│     → Focused scope (answer the specific question, not full research)       │
│     → Cost attributed to parent task                                        │
│                                                                             │
│  5. RESULT MERGE                                                            │
│     ────────────                                                            │
│     Orchestrator receives Agent B result:                                   │
│     → Validates output quality/relevance                                    │
│     → Summarizes if needed (avoid context bloat)                            │
│     → Injects into Agent A's context                                        │
│     → Logs collaboration for audit trail                                    │
│                                                                             │
│  6. CONTINUATION                                                            │
│     ────────────                                                            │
│     Agent A resumes with enriched context:                                  │
│     → Can request additional collaborations if needed                       │
│     → Orchestrator tracks cumulative cost/time                              │
│     → User can view collaboration chain in activity log                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Collaboration Rules:**

| Rule | Description |
|------|-------------|
| **Budget Inheritance** | Sub-tasks draw from parent task's budget. If parent has $5 remaining, sub-task cannot exceed $5. |
| **Depth Limits** | Max 3 levels of collaboration (A→B→C). Prevents runaway recursion. |
| **Timeout Propagation** | If parent has 30 min remaining, sub-task gets proportional time (e.g., 10 min). |
| **Context Compression** | Sub-task results are summarized before injection. Full details available in logs. |
| **User Visibility** | All collaborations appear in activity feed with clear "Agent X requested help from Agent Y" entries. |
| **Abort Cascade** | If user pauses/cancels parent, all active sub-tasks are also paused/cancelled. |

### 4.3 Agent Specifications

#### 4.3.1 Research Agent 🔬

**Purpose:** Autonomous information gathering from internal and external sources

```yaml
Research Agent:
  capabilities:
    - Web search (general internet)
    - NIH Reporter queries (funded grants, abstracts, PIs)
    - NSF Award Search
    - PubMed/literature search
    - arXiv/bioRxiv for preprints
    - Funder website scraping (program announcements, priorities)
    - Prior awardee deep-dives (publications, lab websites, collaborators)
    
  outputs:
    - Competitive landscape reports
    - Funder preference analysis
    - Literature synthesis
    - Gap analysis (what's funded vs. not)
    - Key PI/competitor profiles
    
  constraints:
    - Time limits (user-defined)
    - Source scoping (user-defined)
    - Depth levels: Quick scan → Standard → Comprehensive
    
  learning:
    - Remembers which sources were useful for past projects
    - Learns your field's key journals, PIs, conferences
    - Improves search strategies based on feedback
```

#### 4.3.2 Writing Agent ✍️

**Purpose:** Draft, edit, and refine grant text in YOUR voice

```yaml
Writing Agent:
  capabilities:
    - Section drafting (aims, significance, innovation, approach)
    - Collaborative editing with suggestions
    - Tone matching (learns your writing style)
    - Anti-LLM filter (removes AI-sounding phrases)
    - Persuasive writing optimization
    - Reviewer-perspective critique
    
  style_learning:
    source_materials:
      - Your previous successful grants (high weight)
      - Your published papers
      - Your marked "good examples"
      - Your explicit style preferences
      
    learns:
      - Sentence structure patterns
      - Vocabulary preferences
      - How you frame significance
      - Your argumentation style
      - Technical depth level
      - Transition phrases you use
      
    anti_patterns:
      - Detects and removes LLM-typical phrases:
        - "It's important to note that..."
        - "In conclusion..."
        - "This is a multifaceted..."
        - "Delve into..."
        - Excessive hedging
        - Robotic transitions
      - Flags when output sounds too "AI-generated"
      
  tone_controls:
    - Formality slider (casual ↔ formal)
    - Confidence slider (cautious ↔ assertive)  
    - Technical depth (accessible ↔ expert)
    - Field-specific terminology density
```

**Writing Agent UI Controls:**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ ✍️ Writing Agent — Tone & Style Controls                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ Style Profile: [Dr. [Name]'s Voice ▾]          [Edit Profile] [+ New]       │
│                                                                             │
│ ┌─ Tone Sliders ───────────────────────────────────────────────────────────┐│
│ │                                                                          ││
│ │ Formality:      Conversational ○───────●───○ Formal                      ││
│ │ Confidence:     Cautious       ○───────────●─○ Assertive                 ││
│ │ Technical:      Accessible     ○─●─────────○ Expert                      ││
│ │ Conciseness:    Elaborate      ○─────●─────○ Terse                       ││
│ │                                                                          ││
│ └──────────────────────────────────────────────────────────────────────────┘│
│                                                                             │
│ ┌─ Anti-LLM Detection ─────────────────────────────────────────────────────┐│
│ │ ☑ Flag AI-sounding phrases                                               ││
│ │ ☑ Auto-rephrase detected patterns                                        ││
│ │ ☑ Check against your authentic writing samples                           ││
│ │                                                                          ││
│ │ Detected in current draft: 3 phrases flagged  [Review]                   ││
│ └──────────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 4.3.3 Compliance Agent ✅

**Purpose:** Ensure RFA requirements are met, formats are correct, nothing is missed

```yaml
Compliance Agent:
  capabilities:
    rfa_parsing:
      - Extract explicit requirements (page limits, sections, formats)
      - Identify implicit preferences ("emphasis on X" = they want X)
      - Deadline tracking
      - Eligibility criteria
      - Budget constraints
      - Required attachments checklist
      
    format_checking:
      - Page/word limits per section
      - Font, margin, spacing requirements
      - Required headers/sections present
      - Figure/table limits
      - Reference format compliance
      - Biosketch format validation
      
    content_compliance:
      - Required topics addressed
      - Specific aims alignment with RFA priorities
      - Budget justification completeness
      - Human subjects / vertebrate animals sections
      - Data management plan presence
      
    smart_analysis:
      - "Reading between the lines" — what does this funder really want?
      - Cross-reference with funded grants to infer preferences
      - Study section analysis (who reviews, what they like)
      - Success rate analysis for this mechanism
      
  outputs:
    - Interactive compliance checklist
    - Real-time validation warnings
    - Pre-submission audit report
    - Risk assessment (what might reviewers flag)
```

**Compliance Agent UI:**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ ✅ COMPLIANCE CHECK — R01-Cancer-2024                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ RFA: NIH-RFA-CA-24-001    Deadline: March 5, 2025 (18 days)    Score: 78%   │
│                                                                             │
│ ┌─ Requirements Checklist ─────────────────────────────────────────────────┐│
│ │                                                                          ││
│ │ SECTION                    STATUS    REQUIREMENT         YOUR STATUS     ││
│ │ ─────────────────────────────────────────────────────────────────────── ││
│ │ ☑ Specific Aims            PASS      1 page max          0.9 pages       ││
│ │ ☑ Significance             PASS      No limit            2.1 pages       ││
│ │ ⚠️ Innovation               WARN      Must address 3pts   2 of 3 found   ││
│ │ ☐ Timeline                 MISSING   Required            Not found       ││
│ │ ⚠️ Biosketch - PI           WARN      5 pages max         5.1 pages      ││
│ │                                                                          ││
│ └──────────────────────────────────────────────────────────────────────────┘│
│                                                                             │
│ ┌─ RFA Deep Analysis (Reading Between the Lines) ──────────────────────────┐│
│ │                                                                          ││
│ │ 🎯 Inferred Priorities (what they REALLY want):                          ││
│ │                                                                          ││
│ │ • "Health disparities" mentioned 12x — HIGH PRIORITY                     ││
│ │   → Your draft mentions it 2x. Consider expanding.                       ││
│ │                                                                          ││
│ │ • Based on 23 funded grants under this RFA:                              ││
│ │   → 78% had industry collaborator (you don't — consider?)                ││
│ │                                                                          ││
│ └──────────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 4.3.4 Creative Agent 🎨

**Purpose:** Generate figures, diagrams, schematics for grant applications

```yaml
Creative Agent:
  capabilities:
    figure_generation:
      - Workflow/pipeline diagrams
      - Experimental design schematics  
      - Timeline/Gantt charts
      - Conceptual model illustrations
      - Mechanism diagrams
      - Data visualization suggestions
      
    backends:
      - Nano Banana API — primary (better for scientific illustrations)
      - DALL-E 3 (OpenAI) — fallback
      - Stable Diffusion (local option)
      - Programmatic: matplotlib, plotly, mermaid diagrams
      
    scientific_specific:
      - Cell diagrams
      - Pathway illustrations
      - Study design flowcharts
      - CONSORT diagrams
      - Anatomical schematics
      
  workflow:
    1. User describes need
    2. Agent proposes layout/concept
    3. Generates draft image
    4. Iterative refinement based on feedback
    5. Export in publication-ready format (PNG, SVG, PDF)
    
  style_learning:
    - Learns your preferred figure style from examples
    - Maintains consistent aesthetic across grant
```

#### 4.3.5 Analysis Agent 📊

**Purpose:** Understand and work with your data, figures, and preliminary results

```yaml
Analysis Agent:
  capabilities:
    figure_interpretation:
      - Read and describe figures/images
      - Extract data from charts (approximate values)
      - Identify what figures demonstrate
      - Suggest how to present findings
      
    data_analysis:
      - Basic statistical summaries
      - Power analysis suggestions
      - Sample size calculations
      - Identify patterns in preliminary data
      
    literature_analysis:
      - Synthesize findings across papers
      - Identify gaps in literature
      - Compare your approach to published work
      - Citation network analysis
      
    grant_strategy:
      - Analyze competitor funded grants
      - Study section preference analysis
      - Success rate calculations
      - Budget benchmarking
```

#### 4.3.6 Learning Agent 🧠

**Purpose:** Manage self-learning system, pattern extraction, continuous improvement

```yaml
Learning Agent:
  responsibilities:
    feedback_ingestion:
      - Parse reviewer comments (summary statements)
      - Extract specific critiques and map to grant sections
      - Identify patterns across multiple reviews
      - Track submission → outcome correlations
      
    pattern_extraction:
      - What writing patterns correlate with funding?
      - What critique patterns appear repeatedly?
      - What do successful grants in your field look like?
      - How do your funded vs unfunded grants differ?
      
    knowledge_base_curation:
      - Decide what to add to long-term memory
      - Prune outdated information
      - Identify gaps in knowledge base
      - Suggest documents to add
      
    style_model_updates:
      - Continuously refine "your voice" model
      - Incorporate new successful writing samples
      - Adjust based on explicit feedback
      
  triggers:
    - Manual: User adds feedback/documents
    - Automatic: Periodic reanalysis of knowledge base
    - Event-driven: After submission outcome received
```

---

## 5. Self-Learning RAG System

### 5.1 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        KNOWLEDGE BASE ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  DOCUMENT INGESTION                                                         │
│  ══════════════════                                                         │
│                                                                             │
│   📄 Word  📑 PDF  🖼️ Images  📊 Excel  🌐 Web    📁 Folders                │
│      │       │        │         │        │           │                      │
│      └───────┴────────┴─────────┴────────┴───────────┘                      │
│                              │                                              │
│                              ▼                                              │
│                    ┌─────────────────┐                                      │
│                    │   PROCESSOR     │                                      │
│                    │  • OCR          │                                      │
│                    │  • Text extract │                                      │
│                    │  • Image encode │                                      │
│                    │  • Classify     │                                      │
│                    └─────────────────┘                                      │
│                              │                                              │
│                              ▼                                              │
│  VECTOR STORES                                                              │
│  ═════════════                                                              │
│                                                                             │
│  ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐            │
│  │  📚 DOCUMENTS    │ │  🎓 EXAMPLES     │ │  💡 PATTERNS     │            │
│  │                  │ │                  │ │                  │            │
│  │ Your papers      │ │ Good grant       │ │ Learned writing  │            │
│  │ Your grants      │ │ examples         │ │ style vectors    │            │
│  │ RFAs             │ │ Bad examples     │ │                  │            │
│  │ Biosketches      │ │ (annotated)      │ │ Reviewer         │            │
│  │ Letters          │ │                  │ │ critique         │            │
│  │ Figures          │ │ Funded grant     │ │ patterns         │            │
│  │                  │ │ abstracts        │ │                  │            │
│  └──────────────────┘ └──────────────────┘ └──────────────────┘            │
│           │                    │                    │                       │
│           └────────────────────┴────────────────────┘                       │
│                                │                                            │
│                                ▼                                            │
│                    ┌──────────────────────┐                                 │
│                    │   RETRIEVAL ENGINE   │                                 │
│                    │                      │                                 │
│                    │  • Semantic search   │                                 │
│                    │  • Hybrid (keyword + │                                 │
│                    │    vector)           │                                 │
│                    │  • Filtered by type  │                                 │
│                    │  • Recency weighted  │                                 │
│                    └──────────────────────┘                                 │
│                                │                                            │
│                                ▼                                            │
│  LEARNING LAYER                                                             │
│  ══════════════                                                             │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    FEEDBACK LOOP                                    │   │
│  │                                                                     │   │
│  │    ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐     │   │
│  │    │ Submit  │────▶│ Outcome │────▶│ Analyze │────▶│ Update  │     │   │
│  │    │ Grant   │     │ (score/ │     │ What    │     │ Patterns│     │   │
│  │    │         │     │ reviews)│     │ worked? │     │         │     │   │
│  │    └─────────┘     └─────────┘     └─────────┘     └─────────┘     │   │
│  │         ▲                                               │          │   │
│  │         └───────────────────────────────────────────────┘          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  Learning Mechanisms:                                                       │
│  • Style adaptation: Updates "your voice" model with new samples            │
│  • Pattern extraction: Identifies what leads to funding                     │
│  • Critique learning: Remembers reviewer preferences                        │
│  • Proactive expansion: Suggests papers/grants to add                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Style Learning Confidence System

The style model's effectiveness depends on corpus size and quality. GrantPilot displays confidence tiers to set appropriate expectations:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    STYLE CONFIDENCE TIERS                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  TIER 1: INITIALIZING (< 5 documents)                                       │
│  ─────────────────────────────────────                                      │
│  Confidence: 0-40%                                                          │
│  UI Display: "Style profile initializing — output may be generic"           │
│  Behavior:                                                                  │
│  • Uses general scientific writing patterns                                 │
│  • Anti-LLM detection uses generic phrase list                              │
│  • Suggests user add more writing samples                                   │
│  • Displays "Add more documents to improve style matching" prompt           │
│                                                                             │
│  TIER 2: LEARNING (5-10 documents)                                          │
│  ─────────────────────────────────                                          │
│  Confidence: 40-70%                                                         │
│  UI Display: "Style profile established — refining with more samples"       │
│  Behavior:                                                                  │
│  • Identifies basic vocabulary and structure patterns                       │
│  • Can match formality and technical depth                                  │
│  • May miss subtle stylistic preferences                                    │
│  • Displays confidence % with "Good, but can improve" indicator             │
│                                                                             │
│  TIER 3: CONFIDENT (10+ weighted documents)                                 │
│  ──────────────────────────────────────────                                 │
│  Confidence: 70-95%                                                         │
│  UI Display: "Strong style match expected"                                  │
│  Behavior:                                                                  │
│  • Full vocabulary, phrasing, and argumentation matching                    │
│  • Personalized anti-LLM detection (knows YOUR patterns vs AI patterns)     │
│  • Can distinguish between your grant voice vs paper voice                  │
│  • Displays confidence % with "Well-trained" indicator                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Auto-Weighting System:**

Documents are automatically weighted based on quality signals:

| Factor | Weight Multiplier | Rationale |
|--------|-------------------|-----------|
| **Funded grant** | 2.0x | Strongest signal — this worked |
| **Unfunded but scored well** (< 25th percentile) | 1.5x | Good writing, just competitive |
| **Unfunded, poor score** | 0.5x | May contain weak patterns |
| **Published paper** | 1.2x | Peer-reviewed quality |
| **User-marked "exemplar"** | 1.8x | Explicit quality signal |
| **Document age < 2 years** | 1.0x (no decay) | Recent writing |
| **Document age 2-5 years** | 0.8x | Slight decay |
| **Document age > 5 years** | 0.5x | May not reflect current style |

**Confidence Calculation:**

```
confidence = base_score + corpus_bonus + quality_bonus

base_score:
  - < 5 docs: 20%
  - 5-10 docs: 50%
  - 10-20 docs: 70%
  - 20+ docs: 80%

corpus_bonus:
  - Diversity across grant types: +5%
  - Multiple funded examples: +10%
  - Mix of grants and papers: +5%

quality_bonus:
  - Avg document weight > 1.5: +5%
  - User has edited/approved suggestions: +5% (learning from feedback)
```

### 5.3 Reference Management Integration

**Primary: ReadCube Integration with PMID/DOI preference**

**Fallback: File-based import/export (RIS, BibTeX, PMID/DOI lists)**

```yaml
Citation System:
  primary_integration:
    provider: ReadCube Papers
    features:
      - API connection (when available)
      - Import your library
      - Bidirectional sync
      - Collection-level sync
    limitations:
      - ReadCube API access may be restricted
      - Rate limits on sync operations

  fallback_methods:
    ris_bibtex_import:
      - Import from .ris or .bib files
      - Export from ReadCube/Zotero/Mendeley → import to GrantPilot
      - Periodic manual re-sync workflow
      - File watch on designated exports folder

    identifier_files:
      - Upload text file with PMID list (one per line)
      - Upload text file with DOI list
      - Bulk lookup and import

    manual_entry:
      - Paste title → auto-lookup PMID/DOI via PubMed/CrossRef
      - Manual field entry as last resort

  identifier_priority:
    1. PMID (if available — PubMed indexed)
    2. DOI (fallback for non-PubMed)
    3. Manual entry (last resort)

  features:
    - Auto-lookup: Paste title → get PMID/DOI
    - Citation formatting: Auto-format for NIH, NSF styles
    - Reference checking: Verify all citations are complete
    - Smart suggestions: "Based on your Approach, you might cite..."
    - Gap detection: "Your Significance doesn't cite [key paper]"
    - Duplicate detection across import methods

  in_text_behavior:
    - Insert as (PMID: 12345678) during drafting
    - Convert to formatted citation on export
    - Link to full text in knowledge base

  export:
    - Export to RIS/BibTeX for use in other tools
    - Export formatted bibliography for grant submission
```

### 5.4 Multi-Model Backend

**Seamless switching between cloud and local models:**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           LLM BACKEND ROUTER                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  MODEL REGISTRY                                                             │
│  ══════════════                                                             │
│                                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ Claude API  │  │ OpenAI API  │  │ Ollama      │  │ Image Gen   │        │
│  │ (Anthropic) │  │ (GPT-4)     │  │ (Local)     │  │             │        │
│  ├─────────────┤  ├─────────────┤  ├─────────────┤  ├─────────────┤        │
│  │ claude-3.5  │  │ gpt-4o      │  │ llama3.2    │  │ nano-banana │        │
│  │ claude-3    │  │ gpt-4-turbo │  │ mistral     │  │ dall-e-3    │        │
│  │             │  │ o1          │  │ deepseek    │  │ stable-diff │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                                             │
│  TASK → MODEL MAPPING (configurable):                                       │
│  ════════════════════════════════════                                       │
│                                                                             │
│  Task                    │ Primary       │ Fallback      │ Notes            │
│  ────────────────────────│───────────────│───────────────│──────────────────│
│  Complex reasoning       │ Claude 3.5    │ GPT-4o        │ Best quality     │
│  Writing/drafting        │ Claude 3.5    │ GPT-4         │ Style matters    │
│  Quick edits             │ Ollama local  │ Claude        │ Speed + cost     │
│  Image generation        │ Nano Banana   │ DALL-E 3      │ Scientific figs  │
│  Embeddings              │ OpenAI Ada    │ Local model   │ RAG indexing     │
│  Offline mode            │ Ollama        │ —             │ No internet      │
│                                                                             │
│  Seamless Switching:                                                        │
│  • Auto-detect: If API unreachable, fall back to local                      │
│  • Manual toggle: User can force local/cloud per task                       │
│  • Context preservation: State maintained across switches                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.5 Reviewer Feedback Parser Templates

Since reviewer feedback varies significantly by funder, GrantPilot uses a template-based parser system:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FEEDBACK PARSER TEMPLATE SYSTEM                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  USER FLOW:                                                                 │
│  ──────────                                                                 │
│  1. User uploads feedback document or pastes text                           │
│  2. User selects funder/format (or system auto-detects)                     │
│  3. Parser extracts structured data                                         │
│  4. User reviews/corrects extraction                                        │
│  5. Feedback stored and linked to submission                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Parser Templates by Funder:**

| Funder | Format | Parser Type | Extracts |
|--------|--------|-------------|----------|
| **NIH** | Summary Statement PDF | Structured | Overall score, percentile, criterion scores (1-9), individual reviewer critiques, strengths/weaknesses per section |
| **NSF** | Panel Summary + Reviews | Semi-structured | Panel recommendation, individual reviews, rating categories |
| **DOD** | Varies by program | Keyword-based | Scores (if present), narrative feedback, funding decision |
| **DOE** | Merit Review | Semi-structured | Criterion scores, reviewer comments |
| **Foundations** | Usually email/letter | NLP-based | Sentiment, key concerns, decision, any scores mentioned |
| **Generic** | Any text | NLP-based | Best-effort extraction of critique themes |

**NIH Summary Statement Parser (Example):**

```yaml
NIH_Parser:
  input_format: PDF

  extraction_rules:
    overall_impact:
      pattern: "Overall Impact/Merit.*?Score:\s*(\d)"
      type: integer
      range: 1-9

    percentile:
      pattern: "Percentile:\s*([\d.]+)"
      type: float
      optional: true

    criterion_scores:
      sections:
        - significance
        - investigator
        - innovation
        - approach
        - environment
      pattern: "{section}.*?Score:\s*(\d)"

    reviewer_critiques:
      delimiter: "Reviewer\s+\d+|Critique\s+\d+"
      per_reviewer:
        strengths:
          pattern: "Strengths?:?\s*(.*?)(?=Weakness|$)"
        weaknesses:
          pattern: "Weakness(?:es)?:?\s*(.*?)(?=Strength|$)"

    resume_instructions:
      pattern: "(?:Resume|Resubmission)\s+Instructions?:?\s*(.*)"
      optional: true

  post_processing:
    - Map critiques to grant sections (Aims, Significance, etc.)
    - Extract actionable items
    - Identify recurring themes across reviewers
    - Calculate critique sentiment scores
```

**Foundation/Generic Parser (NLP-based):**

```yaml
Generic_Parser:
  input_format: text, email, PDF

  extraction_strategy:
    decision_detection:
      positive_signals: ["pleased to inform", "congratulations", "funded", "approved"]
      negative_signals: ["regret to inform", "not funded", "declined", "not selected"]

    score_extraction:
      patterns:
        - "score[d]?\s*[:=]?\s*(\d+)"
        - "rated?\s*[:=]?\s*(\d+)"
        - "(\d+)\s*(?:out of|/)\s*(\d+)"

    critique_extraction:
      concern_signals: ["concern", "weakness", "unclear", "lacks", "insufficient", "needs"]
      strength_signals: ["strength", "strong", "excellent", "impressive", "compelling"]

    theme_clustering:
      - Group similar critiques using embedding similarity
      - Identify top 3-5 themes

  confidence_output:
    - Decision: high/medium/low confidence
    - Scores: extracted vs inferred
    - Critiques: structured vs free-form
```

**Extraction Quality Indicators:**

The system displays confidence for each extracted field:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 📝 FEEDBACK EXTRACTION — R01-Cancer-2023 Review                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ Source: NIH Summary Statement (PDF)              Parser: NIH Structured     │
│                                                                             │
│ EXTRACTED DATA                                          CONFIDENCE          │
│ ──────────────────────────────────────────────────────────────────────────  │
│ Overall Impact Score: 32                                ✓ High (exact)      │
│ Percentile: 18%                                         ✓ High (exact)      │
│ Significance Score: 3                                   ✓ High (exact)      │
│ Approach Score: 4                                       ✓ High (exact)      │
│                                                                             │
│ Reviewer 1 Concerns:                                    ◐ Medium            │
│  • "Timeline optimistic for Aim 2"                      (section mapping)   │
│  • "Power calculation not provided"                                         │
│                                                                             │
│ Reviewer 2 Concerns:                                    ◐ Medium            │
│  • "Preliminary data limited for CAR-T efficacy"                            │
│                                                                             │
│ [✓ Accept Extraction]  [✏️ Edit]  [Re-parse with different template]       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.6 Advanced Self-Learning Architecture

GrantPilot employs a multi-layered self-learning system that improves through usage, leveraging both existing pretrained models and custom fine-tuning pipelines.

#### 5.6.1 Pretrained Models to Leverage

| Model | Purpose | Why Use It |
|-------|---------|------------|
| **SPECTER2** (Allen AI) | Scientific paper embeddings | Task-specific adapters for retrieval, classification; trained on 6M scientific triplets across 23 fields |
| **PubMedBERT** | Biomedical text embeddings | 768-dim vectors optimized for medical/life science literature; ideal for RAG retrieval |
| **SciBERT** | General scientific embeddings | Pretrained on 3.17B tokens from biomedical + CS papers; good fallback |
| **BioMistral 2** | Biomedical LLM | Open-source, domain-specific; good for offline/local inference |
| **PMC-LLaMA** (7B/13B) | Biomedical generation | Trained on 4.8M papers + 30K textbooks; alternative to cloud APIs |

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    EMBEDDING MODEL ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  DOCUMENT INGESTION                                                         │
│  ══════════════════                                                         │
│                                                                             │
│   Grant Draft / Paper / RFA                                                 │
│           │                                                                 │
│           ▼                                                                 │
│   ┌───────────────────────────────────────────────────────────────────┐    │
│   │                    SPECTER2 + Adapters                            │    │
│   │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │    │
│   │  │ Retrieval    │  │ Classification│  │ Similarity   │            │    │
│   │  │ Adapter      │  │ Adapter       │  │ Adapter      │            │    │
│   │  └──────────────┘  └──────────────┘  └──────────────┘            │    │
│   └───────────────────────────────────────────────────────────────────┘    │
│           │                    │                    │                       │
│           ▼                    ▼                    ▼                       │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                 │
│   │ RAG Search   │    │ Doc Type     │    │ Style Match  │                 │
│   │ (find similar│    │ Classification│    │ Comparison   │                 │
│   │  content)    │    │              │    │              │                 │
│   └──────────────┘    └──────────────┘    └──────────────┘                 │
│                                                                             │
│  SPECIALIZED PIPELINES                                                      │
│  ════════════════════                                                       │
│                                                                             │
│   PubMedBERT → Citation/reference semantic search                          │
│   SciBERT    → Fallback for non-biomedical content                         │
│   OpenAI Ada → High-quality general embeddings (cloud)                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 5.6.2 Fine-Tuning Strategy (LoRA/PEFT)

GrantPilot uses Parameter-Efficient Fine-Tuning (PEFT) to adapt models without full retraining:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FINE-TUNING ARCHITECTURE                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  WHAT WE FINE-TUNE                                                          │
│  ═════════════════                                                          │
│                                                                             │
│  1. Style Adapter (LoRA)                                                    │
│     ────────────────────                                                    │
│     Base: Mistral 7B or LLaMA 3                                             │
│     Training data: User's funded grants + papers                            │
│     Purpose: Match user's writing voice                                     │
│     Size: ~20MB adapter (vs 14GB full model)                                │
│     Update frequency: After each new document ingestion                     │
│                                                                             │
│  2. Grant Section Classifier (LoRA)                                         │
│     ──────────────────────────────                                          │
│     Base: SciBERT or SPECTER2                                               │
│     Training data: Labeled grant sections (aims, significance, etc.)        │
│     Purpose: Accurate document classification                               │
│     Update: Continuous learning from user corrections                       │
│                                                                             │
│  3. Critique Pattern Extractor (LoRA)                                       │
│     ────────────────────────────────                                        │
│     Base: PubMedBERT                                                        │
│     Training data: Parsed reviewer feedback                                 │
│     Purpose: Identify weakness patterns across submissions                  │
│     Update: After each feedback ingestion                                   │
│                                                                             │
│  TRAINING APPROACH                                                          │
│  ═════════════════                                                          │
│                                                                             │
│  Method: QLoRA (4-bit quantization + LoRA)                                  │
│  • Reduces VRAM from 28GB to 6GB for 7B models                              │
│  • Runs on consumer GPUs or Apple Silicon                                   │
│  • Training time: ~30 min for style adapter on M2 Mac                       │
│                                                                             │
│  Implementation:                                                            │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  from peft import LoraConfig, get_peft_model                       │    │
│  │  from transformers import AutoModelForCausalLM                     │    │
│  │                                                                    │    │
│  │  lora_config = LoraConfig(                                         │    │
│  │      r=16,                    # Rank of update matrices            │    │
│  │      lora_alpha=32,           # Scaling factor                     │    │
│  │      target_modules=["q_proj", "v_proj"],                          │    │
│  │      lora_dropout=0.05,                                            │    │
│  │      bias="none",                                                  │    │
│  │      task_type="CAUSAL_LM"                                         │    │
│  │  )                                                                 │    │
│  │                                                                    │    │
│  │  model = get_peft_model(base_model, lora_config)                   │    │
│  │  # Only 0.1% of parameters are trainable                           │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 5.6.3 Agent Performance Learning

Agents track their own effectiveness to improve over time:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    AGENT PERFORMANCE TRACKING                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  METRICS TRACKED PER AGENT                                                  │
│  ═════════════════════════                                                  │
│                                                                             │
│  Research Agent:                                                            │
│  • Query success rate (found relevant results)                              │
│  • Source reliability (user accepted findings)                              │
│  • Time to useful result                                                    │
│                                                                             │
│  Writing Agent:                                                             │
│  • Acceptance rate (user kept draft)                                        │
│  • Edit distance (how much user changed output)                             │
│  • Style match score over time                                              │
│  • Funded grant correlation (did drafts lead to funding?)                   │
│                                                                             │
│  Compliance Agent:                                                          │
│  • False positive rate (flagged non-issues)                                 │
│  • False negative rate (missed real issues)                                 │
│  • User override frequency                                                  │
│                                                                             │
│  LEARNING LOOP                                                              │
│  ════════════                                                               │
│                                                                             │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐                  │
│  │ Agent   │───▶│ User    │───▶│ Analyze │───▶│ Adjust  │                  │
│  │ Output  │    │ Action  │    │ Delta   │    │ Weights │                  │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘                  │
│       │                                             │                       │
│       └─────────────────────────────────────────────┘                       │
│                      Feedback Loop                                          │
│                                                                             │
│  WHAT GETS ADJUSTED                                                         │
│  ══════════════════                                                         │
│                                                                             │
│  • Prompt template selection (which template works best for this task)      │
│  • Source weighting (which databases yield best results)                    │
│  • Confidence thresholds (calibrate based on actual accuracy)               │
│  • Agent routing (orchestrator learns which agent handles what)             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 5.6.4 Prompt Evolution System

Prompts improve through A/B testing and outcome correlation:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PROMPT EVOLUTION SYSTEM                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  VERSION CONTROL FOR PROMPTS                                                │
│  ═══════════════════════════                                                │
│                                                                             │
│  Each prompt template has:                                                  │
│  • Version number (semantic versioning)                                     │
│  • Performance metrics (acceptance rate, edit distance)                     │
│  • A/B test variants                                                        │
│  • Outcome correlation (funded vs unfunded grants using this prompt)        │
│                                                                             │
│  Example:                                                                   │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  Prompt: writing_specific_aims                                     │    │
│  │  ─────────────────────────────────────                             │    │
│  │  Version: 2.3.1                                                    │    │
│  │  Variants:                                                         │    │
│  │    A (current): Structured bullet approach    | Accept: 78%        │    │
│  │    B (test):    Narrative flow approach       | Accept: 82% ←      │    │
│  │                                                                    │    │
│  │  Outcome data:                                                     │    │
│  │    Grants using v2.x: 12 submitted, 4 funded (33%)                 │    │
│  │    Grants using v1.x: 8 submitted, 1 funded (12.5%)                │    │
│  │                                                                    │    │
│  │  Auto-recommendation: Promote variant B to default                 │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│  EVOLUTION TRIGGERS                                                         │
│  ═════════════════                                                          │
│                                                                             │
│  Automatic:                                                                 │
│  • Low acceptance rate (< 60%) → flag for review                           │
│  • High edit distance (> 50%) → user not using output as-is               │
│  • Negative outcome correlation → prompt may be hurting                    │
│                                                                             │
│  Manual:                                                                    │
│  • User creates custom prompt → becomes candidate variant                   │
│  • User reports "not helpful" → triggers review                            │
│                                                                             │
│  PROMPT LEARNING PIPELINE                                                   │
│  ════════════════════════                                                   │
│                                                                             │
│  1. Collect: Track every prompt invocation + outcome                        │
│  2. Analyze: Weekly batch analysis of prompt effectiveness                  │
│  3. Generate: LLM suggests prompt improvements based on patterns            │
│  4. Test: A/B test new variants on real tasks                               │
│  5. Promote: Winning variants become new defaults                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 5.6.5 Proactive Knowledge Expansion

The system autonomously identifies and suggests additions to the knowledge base:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PROACTIVE KNOWLEDGE EXPANSION                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  AUTOMATED MONITORING                                                       │
│  ════════════════════                                                       │
│                                                                             │
│  1. Literature Monitoring                                                   │
│     ──────────────────────                                                  │
│     • Weekly PubMed alerts for user's research keywords                     │
│     • Track citations to user's papers                                      │
│     • Monitor competitor publications                                       │
│     • Notify: "3 new papers relevant to your R01 aims"                      │
│                                                                             │
│  2. Funder Intelligence Updates                                             │
│     ────────────────────────────                                            │
│     • Monitor NIH Reporter for new awards in user's area                    │
│     • Track funding trends (which topics getting funded?)                   │
│     • Detect new RFAs matching user profile                                 │
│     • Notify: "New R21 opportunity in CAR-T immunotherapy"                  │
│                                                                             │
│  3. Gap Analysis                                                            │
│     ────────────                                                            │
│     • Identify missing document types in knowledge base                     │
│     • Suggest: "No biosketches found — upload for compliance checking"      │
│     • Suggest: "Only 3 papers in corpus — need 7 more for style confidence" │
│                                                                             │
│  KNOWLEDGE FRESHNESS                                                        │
│  ════════════════════                                                       │
│                                                                             │
│  Document Age Decay:                                                        │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  Age           │ Relevance Weight │ Action                        │    │
│  │  ──────────────│──────────────────│───────────────────────────────│    │
│  │  < 2 years     │ 1.0x            │ Full weight                    │    │
│  │  2-5 years     │ 0.8x            │ Slight decay                   │    │
│  │  > 5 years     │ 0.5x            │ Suggest update or archive      │    │
│  │  Superseded    │ 0.2x            │ Keep for history only          │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│  CROSS-PROJECT LEARNING                                                     │
│  ══════════════════════                                                     │
│                                                                             │
│  Optional (user-enabled):                                                   │
│  • Build "funder preference profiles" across multiple submissions           │
│  • Learn which reviewers respond to which argumentation styles              │
│  • Detect patterns: "NIH NIDDK prefers mechanistic detail"                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 5.6.6 Self-Learning Database Tables

```sql
-- Agent performance tracking
CREATE TABLE agent_performance (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_type      VARCHAR(50) NOT NULL,
    task_id         UUID REFERENCES agent_tasks(id),
    prompt_version  VARCHAR(20),

    -- Metrics
    execution_time_ms INTEGER,
    token_count     INTEGER,
    user_accepted   BOOLEAN,
    edit_distance   DECIMAL(5,4),  -- 0.0 = no edits, 1.0 = complete rewrite
    user_rating     INTEGER CHECK (user_rating BETWEEN 1 AND 5),

    -- Outcome correlation (filled later)
    grant_id        UUID REFERENCES projects(id),
    grant_outcome   VARCHAR(50),  -- 'funded', 'not_funded', 'pending'

    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Prompt version tracking
CREATE TABLE prompt_versions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    template_name   VARCHAR(100) NOT NULL,
    version         VARCHAR(20) NOT NULL,
    content         TEXT NOT NULL,

    -- A/B testing
    is_active       BOOLEAN DEFAULT true,
    is_default      BOOLEAN DEFAULT false,
    traffic_weight  DECIMAL(3,2) DEFAULT 0.5,  -- For A/B split

    -- Performance metrics
    invocation_count INTEGER DEFAULT 0,
    acceptance_rate DECIMAL(5,4),
    avg_edit_distance DECIMAL(5,4),
    outcome_correlation DECIMAL(5,4),  -- Correlation with funding

    -- Metadata
    parent_version  VARCHAR(20),
    change_notes    TEXT,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    promoted_at     TIMESTAMP,

    UNIQUE(template_name, version)
);

-- Knowledge expansion suggestions
CREATE TABLE knowledge_suggestions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    suggestion_type VARCHAR(50) NOT NULL,  -- 'paper', 'rfa', 'gap', 'competitor'

    -- What we're suggesting
    title           TEXT,
    source_url      TEXT,
    relevance_score DECIMAL(3,2),

    -- Why we're suggesting it
    reason          TEXT,
    related_project UUID REFERENCES projects(id),

    -- User action
    status          VARCHAR(20) DEFAULT 'pending',  -- 'pending', 'accepted', 'dismissed'
    user_action_at  TIMESTAMP,

    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Fine-tuning jobs
CREATE TABLE finetune_jobs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    model_type      VARCHAR(50) NOT NULL,  -- 'style_adapter', 'classifier', 'critique'
    base_model      VARCHAR(100) NOT NULL,

    -- Training data
    training_docs   UUID[],
    training_size   INTEGER,

    -- Status
    status          VARCHAR(20) DEFAULT 'pending',
    started_at      TIMESTAMP,
    completed_at    TIMESTAMP,
    error_message   TEXT,

    -- Output
    adapter_path    TEXT,
    adapter_size_mb DECIMAL(10,2),

    -- Metrics
    training_loss   DECIMAL(8,6),
    eval_metrics    JSONB,

    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Literature monitoring subscriptions
CREATE TABLE literature_monitors (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES users(id),

    -- What to monitor
    monitor_type    VARCHAR(50) NOT NULL,  -- 'pubmed', 'nih_reporter', 'arxiv'
    query           TEXT NOT NULL,
    keywords        TEXT[],

    -- Schedule
    frequency       VARCHAR(20) DEFAULT 'weekly',
    last_run        TIMESTAMP,
    next_run        TIMESTAMP,

    -- Results
    total_found     INTEGER DEFAULT 0,
    new_since_last  INTEGER DEFAULT 0,

    is_active       BOOLEAN DEFAULT true,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_agent_performance_type ON agent_performance(agent_type);
CREATE INDEX idx_agent_performance_outcome ON agent_performance(grant_outcome);
CREATE INDEX idx_prompt_versions_template ON prompt_versions(template_name, is_active);
CREATE INDEX idx_knowledge_suggestions_status ON knowledge_suggestions(status);
CREATE INDEX idx_literature_monitors_next ON literature_monitors(next_run) WHERE is_active;
```

---

## 6. Technical Stack

### 6.1 Overview

| Layer | Technology |
|-------|------------|
| **Frontend** | React 18 + TypeScript, Tailwind CSS, shadcn/ui, TipTap editor |
| **Backend** | Python 3.11+, FastAPI, Celery + Redis |
| **AI/LLM** | Anthropic SDK, OpenAI SDK, Ollama, LangChain |
| **Database** | PostgreSQL 16 with pgvector |
| **Document Processing** | PyMuPDF, python-docx, Pillow, pytesseract |
| **Deployment** | Docker + Docker Compose |

### 6.2 Detailed Stack

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        GRANTPILOT TECH STACK                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  FRONTEND                                                                   │
│  ════════                                                                   │
│  Framework:     React 18 + TypeScript                                       │
│  UI Library:    Tailwind CSS + shadcn/ui components                         │
│  State:         Zustand                                                     │
│  Rich Text:     TipTap (document editing with AI suggestions)               │
│  File Upload:   react-dropzone                                              │
│  Charts:        Recharts                                                    │
│  Real-time:     WebSockets                                                  │
│                                                                             │
│  BACKEND                                                                    │
│  ═══════                                                                    │
│  Language:      Python 3.11+                                                │
│  Framework:     FastAPI                                                     │
│  Task Queue:    Celery + Redis                                              │
│  WebSockets:    FastAPI native                                              │
│  File Watcher:  Watchdog                                                    │
│                                                                             │
│  AI / LLM                                                                   │
│  ════════                                                                   │
│  Orchestration: LangChain or LlamaIndex                                     │
│  Cloud LLMs:    Anthropic SDK, OpenAI SDK                                   │
│  Local LLMs:    Ollama                                                      │
│  Embeddings:    OpenAI text-embedding-3-small                               │
│  Image Gen:     Nano Banana API (primary), DALL-E 3 (fallback)              │
│  Prompts:       Jinja2 templates                                            │
│                                                                             │
│  DATA                                                                       │
│  ════                                                                       │
│  Primary DB:    PostgreSQL 16 (with pgvector extension)                     │
│  Vector Store:  pgvector                                                    │
│  Cache:         Redis                                                       │
│  File Storage:  Local filesystem (Dropbox folders)                          │
│  Backups:       Automated PostgreSQL dumps                                  │
│  ORM:           SQLAlchemy 2.0                                              │
│  Migrations:    Alembic                                                     │
│                                                                             │
│  DOCUMENT PROCESSING                                                        │
│  ═══════════════════                                                        │
│  PDF:           PyMuPDF                                                     │
│  Word:          python-docx                                                 │
│  Excel:         openpyxl                                                    │
│  Images:        Pillow + pytesseract (OCR)                                  │
│  Web Scraping:  httpx + BeautifulSoup                                       │
│  HTML→PDF:      WeasyPrint                                                  │
│                                                                             │
│  DEPLOYMENT                                                                 │
│  ══════════                                                                 │
│  Containerization:  Docker + Docker Compose                                 │
│  Startup:           Shell script (starts server + opens browser)            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 6.3 Project Directory Structure

```
grantpilot/
├── docker-compose.yml          # One command to start everything
├── start.sh                    # Helper script (starts + opens browser)
├── README.md
│
├── backend/                    # Python FastAPI server
│   ├── app/
│   │   ├── main.py             # FastAPI app entry
│   │   ├── config.py           # Configuration management
│   │   │
│   │   ├── api/                # REST API endpoints
│   │   │   ├── projects.py
│   │   │   ├── documents.py
│   │   │   ├── rfas.py
│   │   │   ├── agents.py
│   │   │   └── settings.py
│   │   │
│   │   ├── agents/             # Agent implementations
│   │   │   ├── base.py         # Base agent class
│   │   │   ├── orchestrator.py # Agent coordinator
│   │   │   ├── research.py     # Research agent
│   │   │   ├── writing.py      # Writing agent
│   │   │   ├── compliance.py   # Compliance agent
│   │   │   ├── creative.py     # Image generation agent
│   │   │   ├── analysis.py     # Analysis agent
│   │   │   └── learning.py     # Learning agent
│   │   │
│   │   ├── llm/                # LLM integrations
│   │   │   ├── router.py       # Model routing logic
│   │   │   ├── anthropic.py    # Claude integration
│   │   │   ├── openai.py       # GPT + DALL-E integration
│   │   │   ├── ollama.py       # Local model integration
│   │   │   └── cost_tracker.py # Token/cost tracking
│   │   │
│   │   ├── rag/                # RAG system
│   │   │   ├── embeddings.py   # Embedding generation
│   │   │   ├── retriever.py    # Vector search
│   │   │   ├── chunker.py      # Document chunking
│   │   │   └── learning.py     # Self-learning logic
│   │   │
│   │   ├── processors/         # Document processing
│   │   │   ├── pdf.py
│   │   │   ├── docx.py
│   │   │   ├── images.py
│   │   │   ├── rfa_parser.py   # RFA-specific parsing
│   │   │   └── classifier.py   # Document type classification
│   │   │
│   │   ├── services/           # Business logic
│   │   │   ├── project_service.py
│   │   │   ├── document_service.py
│   │   │   ├── compliance_service.py
│   │   │   ├── export_service.py  # Word export
│   │   │   └── backup_service.py
│   │   │
│   │   ├── db/                 # Database
│   │   │   ├── models.py       # SQLAlchemy models
│   │   │   ├── session.py      # DB connection
│   │   │   └── migrations/     # Alembic migrations
│   │   │
│   │   ├── prompts/            # LLM prompt templates
│   │   │   ├── research/
│   │   │   ├── writing/
│   │   │   ├── compliance/
│   │   │   └── analysis/
│   │   │
│   │   └── utils/
│   │       ├── file_watcher.py
│   │       ├── pubmed.py       # PubMed API
│   │       ├── nih_reporter.py # NIH Reporter API
│   │       └── web_scraper.py
│   │
│   ├── requirements.txt
│   ├── Dockerfile
│   └── tests/
│
├── frontend/                   # React web application
│   ├── src/
│   │   ├── App.tsx
│   │   ├── index.tsx
│   │   │
│   │   ├── components/
│   │   │   ├── layout/         # App shell, navigation
│   │   │   ├── projects/       # Project management UI
│   │   │   ├── documents/      # Document viewer/uploader
│   │   │   ├── editor/         # TipTap rich text editor
│   │   │   ├── agents/         # Agent control panel
│   │   │   ├── chat/           # Co-pilot chat interface
│   │   │   ├── compliance/     # Compliance checker UI
│   │   │   └── settings/       # Configuration UI
│   │   │
│   │   ├── hooks/              # React hooks
│   │   ├── stores/             # Zustand stores
│   │   ├── api/                # API client
│   │   └── types/              # TypeScript types
│   │
│   ├── package.json
│   ├── Dockerfile
│   └── tailwind.config.js
│
├── data/                       # Persistent data (mounted volume)
│   ├── postgresql/             # Database files
│   ├── redis/                  # Redis persistence
│   ├── backups/                # Automated backups
│   └── uploads/                # Uploaded files
│
└── scripts/
    ├── init_db.py              # Database initialization
    ├── backup.py               # Manual backup script
    └── restore.py              # Restore from backup
```

---

## 7. Database Schema

### 7.1 Complete PostgreSQL Schema

```sql
-- ============================================================================
-- GRANTPILOT DATABASE SCHEMA
-- ============================================================================

-- Enable vector extension for RAG
CREATE EXTENSION IF NOT EXISTS vector;

-- ============================================================================
-- CORE ENTITIES
-- ============================================================================

-- User settings and preferences
CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            VARCHAR(255),
    email           VARCHAR(255),
    institution     VARCHAR(255),
    department      VARCHAR(255),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User preferences (JSON for flexibility)
CREATE TABLE user_preferences (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES users(id),
    category        VARCHAR(100),  -- 'llm', 'ui', 'notifications', 'style'
    preferences     JSONB,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- PROJECTS
-- ============================================================================

CREATE TABLE projects (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES users(id),
    
    -- Basic info
    name            VARCHAR(500) NOT NULL,
    description     TEXT,
    status          VARCHAR(50) DEFAULT 'draft',
    
    -- Grant details
    grant_type      VARCHAR(100),  -- R01, R21, K99, NSF CAREER, etc.
    funder          VARCHAR(255),
    mechanism       VARCHAR(100),
    
    -- Linked RFA
    rfa_id          UUID,
    
    -- Budget tracking
    budget_total    DECIMAL(12,2),
    budget_per_year DECIMAL(12,2),
    
    -- Deadlines
    deadline        TIMESTAMP,
    internal_deadline TIMESTAMP,
    
    -- AI cost tracking for this project
    token_budget    INTEGER,
    tokens_used     INTEGER DEFAULT 0,
    cost_budget     DECIMAL(10,4),
    cost_used       DECIMAL(10,4) DEFAULT 0,
    
    -- Metadata
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    archived_at     TIMESTAMP
);

-- Project sections
CREATE TABLE project_sections (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id      UUID REFERENCES projects(id) ON DELETE CASCADE,
    
    section_type    VARCHAR(100),
    title           VARCHAR(255),
    content         TEXT,
    version         INTEGER DEFAULT 1,
    
    -- Compliance tracking
    word_count      INTEGER,
    page_count      DECIMAL(4,2),
    word_limit      INTEGER,
    page_limit      DECIMAL(4,2),
    is_compliant    BOOLEAN,
    
    -- AI analysis
    ai_suggestions  JSONB,
    compliance_issues JSONB,
    
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Version history
CREATE TABLE section_versions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    section_id      UUID REFERENCES project_sections(id) ON DELETE CASCADE,
    version         INTEGER,
    content         TEXT,
    change_summary  TEXT,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- DOCUMENTS
-- ============================================================================

CREATE TABLE documents (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES users(id),
    project_id      UUID REFERENCES projects(id),
    
    -- File info
    filename        VARCHAR(500) NOT NULL,
    file_path       TEXT NOT NULL,
    file_type       VARCHAR(50),
    file_size       BIGINT,
    file_hash       VARCHAR(64),
    
    -- Classification
    document_type   VARCHAR(100),
    document_subtype VARCHAR(100),
    
    -- Processing status
    processing_status VARCHAR(50) DEFAULT 'pending',
    processed_at    TIMESTAMP,
    
    -- Extracted content
    extracted_text  TEXT,
    extracted_metadata JSONB,
    image_description TEXT,
    
    -- Source tracking
    source          VARCHAR(50),
    source_url      TEXT,
    
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at      TIMESTAMP
);

-- Document chunks for RAG
CREATE TABLE document_chunks (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id     UUID REFERENCES documents(id) ON DELETE CASCADE,
    
    chunk_index     INTEGER,
    chunk_text      TEXT,
    chunk_metadata  JSONB,
    
    -- Vector embedding
    embedding       vector(1536),
    
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Vector similarity search index
CREATE INDEX ON document_chunks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- ============================================================================
-- RFAs
-- ============================================================================

CREATE TABLE rfas (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    title           VARCHAR(1000) NOT NULL,
    funder          VARCHAR(255),
    mechanism       VARCHAR(100),
    rfa_number      VARCHAR(100),
    
    source_url      TEXT,
    
    release_date    DATE,
    deadline        TIMESTAMP,
    letter_of_intent_date DATE,
    
    full_text       TEXT,
    parsed_requirements JSONB,
    parsed_priorities JSONB,
    
    budget_cap_total DECIMAL(12,2),
    budget_cap_yearly DECIMAL(12,2),
    
    ai_analysis     JSONB,
    keyword_frequencies JSONB,
    
    status          VARCHAR(50) DEFAULT 'active',
    
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- RFA requirements checklist
CREATE TABLE rfa_requirements (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rfa_id          UUID REFERENCES rfas(id) ON DELETE CASCADE,
    
    requirement_type VARCHAR(100),
    category        VARCHAR(100),
    description     TEXT,
    is_mandatory    BOOLEAN DEFAULT true,
    
    validation_rule JSONB,
    
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- SUBMISSIONS & REVIEWS
-- ============================================================================

CREATE TABLE submissions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id      UUID REFERENCES projects(id) ON DELETE CASCADE,
    
    submission_date DATE,
    iteration       INTEGER DEFAULT 1,
    
    outcome         VARCHAR(50),
    score           DECIMAL(4,1),
    percentile      DECIMAL(5,2),
    
    award_amount    DECIMAL(12,2),
    award_start_date DATE,
    award_end_date  DATE,
    award_number    VARCHAR(100),
    
    submitted_documents JSONB,
    
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reviews (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    submission_id   UUID REFERENCES submissions(id) ON DELETE CASCADE,
    
    reviewer_number INTEGER,
    raw_text        TEXT,
    
    parsed_critiques JSONB,
    themes          JSONB,
    sentiment       VARCHAR(50),
    actionable_items JSONB,
    criterion_scores JSONB,
    
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- KNOWLEDGE BASE & LEARNING
-- ============================================================================

CREATE TABLE example_grants (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id     UUID REFERENCES documents(id),
    
    title           VARCHAR(500),
    grant_type      VARCHAR(100),
    funder          VARCHAR(255),
    
    quality_rating  VARCHAR(50),
    was_funded      BOOLEAN,
    
    annotations     JSONB,
    strengths       TEXT[],
    weaknesses      TEXT[],
    
    source          VARCHAR(100),
    is_own_grant    BOOLEAN DEFAULT false,
    
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE learned_patterns (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    pattern_type    VARCHAR(100),
    category        VARCHAR(100),
    
    pattern_description TEXT,
    evidence        JSONB,
    
    confidence      DECIMAL(3,2),
    occurrence_count INTEGER DEFAULT 1,
    
    style_vector    vector(1536),
    
    is_active       BOOLEAN DEFAULT true,
    
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE style_profiles (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES users(id),
    
    name            VARCHAR(255) DEFAULT 'Default',
    description     TEXT,
    
    formality       DECIMAL(3,2),
    confidence      DECIMAL(3,2),
    technical_depth DECIMAL(3,2),
    conciseness     DECIMAL(3,2),
    
    vocabulary_preferences JSONB,
    phrase_patterns JSONB,
    avoided_phrases TEXT[],
    
    source_documents UUID[],
    
    is_default      BOOLEAN DEFAULT false,
    
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- REFERENCES & CITATIONS
-- ============================================================================

CREATE TABLE references (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    pmid            VARCHAR(20),
    doi             VARCHAR(255),
    
    title           TEXT,
    authors         JSONB,
    journal         VARCHAR(500),
    year            INTEGER,
    volume          VARCHAR(50),
    pages           VARCHAR(50),
    
    abstract        TEXT,
    
    relevance_embedding vector(1536),
    
    readcube_id     VARCHAR(255),
    
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE document_references (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reference_id    UUID REFERENCES references(id),
    document_id     UUID REFERENCES documents(id),
    section_id      UUID REFERENCES project_sections(id),
    
    context         TEXT,
    citation_number INTEGER,
    
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- AGENT SYSTEM
-- ============================================================================

CREATE TABLE agent_tasks (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id      UUID REFERENCES projects(id),
    
    agent_type      VARCHAR(100),
    task_description TEXT,
    task_config     JSONB,
    
    status          VARCHAR(50) DEFAULT 'pending',
    started_at      TIMESTAMP,
    completed_at    TIMESTAMP,
    
    time_limit_minutes INTEGER,
    depth_level     VARCHAR(50),
    
    result          JSONB,
    result_summary  TEXT,
    
    activity_log    JSONB,
    
    tokens_used     INTEGER DEFAULT 0,
    cost_incurred   DECIMAL(10,4) DEFAULT 0,
    
    user_injections JSONB,
    
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- COST TRACKING
-- ============================================================================

CREATE TABLE api_usage (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    project_id      UUID REFERENCES projects(id),
    agent_task_id   UUID REFERENCES agent_tasks(id),
    
    provider        VARCHAR(50),
    model           VARCHAR(100),
    
    prompt_tokens   INTEGER,
    completion_tokens INTEGER,
    total_tokens    INTEGER,
    
    cost            DECIMAL(10,6),
    
    purpose         VARCHAR(100),
    
    timestamp       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE budget_alerts (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id      UUID REFERENCES projects(id),
    
    alert_type      VARCHAR(50),
    threshold_percent INTEGER,
    
    message         TEXT,
    acknowledged    BOOLEAN DEFAULT false,
    
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- WATCHED FOLDERS
-- ============================================================================

CREATE TABLE watched_folders (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    folder_path     TEXT NOT NULL,
    folder_name     VARCHAR(255),
    
    is_active       BOOLEAN DEFAULT true,
    sync_interval_minutes INTEGER DEFAULT 60,
    last_synced     TIMESTAMP,
    
    auto_classify   BOOLEAN DEFAULT true,
    default_document_type VARCHAR(100),
    
    total_files     INTEGER DEFAULT 0,
    
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- SYSTEM & RECOVERY
-- ============================================================================

CREATE TABLE system_state (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    key             VARCHAR(255) UNIQUE NOT NULL,
    value           JSONB,
    
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE backup_history (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    backup_type     VARCHAR(50),
    backup_path     TEXT,
    file_size       BIGINT,
    
    status          VARCHAR(50),
    error_message   TEXT,
    
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- INDEXES
-- ============================================================================

CREATE INDEX idx_documents_project ON documents(project_id);
CREATE INDEX idx_documents_type ON documents(document_type);
CREATE INDEX idx_documents_hash ON documents(file_hash);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_agent_tasks_status ON agent_tasks(status);
CREATE INDEX idx_api_usage_project ON api_usage(project_id);
CREATE INDEX idx_api_usage_timestamp ON api_usage(timestamp);

CREATE INDEX idx_documents_text_search ON documents USING gin(to_tsvector('english', extracted_text));
CREATE INDEX idx_rfas_text_search ON rfas USING gin(to_tsvector('english', full_text));
```

### 7.2 Crash Recovery & Backup System

**Backup Schedule:**
- **Continuous:** Write-ahead logging (PostgreSQL WAL)
- **Hourly:** State snapshot to local backup folder
- **Daily:** Full database dump to Dropbox/backup_grantpilot/
- **Weekly:** Compressed archive with verification

**What's Preserved:**
- All project data and drafts
- Agent task states (can resume interrupted tasks)
- Learned patterns and style profiles
- Complete conversation history with AI
- Document embeddings (expensive to regenerate)
- Cost tracking history

**Recovery Scenarios:**
- App crash → Auto-restart, resume from last state
- Computer crash → Full recovery from latest backup
- Database corruption → Point-in-time recovery from WAL

**Agent Task Recovery:**
- Task state checkpointed every 30 seconds
- On restart, detect incomplete tasks
- Offer options: Resume, Restart, or Cancel with partial results

---

## 8. API Contracts

**Complete specification available in:** `grantpilot-api-contracts.md`

### 8.1 Overview

The API contracts document defines 70+ REST endpoints organized by resource:

| API Group | Endpoints | Description |
|-----------|-----------|-------------|
| Projects | 11 | Project CRUD, sections, compliance, export |
| Documents | 8 | Upload, processing, preview, bulk operations |
| RFAs | 8 | RFA management, parsing, prior awards |
| Agents | 10 | Task management, injection, control |
| Chat | 4 | Messaging, history, suggestions |
| Knowledge Base | 7 | Search, examples, patterns, styles |
| References | 5 | Citations, lookup, ReadCube sync |
| Settings | 12 | Configuration, folders, costs, backups |

### 8.2 Key Features

- **RESTful design** with consistent response structure
- **Cursor-based pagination** for all list endpoints
- **WebSocket events** for real-time updates (12 event types)
- **Comprehensive error codes** (20+ domain-specific codes)
- **TypeScript type definitions** for frontend development

### 8.3 WebSocket Channels

Real-time events for:
- Agent activity streaming and status changes
- Chat message streaming
- Document processing progress
- Compliance updates
- Cost alerts and notifications

See `grantpilot-api-contracts.md` for complete endpoint specifications, request/response schemas, and examples.

---

## 9. Agent Prompt Templates

**[TODO - To be defined in next iteration]**

This section will include:
- Research agent prompts
- Writing agent prompts (with style matching)
- Compliance agent prompts
- Anti-LLM detection prompts
- RFA analysis prompts

---

## 10. Workflow Diagrams

This section contains visual workflows for key user journeys and system processes.

### 10.1 User Journey Maps

#### 10.1.1 New User Onboarding Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        NEW USER ONBOARDING FLOW                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐           │
│  │  START   │────▶│  Setup   │────▶│  Connect │────▶│  Import  │           │
│  │  Docker  │     │  API     │     │  Folders │     │  Docs    │           │
│  └──────────┘     │  Keys    │     └──────────┘     └──────────┘           │
│                   └──────────┘           │                │                 │
│                                          │                │                 │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                     │   │
│  │  1. LAUNCH                                                          │   │
│  │     └─▶ Double-click start.sh (or docker-compose up)                │   │
│  │     └─▶ Browser opens http://localhost:3000                         │   │
│  │     └─▶ First-run wizard appears                                    │   │
│  │                                                                     │   │
│  │  2. API CONFIGURATION                                               │   │
│  │     ┌─────────────────────────────────────────────────────────┐    │   │
│  │     │ 🔑 Enter API Keys                                        │    │   │
│  │     │                                                          │    │   │
│  │     │ Anthropic API Key: [sk-ant-••••••••••••]  [✓ Valid]     │    │   │
│  │     │ OpenAI API Key:    [sk-••••••••••••••••]  [✓ Valid]     │    │   │
│  │     │                                                          │    │   │
│  │     │ ☐ Enable Ollama for offline (optional)                   │    │   │
│  │     │   Status: [Not detected - Install Ollama]                │    │   │
│  │     └─────────────────────────────────────────────────────────┘    │   │
│  │                                                                     │   │
│  │  3. FOLDER CONNECTION                                               │   │
│  │     ┌─────────────────────────────────────────────────────────┐    │   │
│  │     │ 📁 Connect Your Grant Folders                            │    │   │
│  │     │                                                          │    │   │
│  │     │ Grants Folder: [/Users/you/Dropbox/Grants]  [Browse]    │    │   │
│  │     │   ☑ Watch for changes                                    │    │   │
│  │     │   ☑ Auto-import new files                                │    │   │
│  │     │                                                          │    │   │
│  │     │ Papers Folder: [/Users/you/Papers]  [Browse]  (optional) │    │   │
│  │     └─────────────────────────────────────────────────────────┘    │   │
│  │                                                                     │   │
│  │  4. INITIAL IMPORT                                                  │   │
│  │     ┌─────────────────────────────────────────────────────────┐    │   │
│  │     │ 📄 Scanning folders...                                   │    │   │
│  │     │                                                          │    │   │
│  │     │ Found: 47 documents across 12 potential projects         │    │   │
│  │     │                                                          │    │   │
│  │     │ ├─ R01_Cancer_2024/     (8 files) → Grant Project       │    │   │
│  │     │ ├─ NSF_CAREER_Draft/    (5 files) → Grant Project       │    │   │
│  │     │ ├─ Papers_2023/         (15 files) → Reference Papers   │    │   │
│  │     │ └─ ...                                                   │    │   │
│  │     │                                                          │    │   │
│  │     │ [Accept All]  [Review & Edit]  [Import Later]            │    │   │
│  │     └─────────────────────────────────────────────────────────┘    │   │
│  │                                                                     │   │
│  │  5. STYLE BOOTSTRAP (Optional)                                      │   │
│  │     ┌─────────────────────────────────────────────────────────┐    │   │
│  │     │ ✍️ Help us learn your writing style                      │    │   │
│  │     │                                                          │    │   │
│  │     │ Mark your best writing samples:                          │    │   │
│  │     │ ☑ R01_Cancer_2023_Funded.docx (★ Funded - 2x weight)    │    │   │
│  │     │ ☑ Nature_Paper_2024.pdf       (Published)                │    │   │
│  │     │ ☐ Draft_Aims_v1.docx          (Work in progress)        │    │   │
│  │     │                                                          │    │   │
│  │     │ Style confidence: 45% (Learning - add more for 70%+)     │    │   │
│  │     └─────────────────────────────────────────────────────────┘    │   │
│  │                                                                     │   │
│  │  6. READY!                                                          │   │
│  │     └─▶ Dashboard appears with imported projects                    │   │
│  │     └─▶ Tutorial tooltip: "Start with Agent Mode to research"      │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  TIME: ~5 minutes for basic setup, ~15 minutes with full import            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 10.1.2 Create New Grant Project Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      CREATE NEW GRANT PROJECT FLOW                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  User Action              System Response              Next Step            │
│  ═══════════              ═══════════════              ═════════            │
│                                                                             │
│  ┌────────────┐                                                             │
│  │ Click      │                                                             │
│  │ "+ New     │                                                             │
│  │  Project"  │                                                             │
│  └─────┬──────┘                                                             │
│        │                                                                    │
│        ▼                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  NEW PROJECT WIZARD                                                  │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │                                                                      │   │
│  │  Step 1: Basic Info                                                  │   │
│  │  ────────────────────                                                │   │
│  │  Project Name: [R01 - CAR-T Tumor Microenvironment Study      ]     │   │
│  │  Grant Type:   [R01 - Research Project ▾]                            │   │
│  │  Funder:       [NIH ▾]  Institute: [NCI - Cancer ▾]                 │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│        │                                                                    │
│        ▼                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Step 2: Link RFA (Optional)                                         │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │                                                                      │   │
│  │  ○ No specific RFA (use standard R01 guidelines)                    │   │
│  │  ● Link to RFA:                                                      │   │
│  │    [PAR-24-123 ▾] or [Paste RFA URL / Upload PDF]                   │   │
│  │                                                                      │   │
│  │  ┌───────────────────────────────────────────────────────────────┐  │   │
│  │  │ 📋 RFA-CA-24-001 detected                                      │  │   │
│  │  │    Title: "Tumor Microenvironment Research"                    │  │   │
│  │  │    Deadline: March 5, 2025 (47 days)                           │  │   │
│  │  │    Budget: $500K/year direct                                   │  │   │
│  │  │                                                                │  │   │
│  │  │    [Parse RFA Now] ← Extracts requirements, priorities         │  │   │
│  │  └───────────────────────────────────────────────────────────────┘  │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│        │                                                                    │
│        ▼                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Step 3: Import Documents                                            │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │                                                                      │   │
│  │  Drag & drop files or [Browse]                                       │   │
│  │                                                                      │   │
│  │  ┌───────────────────────────────────────────────────────────────┐  │   │
│  │  │  📄 Specific_Aims_Draft_v1.docx      → Specific Aims (draft)  │  │   │
│  │  │  📄 Preliminary_Data_Fig1.png        → Figure                  │  │   │
│  │  │  📄 Biosketch_Smith.pdf              → Biosketch               │  │   │
│  │  │  📄 Previous_Review_2023.pdf         → Reviewer Feedback       │  │   │
│  │  └───────────────────────────────────────────────────────────────┘  │   │
│  │                                                                      │   │
│  │  ☑ Link folder: /Dropbox/Grants/R01_CAR-T_2025/                     │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│        │                                                                    │
│        ▼                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Step 4: Quick Start Options                                         │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │                                                                      │   │
│  │  What would you like to do first?                                    │   │
│  │                                                                      │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐      │   │
│  │  │ 🔬 Research     │  │ ✍️ Start        │  │ ✅ Check        │      │   │
│  │  │    Competitive  │  │    Writing      │  │    Compliance   │      │   │
│  │  │    Landscape    │  │    Aims         │  │                 │      │   │
│  │  │                 │  │                 │  │                 │      │   │
│  │  │ Agent Mode      │  │ Co-pilot Mode   │  │ Compliance Mode │      │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘      │   │
│  │                                                                      │   │
│  │  [ ] Just go to project dashboard                                    │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│        │                                                                    │
│        ▼                                                                    │
│  ┌────────────┐                                                             │
│  │  PROJECT   │  User lands in chosen mode with context loaded             │
│  │  CREATED   │  RFA parsed, documents indexed, ready to work              │
│  └────────────┘                                                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 10.1.3 Agent Mode Task Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AGENT MODE TASK FLOW                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  USER                           SYSTEM                          AGENTS      │
│  ════                           ══════                          ══════      │
│                                                                             │
│  ┌─────────────┐                                                            │
│  │ Define      │                                                            │
│  │ Mission     │───────────────────────────────────────────────────────────▶│
│  │             │   "Research competitive landscape for                      │
│  │ + Set       │    CAR-T in solid tumors and draft                        │
│  │   constraints│    Significance section"                                  │
│  └─────────────┘                                                            │
│        │                                                                    │
│        ▼                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  CONSTRAINT CONFIGURATION                                            │   │
│  │  ─────────────────────────                                           │   │
│  │  ⏱️ Time Cap: [2 hours]     🔍 Depth: [Comprehensive]               │   │
│  │                                                                      │   │
│  │  📂 Sources to use:                                                  │   │
│  │  ☑ NIH Reporter (funded grants)     ☑ PubMed (literature)           │   │
│  │  ☑ Web search (general)             ☐ My papers only                 │   │
│  │  ☑ This RFA                         ☑ My knowledge base              │   │
│  │                                                                      │   │
│  │  💰 Budget: [$5.00 max for this task]                                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│        │                                                                    │
│        │  [▶ Launch Agent]                                                  │
│        ▼                                                                    │
│                              ┌─────────────────┐                            │
│                              │  ORCHESTRATOR   │                            │
│                              │                 │                            │
│                              │ 1. Parse task   │                            │
│                              │ 2. Plan steps   │                            │
│                              │ 3. Route agents │                            │
│                              └────────┬────────┘                            │
│                                       │                                     │
│                    ┌──────────────────┼──────────────────┐                  │
│                    ▼                  ▼                  ▼                  │
│             ┌───────────┐      ┌───────────┐      ┌───────────┐            │
│             │ RESEARCH  │      │ ANALYSIS  │      │  WRITING  │            │
│             │  AGENT    │      │  AGENT    │      │   AGENT   │            │
│             │           │      │           │      │           │            │
│             │ • NIH     │      │ • Gap     │      │ • Draft   │            │
│             │   Reporter│─────▶│   analysis│─────▶│   section │            │
│             │ • PubMed  │      │ • Trends  │      │ • Style   │            │
│             │ • Web     │      │           │      │   match   │            │
│             └───────────┘      └───────────┘      └───────────┘            │
│                    │                  │                  │                  │
│                    └──────────────────┴──────────────────┘                  │
│                                       │                                     │
│        ┌──────────────────────────────┴──────────────────────────────┐     │
│        │                                                              │     │
│        │  LIVE ACTIVITY FEED                                          │     │
│        │  ══════════════════                                          │     │
│        │                                                              │     │
│        │  14:23:01 🔍 Parsing mission requirements...                 │     │
│        │  14:23:05 📋 Created plan: 3 research tasks → 1 writing task │     │
│        │  14:23:08 🔬 [Research] Querying NIH Reporter for CAR-T...   │     │
│        │  14:24:15 ✓  [Research] Found 47 funded R01s (2021-2024)     │     │
│        │  14:24:20 🔬 [Research] Searching PubMed for reviews...      │     │
│        │  14:25:30 ✓  [Research] Found 23 relevant reviews            │     │
│        │  14:25:35 📊 [Analysis] Identifying research gaps...         │     │
│        │  14:26:45 ✓  [Analysis] 3 major gaps identified              │     │
│        │  14:26:50 ✍️ [Writing] Drafting Significance section...      │     │
│        │  14:28:00 ✓  [Writing] Draft complete (876 words)            │     │
│        │                                                              │     │
│        │  ┌────────────────────────────────────────────────────────┐ │     │
│        │  │ 💬 Inject context: [Type to add info mid-run...]       │ │     │
│        │  └────────────────────────────────────────────────────────┘ │     │
│        │                                                              │     │
│        │  [⏸ Pause]  [🛑 Stop & Save]  [📊 View Interim Results]     │     │
│        │                                                              │     │
│        └──────────────────────────────────────────────────────────────┘     │
│        │                                                                    │
│        ▼                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  TASK COMPLETE                                                       │   │
│  │  ═════════════                                                       │   │
│  │                                                                      │   │
│  │  📊 Research Report          ✍️ Significance Draft                   │   │
│  │  ├─ 47 funded grants         ├─ 876 words                            │   │
│  │  ├─ 23 key papers            ├─ Style match: 82%                     │   │
│  │  ├─ 5 top competitors        ├─ Anti-LLM: 2 flags                    │   │
│  │  └─ 3 research gaps          └─ Confidence: High                     │   │
│  │                                                                      │   │
│  │  💰 Cost: $3.47 | ⏱️ Time: 5m 23s                                    │   │
│  │                                                                      │   │
│  │  [View Full Report]  [Edit Draft]  [Export]  [New Task]              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 10.1.4 Co-pilot Mode Interaction Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      CO-PILOT MODE INTERACTION FLOW                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────┬───────────────────────────────────┐│
│  │         DOCUMENT WORKSPACE          │          CO-PILOT CHAT            ││
│  │         (Left Panel)                │          (Right Panel)            ││
│  ├─────────────────────────────────────┼───────────────────────────────────┤│
│  │                                     │                                   ││
│  │  📄 Specific Aims (v3)              │  💬 CONVERSATION                  ││
│  │  ─────────────────────              │                                   ││
│  │                                     │  🤖 I notice your Aim 2 doesn't   ││
│  │  [Aim 1: CAR-T optimization]        │     reference the preliminary     ││
│  │                                     │     data from your 2024 paper.    ││
│  │  We will engineer next-gen...       │     The RFA emphasizes "strong    ││
│  │                                     │     rationale" — adding Fig 3     ││
│  │  ┌─────────────────────────────┐   │     would strengthen this.        ││
│  │  │ 💡 AI Suggestion            │   │                                   ││
│  │  │    "Consider adding a       │   │  ─────────────────────────────    ││
│  │  │    sentence about tumor     │   │                                   ││
│  │  │    heterogeneity here"      │   │  👤 Can you show me how other     ││
│  │  │    [Accept] [Modify] [X]    │   │     funded grants positioned      ││
│  │  └─────────────────────────────┘   │     similar preliminary data?     ││
│  │                                     │                                   ││
│  │  [Aim 2: TME modulation]            │  🤖 I found 3 relevant examples   ││
│  │                                     │     from funded R01s. Here's      ││
│  │  Our preliminary data shows...      │     how they structured their     ││
│  │  ⚠️ [Missing: Fig 3 reference]      │     preliminary data sections:    ││
│  │                                     │                                   ││
│  │                                     │     1. Dr. Smith (NCI R01):       ││
│  │  ─────────────────────────────      │        "Our published data        ││
│  │                                     │        (Fig 2, Smith et al.)      ││
│  │  [Aim 3: Translational pathway]     │        demonstrates..."           ││
│  │                                     │                                   ││
│  │                                     │     [See all 3 examples]          ││
│  │                                     │                                   ││
│  │                                     │  ─────────────────────────────    ││
│  │                                     │                                   ││
│  │                                     │  👤 Draft a sentence for Aim 2   ││
│  │                                     │     that references my Fig 3      ││
│  │                                     │                                   ││
│  │                                     │  🤖 Here's a suggested addition:  ││
│  │                                     │                                   ││
│  │                                     │     "Our preliminary data         ││
│  │                                     │     (Fig. 3) demonstrates that    ││
│  │                                     │     CAR-T cells exhibit reduced   ││
│  │                                     │     persistence in hypoxic..."    ││
│  │                                     │                                   ││
│  │                                     │     Style match: 87% ✓            ││
│  │                                     │     [Insert at cursor]            ││
│  │                                     │     [Edit first]                  ││
│  └─────────────────────────────────────┴───────────────────────────────────┘│
│  │                                                                         ││
│  │  📊 PROACTIVE ALERTS                                            [Hide] ││
│  │  ┌─────────────────────────────────────────────────────────────────────┐││
│  │  │ ⚠️ Deadline: 18 days │ 🔍 New R01 posted │ ✅ Format: Compliant    │││
│  │  └─────────────────────────────────────────────────────────────────────┘││
│  │                                                                          │
│  └──────────────────────────────────────────────────────────────────────────┘
│                                                                             │
│  INTERACTION PATTERNS                                                       │
│  ════════════════════                                                       │
│                                                                             │
│  User Can:                              AI Will:                            │
│  ─────────                              ────────                            │
│  • Ask questions about content          • Proactively notice issues         │
│  • Request edits/rewrites              • Suggest improvements               │
│  • Select text → "Improve this"        • Compare to funded examples         │
│  • Ask for examples                    • Match user's writing style         │
│  • Request compliance check            • Flag potential problems            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 10.2 System Flow Diagrams

#### 10.2.1 Document Ingestion Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       DOCUMENT INGESTION PIPELINE                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INPUT SOURCES                                                              │
│  ═════════════                                                              │
│                                                                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐          │
│  │ Drag &  │  │ Folder  │  │ URL     │  │ RFA     │  │ API     │          │
│  │ Drop    │  │ Watch   │  │ Import  │  │ Number  │  │ Upload  │          │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘          │
│       │            │            │            │            │                 │
│       └────────────┴────────────┴────────────┴────────────┘                 │
│                                 │                                           │
│                                 ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        FILE RECEIVER                                 │   │
│  │  ────────────────────────────────────────────────────────────────── │   │
│  │  • Detect file type (PDF, DOCX, XLSX, PNG, URL)                     │   │
│  │  • Check for duplicates (hash comparison)                           │   │
│  │  • Queue for processing                                             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                 │                                           │
│                                 ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        CONTENT EXTRACTOR                             │   │
│  │  ────────────────────────────────────────────────────────────────── │   │
│  │                                                                      │   │
│  │  PDF ──────▶ PyMuPDF ──────▶ Text + Images                          │   │
│  │  DOCX ─────▶ python-docx ──▶ Text + Images + Tables                 │   │
│  │  Images ───▶ Pytesseract ──▶ OCR Text                               │   │
│  │  Web ──────▶ Playwright ───▶ Rendered HTML → Text                   │   │
│  │                                                                      │   │
│  │  Output: raw_text, images[], tables[], metadata{}                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                 │                                           │
│                                 ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        DOCUMENT CLASSIFIER                           │   │
│  │  ────────────────────────────────────────────────────────────────── │   │
│  │                                                                      │   │
│  │  Uses: SPECTER2 Classification Adapter + Heuristics                 │   │
│  │                                                                      │   │
│  │  Document Types:                                                     │   │
│  │  ┌────────────────┬────────────────┬────────────────┐               │   │
│  │  │ Specific Aims  │ Biosketch      │ RFA/FOA        │               │   │
│  │  │ Research Strat │ Budget         │ Review Letter  │               │   │
│  │  │ Significance   │ Letter Support │ Published Paper│               │   │
│  │  │ Innovation     │ Figure         │ Draft/Notes    │               │   │
│  │  │ Approach       │ Table          │ Other          │               │   │
│  │  └────────────────┴────────────────┴────────────────┘               │   │
│  │                                                                      │   │
│  │  Confidence displayed to user: ✓ High / ◐ Medium / ○ Low            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                 │                                           │
│                                 ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                          CHUNKER                                     │   │
│  │  ────────────────────────────────────────────────────────────────── │   │
│  │                                                                      │   │
│  │  Strategy: Semantic chunking with overlap                           │   │
│  │                                                                      │   │
│  │  ┌─────────────────────────────────────────────────────────────┐   │   │
│  │  │  Document                                                    │   │   │
│  │  │  ┌──────────────────────────────────────────────────────┐   │   │   │
│  │  │  │ Section 1 (Aims)                                      │   │   │   │
│  │  │  │  ┌────────┐  ┌────────┐  ┌────────┐                  │   │   │   │
│  │  │  │  │Chunk 1 │──│Chunk 2 │──│Chunk 3 │   ← 512 tokens   │   │   │   │
│  │  │  │  │        │  │(overlap│  │        │   ← 50 overlap   │   │   │   │
│  │  │  │  └────────┘  └────────┘  └────────┘                  │   │   │   │
│  │  │  └──────────────────────────────────────────────────────┘   │   │   │
│  │  │  ┌──────────────────────────────────────────────────────┐   │   │   │
│  │  │  │ Section 2 (Significance)                              │   │   │   │
│  │  │  │  ┌────────┐  ┌────────┐                              │   │   │   │
│  │  │  │  │Chunk 4 │──│Chunk 5 │                              │   │   │   │
│  │  │  │  └────────┘  └────────┘                              │   │   │   │
│  │  │  └──────────────────────────────────────────────────────┘   │   │   │
│  │  └─────────────────────────────────────────────────────────────┘   │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                 │                                           │
│                                 ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        EMBEDDING GENERATOR                           │   │
│  │  ────────────────────────────────────────────────────────────────── │   │
│  │                                                                      │   │
│  │  For each chunk:                                                     │   │
│  │  ┌──────────────────────────────────────────────────────────────┐  │   │
│  │  │  Chunk Text ──▶ SPECTER2 (Retrieval Adapter) ──▶ 768-dim vec │  │   │
│  │  │              ──▶ PubMedBERT (for medical)     ──▶ 768-dim vec │  │   │
│  │  └──────────────────────────────────────────────────────────────┘  │   │
│  │                                                                      │   │
│  │  For style learning:                                                 │   │
│  │  ┌──────────────────────────────────────────────────────────────┐  │   │
│  │  │  Full Doc ──▶ SPECTER2 (Similarity Adapter) ──▶ Style vector │  │   │
│  │  └──────────────────────────────────────────────────────────────┘  │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                 │                                           │
│                                 ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         DATABASE STORAGE                             │   │
│  │  ────────────────────────────────────────────────────────────────── │   │
│  │                                                                      │   │
│  │  PostgreSQL + pgvector                                              │   │
│  │                                                                      │   │
│  │  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐            │   │
│  │  │  documents   │   │  doc_chunks  │   │  embeddings  │            │   │
│  │  │  ──────────  │   │  ──────────  │   │  ──────────  │            │   │
│  │  │  id          │──▶│  doc_id      │──▶│  chunk_id    │            │   │
│  │  │  file_path   │   │  content     │   │  vector      │ ←pgvector  │   │
│  │  │  doc_type    │   │  position    │   │  model_name  │            │   │
│  │  │  metadata    │   │  section     │   │              │            │   │
│  │  └──────────────┘   └──────────────┘   └──────────────┘            │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  TIMING: Small doc (~5 pages): 2-5 seconds | Large doc (~50 pages): 15-30s │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 10.2.2 Agent Orchestration Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       AGENT ORCHESTRATION FLOW                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                            ┌─────────────────┐                              │
│                            │   USER REQUEST  │                              │
│                            │                 │                              │
│                            │ "Research and   │                              │
│                            │  draft section" │                              │
│                            └────────┬────────┘                              │
│                                     │                                       │
│                                     ▼                                       │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                         ORCHESTRATOR                                  │  │
│  │  ══════════════════════════════════════════════════════════════════  │  │
│  │                                                                       │  │
│  │  STEP 1: PARSE & PLAN                                                 │  │
│  │  ────────────────────                                                 │  │
│  │  • Analyze user intent                                                │  │
│  │  • Break into subtasks                                                │  │
│  │  • Determine agent routing                                            │  │
│  │  • Estimate cost/time                                                 │  │
│  │                                                                       │  │
│  │  Generated Plan:                                                      │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐ │  │
│  │  │ Task 1: Research (parallel)                                     │ │  │
│  │  │   ├─ 1a: NIH Reporter query      → Research Agent               │ │  │
│  │  │   ├─ 1b: PubMed literature       → Research Agent               │ │  │
│  │  │   └─ 1c: Parse RFA priorities    → Compliance Agent             │ │  │
│  │  │                                                                  │ │  │
│  │  │ Task 2: Synthesize (sequential)                                  │ │  │
│  │  │   └─ 2a: Gap analysis            → Analysis Agent               │ │  │
│  │  │                                                                  │ │  │
│  │  │ Task 3: Write (sequential)                                       │ │  │
│  │  │   └─ 3a: Draft section           → Writing Agent                 │ │  │
│  │  └─────────────────────────────────────────────────────────────────┘ │  │
│  │                                                                       │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                     │                                       │
│          ┌──────────────────────────┼──────────────────────────┐           │
│          ▼                          ▼                          ▼           │
│  ┌──────────────┐           ┌──────────────┐           ┌──────────────┐   │
│  │   RESEARCH   │           │   RESEARCH   │           │  COMPLIANCE  │   │
│  │    AGENT     │           │    AGENT     │           │    AGENT     │   │
│  │              │           │              │           │              │   │
│  │  NIH Query   │           │  PubMed      │           │  RFA Parse   │   │
│  │  ──────────  │           │  ────────    │           │  ──────────  │   │
│  │  47 grants   │           │  23 papers   │           │  8 priorities│   │
│  │  found       │           │  found       │           │  extracted   │   │
│  └──────┬───────┘           └──────┬───────┘           └──────┬───────┘   │
│         │                          │                          │            │
│         └──────────────────────────┴──────────────────────────┘            │
│                                    │                                        │
│                                    ▼                                        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                         ORCHESTRATOR                                  │  │
│  │  ══════════════════════════════════════════════════════════════════  │  │
│  │                                                                       │  │
│  │  STEP 2: MERGE PARALLEL RESULTS                                       │  │
│  │  ──────────────────────────────                                       │  │
│  │  • Combine research findings                                          │  │
│  │  • Deduplicate information                                            │  │
│  │  • Create unified context for next step                               │  │
│  │                                                                       │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                    │                                        │
│                                    ▼                                        │
│                            ┌──────────────┐                                 │
│                            │   ANALYSIS   │                                 │
│                            │    AGENT     │                                 │
│                            │              │                                 │
│                            │  Gap Analysis│                                 │
│                            │  ────────────│                                 │
│                            │  3 key gaps  │                                 │
│                            │  identified  │                                 │
│                            └──────┬───────┘                                 │
│                                   │                                         │
│                                   ▼                                         │
│                            ┌──────────────┐                                 │
│                            │   WRITING    │                                 │
│                            │    AGENT     │                                 │
│                            │              │                                 │
│                            │ Draft Section│                                 │
│                            │ ─────────────│                                 │
│                            │ • 876 words  │                                 │
│                            │ • Style: 82% │                                 │
│                            │ • 2 LLM flags│                                 │
│                            └──────┬───────┘                                 │
│                                   │                                         │
│                                   ▼                                         │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                         ORCHESTRATOR                                  │  │
│  │  ══════════════════════════════════════════════════════════════════  │  │
│  │                                                                       │  │
│  │  STEP 3: FINAL ASSEMBLY                                               │  │
│  │  ─────────────────────                                                │  │
│  │  • Quality check all outputs                                          │  │
│  │  • Compile final deliverables                                         │  │
│  │  • Calculate total cost                                               │  │
│  │  • Generate summary for user                                          │  │
│  │                                                                       │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                    │                                        │
│                                    ▼                                        │
│                            ┌─────────────────┐                              │
│                            │  FINAL OUTPUT   │                              │
│                            │                 │                              │
│                            │ • Research      │                              │
│                            │   Report        │                              │
│                            │ • Draft Section │                              │
│                            │ • Cost Summary  │                              │
│                            └─────────────────┘                              │
│                                                                             │
│  COLLABORATION RULES                                                        │
│  ═══════════════════                                                        │
│  • All agent requests go through orchestrator (no direct agent-to-agent)   │
│  • Cost tracked per agent, per task                                         │
│  • Checkpoints saved after each agent completes                             │
│  • User can inject context at any checkpoint                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 10.2.3 RAG Retrieval Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           RAG RETRIEVAL FLOW                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  USER QUERY (or Agent Request)                                       │   │
│  │                                                                      │   │
│  │  "What preliminary data do I have about CAR-T persistence?"          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                       QUERY PROCESSOR                                │   │
│  │  ─────────────────────────────────────────────────────────────────  │   │
│  │                                                                      │   │
│  │  1. Query Expansion                                                  │   │
│  │     Original: "CAR-T persistence"                                    │   │
│  │     Expanded: ["CAR-T persistence", "chimeric antigen receptor",     │   │
│  │                "T cell exhaustion", "tumor microenvironment"]        │   │
│  │                                                                      │   │
│  │  2. Intent Classification                                            │   │
│  │     Type: Preliminary data search                                    │   │
│  │     Scope: User's documents only                                     │   │
│  │                                                                      │   │
│  │  3. Filter Determination                                             │   │
│  │     doc_type IN ('manuscript', 'figure', 'draft')                   │   │
│  │     project_id = current_project OR project_id IS NULL               │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                       EMBEDDING LOOKUP                               │   │
│  │  ─────────────────────────────────────────────────────────────────  │   │
│  │                                                                      │   │
│  │  Query ──▶ SPECTER2 (Retrieval Adapter) ──▶ Query Vector (768-dim)  │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    HYBRID SEARCH (pgvector)                          │   │
│  │  ─────────────────────────────────────────────────────────────────  │   │
│  │                                                                      │   │
│  │  SELECT chunks.*, embeddings.vector <=> query_vector AS distance     │   │
│  │  FROM doc_chunks chunks                                              │   │
│  │  JOIN embeddings ON chunks.id = embeddings.chunk_id                  │   │
│  │  WHERE doc_type IN ('manuscript', 'figure', 'draft')                 │   │
│  │    AND (project_id = $project OR project_id IS NULL)                 │   │
│  │    AND (                                                             │   │
│  │      chunks.content ILIKE '%CAR-T%'     -- Keyword match             │   │
│  │      OR chunks.content ILIKE '%persistence%'                         │   │
│  │      OR embeddings.vector <=> query_vector < 0.7  -- Vector match    │   │
│  │    )                                                                 │   │
│  │  ORDER BY                                                            │   │
│  │    (keyword_score * 0.3) + (vector_similarity * 0.7) DESC            │   │
│  │  LIMIT 20;                                                           │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         RE-RANKER                                    │   │
│  │  ─────────────────────────────────────────────────────────────────  │   │
│  │                                                                      │   │
│  │  Cross-encoder scoring for top 20 results:                           │   │
│  │                                                                      │   │
│  │  ┌─────────────────────────────────────────────────────────────┐   │   │
│  │  │  Chunk                              │ Vector │ Rerank │ Final│   │   │
│  │  │  ────────────────────────────────────│────────│────────│──────│   │   │
│  │  │  "Fig 3 shows CAR-T persistence..." │ 0.82   │ 0.94   │ 0.91 │   │   │
│  │  │  "Our preliminary data on T cell..."│ 0.78   │ 0.88   │ 0.85 │   │   │
│  │  │  "Previous studies showed..."       │ 0.85   │ 0.65   │ 0.71 │   │   │
│  │  └─────────────────────────────────────────────────────────────┘   │   │
│  │                                                                      │   │
│  │  Re-ranked top 10 returned to user/agent                             │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      CONTEXT ASSEMBLY                                │   │
│  │  ─────────────────────────────────────────────────────────────────  │   │
│  │                                                                      │   │
│  │  For LLM consumption:                                                │   │
│  │                                                                      │   │
│  │  ┌─────────────────────────────────────────────────────────────┐   │   │
│  │  │  RETRIEVED CONTEXT                                          │   │   │
│  │  │                                                              │   │   │
│  │  │  [Source: Fig3_CAR-T_data.pdf, Page 2]                       │   │   │
│  │  │  "Our preliminary data (Figure 3) demonstrates that CAR-T   │   │   │
│  │  │   cells show reduced persistence in hypoxic conditions..."   │   │   │
│  │  │                                                              │   │   │
│  │  │  [Source: Draft_Approach_v2.docx, Section 2.1]               │   │   │
│  │  │  "Building on our published findings, we observed that..."   │   │   │
│  │  │                                                              │   │   │
│  │  └─────────────────────────────────────────────────────────────┘   │   │
│  │                                                                      │   │
│  │  Total tokens: ~2,400 (within context window budget)                │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        LLM RESPONSE                                  │   │
│  │  ─────────────────────────────────────────────────────────────────  │   │
│  │                                                                      │   │
│  │  "Based on your documents, you have the following preliminary       │   │
│  │   data about CAR-T persistence:                                     │   │
│  │                                                                      │   │
│  │   1. Figure 3 from your 2024 manuscript shows reduced CAR-T         │   │
│  │      persistence under hypoxic conditions (p<0.01)                  │   │
│  │                                                                      │   │
│  │   2. Your draft Approach section references additional data on..."  │   │
│  │                                                                      │   │
│  │  [Sources: Fig3_CAR-T_data.pdf, Draft_Approach_v2.docx]             │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  PERFORMANCE: ~500ms for query processing + vector search                  │
│               ~1-3s for LLM response generation                            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 10.2.4 Self-Learning Feedback Loop

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      SELF-LEARNING FEEDBACK LOOP                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    TRIGGER EVENTS                                    │   │
│  │                                                                      │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐    │   │
│  │  │ Document   │  │ Submission │  │ Feedback   │  │ User       │    │   │
│  │  │ Ingested   │  │ Outcome    │  │ Received   │  │ Correction │    │   │
│  │  │            │  │ (funded/   │  │ (review    │  │ (edit/     │    │   │
│  │  │            │  │  declined) │  │  letter)   │  │  reject)   │    │   │
│  │  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘    │   │
│  │        │               │               │               │            │   │
│  │        └───────────────┴───────────────┴───────────────┘            │   │
│  │                                │                                     │   │
│  └────────────────────────────────┼─────────────────────────────────────┘   │
│                                   │                                         │
│                                   ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      LEARNING AGENT                                  │   │
│  │  ═══════════════════════════════════════════════════════════════   │   │
│  │                                                                      │   │
│  │  STYLE LEARNING (on document ingestion)                              │   │
│  │  ───────────────────────────────────────                             │   │
│  │  ┌────────────────────────────────────────────────────────────────┐ │   │
│  │  │  New Document: "Funded_R01_2024.docx"                          │ │   │
│  │  │                                                                │ │   │
│  │  │  1. Extract style features:                                    │ │   │
│  │  │     • Vocabulary: technical_depth=0.82, formality=0.75         │ │   │
│  │  │     • Sentence structure: avg_length=24, complexity=medium     │ │   │
│  │  │     • Argumentation: evidence-first, hedging_rate=0.12         │ │   │
│  │  │                                                                │ │   │
│  │  │  2. Update style profile:                                      │ │   │
│  │  │     • Weight: 2.0x (funded grant)                              │ │   │
│  │  │     • Corpus count: 8 → 9 documents                            │ │   │
│  │  │     • Confidence: 62% → 68%                                    │ │   │
│  │  │                                                                │ │   │
│  │  │  3. Retrain LoRA adapter (background task)                     │ │   │
│  │  └────────────────────────────────────────────────────────────────┘ │   │
│  │                                                                      │   │
│  │  PATTERN LEARNING (on outcome)                                       │   │
│  │  ──────────────────────────────                                      │   │
│  │  ┌────────────────────────────────────────────────────────────────┐ │   │
│  │  │  Outcome: R01-Cancer-2024 → FUNDED (score: 18)                 │ │   │
│  │  │                                                                │ │   │
│  │  │  1. Correlate with writing patterns:                           │ │   │
│  │  │     • Specific Aims: 1 page, 3 aims, clear hypotheses          │ │   │
│  │  │     • Significance: heavy preliminary data references          │ │   │
│  │  │     • Prompt version: writing_specific_aims v2.3               │ │   │
│  │  │                                                                │ │   │
│  │  │  2. Update learned_patterns table:                             │ │   │
│  │  │     • Pattern: "3 aims with clear hypotheses" → success +1     │ │   │
│  │  │     • Pattern: "prelim data in significance" → success +1      │ │   │
│  │  │                                                                │ │   │
│  │  │  3. Update prompt_versions table:                              │ │   │
│  │  │     • writing_specific_aims v2.3: outcome_correlation += 0.05  │ │   │
│  │  └────────────────────────────────────────────────────────────────┘ │   │
│  │                                                                      │   │
│  │  FEEDBACK PARSING (on review received)                               │   │
│  │  ──────────────────────────────────────                              │   │
│  │  ┌────────────────────────────────────────────────────────────────┐ │   │
│  │  │  Feedback: NIH Summary Statement uploaded                      │ │   │
│  │  │                                                                │ │   │
│  │  │  1. Parse structured feedback:                                 │ │   │
│  │  │     • Overall score: 32, Percentile: 22%                       │ │   │
│  │  │     • Approach weakness: "Timeline optimistic"                 │ │   │
│  │  │     • Significance strength: "Addresses important gap"         │ │   │
│  │  │                                                                │ │   │
│  │  │  2. Extract critique patterns:                                 │ │   │
│  │  │     • "Timeline concerns" → 4th occurrence across grants       │ │   │
│  │  │     • Create alert: "Consider adding timeline detail"          │ │   │
│  │  │                                                                │ │   │
│  │  │  3. Store for future reference:                                │ │   │
│  │  │     • Link to project, sections, writing patterns              │ │   │
│  │  └────────────────────────────────────────────────────────────────┘ │   │
│  │                                                                      │   │
│  │  AGENT PERFORMANCE LEARNING (on user action)                         │   │
│  │  ────────────────────────────────────────────                        │   │
│  │  ┌────────────────────────────────────────────────────────────────┐ │   │
│  │  │  User Action: Edited AI-generated draft significantly          │ │   │
│  │  │                                                                │ │   │
│  │  │  1. Calculate edit distance: 0.45 (45% changed)                │ │   │
│  │  │                                                                │ │   │
│  │  │  2. Update agent_performance:                                  │ │   │
│  │  │     • Writing Agent task #1234                                 │ │   │
│  │  │     • user_accepted: true (used the output)                    │ │   │
│  │  │     • edit_distance: 0.45 (high edits = room to improve)       │ │   │
│  │  │     • prompt_version: writing_approach v1.8                    │ │   │
│  │  │                                                                │ │   │
│  │  │  3. If edit_distance > 0.5 frequently:                         │ │   │
│  │  │     • Flag prompt for review                                   │ │   │
│  │  │     • Generate improvement suggestions                         │ │   │
│  │  └────────────────────────────────────────────────────────────────┘ │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                   │                                         │
│                                   ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    PERIODIC BATCH LEARNING                           │   │
│  │  (Weekly Celery job)                                                 │   │
│  │                                                                      │   │
│  │  1. Aggregate agent_performance metrics                              │   │
│  │  2. A/B test analysis: promote winning prompt variants               │   │
│  │  3. Retrain LoRA adapters with new data                             │   │
│  │  4. Update confidence calibration based on accuracy                  │   │
│  │  5. Generate knowledge expansion suggestions                         │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                   │                                         │
│                                   ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    IMPROVEMENTS APPLIED                              │   │
│  │                                                                      │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐      │   │
│  │  │ Better Style    │  │ Improved        │  │ Calibrated      │      │   │
│  │  │ Matching        │  │ Prompts         │  │ Confidence      │      │   │
│  │  │                 │  │                 │  │                 │      │   │
│  │  │ Closer to       │  │ Higher          │  │ More accurate   │      │   │
│  │  │ user voice      │  │ acceptance      │  │ predictions     │      │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘      │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 10.2.5 Submission Tracking & Review Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SUBMISSION TRACKING & REVIEW FLOW                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                              GRANT LIFECYCLE                                │
│                                                                             │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐  │
│  │ DRAFT   │───▶│ SUBMIT  │───▶│ PENDING │───▶│ SCORED  │───▶│ OUTCOME │  │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘  │
│       │              │              │              │              │        │
│       ▼              ▼              ▼              ▼              ▼        │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  DRAFT PHASE                                                         │  │
│  │  ───────────                                                         │  │
│  │  • Documents linked to project                                       │  │
│  │  • Versions tracked (v1, v2, v3...)                                  │  │
│  │  • Compliance checks run                                             │  │
│  │  • Agent tasks logged                                                │  │
│  │                                                                      │  │
│  │  ┌─────────────────────────────────────────────────────────────┐   │  │
│  │  │ Project: R01-Cancer-2024                                     │   │  │
│  │  │ Status: Drafting                                             │   │  │
│  │  │ Deadline: March 5, 2025 (47 days)                            │   │  │
│  │  │                                                              │   │  │
│  │  │ Documents:                                                    │   │  │
│  │  │ ├─ Specific_Aims_v3.docx    ✅ Complete                       │   │  │
│  │  │ ├─ Research_Strategy_v2.docx 🔄 In progress                   │   │  │
│  │  │ ├─ Budget.xlsx              ❌ Not started                    │   │  │
│  │  │ └─ Biosketches/             ✅ 3/3 complete                   │   │  │
│  │  │                                                              │   │  │
│  │  │ Compliance: 78% complete (see 5 issues)                       │   │  │
│  │  └─────────────────────────────────────────────────────────────┘   │  │
│  │                                                                      │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                   │                                        │
│                                   ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  SUBMISSION PHASE                                                    │  │
│  │  ────────────────                                                    │  │
│  │                                                                      │  │
│  │  User clicks "Mark as Submitted"                                     │  │
│  │                                                                      │  │
│  │  ┌─────────────────────────────────────────────────────────────┐   │  │
│  │  │ 📤 SUBMISSION RECORD                                         │   │  │
│  │  │                                                              │   │  │
│  │  │ Submitted: March 5, 2025                                     │   │  │
│  │  │ Tracking #: [Enter NIH tracking number]                      │   │  │
│  │  │ Final Version: [Link final PDF]                              │   │  │
│  │  │                                                              │   │  │
│  │  │ Pre-submission snapshot saved:                               │   │  │
│  │  │ • All document versions locked                               │   │  │
│  │  │ • Agent task history preserved                               │   │  │
│  │  │ • Compliance report archived                                 │   │  │
│  │  │                                                              │   │  │
│  │  │ [Confirm Submission]                                         │   │  │
│  │  └─────────────────────────────────────────────────────────────┘   │  │
│  │                                                                      │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                   │                                        │
│                                   ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  PENDING PHASE                                                       │  │
│  │  ─────────────                                                       │  │
│  │                                                                      │  │
│  │  ┌─────────────────────────────────────────────────────────────┐   │  │
│  │  │ Project: R01-Cancer-2024                                     │   │  │
│  │  │ Status: Submitted → Awaiting Review                          │   │  │
│  │  │ Expected Review: June 2025 (Study Section: ZRG1)             │   │  │
│  │  │                                                              │   │  │
│  │  │ 📅 Add to calendar reminder                                  │   │  │
│  │  │ 📋 Prepare resubmission materials (optional)                 │   │  │
│  │  └─────────────────────────────────────────────────────────────┘   │  │
│  │                                                                      │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                   │                                        │
│                                   ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  SCORED PHASE (Review Received)                                      │  │
│  │  ──────────────────────────────                                      │  │
│  │                                                                      │  │
│  │  User uploads Summary Statement                                      │  │
│  │                                                                      │  │
│  │  ┌─────────────────────────────────────────────────────────────┐   │  │
│  │  │ 📝 REVIEW INGESTION                                          │   │  │
│  │  │                                                              │   │  │
│  │  │ Upload: Summary_Statement_R01CA123456.pdf                    │   │  │
│  │  │ Parser: NIH Structured (auto-detected)                       │   │  │
│  │  │                                                              │   │  │
│  │  │ EXTRACTED DATA:                                              │   │  │
│  │  │ ┌──────────────────────────────────────────────────────────┐ │   │  │
│  │  │ │ Overall Impact: 32        Percentile: 22%                │ │   │  │
│  │  │ │                                                          │ │   │  │
│  │  │ │ Criterion Scores:                                        │ │   │  │
│  │  │ │ ├─ Significance:  3 (Good)                               │ │   │  │
│  │  │ │ ├─ Investigators: 2 (Excellent)                          │ │   │  │
│  │  │ │ ├─ Innovation:    4 (Fair)                               │ │   │  │
│  │  │ │ ├─ Approach:      4 (Fair)  ← Weakness                   │ │   │  │
│  │  │ │ └─ Environment:   2 (Excellent)                          │ │   │  │
│  │  │ │                                                          │ │   │  │
│  │  │ │ Key Concerns Extracted:                                   │ │   │  │
│  │  │ │ • "Timeline appears optimistic for Aim 2"                │ │   │  │
│  │  │ │ • "Power calculation not provided for mouse studies"     │ │   │  │
│  │  │ │ • "Innovation not clearly distinguished from prior work" │ │   │  │
│  │  │ └──────────────────────────────────────────────────────────┘ │   │  │
│  │  │                                                              │   │  │
│  │  │ [Confirm Extraction]  [Edit]  [View Full Statement]          │   │  │
│  │  └─────────────────────────────────────────────────────────────┘   │  │
│  │                                                                      │  │
│  │  → Learning Agent processes feedback for pattern extraction          │  │
│  │  → Critique patterns added to knowledge base                         │  │
│  │                                                                      │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                   │                                        │
│                                   ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  OUTCOME PHASE                                                       │  │
│  │  ─────────────                                                       │  │
│  │                                                                      │  │
│  │  ┌─────────────────────────────────────────────────────────────┐   │  │
│  │  │ 📊 RECORD OUTCOME                                            │   │  │
│  │  │                                                              │   │  │
│  │  │ Outcome: ○ Funded  ● Not Funded  ○ Withdrawn                 │   │  │
│  │  │                                                              │   │  │
│  │  │ ☑ Create resubmission project                                │   │  │
│  │  │   → Copies documents with version suffix "-A1"               │   │  │
│  │  │   → Links to original submission                             │   │  │
│  │  │   → Pre-populates "Response to Reviewers" template           │   │  │
│  │  │                                                              │   │  │
│  │  │ [Save Outcome]                                               │   │  │
│  │  └─────────────────────────────────────────────────────────────┘   │  │
│  │                                                                      │  │
│  │  → Pattern learning triggered                                        │  │
│  │  → Prompt versions correlated with outcome                           │  │
│  │  → Style profile updated based on result                             │  │
│  │                                                                      │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  RESUBMISSION FLOW (if not funded)                                   │  │
│  │  ─────────────────────────────────                                   │  │
│  │                                                                      │  │
│  │  New Project: R01-Cancer-2024-A1                                     │  │
│  │                                                                      │  │
│  │  ┌─────────────────────────────────────────────────────────────┐   │  │
│  │  │ 🔄 RESUBMISSION ASSISTANT                                    │   │  │
│  │  │                                                              │   │  │
│  │  │ Based on reviewer feedback, here are suggested changes:     │   │  │
│  │  │                                                              │   │  │
│  │  │ 1. Approach (Score: 4 → Target: 2)                           │   │  │
│  │  │    ├─ Add detailed timeline for Aim 2                        │   │  │
│  │  │    ├─ Include power calculations                             │   │  │
│  │  │    └─ [Draft Response] [Show in Document]                    │   │  │
│  │  │                                                              │   │  │
│  │  │ 2. Innovation (Score: 4 → Target: 2)                         │   │  │
│  │  │    ├─ Distinguish from competitor approaches                 │   │  │
│  │  │    └─ [Draft Response] [Show in Document]                    │   │  │
│  │  │                                                              │   │  │
│  │  │ Response to Reviewers template ready:                        │   │  │
│  │  │ [Edit Response Document]                                     │   │  │
│  │  └─────────────────────────────────────────────────────────────┘   │  │
│  │                                                                      │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 11. UI Wireframes

**[TODO - To be defined in next iteration]**

This section will include:
- Detailed mockups for each screen
- Component specifications
- Interaction patterns
- Responsive design considerations

---

## 12. Development Phases

### Phase 1a: Core Foundation

**Goal:** Get something working and usable as quickly as possible

**Deliverables:**
- [ ] Web UI shell (React + Tailwind + shadcn/ui)
- [ ] Document upload and viewing (PDF, DOCX)
- [ ] Basic chat interface with single LLM (Claude)
- [ ] Basic project CRUD (create, list, view)
- [ ] PostgreSQL setup with core tables (projects, documents, users)
- [ ] Docker Compose for local development

**Success Criteria:**
- Can create a project, upload documents, and chat about them
- Single-command startup (`docker-compose up`)
- Basic but functional UI

**Dependencies:** None — this is the foundation

---

### Phase 1b: Agent Foundation

**Goal:** Enable autonomous research and basic agentic capabilities

**Deliverables:**
- [ ] Research Agent (web search + NIH Reporter basic)
- [ ] Agent task queue (Celery + Redis)
- [ ] Real-time activity streaming (WebSocket)
- [ ] Folder watching system (Watchdog)
- [ ] Document processing pipeline (text extraction, chunking)
- [ ] pgvector setup for embeddings
- [ ] Basic RAG retrieval

**Success Criteria:**
- Can launch a research task and see live progress
- Agent can search NIH Reporter and return results
- Documents are searchable via semantic search

**Dependencies:** Phase 1a complete

---

### Phase 2: Core Agents

**Goal:** Full agent functionality with collaboration

**Deliverables:**
- [ ] Research Agent (full: web search, NIH Reporter, PubMed, arXiv)
- [ ] Writing Agent (drafting, basic tone controls)
- [ ] Compliance Agent (RFA parsing, checklist generation)
- [ ] Orchestrator collaboration protocol (agent-to-agent)
- [ ] Mid-task context injection
- [ ] Pause/resume/cancel with checkpointing
- [ ] Cost tracking per task

**Success Criteria:**
- Agents can collaborate (Research → Writing handoff)
- Can draft grant sections with references to your documents
- Can parse RFA and generate interactive checklist

**Dependencies:** Phase 1b complete

---

### Phase 3: RAG & Learning

**Goal:** Self-learning system that improves over time

**Deliverables:**
- [ ] Style profile learning (confidence tiers)
- [ ] Auto-weighting of style corpus
- [ ] Feedback ingestion system (reviewer comments)
- [ ] Parser templates (NIH, NSF, Foundation, Generic)
- [ ] Pattern extraction from outcomes
- [ ] Anti-LLM detection (balanced mode)
- [ ] Confidence indicators throughout UI

**Success Criteria:**
- System learns your writing style from 10+ documents
- Can parse NIH summary statements into structured data
- Writing output includes style match confidence score

**Dependencies:** Phase 2 complete

---

### Phase 4: Advanced Features

**Goal:** Full feature set including creative and analysis capabilities

**Deliverables:**
- [ ] Creative Agent (Nano Banana / DALL-E integration for figures)
- [ ] Analysis Agent (figure interpretation, data synthesis)
- [ ] ReadCube integration (with RIS/BibTeX fallback)
- [ ] Review & Learn mode UI
- [ ] Submission tracking dashboard
- [ ] Learning Agent (automated pattern discovery)

**Success Criteria:**
- Can generate scientific figures from descriptions
- Can analyze uploaded figures and summarize findings
- References sync from ReadCube or import via files
- Full submission → outcome → learning loop working

**Dependencies:** Phase 3 complete

---

### Phase 5: Polish & Production

**Goal:** Production-ready stability with all edge cases handled

**Deliverables:**
- [ ] Proactive alerts system (deadlines, new RFAs)
- [ ] Pre-submission audit reports
- [ ] Ollama fallback (offline mode)
- [ ] Cost optimization suggestions
- [ ] Export to Word (clean, formatted)
- [ ] Comprehensive backup/recovery system
- [ ] Offline/sync conflict handling
- [ ] Security hardening (API key encryption)

**Success Criteria:**
- Production-ready stability
- Graceful handling of network failures, crashes
- Smooth user experience across all modes
- All security best practices implemented

**Dependencies:** Phase 4 complete

---

## 13. Appendices

### Appendix A: Cost Tracking UI

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 💰 COST TRACKING                                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ ┌─ Global Usage (This Month) ──────────────────────────────────────────────┐│
│ │                                                                          ││
│ │  Total Spent: $12.47 / $50.00 budget                                     ││
│ │  ████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░  24.9%                 ││
│ │                                                                          ││
│ │  By Provider:                                                            ││
│ │  • Anthropic (Claude):  $8.23  (66%)                                     ││
│ │  • OpenAI (GPT-4):      $3.12  (25%)                                     ││
│ │  • Nano Banana:         $0.89  (7%)                                      ││
│ │  • OpenAI (DALL-E):     $0.23  (2%)                                      ││
│ │  • Ollama (local):      $0.00  (free)                                    ││
│ │                                                                          ││
│ └──────────────────────────────────────────────────────────────────────────┘│
│                                                                             │
│ ┌─ By Project ─────────────────────────────────────────────────────────────┐│
│ │                                                                          ││
│ │  Project                  Budget      Used        Remaining    Status    ││
│ │  ─────────────────────────────────────────────────────────────────────── ││
│ │  R01-Cancer-2024          $20.00      $7.82       $12.18       ✓ OK      ││
│ │  K99-Neuroscience         $15.00      $3.45       $11.55       ✓ OK      ││
│ │  NSF-CAREER-2025          $10.00      $8.92       $1.08        ⚠ 89%     ││
│ │  Foundation-Pilot         $5.00       $5.00       $0.00        🛑 Limit  ││
│ │                                                                          ││
│ └──────────────────────────────────────────────────────────────────────────┘│
│                                                                             │
│ ┌─ Budget Alerts Configuration ────────────────────────────────────────────┐│
│ │                                                                          ││
│ │  ☑ Warn at 80% of project budget                                         ││
│ │  ☑ Warn at 90% of project budget                                         ││
│ │  ☑ Hard stop at 100% (require manual override)                           ││
│ │                                                                          ││
│ └──────────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────────┘
```

### Appendix B: Glossary

| Term | Definition |
|------|------------|
| **RFA** | Request for Applications — funding announcement from agencies |
| **RAG** | Retrieval-Augmented Generation — AI technique using document retrieval |
| **Agent** | Autonomous AI component that performs tasks without step-by-step guidance |
| **Co-pilot** | Interactive AI assistant mode with human-in-the-loop |
| **pgvector** | PostgreSQL extension for vector similarity search |
| **PMID** | PubMed ID — unique identifier for biomedical literature |
| **DOI** | Digital Object Identifier — persistent identifier for documents |

### Appendix C: External API Dependencies

| Service | Purpose | Required |
|---------|---------|----------|
| Anthropic API | Claude LLM | Yes |
| OpenAI API | GPT-4, Embeddings | Yes |
| Nano Banana API | Image generation (primary) | Yes |
| OpenAI DALL-E | Image generation (fallback) | Optional |
| NIH Reporter API | Funded grants database | Yes |
| PubMed API | Literature search | Yes |
| ReadCube API | Reference manager sync | Optional |
| Ollama | Local LLM fallback | Optional |

### Appendix D: Offline/Sync Strategy

**Problem:** User may work offline, Dropbox folders may update while app is closed, conflicts may arise.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    OFFLINE/SYNC STATE MACHINE                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  STATES                                                                     │
│  ══════                                                                     │
│                                                                             │
│  [ONLINE]  ←→  [DEGRADED]  ←→  [OFFLINE]                                   │
│      │              │               │                                       │
│      │              │               │                                       │
│      ▼              ▼               ▼                                       │
│  Full cloud     Ollama only    Local only                                   │
│  LLM + sync     for LLM        (read/edit)                                  │
│                                                                             │
│  TRANSITIONS                                                                │
│  ═══════════                                                                │
│                                                                             │
│  ONLINE → DEGRADED: Cloud LLM API unreachable                              │
│  DEGRADED → OFFLINE: All network unavailable                               │
│  OFFLINE → ONLINE: Network restored, sync triggered                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Sync Behavior:**

| Scenario | Behavior |
|----------|----------|
| **App starts, Dropbox changed** | Scan watched folders, detect changes, prompt user: "5 files added, 2 modified. Process now?" |
| **File modified locally + remotely** | Conflict detection by timestamp + hash. Show diff, let user choose or merge |
| **File deleted in Dropbox** | Mark as "missing source" in DB, don't auto-delete (data safety) |
| **Agent task running, network drops** | Checkpoint task, switch to Ollama if available, or pause with "Network lost" status |
| **Offline edits to project** | Queue changes locally, sync when back online |

**Conflict Resolution UI:**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ ⚠️ SYNC CONFLICT — Specific_Aims_v3.docx                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ This file was modified in both locations:                                   │
│                                                                             │
│ LOCAL (GrantPilot)              REMOTE (Dropbox)                            │
│ Modified: Jan 10, 2:30 PM       Modified: Jan 10, 3:15 PM                   │
│ By: AI edit (Writing Agent)     By: External edit                           │
│                                                                             │
│ [Keep Local]  [Keep Remote]  [Keep Both]  [View Diff]                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Appendix E: Security Considerations

**Threat Model:** Single-user local application, but handles sensitive research and API keys.

| Area | Risk | Mitigation |
|------|------|------------|
| **API Keys** | Keys stored in plaintext could be extracted | Encrypt at rest using OS keychain (macOS Keychain, Windows Credential Manager) or encrypted config file |
| **Grant Content** | Sensitive research data | All data stays local. No telemetry. Optional local-only mode (Ollama) |
| **LLM Transmission** | Grant text sent to cloud APIs | Document this clearly. User consent on first use. Consider offering chunk-level consent for sensitive sections |
| **Database** | PostgreSQL accessible locally | Bind to localhost only. Optional PIN lock for app access |
| **Backups** | Backup files contain full database | Encrypt backup files with user-provided password or derived key |
| **Dependencies** | Supply chain attacks | Pin dependency versions. Use lockfiles. Periodic security audits |

**Implementation:**

```yaml
Security_Implementation:
  api_keys:
    storage: OS keychain (preferred) or encrypted file
    encryption: AES-256-GCM
    key_derivation: User PIN → PBKDF2 → encryption key
    never: Store in plaintext, commit to git, log to console

  database:
    binding: 127.0.0.1 only (no network access)
    authentication: Local socket or password (for Docker)
    backup_encryption: Optional, user-configurable

  network:
    llm_apis: HTTPS only, verify certificates
    local_dev: No external access required except LLM APIs
    telemetry: None. Zero data collection.

  user_consent:
    first_run:
      - Explain what data goes to cloud LLM APIs
      - Offer Ollama-only mode for maximum privacy
      - Document what's stored locally
    per_session:
      - Show active LLM provider in status bar
```

### Appendix F: Error Recovery & Crash Handling

**Philosophy:** Never lose user work. Graceful degradation. Clear communication.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ERROR RECOVERY MATRIX                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ERROR TYPE              │ DETECTION        │ RECOVERY                      │
│  ─────────────────────────────────────────────────────────────────────────  │
│  App crash               │ Process monitor  │ Auto-restart, restore state   │
│  Browser tab closed      │ WS disconnect    │ Backend continues, rejoin OK  │
│  LLM API timeout         │ Request timeout  │ Retry 3x, then fallback/fail  │
│  LLM API error           │ HTTP 4xx/5xx     │ Log, notify user, suggest fix │
│  Database corruption     │ Query failure    │ Alert, restore from WAL/backup│
│  Disk full               │ Write failure    │ Alert, pause operations       │
│  Agent task hang         │ Timeout          │ Kill, checkpoint, notify      │
│  Network loss mid-task   │ Request failure  │ Pause, checkpoint, queue      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Agent Task Recovery:**

```yaml
Task_Checkpointing:
  frequency: Every 30 seconds during active task
  checkpoint_includes:
    - Current step/progress
    - Accumulated results so far
    - Context (what's been retrieved/generated)
    - Token/cost usage
    - User injections received

  on_crash:
    detection: Task status stuck in "running" for > checkpoint_interval + buffer
    recovery_options:
      - Resume from checkpoint (if data intact)
      - Restart from beginning (if checkpoint corrupt)
      - Cancel with partial results
    user_prompt: "Task 'Research CAR-T landscape' was interrupted. Resume from 65% or restart?"

  partial_results:
    always_save: true
    accessible_via: "View partial results" button even for failed/cancelled tasks
```

**Backup Recovery:**

```yaml
Backup_System:
  continuous:
    method: PostgreSQL WAL (Write-Ahead Logging)
    retention: 24 hours of point-in-time recovery

  scheduled:
    hourly: State snapshot (lightweight, incremental)
    daily: Full database dump to backup folder
    weekly: Compressed archive with verification checksum

  recovery_scenarios:
    app_crash:
      - Auto-restart via Docker restart policy
      - Detect incomplete tasks, offer resume
      - No data loss (WAL ensures durability)

    database_corruption:
      - Detect via query errors or integrity checks
      - Offer: "Restore from backup?" with list of available backups
      - Show backup age and estimated data loss

    full_system_restore:
      - User runs: ./scripts/restore.py --backup backup_2025-01-10.sql.gz
      - Restores database + document index
      - Triggers re-embedding only if needed
```

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | January 2025 | Initial comprehensive specification |
| 1.1 | January 2025 | Added complete API contracts (Section 8) |
| 1.2 | January 2025 | Added: Orchestrator collaboration protocol (4.2), Style confidence tiers (5.2), ReadCube fallbacks (5.3), Feedback parser templates (5.5), Confidence indicators UI (3.6), Split Phase 1 into 1a/1b, Appendices D/E/F (sync, security, error recovery) |

---

## Outstanding TODOs

- [x] **Section 8:** Define detailed API contracts ✅ Complete — see `grantpilot-api-contracts.md`
- [x] **Section 9:** Create agent prompt templates ✅ Complete — see `grantpilot-agent-prompts.md`
- [ ] **Section 10:** Design workflow diagrams ← **NEXT**
- [ ] **Section 11:** Create detailed UI wireframes
- [ ] **Additional:** Define testing strategy
- [ ] **Additional:** Create deployment guide
- [x] **Additional:** Define security considerations ✅ Complete — see Appendix E

---

*End of Specification Document*

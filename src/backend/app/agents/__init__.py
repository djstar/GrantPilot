"""
GrantPilot Agent System

Specialized AI agents for grant writing tasks:
- WritingAgent: Generates grant section drafts
- ResearchAgent: Gathers competitive intelligence (Phase 2)
- ComplianceAgent: Checks RFA requirements (Phase 2)
- CreativeAgent: Generates figures (Phase 2)
- AnalysisAgent: Analyzes data and literature (Phase 2)
- ReviewAgent: Adversarial multi-LLM review (Phase 1c)
"""

from app.agents.base import BaseAgent, AgentConfig, AgentResult
from app.agents.writing import WritingAgent

__all__ = [
    "BaseAgent",
    "AgentConfig",
    "AgentResult",
    "WritingAgent",
]

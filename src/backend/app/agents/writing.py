"""
Writing Agent for GrantPilot.

Generates grant section drafts using RAG context and LLM.
Supports all standard NIH grant sections.
"""

import logging
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel

from app.agents.base import (
    BaseAgent,
    AgentConfig,
    AgentResult,
    AgentType,
    AgentStatus,
)
from app.services.chat import ChatService
from app.services.search import SearchService
from app.services.embeddings import EmbeddingService
from app.websocket.manager import manager
from app.websocket.events import AgentStatusEvent, TaskProgressEvent

logger = logging.getLogger(__name__)


class GrantSection(str, Enum):
    """Standard NIH grant sections"""
    SPECIFIC_AIMS = "specific_aims"
    SIGNIFICANCE = "significance"
    INNOVATION = "innovation"
    APPROACH = "approach"
    PRELIMINARY_DATA = "preliminary_data"
    TIMELINE = "timeline"
    BUDGET_JUSTIFICATION = "budget_justification"
    FACILITIES = "facilities"
    EQUIPMENT = "equipment"
    BIBLIOGRAPHY = "bibliography"


class WritingInput(BaseModel):
    """Input for Writing Agent"""
    section: GrantSection
    project_id: UUID
    project_title: str
    project_description: Optional[str] = None

    # Optional context
    rfa_requirements: Optional[str] = None
    previous_feedback: Optional[str] = None
    user_notes: Optional[str] = None

    # Style settings
    formality: float = 0.8  # 0-1, higher = more formal
    technical_depth: float = 0.7  # 0-1, higher = more technical
    max_words: int = 500


class WritingAgent(BaseAgent):
    """
    Agent for generating grant section drafts.

    Features:
    - RAG-based context retrieval from user's documents
    - Section-specific prompts
    - Style adaptation (formality, technical depth)
    - Real-time progress updates via WebSocket
    """

    agent_type = AgentType.WRITING

    # Section-specific guidance
    SECTION_GUIDANCE = {
        GrantSection.SPECIFIC_AIMS: """
Structure the Specific Aims page as follows:
1. Opening paragraph: Hook with the problem and its significance
2. Gap in knowledge: What is unknown that this research will address
3. Long-term goal and objective: Career trajectory and immediate purpose
4. Central hypothesis: Testable, mechanistic statement
5. Rationale: Why this approach will work
6. Specific Aims (2-3): Clear, measurable objectives
7. Expected outcomes and impact: What will be achieved

Keep to ~1 page (500 words). Each aim should be independent yet synergistic.
Avoid jargon. Write in future tense for proposed work.
""",
        GrantSection.SIGNIFICANCE: """
Address these key questions:
1. What is the clinical/scientific problem?
2. What is the current state of knowledge?
3. What are the barriers to progress?
4. How will this research advance the field?
5. What is the potential impact on human health?

Be specific about gaps in knowledge. Cite key literature.
Explain why solving this problem matters NOW.
""",
        GrantSection.INNOVATION: """
Highlight what is NEW about:
1. Conceptual/theoretical approach
2. Technical/methodological approach
3. Instrumentation or resources

Avoid claiming innovation without justification.
Be specific: "This is the first study to..." or "Unlike prior approaches..."
Innovation can be incremental - focus on meaningful advances.
""",
        GrantSection.APPROACH: """
For each Specific Aim, include:
1. Rationale: Why this aim and approach
2. Experimental design: Clear methods with controls
3. Expected results: What you anticipate
4. Potential problems: Honest assessment of risks
5. Alternative approaches: Backup plans

Include preliminary data to demonstrate feasibility.
Be specific about sample sizes, statistical approaches, and timelines.
""",
        GrantSection.PRELIMINARY_DATA: """
Present data that demonstrates:
1. Feasibility of the proposed approach
2. Your expertise in the methods
3. Initial support for your hypothesis

Each figure should have a clear purpose.
Interpret results honestly - acknowledge limitations.
Connect preliminary data to proposed experiments.
""",
    }

    def __init__(self, config: AgentConfig, db_session=None):
        super().__init__(config)
        self.db_session = db_session
        self.chat_service = ChatService()
        self.search_service = SearchService()
        self.embedding_service = EmbeddingService()

    def get_system_prompt(self) -> str:
        return """You are an expert NIH grant writing assistant with extensive experience
in biomedical research and successful grant applications. You help researchers
draft compelling, scientifically rigorous grant sections.

Your writing should be:
- Clear and accessible to non-specialists on the review panel
- Scientifically precise and mechanistic
- Well-structured with clear transitions
- Free of unnecessary jargon
- Persuasive without being hyperbolic

Always ground your writing in the provided context and research materials.
If you don't have enough information for a specific detail, note what the
researcher should add rather than making up information.
"""

    async def execute(self, input_data: Dict[str, Any]) -> AgentResult:
        """
        Generate a grant section draft.

        Args:
            input_data: WritingInput as dict

        Returns:
            AgentResult with draft content
        """
        # Parse input
        try:
            writing_input = WritingInput(**input_data)
        except Exception as e:
            return self._create_result(
                status=AgentStatus.FAILED,
                error_message=f"Invalid input: {e}",
            )

        # Broadcast start
        await self._broadcast_status("starting", f"Starting {writing_input.section.value} draft")

        # Step 1: Retrieve relevant context
        self.update_checkpoint("retrieving_context", 0, total_steps=4)
        await self._broadcast_progress(0, 4, "Retrieving context", "Searching your documents...")

        context = await self._retrieve_context(writing_input)

        if self.is_cancelled:
            return self._create_result(status=AgentStatus.CANCELLED)

        # Step 2: Build prompt
        self.update_checkpoint("building_prompt", 1, total_steps=4)
        await self._broadcast_progress(1, 4, "Building prompt", "Preparing writing instructions...")

        prompt = self._build_prompt(writing_input, context)

        if self.is_cancelled:
            return self._create_result(status=AgentStatus.CANCELLED)

        # Step 3: Generate draft
        self.update_checkpoint("generating_draft", 2, total_steps=4)
        await self._broadcast_progress(2, 4, "Generating draft", "Writing section content...")

        draft = await self._generate_draft(prompt, writing_input)

        if self.is_cancelled:
            return self._create_result(status=AgentStatus.CANCELLED)

        # Step 4: Format output
        self.update_checkpoint("formatting", 3, total_steps=4)
        await self._broadcast_progress(3, 4, "Formatting", "Finalizing draft...")

        # Broadcast completion
        await self._broadcast_status("completed", f"Completed {writing_input.section.value} draft")

        return self._create_result(
            status=AgentStatus.COMPLETED,
            output=draft,
            output_sections={writing_input.section.value: draft},
        )

    async def _retrieve_context(self, input: WritingInput) -> str:
        """Retrieve relevant context from user's documents"""
        if not self.config.use_rag:
            return ""

        try:
            # Build search query based on section
            query = self._build_search_query(input)

            # Search for relevant chunks
            results = await self.search_service.search(
                query=query,
                project_id=input.project_id,
                limit=self.config.max_context_chunks,
                db=self.db_session,
            )

            if not results:
                return ""

            # Format context
            context_parts = []
            for i, result in enumerate(results, 1):
                context_parts.append(f"[Source {i}]\n{result['content']}\n")

            return "\n".join(context_parts)

        except Exception as e:
            logger.warning(f"Context retrieval failed: {e}")
            return ""

    def _build_search_query(self, input: WritingInput) -> str:
        """Build a search query for the section type"""
        section_queries = {
            GrantSection.SPECIFIC_AIMS: f"specific aims hypothesis objectives {input.project_title}",
            GrantSection.SIGNIFICANCE: f"significance importance clinical impact {input.project_title}",
            GrantSection.INNOVATION: f"innovation novel approach new methods {input.project_title}",
            GrantSection.APPROACH: f"methods experimental design approach {input.project_title}",
            GrantSection.PRELIMINARY_DATA: f"preliminary data results findings {input.project_title}",
        }
        return section_queries.get(input.section, input.project_title)

    def _build_prompt(self, input: WritingInput, context: str) -> str:
        """Build the full prompt for LLM"""
        section_guidance = self.SECTION_GUIDANCE.get(input.section, "")

        prompt_parts = [
            f"# Task: Write the {input.section.value.replace('_', ' ').title()} section",
            "",
            f"## Project Title\n{input.project_title}",
        ]

        if input.project_description:
            prompt_parts.extend([
                "",
                f"## Project Description\n{input.project_description}",
            ])

        if context:
            prompt_parts.extend([
                "",
                "## Relevant Context from Your Documents",
                context,
            ])

        if input.rfa_requirements:
            prompt_parts.extend([
                "",
                "## RFA Requirements to Address",
                input.rfa_requirements,
            ])

        if input.previous_feedback:
            prompt_parts.extend([
                "",
                "## Previous Reviewer Feedback to Address",
                input.previous_feedback,
            ])

        if input.user_notes:
            prompt_parts.extend([
                "",
                "## Additional Notes from Researcher",
                input.user_notes,
            ])

        if section_guidance:
            prompt_parts.extend([
                "",
                "## Section-Specific Guidelines",
                section_guidance,
            ])

        prompt_parts.extend([
            "",
            "## Style Requirements",
            f"- Formality level: {'High' if input.formality > 0.7 else 'Medium' if input.formality > 0.4 else 'Low'}",
            f"- Technical depth: {'High' if input.technical_depth > 0.7 else 'Medium' if input.technical_depth > 0.4 else 'Low'}",
            f"- Target length: ~{input.max_words} words",
            "",
            "## Instructions",
            "Write a draft for this section. Use the context provided but don't fabricate specific data.",
            "Mark any areas where the researcher needs to add specific information with [TODO: ...].",
            "Focus on clarity and scientific rigor.",
        ])

        return "\n".join(prompt_parts)

    async def _generate_draft(self, prompt: str, input: WritingInput) -> str:
        """Generate the draft using LLM"""
        try:
            # Use chat service for generation
            response = await self.chat_service.generate(
                messages=[
                    {"role": "system", "content": self.get_system_prompt()},
                    {"role": "user", "content": prompt},
                ],
                model=self.config.model,
                temperature=self.config.temperature,
                max_tokens=input.max_words * 2,  # Rough token estimate
            )

            # Track tokens
            if response.get("usage"):
                self.track_tokens(
                    prompt_tokens=response["usage"].get("prompt_tokens", 0),
                    completion_tokens=response["usage"].get("completion_tokens", 0),
                    cost=response.get("cost", 0.0),
                )

            return response.get("content", "")

        except Exception as e:
            logger.error(f"Draft generation failed: {e}")
            raise

    async def _broadcast_status(self, status: str, message: str):
        """Broadcast agent status via WebSocket"""
        event = AgentStatusEvent(
            task_id=self.task_id,
            agent_type=self.agent_type.value,
            status=status,
            message=message,
            tokens_used=self.prompt_tokens + self.completion_tokens,
            cost_incurred=self.cost_usd,
        )
        await manager.broadcast(event.to_event())

    async def _broadcast_progress(
        self,
        step_index: int,
        total_steps: int,
        step_name: str,
        description: str,
    ):
        """Broadcast task progress via WebSocket"""
        event = TaskProgressEvent(
            task_id=self.task_id,
            step_index=step_index,
            total_steps=total_steps,
            step_name=step_name,
            step_description=description,
            completed_items=self.checkpoint.completed_items,
        )
        await manager.broadcast(event.to_event())

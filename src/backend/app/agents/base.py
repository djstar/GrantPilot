"""
Base Agent class for GrantPilot agent system.

All agents inherit from BaseAgent and implement the execute() method.
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class AgentType(str, Enum):
    """Agent type identifiers"""
    WRITING = "writing"
    RESEARCH = "research"
    COMPLIANCE = "compliance"
    CREATIVE = "creative"
    ANALYSIS = "analysis"
    REVIEW = "review"
    LEARNING = "learning"


class AgentStatus(str, Enum):
    """Agent execution status"""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentConfig(BaseModel):
    """Configuration for agent execution"""
    # Task identification
    task_id: UUID = field(default_factory=uuid4)
    project_id: Optional[UUID] = None

    # Time and resource limits
    time_limit_minutes: int = 30
    max_tokens: int = 100000
    max_cost_usd: float = 5.0

    # LLM settings
    model: str = "claude-sonnet-4-20250514"
    temperature: float = 0.7

    # Context settings
    use_rag: bool = True
    max_context_chunks: int = 10

    # Collaboration
    depth_level: int = 0  # 0=root, max 3
    parent_task_id: Optional[UUID] = None

    class Config:
        arbitrary_types_allowed = True


class AgentResult(BaseModel):
    """Result from agent execution"""
    task_id: UUID
    agent_type: AgentType
    status: AgentStatus

    # Output
    output: Optional[str] = None
    output_sections: Dict[str, str] = field(default_factory=dict)

    # Metadata
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_seconds: float = 0.0

    # Token usage
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cost_usd: float = 0.0

    # Error info
    error_message: Optional[str] = None

    # Checkpoint for resume
    checkpoint: Dict[str, Any] = field(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True


@dataclass
class AgentCheckpoint:
    """Checkpoint state for crash recovery"""
    version: int = 1
    last_step: str = ""
    step_index: int = 0
    total_steps: Optional[int] = None
    completed_items: List[str] = field(default_factory=list)
    interim_results: Dict[str, Any] = field(default_factory=dict)
    context_state: Dict[str, Any] = field(default_factory=dict)
    tokens_at_checkpoint: int = 0
    timestamp: datetime = field(default_factory=datetime.utcnow)


class BaseAgent(ABC):
    """
    Base class for all GrantPilot agents.

    Subclasses must implement:
    - execute(): Main task execution logic
    - get_system_prompt(): Agent-specific system prompt
    """

    agent_type: AgentType = AgentType.WRITING

    def __init__(self, config: AgentConfig):
        self.config = config
        self.task_id = config.task_id
        self.status = AgentStatus.PENDING
        self.checkpoint = AgentCheckpoint()

        # Token tracking
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.cost_usd = 0.0

        # Timing
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None

        # Cancellation
        self._cancelled = False
        self._paused = False

    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> AgentResult:
        """
        Execute the agent's main task.

        Args:
            input_data: Task-specific input data

        Returns:
            AgentResult with output and metadata
        """
        pass

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Get the agent's system prompt"""
        pass

    async def run(self, input_data: Dict[str, Any]) -> AgentResult:
        """
        Run the agent with lifecycle management.

        Handles:
        - Status transitions
        - Timing
        - Error handling
        - Checkpointing
        """
        self.started_at = datetime.utcnow()
        self.status = AgentStatus.RUNNING

        try:
            # Execute main task
            result = await self.execute(input_data)

            self.completed_at = datetime.utcnow()
            self.status = AgentStatus.COMPLETED

            return result

        except asyncio.CancelledError:
            self.status = AgentStatus.CANCELLED
            self.completed_at = datetime.utcnow()
            return self._create_result(
                status=AgentStatus.CANCELLED,
                error_message="Task was cancelled",
            )

        except Exception as e:
            logger.error(f"Agent {self.agent_type} failed: {e}", exc_info=True)
            self.status = AgentStatus.FAILED
            self.completed_at = datetime.utcnow()
            return self._create_result(
                status=AgentStatus.FAILED,
                error_message=str(e),
            )

    def _create_result(
        self,
        status: AgentStatus,
        output: Optional[str] = None,
        output_sections: Optional[Dict[str, str]] = None,
        error_message: Optional[str] = None,
    ) -> AgentResult:
        """Create an AgentResult with current state"""
        duration = 0.0
        if self.started_at:
            end = self.completed_at or datetime.utcnow()
            duration = (end - self.started_at).total_seconds()

        return AgentResult(
            task_id=self.task_id,
            agent_type=self.agent_type,
            status=status,
            output=output,
            output_sections=output_sections or {},
            started_at=self.started_at,
            completed_at=self.completed_at,
            duration_seconds=duration,
            prompt_tokens=self.prompt_tokens,
            completion_tokens=self.completion_tokens,
            total_tokens=self.prompt_tokens + self.completion_tokens,
            cost_usd=self.cost_usd,
            error_message=error_message,
            checkpoint=self.checkpoint.__dict__,
        )

    def update_checkpoint(
        self,
        step: str,
        step_index: int,
        total_steps: Optional[int] = None,
        completed_item: Optional[str] = None,
        interim_result: Optional[Dict[str, Any]] = None,
    ):
        """Update checkpoint for crash recovery"""
        self.checkpoint.last_step = step
        self.checkpoint.step_index = step_index
        self.checkpoint.total_steps = total_steps
        self.checkpoint.tokens_at_checkpoint = self.prompt_tokens + self.completion_tokens
        self.checkpoint.timestamp = datetime.utcnow()

        if completed_item:
            self.checkpoint.completed_items.append(completed_item)

        if interim_result:
            self.checkpoint.interim_results.update(interim_result)

    def cancel(self):
        """Request cancellation"""
        self._cancelled = True

    def pause(self):
        """Pause execution"""
        self._paused = True
        self.status = AgentStatus.PAUSED

    def resume(self):
        """Resume execution"""
        self._paused = False
        self.status = AgentStatus.RUNNING

    @property
    def is_cancelled(self) -> bool:
        return self._cancelled

    @property
    def is_paused(self) -> bool:
        return self._paused

    def track_tokens(self, prompt_tokens: int, completion_tokens: int, cost: float):
        """Track token usage and cost"""
        self.prompt_tokens += prompt_tokens
        self.completion_tokens += completion_tokens
        self.cost_usd += cost

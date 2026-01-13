"""
WebSocket event types for GrantPilot real-time updates.

Event structure follows a consistent pattern:
{
    "type": "event_type",
    "payload": { ... event-specific data ... },
    "timestamp": "ISO8601 timestamp"
}
"""

from datetime import datetime
from enum import Enum
from typing import Any, Optional, Dict, List
from pydantic import BaseModel, Field
from uuid import UUID


class EventType(str, Enum):
    """WebSocket event types"""
    # Connection events
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    HEARTBEAT = "heartbeat"

    # Agent events
    AGENT_STATUS = "agent_status"
    AGENT_STARTED = "agent_started"
    AGENT_COMPLETED = "agent_completed"
    AGENT_FAILED = "agent_failed"
    AGENT_PAUSED = "agent_paused"
    AGENT_RESUMED = "agent_resumed"

    # Task events
    TASK_PROGRESS = "task_progress"
    TASK_CHECKPOINT = "task_checkpoint"

    # Chat events
    CHAT_STREAM = "chat_stream"
    CHAT_COMPLETE = "chat_complete"

    # Document events
    DOCUMENT_PROCESSING = "document_processing"
    DOCUMENT_READY = "document_ready"
    DOCUMENT_FAILED = "document_failed"

    # Notification events
    NOTIFICATION = "notification"

    # Cost events
    COST_UPDATE = "cost_update"
    BUDGET_WARNING = "budget_warning"


class WebSocketEvent(BaseModel):
    """Base WebSocket event structure"""
    type: EventType
    payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    def to_json(self) -> dict:
        """Convert to JSON-serializable dict"""
        return {
            "type": self.type.value,
            "payload": self.payload,
            "timestamp": self.timestamp.isoformat(),
        }


class AgentStatusEvent(BaseModel):
    """Agent status update event"""
    task_id: UUID
    agent_type: str
    status: str  # pending, running, paused, completed, failed
    message: Optional[str] = None
    progress_percent: Optional[int] = None
    current_step: Optional[str] = None
    tokens_used: int = 0
    cost_incurred: float = 0.0

    def to_event(self) -> WebSocketEvent:
        return WebSocketEvent(
            type=EventType.AGENT_STATUS,
            payload=self.model_dump(mode="json"),
        )


class TaskProgressEvent(BaseModel):
    """Task progress update event"""
    task_id: UUID
    step_index: int
    total_steps: Optional[int] = None
    step_name: str
    step_description: Optional[str] = None
    completed_items: List[str] = Field(default_factory=list)

    def to_event(self) -> WebSocketEvent:
        return WebSocketEvent(
            type=EventType.TASK_PROGRESS,
            payload=self.model_dump(mode="json"),
        )


class ChatStreamEvent(BaseModel):
    """Chat streaming token event"""
    conversation_id: Optional[UUID] = None
    chunk: str
    is_final: bool = False
    sources: List[Dict[str, Any]] = Field(default_factory=list)

    def to_event(self) -> WebSocketEvent:
        return WebSocketEvent(
            type=EventType.CHAT_STREAM if not self.is_final else EventType.CHAT_COMPLETE,
            payload=self.model_dump(mode="json"),
        )


class NotificationEvent(BaseModel):
    """User notification event"""
    level: str = "info"  # info, success, warning, error
    title: str
    message: str
    action_url: Optional[str] = None
    auto_dismiss: bool = True
    dismiss_after_ms: int = 5000

    def to_event(self) -> WebSocketEvent:
        return WebSocketEvent(
            type=EventType.NOTIFICATION,
            payload=self.model_dump(mode="json"),
        )


class DocumentProcessingEvent(BaseModel):
    """Document processing status event"""
    document_id: UUID
    filename: str
    status: str  # uploading, processing, chunking, embedding, ready, failed
    progress_percent: int = 0
    chunks_created: int = 0
    error_message: Optional[str] = None

    def to_event(self) -> WebSocketEvent:
        event_type = EventType.DOCUMENT_PROCESSING
        if self.status == "ready":
            event_type = EventType.DOCUMENT_READY
        elif self.status == "failed":
            event_type = EventType.DOCUMENT_FAILED

        return WebSocketEvent(
            type=event_type,
            payload=self.model_dump(mode="json"),
        )


class CostUpdateEvent(BaseModel):
    """Cost tracking update event"""
    project_id: Optional[UUID] = None
    task_id: Optional[UUID] = None
    provider: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    cost_usd: float
    cumulative_cost_usd: float
    budget_remaining: Optional[float] = None

    def to_event(self) -> WebSocketEvent:
        return WebSocketEvent(
            type=EventType.COST_UPDATE,
            payload=self.model_dump(mode="json"),
        )


class BudgetWarningEvent(BaseModel):
    """Budget warning event"""
    project_id: UUID
    budget_limit: float
    current_spend: float
    percent_used: float
    warning_level: str  # approaching, exceeded

    def to_event(self) -> WebSocketEvent:
        return WebSocketEvent(
            type=EventType.BUDGET_WARNING,
            payload=self.model_dump(mode="json"),
        )

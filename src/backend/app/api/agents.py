"""
Agent API endpoints for GrantPilot.

Provides REST endpoints for:
- Creating and running agent tasks
- Querying task status
- Pausing/resuming/cancelling tasks
"""

import logging
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.agents import WritingAgent, AgentConfig
from app.agents.base import AgentType, AgentStatus
from app.agents.writing import GrantSection, WritingInput

logger = logging.getLogger(__name__)

router = APIRouter()

# In-memory task tracking (replace with DB in production)
active_tasks: dict[UUID, WritingAgent] = {}


class CreateWritingTaskRequest(BaseModel):
    """Request to create a writing task"""
    project_id: UUID
    project_title: str
    section: GrantSection
    project_description: Optional[str] = None
    rfa_requirements: Optional[str] = None
    previous_feedback: Optional[str] = None
    user_notes: Optional[str] = None
    formality: float = 0.8
    technical_depth: float = 0.7
    max_words: int = 500
    model: str = "claude-sonnet-4-20250514"


class TaskStatusResponse(BaseModel):
    """Response with task status"""
    task_id: UUID
    agent_type: str
    status: str
    progress_percent: Optional[int] = None
    current_step: Optional[str] = None
    output: Optional[str] = None
    error_message: Optional[str] = None
    tokens_used: int = 0
    cost_usd: float = 0.0


async def run_writing_task(
    task_id: UUID,
    input_data: dict,
    db: AsyncSession,
):
    """Background task to run the writing agent"""
    agent = active_tasks.get(task_id)
    if not agent:
        logger.error(f"Task {task_id} not found in active_tasks")
        return

    try:
        result = await agent.run(input_data)
        logger.info(f"Task {task_id} completed with status: {result.status}")
    except Exception as e:
        logger.error(f"Task {task_id} failed: {e}")
    finally:
        # Keep in active_tasks for status queries, clean up later
        pass


@router.post("/writing", response_model=TaskStatusResponse)
async def create_writing_task(
    request: CreateWritingTaskRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new writing task.

    Starts the Writing Agent in the background to generate a grant section draft.
    Returns immediately with task_id for status polling.
    """
    # Create agent config
    config = AgentConfig(
        project_id=request.project_id,
        model=request.model,
    )

    # Create agent
    agent = WritingAgent(config=config, db_session=db)
    task_id = agent.task_id

    # Store in active tasks
    active_tasks[task_id] = agent

    # Prepare input
    input_data = WritingInput(
        section=request.section,
        project_id=request.project_id,
        project_title=request.project_title,
        project_description=request.project_description,
        rfa_requirements=request.rfa_requirements,
        previous_feedback=request.previous_feedback,
        user_notes=request.user_notes,
        formality=request.formality,
        technical_depth=request.technical_depth,
        max_words=request.max_words,
    ).model_dump()

    # Start background task
    background_tasks.add_task(run_writing_task, task_id, input_data, db)

    return TaskStatusResponse(
        task_id=task_id,
        agent_type=AgentType.WRITING.value,
        status=AgentStatus.PENDING.value,
        progress_percent=0,
        current_step="queued",
    )


@router.get("/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: UUID):
    """Get the status of an agent task"""
    agent = active_tasks.get(task_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Task not found")

    # Calculate progress
    progress = 0
    if agent.checkpoint.total_steps:
        progress = int((agent.checkpoint.step_index / agent.checkpoint.total_steps) * 100)

    return TaskStatusResponse(
        task_id=task_id,
        agent_type=agent.agent_type.value,
        status=agent.status.value,
        progress_percent=progress,
        current_step=agent.checkpoint.last_step,
        output=agent.checkpoint.interim_results.get("output"),
        tokens_used=agent.prompt_tokens + agent.completion_tokens,
        cost_usd=agent.cost_usd,
    )


@router.post("/{task_id}/pause")
async def pause_task(task_id: UUID):
    """Pause an agent task"""
    agent = active_tasks.get(task_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Task not found")

    if agent.status != AgentStatus.RUNNING:
        raise HTTPException(status_code=400, detail="Task is not running")

    agent.pause()
    return {"status": "paused", "task_id": str(task_id)}


@router.post("/{task_id}/resume")
async def resume_task(task_id: UUID):
    """Resume a paused agent task"""
    agent = active_tasks.get(task_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Task not found")

    if agent.status != AgentStatus.PAUSED:
        raise HTTPException(status_code=400, detail="Task is not paused")

    agent.resume()
    return {"status": "resumed", "task_id": str(task_id)}


@router.post("/{task_id}/cancel")
async def cancel_task(task_id: UUID):
    """Cancel an agent task"""
    agent = active_tasks.get(task_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Task not found")

    if agent.status in [AgentStatus.COMPLETED, AgentStatus.FAILED, AgentStatus.CANCELLED]:
        raise HTTPException(status_code=400, detail="Task already finished")

    agent.cancel()
    return {"status": "cancelled", "task_id": str(task_id)}


@router.delete("/{task_id}")
async def delete_task(task_id: UUID):
    """Delete a completed task from memory"""
    if task_id not in active_tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    del active_tasks[task_id]
    return {"status": "deleted", "task_id": str(task_id)}

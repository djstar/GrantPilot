"""
WebSocket API endpoint for GrantPilot real-time updates.

Handles:
- Client connection/disconnection
- Message routing
- Heartbeat ping-pong
- Event subscriptions
"""

import json
import logging
from typing import Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from pydantic import ValidationError

from app.websocket.manager import manager
from app.websocket.events import EventType, WebSocketEvent

logger = logging.getLogger(__name__)

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: Optional[str] = Query(None, description="Optional client identifier"),
):
    """
    Main WebSocket endpoint for real-time updates.

    Query params:
        client_id: Optional identifier for reconnection support

    Message types from client:
        - {"type": "heartbeat"} - Keep connection alive
        - {"type": "subscribe", "events": ["agent_status", "task_progress"]}
        - {"type": "unsubscribe", "events": ["agent_status"]}

    Events sent to client:
        - connected: Connection confirmation with client_id
        - heartbeat: Response to heartbeat
        - agent_status: Agent state changes
        - task_progress: Task progress updates
        - chat_stream: Streaming chat tokens
        - notification: User notifications
        - document_processing: Document processing status
        - cost_update: Cost tracking updates
    """
    # Accept connection
    assigned_client_id = await manager.connect(websocket, client_id)

    try:
        while True:
            # Wait for messages from client
            try:
                data = await websocket.receive_text()
                message = json.loads(data)
            except json.JSONDecodeError:
                await manager.send_to_client(
                    assigned_client_id,
                    WebSocketEvent(
                        type=EventType.NOTIFICATION,
                        payload={
                            "level": "error",
                            "title": "Invalid Message",
                            "message": "Could not parse JSON message",
                        },
                    ),
                )
                continue

            # Handle different message types
            msg_type = message.get("type", "").lower()

            if msg_type == "heartbeat":
                await manager.handle_heartbeat(assigned_client_id)

            elif msg_type == "subscribe":
                events = message.get("events", [])
                try:
                    event_types = [EventType(e) for e in events if e in EventType.__members__.values()]
                    await manager.subscribe(assigned_client_id, event_types)
                    await manager.send_to_client(
                        assigned_client_id,
                        WebSocketEvent(
                            type=EventType.NOTIFICATION,
                            payload={
                                "level": "info",
                                "title": "Subscribed",
                                "message": f"Subscribed to {len(event_types)} event types",
                                "auto_dismiss": True,
                            },
                        ),
                    )
                except Exception as e:
                    logger.error(f"Subscribe error: {e}")

            elif msg_type == "unsubscribe":
                events = message.get("events", [])
                try:
                    event_types = [EventType(e) for e in events if e in EventType.__members__.values()]
                    await manager.unsubscribe(assigned_client_id, event_types)
                except Exception as e:
                    logger.error(f"Unsubscribe error: {e}")

            elif msg_type == "ping":
                # Simple ping-pong for connection testing
                await manager.send_to_client(
                    assigned_client_id,
                    WebSocketEvent(
                        type=EventType.HEARTBEAT,
                        payload={"pong": True},
                    ),
                )

            else:
                logger.debug(f"Unknown message type from {assigned_client_id}: {msg_type}")

    except WebSocketDisconnect:
        await manager.disconnect(assigned_client_id)
        logger.info(f"Client {assigned_client_id} disconnected normally")

    except Exception as e:
        logger.error(f"WebSocket error for {assigned_client_id}: {e}")
        await manager.disconnect(assigned_client_id)


@router.get("/ws/stats")
async def websocket_stats():
    """Get WebSocket connection statistics"""
    return {
        "active_connections": manager.get_connection_count(),
        "client_ids": manager.get_client_ids(),
    }

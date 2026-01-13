"""
WebSocket Connection Manager for GrantPilot.

Handles:
- Client connection/disconnection
- Broadcasting events to all clients
- Targeted messaging to specific clients
- Heartbeat/ping-pong for connection health
- Automatic reconnection support
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Set, Optional, Any
from uuid import UUID, uuid4
from fastapi import WebSocket, WebSocketDisconnect

from app.websocket.events import WebSocketEvent, EventType

logger = logging.getLogger(__name__)


class ConnectionManager:
    """
    Manages WebSocket connections for real-time updates.

    Features:
    - Multiple clients per user (e.g., multiple browser tabs)
    - Broadcast to all connections
    - Targeted messaging by client_id
    - Heartbeat monitoring
    - Event filtering by type
    """

    def __init__(self):
        # client_id -> WebSocket mapping
        self.active_connections: Dict[str, WebSocket] = {}
        # Track connection metadata
        self.connection_info: Dict[str, Dict[str, Any]] = {}
        # Subscriptions: event_type -> set of client_ids
        self.subscriptions: Dict[EventType, Set[str]] = {}
        # Heartbeat tracking
        self.last_heartbeat: Dict[str, datetime] = {}
        # Lock for thread-safe operations
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, client_id: Optional[str] = None) -> str:
        """
        Accept a new WebSocket connection.

        Args:
            websocket: The WebSocket connection
            client_id: Optional client identifier (generated if not provided)

        Returns:
            The client_id for this connection
        """
        await websocket.accept()

        if client_id is None:
            client_id = str(uuid4())

        async with self._lock:
            self.active_connections[client_id] = websocket
            self.connection_info[client_id] = {
                "connected_at": datetime.utcnow(),
                "last_activity": datetime.utcnow(),
            }
            self.last_heartbeat[client_id] = datetime.utcnow()

        logger.info(f"WebSocket connected: {client_id}")

        # Send connection confirmation
        await self.send_to_client(
            client_id,
            WebSocketEvent(
                type=EventType.CONNECTED,
                payload={"client_id": client_id},
            ),
        )

        return client_id

    async def disconnect(self, client_id: str):
        """
        Handle client disconnection.

        Args:
            client_id: The client to disconnect
        """
        async with self._lock:
            if client_id in self.active_connections:
                del self.active_connections[client_id]

            if client_id in self.connection_info:
                del self.connection_info[client_id]

            if client_id in self.last_heartbeat:
                del self.last_heartbeat[client_id]

            # Remove from all subscriptions
            for event_type in self.subscriptions:
                self.subscriptions[event_type].discard(client_id)

        logger.info(f"WebSocket disconnected: {client_id}")

    async def send_to_client(self, client_id: str, event: WebSocketEvent) -> bool:
        """
        Send an event to a specific client.

        Args:
            client_id: Target client
            event: Event to send

        Returns:
            True if sent successfully, False otherwise
        """
        if client_id not in self.active_connections:
            return False

        try:
            websocket = self.active_connections[client_id]
            await websocket.send_json(event.to_json())

            async with self._lock:
                if client_id in self.connection_info:
                    self.connection_info[client_id]["last_activity"] = datetime.utcnow()

            return True
        except Exception as e:
            logger.error(f"Error sending to client {client_id}: {e}")
            await self.disconnect(client_id)
            return False

    async def broadcast(self, event: WebSocketEvent, exclude: Optional[Set[str]] = None):
        """
        Broadcast an event to all connected clients.

        Args:
            event: Event to broadcast
            exclude: Optional set of client_ids to exclude
        """
        exclude = exclude or set()
        disconnected = []

        for client_id, websocket in list(self.active_connections.items()):
            if client_id in exclude:
                continue

            try:
                await websocket.send_json(event.to_json())
            except Exception as e:
                logger.error(f"Error broadcasting to {client_id}: {e}")
                disconnected.append(client_id)

        # Clean up disconnected clients
        for client_id in disconnected:
            await self.disconnect(client_id)

    async def broadcast_to_subscribers(self, event: WebSocketEvent):
        """
        Broadcast an event only to clients subscribed to that event type.

        Args:
            event: Event to broadcast
        """
        if event.type not in self.subscriptions:
            return

        subscribers = self.subscriptions[event.type]
        for client_id in list(subscribers):
            await self.send_to_client(client_id, event)

    async def subscribe(self, client_id: str, event_types: list[EventType]):
        """
        Subscribe a client to specific event types.

        Args:
            client_id: Client to subscribe
            event_types: List of event types to subscribe to
        """
        async with self._lock:
            for event_type in event_types:
                if event_type not in self.subscriptions:
                    self.subscriptions[event_type] = set()
                self.subscriptions[event_type].add(client_id)

    async def unsubscribe(self, client_id: str, event_types: list[EventType]):
        """
        Unsubscribe a client from specific event types.

        Args:
            client_id: Client to unsubscribe
            event_types: List of event types to unsubscribe from
        """
        async with self._lock:
            for event_type in event_types:
                if event_type in self.subscriptions:
                    self.subscriptions[event_type].discard(client_id)

    async def handle_heartbeat(self, client_id: str) -> bool:
        """
        Handle heartbeat from client.

        Args:
            client_id: Client sending heartbeat

        Returns:
            True if heartbeat acknowledged
        """
        if client_id not in self.active_connections:
            return False

        async with self._lock:
            self.last_heartbeat[client_id] = datetime.utcnow()

        await self.send_to_client(
            client_id,
            WebSocketEvent(type=EventType.HEARTBEAT, payload={"status": "ok"}),
        )
        return True

    def get_connection_count(self) -> int:
        """Get number of active connections"""
        return len(self.active_connections)

    def get_client_ids(self) -> list[str]:
        """Get list of connected client IDs"""
        return list(self.active_connections.keys())

    async def cleanup_stale_connections(self, max_idle_seconds: int = 300):
        """
        Clean up connections that haven't sent a heartbeat recently.

        Args:
            max_idle_seconds: Maximum seconds since last heartbeat
        """
        now = datetime.utcnow()
        stale = []

        for client_id, last_beat in list(self.last_heartbeat.items()):
            idle_seconds = (now - last_beat).total_seconds()
            if idle_seconds > max_idle_seconds:
                stale.append(client_id)

        for client_id in stale:
            logger.warning(f"Cleaning up stale connection: {client_id}")
            await self.disconnect(client_id)


# Global connection manager instance
manager = ConnectionManager()

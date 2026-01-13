/**
 * WebSocket hook for GrantPilot real-time updates.
 *
 * Features:
 * - Automatic reconnection with exponential backoff
 * - Heartbeat to keep connection alive
 * - Event subscription management
 * - Type-safe event handling
 */

import { useEffect, useRef, useState, useCallback } from 'react';

// Event types matching backend
export type EventType =
  | 'connected'
  | 'disconnected'
  | 'heartbeat'
  | 'agent_status'
  | 'agent_started'
  | 'agent_completed'
  | 'agent_failed'
  | 'agent_paused'
  | 'agent_resumed'
  | 'task_progress'
  | 'task_checkpoint'
  | 'chat_stream'
  | 'chat_complete'
  | 'document_processing'
  | 'document_ready'
  | 'document_failed'
  | 'notification'
  | 'cost_update'
  | 'budget_warning';

export interface WebSocketEvent<T = unknown> {
  type: EventType;
  payload: T;
  timestamp: string;
}

export interface AgentStatusPayload {
  task_id: string;
  agent_type: string;
  status: string;
  message?: string;
  progress_percent?: number;
  current_step?: string;
  tokens_used: number;
  cost_incurred: number;
}

export interface TaskProgressPayload {
  task_id: string;
  step_index: number;
  total_steps?: number;
  step_name: string;
  step_description?: string;
  completed_items: string[];
}

export interface NotificationPayload {
  level: 'info' | 'success' | 'warning' | 'error';
  title: string;
  message: string;
  action_url?: string;
  auto_dismiss: boolean;
  dismiss_after_ms: number;
}

export interface ChatStreamPayload {
  conversation_id?: string;
  chunk: string;
  is_final: boolean;
  sources: Array<{ document_id: string; chunk_id: string; score: number }>;
}

export interface DocumentProcessingPayload {
  document_id: string;
  filename: string;
  status: string;
  progress_percent: number;
  chunks_created: number;
  error_message?: string;
}

export interface CostUpdatePayload {
  project_id?: string;
  task_id?: string;
  provider: string;
  model: string;
  prompt_tokens: number;
  completion_tokens: number;
  cost_usd: number;
  cumulative_cost_usd: number;
  budget_remaining?: number;
}

type EventHandler<T = unknown> = (event: WebSocketEvent<T>) => void;

interface UseWebSocketOptions {
  url?: string;
  autoConnect?: boolean;
  reconnect?: boolean;
  reconnectInterval?: number;
  maxReconnectAttempts?: number;
  heartbeatInterval?: number;
}

interface UseWebSocketReturn {
  isConnected: boolean;
  clientId: string | null;
  lastEvent: WebSocketEvent | null;
  connect: () => void;
  disconnect: () => void;
  subscribe: (eventTypes: EventType[]) => void;
  unsubscribe: (eventTypes: EventType[]) => void;
  on: <T = unknown>(eventType: EventType, handler: EventHandler<T>) => () => void;
  send: (message: Record<string, unknown>) => void;
}

const DEFAULT_WS_URL = `ws://${window.location.hostname}:8000/ws`;

export function useWebSocket(options: UseWebSocketOptions = {}): UseWebSocketReturn {
  const {
    url = DEFAULT_WS_URL,
    autoConnect = true,
    reconnect = true,
    reconnectInterval = 1000,
    maxReconnectAttempts = 10,
    heartbeatInterval = 30000,
  } = options;

  const [isConnected, setIsConnected] = useState(false);
  const [clientId, setClientId] = useState<string | null>(null);
  const [lastEvent, setLastEvent] = useState<WebSocketEvent | null>(null);

  const wsRef = useRef<WebSocket | null>(null);
  const reconnectAttemptsRef = useRef(0);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const heartbeatIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const handlersRef = useRef<Map<EventType, Set<EventHandler>>>(new Map());

  // Clear all timeouts/intervals
  const clearTimers = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }
    if (heartbeatIntervalRef.current) {
      clearInterval(heartbeatIntervalRef.current);
      heartbeatIntervalRef.current = null;
    }
  }, []);

  // Start heartbeat
  const startHeartbeat = useCallback(() => {
    if (heartbeatIntervalRef.current) {
      clearInterval(heartbeatIntervalRef.current);
    }
    heartbeatIntervalRef.current = setInterval(() => {
      if (wsRef.current?.readyState === WebSocket.OPEN) {
        wsRef.current.send(JSON.stringify({ type: 'heartbeat' }));
      }
    }, heartbeatInterval);
  }, [heartbeatInterval]);

  // Handle incoming messages
  const handleMessage = useCallback((event: MessageEvent) => {
    try {
      const data: WebSocketEvent = JSON.parse(event.data);
      setLastEvent(data);

      // Handle connection event
      if (data.type === 'connected' && data.payload) {
        setClientId((data.payload as { client_id: string }).client_id);
      }

      // Dispatch to registered handlers
      const handlers = handlersRef.current.get(data.type);
      if (handlers) {
        handlers.forEach((handler) => handler(data));
      }
    } catch (error) {
      console.error('WebSocket message parse error:', error);
    }
  }, []);

  // Connect to WebSocket
  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      return;
    }

    clearTimers();

    const wsUrl = clientId ? `${url}?client_id=${clientId}` : url;
    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      console.log('WebSocket connected');
      setIsConnected(true);
      reconnectAttemptsRef.current = 0;
      startHeartbeat();
    };

    ws.onclose = (event) => {
      console.log('WebSocket closed:', event.code, event.reason);
      setIsConnected(false);
      clearTimers();

      // Attempt reconnection
      if (reconnect && reconnectAttemptsRef.current < maxReconnectAttempts) {
        const delay = reconnectInterval * Math.pow(2, reconnectAttemptsRef.current);
        console.log(`Reconnecting in ${delay}ms (attempt ${reconnectAttemptsRef.current + 1})`);
        reconnectTimeoutRef.current = setTimeout(() => {
          reconnectAttemptsRef.current++;
          connect();
        }, Math.min(delay, 30000)); // Cap at 30 seconds
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    ws.onmessage = handleMessage;

    wsRef.current = ws;
  }, [url, clientId, reconnect, reconnectInterval, maxReconnectAttempts, clearTimers, startHeartbeat, handleMessage]);

  // Disconnect from WebSocket
  const disconnect = useCallback(() => {
    clearTimers();
    if (wsRef.current) {
      wsRef.current.close(1000, 'Client disconnect');
      wsRef.current = null;
    }
    setIsConnected(false);
    setClientId(null);
  }, [clearTimers]);

  // Subscribe to event types
  const subscribe = useCallback((eventTypes: EventType[]) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ type: 'subscribe', events: eventTypes }));
    }
  }, []);

  // Unsubscribe from event types
  const unsubscribe = useCallback((eventTypes: EventType[]) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ type: 'unsubscribe', events: eventTypes }));
    }
  }, []);

  // Register event handler
  const on = useCallback(<T = unknown>(eventType: EventType, handler: EventHandler<T>): (() => void) => {
    if (!handlersRef.current.has(eventType)) {
      handlersRef.current.set(eventType, new Set());
    }
    handlersRef.current.get(eventType)!.add(handler as EventHandler);

    // Return cleanup function
    return () => {
      handlersRef.current.get(eventType)?.delete(handler as EventHandler);
    };
  }, []);

  // Send arbitrary message
  const send = useCallback((message: Record<string, unknown>) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message));
    }
  }, []);

  // Auto-connect on mount
  useEffect(() => {
    if (autoConnect) {
      connect();
    }

    return () => {
      disconnect();
    };
  }, [autoConnect, connect, disconnect]);

  return {
    isConnected,
    clientId,
    lastEvent,
    connect,
    disconnect,
    subscribe,
    unsubscribe,
    on,
    send,
  };
}

export default useWebSocket;

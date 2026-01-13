/**
 * WebSocket Context Provider for GrantPilot.
 *
 * Provides WebSocket connection state and methods to all child components.
 */

import { createContext, useContext, ReactNode } from 'react';
import { useWebSocket, EventType, WebSocketEvent } from './useWebSocket';

interface WebSocketContextValue {
  isConnected: boolean;
  clientId: string | null;
  lastEvent: WebSocketEvent | null;
  connect: () => void;
  disconnect: () => void;
  subscribe: (eventTypes: EventType[]) => void;
  unsubscribe: (eventTypes: EventType[]) => void;
  on: <T = unknown>(eventType: EventType, handler: (event: WebSocketEvent<T>) => void) => () => void;
  send: (message: Record<string, unknown>) => void;
}

const WebSocketContext = createContext<WebSocketContextValue | null>(null);

interface WebSocketProviderProps {
  children: ReactNode;
  url?: string;
  autoConnect?: boolean;
}

export function WebSocketProvider({
  children,
  url,
  autoConnect = true,
}: WebSocketProviderProps) {
  const ws = useWebSocket({ url, autoConnect });

  return (
    <WebSocketContext.Provider value={ws}>
      {children}
    </WebSocketContext.Provider>
  );
}

export function useWebSocketContext(): WebSocketContextValue {
  const context = useContext(WebSocketContext);
  if (!context) {
    throw new Error('useWebSocketContext must be used within a WebSocketProvider');
  }
  return context;
}

export default WebSocketContext;

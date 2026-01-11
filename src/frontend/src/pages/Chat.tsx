import { useState, useRef, useEffect } from 'react'
import { useMutation } from '@tanstack/react-query'
import { Send, Bot, User, Loader2 } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { api } from '@/api/client'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

interface ChatResponse {
  response: string
  sources?: Array<{
    chunk_id: string
    document_id: string
    content: string
    score: number
    document_filename: string
  }>
}

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const chatMutation = useMutation({
    mutationFn: async (message: string) => {
      const history = messages.map((m) => ({
        role: m.role,
        content: m.content,
      }))

      return api.post<ChatResponse>('/chat', {
        message,
        history,
        stream: false,
      })
    },
    onSuccess: (data) => {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: data.response },
      ])
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || chatMutation.isPending) return

    const userMessage = input.trim()
    setInput('')
    setMessages((prev) => [...prev, { role: 'user', content: userMessage }])
    chatMutation.mutate(userMessage)
  }

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)]">
      <div className="mb-4">
        <h1 className="text-2xl font-bold tracking-tight">Chat with GrantPilot</h1>
        <p className="text-muted-foreground">
          Ask questions about your documents or get help with grant writing
        </p>
      </div>

      <Card className="flex-1 flex flex-col overflow-hidden">
        <CardHeader className="border-b py-3">
          <CardTitle className="text-base font-medium">Conversation</CardTitle>
        </CardHeader>

        <CardContent className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center text-muted-foreground">
              <Bot className="h-12 w-12 mb-4 opacity-50" />
              <p className="text-lg font-medium">Welcome to GrantPilot</p>
              <p className="text-sm max-w-md mt-2">
                Upload documents and ask questions. I can help you with grant writing,
                research synthesis, and more.
              </p>
              <div className="mt-6 space-y-2 text-sm">
                <p className="font-medium">Try asking:</p>
                <ul className="space-y-1 text-left">
                  <li>&bull; "What are the key requirements for this RFA?"</li>
                  <li>&bull; "Summarize the significance section"</li>
                  <li>&bull; "Help me write specific aims"</li>
                </ul>
              </div>
            </div>
          ) : (
            messages.map((message, index) => (
              <div
                key={index}
                className={`flex gap-3 ${
                  message.role === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                {message.role === 'assistant' && (
                  <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
                    <Bot className="h-4 w-4 text-primary" />
                  </div>
                )}
                <div
                  className={`max-w-[80%] rounded-lg px-4 py-2 ${
                    message.role === 'user'
                      ? 'bg-primary text-primary-foreground'
                      : 'bg-muted'
                  }`}
                >
                  <p className="whitespace-pre-wrap">{message.content}</p>
                </div>
                {message.role === 'user' && (
                  <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center flex-shrink-0">
                    <User className="h-4 w-4 text-primary-foreground" />
                  </div>
                )}
              </div>
            ))
          )}

          {chatMutation.isPending && (
            <div className="flex gap-3 justify-start">
              <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
                <Bot className="h-4 w-4 text-primary" />
              </div>
              <div className="bg-muted rounded-lg px-4 py-2">
                <Loader2 className="h-4 w-4 animate-spin" />
              </div>
            </div>
          )}

          {chatMutation.isError && (
            <div className="flex gap-3 justify-start">
              <div className="w-8 h-8 rounded-full bg-destructive/10 flex items-center justify-center flex-shrink-0">
                <Bot className="h-4 w-4 text-destructive" />
              </div>
              <div className="bg-destructive/10 text-destructive rounded-lg px-4 py-2">
                <p>Error: Failed to get response. Please try again.</p>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </CardContent>

        <div className="border-t p-4">
          <form onSubmit={handleSubmit} className="flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
              disabled={chatMutation.isPending}
            />
            <Button type="submit" disabled={chatMutation.isPending || !input.trim()}>
              {chatMutation.isPending ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Send className="h-4 w-4" />
              )}
            </Button>
          </form>
        </div>
      </Card>
    </div>
  )
}

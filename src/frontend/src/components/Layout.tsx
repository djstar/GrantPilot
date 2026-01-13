import { Outlet, Link, useLocation } from 'react-router-dom'
import { cn } from '@/lib/utils'
import { useWebSocketContext } from '@/hooks'

const navigation = [
  { name: 'Dashboard', href: '/' },
  { name: 'Projects', href: '/projects' },
  { name: 'Documents', href: '/documents' },
  { name: 'Chat', href: '/chat' },
]

export default function Layout() {
  const location = useLocation()
  const { isConnected } = useWebSocketContext()

  return (
    <div className="min-h-screen bg-background">
      {/* Sidebar */}
      <aside className="fixed inset-y-0 left-0 z-50 w-64 border-r bg-card">
        <div className="flex h-16 items-center border-b px-6">
          <Link to="/" className="flex items-center gap-2">
            <div className="h-8 w-8 rounded-lg bg-primary flex items-center justify-center">
              <span className="text-primary-foreground font-bold text-lg">G</span>
            </div>
            <span className="font-semibold text-xl">GrantPilot</span>
          </Link>
          {/* Connection status indicator */}
          <div className="ml-auto" title={isConnected ? 'Connected' : 'Disconnected'}>
            <div className={cn(
              'h-2 w-2 rounded-full',
              isConnected ? 'bg-green-500' : 'bg-red-500'
            )} />
          </div>
        </div>
        <nav className="flex flex-col gap-1 p-4">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href ||
              (item.href !== '/' && location.pathname.startsWith(item.href))
            return (
              <Link
                key={item.name}
                to={item.href}
                className={cn(
                  'flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors',
                  isActive
                    ? 'bg-primary text-primary-foreground'
                    : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
                )}
              >
                {item.name}
              </Link>
            )
          })}
        </nav>
      </aside>

      {/* Main content */}
      <main className="pl-64">
        <div className="p-8">
          <Outlet />
        </div>
      </main>
    </div>
  )
}

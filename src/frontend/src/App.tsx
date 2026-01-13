import { Routes, Route } from 'react-router-dom'
import { Toaster } from 'sonner'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Projects from './pages/Projects'
import ProjectDetail from './pages/ProjectDetail'
import Documents from './pages/Documents'
import Chat from './pages/Chat'
import { WebSocketProvider } from './hooks'

function App() {
  return (
    <WebSocketProvider>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="projects" element={<Projects />} />
          <Route path="projects/:id" element={<ProjectDetail />} />
          <Route path="documents" element={<Documents />} />
          <Route path="chat" element={<Chat />} />
        </Route>
      </Routes>
      <Toaster position="bottom-right" />
    </WebSocketProvider>
  )
}

export default App

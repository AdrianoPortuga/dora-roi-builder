import { Routes, Route, Navigate, Link } from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext'
import Login from './pages/Login'
import Vendors from './pages/Vendors'

function Protected({ children }) {
  const { token } = useAuth()
  if (!token) return <Navigate to="/login" replace />
  return children
}
function Layout({ children }) {
  const { user, logout } = useAuth()
  return (
  <div className="container-app">
    <aside className="sidebar border-r border-slate-800 bg-slate-950/80 p-3">
      <div className="flex items-center gap-2 font-semibold text-slate-100 mb-3">
        <div className="w-6 h-6 rounded bg-blue-600" /><span>DORA RoI Builder</span></div>
      <nav className="space-y-1 text-slate-200">
        <Link className="block px-3 py-2 rounded hover:bg-slate-800" to="/vendors">Vendors</Link>
        <span className="block px-3 py-2 rounded opacity-60">Riscos (em breve)</span>
        <span className="block px-3 py-2 rounded opacity-60">EvidÃªncias (em breve)</span>
        <span className="block px-3 py-2 rounded opacity-60">RelatÃ³rios (em breve)</span>
      </nav>
    </aside>
    <header className="topbar flex items-center justify-between px-4 border-b border-slate-800 backdrop-blur bg-slate-900/50">
      <div className="flex items-center gap-2"><span className="text-sm text-slate-400">Ambiente</span>
        <span className="text-xs px-2 py-1 rounded-full border border-blue-500/40 text-blue-300">MVP UI</span></div>
      <div className="flex items-center gap-3">
        <span className="text-sm text-slate-300">{user?.email}</span>
        <button onClick={logout} className="text-sm px-3 py-1 rounded border border-slate-700 hover:bg-slate-800">Sair</button>
      </div>
    </header>
    <main className="main p-4">{children}</main>
  </div> )
}
export default function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Protected><Layout><Vendors /></Layout></Protected>} />
        <Route path="/vendors" element={<Protected><Layout><Vendors /></Layout></Protected>} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </AuthProvider>
  )
}

import { Routes, Route, Navigate, Link } from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext'
import Login from './pages/Login'
import Vendors from './pages/Vendors'
import PageShell from './layouts/PageShell'

function Protected({ children }) {
  const { user, loading } = useAuth()
  if (loading) return null
  if (!user) return <Navigate to="/login" replace />
  return children
}
function Layout({ children }) { return <PageShell>{children}</PageShell> }
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

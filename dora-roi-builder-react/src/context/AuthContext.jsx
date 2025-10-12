import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import api from '../api/client'

const Ctx = createContext(null)
export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem('access_token') || '')
  const [refresh, setRefresh] = useState(localStorage.getItem('refresh_token') || '')
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (token) {
      api.setToken(token)
      api.me().then(setUser).catch(() => {})
    }
  }, [token])

  const login = async (email, password) => {
    setLoading(true); setError('')
    try {
      const res = await api.login(email, password)
      setToken(res.access_token); localStorage.setItem('access_token', res.access_token)
      if (res.refresh_token) { setRefresh(res.refresh_token); localStorage.setItem('refresh_token', res.refresh_token) }
      api.setToken(res.access_token)
      const me = await api.me(); setUser(me)
      return true
    } catch (e) {
      setError(e?.response?.data?.detail || 'Falha no login'); return false
    } finally { setLoading(false) }
  }
  const logout = () => {
    setToken(''); setRefresh(''); setUser(null)
    localStorage.removeItem('access_token'); localStorage.removeItem('refresh_token')
  }
  const value = useMemo(() => ({ token, refresh, user, loading, error, login, logout }), [token, refresh, user, loading, error])
  return <Ctx.Provider value={value}>{children}</Ctx.Provider>
}
export function useAuth(){ return useContext(Ctx) }

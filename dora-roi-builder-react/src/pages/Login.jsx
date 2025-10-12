import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Login(){
  const { login, loading, error } = useAuth()
  const [email, setEmail] = useState('admin@demo.com')
  const [password, setPassword] = useState('demo123')
  const nav = useNavigate()
  const onSubmit = async (e) => { e.preventDefault(); const ok = await login(email, password); if (ok) nav('/') }
  return (
    <div className="min-h-screen flex items-center justify-center">
      <form onSubmit={onSubmit} className="w-full max-w-sm bg-slate-900/60 border border-slate-800 rounded-xl p-6 shadow-lg">
        <h1 className="text-xl font-bold mb-1">Acessar</h1>
        <p className="text-sm text-slate-400 mb-4">Entre com suas credenciais para continuar.</p>
        <label className="text-sm">Email</label>
        <input className="w-full mb-3 mt-1 px-3 py-2 rounded border border-slate-700 bg-slate-900" value={email} onChange={e=>setEmail(e.target.value)} />
        <label className="text-sm">Senha</label>
        <input type="password" className="w-full mb-4 mt-1 px-3 py-2 rounded border border-slate-700 bg-slate-900" value={password} onChange={e=>setPassword(e.target.value)} />
        {error && <div className="text-red-400 text-sm mb-2">{error}</div>}
        <button disabled={loading} className="w-full py-2 rounded bg-blue-600 hover:bg-blue-500 font-semibold">
          {loading ? 'Entrando...' : 'Entrar'}
        </button>
      </form>
    </div>
  )
}

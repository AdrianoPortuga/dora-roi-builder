import { useState } from "react";
import { api } from "../api/client";
import { setToken } from "../api/client";

export default function Login() {
  const [email, setEmail] = useState("admin@demo.com");
  const [password, setPassword] = useState("admin");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const r = await api.login(email, password); // { access_token, token_type }
      if (!r?.access_token) throw new Error("Sem token");

      // grava token no axios e localStorage e redireciona
      setToken(r.access_token);
      window.location.href = "/vendors";
    } catch (err) {
      console.error(err);
      setError("Credenciais inválidas");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-900">
      <form
        onSubmit={handleSubmit}
        className="w-[360px] bg-slate-800 p-6 rounded-2xl shadow-lg space-y-4"
      >
        <h1 className="text-white text-xl font-semibold">Acessar</h1>

        {error && (
          <div className="text-sm text-red-400 bg-red-950/40 px-3 py-2 rounded">
            {error}
          </div>
        )}

        <div className="space-y-1">
          <label className="text-slate-300 text-sm">Email</label>
          <input
            type="email"
            className="w-full rounded-md px-3 py-2 bg-slate-900 text-slate-100 outline-none ring-1 ring-slate-700 focus:ring-2 focus:ring-indigo-500"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            autoComplete="username"
            required
          />
        </div>

        <div className="space-y-1">
          <label className="text-slate-300 text-sm">Senha</label>
          <input
            type="password"
            className="w-full rounded-md px-3 py-2 bg-slate-900 text-slate-100 outline-none ring-1 ring-slate-700 focus:ring-2 focus:ring-indigo-500"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="current-password"
            required
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-indigo-600 hover:bg-indigo-500 disabled:opacity-60 text-white font-semibold py-2 rounded-md transition-colors"
        >
          {loading ? "Entrando..." : "Entrar"}
        </button>
      </form>
    </div>
  );
}

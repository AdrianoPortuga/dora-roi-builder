# 12c-frontend-fix-paths.ps1
$ErrorActionPreference = "Stop"

Write-Host "🔎 Iniciando correção de paths do frontend..." -ForegroundColor Cyan

# --- 1) Validar raiz do projeto ---
$Root = (Get-Location).Path
$rootReact = Join-Path $Root "dora-roi-builder-react"
if (-not (Test-Path $rootReact)) {
  throw "Execute este script na RAIZ do repo (onde existe a pasta 'dora-roi-builder-react')."
}

# --- 2) Detectar onde está o app React (nível 1 ou duplicado em nível 2) ---
$level1 = Join-Path $Root "dora-roi-builder-react"
$level2 = Join-Path $Root "dora-roi-builder-react\dora-roi-builder-react"

if (Test-Path (Join-Path $level2 "package.json")) {
  $Front = $level2
  Write-Host "⚠️  App React detectado em pasta DUPLICADA:" -ForegroundColor Yellow
  Write-Host "    $Front"
} elseif (Test-Path (Join-Path $level1 "package.json")) {
  $Front = $level1
  Write-Host "✅ App React detectado:" -ForegroundColor Green
  Write-Host "   $Front"
} else {
  # fallback: usa nível 1 e segue criando estrutura
  $Front = $level1
  Write-Host "ℹ️  package.json não encontrado; vou usar:" -ForegroundColor Yellow
  Write-Host "   $Front"
}

# Normaliza o caminho (remove barras estranhas)
try {
  $Front = (Resolve-Path $Front).Path
} catch {
  New-Item -ItemType Directory -Force -Path $Front | Out-Null
  $Front = (Resolve-Path $Front).Path
}

# --- 3) Garantir estrutura src/ src/api src/pages ---
$srcDir    = Join-Path $Front "src"
$apiDir    = Join-Path $srcDir "api"
$pagesDir  = Join-Path $srcDir "pages"

foreach ($d in @($srcDir, $apiDir, $pagesDir)) {
  if (-not (Test-Path $d)) {
    New-Item -ItemType Directory -Force -Path $d | Out-Null
  }
}

if ([string]::IsNullOrWhiteSpace($pagesDir)) { throw "pagesDir não definido." }
if (-not (Test-Path $pagesDir)) { throw "Pasta pages não existe: $pagesDir" }

# --- 4) client.js (só cria se não existir) ---
$clientJs = Join-Path $apiDir "client.js"
if (-not (Test-Path $clientJs)) {
@"
import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api",
});

export function setToken(token) {
  if (token) {
    api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    localStorage.setItem("dora_token", token);
  } else {
    delete api.defaults.headers.common["Authorization"];
    localStorage.removeItem("dora_token");
  }
}

export function getToken() {
  return localStorage.getItem("dora_token");
}

export function clearToken() {
  setToken(null);
}

export default api;
"@ | Set-Content -Path $clientJs -Encoding UTF8
  Write-Host "✅ Criado: $clientJs"
} else {
  Write-Host "ℹ️  Mantido (já existia): $clientJs"
}

# --- 5) Vendors.jsx (lista + cadastro) ---
$vendorsJsx = Join-Path $pagesDir "Vendors.jsx"
@"
import { useEffect, useState } from "react";
import api from "../api/client";

export default function Vendors() {
  const [rows, setRows] = useState([]);
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);
  const [form, setForm] = useState({ name: "", country: "PT", criticality: "low" });

  async function load() {
    try {
      const { data } = await api.get("/vendors");
      setRows(data);
    } catch (err) {
      if (err?.response?.status === 401) {
        window.location.href = "/";
      } else {
        setError("Erro ao carregar vendors");
        console.error(err);
      }
    }
  }

  useEffect(() => { load(); }, []);

  async function onCreate(e) {
    e.preventDefault();
    if (!form.name.trim()) return;
    setSaving(true);
    try {
      const { data } = await api.post("/vendors", form);
      setRows((prev) => [data, ...prev]);
      setForm({ name: "", country: "PT", criticality: "low" });
    } catch (err) {
      if (err?.response?.status === 401) {
        window.location.href = "/";
      } else {
        alert("Falha ao criar vendor");
        console.error(err);
      }
    } finally {
      setSaving(false);
    }
  }

  if (error) return <p style={{ color: "tomato" }}>{error}</p>;

  return (
    <div style={{ padding: 16, maxWidth: 680 }}>
      <h2>Vendors</h2>

      <form onSubmit={onCreate} style={{ display: "grid", gap: 8, margin: "12px 0", gridTemplateColumns: "1fr 120px 140px 120px" }}>
        <input
          placeholder="Nome do fornecedor"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
        />
        <input
          placeholder="País (ex.: PT, BR)"
          value={form.country}
          onChange={(e) => setForm({ ...form, country: e.target.value })}
        />
        <select
          value={form.criticality}
          onChange={(e) => setForm({ ...form, criticality: e.target.value })}
        >
          <option value="low">low</option>
          <option value="medium">medium</option>
          <option value="high">high</option>
        </select>
        <button type="submit" disabled={saving}>{saving ? "Gravando..." : "Adicionar"}</button>
      </form>

      <ul>
        {rows.map((v) => (
          <li key={v.id}>
            <b>{v.name}</b> — {v.country} — {v.criticality}
          </li>
        ))}
      </ul>
    </div>
  );
}
"@ | Set-Content -Path $vendorsJsx -Encoding UTF8

Write-Host "✅ Atualizado: $vendorsJsx"

Write-Host "`n✅ Caminho do app React em uso:" -ForegroundColor Green
Write-Host $Front
Write-Host "`n👉 Para rodar o front, execute:"
Write-Host "cd `"$Front`""
Write-Host "npm run dev"

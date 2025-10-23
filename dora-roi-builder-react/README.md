# DORA RoI Builder — React + Vite + Tailwind (MVP)

Front-end inicial em React já integrado ao backend (FastAPI) via axios, com:
- Login (JWT) + `/api/auth/me`
- Vendors CRUD (`/api/vendors/`)
- Rotas protegidas com React Router
- Config por `.env` (`VITE_API_BASE`)

## Como rodar

```bash
# 1) Entre na pasta do projeto
cd dora-roi-builder-react

# 2) Copie o .env exemplo e ajuste a URL da API
cp .env.example .env
# edite .env para apontar para http://127.0.0.1:8000 ou sua URL

# 3) Instale dependências
npm install

# 4) Rode o dev server
npm run dev
```

Abra http://localhost:5173

## Estrutura
- `src/api/client.js` — axios + Bearer token
- `src/context/AuthContext.jsx` — sessão, login e me
- `src/layouts/PageShell.jsx` — shell + Header + Toaster
- `src/components/Header.jsx` — marca, navegação e usuário
- `src/components/ToastProvider.jsx` — toasts (sucesso/erro)
- `src/components/ConfirmDialog.jsx` — confirmação genérica
- `src/components/ui/*` — Button, Input, Select, Card, Table
- `src/pages/Login.jsx` — tela de login
- `src/pages/Vendors.jsx` — CRUD com dialogs e toasts

## Variáveis .env do front
Use `VITE_API_BASE` para apontar a API, ex.:

```
VITE_API_BASE=http://127.0.0.1:8000/api/v1
```

## Observações
- Sem dependências externas de UI (shadcn/lucide), apenas Tailwind.
- Para Refresh Token, adicione um interceptor 401 que chame `/auth/refresh` (se disponível) antes do logout.

Feito para Adriano (Codestech Ltda).

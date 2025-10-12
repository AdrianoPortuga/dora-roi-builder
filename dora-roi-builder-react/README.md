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
- `src/api/client.js` — axios + interceptador de Bearer token
- `src/context/AuthContext.jsx` — guarda token, usuário e faz login/me
- `src/pages/Login.jsx` — tela de login
- `src/pages/Vendors.jsx` — listagem, criação, edição e exclusão
- `src/App.jsx` — rotas e layout

## Ajustes
- Se sua API retorna outra estrutura (ex.: `{items: [...]}`), o componente Vendors já tenta normalizar (`results/items/array`).
- Para Refresh Token, você pode adicionar um interceptor 401 para tentar `/api/auth/refresh` antes do logout.

Feito para Adriano (Codestech Ltda).

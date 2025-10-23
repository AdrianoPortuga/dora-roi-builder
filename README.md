# DORA RoI Builder

Plataforma de gestão e compliance DORA (Digital Operational Resilience Act) para controlar **fornecedores, riscos e evidências** de conformidade.

## 📌 Descrição do Projeto
Monorepo com **backend FastAPI (Python)** e **frontend React (Vite)**.

---

## ⚙️ Arquitetura
```
dora-roi-builder/
├── backend/                # API FastAPI
│   ├── main.py
│   ├── requirements.txt
│   └── ...
├── dora-roi-builder-react/ # Frontend React (Vite)
│   ├── src/
│   │   ├── api/
│   │   ├── pages/
│   │   ├── components/
│   │   ├── context/
│   │   └── layouts/
│   └── package.json
├── backups/                # Snapshots automáticos (.zip)
├── scripts/                # Scripts PowerShell (.ps1)
└── README.md
```

---

## 🚀 Stack Tecnológica
| Camada   | Tecnologia            |
|---------|------------------------|
| Backend | FastAPI (Python 3.11) |
| Front   | React + Vite          |
| Banco   | SQLite (MVP) / PostgreSQL (planejado) |
| Estilos | TailwindCSS + shadcn/ui (planejado) |
| Version | Git + GitHub          |
| Autom.  | PowerShell (setup, backup, push) |

---

## 🧰 Requisitos e Setup

### Backend
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
Docs: http://127.0.0.1:8000/docs

### Frontend
```powershell
cd dora-roi-builder-react
npm install
npm run dev
```
App: http://127.0.0.1:5173

---

## 🔐 Login Demo
| Campo   | Valor            |
|---------|------------------|
| Usuário | admin@demo.com   |
| Senha   | 1234             |

---

## ✅ Funcionalidades Atuais
- Login funcional (AuthContext + localStorage)
- Rota protegida (ProtectedRoute)
- CRUD de Fornecedores (Vendors)
- Integração com API (Axios + Bearer token)
- Backup automático (`13-backup-and-push.ps1`)
- UI redesign (Codex + gradiente azul)

## 🧭 Em Desenvolvimento
- Tailwind + shadcn/ui em toda a UI
- Dialogs, toasts e tema escuro
- Módulos de Riscos e Evidências
- Dashboards DORA
- JWT completo com refresh token
- Deploy em staging (Render / Railway)

---

## 📜 Scripts Principais
| Script                      | Função                                   |
|----------------------------|-------------------------------------------|
| 12c-frontend-fix-paths.ps1 | Corrige estrutura do React                |
| 13-backup-and-push.ps1     | Backup + commit + tag + push              |
| start-backend.ps1          | Inicia backend FastAPI                    |
| start-frontend.ps1         | Inicia frontend Vite                      |

---

## 🧾 Versionamento
- Commits semânticos: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`
- Branches: `main`, `feature/*`, `backups/*`
- Tags: `ui-redesign-YYYYMMDD_HHMMSS`

---

## 🔄 Backup Automático
```powershell
.-backup-and-push.ps1
```
- Gera zips de backend e frontend
- Cria commit e tag com timestamp
- Faz push e guia PR

---

## 📘 Boas Práticas
- Manter `.env.local` (`VITE_API_URL`) atualizado
- `git pull --rebase` antes de novas features
- Commits pequenos e descritivos
- Testar login e vendors após cada build

---

## 👤 Autor
**Adriano Corrêa**  
Repositório: https://github.com/AdrianoPortuga/dora-roi-builder  
Data: 2025-10-23

---

## 🏁 Licença
Projeto de estudo e uso interno — todos os direitos reservados à Codestech Ltd.

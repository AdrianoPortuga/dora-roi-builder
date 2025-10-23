# scripts\start-backend.ps1
$ErrorActionPreference = "Stop"

$root = "C:\dora-roi-builder"
cd $root

# ativa venv
& .\.venv\Scripts\Activate.ps1

# (opcional) variáveis de ambiente do backend
$env:APP_VERSION = "0.1.0"
$env:APP_ENV = "local"

# sobe o uvicorn
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

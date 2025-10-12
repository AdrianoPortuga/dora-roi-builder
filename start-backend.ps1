# start-backend.ps1
$ErrorActionPreference = "Stop"

# 1) Ativa o venv
& "$PSScriptRoot\.venv\Scripts\Activate.ps1"

# 2) Garante que a pasta app é um package
if (-not (Test-Path "$PSScriptRoot\app\__init__.py")) {
  New-Item -ItemType File -Path "$PSScriptRoot\app\__init__.py" -Force | Out-Null
  Write-Host "Criado: app\__init__.py"
}

# 3) Sobe o Uvicorn (módulo app.main:app)
Set-Location $PSScriptRoot
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

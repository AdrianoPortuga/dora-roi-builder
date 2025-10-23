param(
  [string]$Root = "."
)

Write-Host " Aplicando correções (v2) em: $((Resolve-Path $Root).Path)" -ForegroundColor Cyan

function Save-With-Backup {
  param(
    [string]$Path,
    [string]$NewContent
  )
  $backup = "$Path.bak"
  if (-not (Test-Path $backup)) {
    Copy-Item -Path $Path -Destination $backup
  }
  Set-Content -Path $Path -Value $NewContent -Encoding UTF8
}

# Padrões individuais (sem pipes) para -SimpleMatch
$findPatterns = @("create_engine","sqlite","dev.db","DATABASE_URL")

# Regex úteis
$rxDbUrlLine   = [regex]"^\s*DATABASE_URL\s*=\s*['""]sqlite:[^'""]+['""]\s*$"
$rxConfigDecl  = [regex]"^\s*database_url\s*:\s*str\s*=\s*os\.getenv\([^\)]*['""]sqlite:[^'""]+['""][^\)]*\)\s*$"
$rxCreateEng   = [regex]"create_engine\s*\((?<args>[^)]*)\)"
$rxDropAll     = [regex]"Base\.metadata\.drop_all\s*\("

# Blocos para config.py (sobe 1 nível: app/ -> raiz do repo)
$blockConfig = @"
from pathlib import Path
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # Caminho absoluto para dev.db na raiz do projeto
    ROOT_DIR = Path(__file__).resolve().parents[1]
    DB_PATH = ROOT_DIR / "dev.db"
    database_url: str = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH.as_posix()}")

settings = Settings()
"@

# Bloco de DATABASE_URL absoluto genérico (para app/db.py)
$blockDbPyHeader = @"
from pathlib import Path
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

ROOT_DIR = Path(__file__).resolve().parents[1]
DB_PATH = ROOT_DIR / "dev.db"
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH.as_posix()}")
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
"@

# Varre candidatos de código-próprio (ignora .venv)
$candidates = Get-ChildItem -Path $Root -Recurse -Include *.py |
  Where-Object { $_.FullName -notmatch "\\\.venv\\|" } |
  Where-Object {
    (Select-String -Path $_.FullName -Pattern $findPatterns -SimpleMatch -Quiet)
  }

if (-not $candidates) {
  Write-Host "Nenhum arquivo candidato encontrado no código do projeto." -ForegroundColor Yellow
  exit 0
}

$changed = @()

foreach ($file in $candidates) {
  $p = $file.FullName
  $orig = Get-Content -Path $p -Raw -Encoding UTF8
  $new  = $orig
  $fileChanged = $false

  $isConfig = ($p -match "[\\\/]app[\\\/]config\.py$")
  $isDbPy   = ($p -match "[\\\/]app[\\\/]db\.py$")

  if ($isConfig) {
    # Substitui a linha de database_url default relativa por bloco com caminho absoluto
    if ($orig -match $rxConfigDecl) {
      $new = $blockConfig.Trim() + "`r`n"
      $fileChanged = $true
      Write-Host "  app/config.py ajustado para caminho absoluto (database_url)" -ForegroundColor Green
    }
  }

  if ($isDbPy) {
    # Se tiver uma linha DATABASE_URL relativa, substitui por cabeçalho completo
    if ($orig -match $rxDbUrlLine -or $orig -match "sqlite:///./dev\.db") {
      $new = $blockDbPyHeader.Trim() + "`r`n"
      $fileChanged = $true
      Write-Host "  app/db.py ajustado para caminho absoluto (DATABASE_URL + engine)" -ForegroundColor Green
    } else {
      # Caso não tenha a linha direta, apenas injeta ROOT_DIR/DB_PATH e força connect_args
      if ($new -notmatch "ROOT_DIR\s*=\s*Path\(__file__\)\.resolve\(\)\.parents\[1\]") {
        $inject = @"
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parents[1]
DB_PATH = ROOT_DIR / "dev.db"
"@
        $new = $inject + "`r`n" + $new
        $fileChanged = $true
        Write-Host "  app/db.py recebeu ROOT_DIR/DB_PATH para caminho absoluto" -ForegroundColor Green
      }
      if ($orig -match $rxCreateEng) {
        $tmp = $rxCreateEng.Replace($new, {
          param($m)
          $args = $m.Groups["args"].Value
          if ($args -match "connect_args") {
            "create_engine($args)"
          } else {
            $argsTrim = $args.Trim()
            if ($argsTrim -eq "") {
              'create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, future=True)'
            } else {
              "create_engine($argsTrim, connect_args={""check_same_thread"": False})"
            }
          }
        })
        if ($tmp -ne $new) {
          $new = $tmp
          $fileChanged = $true
          Write-Host "  app/db.py garantiu check_same_thread=False no create_engine" -ForegroundColor Green
        }
      }
    }
  }

  # Segurança: comentar qualquer drop_all em qualquer arquivo do projeto (se houver)
  if ($orig -match $rxDropAll) {
    $new = $new -replace $rxDropAll, "# [REMOVIDO PELO FIX] Base.metadata.drop_all("
    $fileChanged = $true
    Write-Host "  drop_all comentado em: $p" -ForegroundColor Green
  }

  if ($fileChanged -and ($new -ne $orig)) {
    Save-With-Backup -Path $p -NewContent $new
    $changed += $p
  }
}

if ($changed.Count -gt 0) {
  "`n===  ARQUIVOS ALTERADOS ==="
  $changed | ForEach-Object { " - $_" }
  "`nBackups criados com extensão .bak ao lado dos arquivos originais."
} else {
  Write-Host "`nNenhuma alteração necessária (v2)." -ForegroundColor Yellow
}

"`n===  Verificação de dev.db existentes (pós-fix) ==="
Get-ChildItem -Path $Root -Recurse -Filter dev.db -ErrorAction SilentlyContinue |
  Select-Object FullName, Length, LastWriteTime |
  Format-Table -AutoSize

"`n Fim da correção (v2)."

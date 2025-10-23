param(
  [string]$Root = "."
)

Write-Host " Aplicando correções em: $((Resolve-Path $Root).Path)" -ForegroundColor Cyan

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

$rxDbUrl = [regex]"^\s*DATABASE_URL\s*=\s*['""]sqlite:[^'""]+['""]\s*$"
$rxCreateEngine = [regex]"create_engine\s*\((?<args>[^)]*)\)"
$rxDropAll = [regex]"Base\.metadata\.drop_all\s*\("

$blockHeader = @"
from pathlib import Path
from sqlalchemy import create_engine
try:
    BASE_DIR = Path(__file__).resolve().parent
except NameError:
    from os.path import dirname, abspath
    BASE_DIR = Path(dirname(abspath(__file__)))
DB_PATH = BASE_DIR / "dev.db"
DATABASE_URL = f"sqlite:///{DB_PATH.as_posix()}"
"@

$candidates = Get-ChildItem -Path $Root -Recurse -Include *.py |
  Where-Object {
    (Select-String -Path $_.FullName -Pattern "create_engine|sqlite|dev\.db|DATABASE_URL" -SimpleMatch -Quiet)
  }

if (-not $candidates) {
  Write-Host "Nenhum arquivo candidato encontrado." -ForegroundColor Yellow
  exit 0
}

$changed = @()

foreach ($file in $candidates) {
  $path = $file.FullName
  $orig = Get-Content -Path $path -Raw -Encoding UTF8
  $new  = $orig
  $fileChanged = $false

  if ($orig -match $rxDbUrl) {
    $new = $new -replace $rxDbUrl, $blockHeader.Trim()
    $fileChanged = $true
    Write-Host "  DATABASE_URL absolutizado em: $path" -ForegroundColor Green
  } elseif ($orig -match "sqlite:") {
    if ($new -notmatch "DB_PATH\s*=\s*BASE_DIR\s*/\s*""dev\.db""") {
      $new = $blockHeader + "`r`n" + $new
      $fileChanged = $true
      Write-Host "  Bloco de DB inserido no topo: $path" -ForegroundColor Green
    }
  }

  if ($orig -match "sqlite:") {
    $tmp = $rxCreateEngine.Replace($new, {
      param($m)
      $args = $m.Groups["args"].Value
      if ($args -match "connect_args") {
        "create_engine($args)"
      } else {
        $argsTrim = $args.Trim()
        if ($argsTrim -eq "") {
          'create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=False, future=True)'
        } else {
          "create_engine($argsTrim, connect_args={""check_same_thread"": False})"
        }
      }
    })
    if ($tmp -ne $new) {
      $new = $tmp
      $fileChanged = $true
      Write-Host "  check_same_thread aplicado em: $path" -ForegroundColor Green
    }
  }

  if ($orig -match $rxDropAll) {
    $new = $new -replace $rxDropAll, "# [REMOVIDO PELO FIX] Base.metadata.drop_all("
    $fileChanged = $true
    Write-Host "  drop_all comentado em: $path" -ForegroundColor Green
  }

  if ($fileChanged -and ($new -ne $orig)) {
    Save-With-Backup -Path $path -NewContent $new
    $changed += $path
  }
}

if ($changed.Count -gt 0) {
  "`n===  ARQUIVOS ALTERADOS ==="
  $changed | ForEach-Object { " - $_" }
  "`nBackups criados com extensão .bak ao lado dos arquivos originais."
} else {
  Write-Host "`nNenhuma alteração necessária." -ForegroundColor Yellow
}

"`n===  Verificação de dev.db existentes (pós-fix) ==="
Get-ChildItem -Path $Root -Recurse -Filter dev.db -ErrorAction SilentlyContinue |
  Select-Object FullName, Length, LastWriteTime |
  Format-Table -AutoSize

"`n Fim da correção."

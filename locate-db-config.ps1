param(
  [string]$Root = "."
)

Write-Host " Varredura iniciada em: $((Resolve-Path $Root).Path)" -ForegroundColor Cyan

$patterns = @(
  "create_engine",
  "sqlite",
  "dev\.db",
  "DATABASE_URL",
  "SessionLocal",
  "check_same_thread",
  "drop_all",
  "create_all"
)

"`n===  ARQUIVOS .py COM ASSUNTOS DE DB ==="
Get-ChildItem -Path $Root -Recurse -Include *.py | ForEach-Object {
  $file = $_.FullName
  $hits = Select-String -Path $file -Pattern $patterns -SimpleMatch -List
  if ($hits) {
    Write-Host "`n$file" -ForegroundColor Yellow
    Select-String -Path $file -Pattern $patterns | ForEach-Object {
      ("  {0}:{1}  {2}" -f $_.Filename, $_.LineNumber, $_.Line.Trim())
    }
  }
}

"`n===  FRONT (.env/.ts/.tsx) E POSTMAN (collection.json) ==="
$frontPatterns = @(
  "VITE_API_URL",
  "baseUrl",
  "localhost",
  "127\.0\.0\.1"
)

Get-ChildItem -Path $Root -Recurse -Include *.env,*.ts,*.tsx,*.json | ForEach-Object {
  $file = $_.FullName
  $hits = Select-String -Path $file -Pattern $frontPatterns -SimpleMatch -List
  if ($hits) {
    Write-Host "`n$file" -ForegroundColor Green
    Select-String -Path $file -Pattern $frontPatterns | ForEach-Object {
      ("  {0}:{1}  {2}" -f $_.Filename, $_.LineNumber, $_.Line.Trim())
    }
  }
}

"`n===  CÓPIAS DE dev.db ENCONTRADAS ==="
Get-ChildItem -Path $Root -Recurse -Filter dev.db -ErrorAction SilentlyContinue |
  Select-Object FullName, Length, LastWriteTime |
  Format-Table -AutoSize

"`n Fim da varredura."

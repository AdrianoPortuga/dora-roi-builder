Param(
  [string]$ApiBase = "http://127.0.0.1:8000",
  [string]$FrontBase = "http://localhost:5173",
  [string]$Email = "admin@demo.com",
  [string]$Password = "demo123"
)

$ErrorActionPreference = "Stop"

function Write-Info($msg)  { Write-Host "[INFO] $msg"  -ForegroundColor Cyan }
function Write-Ok($msg)    { Write-Host "[ OK ] $msg"  -ForegroundColor Green }
function Write-Warn($msg)  { Write-Host "[WARN] $msg"  -ForegroundColor Yellow }
function Write-Err($msg)   { Write-Host "[ERR ] $msg"  -ForegroundColor Red }

function Test-Cmd($cmd, $args) {
  try { & $cmd $args | Out-Null; return $true } catch { return $false }
}

# Renomeada para evitar conflito com a variável automática $host
function Test-TcpPort($hostname, $port) {
  try {
    $res = Test-NetConnection -ComputerName $hostname -Port $port -WarningAction SilentlyContinue
    return $res.TcpTestSucceeded
  } catch { return $false }
}

function Expect-Status($method, $url, $expected, $headers=@{}, $body=$null) {
  try {
    $params = @{ Uri = $url; Method = $method; Headers = $headers; TimeoutSec = 10 }
    if ($null -ne $body) {
      $params["Body"] = ($body | ConvertTo-Json -Depth 5)
      $params["ContentType"] = "application/json"
    }
    $resp = Invoke-WebRequest @params
    if ($resp.StatusCode -eq $expected) {
      return @{ ok=$true; status=$resp.StatusCode; body=$resp.Content }
    } else {
      return @{ ok=$false; status=$resp.StatusCode; body=$resp.Content }
    }
  } catch {
    if ($_.Exception.Response) {
      $code = $_.Exception.Response.StatusCode.value__
      $stream = $_.Exception.Response.GetResponseStream()
      $reader = New-Object System.IO.StreamReader($stream)
      $body = $reader.ReadToEnd()
      return @{ ok=($code -eq $expected); status=$code; body=$body }
    } else {
      return @{ ok=$false; status=-1; body=$_.Exception.Message }
    }
  }
}

# 1) Tools
Write-Info "Checking tools..."
try { $pyv = python --version 2>&1; Write-Ok "Python: $pyv" } catch { Write-Warn "Python not found in PATH" }
try { $nodev = node -v; $npmv = npm -v; Write-Ok "Node: $nodev | npm: $npmv" } catch { Write-Warn "Node/npm not found in PATH" }
if (Test-Cmd "docker" "--version") { Write-Ok "Docker: OK" } else { Write-Warn "Docker not found (optional)" }

# 2) Backend
Write-Info "Checking API at $ApiBase ..."
$apiHost = ([uri]$ApiBase).Host
$apiPort = ([uri]$ApiBase).Port
if (-not $apiPort) { $apiPort = 80 }

if (Test-TcpPort $apiHost $apiPort) {
  Write-Ok "Port $apiPort open on $apiHost"
} else {
  Write-Err "Port $apiPort closed on $apiHost - backend does not seem running."
}

$h = Expect-Status "GET" "$ApiBase/health" 200
if ($h.ok) { Write-Ok "/health -> 200 OK" } else { Write-Err "/health -> expected 200, got $($h.status). Body: $($h.body)" }

$d = Expect-Status "GET" "$ApiBase/docs" 200
if ($d.ok) { Write-Ok "/docs -> 200 OK" } else { Write-Err "/docs -> expected 200, got $($d.status)" }

# 3) Auth
Write-Info "Checking authentication..."
$loginBody = @{ email = $Email; password = $Password }
$login = Expect-Status "POST" "$ApiBase/api/auth/login" 200 @{} $loginBody
$token = $null
if ($login.ok) {
  try {
    $loginJson = $login.body | ConvertFrom-Json
    $token = $loginJson.access_token
  } catch {
    $token = $null
  }
  if ([string]::IsNullOrWhiteSpace($token)) {
    Write-Err "Login returned 200 but no access_token found. Body: $($login.body)"
  } else {
    Write-Ok "Login OK and token captured."
  }
} else {
  Write-Err "Login failed (status $($login.status)). Body: $($login.body)"
}

# 4) Vendors
Write-Info "Checking Vendors protection..."
$noAuth = Expect-Status "GET" "$ApiBase/api/vendors/" 401
if ($noAuth.ok) { Write-Ok "GET /api/vendors/ without token -> 401 OK" }
else { Write-Err "GET /api/vendors/ without token -> expected 401, got $($noAuth.status). Body: $($noAuth.body)" }

if ($token) {
  $authHeaders = @{ Authorization = "Bearer $token" }
  $withAuth = Expect-Status "GET" "$ApiBase/api/vendors/" 200 $authHeaders
  if ($withAuth.ok) { Write-Ok "GET /api/vendors/ with token -> 200 OK" }
  else { Write-Err "GET /api/vendors/ with token -> expected 200, got $($withAuth.status). Body: $($withAuth.body)" }
}

# 5) Frontend
Write-Info "Checking Frontend at $FrontBase ..."
$frontHost = ([uri]$FrontBase).Host
$frontPort = ([uri]$FrontBase).Port
if (-not $frontPort) { $frontPort = 80 }

if (Test-TcpPort $frontHost $frontPort) {
  Write-Ok "Port $frontPort open on $frontHost"
  $f = Expect-Status "GET" "$FrontBase" 200
  if ($f.ok) { Write-Ok "Frontend root -> 200 OK" } else { Write-Warn "Frontend root did not return 200 (status $($f.status))" }
} else {
  Write-Warn "Frontend does not seem running at $FrontBase (port $frontPort closed)."
}

Write-Host ""
Write-Host "===== SUMMARY =====" -ForegroundColor White
Write-Host "API base:    $ApiBase"
Write-Host "Frontend:    $FrontBase"
Write-Host "Credentials: $Email / $Password"
Write-Host "==================="

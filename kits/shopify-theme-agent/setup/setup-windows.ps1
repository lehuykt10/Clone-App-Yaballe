# Shopify Theme Agent - cai dat phan mem cho Windows 10/11
# Cach chay (PowerShell, trong thu muc du an):
#   powershell -ExecutionPolicy Bypass -File setup\setup-windows.ps1
# Chi kiem tra, khong cai:
#   powershell -ExecutionPolicy Bypass -File setup\setup-windows.ps1 -CheckOnly

param([switch]$CheckOnly)
$ErrorActionPreference = "Continue"

function Refresh-Path {
  $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" +
              [System.Environment]::GetEnvironmentVariable("Path", "User")
}
function Has($cmd) { return [bool](Get-Command $cmd -ErrorAction SilentlyContinue) }
function Ok($msg)   { Write-Host "  [OK]  $msg" -ForegroundColor Green }
function Bad($msg)  { Write-Host "  [--]  $msg" -ForegroundColor Yellow }
function Step($msg) { Write-Host ""; Write-Host "==> $msg" -ForegroundColor Cyan }

function Show-Status {
  Step "Kiem tra phan mem"
  Refresh-Path
  if (Has node)    { Ok "Node.js $(node -v)" } else { Bad "Node.js chua co" }
  if (Has py)      { Ok "Python $(py --version)" } elseif (Has python) { Ok "Python $(python --version)" } else { Bad "Python chua co" }
  if (Has git)     { Ok "Git $(git --version)" } else { Bad "Git chua co" }
  if (Has shopify) { Ok "Shopify CLI $(shopify version)" } else { Bad "Shopify CLI chua co" }
  if (Has claude)  { Ok "Claude Code $(claude --version)" } else { Bad "Claude Code chua co" }
  if (Has npx) {
    $pw = npx --no-install playwright --version 2>$null
    if ($LASTEXITCODE -eq 0) { Ok "Playwright $pw" } else { Bad "Playwright chua co" }
  }
}

if ($CheckOnly) { Show-Status; exit 0 }

if (-not (Has winget)) {
  Write-Host "Khong tim thay 'winget'. Cai 'App Installer' tu Microsoft Store roi chay lai script." -ForegroundColor Red
  Write-Host "Hoac cai tay: https://nodejs.org (LTS), https://www.python.org (tich Add to PATH), https://git-scm.com"
  exit 1
}

Step "1/5 Node.js LTS"
if (Has node) { Ok "Da co Node.js $(node -v)" } else {
  winget install -e --id OpenJS.NodeJS.LTS --accept-source-agreements --accept-package-agreements
  Refresh-Path
}

Step "2/5 Python 3.12"
if ((Has py) -or (Has python)) { Ok "Da co Python" } else {
  winget install -e --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements
  Refresh-Path
}

Step "3/5 Git"
if (Has git) { Ok "Da co Git" } else {
  winget install -e --id Git.Git --accept-source-agreements --accept-package-agreements
  Refresh-Path
}

Step "4/5 Shopify CLI + Playwright (trinh duyet de phan tich doi thu)"
if (-not (Has npm)) { Refresh-Path }
npm install -g @shopify/cli@latest playwright
Refresh-Path
npx playwright install chromium

Step "5/5 Claude Code"
if (Has claude) { Ok "Da co Claude Code" } else {
  try { Invoke-RestMethod https://claude.ai/install.ps1 | Invoke-Expression }
  catch { npm install -g @anthropic-ai/claude-code }
  Refresh-Path
}

Show-Status
Write-Host ""
Write-Host "XONG. Dong PowerShell, mo lai, vao thu muc du an va go: claude" -ForegroundColor Green
Write-Host "Neu con dong [--], xem muc 'Loi thuong gap' trong HUONG-DAN.html"

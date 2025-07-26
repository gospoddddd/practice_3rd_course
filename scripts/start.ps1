Param(
  [switch]$RebuildPlugins = $false
)

Write-Host "==> practice_3rd_course quick start for Windows" -ForegroundColor Cyan

# Ensure Docker is running
try {
  docker version | Out-Null
} catch {
  Write-Error "Docker Desktop is not running. Please start it and re-run this script."
  exit 1
}

# Create .env from example if not exists
if (-not (Test-Path ".\.env")) {
  Copy-Item ".\.env.example" ".\.env"
  Write-Host "Created .env from .env.example. Please edit it to set GIT_REPO_URL and Telegram secrets." -ForegroundColor Yellow
}

# Optionally force plugin re-install (clean Jenkins volume)
if ($RebuildPlugins) {
  Write-Host "Rebuilding Jenkins image and resetting jenkins_home volume..." -ForegroundColor Yellow
  docker compose down -v
}

# Build and start
docker compose up -d --build

Write-Host "Jenkins:   http://localhost:8080" -ForegroundColor Green
Write-Host "Registry:  http://localhost:5000/v2/_catalog" -ForegroundColor Green
Write-Host "Postgres:  localhost:$((Get-Content .\.env | Select-String 'POSTGRES_PORT=').ToString().Split('=')[1])" -ForegroundColor Green

Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "  1) Edit .env and set GIT_REPO_URL to your GitHub repo URL, TELEGRAM_* secrets."
Write-Host "  2) Jenkins will auto-create a pipeline job 'practice_3rd_course' via JCasC."
Write-Host "  3) Run the job in Jenkins → it will lint, test, build, push image, ask for approval, and deploy."

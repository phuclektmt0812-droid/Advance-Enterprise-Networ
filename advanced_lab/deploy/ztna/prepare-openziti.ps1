$ErrorActionPreference = "Stop"

# OpenZiti learning quickstart only. For long-lived deployments, follow the
# official production deployment guide and pin reviewed image versions.
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw "Docker CLI was not found. Install Docker Desktop and enable its Linux engine first."
}
docker compose version | Out-Null
if ($LASTEXITCODE -ne 0) {
    throw "Docker Compose V2 is required."
}

$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Compose = Join-Path $Here "docker-compose.yml"
$EnvExample = Join-Path $Here ".env.example"
$EnvFile = Join-Path $Here ".env"

Invoke-WebRequest -Uri "https://get.openziti.io/dock/docker-compose.yml" -OutFile $Compose
Invoke-WebRequest -Uri "https://get.openziti.io/dock/.env" -OutFile $EnvExample

if (-not (Test-Path $EnvFile)) {
    Copy-Item $EnvExample $EnvFile
    Write-Host "Created .env from the official OpenZiti quickstart template."
    Write-Host "Review advertised controller/router addresses and credentials before starting."
    Write-Host "The .env file is local and must not be committed."
    exit 0
}

Write-Host "Existing .env preserved. Review it before starting the lab."
Write-Host "When ready, run: docker compose up -d"

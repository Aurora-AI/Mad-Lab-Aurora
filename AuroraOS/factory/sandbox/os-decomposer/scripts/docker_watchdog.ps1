# Docker Watchdog for Aurora Platform
# Resolves "500 Internal Server Error" on npipe:////./pipe/dockerDesktopLinuxEngine

$ErrorActionPreference = "SilentlyContinue"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..\..\..\..")
$VaultScript = Join-Path $RepoRoot "aurora_vault.py"

Write-Host "Checking Docker Engine integrity..." -ForegroundColor Cyan

# Test if docker version returns successfully with a timeout
$testCommand = Start-Job -ScriptBlock { docker version }
if (-not (Wait-Job $testCommand -Timeout 10)) {
    Write-Warning "Docker Engine is hanging! Initiating emergency recovery protocol..."
    
    # Log incident to Vault (MTBF Analysis)
    $timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    $logData = @{
        timestamp = $timestamp
        event = "DOCKER_ENGINE_HANG"
        recovery_triggered = $true
    } | ConvertTo-Json -Compress
    
    Write-Host "Logging incident to Aurora Vault..." -ForegroundColor Gray
    # Ensure AURORA_MASTER_KEY_FILE is set for the python call if available in current scope
    python $VaultScript set --name "DOCKER_RECOVERY_$(Get-Date -Format 'yyyyMMdd_HHmmss')" --value $logData --namespace "DOCKER_LOGS"
    
    # Kill Docker processes
    Write-Host "Killing Docker processes..." -ForegroundColor Yellow
    Stop-Process -Name "Docker*", "com.docker*", "docker-agent", "docker-sandbox" -Force
    
    # Shutdown WSL
    Write-Host "Shutting down WSL..." -ForegroundColor Yellow
    wsl --shutdown
    
    # Start Docker Desktop
    $dockerPath = "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    if (Test-Path $dockerPath) {
        Write-Host "Restarting Docker Desktop..." -ForegroundColor Green
        Start-Process $dockerPath
        Write-Host "Waiting 30s for engine initialization..."
        Start-Sleep -Seconds 30
        
        # Verify
        if (docker version) {
            Write-Host "Docker recovery SUCCESSFUL." -ForegroundColor Green
        } else {
            Write-Error "Docker recovery FAILED. Manual intervention required."
        }
    } else {
        Write-Error "Docker Desktop executable not found at $dockerPath"
    }
} else {
    Receive-Job $testCommand
    Write-Host "Docker Engine is healthy." -ForegroundColor Green
}

Remove-Job $testCommand

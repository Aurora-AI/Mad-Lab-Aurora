param (
    [Parameter(Mandatory=$true)]
    [string]$WatchDir,
    
    [Parameter(Mandatory=$false)]
    [string]$LogPath = "activity.jsonl"
)

# Garantir que os diretórios existam
if (-not (Test-Path -Path $WatchDir)) {
    New-Item -ItemType Directory -Force -Path $WatchDir | Out-Null
}

$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = $WatchDir
$watcher.Filter = "*.json"
$watcher.IncludeSubdirectories = $false
$watcher.EnableRaisingEvents = $true

Write-Host "Iniciando Dispatcher (FileSystemWatcher) v0."
Write-Host "Monitorando: $WatchDir"

# Dicionário para debounce
$script:lastTriggered = @{}

# Action block for file creation/change
$action = {
    $path = $Event.SourceEventArgs.FullPath
    $changeType = $Event.SourceEventArgs.ChangeType
    $name = $Event.SourceEventArgs.Name
    
    # Debounce simples (1 segundo)
    $now = [datetime]::UtcNow
    if ($script:lastTriggered.ContainsKey($path)) {
        if (($now - $script:lastTriggered[$path]).TotalSeconds -lt 1) {
            return
        }
    }
    $script:lastTriggered[$path] = $now
    
    Write-Host "[$now] Detectado $changeType em $name"
    
    # Chama o script python passando apenas este arquivo, ou chama uma CLI dedicada.
    # Por enquanto, log simples simulando roteamento
    
    $eventLog = @{
        timestamp = $now.ToString('o')
        event_type = "DISPATCH_TRIGGERED_PS1"
        os_id = "UNKNOWN"
        task_id = "UNKNOWN"
        metadata = @{
            source_file = $name
            change_type = $changeType.ToString()
        }
    }
    
    $jsonEntry = $eventLog | ConvertTo-Json -Compress
    Add-Content -Path $LogPath -Value $jsonEntry
}

# Register the event
$createdEvent = Register-ObjectEvent $watcher "Created" -Action $action
$changedEvent = Register-ObjectEvent $watcher "Changed" -Action $action

try {
    # Keep running until Ctrl+C
    while ($true) {
        Start-Sleep -Seconds 1
    }
}
finally {
    Write-Host "Encerrando Dispatcher graciosamente."
    Unregister-Event -SourceIdentifier $createdEvent.Name
    Unregister-Event -SourceIdentifier $changedEvent.Name
    $watcher.EnableRaisingEvents = $false
    $watcher.Dispose()
}

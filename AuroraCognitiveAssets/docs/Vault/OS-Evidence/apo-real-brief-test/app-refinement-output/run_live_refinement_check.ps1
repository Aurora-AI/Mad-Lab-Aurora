$ErrorActionPreference = "Stop"

$env:INFOPRODUCT_FACTORY_PORT = "4312"
$env:INFOPRODUCT_FACTORY_AUTH_BACKEND = "registry-dir"
$env:INFOPRODUCT_FACTORY_AUTH_REGISTRY_DIR = "C:\Aurora\AuroraCognitiveAssets\docs\Vault\OS-Evidence\ifactory-e2e\internal-auth"

$serviceLog = "C:\Aurora\AuroraCognitiveAssets\docs\Vault\OS-Evidence\apo-real-brief-test\app-refinement-output\service.log"
$serviceErrorLog = "C:\Aurora\AuroraCognitiveAssets\docs\Vault\OS-Evidence\apo-real-brief-test\app-refinement-output\service.err.log"
$payloadDir = "C:\Aurora\AuroraCognitiveAssets\docs\Vault\OS-Evidence\apo-real-brief-test"
$outputDir = "C:\Aurora\AuroraCognitiveAssets\docs\Vault\OS-Evidence\apo-real-brief-test\app-refinement-output"
$serviceWorkingDir = "C:\Aurora\Ozzmosis\apps\infoproduct-factory-service"
$tsxPath = "C:\Aurora\Ozzmosis\apps\aurora-omnichannel-ingestor\node_modules\.pnpm\tsx@4.21.0\node_modules\tsx\dist\cli.mjs"
$serviceEntry = "C:\Aurora\Ozzmosis\apps\infoproduct-factory-service\src\server.ts"
$nodePath = "C:\PythonShim\node.cmd"
$cliPath = "C:\Aurora\AuroraCognitiveAssets\apps\content-engine\client\run_refinement_pipeline.py"

$serviceCommand = "set INFOPRODUCT_FACTORY_PORT=4312&& set INFOPRODUCT_FACTORY_AUTH_BACKEND=registry-dir&& set INFOPRODUCT_FACTORY_AUTH_REGISTRY_DIR=C:\Aurora\AuroraCognitiveAssets\docs\Vault\OS-Evidence\ifactory-e2e\internal-auth&& `"$nodePath`" `"$tsxPath`" `"$serviceEntry`""

$proc = Start-Process `
  -FilePath "C:\Windows\System32\cmd.exe" `
  -ArgumentList "/c", $serviceCommand `
  -WorkingDirectory $serviceWorkingDir `
  -RedirectStandardOutput $serviceLog `
  -RedirectStandardError $serviceErrorLog `
  -PassThru

try {
  $ready = $false
  for ($i = 0; $i -lt 80; $i++) {
    try {
      Invoke-WebRequest -UseBasicParsing "http://localhost:4312/health" | Out-Null
      $ready = $true
      break
    } catch {
      Start-Sleep -Milliseconds 250
    }
  }

  if (-not $ready) {
    throw "service_not_ready"
  }

  $env:INFOPRODUCT_FACTORY_BASE_URL = "http://localhost:4312"
  $env:INFOPRODUCT_FACTORY_TOKEN = "rotated-secret-v4"
  $env:INFOPRODUCT_FACTORY_CONSUMER_ID = "AuroraCognitiveAssets"
  $env:INFOPRODUCT_FACTORY_ENVIRONMENT = "dev"

  python $cliPath `
    --payload-dir $payloadDir `
    --output-dir $outputDir `
    --print-summary
} finally {
  if ($proc -and -not $proc.HasExited) {
    Stop-Process -Id $proc.Id -Force
  }
}

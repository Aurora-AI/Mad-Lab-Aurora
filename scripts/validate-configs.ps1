$ErrorActionPreference = "Stop"

$rootPath = "C:\Projetos\MadLabAurora"
$rootPolicyPath = "$rootPath\.aurora\domain-policy.json"
$rootConsumerPath = "$rootPath\.aurora\toolbelt-consumer.json"

$subprojectPolicies = @(
    "$rootPath\ElysianCorp\.aurora\domain-policy.json",
    "$rootPath\aurora-web\.aurora\domain-policy.json",
    "$rootPath\AuroraCognitiveAssets\.aurora\domain-policy.json"
)

Write-Output "[SEMANTIC-GATE] Iniciando validação semântica de governança e soberania..."
$failed = $false

# 1. Validar integridade dos arquivos root
if (Test-Path $rootPolicyPath) {
    try {
        $content = Get-Content -Path $rootPolicyPath -Raw
        $policy = ConvertFrom-Json $content
        
        # Verificar regras básicas da política de domínio
        if ($policy.domain -ne "madlab") {
            Write-Error "❌ [FAILED] Root policy deve pertencer ao domínio 'madlab'."
            $failed = $true
        }
        if ($policy.governance.prohibited_actions -notcontains "replicate_alvaro_runtime") {
            Write-Error "❌ [FAILED] Root policy ausente da proibição 'replicate_alvaro_runtime'."
            $failed = $true
        }
        if ($policy.governance.global_promotion_path.auto_promotion -ne $false) {
            Write-Error "❌ [FAILED] Auto-promocão global de KIs deve ser desativada ('auto_promotion': false)."
            $failed = $true
        }
        Write-Output "✅ [ROOT-POLICY] Política de domínio raiz íntegra."
    } catch {
        Write-Error "❌ [FAILED] Falha ao ler ou analisar a root policy. Detalhe: $_"
        $failed = $true
    }
} else {
    Write-Error "❌ [FAILED] Root policy não localizada no caminho esperado: $rootPolicyPath"
    $failed = $true
}

if (Test-Path $rootConsumerPath) {
    try {
        $content = Get-Content -Path $rootConsumerPath -Raw
        $consumer = ConvertFrom-Json $content
        
        # Verificar requisitos do toolbelt-consumer
        if ($consumer.domain -ne "madlab") {
            Write-Error "❌ [FAILED] Toolbelt consumer deve declarar domínio 'madlab'."
            $failed = $true
        }
        if ($consumer.on_unavailable -ne "FACTORY_TOOL_UNAVAILABLE") {
            Write-Error "❌ [FAILED] Fallback do Toolbelt deve ser exatamente 'FACTORY_TOOL_UNAVAILABLE'."
            $failed = $true
        }
        
        # Validar status e tipos de capabilities
        $obsSummary = $consumer.capabilities."observability.get_trace_summary"
        $obsQa = $consumer.capabilities."observability.osqa.list_qa_artifacts_by_os"
        $topo = $consumer.capabilities."topology-impact-analyzer"
        
        if ($obsSummary.type -ne "read-only" -or $obsSummary.required -ne $true) {
            Write-Error "❌ [FAILED] Capability 'observability.get_trace_summary' deve ser obrigatória (required: true) e read-only."
            $failed = $true
        }
        if ($obsQa.type -ne "read-only" -or $obsQa.required -ne $true) {
            Write-Error "❌ [FAILED] Capability 'observability.osqa.list_qa_artifacts_by_os' deve ser obrigatória (required: true) e read-only."
            $failed = $true
        }
        if ($topo.required -ne $false -or $topo.status -ne "planned_or_contract_only") {
            Write-Error "❌ [FAILED] Capability 'topology-impact-analyzer' deve ser opcional (required: false) com status 'planned_or_contract_only'."
            $failed = $true
        }
        Write-Output "✅ [TOOLBELT-CONSUMER] Manifesto de consumo do Toolbelt íntegro."
    } catch {
        Write-Error "❌ [FAILED] Falha ao ler ou analisar o toolbelt-consumer. Detalhe: $_"
        $failed = $true
    }
} else {
    Write-Error "❌ [FAILED] Toolbelt consumer não localizado no caminho esperado: $rootConsumerPath"
    $failed = $true
}

# 2. Validar herança (extends) de subprojetos
foreach ($file in $subprojectPolicies) {
    if (Test-Path $file) {
        try {
            $content = Get-Content -Path $file -Raw
            $json = ConvertFrom-Json $content
            
            # Validar presença e resolução semântica do 'extends'
            if (-not $json.PSObject.Properties.Name -contains "extends") {
                Write-Error "❌ [FAILED] Política do subprojeto deve herdar da raiz. Propriedade 'extends' ausente em: $file"
                $failed = $true
            } else {
                # Obter a raiz do subprojeto (pasta pai de .aurora)
                $fileDir = Split-Path -Path $file -Parent
                $subprojectRoot = Split-Path -Path $fileDir -Parent
                $extendsRaw = $json.extends
                $resolvedPath = [System.IO.Path]::GetFullPath([System.IO.Path]::Combine($subprojectRoot, $extendsRaw))
                
                # Comparação de paths de forma case-insensitive e canonicalizada
                if ($resolvedPath -ne [System.IO.Path]::GetFullPath($rootPolicyPath)) {
                    Write-Error "❌ [FAILED] Referência 'extends' inválida em: $file`nCaminho resolvido: $resolvedPath`nCaminho esperado: $rootPolicyPath"
                    $failed = $true
                }
                
                # Bloquear auto-referência
                if ($resolvedPath -eq [System.IO.Path]::GetFullPath($file)) {
                    Write-Error "❌ [FAILED] Auto-referência detectada em: $file"
                    $failed = $true
                }
            }
            Write-Output "✅ [SUBPROJECT-POLICY] Validação de herança OK para: $file"
        } catch {
            Write-Error "❌ [FAILED] Falha na validação semântica de: $file`nDetalhe: $_"
            $failed = $true
        }
    } else {
        Write-Warning "⚠️ [MISSING] Política opcional de subprojeto não ativa em: $file"
    }
}

# 3. Validar não-duplicação (Garantias de Soberania da Fábrica)
# Buscar por pastas alvaro-core, gateways MCP de escrita ou instâncias locais Qdrant nos subprojetos
$forbiddenPaths = @(
    "ElysianCorp\alvaro-core",
    "aurora-web\alvaro-core",
    "AuroraCognitiveAssets\alvaro-core",
    "ElysianCorp\qdrant",
    "aurora-web\qdrant"
)

foreach ($forbidden in $forbiddenPaths) {
    $fullForbidden = "$rootPath\$forbidden"
    if (Test-Path $fullForbidden) {
        Write-Error "❌ [SOVEREIGNTY-VIOLATION] Pasta de runtime ou banco de dados duplicado detectado no domínio criativo: $fullForbidden"
        $failed = $true
    }
}

if ($failed) {
    Write-Output "❌ [SEMANTIC-GATE] Validação de Governança falhou. Verifique as violações de regras listadas acima."
    exit 1
} else {
    Write-Output "✅ [SEMANTIC-GATE] Sucesso! Todas as regras de herança, não-duplicação e soberania do domínio madlab foram validadas."
    exit 0
}

# Design System Lint for Mad Lab Aurora
# Enforces strict visual quality gates:
# - No hardcoded colors (hex, rgb, hsl, etc.) outside CSS variables/tokens
# - No border-radius > 2px
# - No box-shadows (unless whitelisted tokens)
# - Exits with 1 on violations

$ErrorActionPreference = "Stop"

# Configuration
$ScanExtensions = @(".tsx", ".astro", ".html", ".css", ".jsx")
$ActiveSubprojects = @("ElysianCorp", "aurora-web", "AuroraCognitiveAssets")

$IgnorePatterns = @(
    "\\node_modules\\",
    "\\.next\\",
    "\\.astro\\",
    "\\dist\\",
    "\\build\\",
    "\\tailwind.config\\.",
    "\\postcss.config\\.",
    "tokens.css",
    "globals.css"
)

$ViolationsCount = 0

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Running Mad Lab Aurora Design System Lint" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# Gather files only from active subprojects
$Files = @()
foreach ($Subproject in $ActiveSubprojects) {
    $SubprojectPath = Join-Path -Path $PSScriptRoot -ChildPath "..\$Subproject"
    if (Test-Path -Path $SubprojectPath) {
        $FoundFiles = Get-ChildItem -Path $SubprojectPath -Recurse -File | Where-Object {
            $File = $_
            $MatchExt = $false
            foreach ($Ext in $ScanExtensions) {
                if ($File.Extension -eq $Ext) {
                    $MatchExt = $true
                    break
                }
            }
            if (-not $MatchExt) { return $false }

            $Ignore = $false
            foreach ($Pattern in $IgnorePatterns) {
                if ($File.FullName -match [regex]::Escape($Pattern) -or $File.FullName -like "*$Pattern*") {
                    $Ignore = $true
                    break
                }
            }
            return -not $Ignore
        }
        $Files += $FoundFiles
    }
}

Write-Host "Scanning $($Files.Count) files in active subprojects ($($ActiveSubprojects -join ', '))..." -ForegroundColor Gray

foreach ($File in $Files) {
    $Lines = @(Get-Content -Path $File.FullName)
    $RelativePath = Resolve-Path -Path $File.FullName -Relative

    for ($i = 0; $i -lt $Lines.Count; $i++) {
        $Line = [string]$Lines[$i]
        $LineNum = $i + 1

        # Skip comments or empty lines
        if ([string]::IsNullOrWhiteSpace($Line) -or $Line.Trim().StartsWith("//") -or $Line.Trim().StartsWith("/*") -or $Line.Trim().StartsWith("*")) {
            continue
        }

        # 1. Check for Hardcoded Hex/RGB/HSL Colors (e.g. #fff, rgb(0,0,0), hsl(0,0%,0%))
        # Excludes hex numbers in Tailwind classes like grid-cols-12, opacity-50, etc., but checks for color-like strings.
        if ($Line -match '#[a-fA-F0-9]{3,8}' -and $Line -notmatch 'href\s*=\s*[\x27\x22]?#[a-zA-Z]' -and $Line -notmatch 'id\s*=\s*[\x27\x22]?[a-zA-Z]' -and $Line -notmatch '#svg' -and $Line -notmatch '#ffffff/0' -and $Line -notmatch 'https?://') {
            # Double check if it is inside Tailwind arbitrary color syntax like bg-[#0a0a0a] or hardcoded CSS style
            if ($Line -match 'bg-\[' -or $Line -match 'text-\[' -or $Line -match 'border-\[' -or $Line -match 'color:\s*#' -or $Line -match 'background(-color)?:\s*#' -or $Line -match 'border(-color)?:\s*#') {
                Write-Host "Violation [Hardcoded Color] in $($RelativePath):$($LineNum)" -ForegroundColor Red
                Write-Host "  > $Line" -ForegroundColor DarkGray
                $ViolationsCount++
            }
        }
        
        # Check for rgb() or hsl() hardcoded in CSS styles or Tailwind brackets
        if ($Line -match 'rgb\(' -or $Line -match 'rgba\(' -or $Line -match 'hsl\(' -or $Line -match 'hsla\(') {
            if ($Line -match 'bg-\[' -or $Line -match 'text-\[' -or $Line -match 'border-\[' -or $Line -match 'color:\s*' -or $Line -match 'background') {
                Write-Host "Violation [Hardcoded Color (RGB/HSL)] in $($RelativePath):$($LineNum)" -ForegroundColor Red
                Write-Host "  > $Line" -ForegroundColor DarkGray
                $ViolationsCount++
            }
        }

        # 2. Check for Border-Radius > 2px
        # Allowed values: rounded-none (0px), rounded-sm (2px).
        # Prohibited: rounded, rounded-md, rounded-lg, rounded-xl, rounded-2xl, rounded-3xl, rounded-full
        if ($Line -match 'rounded\b' -or $Line -match 'rounded-md' -or $Line -match 'rounded-lg' -or $Line -match 'rounded-xl' -or $Line -match 'rounded-2xl' -or $Line -match 'rounded-3xl' -or $Line -match 'rounded-full' -or $Line -match 'border-radius\s*:\s*[3-9]px' -or $Line -match 'border-radius\s*:\s*\d{2,}px' -or $Line -match 'border-radius\s*:\s*\d+(\.\d+)?(rem|em)') {
            # Make sure we don't match rounded-sm or rounded-none
            if ($Line -notmatch 'rounded-sm\b' -and $Line -notmatch 'rounded-none\b') {
                Write-Host "Violation [Border Radius > 2px] in $($RelativePath):$($LineNum)" -ForegroundColor Red
                Write-Host "  > $Line" -ForegroundColor DarkGray
                $ViolationsCount++
            }
        }

        # 3. Check for Prohibited Box Shadows
        # Prohibited: shadow, shadow-sm, shadow-md, shadow-lg, shadow-xl, shadow-2xl, shadow-inner, box-shadow
        # Allowed: shadow-none
        if ($Line -match 'shadow\b' -or $Line -match 'shadow-sm' -or $Line -match 'shadow-md' -or $Line -match 'shadow-lg' -or $Line -match 'shadow-xl' -or $Line -match 'shadow-2xl' -or $Line -match 'shadow-inner' -or $Line -match 'box-shadow') {
            if ($Line -notmatch 'shadow-none\b') {
                Write-Host "Violation [Prohibited Shadow] in $($RelativePath):$($LineNum)" -ForegroundColor Red
                Write-Host "  > $Line" -ForegroundColor DarkGray
                $ViolationsCount++
            }
        }
    }
}

Write-Host "=========================================" -ForegroundColor Cyan
if ($ViolationsCount -gt 0) {
    Write-Host "Design System Lint: FAILED ($ViolationsCount violations found)" -ForegroundColor Red
    exit 1
} else {
    Write-Host "Design System Lint: PASSED" -ForegroundColor Green
    exit 0
}

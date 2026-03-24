<#
.SYNOPSIS
    My Marketplace version bump script

.DESCRIPTION
    Batch-replace version numbers across project files.
    Supports multiple scopes:
      - marketplace: updates VERSION, marketplace.json (metadata.version)
      - mj-nlm:     updates plugin.json (version), marketplace.json (plugins[name].version)
      - mp-git:     updates plugin.json (version), marketplace.json (plugins[name].version)
      - mp-dev:     updates plugin.json (version), marketplace.json (plugins[name].version)

.PARAMETER From
    Current version (e.g. "1.0.0")

.PARAMETER To
    Target version (e.g. "1.1.0")

.PARAMETER Scope
    Target scope: "marketplace" (default), "mj-nlm", "mp-git", or "mp-dev"

.PARAMETER DryRun
    Preview mode: show what would change without modifying files

.EXAMPLE
    .\scripts\bump-version.ps1 -From "1.0.0" -To "1.1.0" -DryRun
    .\scripts\bump-version.ps1 -From "1.0.0" -To "1.1.0"
    .\scripts\bump-version.ps1 -From "1.0.0" -To "1.1.0" -Scope "mj-nlm" -DryRun
    .\scripts\bump-version.ps1 -From "1.0.0" -To "1.1.0" -Scope "mj-nlm"
    .\scripts\bump-version.ps1 -From "1.0.0" -To "1.1.0" -Scope "mp-git" -DryRun
    .\scripts\bump-version.ps1 -From "1.0.0" -To "1.1.0" -Scope "mp-dev"
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$From,

    [Parameter(Mandatory = $true)]
    [string]$To,

    [Parameter(Mandatory = $false)]
    [ValidateSet("marketplace", "mj-nlm", "mp-git", "mp-dev")]
    [string]$Scope = "marketplace",

    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Locate project root (script lives in scripts/)
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

# Build target file list based on scope
if ($Scope -eq "marketplace") {
    $TargetFiles = @(
        "VERSION",
        ".claude-plugin/marketplace.json",
        "README.md"
    )
    $MarketplaceJsonMode = "metadata"
} else {
    $TargetFiles = @(
        "plugins/$Scope/.claude-plugin/plugin.json",
        ".claude-plugin/marketplace.json",
        "README.md"
    )
    $MarketplaceJsonMode = "plugin:$Scope"
}

Write-Host ""
if ($DryRun) {
    Write-Host "[DryRun] Preview mode - no files will be modified" -ForegroundColor Yellow
} else {
    Write-Host "[Execute] Will modify files" -ForegroundColor Cyan
}
Write-Host "Scope: $Scope" -ForegroundColor White
Write-Host "Version: $From -> $To" -ForegroundColor White
Write-Host "Project root: $ProjectRoot" -ForegroundColor White
Write-Host ("-" * 60)

$TotalMatches = 0
$ModifiedFiles = 0

foreach ($RelPath in $TargetFiles) {
    $FilePath = Join-Path $ProjectRoot $RelPath

    if (-not (Test-Path $FilePath)) {
        Write-Host "  [SKIP] $RelPath - file not found" -ForegroundColor DarkGray
        continue
    }

    $Content = Get-Content -Path $FilePath -Raw -Encoding UTF8

    # Special handling for marketplace.json to avoid replacing wrong version fields
    if ($RelPath -eq ".claude-plugin/marketplace.json") {
        if ($MarketplaceJsonMode -eq "metadata") {
            # Only replace version in the metadata block
            $Pattern = '("metadata"\s*:\s*\{[^}]*"version"\s*:\s*")' + [regex]::Escape($From) + '"'
            $Replacement = '${1}' + $To + '"'
        } else {
            # Only replace version for the specific plugin entry
            $PluginName = $MarketplaceJsonMode -replace "^plugin:", ""
            $Pattern = '("name"\s*:\s*"' + [regex]::Escape($PluginName) + '"[^}]*"version"\s*:\s*")' + [regex]::Escape($From) + '"'
            $Replacement = '${1}' + $To + '"'
        }

        $MatchCount = ([regex]::Matches($Content, $Pattern, [System.Text.RegularExpressions.RegexOptions]::Singleline)).Count

        if ($MatchCount -eq 0) {
            Write-Host "  [SKIP] $RelPath - no match for '$From' in scope '$Scope'" -ForegroundColor DarkGray
            continue
        }

        Write-Host ""
        Write-Host "  [MATCH] $RelPath ($MatchCount occurrences, scoped: $Scope)" -ForegroundColor Green

        $Lines = @(Get-Content -Path $FilePath -Encoding UTF8)
        $EscapedFrom = [regex]::Escape($From)
        for ($i = 0; $i -lt $Lines.Count; $i++) {
            if ($Lines[$i] -match $EscapedFrom) {
                $LineNum = $i + 1
                $Before = $Lines[$i].Trim()
                $After = $Before -replace $EscapedFrom, $To
                Write-Host "    L${LineNum}: $Before" -ForegroundColor Red
                Write-Host "      -> $After" -ForegroundColor Green
            }
        }

        $TotalMatches += $MatchCount

        if (-not $DryRun) {
            $NewContent = [regex]::Replace($Content, $Pattern, $Replacement, [System.Text.RegularExpressions.RegexOptions]::Singleline)
            [System.IO.File]::WriteAllText($FilePath, $NewContent, [System.Text.UTF8Encoding]::new($false))
            $ModifiedFiles++
        }
    } else {
        # Simple string replacement for VERSION, plugin.json
        $EscapedFrom = [regex]::Escape($From)
        $MatchCount = ([regex]::Matches($Content, $EscapedFrom)).Count

        if ($MatchCount -eq 0) {
            Write-Host "  [SKIP] $RelPath - no match for '$From'" -ForegroundColor DarkGray
            continue
        }

        Write-Host ""
        Write-Host "  [MATCH] $RelPath ($MatchCount occurrences)" -ForegroundColor Green

        $Lines = @(Get-Content -Path $FilePath -Encoding UTF8)
        for ($i = 0; $i -lt $Lines.Count; $i++) {
            if ($Lines[$i] -match $EscapedFrom) {
                $LineNum = $i + 1
                $Before = $Lines[$i].Trim()
                $After = $Before -replace $EscapedFrom, $To
                Write-Host "    L${LineNum}: $Before" -ForegroundColor Red
                Write-Host "      -> $After" -ForegroundColor Green
            }
        }

        $TotalMatches += $MatchCount

        if (-not $DryRun) {
            $NewContent = $Content -replace $EscapedFrom, $To
            [System.IO.File]::WriteAllText($FilePath, $NewContent, [System.Text.UTF8Encoding]::new($false))
            $ModifiedFiles++
        }
    }
}

Write-Host ""
Write-Host ("-" * 60)
if ($DryRun) {
    Write-Host "[DryRun] Found $TotalMatches matches in scope '$Scope'" -ForegroundColor Yellow
    Write-Host "[DryRun] Remove -DryRun to apply changes" -ForegroundColor Yellow
} else {
    Write-Host "[Done] Modified $ModifiedFiles files, replaced $TotalMatches occurrences" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor White
    Write-Host '  1. git diff  (review changes)' -ForegroundColor White
    Write-Host '  2. Update CHANGELOG.md (move [Unreleased] to [X.Y.Z])' -ForegroundColor White
    Write-Host '  3. git add ... then git commit' -ForegroundColor White
}
Write-Host ""
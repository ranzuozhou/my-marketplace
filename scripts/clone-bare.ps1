# scripts/clone-bare.ps1
# 鍏嬮殕 MJ Marketplace 涓?Bare Repo + Worktree 缁撴瀯
# 鏀寔澧為噺妯″紡锛氶」鐩洰褰曞凡瀛樺湪鏃讹紝璺宠繃鍒濆鍖栵紝浠呮坊鍔犳柊 worktree
#
# Usage:
#   .\scripts\clone-bare.ps1 -RepoUrl <url> [-Branches "develop"]
#
# Examples:
#   # 鏂版垚鍛樺叆鑱岋紙鍏嬮殕 develop worktree锛?
#   powershell -ExecutionPolicy Bypass -File .\scripts\clone-bare.ps1 -RepoUrl https://github.com/ranzuozhou/my-marketplace
#
#   # 鍚屾椂鍒涘缓澶氫釜 worktree
#   powershell -ExecutionPolicy Bypass -File .\scripts\clone-bare.ps1 -RepoUrl https://github.com/ranzuozhou/my-marketplace -Branches "develop,main"
#
#   # 澧為噺娣诲姞鏂板垎鏀紙椤圭洰宸插瓨鍦ㄦ椂鑷姩璺宠繃鍒濆鍖栵級
#   powershell -ExecutionPolicy Bypass -File .\scripts\clone-bare.ps1 -RepoUrl https://github.com/ranzuozhou/my-marketplace -Branches "feature/1-some-feature"

param(
    [Parameter(Mandatory=$true)]
    [string]$RepoUrl,

    [Parameter(Mandatory=$false)]
    [string]$Branches = "develop"
)

$BranchList = @($Branches -split "," | ForEach-Object { $_.Trim() })
$ProjectName = ($RepoUrl -split "/")[-1]

if (Test-Path $ProjectName) {
    Write-Host ">>> Project directory '$ProjectName' already exists, entering incremental mode" -ForegroundColor Yellow
    Set-Location $ProjectName
} else {
    Write-Host ">>> Creating project directory: $ProjectName" -ForegroundColor Cyan
    mkdir $ProjectName | Out-Null
    Set-Location $ProjectName

    Write-Host ">>> Cloning bare repo..." -ForegroundColor Cyan
    git clone --bare $RepoUrl .bare
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "ERROR: git clone --bare failed (exit code: $LASTEXITCODE)" -ForegroundColor Red
        Write-Host "Possible causes:" -ForegroundColor Yellow
        Write-Host "  - Network unreachable or unstable" -ForegroundColor Yellow
        Write-Host "  - SSL certificate verification failed (check proxy/VPN)" -ForegroundColor Yellow
        Write-Host "  - Repository URL is incorrect: $RepoUrl" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Cleaning up empty project directory..." -ForegroundColor Yellow
        Set-Location ..
        Remove-Item -Recurse -Force $ProjectName
        exit 1
    }

    Write-Host ">>> Creating .git pointer..." -ForegroundColor Cyan
    New-Item .git -ItemType File -Value "gitdir: ./.bare" | Out-Null
}

Write-Host ">>> Fixing refspec and fetching..." -ForegroundColor Cyan
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git fetch origin
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: git fetch origin failed (exit code: $LASTEXITCODE)" -ForegroundColor Red
    Write-Host "Possible causes:" -ForegroundColor Yellow
    Write-Host "  - Network unreachable or unstable" -ForegroundColor Yellow
    Write-Host "  - SSL certificate verification failed (check proxy/VPN)" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

foreach ($Branch in $BranchList) {
    if (Test-Path $Branch) {
        Write-Host ">>> Worktree '$Branch' already exists, skipping" -ForegroundColor Yellow
    } else {
        Write-Host ">>> Adding worktree: $Branch" -ForegroundColor Cyan
        git worktree add $Branch $Branch
        if ($LASTEXITCODE -ne 0) {
            Write-Host "WARNING: Failed to add worktree '$Branch' (exit code: $LASTEXITCODE), skipping" -ForegroundColor Red
            continue
        }
    }
}

$FirstBranch = $BranchList[0]
if (-not (Test-Path $FirstBranch)) {
    Write-Host ""
    Write-Host "WARNING: No worktree was created successfully" -ForegroundColor Red
    exit 0
}

# Return to project root (handle nested paths like feature/12-add-skill)
Set-Location $FirstBranch
Write-Host ">>> Verifying remotes..." -ForegroundColor Cyan
git remote -v

$Depth = ($FirstBranch -split "/").Count
Set-Location ("../" * $Depth)

Write-Host ""
Write-Host "Done! Directory structure:" -ForegroundColor Green
Get-ChildItem -Force | Select-Object Name
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  cd $ProjectName/$FirstBranch" -ForegroundColor White
Write-Host "  git push origin HEAD" -ForegroundColor White
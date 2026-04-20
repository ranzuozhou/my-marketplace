<#
.SYNOPSIS
    定位 draw.io Desktop CLI(drawio.exe)路径。

.DESCRIPTION
    按 ProgramFiles / LOCALAPPDATA / ProgramFiles(x86) 优先级依次探测。
    找到返回路径字符串(stdout,exit 0),未找到报 winget 安装指引(stderr,exit 1)。

    两个 skill(mj-drawio-create / mj-drawio-export)共用此脚本。
#>

$candidates = @(
    "$env:ProgramFiles\draw.io\draw.io.exe",
    "$env:LOCALAPPDATA\Programs\draw.io\draw.io.exe",
    "${env:ProgramFiles(x86)}\draw.io\draw.io.exe"
)

foreach ($p in $candidates) {
    if (Test-Path $p) {
        Write-Output $p
        exit 0
    }
}

Write-Error "draw.io Desktop 未找到。请运行: winget install JGraph.Draw"
exit 1

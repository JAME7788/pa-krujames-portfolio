$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$stage = Join-Path $root 'tmp\publish-photo-review-20260913'
New-Item -ItemType Directory -Force -Path $stage | Out-Null
# Deploy website directories only, never workspace reports, student source data, or QA output.
foreach ($name in @('index.html', 'admin.html', 'firebase-config.js', 'vercel.json')) {
  Copy-Item -LiteralPath (Join-Path $root $name) -Destination $stage -Force
}
foreach ($name in @('assets', 'assets_drop', 'embeds')) {
  Copy-Item -LiteralPath (Join-Path $root $name) -Destination $stage -Recurse -Force
}
New-Item -ItemType Directory -Force -Path (Join-Path $stage '.vercel') | Out-Null
Copy-Item -LiteralPath (Join-Path $root '.vercel\project.json') -Destination (Join-Path $stage '.vercel\project.json') -Force
Write-Output $stage

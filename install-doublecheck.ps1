$ErrorActionPreference = "Stop"

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$homeRoot = if ($env:DOUBLECHECK_HOME) { $env:DOUBLECHECK_HOME } else { $HOME }
$pluginSource = Join-Path $scriptRoot "plugin\doublecheck"
$targetPluginRoot = Join-Path $homeRoot "plugins\doublecheck"
$marketplacePath = Join-Path $homeRoot ".agents\plugins\marketplace.json"
$pythonCandidates = @(
  "C:\Users\yamat\AppData\Local\Programs\Python\Python313\python.exe",
  "py"
)

if (-not (Test-Path $pluginSource)) {
  throw "Plugin source not found: $pluginSource"
}

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $targetPluginRoot) | Out-Null
if (Test-Path $targetPluginRoot) {
  Remove-Item -Recurse -Force -LiteralPath $targetPluginRoot
}
Copy-Item -Recurse -Force -LiteralPath $pluginSource -Destination $targetPluginRoot

$pythonCommand = $null
foreach ($candidate in $pythonCandidates) {
  if ($candidate -eq "py") {
    if (Get-Command py -ErrorAction SilentlyContinue) {
      $pythonCommand = @("py", "-3")
      break
    }
  } elseif (Test-Path $candidate) {
    $pythonCommand = @($candidate)
    break
  }
}

if (-not $pythonCommand) {
  throw "Python 3 was not found. Install Python 3 before running this installer."
}

if (-not (Get-Command npx -ErrorAction SilentlyContinue)) {
  throw "npx was not found. Install Node.js before running this installer."
}

if ($pythonCommand.Length -eq 1) {
  & $pythonCommand[0] `
    (Join-Path $scriptRoot "scripts\upsert_marketplace.py") `
    $marketplacePath `
    --plugin-name doublecheck `
    --source-path ./plugins/doublecheck
} else {
  & $pythonCommand[0] $pythonCommand[1] `
    (Join-Path $scriptRoot "scripts\upsert_marketplace.py") `
    $marketplacePath `
    --plugin-name doublecheck `
    --source-path ./plugins/doublecheck
}

Write-Host "Installed doublecheck to $targetPluginRoot"
Write-Host "Updated marketplace: $marketplacePath"

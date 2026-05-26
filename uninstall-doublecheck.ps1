$ErrorActionPreference = "Stop"

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$homeRoot = if ($env:DOUBLECHECK_HOME) { $env:DOUBLECHECK_HOME } else { $HOME }
$targetPluginRoot = Join-Path $homeRoot "plugins\doublecheck"
$marketplacePath = Join-Path $homeRoot ".agents\plugins\marketplace.json"
$pythonCandidates = @(
  "C:\Users\yamat\AppData\Local\Programs\Python\Python313\python.exe",
  "py"
)

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
  throw "Python 3 was not found. Install Python 3 before running this uninstaller."
}

if (Test-Path $targetPluginRoot) {
  Remove-Item -Recurse -Force -LiteralPath $targetPluginRoot
}

if ($pythonCommand.Length -eq 1) {
  & $pythonCommand[0] `
    (Join-Path $scriptRoot "scripts\upsert_marketplace.py") `
    $marketplacePath `
    --mode uninstall `
    --plugin-name doublecheck
} else {
  & $pythonCommand[0] $pythonCommand[1] `
    (Join-Path $scriptRoot "scripts\upsert_marketplace.py") `
    $marketplacePath `
    --mode uninstall `
    --plugin-name doublecheck
}

Write-Host "Removed doublecheck from $targetPluginRoot"
Write-Host "Updated marketplace: $marketplacePath"

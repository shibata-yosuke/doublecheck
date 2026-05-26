$ErrorActionPreference = "Stop"

$repoSlug = if ($env:DOUBLECHECK_REPO_SLUG) { $env:DOUBLECHECK_REPO_SLUG } else { "shibata-yosuke/doublecheck" }
$repoRef = if ($env:DOUBLECHECK_REPO_REF) { $env:DOUBLECHECK_REPO_REF } else { "main" }
$archivePath = $env:DOUBLECHECK_ARCHIVE_PATH
$archiveUrl = if ($env:DOUBLECHECK_ARCHIVE_URL) {
  $env:DOUBLECHECK_ARCHIVE_URL
} else {
  "https://github.com/$repoSlug/archive/refs/heads/$repoRef.zip"
}

$tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("doublecheck-" + [System.Guid]::NewGuid().ToString("N"))
$archiveFile = Join-Path $tempRoot "doublecheck.zip"
$extractDir = Join-Path $tempRoot "extracted"

New-Item -ItemType Directory -Force -Path $tempRoot | Out-Null

try {
  if ($archivePath) {
    Copy-Item -LiteralPath $archivePath -Destination $archiveFile
  } else {
    Invoke-WebRequest -Uri $archiveUrl -OutFile $archiveFile
  }

  Expand-Archive -LiteralPath $archiveFile -DestinationPath $extractDir -Force
  $installScript = Join-Path $extractDir "install-doublecheck.ps1"
  if (-not (Test-Path $installScript)) {
    $repoDir = Get-ChildItem -Path $extractDir -Directory | Select-Object -First 1
    if (-not $repoDir) {
      throw "Could not find extracted repository directory."
    }
    $installScript = Join-Path $repoDir.FullName "install-doublecheck.ps1"
  }
  if (-not (Test-Path $installScript)) {
    throw "Could not find install-doublecheck.ps1 in downloaded archive."
  }

  & $installScript
} finally {
  if (Test-Path $tempRoot) {
    Remove-Item -Recurse -Force -LiteralPath $tempRoot
  }
}

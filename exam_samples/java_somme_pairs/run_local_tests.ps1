param(
    [ValidateSet("ok", "ko")]
    [string]$Solution = "ok"
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$sourceFile = Join-Path $scriptDir ("solutions\\Main_{0}.java" -f $Solution)
$targetFile = Join-Path $scriptDir "tests_repo\\src\\Main.java"

if (-not (Test-Path $sourceFile)) {
    Write-Error "Solution introuvable: $sourceFile"
    exit 1
}

Copy-Item -Path $sourceFile -Destination $targetFile -Force

$testsDir = Join-Path $scriptDir "tests_repo"
Push-Location $testsDir

$exitCode = 0
try {
    mvn -q clean test
    $exitCode = $LASTEXITCODE
} finally {
    Pop-Location
}

exit $exitCode

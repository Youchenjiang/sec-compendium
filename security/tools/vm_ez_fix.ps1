# vm_ez_fix.ps1 - diagnose the Microsoft.PowerShell.Archive failure and repair EZ Tools
#
# Symptom observed on the guest: Get-ZimmermanTools.ps1 reported
#   Error downloading iisGeolocate.zip
#   (Cannot load module 'Microsoft.PowerShell.Archive'. Run 'Import-Module Microsoft.PowerShell.Archive'.)
# and C:\Tools\DFIR\EZTools ended up with 0 exes.
#
# This script:
#   1. reports PS version, language mode, PSModulePath and whether the Archive module dir exists
#   2. actually EXERCISES Expand-Archive on a throwaway zip (resolving the command is not enough:
#      it resolves even when loading the module fails)
#   3. if it fails, installs a global Expand-Archive shim backed by
#      System.IO.Compression.ZipFile (present in .NET Framework 4.5+)
#   4. re-runs the EZ Tools fetcher and reports a real exe count
#
# ASCII-only output: the guest console codepage is CP950 and mojibake would hide failures.

[CmdletBinding()]
param(
    [string]$Dest = 'C:\Tools\DFIR',
    [switch]$SkipInstall
)

$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$UA = @{ 'User-Agent' = 'vm-ez-fix' }
$tmp = Join-Path $env:TEMP 'ezfix'

function Log { param([string]$m) Write-Output $m }

Log '### DIAG ###'
$mod = Get-Module -ListAvailable Microsoft.PowerShell.Archive -ErrorAction SilentlyContinue
if ($mod) {
    Log ('archive-module  : ' + (($mod | ForEach-Object { $_.Path }) -join ';'))
} else {
    Log 'archive-module  : MISSING (not listed)'
}
Log ('psversion       : ' + $PSVersionTable.PSVersion)
Log ('language-mode   : ' + $ExecutionContext.SessionState.LanguageMode)
Log ('psmodulepath    : ' + $env:PSModulePath)
Log ('archive-dir     : ' + (Test-Path 'C:\Windows\System32\WindowsPowerShell\v1.0\Modules\Microsoft.PowerShell.Archive'))
foreach ($d in @(
    'C:\Windows\System32\WindowsPowerShell\v1.0\Modules\Microsoft.PowerShell.Archive',
    'C:\Windows\System32\WindowsPowerShell\v1.0\Modules\Microsoft.PowerShell.Archive\Microsoft.PowerShell.Archive.psd1'
)) {
    Log ('exists {0,-6} {1}' -f (Test-Path $d), $d)
}

Log ''
Log '### ZIP TYPE ###'
$zipOk = $false
try {
    Add-Type -AssemblyName System.IO.Compression.FileSystem -ErrorAction Stop
    $zipOk = $true
    Log 'System.IO.Compression.FileSystem : OK'
} catch {
    Log ('System.IO.Compression.FileSystem : FAIL ' + $_.Exception.Message)
}

Log ''
Log '### EXERCISE Expand-Archive ###'
$probeOk = $false
try {
    if (-not (Test-Path $tmp)) { New-Item -ItemType Directory -Path $tmp -Force | Out-Null }
    $src = Join-Path $tmp 'src'
    if (Test-Path $src) { Remove-Item $src -Recurse -Force }
    New-Item -ItemType Directory -Path $src -Force | Out-Null
    'probe' | Out-File (Join-Path $src 'probe.txt') -Encoding ascii
    $probeZip = Join-Path $tmp 'probe.zip'
    if (Test-Path $probeZip) { Remove-Item $probeZip -Force }
    [System.IO.Compression.ZipFile]::CreateFromDirectory($src, $probeZip)
    $probeOut = Join-Path $tmp 'out'
    if (Test-Path $probeOut) { Remove-Item $probeOut -Recurse -Force }
    Expand-Archive -Path $probeZip -DestinationPath $probeOut -Force -ErrorAction Stop
    $probeOk = Test-Path (Join-Path $probeOut 'probe.txt')
    Log ('Expand-Archive  : ' + $(if ($probeOk) { 'WORKS' } else { 'ran but produced nothing' }))
} catch {
    Log ('Expand-Archive  : FAILED -> ' + $_.Exception.Message)
}

if (-not $probeOk -and $zipOk) {
    Log ''
    Log '### INSTALLING SHIM ###'
    function global:Expand-Archive {
        [CmdletBinding()]
        param(
            [Parameter(Mandatory, Position = 0)][string]$Path,
            [Parameter(Position = 1)][string]$DestinationPath = '.',
            [switch]$Force
        )
        if (-not [System.IO.Compression.ZipFile]) { Add-Type -AssemblyName System.IO.Compression.FileSystem }
        $full = [System.IO.Path]::GetFullPath($DestinationPath)
        if ($Force -and (Test-Path $full)) { Remove-Item $full -Recurse -Force }
        if (-not (Test-Path $full)) { New-Item -ItemType Directory -Path $full -Force | Out-Null }
        [System.IO.Compression.ZipFile]::ExtractToDirectory($Path, $full)
    }
    $probeOut2 = Join-Path $tmp 'out2'
    if (Test-Path $probeOut2) { Remove-Item $probeOut2 -Recurse -Force }
    Expand-Archive -Path (Join-Path $tmp 'probe.zip') -DestinationPath $probeOut2 -Force
    Log ('shim probe      : ' + (Test-Path (Join-Path $probeOut2 'probe.txt')))
}

if ($SkipInstall) { Log ''; Log '### SKIP INSTALL ###'; exit 0 }

Log ''
Log '### EZ TOOLS INSTALL ###'
$ezDir = Join-Path $Dest 'EZTools'
try {
    $fetcher = Join-Path $env:TEMP 'Get-ZimmermanTools.ps1'
    Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/EricZimmerman/Get-ZimmermanTools/master/Get-ZimmermanTools.ps1' `
        -OutFile $fetcher -UseBasicParsing -Headers $UA -TimeoutSec 120
    Log ('fetcher bytes   : ' + (Get-Item $fetcher).Length)
    $transcript = Join-Path $env:TEMP 'ez_fix_transcript.txt'
    Start-Transcript -Path $transcript -Force | Out-Null
    & $fetcher -Dest $ezDir -NetVersion 9
    Stop-Transcript | Out-Null
    $exes = @(Get-ChildItem $ezDir -Filter '*.exe' -Recurse -ErrorAction SilentlyContinue)
    Log ('exes found      : ' + $exes.Count)
    foreach ($e in ($exes | Sort-Object Name | Select-Object -First 12)) { Log ('  ' + $e.Name) }
    if ($exes.Count -eq 0) {
        Log '--- transcript tail ---'
        Get-Content $transcript -Tail 15 -ErrorAction SilentlyContinue
    }
} catch {
    Log ('FAILED: ' + $_.Exception.Message)
}

Log ''
Log '### DONE ###'

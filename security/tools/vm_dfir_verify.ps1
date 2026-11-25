# vm_dfir_verify.ps1 - prove the DFIR toolchain actually runs, using the guest's own event logs
#
# Installed by vm_setup_dfir.ps1; this script is read-mostly: it copies live event logs out
# with wevtutil (the files are held open by the Event Log service) and writes reports to $Out.
#
# ASCII-only output: the guest console codepage is CP950.

[CmdletBinding()]
param(
    [string]$Root = 'C:\Tools\DFIR',
    [string]$Out = 'C:\Tools\DFIR\out'
)

$ErrorActionPreference = 'Continue'
$sysModules = Join-Path $env:windir 'System32\WindowsPowerShell\v1.0\Modules'
if ($env:PSModulePath -notlike "*$sysModules*") {
    $env:PSModulePath = $sysModules + ';' + $env:PSModulePath
}
function Log { param([string]$m) Write-Output $m }

$ezDir = Join-Path $Root 'EZTools'
$chainsaw = Join-Path $Root 'chainsaw\chainsaw.exe'
$hayabusa = Get-ChildItem (Join-Path $Root 'hayabusa') -Filter 'hayabusa*.exe' -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
$evtxecmd = Get-ChildItem $ezDir -Filter 'EvtxECmd.exe' -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1

if (-not (Test-Path $Out)) { New-Item -ItemType Directory -Path $Out -Force | Out-Null }

Log '### TOOL PATHS ###'
Log ('chainsaw    : ' + $(if (Test-Path $chainsaw) { $chainsaw } else { 'MISSING' }))
Log ('hayabusa    : ' + $(if ($hayabusa) { $hayabusa.FullName } else { 'MISSING' }))
Log ('EvtxECmd    : ' + $(if ($evtxecmd) { $evtxecmd.FullName } else { 'MISSING' }))
Log ('sysmon svc  : ' + (Get-Service Sysmon64 -ErrorAction SilentlyContinue).Status)
Log ('sysmondrv   : ' + (Get-Service SysmonDrv  -ErrorAction SilentlyContinue).Status)

Log ''
Log '### EZ TOOLS EXES (relative to EZTools) ###'
Get-ChildItem $ezDir -Filter '*.exe' -Recurse -ErrorAction SilentlyContinue |
    Sort-Object FullName |
    ForEach-Object { Log ('  ' + $_.FullName.Substring($ezDir.Length + 1)) }

Log ''
Log '### VERSIONS ###'
try { Log ('chainsaw    : ' + ((& $chainsaw --version 2>&1 | Select-Object -First 1) -join ' ')) } catch { Log ('chainsaw    : FAIL ' + $_.Exception.Message) }
try {
    $hbVer = ((& $hayabusa.FullName --version 2>&1) -join ' ').Trim()
    Log ('hayabusa    : ' + $hbVer)
} catch {
    Log ('hayabusa    : FAIL ' + $_.Exception.Message)
}

Log ''
Log '### EXPORT LIVE EVENT LOGS ###'
$evtxDir = Join-Path $Out 'evtx'
if (-not (Test-Path $evtxDir)) { New-Item -ItemType Directory -Path $evtxDir -Force | Out-Null }
foreach ($name in @('Security', 'System', 'Application', 'Microsoft-Windows-Sysmon/Operational')) {
    $file = Join-Path $evtxDir (($name -replace '/', '_') + '.evtx')
    & wevtutil epl $name $file 2>&1 | Out-Null
    if (Test-Path $file) {
        Log ('{0,-42} {1} bytes' -f $name, (Get-Item $file).Length)
    } else {
        Log ('{0,-42} export FAILED' -f $name)
    }
}

Log ''
Log '### RUN: EvtxECmd (CSV timeline) ###'
try {
    $csvOut = Join-Path $Out 'evtxecmd'
    if (-not (Test-Path $csvOut)) { New-Item -ItemType Directory -Path $csvOut -Force | Out-Null }
    $sec = Join-Path $evtxDir 'Security.evtx'
    & $evtxecmd.FullName -f $sec --csv $csvOut --csvf security.csv 2>&1 | Select-Object -Last 4 | ForEach-Object { Log ('  ' + $_) }
    $csvFile = Join-Path $csvOut 'security.csv'
    if (Test-Path $csvFile) {
        $lines = @(Get-Content $csvFile)
        Log ('  rows        : ' + ($lines.Count - 1))
        Log ('  header      : ' + $lines[0].Substring(0, [Math]::Min(150, $lines[0].Length)))
    }
} catch {
    Log ('  FAIL ' + $_.Exception.Message)
}

Log ''
Log '### RUN: Hayabusa (threat hunt) ###'
try {
    $hbOut = Join-Path $Out 'hayabusa_security.csv'
    $hbArgs = @('-d', $evtxDir, '-o', $hbOut, '-q')
    & $hayabusa.FullName @hbArgs 2>&1 | Select-Object -Last 6 | ForEach-Object { Log ('  ' + $_) }
    if (Test-Path $hbOut) {
        $hb = @(Import-Csv $hbOut -ErrorAction SilentlyContinue)
        Log ('  detections  : ' + $hb.Count)
    } else {
        Log '  no CSV produced'
    }
} catch {
    Log ('  FAIL ' + $_.Exception.Message)
}

Log ''
Log '### RUN: Chainsaw (rules bundled?) ###'
try {
    $csDir = Split-Path $chainsaw -Parent
    Log ('  rules dir   : ' + (Test-Path (Join-Path $csDir 'rules')))
    Get-ChildItem $csDir -Directory -ErrorAction SilentlyContinue | ForEach-Object { Log ('  subdir      : ' + $_.Name) }
} catch {
    Log ('  FAIL ' + $_.Exception.Message)
}

Log ''
Log '### DONE ###'

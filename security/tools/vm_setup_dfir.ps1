# vm_setup_dfir.ps1 - install the DFIR toolchain on a Windows lab VM
#
# Installs (idempotent, skips what already exists):
#   1. Eric Zimmerman Tools  (EvtxECmd / MFTECmd / PECmd / AmcacheParser / RECmd / ...)  - Windows only
#   2. Chainsaw              (Sigma-based EVTX hunting, Rust binary)
#   3. Hayabusa              (EVTX threat hunting with ATT&CK mapping, Rust binary)
#   4. Sysmon                (telemetry source, for generating practice samples)
#   5. optional EVTX sample set (sbousseaden/EVTX-ATTACK-SAMPLES)
#
# Usage (from the host, via the vmrun wrapper):
#   put  security/tools/vm_setup_dfir.ps1  C:\Windows\Temp\setup_dfir.ps1
#   exec powershell -NoProfile -ExecutionPolicy Bypass -File C:\Windows\Temp\setup_dfir.ps1 -DryRun
#   exec powershell -NoProfile -ExecutionPolicy Bypass -File C:\Windows\Temp\setup_dfir.ps1
#
# IMPORTANT: all output strings are ASCII-only. The guest console codepage is CP950,
# so non-ASCII text turns into mojibake once cmd.exe redirects stdout to a file.
#
# NOTE: Get-ZimmermanTools.ps1 writes via Write-Host, which BYPASSES stdout redirection
# in PowerShell 5.1. It is therefore wrapped in Start-Transcript so its output is captured.

[CmdletBinding()]
param(
    [string]$Dest = 'C:\Tools\DFIR',
    [switch]$DryRun,
    [switch]$WithSamples,
    [switch]$InstallSysmon,
    [switch]$Force
)

$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$UA = @{ 'User-Agent' = 'vm-setup-dfir' }

$script:Summary = @()

function Log { param([string]$Message) Write-Output $Message }
function Note { param([string]$Name, [string]$Status, [string]$Detail = '')
    Log ('{0,-26} {1,-10} {2}' -f $Name, $Status, $Detail)
    $script:Summary += [pscustomobject]@{ Tool = $Name; Status = $Status; Detail = $Detail }
}

# Repair PSModulePath before installing anything.
# Measured on the FLARE-VM guest: PSModulePath had been overridden to a user-only path
# (C:\Users\LabStrix\Documents\WindowsPowerShell\Modules), so the system module directory
# was absent. Expand-Archive therefore failed to autoload Microsoft.PowerShell.Archive
# INTERMITTENTLY -- Get-ZimmermanTools.ps1 aborted with
#   Cannot load module 'Microsoft.PowerShell.Archive'
# and left 0 exes installed. Prepending the system path makes it deterministic.
$sysModules = Join-Path $env:windir 'System32\WindowsPowerShell\v1.0\Modules'
if ($env:PSModulePath -notlike "*$sysModules*") {
    $env:PSModulePath = $sysModules + ';' + $env:PSModulePath
}

function Get-GithubAsset {
    param([string]$Repo, [string[]]$Patterns)
    try {
        $rel = Invoke-RestMethod -Uri "https://api.github.com/repos/$Repo/releases/latest" -Headers $UA -TimeoutSec 30
    } catch {
        return $null
    }
    foreach ($p in $Patterns) {
        $a = $rel.assets | Where-Object { $_.name -match $p } | Select-Object -First 1
        if ($a) {
            return [pscustomobject]@{
                Tag  = $rel.tag_name
                Name = $a.name
                Url  = $a.browser_download_url
                Size = [math]::Round($a.size / 1MB, 1)
            }
        }
    }
    return $null
}

function Save-File {
    param([string]$Url, [string]$OutFile)
    Invoke-WebRequest -Uri $Url -OutFile $OutFile -UseBasicParsing -Headers $UA -TimeoutSec 900
    return (Get-Item $OutFile).Length
}

# ---------------------------------------------------------------- environment
Log '### ENVIRONMENT ###'
"Dest        : [$Dest]"
"BoundParams : [$($PSBoundParameters.Keys -join ',')]"
"PSModulePath: [$env:PSModulePath]"
"ScriptRoot  : [$PSScriptRoot]"
"IsAdmin     : $((New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator))"
Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" | ForEach-Object {
    'Disk {0} free {1} GB / total {2} GB' -f $_.DeviceID, [math]::Round($_.FreeSpace / 1GB, 1), [math]::Round($_.Size / 1GB, 1)
}
$dotnet = (& dotnet --list-runtimes 2>$null) -join '; '
"DOTNET      : $(if ($dotnet) { $dotnet.Substring(0, [Math]::Min(160, $dotnet.Length)) } else { 'none' })"
if (-not (Test-Path $Dest)) {
    if ($DryRun) { "Would create: $Dest" } else { New-Item -ItemType Directory -Path $Dest -Force | Out-Null; "Created: $Dest" }
}

if ($DryRun) { Log ''; Log '### DRY RUN: resolving download sources ###' }

# ---------------------------------------------------------------- 1. EZ Tools
Log ''
Log '### 1. ERIC ZIMMERMAN TOOLS ###'
$ezDir = Join-Path $Dest 'EZTools'
$ezHave = Test-Path (Join-Path $ezDir 'EvtxECmd.exe')
if ($ezHave -and -not $Force) {
    Note 'ez-tools' 'SKIP' $ezDir
} elseif ($DryRun) {
    Note 'ez-tools' 'WOULD-INSTALL' 'Get-ZimmermanTools.ps1 -Dest EZTools (net9)'
} else {
    try {
        $fetcher = Join-Path $env:TEMP 'Get-ZimmermanTools.ps1'
        $null = Save-File 'https://raw.githubusercontent.com/EricZimmerman/Get-ZimmermanTools/master/Get-ZimmermanTools.ps1' $fetcher
        $transcript = Join-Path $env:TEMP 'ez_tools_transcript.txt'
        Start-Transcript -Path $transcript -Force | Out-Null
        & $fetcher -Dest $ezDir -NetVersion 9
        Stop-Transcript | Out-Null
        # Recurse: the upstream zips have mixed layouts, so some tools land in subdirectories
        # (e.g. EZTools\net9\EvtxeCmd\EvtxECmd.exe) and a flat count reports a false zero.
        $exe = @(Get-ChildItem $ezDir -Filter '*.exe' -Recurse -ErrorAction SilentlyContinue)
        if ($exe.Count -eq 0) {
            Note 'ez-tools' 'FAILED' ("0 exes under {0}; see transcript" -f $ezDir)
        } else {
            Note 'ez-tools' 'INSTALLED' ("{0} exes under {1}" -f $exe.Count, $ezDir)
        }
        "--- transcript tail ---"
        Get-Content $transcript -Tail 12 -ErrorAction SilentlyContinue
    } catch {
        Note 'ez-tools' 'FAILED' $_.Exception.Message
    }
}

# ---------------------------------------------------------------- 2. Chainsaw
Log ''
Log '### 2. CHAINSAW ###'
$csDir = Join-Path $Dest 'chainsaw'
if ((Test-Path (Join-Path $csDir 'chainsaw.exe')) -and -not $Force) {
    Note 'chainsaw' 'SKIP' $csDir
} else {
    $cs = Get-GithubAsset -Repo 'WithSecureLabs/chainsaw' -Patterns @('x86_64-pc-windows-msvc', 'windows', 'win')
    if (-not $cs) {
        Note 'chainsaw' 'FAILED' 'no Windows asset found via GitHub API'
    } elseif ($DryRun) {
        Note 'chainsaw' 'WOULD-INSTALL' ("{0} ({1} MB) {2}" -f $cs.Name, $cs.Size, $cs.Tag)
    } else {
        try {
            $zip = Join-Path $env:TEMP $cs.Name
            $null = Save-File $cs.Url $zip
            Expand-Archive -Path $zip -DestinationPath $csDir -Force
            # The upstream zip ships a single top-level directory, so the binary lands at
            # chainsaw\chainsaw\chainsaw.exe. Flatten it so the documented path holds.
            $nested = Join-Path $csDir 'chainsaw'
            if ((Test-Path (Join-Path $nested 'chainsaw.exe')) -and -not (Test-Path (Join-Path $csDir 'chainsaw.exe'))) {
                Get-ChildItem $nested -Force | ForEach-Object { Move-Item $_.FullName $csDir -Force }
                Remove-Item $nested -Recurse -Force -ErrorAction SilentlyContinue
                Note 'chainsaw' 'FLATTENED' 'moved chainsaw\chainsaw\* up one level'
            }
            $rules = Test-Path (Join-Path $csDir 'rules')
            $maps = Test-Path (Join-Path $csDir 'mappings')
            Note 'chainsaw' 'INSTALLED' ("{0} rules={1} mappings={2}" -f $cs.Tag, $rules, $maps)
        } catch {
            Note 'chainsaw' 'FAILED' $_.Exception.Message
        }
    }
}

# ---------------------------------------------------------------- 3. Hayabusa
Log ''
Log '### 3. HAYABUSA ###'
$hbDir = Join-Path $Dest 'hayabusa'
if ((Test-Path (Join-Path $hbDir 'hayabusa.exe')) -and -not $Force) {
    Note 'hayabusa' 'SKIP' $hbDir
} else {
    $hb = Get-GithubAsset -Repo 'Yamato-Security/hayabusa' -Patterns @('win-x64', 'all-platforms', 'windows')
    if (-not $hb) {
        Note 'hayabusa' 'FAILED' 'no asset found via GitHub API'
    } elseif ($DryRun) {
        Note 'hayabusa' 'WOULD-INSTALL' ("{0} ({1} MB) {2}" -f $hb.Name, $hb.Size, $hb.Tag)
    } else {
        try {
            $zip = Join-Path $env:TEMP $hb.Name
            $null = Save-File $hb.Url $zip
            Expand-Archive -Path $zip -DestinationPath $hbDir -Force
            $found = Get-ChildItem $hbDir -Filter 'hayabusa*.exe' -Recurse | Select-Object -First 1
            Note 'hayabusa' 'INSTALLED' ("{0} -> {1}" -f $hb.Tag, $(if ($found) { $found.FullName } else { $hbDir }))
            # Hayabusa v4 expects `hayabusa <COMMAND>` (dfir-timeline replaces the old csv-timeline).
            # The live-response zip ships no rules, so pull them from the hayabusa-rules repo.
            if ($found) {
                try {
                    & $found.FullName update-rules 2>&1 | Select-Object -Last 4 | ForEach-Object { Log ('  ' + $_) }
                    $rc = Join-Path $hbDir 'rules'
                    Note 'hayabusa-rules' 'READY' ("{0} files under {1}" -f @(Get-ChildItem $rc -Recurse -ErrorAction SilentlyContinue).Count, $rc)
                } catch {
                    Note 'hayabusa-rules' 'FAILED' $_.Exception.Message
                }
            }
        } catch {
            Note 'hayabusa' 'FAILED' $_.Exception.Message
        }
    }
}

# ---------------------------------------------------------------- 4. Sysmon
Log ''
Log '### 4. SYSMON ###'
$sysmonSvc = Get-Service -Name 'Sysmon64' -ErrorAction SilentlyContinue
if ($sysmonSvc) {
    Note 'sysmon' 'SKIP' ("service {0}" -f $sysmonSvc.Status)
} elseif ($DryRun -or -not $InstallSysmon) {
    $why = if ($DryRun) { 'dry-run; use -InstallSysmon to install' } else { 'pass -InstallSysmon to install' }
    Note 'sysmon' 'NOT-INSTALLED' $why
} else {
    try {
        $smExe = Join-Path $Dest 'Sysmon64.exe'
        $smCfg = Join-Path $Dest 'sysmonconfig.xml'
        $null = Save-File 'https://live.sysinternals.com/Sysmon64.exe' $smExe
        $null = Save-File 'https://raw.githubusercontent.com/SwiftOnSecurity/sysmon-config/master/sysmonconfig-export.xml' $smCfg
        & $smExe -accepteula -i $smCfg | Out-Null
        Start-Sleep -Seconds 3
        Note 'sysmon' 'INSTALLED' ((Get-Service -Name 'Sysmon64' -ErrorAction SilentlyContinue).Status)
    } catch {
        Note 'sysmon' 'FAILED' $_.Exception.Message
    }
}

# ---------------------------------------------------------------- 5. Samples
Log ''
Log '### 5. EVTX SAMPLE SET ###'
$sampleDir = Join-Path $Dest 'samples'
if ((Test-Path $sampleDir) -and -not $Force) {
    Note 'evtx-samples' 'SKIP' $sampleDir
} elseif ($DryRun -or -not $WithSamples) {
    Note 'evtx-samples' 'SKIPPED' 'pass -WithSamples to download EVTX-ATTACK-SAMPLES'
} else {
    try {
        $zip = Join-Path $env:TEMP 'evtx-samples.zip'
        $null = Save-File 'https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES/archive/refs/heads/master.zip' $zip
        Expand-Archive -Path $zip -DestinationPath $sampleDir -Force
        $n = (Get-ChildItem $sampleDir -Filter '*.evtx' -Recurse).Count
        Note 'evtx-samples' 'INSTALLED' ("{0} .evtx files" -f $n)
    } catch {
        Note 'evtx-samples' 'FAILED' $_.Exception.Message
    }
}

# ---------------------------------------------------------------- 6. Sigma rules
Log ''
Log '### 6. SIGMA RULES (for Chainsaw hunt) ###'
# The Chainsaw Windows zip ships mappings/ but NO rules/, so `chainsaw hunt` cannot run
# out of the box. SigmaHQ is the upstream rule set that the bundled mappings target.
$sigmaDir = Join-Path $Dest 'sigma-rules'
$sigmaRoot = Join-Path $sigmaDir 'sigma-master'
if ((Test-Path (Join-Path $sigmaRoot 'rules')) -and -not $Force) {
    Note 'sigma-rules' 'SKIP' $sigmaRoot
} elseif ($DryRun) {
    Note 'sigma-rules' 'WOULD-INSTALL' 'SigmaHQ/sigma master.zip -> sigma-rules\sigma-master\rules'
} else {
    try {
        $zip = Join-Path $env:TEMP 'sigma.zip'
        $null = Save-File 'https://github.com/SigmaHQ/sigma/archive/refs/heads/master.zip' $zip
        Expand-Archive -Path $zip -DestinationPath $sigmaDir -Force
        $n = @(Get-ChildItem (Join-Path $sigmaRoot 'rules') -Filter '*.yml' -Recurse -ErrorAction SilentlyContinue).Count
        Note 'sigma-rules' 'INSTALLED' ("{0} yml rules under {1}" -f $n, (Join-Path $sigmaRoot 'rules'))
    } catch {
        Note 'sigma-rules' 'FAILED' $_.Exception.Message
    }
}

# ---------------------------------------------------------------- summary
Log ''
Log '### SUMMARY ###'
$script:Summary | ForEach-Object { '{0,-26} {1,-14} {2}' -f $_.Tool, $_.Status, $_.Detail }
Log ''
Log '### DONE ###'

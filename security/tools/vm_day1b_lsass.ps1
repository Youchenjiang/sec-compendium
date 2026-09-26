# vm_day1b_lsass.ps1 -- Day 1B Phase B: turn Sysmon EID 10 back on and re-run
# the exact same LSASS handle-open from Phase A, so the delta is unambiguous.
#
# WHY
#   The baseline SwiftOnSecurity config contains a bare
#       <ProcessAccess onmatch="include"></ProcessAccess>
#   tag with ZERO rules. In Sysmon, "include with no rules" means NOTHING is
#   logged -- the section exists but is inert. A naive grep for the tag name
#   says "EID 10 is enabled", which is exactly the wrong conclusion.
#   Phase A proved the blind spot (only EID 1 appeared). Phase B adds one
#   narrowly scoped rule and re-runs the identical action.
#
# We scope the rule to lsass.exe ONLY. Enabling ProcessAccess globally is one
# of the noisiest things you can do to a Sysmon install.
# ASCII ONLY.

$ErrorActionPreference = 'Continue'
$out = 'C:\Tools\DFIR\day1b'
$log = Join-Path $out 'phaseb_log.txt'
$utf8 = New-Object System.Text.UTF8Encoding($false)
[IO.File]::WriteAllText($log, '', $utf8)
function L([string]$m) { [IO.File]::AppendAllText($log, $m + "`r`n", $utf8) }
function Say([string]$m) { Write-Host $m }

$live = 'C:\Tools\DFIR\sysmonconfig.xml'
$base = Join-Path $out 'sysmonconfig.baseline.xml'
$new = Join-Path $out 'sysmonconfig.day1b.xml'

$t0 = Get-Date
L '=== Phase B: enable Sysmon EID 10 for lsass and re-run the probe ==='
L ('local ' + $t0.ToString('yyyy-MM-dd HH:mm:ss K') + ' | utc ' + $t0.ToUniversalTime().ToString('yyyy-MM-dd HH:mm:ss') + 'Z')

# ---- 1. build the patched config -------------------------------------------
L ''
L '--- 1. patch config (exact string insert, no regex escaping traps) ---'
if (-not (Test-Path $base)) { L 'ERROR: sysmonconfig.baseline.xml missing -- run vm_day1b_harden.ps1 first'; Say 'ERROR baseline missing'; return }
Copy-Item $base $new -Force
$raw = [IO.File]::ReadAllText($new)
$needle = '<ProcessAccess onmatch="include">'
$i = $raw.IndexOf($needle)
if ($i -lt 0) { L 'ERROR: ProcessAccess include block not found'; Say 'ERROR block not found'; return }
$insert = $needle +
          "`r`n`t`t`t" +
          '<TargetImage condition="is">C:\Windows\system32\lsass.exe</TargetImage>' +
          ' <!--Day1B: scope EID 10 to lsass only; global ProcessAccess is far too noisy-->' +
          "`r`n`t`t"
$patched = $raw.Substring(0, $i) + $insert + $raw.Substring($i + $needle.Length)
[IO.File]::WriteAllText($new, $patched, $utf8)
L ('  baseline bytes : ' + $raw.Length)
L ('  patched bytes  : ' + $patched.Length + '  (delta ' + ($patched.Length - $raw.Length) + ')')

$pb = [regex]::Match($patched, '(?s)<ProcessAccess onmatch="include">(.*?)</ProcessAccess>')
$ruleCount = ([regex]::Matches($pb.Groups[1].Value, '<TargetImage')).Count
L ('  ProcessAccess include rule count now = ' + $ruleCount + ' (was 0)')

# ---- 2. reload Sysmon -------------------------------------------------------
L ''
L '--- 2. reload sysmon with the patched config ---'
$sw = [Diagnostics.Stopwatch]::StartNew()
$rc = & 'C:\Tools\DFIR\Sysmon64.exe' -c $new 2>&1 | Out-String
$sw.Stop()
L ('  Sysmon64 -c exit=' + $LASTEXITCODE + ' elapsed=' + [math]::Round($sw.Elapsed.TotalSeconds, 1) + 's')
foreach ($line in ($rc -split "`n")) { if ($line.Trim()) { L ('  | ' + $line.Trim()) } }
$svc = Get-Service -Name 'Sysmon*' -ErrorAction SilentlyContinue
foreach ($s in $svc) { L ('  service ' + $s.Name + ' = ' + $s.Status) }
Start-Sleep -Seconds 2

# ---- 3. re-run the identical probe -----------------------------------------
L ''
L '--- 3. re-run the identical lsass handle-open ---'
$ntSig = @'
using System;
using System.Runtime.InteropServices;
public static class SprintNt {
    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern IntPtr OpenProcess(uint dwDesiredAccess, bool bInheritHandle, int dwProcessId);
    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern bool CloseHandle(IntPtr hObject);
}
'@
Add-Type -TypeDefinition $ntSig -ErrorAction SilentlyContinue

$markU = (Get-Date).ToUniversalTime()
$markL = Get-Date
$lsass = Get-Process -Name lsass -ErrorAction SilentlyContinue | Select-Object -First 1
$detail = 'lsass not found'
if ($lsass) {
    $h1 = [SprintNt]::OpenProcess(0x1000, $false, $lsass.Id)
    $ok1 = ($h1 -ne [IntPtr]::Zero); if ($ok1) { [void][SprintNt]::CloseHandle($h1) }
    Start-Sleep -Milliseconds 400
    $h2 = [SprintNt]::OpenProcess(0x1410, $false, $lsass.Id)
    $ok2 = ($h2 -ne [IntPtr]::Zero); if ($ok2) { [void][SprintNt]::CloseHandle($h2) }
    $detail = 'lsass_pid=' + $lsass.Id + ' open_0x1000=' + $ok1 + ' open_0x1410=' + $ok2
}
L ('  probe_utc   : ' + $markU.ToString('yyyy-MM-dd HH:mm:ss.fff') + 'Z')
L ('  probe_local : ' + $markL.ToString('yyyy-MM-dd HH:mm:ss.fff K'))
L ('  result      : ' + $detail)
Start-Sleep -Seconds 4

# ---- 4. pull the EID 10 evidence -------------------------------------------
L ''
L '--- 4. Sysmon EID 10 evidence after the patch ---'
$ev10 = @()
try {
    $ev10 = Get-WinEvent -FilterHashtable @{
        LogName = 'Microsoft-Windows-Sysmon/Operational'; Id = 10; StartTime = $t0.AddMinutes(-5)
    } -ErrorAction Stop
} catch { L ('  query error: ' + $_.Exception.Message) }
L ('  EID 10 events in window: ' + @($ev10).Count)

$lines = @()
$lines += 'Phase B / Sysmon EID 10 (ProcessAccess) evidence'
$lines += 'probe_utc   = ' + $markU.ToString('yyyy-MM-dd HH:mm:ss.fff') + 'Z'
$lines += 'probe_local = ' + $markL.ToString('yyyy-MM-dd HH:mm:ss.fff K')
$lines += 'probe       = ' + $detail
$lines += 'config      = ' + $new + ' (ProcessAccess include rules = ' + $ruleCount + ')'
$lines += 'count       = ' + @($ev10).Count
$lines += ''
foreach ($e in $ev10) {
    $xml = [xml]$e.ToXml()
    $lines += '-----------------------------------------------------------'
    $lines += 'TimeCreated(local) = ' + $e.TimeCreated.ToString('yyyy-MM-dd HH:mm:ss.fff K')
    $lines += 'TimeCreated(utc)   = ' + $e.TimeCreated.ToUniversalTime().ToString('yyyy-MM-dd HH:mm:ss.fff') + 'Z'
    foreach ($d in $xml.Event.EventData.Data) {
        $lines += ('  ' + $d.Name.PadRight(22) + ' = ' + $d.'#text')
    }
}
[IO.File]::WriteAllLines((Join-Path $out 'phaseb_eid10.txt'), $lines, $utf8)
L '  wrote phaseb_eid10.txt'

L ''
L ('elapsed_sec ' + [math]::Round(((Get-Date) - $t0).TotalSeconds, 1))
L 'DONE phase B'
Say 'DONE phase B -> read C:\Tools\DFIR\day1b\phaseb_log.txt and phaseb_eid10.txt'

# vm_day1b_export.ps1 -- Day 1B: collect evidence and run the three parsers.
#
# All three tools are pointed at the SAME directory of exported .evtx files so
# the outputs are directly comparable. Timings and exit codes are logged
# because "the tool worked" is a claim that should be backed by numbers.
# ASCII ONLY.

$ErrorActionPreference = 'Continue'
$out = 'C:\Tools\DFIR\day1b'
$log = Join-Path $out 'export_log.txt'
$utf8 = New-Object System.Text.UTF8Encoding($false)
[IO.File]::WriteAllText($log, '', $utf8)
function L([string]$m) { [IO.File]::AppendAllText($log, $m + "`r`n", $utf8) }
function Say([string]$m) { Write-Host $m }

$evtxDir = Join-Path $out 'evtx'
$toolDir = Join-Path $out 'toolout'
Remove-Item $evtxDir -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item $toolDir -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $evtxDir | Out-Null
New-Item -ItemType Directory -Force -Path $toolDir | Out-Null

$nowL = Get-Date
$nowU = $nowL.ToUniversalTime()
L '=== Day 1B evidence collection ==='
L ('collect_local = ' + $nowL.ToString('yyyy-MM-dd HH:mm:ss K'))
L ('collect_utc   = ' + $nowU.ToString('yyyy-MM-dd HH:mm:ss') + 'Z')

# ---------- 1. export channels ----------------------------------------------
L ''
L '--- 1. wevtutil epl per channel ---'
function ExpEvtx([string]$channel, [string]$file) {
    $dst = Join-Path $evtxDir $file
    & wevtutil.exe epl $channel $dst 2>&1 | Out-Null
    if (Test-Path $dst) {
        $mb = [math]::Round((Get-Item $dst).Length / 1MB, 2)
        L ('  OK    ' + $channel.PadRight(46) + ' -> ' + $file.PadRight(34) + ' ' + $mb + ' MB')
    } else {
        L ('  FAIL  ' + $channel + ' (channel missing or not readable)')
    }
}
ExpEvtx 'Security'                                    'Security.evtx'
ExpEvtx 'System'                                      'System.evtx'
ExpEvtx 'Microsoft-Windows-Sysmon/Operational'        'Sysmon.evtx'
ExpEvtx 'Microsoft-Windows-PowerShell/Operational'    'PowerShell-Operational.evtx'
ExpEvtx 'Microsoft-Windows-Windows Defender/Operational' 'Defender-Operational.evtx'
ExpEvtx 'Microsoft-Windows-TaskScheduler/Operational' 'TaskScheduler-Operational.evtx'

# ---------- 2. event-id census in the simulation window ---------------------
L ''
L '--- 2. EID census for the simulation window (direct Win32 query) ---'
$winStart = $nowL.AddMinutes(-30)
$census = @()
foreach ($ch in @('Security', 'Microsoft-Windows-Sysmon/Operational', 'Microsoft-Windows-PowerShell/Operational', 'Microsoft-Windows-Windows Defender/Operational', 'Microsoft-Windows-TaskScheduler/Operational')) {
    try {
        $ev = Get-WinEvent -FilterHashtable @{ LogName = $ch; StartTime = $winStart } -ErrorAction Stop
    } catch { L ('  ' + $ch.PadRight(46) + ' (no events / unavailable)'); continue }
    L ('  ' + $ch + '  total=' + @($ev).Count)
    foreach ($g in ($ev | Group-Object Id | Sort-Object { [int]$_.Name })) {
        $line = '         EID ' + $g.Name.PadRight(6) + ' x ' + $g.Count
        L $line
        $census += [pscustomobject]@{ Channel = $ch; EID = [int]$g.Name; Count = $g.Count }
    }
}
$census | Export-Csv -Path (Join-Path $out 'eid_census.csv') -NoTypeInformation -Encoding UTF8

# ---------- 3. EvtxECmd ------------------------------------------------------
L ''
L '--- 3. EvtxECmd (Eric Zimmerman) ---'
$sw = [Diagnostics.Stopwatch]::StartNew()
$evtxecmd = & 'C:\Tools\DFIR\EZTools\net9\EvtxeCmd\EvtxECmd.exe' -d $evtxDir --csv $toolDir --csvf day1b_evtxecmd.csv 2>&1 | Out-String
$sw.Stop()
L ('  exit=' + $LASTEXITCODE + ' elapsed=' + [math]::Round($sw.Elapsed.TotalSeconds, 1) + 's')
foreach ($line in ($evtxecmd -split "`n")) { if ($line.Trim()) { L ('  | ' + $line.Trim()) } }
$f = Join-Path $toolDir 'day1b_evtxecmd.csv'
if (Test-Path $f) {
    $rows = (Get-Content $f | Measure-Object -Line).Lines - 1
    L ('  output day1b_evtxecmd.csv rows=' + $rows + ' size=' + [math]::Round((Get-Item $f).Length / 1KB, 1) + ' KB')
} else { L '  output MISSING' }

# ---------- 4. Hayabusa ------------------------------------------------------
L ''
L '--- 4. Hayabusa v4 dfir-timeline ---'
$sw = [Diagnostics.Stopwatch]::StartNew()
$hay = & 'C:\Tools\DFIR\hayabusa\hayabusa-4.1.0-win-x64.exe' dfir-timeline -d $evtxDir -o (Join-Path $toolDir 'day1b_hayabusa.csv') -w -K -N -U -C 2>&1 | Out-String
$sw.Stop()
L ('  exit=' + $LASTEXITCODE + ' elapsed=' + [math]::Round($sw.Elapsed.TotalSeconds, 1) + 's')
foreach ($line in ($hay -split "`n")) { if ($line.Trim()) { L ('  | ' + $line.Trim()) } }
$f = Join-Path $toolDir 'day1b_hayabusa.csv'
if (Test-Path $f) {
    $rows = (Get-Content $f | Measure-Object -Line).Lines - 1
    L ('  output day1b_hayabusa.csv rows=' + $rows + ' size=' + [math]::Round((Get-Item $f).Length / 1KB, 1) + ' KB')
} else { L '  output MISSING' }

# ---------- 5. Chainsaw ------------------------------------------------------
L ''
L '--- 5. Chainsaw v2.16.5 hunt with Sigma ---'
$sw = [Diagnostics.Stopwatch]::StartNew()
$cs = & 'C:\Tools\DFIR\chainsaw\chainsaw.exe' hunt -s 'C:\Tools\DFIR\sigma-rules' -m 'C:\Tools\DFIR\chainsaw\mappings\sigma-event-logs-all.yml' -o (Join-Path $toolDir 'day1b_chainsaw.json') --json $evtxDir 2>&1 | Out-String
$sw.Stop()
L ('  exit=' + $LASTEXITCODE + ' elapsed=' + [math]::Round($sw.Elapsed.TotalSeconds, 1) + 's')
foreach ($line in ($cs -split "`n")) { if ($line.Trim()) { L ('  | ' + $line.Trim()) } }
$f = Join-Path $toolDir 'day1b_chainsaw.json'
if (Test-Path $f) {
    $txt = Get-Content $f -Raw
    $hits = ([regex]::Matches($txt, '"tag"')).Count
    L ('  output day1b_chainsaw.json size=' + [math]::Round((Get-Item $f).Length / 1KB, 1) + ' KB  tag_markers=' + $hits)
} else { L '  output MISSING' }

# ---------- 6. inventory ------------------------------------------------------
L ''
L '--- 6. produced files ---'
L '  [evtx]'
Get-ChildItem $evtxDir | Sort-Object Name | ForEach-Object { L ('    ' + $_.Name.PadRight(38) + ' ' + [math]::Round($_.Length / 1KB, 1) + ' KB') }
L '  [toolout]'
Get-ChildItem $toolDir | Sort-Object Name | ForEach-Object { L ('    ' + $_.Name.PadRight(38) + ' ' + [math]::Round($_.Length / 1KB, 1) + ' KB') }
L '  [keys]'
Get-ChildItem $out -File | Sort-Object Name | ForEach-Object { L ('    ' + $_.Name.PadRight(38) + ' ' + [math]::Round($_.Length / 1KB, 1) + ' KB') }

L ''
L 'DONE export'
Say 'DONE export -> read C:\Tools\DFIR\day1b\export_log.txt'

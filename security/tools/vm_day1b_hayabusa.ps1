# vm_day1b_hayabusa.ps1 -- Day 1B: repair Hayabusa and run its timeline pass.
#
# WHY THIS FILE EXISTS
#   The Hayabusa install on this VM contains only three files:
#     hayabusa-4.1.0-win-x64.exe, encoded_rules.yml, rules_config_files.txt
#   The release also ships a rules/ tree, and Hayabusa needs
#     rules/config/*.txt  (generic_abbreviations.txt, eventkey_alias.txt, ...)
#   at runtime relative to its WORKING DIRECTORY. Without them dfir-timeline
#   exits 1 with "Cannot open file. [file:rules/config/generic_abbreviations.txt]".
#   `update-rules` fetches the full rules tree, config included.
#
# Two details that matter:
#   - the process WorkingDirectory is set to the Hayabusa folder, because both
#     -r (rules) and -c (rules config) default to ./rules which is resolved
#     against the CWD, not against the exe path.
#   - stdin is closed for every child (see Run): update-rules and the scan both
#     have interactive paths, and a blocked read on stdin is exactly what hung
#     the first simulation attempt.
# ASCII ONLY.

$ErrorActionPreference = 'Continue'
$out = 'C:\Tools\DFIR\day1b'
$HBDIR = 'C:\Tools\DFIR\hayabusa'
$HB = Join-Path $HBDIR 'hayabusa-4.1.0-win-x64.exe'
$log = Join-Path $out 'hayabusa_log.txt'
$utf8 = New-Object System.Text.UTF8Encoding($false)
[IO.File]::WriteAllText($log, '', $utf8)
function L([string]$m) { [IO.File]::AppendAllText($log, $m + "`r`n", $utf8) }
function Say([string]$m) { Write-Host $m }

function Run([string]$ArgLine, [int]$TimeoutSec) {
    # NOTE: the parameter must NOT be called $Args -- that name is PowerShell's
    # automatic argument array, and the assignment below silently picked that up
    # instead, so the child received an empty command line and printed its usage.
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $HB
    $psi.Arguments = $ArgLine
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.RedirectStandardInput = $true
    $psi.WorkingDirectory = $HBDIR
    $p = [Diagnostics.Process]::Start($psi)
    $p.StandardInput.Close()
    $ot = $p.StandardOutput.ReadToEndAsync()
    $et = $p.StandardError.ReadToEndAsync()
    if (-not $p.WaitForExit($TimeoutSec * 1000)) { try { $p.Kill() } catch { } ; return @{ exit = -1; text = '<TIMEOUT>' } }
    return @{ exit = $p.ExitCode; text = ($ot.Result + "`n" + $et.Result) }
}

L '=== Day 1B Hayabusa repair + run ==='
L ('local ' + (Get-Date).ToString('yyyy-MM-dd HH:mm:ss K'))

# ---- 1. what is actually installed -----------------------------------------
L ''
L '--- 1. current install state ---'
foreach ($f in (Get-ChildItem $HBDIR -Force | Select-Object -First 30)) {
    L ('  ' + $f.Name.PadRight(34) + $(if ($f.PSIsContainer) { '<DIR>' } else { [math]::Round($f.Length / 1KB, 1).ToString() + ' KB' }))
}
L ('  rules\config exists : ' + (Test-Path (Join-Path $HBDIR 'rules\config')))

# ---- 2. update-rules -------------------------------------------------------
L ''
L '--- 2. update-rules (downloads the rules tree incl. config) ---'
$sw = [Diagnostics.Stopwatch]::StartNew()
$r = Run 'update-rules' 300
$sw.Stop()
L ('  exit=' + $r.exit + ' elapsed=' + [math]::Round($sw.Elapsed.TotalSeconds, 1) + 's')
foreach ($line in ($r.text -split "`n")) { if ($line.Trim()) { L ('  | ' + $line.Trim()) } }
L ('  rules\config exists now : ' + (Test-Path (Join-Path $HBDIR 'rules\config')))
if (Test-Path (Join-Path $HBDIR 'rules\config')) {
    $cfg = Get-ChildItem (Join-Path $HBDIR 'rules\config') -File
    L ('  rules\config files      : ' + $cfg.Count)
    foreach ($c in ($cfg | Select-Object -First 20)) { L ('    ' + $c.Name) }
}

# ---- 3. dfir-timeline ------------------------------------------------------
L ''
L '--- 3. dfir-timeline over the exported evtx set ---'
$evtx = Join-Path $out 'evtx'
$csv = Join-Path $out 'toolout\day1b_hayabusa.csv'
Remove-Item $csv -Force -ErrorAction SilentlyContinue
$sw = [Diagnostics.Stopwatch]::StartNew()
$r = Run ('dfir-timeline -d ' + $evtx + ' -o ' + $csv + ' -w -K -N -U -C') 480
$sw.Stop()
L ('  exit=' + $r.exit + ' elapsed=' + [math]::Round($sw.Elapsed.TotalSeconds, 1) + 's')
foreach ($line in ($r.text -split "`n")) { if ($line.Trim()) { L ('  | ' + $line.Trim()) } }
if (Test-Path $csv) {
    $rows = (Get-Content $csv | Measure-Object -Line).Lines - 1
    L ('  output day1b_hayabusa.csv rows=' + $rows + ' size=' + [math]::Round((Get-Item $csv).Length / 1KB, 1) + ' KB')
} else { L '  output MISSING' }

L ''
L 'DONE hayabusa'
Say 'DONE hayabusa -> C:\Tools\DFIR\day1b\hayabusa_log.txt'

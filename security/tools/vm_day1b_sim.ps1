# vm_day1b_sim.ps1 -- Day 1B Phase A: controlled intrusion simulation.
#
# Every action is BENIGN and REVERSIBLE. It exists only to make specific
# telemetry artifacts appear:
#   - calc.exe is REFERENCED in command lines but never executed
#   - no existing file is deleted or modified
#   - Defender is deliberately left ON; where Defender interferes, that
#     interference is part of the known answer
# Artifacts are removed by vm_day1b_cleanup.ps1 (and by this script's
# prologue, so the simulation is idempotent / re-runnable).
#
# Output: ground_truth.csv -- one row per step: UTC + local start/end
# timestamps and the events we EXPECT. That file is the answer key.
#
# WHY EVERY NATIVE CALL GOES THROUGH RunNative
#   The first attempt hung for five minutes on `net user ... /add`: the guest
#   command never returned because a child process blocked reading stdin, and
#   the cmd wrapper could not recover. RunNative fixes the whole class of
#   problem: stdin is explicitly CLOSED (a prompt gets immediate EOF) and
#   WaitForExit has a hard timeout so nothing can stall the run forever.
#   It also captures stdout+stderr without deadlocking on full pipes.
#
# ASCII ONLY (PS 5.1 parses a BOM-less .ps1 using the ANSI codepage).

$ErrorActionPreference = 'Continue'
$out = 'C:\Tools\DFIR\day1b'
New-Item -ItemType Directory -Force -Path $out | Out-Null
$gt = Join-Path $out 'ground_truth.csv'
$slog = Join-Path $out 'sim_log.txt'
$utf8 = New-Object System.Text.UTF8Encoding($false)
[IO.File]::WriteAllText($gt, '', $utf8)
[IO.File]::WriteAllText($slog, '', $utf8)

function L([string]$m) { [IO.File]::AppendAllText($slog, $m + "`r`n", $utf8) }
function AppCsv([string]$line) { [IO.File]::AppendAllText($gt, $line + "`r`n", $utf8) }
function Q([string]$s) { '"' + ($s -replace '"', '""') + '"' }
function Show-Message([string]$m) { Write-Host $m }

# ---------------------------------------------------------------------------
# native runner: stdin closed + hard timeout + no pipe deadlock
# ---------------------------------------------------------------------------
function RunNative {
    param([string]$Exe, [string[]]$Argv, [int]$TimeoutSec = 30)
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $Exe
    $psi.Arguments = (($Argv | ForEach-Object {
                if ($_ -match '[\s"]') { '"' + ($_ -replace '"', '\"') + '"' } else { $_ }
            }) -join ' ')
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.RedirectStandardInput = $true
    $psi.WorkingDirectory = 'C:\Windows\System32'
    try { $p = [Diagnostics.Process]::Start($psi) } catch { return ('<START-FAILED: ' + $_.Exception.Message + '>') }
    $p.StandardInput.Close()                       # EOF: a prompt can never block us
    $ot = $p.StandardOutput.ReadToEndAsync()
    $et = $p.StandardError.ReadToEndAsync()
    if (-not $p.WaitForExit($TimeoutSec * 1000)) {
        try { $p.Kill() } catch { Write-Verbose ("process already exited: " + $_.Exception.Message) }
        return ('<TIMEOUT after ' + $TimeoutSec + 's, process killed> ' + $ot.Result + $et.Result)
    }
    $o = ($ot.Result + ' ' + $et.Result)
    return ((($o -replace '\s+', ' ').Trim()) + ' [exit=' + $p.ExitCode + ']')
}

# ---------------------------------------------------------------------------
# prologue: reset artifacts from any previous attempt (idempotency)
# ---------------------------------------------------------------------------
L '=== Day 1B Phase A: controlled intrusion simulation ==='
L ''
L '--- prologue: reset leftovers so this run starts from a clean baseline ---'
foreach ($r in @(
        @('schtasks.exe', @('/delete', '/tn', 'SprintDay1B', '/f'), 20),
        @('sc.exe', @('delete', 'SprintDay1BSvc'), 20),
        @('reg.exe', @('delete', 'HKCU\Software\Microsoft\Windows\CurrentVersion\Run', '/v', 'SprintDay1B', '/f'), 20),
        @('net.exe', @('user', 'sprint_svc', '/delete'), 20)
    )) {
    $res = RunNative $r[0] $r[1] $r[2]
    L ('  ' + $r[0].PadRight(14) + ' ' + ($r[1] -join ' ').PadRight(52) + ' -> ' + $res)
}
foreach ($cls in @('__FilterToConsumerBinding', 'CommandLineEventConsumer', '__EventFilter')) {
    try {
        Get-CimInstance -Namespace root\subscription -ClassName $cls -ErrorAction SilentlyContinue |
            Where-Object { $_.Name -eq 'SprintDay1BFilter' -or $_.Name -eq 'SprintDay1BConsumer' -or ($_.Filter -and $_.Filter.Name -match 'SprintDay1B') } |
            Remove-CimInstance
        L ('  WMI ' + $cls.PadRight(26) + ' reset')
    } catch { L ('  WMI ' + $cls + ' reset error: ' + $_.Exception.Message) }
}
Remove-Item 'C:\Windows\Temp\sprint_*' -Force -ErrorAction SilentlyContinue
Remove-Item 'C:\Windows\Temp\sprint_eicar.exe' -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
L '  reset complete'
L ''

$t0u = (Get-Date).ToUniversalTime()
$t0l = Get-Date
L '=== simulation window opens ==='
L ('sim_start_local : ' + $t0l.ToString('yyyy-MM-dd HH:mm:ss.fff K'))
L ('sim_start_utc   : ' + $t0u.ToString('yyyy-MM-dd HH:mm:ss.fff') + 'Z')
Show-Message ('SIM START  local=' + $t0l.ToString('HH:mm:ss') + '  utc=' + $t0u.ToString('HH:mm:ss') + 'Z')

AppCsv 'seq,step,technique,name,start_utc,start_local,end_utc,end_local,expect_sysmon,expect_security,expect_other,observed_output'

$script:seq = 0
function Step {
    param(
        [string]$Id, [string]$Tech, [string]$Name, [string]$Desc,
        [scriptblock]$Body, [string]$ExpS, [string]$ExpSec, [string]$ExpO
    )
    $script:seq++
    $su = (Get-Date).ToUniversalTime(); $sl = Get-Date
    L ''
    L ('--- [' + $Id + '] (' + $Tech + ') ' + $Name)
    L ('    command : ' + $Desc)
    Show-Message ('STEP ' + $Id.PadRight(4) + ' (' + $Tech + ') ' + $Name)
    $note = ''
    try { $note = (& $Body 2>&1 | Out-String) } catch { $note = 'THREW: ' + $_.Exception.Message }
    Start-Sleep -Milliseconds 800
    $eu = (Get-Date).ToUniversalTime(); $el = Get-Date
    $note = (($note -replace '\s+', ' ').Trim())
    if ($note.Length -gt 400) { $note = $note.Substring(0, 400) }
    L ('    expected: SYSMON[' + $ExpS + '] SECURITY[' + $ExpSec + '] OTHER[' + $ExpO + ']')
    L ('    observed: ' + $note)
    AppCsv ((@($script:seq, $Id, $Tech, $Name,
                 $su.ToString('yyyy-MM-dd HH:mm:ss.fff'), $sl.ToString('yyyy-MM-dd HH:mm:ss.fff'),
                 $eu.ToString('yyyy-MM-dd HH:mm:ss.fff'), $el.ToString('yyyy-MM-dd HH:mm:ss.fff'),
                 $ExpS, $ExpSec, $ExpO, $note) | ForEach-Object { Q ([string]$_) }) -join ',')
}

# ---- LSASS probe helper (P/Invoke only; NO dump is ever written) ------------
$ntSig = @'
using System;
using System.Runtime.InteropServices;
public static class SprintNt {
    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern IntPtr OpenProcess(uint dwDesiredAccess, bool bInheritHandle, int dwProcessId);
    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern bool CloseHandle(IntPtr hObject);
    [DllImport("advapi32.dll", SetLastError = true, CharSet = CharSet.Unicode)]
    public static extern bool LogonUser(string user, string domain, string password,
        int logonType, int logonProvider, out IntPtr token);
}
'@
Add-Type -TypeDefinition $ntSig -ErrorAction SilentlyContinue

# ===========================================================================
# S01  T1053.005  scheduled task creation
# ===========================================================================
Step 'S01' 'T1053.005' 'Scheduled task creation through schtasks.exe' `
    'schtasks /create /tn SprintDay1B /tr "cmd.exe /c calc.exe" /sc once /st 23:59 /f' `
    { RunNative 'schtasks.exe' @('/create', '/tn', 'SprintDay1B', '/tr', 'cmd.exe /c calc.exe', '/sc', 'once', '/st', '23:59', '/f') 30 } `
    '1(schtasks.exe);11(C:\Windows\System32\Tasks\SprintDay1B matches the T1053 path rule)' '4698' 'TaskScheduler/106'

# ===========================================================================
# S02  T1543.002  Windows service creation
# ===========================================================================
Step 'S02' 'T1543.002' 'Service creation through sc.exe' `
    'sc create SprintDay1BSvc binPath= "C:\Windows\System32\cmd.exe /c calc.exe" start= demand' `
    { RunNative 'sc.exe' @('create', 'SprintDay1BSvc', 'binPath=', 'C:\Windows\System32\cmd.exe /c calc.exe', 'start=', 'demand') 30 } `
    '1(sc.exe);13(TargetObject ends with \ImagePath)' '7045 lives in System.evtx (SCM writes it regardless of audit policy);4697 needs Security System Extension auditing which is OFF' 'System/7040'

# ===========================================================================
# S03  T1547.001  Registry Run key persistence
# ===========================================================================
Step 'S03' 'T1547.001' 'HKCU Run key persistence via reg.exe' `
    'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v SprintDay1B /t REG_SZ /d "C:\Windows\Temp\sprint_loader.exe" /f' `
    { RunNative 'reg.exe' @('add', 'HKCU\Software\Microsoft\Windows\CurrentVersion\Run', '/v', 'SprintDay1B', '/t', 'REG_SZ', '/d', 'C:\Windows\Temp\sprint_loader.exe', '/f') 30 } `
    '1(reg.exe);13(TargetObject contains CurrentVersion\Run)' '4657 (needs Registry object-access auditing, which is OFF)' '-'

# ===========================================================================
# S04  T1136.001  local account creation
# ===========================================================================
Step 'S04' 'T1136.001' 'Create a local account with net.exe' `
    'net user sprint_svc Spr1nt.Day1B /add   (password kept under 14 chars on purpose)' `
    { RunNative 'net.exe' @('user', 'sprint_svc', 'Spr1nt.Day1B', '/add') 30 } `
    '1(net.exe spawning net1.exe)' '4720' '-'

# ===========================================================================
# S05  T1098  add the new account to local Administrators
# ===========================================================================
Step 'S05' 'T1098' 'Add the new account to the local Administrators group' `
    'net localgroup Administrators sprint_svc /add' `
    { RunNative 'net.exe' @('localgroup', 'Administrators', 'sprint_svc', '/add') 30 } `
    '1(net.exe spawning net1.exe)' '4732' '-'

# ===========================================================================
# S06  T1110  failed network logons (brute-force signal)
# ===========================================================================
Step 'S06' 'T1110' 'Four failed network logons straight through LSA (LogonUser)' `
    'LogonUser(user,.,pwd, LOGON32_LOGON_NETWORK=3, DEFAULT) x4: 2 unknown accounts, 2 wrong passwords' `
    {
        # net use to \\127.0.0.1 blocked for 20s each time (SMB redirector), so we call
        # LogonUser directly: instant, and it yields LogonType 3 exactly like an SMB
        # brute-force attempt, with a distinct SubStatus per failure mode.
        $o = @()
        $targets = @(
            @('sprint_bad', 'Ghost#1'),
            @('sprint_bad', 'Ghost#2'),
            @('sprint_svc', 'WrongPass1'),
            @('sprint_svc', 'WrongPass2')
        )
        foreach ($t in $targets) {
            $tok = [IntPtr]::Zero
            $ok = [SprintNt]::LogonUser($t[0], '.', $t[1], 3, 0, [ref]$tok)
            if ($ok -and ($tok -ne [IntPtr]::Zero)) { [void][SprintNt]::CloseHandle($tok) }
            $winerr = [Runtime.InteropServices.Marshal]::GetLastWin32Error()
            $o += ($t[0] + ' ok=' + $ok + ' Win32Err=' + $winerr)
        }
        $o -join ' | '
    } `
    '1(powershell.exe only; LogonUser is in-process)' '4625 x4 LogonType 3;substatus 0xC0000064 unknown-account vs 0xC000006A bad-password;4776 x4 (Credential Validation now ON)' '-'

# ===========================================================================
# S07  T1059.001 / T1027  encoded PowerShell
# ===========================================================================
Step 'S07' 'T1059.001' 'Base64 encoded PowerShell command line' `
    'powershell.exe -NoProfile -EncodedCommand <b64 of a benign marker>' `
    {
        $inner = 'Write-Output "SPRINT_DAY1B_ENCODED_MARKER"; $env:COMPUTERNAME'
        $b64 = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($inner))
        'b64len=' + $b64.Length + ' :: ' + (RunNative 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe' @('-NoProfile', '-EncodedCommand', $b64) 30)
    } `
    '1(powershell.exe; CommandLine carries -EncodedCommand)' '-' 'PowerShell/4104 recovers the plaintext via ScriptBlockLogging'

# ===========================================================================
# S08  T1140  decode a dropped script with certutil
# ===========================================================================
Step 'S08' 'T1140' 'certutil -decode drops a .ps1 from a base64 blob' `
    'certutil -decode C:\Windows\Temp\sprint_blob.txt C:\Windows\Temp\sprint_decoded.ps1' `
    {
        $payload = "# SprintDay1B decoded payload (benign marker only)`nWrite-Output 'SPRINT_DAY1B_DECODED'"
        $b64 = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes($payload))
        $lines = @()
        for ($i = 0; $i -lt $b64.Length; $i += 64) { $lines += $b64.Substring($i, [Math]::Min(64, $b64.Length - $i)) }
        Set-Content -Path 'C:\Windows\Temp\sprint_blob.txt' -Value $lines -Encoding ASCII
        RunNative 'certutil.exe' @('-decode', 'C:\Windows\Temp\sprint_blob.txt', 'C:\Windows\Temp\sprint_decoded.ps1') 30
    } `
    '1(certutil.exe);11(.ps1 FileCreate)' '4688 (Detailed Tracking now ON)' '-'

# ===========================================================================
# S09  T1564.004  NTFS alternate data stream
# ===========================================================================
Step 'S09' 'T1564.004' 'Hide data in an NTFS alternate data stream' `
    'Set-Content C:\Windows\Temp\sprint_ads.ps1 -Stream Zone.Identifier -Value <marker>' `
    {
        Set-Content -Path 'C:\Windows\Temp\sprint_ads.ps1' -Stream 'Zone.Identifier' -Value 'sprint-ads-payload' -Encoding ASCII
        'streams=' + ((Get-Item 'C:\Windows\Temp\sprint_ads.ps1' -Stream * | Select-Object -ExpandProperty Stream) -join ' / ')
    } `
    '15(FileCreateStreamHash; target ends with .ps1)' '- (Security.evtx cannot see streams at all)' '-'

# ===========================================================================
# S10  T1105 / T1218  LOLBin staged in a temp path and used for egress
# ===========================================================================
Step 'S10' 'T1105' 'curl.exe staged in C:\Windows\Temp and used for egress' `
    'copy curl.exe -> C:\Windows\Temp\sprint_net.exe; sprint_net.exe -s -o NUL -m 10 https://example.com' `
    {
        Copy-Item 'C:\Windows\System32\curl.exe' 'C:\Windows\Temp\sprint_net.exe' -Force
        RunNative 'C:\Windows\Temp\sprint_net.exe' @('-s', '-o', 'NUL', '-m', '10', 'https://example.com') 25
    } `
    '1(Image under C:\Windows\Temp);3(NetworkConnect; Image begins with C:\Windows\Temp);22(DnsQuery example.com)' '- (5156 Filtering Platform auditing OFF)' '-'

# ===========================================================================
# S11  T1082 / T1016 / T1069  discovery burst
# ===========================================================================
Step 'S11' 'T1082' 'Discovery burst: host, account and network enumeration' `
    'whoami /all ; net user ; net localgroup Administrators ; ipconfig /all ; tasklist' `
    {
        $o = @()
        $o += 'whoami:' + (RunNative 'whoami.exe' @('/all') 20)
        $o += 'netuser:' + (RunNative 'net.exe' @('user') 20)
        $o += 'netlg:' + (RunNative 'net.exe' @('localgroup', 'Administrators') 20)
        $o += 'ipconfig:' + (RunNative 'ipconfig.exe' @('/all') 20)
        $o += 'tasklist:' + (RunNative 'tasklist.exe' @() 20)
        ($o -join ' | ')
    } `
    '1 x5+ (whoami; net.exe->net1.exe; net.exe->net1.exe; ipconfig; tasklist)' '4688 x5 with CommandLine' '-'

# ===========================================================================
# S12  T1204.002  AV trigger with the EICAR test file
# ===========================================================================
Step 'S12' 'T1204.002' 'EICAR test file written to disk (Defender left ON)' `
    'Set-Content C:\Windows\Temp\sprint_eicar.exe <EICAR assembled from two fragments>' `
    {
        # Assembled from two fragments at runtime so this script file is never
        # itself a complete signature (that would quarantine the simulator).
        $e1 = 'X5O!P%@AP[4\PZX54(P^)7CC)7}$'
        $e2 = 'EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'
        Set-Content -Path 'C:\Windows\Temp\sprint_eicar.exe' -Value ($e1 + $e2) -Encoding ASCII -NoNewline
        Start-Sleep -Seconds 6
        'file_still_present=' + (Test-Path 'C:\Windows\Temp\sprint_eicar.exe')
    } `
    '11(.exe FileCreate; may be missed if Defender blocks the write first)' '-' 'Defender/1116 + 1117 (separate channel)'

# ===========================================================================
# S13  T1003.001  LSASS handle open -- Phase A: expected to be INVISIBLE
# ===========================================================================
Step 'S13' 'T1003.001' 'Open a handle to lsass.exe (P/Invoke only; no dump written)' `
    'OpenProcess(0x1000) then OpenProcess(0x1410) against the lsass pid' `
    {
        $lsass = Get-Process -Name lsass -ErrorAction SilentlyContinue | Select-Object -First 1
        if (-not $lsass) { 'lsass not found' }
        else {
            $h1 = [SprintNt]::OpenProcess(0x1000, $false, $lsass.Id)
            $ok1 = ($h1 -ne [IntPtr]::Zero); if ($ok1) { [void][SprintNt]::CloseHandle($h1) }
            Start-Sleep -Milliseconds 400
            $h2 = [SprintNt]::OpenProcess(0x1410, $false, $lsass.Id)
            $ok2 = ($h2 -ne [IntPtr]::Zero); if ($ok2) { [void][SprintNt]::CloseHandle($h2) }
            'lsass_pid=' + $lsass.Id + ' open_QUERY_LIMITED_0x1000=' + $ok1 + ' open_QUERYINFO_VMREAD_0x1410=' + $ok2
        }
    } `
    '1(powershell.exe) ONLY -- EID 10 is INERT in the baseline config' '-' 'NONE. This is the blind spot Phase B turns back on.'

# ===========================================================================
# S14  T1546.003  WMI permanent event subscription
# ===========================================================================
Step 'S14' 'T1546.003' 'WMI permanent event subscription (filter + consumer + binding)' `
    'Set-WmiInstance __EventFilter / CommandLineEventConsumer / __FilterToConsumerBinding' `
    {
        $f = New-CimInstance -Namespace root\subscription -ClassName __EventFilter -Property @{
            Name = 'SprintDay1BFilter'; EventNamespace = 'root\cimv2'; QueryLanguage = 'WQL'
            Query = "SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_PerfFormattedData_PerfOS_System'"
        }
        $c = New-CimInstance -Namespace root\subscription -ClassName CommandLineEventConsumer -Property @{
            Name = 'SprintDay1BConsumer'; CommandLineTemplate = 'cmd.exe /c calc.exe'
        }
        $b = New-CimInstance -Namespace root\subscription -ClassName __FilterToConsumerBinding -Property @{ Filter = [ref]$f; Consumer = [ref]$c }
        'filter=' + $f.Name + ' consumer=' + $c.Name + ' binding=' + $b.CimClass.CimClassName
    } `
    '19(WmiEventFilter);20(WmiEventConsumer);21(WmiEventConsumerToFilter)' '-' '-'

# ===========================================================================
$t1u = (Get-Date).ToUniversalTime()
$t1l = Get-Date
L ''
L '=== simulation window closes ==='
L ('sim_end_local : ' + $t1l.ToString('yyyy-MM-dd HH:mm:ss.fff K'))
L ('sim_end_utc   : ' + $t1u.ToString('yyyy-MM-dd HH:mm:ss.fff') + 'Z')
L ('elapsed_sec   : ' + [math]::Round(($t1l - $t0l).TotalSeconds, 1))
L ('steps_recorded: ' + $script:seq)

$win = @(
    'Day 1B Phase A simulation window'
    'start_local = ' + $t0l.ToString('yyyy-MM-dd HH:mm:ss.fff K')
    'start_utc   = ' + $t0u.ToString('yyyy-MM-dd HH:mm:ss.fff') + 'Z'
    'end_local   = ' + $t1l.ToString('yyyy-MM-dd HH:mm:ss.fff K')
    'end_utc     = ' + $t1u.ToString('yyyy-MM-dd HH:mm:ss.fff') + 'Z'
    'steps       = ' + $script:seq
    'local tz    = ' + [TimeZoneInfo]::Local.Id
    'NOTE        = the prologue reset before start_utc also generates events; treat anything before start_utc as setup noise'
)
[IO.File]::WriteAllLines((Join-Path $out 'window.txt'), $win, $utf8)

Show-Message ''
Show-Message ('SIM END  steps=' + $script:seq + '  elapsed=' + [math]::Round(($t1l - $t0l).TotalSeconds, 1) + 's')
Show-Message 'DONE sim -> C:\Tools\DFIR\day1b\ground_truth.csv'

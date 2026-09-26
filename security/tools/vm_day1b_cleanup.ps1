# vm_day1b_cleanup.ps1 -- Day 1B: remove everything the simulation created.
#
# Two tiers on purpose:
#   default   : remove only the ARTIFACTS (task, service, account, Run key,
#               WMI subscription, staged files). The visibility improvements
#               (audit subcategories, 4688 cmdline, 4104, ProcessAccess rule)
#               are LEFT IN PLACE because they are useful for the rest of the
#               sprint -- but they are all documented and revertible.
#   -Full     : also revert the visibility changes (audit policy restore from
#               the Phase 0 snapshot, 4688 cmdline value removed, Sysmon
#               reloaded from the baseline config).
#
# ASCII ONLY.
param([switch]$Full)

$ErrorActionPreference = 'Continue'
$out = 'C:\Tools\DFIR\day1b'
$log = Join-Path $out 'cleanup_log.txt'
$utf8 = New-Object System.Text.UTF8Encoding($false)
[IO.File]::WriteAllText($log, '', $utf8)
function L([string]$m) { [IO.File]::AppendAllText($log, $m + "`r`n", $utf8) }
function Say([string]$m) { Write-Host $m }

L '=== Day 1B cleanup ==='
L ('local ' + (Get-Date).ToString('yyyy-MM-dd HH:mm:ss K') + ' | Full=' + $Full)
L ''

function Try1([string]$label, [scriptblock]$body) {
    try {
        $o = (& $body 2>&1 | Out-String).Trim()
        if ($o.Length -gt 200) { $o = $o.Substring(0, 200) }
        L ('  [ok]   ' + $label.PadRight(46) + ' ' + $o)
    } catch {
        L ('  [FAIL] ' + $label.PadRight(46) + ' ' + $_.Exception.Message)
    }
}

# ---- 1. artifacts -----------------------------------------------------------
L '--- 1. remove simulation artifacts ---'
Try1 'scheduled task SprintDay1B'      { schtasks.exe /delete /tn 'SprintDay1B' /f }
Try1 'service SprintDay1BSvc'          { sc.exe delete 'SprintDay1BSvc' }
Try1 'HKCU Run value SprintDay1B'      { reg.exe delete 'HKCU\Software\Microsoft\Windows\CurrentVersion\Run' /v 'SprintDay1B' /f }
Try1 'local account sprint_svc'        { net.exe user 'sprint_svc' /delete }
Try1 'WMI binding' {
    Get-WmiObject -Namespace root\subscription -Class __FilterToConsumerBinding -ErrorAction SilentlyContinue |
        Where-Object { ('{0}' -f $_.Filter) -match 'SprintDay1B' } |
        ForEach-Object { $_.Delete() }
}
Try1 'WMI consumer SprintDay1BConsumer' {
    Get-WmiObject -Namespace root\subscription -Class CommandLineEventConsumer -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -eq 'SprintDay1BConsumer' } |
        ForEach-Object { $_.Delete() }
}
Try1 'WMI filter SprintDay1BFilter' {
    Get-WmiObject -Namespace root\subscription -Class __EventFilter -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -eq 'SprintDay1BFilter' } |
        ForEach-Object { $_.Delete() }
}
Try1 'staged files in C:\Windows\Temp' { Remove-Item 'C:\Windows\Temp\sprint_*' -Force -ErrorAction SilentlyContinue; 'removed' }

# ---- 2. verification --------------------------------------------------------
L ''
L '--- 2. verification (all lines should say GONE) ---'
$chk = @(
    @{ n = 'task SprintDay1B'; f = { (schtasks.exe /query /tn 'SprintDay1B' 2>&1 | Out-String) -notmatch 'SprintDay1B' } },
    @{ n = 'service SprintDay1BSvc'; f = { -not (Get-Service -Name 'SprintDay1BSvc' -ErrorAction SilentlyContinue) } },
    @{ n = 'Run value SprintDay1B'; f = { -not (Get-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run' -Name 'SprintDay1B' -ErrorAction SilentlyContinue) } },
    @{ n = 'account sprint_svc'; f = { -not (Get-LocalUser -Name 'sprint_svc' -ErrorAction SilentlyContinue) } },
    @{ n = 'WMI filter/consumer'; f = { -not (Get-WmiObject -Namespace root\subscription -Class __EventFilter -ErrorAction SilentlyContinue | Where-Object { $_.Name -eq 'SprintDay1BFilter' }) } },
    @{ n = 'temp files'; f = { @(Get-ChildItem 'C:\Windows\Temp\sprint_*' -ErrorAction SilentlyContinue).Count -eq 0 } }
)
foreach ($c in $chk) {
    $gone = $false
    try { $gone = [bool](& $c.f) } catch { $gone = $false }
    L ('  ' + $c.n.PadRight(30) + ' : ' + $(if ($gone) { 'GONE' } else { 'STILL PRESENT <<<' }))
}
L ''
L '--- 2b. what is intentionally LEFT Enabled (revert with -Full) ---'
L '  audit: Process Creation / Other Object Access Events / Credential Validation'
L '  reg  : ProcessCreationIncludeCmdLine_Enabled = 1'
L '  reg  : PowerShell ScriptBlockLogging = 1'
L '  chan : Microsoft-Windows-TaskScheduler/Operational enabled'
L '  chan : Security/System/Sysmon/PS log sizes raised'
L '  sysmon: config = ' + $(if ($Full) { 'baseline' } else { 'day1b (ProcessAccess include for lsass added)' })

# ---- 3. optional full revert -----------------------------------------------
if ($Full) {
    L ''
    L '--- 3. -Full: reverting visibility changes ---'
    Try1 'auditpol /restore from Phase 0 snapshot' { auditpol.exe /restore /file:$out\auditpol_backup.csv }
    Try1 'remove 4688 cmdline value' { Remove-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\Audit' -Name 'ProcessCreationIncludeCmdLine_Enabled' -ErrorAction SilentlyContinue; 'removed' }
    Try1 'reload Sysmon from baseline config' { & 'C:\Tools\DFIR\Sysmon64.exe' -c (Join-Path $out 'sysmonconfig.baseline.xml') }
    Try1 'confirm ProcessAccess rule count = 0' {
        $b = [IO.File]::ReadAllText('C:\Tools\DFIR\sysmonconfig.xml')
        $m = [regex]::Match($b, '(?s)<ProcessAccess onmatch="include">(.*?)</ProcessAccess>')
        'rules=' + ([regex]::Matches($m.Groups[1].Value, '<TargetImage')).Count
    }
    Copy-Item (Join-Path $out 'sysmonconfig.baseline.xml') 'C:\Tools\DFIR\sysmonconfig.xml' -Force
}

L ''
L 'DONE cleanup'
Say 'DONE cleanup'

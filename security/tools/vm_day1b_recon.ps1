# vm_day1b_recon.ps1 -- Day 1B 前置偵察：確認遙測產生器的能力邊界
# 目的：在設計「已知答案」的攻擊模擬之前，先確認哪些事件通道真的會產生事件。
# 注意：輸出必須為純 ASCII（客體 console codepage CP950 會破壞中文）。

$ErrorActionPreference = 'Continue'
$out = 'C:\Tools\DFIR\day1b'
New-Item -ItemType Directory -Force -Path $out | Out-Null

function Show-Message([string]$m) { Write-Host $m }

Show-Message '=== 1. 目前身分與權杖 ==='
Show-Message ("whoami      : " + (whoami))
$id = [Security.Principal.WindowsIdentity]::GetCurrent()
$pr = New-Object Security.Principal.WindowsPrincipal($id)
Show-Message ("IsAdmin     : " + $pr.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator))
Show-Message ("IntegrityLvl: " + $id.Name)

Show-Message ''
Show-Message '=== 2. Sysmon 服務與設定檔 ==='
$svc = Get-Service -Name 'Sysmon*' -ErrorAction SilentlyContinue
if ($svc) {
    foreach ($s in $svc) { Show-Message ("service     : " + $s.Name + " = " + $s.Status) }
} else { Show-Message 'service     : NOT FOUND' }

$sysmonExe = Get-ChildItem 'C:\Tools\DFIR' -Filter 'Sysmon64.exe' -ErrorAction SilentlyContinue
if ($sysmonExe) { Show-Message ("exe         : " + $sysmonExe.FullName) }

$cfg = 'C:\Tools\DFIR\sysmonconfig.xml'
if (Test-Path $cfg) {
    $raw = Get-Content $cfg -Raw
    Show-Message ("cfg size    : " + $raw.Length + " bytes")
    # 關鍵：ProcessAccess 是 Sysmon EID 10，預設未啟用，需要設定檔明確開啟
    $hasPA = $raw -match '<ProcessAccess'
    Show-Message ("cfg ProcessAccess(EID10) : " + $hasPA)
    if ($hasPA) {
        # 抓出 include 條件，判斷是否涵蓋 lsass.exe
        $m = [regex]::Matches($raw, '(?s)<ProcessAccess.*?</ProcessAccess>')
        foreach ($x in $m) {
            $seg = $x.Value
            Show-Message ('  PA-block len = ' + $seg.Length)
            foreach ($line in ($seg -split "`n")) {
                $t = $line.Trim()
                if ($t -match 'TargetImage|Include|onmatch|<ProcessAccess|</ProcessAccess') { Show-Message ('    ' + $t) }
            }
        }
    }
    foreach ($k in @('FileCreate', 'RegistryEvent', 'NetworkConnect', 'CreateRemoteThread', 'ImageLoad')) {
        Show-Message ("cfg has <$k> : " + ($raw -match ("<" + $k)))
    }
    # RegistryEvent 的 onmatch 方向很重要：include 只記特定機碼，exclude 則是反向
    $re = [regex]::Match($raw, '(?s)<RegistryEvent.*?</RegistryEvent>')
    if ($re.Success) { Show-Message ('  RegEvt onmatch = ' + (([regex]::Match($re.Value, 'onmatch="(\w+)"')).Groups[1].Value)) }
} else { Show-Message "cfg         : NOT FOUND ($cfg)" }

Show-Message ''
Show-Message '=== 3. 進階稽核政策（哪些 Security EID 會被寫入）==='
$ap = & auditpol.exe /get /category:* 2>&1
foreach ($line in $ap) { Show-Message $line }

Show-Message ''
Show-Message '=== 4. Windows Defender 狀態（EICAR 測試前必查）==='
try {
    $mp = Get-MpComputerStatus -ErrorAction Stop
    Show-Message ("RealTimeProtection : " + $mp.RealTimeProtectionEnabled)
    Show-Message ("AntivirusEnabled   : " + $mp.AntivirusEnabled)
    Show-Message ("BehaviorMonitor    : " + $mp.BehaviorMonitorEnabled)
    Show-Message ("TamperProtection   : " + $mp.IsTamperProtected)
} catch { Show-Message ("Get-MpComputerStatus failed: " + $_.Exception.Message) }
try {
    $pref = Get-MpPreference -ErrorAction Stop
    Show-Message ("ExclusionPath count: " + @($pref.ExclusionPath).Count)
    foreach ($p in @($pref.ExclusionPath)) { if ($p) { Show-Message ("  excl: " + $p) } }
    Show-Message ("DisableRealtimeMon : " + $pref.DisableRealtimeMonitoring)
} catch { Show-Message ("Get-MpPreference failed: " + $_.Exception.Message) }

Show-Message ''
Show-Message '=== 5. 日誌規模與時間基準 ==='
$now = Get-Date
Show-Message ("LocalNow  : " + $now.ToString('yyyy-MM-dd HH:mm:ss K'))
Show-Message ("UtcNow    : " + $now.ToUniversalTime().ToString('yyyy-MM-dd HH:mm:ss') + 'Z')
Show-Message ("TimeZone  : " + [TimeZoneInfo]::Local.Id + " (offset " + [TimeZoneInfo]::Local.BaseUtcOffset + ")")
foreach ($ln in @('Security', 'System', 'Application', 'Microsoft-Windows-Sysmon/Operational', 'Microsoft-Windows-PowerShell/Operational', 'Microsoft-Windows-TaskScheduler/Operational')) {
    try {
        $ev = Get-WinEvent -ListLog $ln -ErrorAction Stop
        Show-Message ("log : " + $ln.PadRight(46) + " count=" + $ev.RecordCount + " max=" + [math]::Round($ev.MaximumSizeInBytes/1MB,1) + "MB enabled=" + $ev.IsEnabled)
    } catch { Show-Message ("log : " + $ln.PadRight(46) + " (unavailable)") }
}

Show-Message ''
Show-Message '=== 6. Sysmon 已產生的事件類型分布 ==='
try {
    $start = (Get-Date).AddDays(-1)
    $events = Get-WinEvent -FilterHashtable @{ LogName = 'Microsoft-Windows-Sysmon/Operational'; StartTime = $start } -ErrorAction Stop
    $events | Group-Object Id | Sort-Object { [int]$_.Name } | ForEach-Object {
        Show-Message ("EID " + $_.Name.PadRight(4) + " x " + $_.Count)
    }
} catch { Show-Message ('Sysmon log query failed: ' + $_.Exception.Message) }

Show-Message ''
Show-Message '=== 7. 現有本機帳號（避免與模擬帳號碰撞）==='
& net user 2>&1 | ForEach-Object { Show-Message $_ }

Show-Message ''
Show-Message 'DONE'

# vm_day1b_recon.ps1 -- Day 1B 前置偵察：確認遙測產生器的能力邊界
# 目的：在設計「已知答案」的攻擊模擬之前，先確認哪些事件通道真的會產生事件。
# 注意：輸出必須為純 ASCII（客體 console codepage CP950 會破壞中文）。

$ErrorActionPreference = 'Continue'
$out = 'C:\Tools\DFIR\day1b'
New-Item -ItemType Directory -Force -Path $out | Out-Null

function Say([string]$m) { Write-Host $m }

Say '=== 1. 目前身分與權杖 ==='
Say ("whoami      : " + (whoami))
$id = [Security.Principal.WindowsIdentity]::GetCurrent()
$pr = New-Object Security.Principal.WindowsPrincipal($id)
Say ("IsAdmin     : " + $pr.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator))
Say ("IntegrityLvl: " + $id.Name)

Say ''
Say '=== 2. Sysmon 服務與設定檔 ==='
$svc = Get-Service -Name 'Sysmon*' -ErrorAction SilentlyContinue
if ($svc) {
    foreach ($s in $svc) { Say ("service     : " + $s.Name + " = " + $s.Status) }
} else { Say 'service     : NOT FOUND' }

$sysmonExe = Get-ChildItem 'C:\Tools\DFIR' -Filter 'Sysmon64.exe' -ErrorAction SilentlyContinue
if ($sysmonExe) { Say ("exe         : " + $sysmonExe.FullName) }

$cfg = 'C:\Tools\DFIR\sysmonconfig.xml'
if (Test-Path $cfg) {
    $raw = Get-Content $cfg -Raw
    Say ("cfg size    : " + $raw.Length + " bytes")
    # 關鍵：ProcessAccess 是 Sysmon EID 10，預設未啟用，需要設定檔明確開啟
    $hasPA = $raw -match '<ProcessAccess'
    Say ("cfg ProcessAccess(EID10) : " + $hasPA)
    if ($hasPA) {
        # 抓出 include 條件，判斷是否涵蓋 lsass.exe
        $m = [regex]::Matches($raw, '(?s)<ProcessAccess.*?</ProcessAccess>')
        foreach ($x in $m) {
            $seg = $x.Value
            Say ('  PA-block len = ' + $seg.Length)
            foreach ($line in ($seg -split "`n")) {
                $t = $line.Trim()
                if ($t -match 'TargetImage|Include|onmatch|<ProcessAccess|</ProcessAccess') { Say ('    ' + $t) }
            }
        }
    }
    foreach ($k in @('FileCreate', 'RegistryEvent', 'NetworkConnect', 'CreateRemoteThread', 'ImageLoad')) {
        Say ("cfg has <$k> : " + ($raw -match ("<" + $k)))
    }
    # RegistryEvent 的 onmatch 方向很重要：include 只記特定機碼，exclude 則是反向
    $re = [regex]::Match($raw, '(?s)<RegistryEvent.*?</RegistryEvent>')
    if ($re.Success) { Say ('  RegEvt onmatch = ' + (([regex]::Match($re.Value, 'onmatch="(\w+)"')).Groups[1].Value)) }
} else { Say "cfg         : NOT FOUND ($cfg)" }

Say ''
Say '=== 3. 進階稽核政策（哪些 Security EID 會被寫入）==='
$ap = & auditpol.exe /get /category:* 2>&1
foreach ($line in $ap) { Say $line }

Say ''
Say '=== 4. Windows Defender 狀態（EICAR 測試前必查）==='
try {
    $mp = Get-MpComputerStatus -ErrorAction Stop
    Say ("RealTimeProtection : " + $mp.RealTimeProtectionEnabled)
    Say ("AntivirusEnabled   : " + $mp.AntivirusEnabled)
    Say ("BehaviorMonitor    : " + $mp.BehaviorMonitorEnabled)
    Say ("TamperProtection   : " + $mp.IsTamperProtected)
} catch { Say ("Get-MpComputerStatus failed: " + $_.Exception.Message) }
try {
    $pref = Get-MpPreference -ErrorAction Stop
    Say ("ExclusionPath count: " + @($pref.ExclusionPath).Count)
    foreach ($p in @($pref.ExclusionPath)) { if ($p) { Say ("  excl: " + $p) } }
    Say ("DisableRealtimeMon : " + $pref.DisableRealtimeMonitoring)
} catch { Say ("Get-MpPreference failed: " + $_.Exception.Message) }

Say ''
Say '=== 5. 日誌規模與時間基準 ==='
$now = Get-Date
Say ("LocalNow  : " + $now.ToString('yyyy-MM-dd HH:mm:ss K'))
Say ("UtcNow    : " + $now.ToUniversalTime().ToString('yyyy-MM-dd HH:mm:ss') + 'Z')
Say ("TimeZone  : " + [TimeZoneInfo]::Local.Id + " (offset " + [TimeZoneInfo]::Local.BaseUtcOffset + ")")
foreach ($ln in @('Security', 'System', 'Application', 'Microsoft-Windows-Sysmon/Operational', 'Microsoft-Windows-PowerShell/Operational', 'Microsoft-Windows-TaskScheduler/Operational')) {
    try {
        $ev = Get-WinEvent -ListLog $ln -ErrorAction Stop
        Say ("log : " + $ln.PadRight(46) + " count=" + $ev.RecordCount + " max=" + [math]::Round($ev.MaximumSizeInBytes/1MB,1) + "MB enabled=" + $ev.IsEnabled)
    } catch { Say ("log : " + $ln.PadRight(46) + " (unavailable)") }
}

Say ''
Say '=== 6. Sysmon 已產生的事件類型分布 ==='
try {
    $start = (Get-Date).AddDays(-1)
    $events = Get-WinEvent -FilterHashtable @{ LogName = 'Microsoft-Windows-Sysmon/Operational'; StartTime = $start } -ErrorAction Stop
    $events | Group-Object Id | Sort-Object { [int]$_.Name } | ForEach-Object {
        Say ("EID " + $_.Name.PadRight(4) + " x " + $_.Count)
    }
} catch { Say ('Sysmon log query failed: ' + $_.Exception.Message) }

Say ''
Say '=== 7. 現有本機帳號（避免與模擬帳號碰撞）==='
& net user 2>&1 | ForEach-Object { Say $_ }

Say ''
Say 'DONE'

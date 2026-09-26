# vm_day2_recon.ps1 -- Day 2 pre-flight: survey the execution-artifact sources on the guest.
# Goal: know EXACTLY which artifacts exist and are enabled BEFORE generating any activity,
#       so that "the artifact was empty" can never be confused with "we looked wrong".
# ASCII ONLY (guest console codepage is CP950).
#
# Artifact families probed:
#   1. Prefetch        (execution count / first / last run)
#   2. Amcache         (SHA-1 of executed files)
#   3. Shimcache       (AppCompatCache, execution presence)
#   4. USBSTOR         (device serials / first install)
#   5. UserAssist      (ROT13 GUI launch paths)
#   6. ConsentStore    (mic / camera usage windows)

$ErrorActionPreference = 'Continue'
$out = 'C:\Tools\DFIR\day2'
New-Item -ItemType Directory -Force -Path $out | Out-Null

function Say([string]$m) { Write-Host $m }

$now = Get-Date
Say '=== 0. Identity / time basis ==='
Say ("whoami     : " + (whoami))
$id = [Security.Principal.WindowsIdentity]::GetCurrent()
$pr = New-Object Security.Principal.WindowsPrincipal($id)
Say ("IsAdmin    : " + $pr.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator))
Say ("LocalNow   : " + $now.ToString('yyyy-MM-dd HH:mm:ss K'))
Say ("UtcNow     : " + $now.ToUniversalTime().ToString('yyyy-MM-dd HH:mm:ss') + 'Z')
Say ("TimeZone   : " + [TimeZoneInfo]::Local.Id + " (offset " + [TimeZoneInfo]::Local.BaseUtcOffset + ")")

Say ''
Say '=== 1. Prefetch ==='
$pp = 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters'
try {
    $v = Get-ItemProperty -Path $pp -ErrorAction Stop
    Say ("EnablePrefetcher : " + $v.EnablePrefetcher + "  (0=off 1=app 2=boot 3=both)")
    Say ("EnableSuperfetch : " + $v.EnableSuperfetch)
} catch { Say ("PrefetchParameters read failed: " + $_.Exception.Message) }
$pfDir = "$env:SystemRoot\Prefetch"
if (Test-Path $pfDir) {
    $pfs = Get-ChildItem $pfDir -Filter '*.pf' -ErrorAction SilentlyContinue
    Say ("prefetch dir     : $pfDir (.pf count = " + @($pfs).Count + ")")
    Say '  sample of 10:'
    $pfs | Sort-Object LastWriteTime -Descending | Select-Object -First 10 | ForEach-Object {
        Say ('    ' + $_.Name.PadRight(40) + ' ' + $_.LastWriteTimeUtc.ToString('yyyy-MM-dd HH:mm:ss') + 'Z')
    }
    Say ("  READY1 layout   : " + (Test-Path (Join-Path $pfDir 'Layout.ini')))
    Say ("  ReadyBoot       : " + (Test-Path (Join-Path $pfDir 'ReadyBoot')))
} else { Say ("prefetch dir     : MISSING ($pfDir)") }
$sysmain = Get-Service -Name 'SysMain' -ErrorAction SilentlyContinue
if ($sysmain) { Say ("SysMain service  : " + $sysmain.Status + " / " + $sysmain.StartType) } else { Say 'SysMain service  : NOT FOUND' }

Say ''
Say '=== 2. Amcache ==='
foreach ($p in @("$env:SystemRoot\AppCompat\Programs\Amcache.hve", "$env:SystemRoot\AppCompat\Programs\Amcache.hve.LOG1", "$env:SystemRoot\AppCompat\Programs\Amcache.hve.LOG2", "$env:SystemRoot\AppCompat\Programs\RecentFileCache.bcf")) {
    if (Test-Path $p) {
        Say ('  EXISTS ' + $p + '  ' + [math]::Round((Get-Item $p).Length / 1MB, 2) + ' MB  ' + (Get-Item $p).LastWriteTimeUtc.ToString('yyyy-MM-dd HH:mm:ss') + 'Z')
    } else { Say ('  MISSING ' + $p) }
}

Say ''
Say '=== 3. Shimcache (AppCompatCache) ==='
$systemLive = 'C:\Windows\System32\config\SYSTEM'
if (Test-Path $systemLive) { Say ('  SYSTEM hive: ' + [math]::Round((Get-Item $systemLive).Length / 1MB, 2) + ' MB  ' + (Get-Item $systemLive).LastWriteTimeUtc.ToString('yyyy-MM-dd HH:mm:ss') + 'Z') }
try {
    $key = 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\AppCompatCache\AppCompatCache'
    $item = Get-Item -Path $key -ErrorAction Stop
    Say ('  AppCompatCache value size = ' + $item.GetValue('AppCompatCache').Length + ' bytes')
} catch { Say ('  AppCompatCache registry read: ' + $_.Exception.Message) }

Say ''
Say '=== 4. USBSTOR ==='
$usb = 'HKLM:\SYSTEM\CurrentControlSet\Enum\USBSTOR'
if (Test-Path $usb) {
    $devs = Get-ChildItem $usb -ErrorAction SilentlyContinue
    Say ('  USBSTOR device types = ' + @($devs).Count)
    foreach ($d in $devs) {
        $insts = Get-ChildItem $d.PSPath -ErrorAction SilentlyContinue
        foreach ($i in $insts) {
            Say ('    ' + $i.PSChildName)
        }
    }
} else { Say '  USBSTOR key MISSING' }
$setupapi = "$env:SystemRoot\inf\setupapi.dev.log"
if (Test-Path $setupapi) { Say ('  setupapi.dev.log : ' + [math]::Round((Get-Item $setupapi).Length / 1KB, 1) + ' KB') } else { Say '  setupapi.dev.log : MISSING' }
# also current mount points (real USB volumes get mountpoints2)
$mp2 = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\MountPoints2'
if (Test-Path $mp2) { Say ('  MountPoints2 entries = ' + @(Get-ChildItem $mp2 -ErrorAction SilentlyContinue).Count) } else { Say '  MountPoints2 : MISSING' }

Say ''
Say '=== 5. UserAssist ==='
$ua = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist'
if (Test-Path $ua) {
    $guids = Get-ChildItem $ua -ErrorAction SilentlyContinue
    Say ('  UserAssist GUID subkeys = ' + @($guids).Count)
    foreach ($g in $guids) {
        $cnt = Get-Item (Join-Path $g.PSPath 'Count') -ErrorAction SilentlyContinue
        if ($cnt) { Say ('    ' + $g.PSChildName + '  Count values = ' + @($cnt.GetValueNames()).Count) }
    }
} else { Say '  UserAssist : MISSING' }

Say ''
Say '=== 6. ConsentStore (mic / camera) ==='
$csRoot = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore'
foreach ($cap in @('microphone', 'webcam')) {
    $p = Join-Path $csRoot $cap
    if (Test-Path $p) {
        $subs = @(Get-ChildItem $p -Recurse -ErrorAction SilentlyContinue)
        Say ('  ' + $cap + ' : subkeys = ' + $subs.Count)
    } else { Say ('  ' + $cap + ' : MISSING') }
}
$csNonPkg = Join-Path $csRoot 'microphone\NonPackaged'
if (Test-Path $csNonPkg) { Say ('  microphone\NonPackaged apps = ' + @(Get-ChildItem $csNonPkg -ErrorAction SilentlyContinue).Count) }

Say ''
Say '=== 7. EZ Tools presence ==='
foreach ($t in @('PECmd.exe', 'AmcacheParser.exe', 'AppCompatCacheParser.exe', 'RECmd.exe', 'MFTECmd.exe', 'SBECmd.exe')) {
    $f = Get-ChildItem 'C:\Tools\DFIR\EZTools' -Filter $t -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($f) { Say ('  OK   ' + $t.PadRight(28) + $f.FullName) } else { Say ('  MISS ' + $t) }
}
$recmdBatch = Get-ChildItem 'C:\Tools\DFIR' -Filter '*.reb' -Recurse -ErrorAction SilentlyContinue | Select-Object -First 5
Say ('  RECmd batch files found: ' + @($recmdBatch).Count)
foreach ($b in $recmdBatch) { Say ('    ' + $b.FullName) }

Say ''
Say '=== 8. Baseline: known-benign already-executed programs ==='
# these give us a "before" set; after we run our own programs we can diff.
foreach ($exe in @('notepad.exe', 'calc.exe', 'cmd.exe', 'powershell.exe', 'mspaint.exe', 'write.exe', 'charmap.exe')) {
    $pf = Join-Path $pfDir (($exe.ToUpper() -replace '\.EXE$', '.EXE') + '-')
    $found = Get-ChildItem $pfDir -Filter ($exe.Split('.')[0].ToUpper() + '.EXE-*') -ErrorAction SilentlyContinue
    $n = @($found).Count
    Say ('  ' + $exe.PadRight(16) + ' prefetch present = ' + $n)
}

Say ''
Say 'DONE recon'

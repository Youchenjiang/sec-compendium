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

function Show-Message([string]$m) { Write-Host $m }

$now = Get-Date
Show-Message '=== 0. Identity / time basis ==='
Show-Message ("whoami     : " + (whoami))
$id = [Security.Principal.WindowsIdentity]::GetCurrent()
$pr = New-Object Security.Principal.WindowsPrincipal($id)
Show-Message ("IsAdmin    : " + $pr.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator))
Show-Message ("LocalNow   : " + $now.ToString('yyyy-MM-dd HH:mm:ss K'))
Show-Message ("UtcNow     : " + $now.ToUniversalTime().ToString('yyyy-MM-dd HH:mm:ss') + 'Z')
Show-Message ("TimeZone   : " + [TimeZoneInfo]::Local.Id + " (offset " + [TimeZoneInfo]::Local.BaseUtcOffset + ")")

Show-Message ''
Show-Message '=== 1. Prefetch ==='
$pp = 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters'
try {
    $v = Get-ItemProperty -Path $pp -ErrorAction Stop
    Show-Message ("EnablePrefetcher : " + $v.EnablePrefetcher + "  (0=off 1=app 2=boot 3=both)")
    Show-Message ("EnableSuperfetch : " + $v.EnableSuperfetch)
} catch { Show-Message ("PrefetchParameters read failed: " + $_.Exception.Message) }
$pfDir = "$env:SystemRoot\Prefetch"
if (Test-Path $pfDir) {
    $pfs = Get-ChildItem $pfDir -Filter '*.pf' -ErrorAction SilentlyContinue
    Show-Message ("prefetch dir     : $pfDir (.pf count = " + @($pfs).Count + ")")
    Show-Message '  sample of 10:'
    $pfs | Sort-Object LastWriteTime -Descending | Select-Object -First 10 | ForEach-Object {
        Show-Message ('    ' + $_.Name.PadRight(40) + ' ' + $_.LastWriteTimeUtc.ToString('yyyy-MM-dd HH:mm:ss') + 'Z')
    }
    Show-Message ("  READY1 layout   : " + (Test-Path (Join-Path $pfDir 'Layout.ini')))
    Show-Message ("  ReadyBoot       : " + (Test-Path (Join-Path $pfDir 'ReadyBoot')))
} else { Show-Message ("prefetch dir     : MISSING ($pfDir)") }
$sysmain = Get-Service -Name 'SysMain' -ErrorAction SilentlyContinue
if ($sysmain) { Show-Message ("SysMain service  : " + $sysmain.Status + " / " + $sysmain.StartType) } else { Show-Message 'SysMain service  : NOT FOUND' }

Show-Message ''
Show-Message '=== 2. Amcache ==='
foreach ($p in @("$env:SystemRoot\AppCompat\Programs\Amcache.hve", "$env:SystemRoot\AppCompat\Programs\Amcache.hve.LOG1", "$env:SystemRoot\AppCompat\Programs\Amcache.hve.LOG2", "$env:SystemRoot\AppCompat\Programs\RecentFileCache.bcf")) {
    if (Test-Path $p) {
        Show-Message ('  EXISTS ' + $p + '  ' + [math]::Round((Get-Item $p).Length / 1MB, 2) + ' MB  ' + (Get-Item $p).LastWriteTimeUtc.ToString('yyyy-MM-dd HH:mm:ss') + 'Z')
    } else { Show-Message ('  MISSING ' + $p) }
}

Show-Message ''
Show-Message '=== 3. Shimcache (AppCompatCache) ==='
$systemLive = 'C:\Windows\System32\config\SYSTEM'
if (Test-Path $systemLive) { Show-Message ('  SYSTEM hive: ' + [math]::Round((Get-Item $systemLive).Length / 1MB, 2) + ' MB  ' + (Get-Item $systemLive).LastWriteTimeUtc.ToString('yyyy-MM-dd HH:mm:ss') + 'Z') }
try {
    $key = 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\AppCompatCache\AppCompatCache'
    $item = Get-Item -Path $key -ErrorAction Stop
    Show-Message ('  AppCompatCache value size = ' + $item.GetValue('AppCompatCache').Length + ' bytes')
} catch { Show-Message ('  AppCompatCache registry read: ' + $_.Exception.Message) }

Show-Message ''
Show-Message '=== 4. USBSTOR ==='
$usb = 'HKLM:\SYSTEM\CurrentControlSet\Enum\USBSTOR'
if (Test-Path $usb) {
    $devs = Get-ChildItem $usb -ErrorAction SilentlyContinue
    Show-Message ('  USBSTOR device types = ' + @($devs).Count)
    foreach ($d in $devs) {
        $insts = Get-ChildItem $d.PSPath -ErrorAction SilentlyContinue
        foreach ($i in $insts) {
            Show-Message ('    ' + $i.PSChildName)
        }
    }
} else { Show-Message '  USBSTOR key MISSING' }
$setupapi = "$env:SystemRoot\inf\setupapi.dev.log"
if (Test-Path $setupapi) { Show-Message ('  setupapi.dev.log : ' + [math]::Round((Get-Item $setupapi).Length / 1KB, 1) + ' KB') } else { Show-Message '  setupapi.dev.log : MISSING' }
# also current mount points (real USB volumes get mountpoints2)
$mp2 = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\MountPoints2'
if (Test-Path $mp2) { Show-Message ('  MountPoints2 entries = ' + @(Get-ChildItem $mp2 -ErrorAction SilentlyContinue).Count) } else { Show-Message '  MountPoints2 : MISSING' }

Show-Message ''
Show-Message '=== 5. UserAssist ==='
$ua = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist'
if (Test-Path $ua) {
    $guids = Get-ChildItem $ua -ErrorAction SilentlyContinue
    Show-Message ('  UserAssist GUID subkeys = ' + @($guids).Count)
    foreach ($g in $guids) {
        $cnt = Get-Item (Join-Path $g.PSPath 'Count') -ErrorAction SilentlyContinue
        if ($cnt) { Show-Message ('    ' + $g.PSChildName + '  Count values = ' + @($cnt.GetValueNames()).Count) }
    }
} else { Show-Message '  UserAssist : MISSING' }

Show-Message ''
Show-Message '=== 6. ConsentStore (mic / camera) ==='
$csRoot = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore'
foreach ($cap in @('microphone', 'webcam')) {
    $p = Join-Path $csRoot $cap
    if (Test-Path $p) {
        $subs = @(Get-ChildItem $p -Recurse -ErrorAction SilentlyContinue)
        Show-Message ('  ' + $cap + ' : subkeys = ' + $subs.Count)
    } else { Show-Message ('  ' + $cap + ' : MISSING') }
}
$csNonPkg = Join-Path $csRoot 'microphone\NonPackaged'
if (Test-Path $csNonPkg) { Show-Message ('  microphone\NonPackaged apps = ' + @(Get-ChildItem $csNonPkg -ErrorAction SilentlyContinue).Count) }

Show-Message ''
Show-Message '=== 7. EZ Tools presence ==='
foreach ($t in @('PECmd.exe', 'AmcacheParser.exe', 'AppCompatCacheParser.exe', 'RECmd.exe', 'MFTECmd.exe', 'SBECmd.exe')) {
    $f = Get-ChildItem 'C:\Tools\DFIR\EZTools' -Filter $t -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($f) { Show-Message ('  OK   ' + $t.PadRight(28) + $f.FullName) } else { Show-Message ('  MISS ' + $t) }
}
$recmdBatch = Get-ChildItem 'C:\Tools\DFIR' -Filter '*.reb' -Recurse -ErrorAction SilentlyContinue | Select-Object -First 5
Show-Message ('  RECmd batch files found: ' + @($recmdBatch).Count)
foreach ($b in $recmdBatch) { Show-Message ('    ' + $b.FullName) }

Show-Message ''
Show-Message '=== 8. Baseline: known-benign already-executed programs ==='
# these give us a "before" set; after we run our own programs we can diff.
foreach ($exe in @('notepad.exe', 'calc.exe', 'cmd.exe', 'powershell.exe', 'mspaint.exe', 'write.exe', 'charmap.exe')) {
    $pf = Join-Path $pfDir (($exe.ToUpper() -replace '\.EXE$', '.EXE') + '-')
    $found = Get-ChildItem $pfDir -Filter ($exe.Split('.')[0].ToUpper() + '.EXE-*') -ErrorAction SilentlyContinue
    $n = @($found).Count
    Show-Message ('  ' + $exe.PadRight(16) + ' prefetch present = ' + $n)
}

Show-Message ''
Show-Message 'DONE recon'

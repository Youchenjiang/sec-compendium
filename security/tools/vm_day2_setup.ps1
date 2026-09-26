# vm_day2_setup.ps1 -- Day 2 known-answer dataset builder (FLARE-VM guest).
#
# Produces two data sources, both with a recorded answer key:
#   A. Organic activity  -> Prefetch / Amcache / Shimcache (real tool telemetry, we control timing)
#   B. Hive fixtures     -> USBSTOR / UserAssist / ConsentStore (real hive FORMAT, injected values)
#      Why fixtures: this VM is headless (no interactive user hive, no USB device, no camera/mic),
#      so those three artifacts can never appear organically. We clone REAL hives with `reg save`,
#      inject exactly-known values, unload, and let the parsers read them like any on-disk hive.
#
# ASCII ONLY. Idempotent: re-running rebuilds everything from scratch.
# Every injected value is written into groundtruth\ground_truth.csv so verification is possible.

$ErrorActionPreference = 'Continue'
$base  = 'C:\Tools\DFIR\day2'
$hives = Join-Path $base 'hives'
$gtDir = Join-Path $base 'groundtruth'
$snap  = Join-Path $base 'snapshot'
New-Item -ItemType Directory -Force -Path $base | Out-Null
foreach ($d in @($hives, $gtDir, $snap)) {
    Remove-Item $d -Recurse -Force -ErrorAction SilentlyContinue
    New-Item -ItemType Directory -Force -Path $d | Out-Null
}
function Say([string]$m) { Write-Host $m }

$gt = New-Object System.Collections.Generic.List[object]
function AddGt($kind, $key, $value, $note) {
    $gt.Add([pscustomobject]@{ kind = $kind; key = $key; value = $value; note = $note }) | Out-Null
}

# ---------------------------------------------------------------- 0. baseline time
$t0 = [DateTime]::UtcNow
Say ('=== Day 2 setup start  UTC=' + $t0.ToString('yyyy-MM-dd HH:mm:ss') + 'Z ===')
$tz = [TimeZoneInfo]::Local
Say ('local timezone: ' + $tz.Id + ' offset ' + $tz.BaseUtcOffset)

# ---------------------------------------------------------------- 1. enable Prefetch
Say ''
Say '=== 1. enable Prefetch / start SysMain ==='
$pp = 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters'
Set-ItemProperty -Path $pp -Name 'EnablePrefetcher' -Value 3 -Type DWord
Set-ItemProperty -Path $pp -Name 'EnableSuperfetch' -Value 3 -Type DWord
$sysmain = Get-Service -Name 'SysMain' -ErrorAction SilentlyContinue
if ($sysmain) {
    if ($sysmain.StartType -eq 'Disabled') { Set-Service -Name 'SysMain' -StartupType Automatic }
    if ($sysmain.Status -ne 'Running') { Start-Service -Name 'SysMain' -ErrorAction SilentlyContinue; Start-Sleep -Seconds 2 }
    $sysmain2 = Get-Service -Name 'SysMain'
    Say ('  SysMain now: ' + $sysmain2.Status + ' / ' + $sysmain2.StartType)
} else { Say '  SysMain NOT FOUND' }
AddGt 'config' 'EnablePrefetcher' '3' 'prefetch enabled (both)'
AddGt 'config' 'SysMain' ($(if ($sysmain) { (Get-Service SysMain).Status } else { 'n/a' })) 'prefetch generation service'

# Only remove Prefetch entries owned by this lab. Never delete unrelated host history.
$pfDir = "$env:SystemRoot\Prefetch"
$oldPf = @(Get-ChildItem $pfDir -Filter 'SPRINT_DAY2_*.pf' -ErrorAction SilentlyContinue)
$oldPf | Remove-Item -Force -ErrorAction SilentlyContinue
Say ('  removed prior SPRINT_DAY2 prefetch entries: ' + $oldPf.Count)

# ---------------------------------------------------------------- 2. custom test program
Say ''
Say '=== 2. stage a distinctive test program ==='
$custom = Join-Path $base 'sprint_day2_app.exe'
Copy-Item "$env:SystemRoot\System32\cmd.exe" $custom -Force
$sha1   = (Get-FileHash $custom -Algorithm SHA1).Hash
$sha256 = (Get-FileHash $custom -Algorithm SHA256).Hash
Say ('  path   : ' + $custom)
Say ('  sha1   : ' + $sha1)
Say ('  sha256 : ' + $sha256)
AddGt 'amcache' 'sprint_day2_app.exe' $sha1 'expected SHA1 line in amcache (same content as cmd.exe)'

# A UNIQUE binary: Amcache keys file entries by CONTENT hash, so a byte copy of cmd.exe
# collapses onto cmd.exe's SHA1. Compiling once gives us a hash that can only be ours.
$uniq = Join-Path $base 'sprint_day2_unique.exe'
Remove-Item $uniq -Force -ErrorAction SilentlyContinue
try {
    Add-Type -TypeDefinition 'public class S2 { public static void Main() { System.Console.WriteLine("day2-unique"); } }' `
        -OutputAssembly $uniq -OutputType ConsoleApplication -ErrorAction Stop
    $uSha1 = (Get-FileHash $uniq -Algorithm SHA1).Hash
    Say ('  unique path : ' + $uniq)
    Say ('  unique sha1 : ' + $uSha1)
    AddGt 'amcache' 'sprint_day2_unique.exe' $uSha1 'expected SHA1 line in amcache (unique binary)'
} catch { Say ('  unique compile FAILED: ' + $_.Exception.Message) }

# Give the remaining controls dedicated executable names too. Running the system
# WHERE.EXE / SORT.EXE directly would inherit historical Prefetch counts and break
# the known-answer invariant after any earlier use of those binaries.
$whereCopy = Join-Path $base 'sprint_day2_where.exe'
$sortCopy  = Join-Path $base 'sprint_day2_sort.exe'
Copy-Item "$env:SystemRoot\System32\where.exe" $whereCopy -Force
Copy-Item "$env:SystemRoot\System32\sort.exe"  $sortCopy  -Force

# ---------------------------------------------------------------- 3. organic execution activity
Say ''
Say '=== 3. run known-answer execution activity ==='
# (program, argument list, run count, label)
$plan = @(
    @{ exe = $custom;               args = @('/c', 'exit'); label = 'sprint_day2_app.exe'; runs = 5 },
    @{ exe = $uniq;                 args = @();            label = 'sprint_day2_unique.exe'; runs = 3 },
    @{ exe = $whereCopy;            args = @('/?');         label = 'sprint_day2_where.exe'; runs = 3 },
    @{ exe = $sortCopy;             args = @('/?');         label = 'sprint_day2_sort.exe';  runs = 2 }
)
foreach ($p in $plan) {
    if (-not (Test-Path $p.exe)) { Say ('  SKIP missing: ' + $p.exe); continue }
    for ($i = 1; $i -le $p.runs; $i++) {
        $s = [DateTime]::UtcNow
        try {
            # Redirected stdin closed immediately => an app that prompts can never hang us (Day 1B lesson).
            $psi = New-Object System.Diagnostics.ProcessStartInfo
            $psi.FileName = $p.exe
            $psi.Arguments = ($p.args -join ' ')
            $psi.UseShellExecute = $false
            $psi.RedirectStandardInput = $true
            $psi.RedirectStandardOutput = $true
            $psi.RedirectStandardError = $true
            $proc = [System.Diagnostics.Process]::Start($psi)
            $proc.StandardInput.Close()
            if (-not $proc.WaitForExit(15000)) { $proc.Kill() }
            $s2 = $proc.ExitCode
        } catch {
            $s2 = 'ERR:' + $_.Exception.Message
        }
        $e = [DateTime]::UtcNow
        Say ('  run ' + $p.label.PadRight(20) + ' #' + $i + '  utc=' + $s.ToString('yyyy-MM-dd HH:mm:ss.fff') + 'Z  exit=' + $s2)
        AddGt 'exec' $p.label ('(' + $i + '/' + $p.runs + ') ' + $s.ToString('yyyy-MM-dd HH:mm:ss') + 'Z') 'organic run for prefetch/amcache/shimcache'
        Start-Sleep -Milliseconds 700
    }
}

# ---------------------------------------------------------------- 4. USBSTOR fixture (real SYSTEM hive)
Say ''
Say '=== 4. build USBSTOR fixture on a cloned SYSTEM hive ==='
$sysHive = Join-Path $hives 'SYSTEM_copy.hive'
Remove-Item $sysHive -Force -ErrorAction SilentlyContinue
& reg.exe save 'HKLM\SYSTEM' $sysHive /y 2>&1 | ForEach-Object { Say ('  ' + $_) }
$devType  = 'Disk&Ven_Sprint&Prod_Day2USB&Rev_1.00'
$serial   = 'SPRINT2FLASH'
$instId   = "$serial&0"                 # <-- the '&0' suffix that must be stripped for the true serial
$mountKey = 'HKLM\Day2Sys'
& reg.exe load $mountKey $sysHive 2>&1 | ForEach-Object { Say ('  load: ' + $_) }
$usbRoot = "$mountKey\CurrentControlSet\Enum\USBSTOR\$devType\$instId"
& reg.exe add $usbRoot /v 'DeviceDesc'      /t REG_SZ    /d '@usbstor.inf,%disk%;USB Mass Storage Device' /f 2>&1 | Out-Null
& reg.exe add $usbRoot /v 'FriendlyName'    /t REG_SZ    /d 'Sprint Day2 USB Flash' /f 2>&1 | Out-Null
& reg.exe add $usbRoot /v 'Mfg'             /t REG_SZ    /d '@usbstor.inf,%manufacturer%;USB Mass Storage' /f 2>&1 | Out-Null
& reg.exe add $usbRoot /v 'Service'         /t REG_SZ    /d 'USBSTOR' /f 2>&1 | Out-Null
$firstInstall = [DateTime]::UtcNow.ToFileTimeUtc()
& reg.exe add $usbRoot /v 'FirstInstallDate' /t REG_QWORD /d $firstInstall /f 2>&1 | Out-Null
# a decoy USB (non-storage) device so analysts must pick the storage one
$usbDev = "$mountKey\CurrentControlSet\Enum\USB\VID_0E0F&PID_0002\5&2bobfak3&0&1"
& reg.exe add $usbDev /v 'DeviceDesc' /t REG_SZ /d '@usb.inf,%usb\composite.devicedesc%;USB Composite Device' /f 2>&1 | Out-Null
& reg.exe unload $mountKey 2>&1 | ForEach-Object { Say ('  unload: ' + $_) }
Say ('  device type : ' + $devType)
Say ('  instance id : ' + $instId + '  (true serial = ' + $serial + ')')
AddGt 'usbstore' 'device_type' $devType 'USBSTOR device class key'
AddGt 'usbstore' 'instance_id' $instId 'contains &0 suffix'
AddGt 'usbstore' 'true_serial' $serial 'serial after stripping &0'
AddGt 'usbstore' 'first_install_utc' ([DateTime]::FromFileTimeUtc($firstInstall).ToString('yyyy-MM-dd HH:mm:ss') + 'Z') 'injected FirstInstallDate'

# ---------------------------------------------------------------- 5. UserAssist + ConsentStore fixture (real user hive)
Say ''
Say '=== 5. build UserAssist + ConsentStore fixture on a cloned user hive ==='
$userHive = Join-Path $hives 'NTUSER_fixture.hive'
Remove-Item $userHive -Force -ErrorAction SilentlyContinue
& reg.exe save 'HKU\.DEFAULT' $userHive /y 2>&1 | ForEach-Object { Say ('  ' + $_) }
$mountU = 'HKLM\Day2U'
& reg.exe load $mountU $userHive 2>&1 | ForEach-Object { Say ('  load: ' + $_) }

function Rot13([string]$s) {
    $sb = New-Object System.Text.StringBuilder
    foreach ($c in $s.ToCharArray()) {
        $code = [int][char]$c
        if     ($code -ge 65 -and $code -le 90)  { [void]$sb.Append([char](65  + (($code - 65  + 13) % 26))) }
        elseif ($code -ge 97 -and $code -le 122) { [void]$sb.Append([char](97  + (($code - 97  + 13) % 26))) }
        else { [void]$sb.Append($c) }
    }
    return $sb.ToString()
}

# UserAssist: 72-byte count blob; run count at offset 4 (DWORD LE), last-run FILETIME at offset 8 (QWORD LE).
$uaGuid = '{CEBFF5CD-ACE2-4F4F-9178-9926F41749EA}'
$uaCountKey = "$mountU\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist\$uaGuid\Count"
& reg.exe add $uaCountKey /f 2>&1 | Out-Null
$uaPath = 'C:\Tools\DFIR\day2\sprint_day2_app.exe'
$uaRot  = Rot13($uaPath)
$uaRuns = 5
$uaLast = [DateTime]::UtcNow.AddMinutes(-2).ToFileTimeUtc()
$bytes = New-Object byte[] 72
[BitConverter]::GetBytes([uint32]$uaRuns).CopyTo($bytes, 4)
[BitConverter]::GetBytes([int64]$uaLast).CopyTo($bytes, 60)
$uaHex = ($bytes | ForEach-Object { $_.ToString('x2') }) -join ''
& reg.exe add $uaCountKey /v $uaRot /t REG_BINARY /d $uaHex /f 2>&1 | ForEach-Object { Say ('  ua: ' + $_) }
Say ('  UserAssist value (ROT13) : ' + $uaRot)
Say ('  -> decoded path          : ' + $uaPath + '  (runs=' + $uaRuns + ', last->' + [DateTime]::FromFileTimeUtc($uaLast).ToString('yyyy-MM-dd HH:mm:ss') + 'Z)')
AddGt 'userassist' 'rot13_value' $uaRot 'raw value name as stored'
AddGt 'userassist' 'decoded_path' $uaPath 'ROT13-decoded'
AddGt 'userassist' 'run_count' "$uaRuns" 'expected run count'
AddGt 'userassist' 'last_run_utc' ([DateTime]::FromFileTimeUtc($uaLast).ToString('yyyy-MM-dd HH:mm:ss') + 'Z') 'expected last run'

# ConsentStore: microphone + webcam with known start/stop windows for NonPackaged apps.
$csRoot = "$mountU\Software\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore"
$micStart = [DateTime]::UtcNow.AddMinutes(-30).ToFileTimeUtc()
$micStop  = [DateTime]::UtcNow.AddMinutes(-28).ToFileTimeUtc()
$camStart = [DateTime]::UtcNow.AddMinutes(-10).ToFileTimeUtc()
$camStop  = [DateTime]::UtcNow.AddMinutes(-9).ToFileTimeUtc()
$micKey = "$csRoot\microphone\NonPackaged\C:#Tools#DFIR#day2#day2_mic.exe"
$camKey = "$csRoot\webcam\NonPackaged\C:#Tools#DFIR#day2#day2_cam.exe"
& reg.exe add $micKey /v 'Value' /t REG_SZ /d 'Allow' /f 2>&1 | Out-Null
& reg.exe add $micKey /v 'LastUsedTimeStart' /t REG_QWORD /d $micStart /f 2>&1 | Out-Null
& reg.exe add $micKey /v 'LastUsedTimeStop'  /t REG_QWORD /d $micStop  /f 2>&1 | Out-Null
& reg.exe add $camKey /v 'Value' /t REG_SZ /d 'Allow' /f 2>&1 | Out-Null
& reg.exe add $camKey /v 'LastUsedTimeStart' /t REG_QWORD /d $camStart /f 2>&1 | Out-Null
& reg.exe add $camKey /v 'LastUsedTimeStop'  /t REG_QWORD /d $camStop  /f 2>&1 | Out-Null
Say ('  mic window : ' + [DateTime]::FromFileTimeUtc($micStart).ToString('yyyy-MM-dd HH:mm:ss') + 'Z -> ' + [DateTime]::FromFileTimeUtc($micStop).ToString('yyyy-MM-dd HH:mm:ss') + 'Z  (' + ([DateTime]::FromFileTimeUtc($micStop) - [DateTime]::FromFileTimeUtc($micStart)).TotalSeconds + ' s)')
Say ('  cam window : ' + [DateTime]::FromFileTimeUtc($camStart).ToString('yyyy-MM-dd HH:mm:ss') + 'Z -> ' + [DateTime]::FromFileTimeUtc($camStop).ToString('yyyy-MM-dd HH:mm:ss') + 'Z  (' + ([DateTime]::FromFileTimeUtc($camStop) - [DateTime]::FromFileTimeUtc($camStart)).TotalSeconds + ' s)')
AddGt 'consentstore' 'microphone' ('start=' + [DateTime]::FromFileTimeUtc($micStart).ToString('yyyy-MM-dd HH:mm:ss') + 'Z stop=' + [DateTime]::FromFileTimeUtc($micStop).ToString('yyyy-MM-dd HH:mm:ss') + 'Z') 'expected mic window (120s)'
AddGt 'consentstore' 'webcam'     ('start=' + [DateTime]::FromFileTimeUtc($camStart).ToString('yyyy-MM-dd HH:mm:ss') + 'Z stop=' + [DateTime]::FromFileTimeUtc($camStop).ToString('yyyy-MM-dd HH:mm:ss') + 'Z') 'expected cam window (60s)'

& reg.exe unload $mountU 2>&1 | ForEach-Object { Say ('  unload: ' + $_) }

# ---------------------------------------------------------------- 6. snapshot organic artifacts
Say ''
Say '=== 6. snapshot organic artifacts ==='
Copy-Item "$env:SystemRoot\Prefetch\*.pf" $snap -Force -ErrorAction SilentlyContinue
Say ('  prefetch .pf copied : ' + @(Get-ChildItem $snap -Filter '*.pf').Count)

# Amcache.hve is held open by the OS: esentutl /y /vss makes a VSS copy without touching the source.
$amSrc = "$env:SystemRoot\AppCompat\Programs\Amcache.hve"
$amDst = Join-Path $snap 'Amcache.hve'
Remove-Item $amDst -Force -ErrorAction SilentlyContinue
$esy = & "$env:SystemRoot\System32\esentutl.exe" /y /vss $amSrc /d $amDst 2>&1 | Out-String
if (Test-Path $amDst) {
    Say ('  Amcache.hve copied : ' + [math]::Round((Get-Item $amDst).Length / 1MB, 2) + ' MB')
} else {
    Say '  esentutl copy failed, trying plain copy'
    Copy-Item $amSrc $amDst -Force -ErrorAction SilentlyContinue
    if (Test-Path $amDst) { Say ('  Amcache.hve copied (plain): ' + [math]::Round((Get-Item $amDst).Length / 1MB, 2) + ' MB') } else { Say '  Amcache.hve STILL MISSING' }
}

# SYSTEM + SOFTWARE live hives already captured via reg save above; add a SOFTWARE copy for completeness.
$softHive = Join-Path $hives 'SOFTWARE_copy.hive'
Remove-Item $softHive -Force -ErrorAction SilentlyContinue
& reg.exe save 'HKLM\SOFTWARE' $softHive /y 2>&1 | ForEach-Object { Say ('  ' + $_) }

# ---------------------------------------------------------------- 7. write ground truth
$gtCsv = Join-Path $gtDir 'ground_truth.csv'
$gt | Export-Csv -Path $gtCsv -NoTypeInformation -Encoding UTF8
Say ''
Say ('=== ground truth written: ' + $gtCsv + '  rows=' + $gt.Count + ' ===')
Say ''
Say ('=== setup finished UTC=' + [DateTime]::UtcNow.ToString('yyyy-MM-dd HH:mm:ss') + 'Z ===')
Say 'DONE setup'

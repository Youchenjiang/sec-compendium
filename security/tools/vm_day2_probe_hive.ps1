# vm_day2_probe_hive.ps1 -- resolve WHICH user hive the guest artifacts actually live in.
# Day 1B lesson: under a non-interactive vmrun session, HKCU can resolve to HKU\.DEFAULT
# instead of the real logged-on user. That would make UserAssist/ConsentStore look "MISSING"
# when they are not. This probe settles it by addressing the user hive by SID explicitly.
# ASCII ONLY.

$ErrorActionPreference = 'Continue'
function Show-Message([string]$m) { Write-Host $m }

Show-Message '=== whoami /user ==='
& whoami.exe /user 2>&1 | ForEach-Object { Show-Message $_ }

Show-Message ''
Show-Message '=== HKU loaded hives ==='
& reg.exe query HKU 2>&1 | ForEach-Object { Show-Message $_ }

Show-Message ''
Show-Message '=== current user profile files ==='
foreach ($f in @("$env:USERPROFILE\NTUSER.DAT", 'C:\Users\LabStrix\NTUSER.DAT', "$env:USERPROFILE\NTUSER.DAT.LOG1")) {
    if (Test-Path $f) {
        Show-Message ('  EXISTS ' + $f + '  ' + [math]::Round((Get-Item $f).Length / 1MB, 2) + ' MB  ' + (Get-Item $f).LastWriteTimeUtc.ToString('yyyy-MM-dd HH:mm:ss') + 'Z')
    } else { Show-Message ('  MISSING ' + $f) }
}

$sid = ([Security.Principal.WindowsIdentity]::GetCurrent()).User.Value
Show-Message ''
Show-Message ('=== artifacts under the real user hive HKU\' + $sid + ' ===')
foreach ($rel in @(
    'Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist',
    'Software\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\microphone',
    'Software\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam'
)) {
    $p = "HKU:\$sid\$rel"
    if (Test-Path $p) {
        $subs = @(Get-ChildItem $p -ErrorAction SilentlyContinue)
        Show-Message ('  PRESENT ' + $rel + '  subkeys=' + $subs.Count)
        foreach ($s in $subs) { Show-Message ('      ' + $s.PSChildName) }
    } else { Show-Message ('  ABSENT  ' + $rel) }
}

Show-Message ''
Show-Message '=== HKLM USBSTOR (explicit) ==='
& reg.exe query 'HKLM\SYSTEM\CurrentControlSet\Enum\USBSTOR' 2>&1 | ForEach-Object { Show-Message ('  ' + $_) }

Show-Message ''
Show-Message '=== setupapi.dev.log tail (device install history) ==='
$log = "$env:SystemRoot\inf\setupapi.dev.log"
if (Test-Path $log) {
    $lines = Get-Content $log -ErrorAction SilentlyContinue
    Show-Message ('  total lines = ' + @($lines).Count)
    $usbHits = $lines | Select-String -Pattern 'USB' -SimpleMatch | Select-Object -First 15
    foreach ($h in $usbHits) { Show-Message ('  | ' + $h.Line.Trim()) }
} else { Show-Message '  setupapi.dev.log MISSING' }

Show-Message ''
Show-Message 'DONE probe'

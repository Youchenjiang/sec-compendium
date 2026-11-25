# vm_day1b_harden.ps1 -- Day 1B Phase 0: visibility baseline.
#
# WHY THIS EXISTS
#   A "known-answer" dataset is only useful if the events we care about are
#   actually written somewhere. On a stock Windows 10 install several are NOT:
#     - 4688 (process creation)      : audit subcategory "Process Creation"
#                                      defaults to Not Configured
#     - 4698 (scheduled task created): "Other Object Access Events" Not Configured
#     - 4776 (NTLM credential check) : "Credential Validation" Not Configured
#     - 4104 (PS script block)       : ScriptBlockLogging policy absent
#     - TaskScheduler/Operational    : channel disabled
#   Everything here is reversible: vm_day1b_cleanup.ps1 -Full reverts it.
#
# ASCII ONLY. PowerShell 5.1 parses a BOM-less .ps1 as the ANSI codepage
# (CP950 on this guest), so non-ASCII literals would be corrupted.

$ErrorActionPreference = 'Continue'
$out = 'C:\Tools\DFIR\day1b'
New-Item -ItemType Directory -Force -Path $out | Out-Null
$log = Join-Path $out 'harden_log.txt'
$utf8 = New-Object System.Text.UTF8Encoding($false)
function L([string]$m) { [IO.File]::AppendAllText($log, $m + "`r`n", $utf8) }
[IO.File]::WriteAllText($log, '', $utf8)

L '=== Day 1B Phase 0: visibility baseline ==='
L ('local : ' + (Get-Date).ToString('yyyy-MM-dd HH:mm:ss K'))
L ('utc   : ' + (Get-Date).ToUniversalTime().ToString('yyyy-MM-dd HH:mm:ss') + 'Z')
L ('tz    : ' + [TimeZoneInfo]::Local.Id)

# ---------- 0-1  audit policy: snapshot + raw CSV dump ----------
L ''
L '--- 0-1 audit policy snapshot ---'
& auditpol.exe /backup /file:$out\auditpol_backup.csv 2>&1 | ForEach-Object { L ('  ' + $_) }
L ('  auditpol /backup exit=' + $LASTEXITCODE)
foreach ($f in @("$out\auditpol_backup.csv", "$out\auditpol_backup.csv.old")) {
    if (Test-Path $f) { L ('  snapshot file: ' + (Split-Path $f -Leaf) + ' (' + (Get-Item $f).Length + ' bytes)') }
}
# /r gives CSV; subcategory names come out in the OS language but the
# Subcategory GUID column is always ASCII, so we key on GUIDs.
$csvBefore = & auditpol.exe /get /category:* /r 2>&1
[IO.File]::WriteAllLines("$out\auditpol_before.csv", $csvBefore, $utf8)
L ('  auditpol_before.csv lines=' + @($csvBefore).Count)

$guids = [ordered]@{
    'Process Creation'             = '{0CCE922B-69AE-11D9-BED3-505054503030}'
    'Other Object Access Events'   = '{0CCE9227-69AE-11D9-BED3-505054503030}'
    'Credential Validation'        = '{0CCE923F-69AE-11D9-BED3-505054503030}'
    'Logon'                        = '{0CCE9215-69AE-11D9-BED3-505054503030}'
    'Special Logon'                = '{0CCE921B-69AE-11D9-BED3-505054503030}'
    'User Account Management'      = '{0CCE9235-69AE-11D9-BED3-505054503030}'
    'Security System Extension'    = '{0CCE9211-69AE-11D9-BED3-505054503030}'
    'Audit Policy Change'          = '{0CCE922F-69AE-11D9-BED3-505054503030}'
}
L ''
L '--- 0-1b BEFORE: setting per GUID (CSV col5 = inclusion) ---'
foreach ($k in $guids.Keys) {
    $hit = $csvBefore | Where-Object { $_ -like ('*' + $guids[$k] + '*') }
    L ('  ' + $k.PadRight(28) + ' => ' + (($hit | Select-Object -First 1) -replace '.*', '$0'))
}

# ---------- 0-2  enable the three audit subcategories ----------
L ''
L '--- 0-2 enabling audit subcategories (by GUID, locale independent) ---'
$enable = @(
    @{ name = 'Process Creation';           guid = $guids['Process Creation'];           why = 'Security 4688 -> process tree can be rebuilt from Security.evtx' },
    @{ name = 'Other Object Access Events'; guid = $guids['Other Object Access Events']; why = 'Security 4698/4699 -> scheduled task object access' },
    @{ name = 'Credential Validation';      guid = $guids['Credential Validation'];      why = 'Security 4776 -> NTLM credential check, pairs with 4625' }
)
foreach ($e in $enable) {
    & auditpol.exe /set /subcategory:$($e.guid) /success:enable /failure:enable 2>&1 | Out-Null
    L ('  enabled ' + $e.name.PadRight(28) + ' exit=' + $LASTEXITCODE + '  (' + $e.why + ')')
}

# ---------- 0-3  4688 command line ----------
L ''
L '--- 0-3 4688 command line capture ---'
$auditKey = 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\Audit'
New-Item -Path $auditKey -Force | Out-Null
New-ItemProperty -Path $auditKey -Name 'ProcessCreationIncludeCmdLine_Enabled' -Value 1 -PropertyType DWord -Force | Out-Null
L ('  ProcessCreationIncludeCmdLine_Enabled = ' + (Get-ItemProperty -Path $auditKey -Name ProcessCreationIncludeCmdLine_Enabled).ProcessCreationIncludeCmdLine_Enabled)
L '  NOTE: without this, 4688 fires but CommandLine is a single dash.'

# ---------- 0-4  PowerShell script block logging ----------
L ''
L '--- 0-4 PowerShell script block logging (EID 4104) ---'
$psKey = 'HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging'
New-Item -Path $psKey -Force | Out-Null
New-ItemProperty -Path $psKey -Name 'EnableScriptBlockLogging' -Value 1 -PropertyType DWord -Force | Out-Null
New-ItemProperty -Path $psKey -Name 'EnableScriptBlockInvocationLogging' -Value 1 -PropertyType DWord -Force | Out-Null
L ('  EnableScriptBlockLogging = ' + (Get-ItemProperty -Path $psKey -Name EnableScriptBlockLogging).EnableScriptBlockLogging)
L '  NOTE: 4104 is what recovers the plaintext of -EncodedCommand.'

# ---------- 0-5  log sizes + disabled channels ----------
L ''
L '--- 0-5 log sizes and channels ---'
$sizes = [ordered]@{
    'Security'                                  = 104857600   # 100 MB
    'System'                                    = 67108864    #  64 MB
    'Microsoft-Windows-Sysmon/Operational'      = 134217728   # 128 MB
    'Microsoft-Windows-PowerShell/Operational'  = 67108864    #  64 MB
}
foreach ($n in $sizes.Keys) {
    & wevtutil.exe sl $n /ms:$($sizes[$n]) 2>&1 | Out-Null
    $gl = (& wevtutil.exe gl $n 2>&1 | Select-String -Pattern 'maxSize' | Select-Object -First 1)
    L ('  ' + $n.PadRight(42) + ' ' + ("$gl".Trim()))
}
$tsChan = 'Microsoft-Windows-TaskScheduler/Operational'
& wevtutil.exe sl $tsChan /e:true 2>&1 | Out-Null
$tsState = (& wevtutil.exe gl $tsChan 2>&1 | Select-String -Pattern 'enabled:' | Select-Object -First 1)
L ('  enabled channel ' + $tsChan + ' -> ' + ("$tsState".Trim()))

# ---------- 0-6  sysmon config backup ----------
L ''
L '--- 0-6 sysmon config backup ---'
$cfg = 'C:\Tools\DFIR\sysmonconfig.xml'
Copy-Item $cfg (Join-Path $out 'sysmonconfig.baseline.xml') -Force
L ('  baseline copy: sysmonconfig.baseline.xml (' + (Get-Item $cfg).Length + ' bytes)')

# ---------- 0-7  sysmon EFFECTIVENESS probe ----------
L ''
L '--- 0-7 sysmon effectiveness probe (tag present != rule present) ---'
$raw = Get-Content $cfg -Raw
foreach ($sec in @('ProcessAccess', 'FileCreate', 'RegistryEvent', 'FileCreateStreamHash', 'DnsQuery', 'WmiEvent', 'CreateRemoteThread')) {
    $m = [regex]::Match($raw, '(?s)<' + $sec + ' ([^>]*?)>(.*?)</' + $sec + '>')
    if (-not $m.Success) { L ('  ' + $sec.PadRight(22) + ' : section missing'); continue }
    $attr = $m.Groups[1].Value.Trim()
    $rules = ([regex]::Matches($m.Groups[2].Value, '<(TargetImage|TargetObject|TargetFilename|Image|EventType|Query)\b')).Count
    $verdict = if ($attr -match 'include' -and $rules -eq 0) { 'INERT (include + 0 rules => nothing logged)' } else { 'effective' }
    L ('  ' + $sec.PadRight(22) + ' : ' + $attr.PadRight(22) + ' rules=' + $rules.ToString().PadLeft(3) + '  ' + $verdict)
}
$svc = Get-Service -Name 'Sysmon*' -ErrorAction SilentlyContinue
foreach ($s in $svc) { L ('  service ' + $s.Name + ' = ' + $s.Status) }

# ---------- 0-8  after snapshot ----------
L ''
L '--- 0-8 AFTER: setting per GUID ---'
$csvAfter = & auditpol.exe /get /category:* /r 2>&1
[IO.File]::WriteAllLines("$out\auditpol_after.csv", $csvAfter, $utf8)
foreach ($k in $guids.Keys) {
    $hit = $csvAfter | Where-Object { $_ -like ('*' + $guids[$k] + '*') } | Select-Object -First 1
    $setting = ''
    if ($hit) { $setting = ($hit -split ',' | Select-Object -Last 3) -join '|' }
    L ('  ' + $k.PadRight(28) + ' => ' + $setting)
}

L ''
L 'DONE harden'
Write-Host 'DONE harden -> read C:\Tools\DFIR\day1b\harden_log.txt'

# vm_day2_analyze.ps1 -- Day 2: turn the captured artifacts into CSVs with the EZ tool chain.
#
# Three hard-won rules baked in here:
#   1. RECmd picks the hive TYPE from the hive header's EMBEDDED base name
#      ("ntuser.dat" -> NtUser, "SYSTEM" -> System). A hive made by `reg save` to a
#      custom file name keeps a non-standard embedded name and is typed "Other", so
#      EVERY batch rule is silently skipped. We rewrite the 64-byte name field at
#      base-block offset 0x30.
#   2. RECmd batch (.reb) files MUST use LF line endings. With CRLF the YAML parser
#      keeps a trailing \r inside KeyPath, so the regex can never match.
#   3. AmcacheParser aborts on a dirty hive unless --nl true is given.
#
# ASCII ONLY.

$ErrorActionPreference = 'Continue'
$base  = 'C:\Tools\DFIR\day2'
$snap  = Join-Path $base 'snapshot'
$hives = Join-Path $base 'hives'
$out   = Join-Path $base 'toolout'
$batch = Join-Path $base 'batch'
Remove-Item $out -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item $batch -Recurse -Force -ErrorAction SilentlyContinue
foreach ($d in @($out, $batch)) { New-Item -ItemType Directory -Force -Path $d | Out-Null }
$log = Join-Path $out 'analyze_log.txt'
$utf8 = New-Object System.Text.UTF8Encoding($false)
[IO.File]::WriteAllText($log, '', $utf8)
function L([string]$m) { [IO.File]::AppendAllText($log, $m + "`r`n", $utf8) }
function Show-Message([string]$m) { Write-Host $m }

$EZ = 'C:\Tools\DFIR\EZTools\net9'
$script:failures = 0

function Set-HiveBaseName($path, $name) {
    $b = [IO.File]::ReadAllBytes($path)
    for ($i = 0; $i -lt 64; $i++) { $b[0x30 + $i] = 0 }
    $nb = [Text.Encoding]::Unicode.GetBytes($name)
    [Array]::Copy($nb, 0, $b, 0x30, $nb.Length)
    [IO.File]::WriteAllBytes($path, $b)
    L ('  base name patched -> ' + $name + '  (' + $path + ')')
}

# RECmd batch with LF endings (NOT CRLF)
function WriteRebLf($path, $desc, $hiveType, $category, $keyPath) {
    $content = @(
        "Description: $desc",
        'Author: hitcon-sprint',
        'Version: 1',
        ('Id: ' + [guid]::NewGuid().ToString()),
        'Keys:',
        '    -',
        ('        Description: ' + $desc),
        ('        HiveType: ' + $hiveType),
        ('        Category: ' + $category),
        ('        KeyPath: ' + $keyPath),
        '        Recursive: True',   # capital T: YamlDotNet is case-sensitive on bools
        '        Comment:'
    ) -join "`n"
    [IO.File]::WriteAllText($path, $content + "`n", $utf8)
}

function RunTool($name, $exe, $argList, $csvFile) {
    L ''
    L ('--- ' + $name + ' ---')
    L ('  cmd: ' + $exe + ' ' + ($argList -join ' '))
    $sw = [Diagnostics.Stopwatch]::StartNew()
    $res = & $exe @argList 2>&1 | Out-String
    $sw.Stop()
    L ('  exit=' + $LASTEXITCODE + ' elapsed=' + [math]::Round($sw.Elapsed.TotalSeconds, 1) + 's')
    if ($LASTEXITCODE -ne 0) { $script:failures++ }
    foreach ($line in ($res -split "`n")) { if ($line.Trim()) { L ('  | ' + $line.Trim()) } }
    if ($csvFile) {
        $f = Join-Path $out $csvFile
        if (Test-Path $f) {
            $rows = [math]::Max(0, ((Get-Content $f | Measure-Object -Line).Lines - 1))
            L ('  output ' + $csvFile + ' rows=' + $rows + ' size=' + [math]::Round((Get-Item $f).Length / 1KB, 1) + ' KB')
        } else { L ('  output ' + $csvFile + ' MISSING'); $script:failures++ }
    }
}

L ('=== Day 2 analysis v3  UTC=' + [DateTime]::UtcNow.ToString('yyyy-MM-dd HH:mm:ss') + 'Z ===')

# 0. make the fixture hives self-identifying
Set-HiveBaseName (Join-Path $hives 'SYSTEM_copy.hive') 'SYSTEM'
Set-HiveBaseName (Join-Path $hives 'NTUSER_fixture.hive') 'NTUSER.DAT'

# 1. batch files (LF)
# KeyPath is matched with SINGLE backslashes (empirically: doubled backslashes never match).
WriteRebLf (Join-Path $batch 'day2_usbstore.reb')     'USBSTOR devices'    'System' 'USB'        'CurrentControlSet\Enum\USBSTOR'
WriteRebLf (Join-Path $batch 'day2_userassist.reb')   'UserAssist counts'  'NtUser' 'UserAssist' 'Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist'
WriteRebLf (Join-Path $batch 'day2_consentstore.reb') 'ConsentStore usage' 'NtUser' 'Consent'    'Software\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore'

# 2. Prefetch
RunTool 'PECmd' "$EZ\PECmd.exe" @('-q', '-d', $snap, '--csv', $out, '--csvf', 'prefetch.csv') 'prefetch.csv'

# 3. Amcache
RunTool 'AmcacheParser' "$EZ\AmcacheParser.exe" @('-f', (Join-Path $snap 'Amcache.hve'), '-i', '--nl', 'true', '--csv', $out, '--csvf', 'amcache.csv') 'amcache_UnassociatedFileEntries.csv'

# 4. Shimcache
RunTool 'AppCompatCacheParser' "$EZ\AppCompatCacheParser.exe" @('-f', (Join-Path $hives 'SYSTEM_copy.hive'), '--csv', $out, '--csvf', 'shimcache.csv') 'shimcache.csv'

# 5. USBSTOR (RECmd batch, type System)
RunTool 'RECmd-USBSTOR' "$EZ\RECmd\RECmd.exe" @('-f', (Join-Path $hives 'SYSTEM_copy.hive'), '--bn', (Join-Path $batch 'day2_usbstore.reb'), '--csv', $out, '--csvf', 'usbstore.csv', '--nl', 'true') 'usbstore.csv'

# 6. UserAssist (RECmd batch, type NtUser)
RunTool 'RECmd-UserAssist' "$EZ\RECmd\RECmd.exe" @('-f', (Join-Path $hives 'NTUSER_fixture.hive'), '--bn', (Join-Path $batch 'day2_userassist.reb'), '--csv', $out, '--csvf', 'userassist_raw.csv', '--nl', 'true') 'userassist_raw.csv'

# 7. ConsentStore (RECmd batch, type NtUser)
RunTool 'RECmd-ConsentStore' "$EZ\RECmd\RECmd.exe" @('-f', (Join-Path $hives 'NTUSER_fixture.hive'), '--bn', (Join-Path $batch 'day2_consentstore.reb'), '--csv', $out, '--csvf', 'consentstore_raw.csv', '--nl', 'true') 'consentstore_raw.csv'

L ''
L '--- produced files ---'
Get-ChildItem $out | Sort-Object Name | ForEach-Object { L ('  ' + $_.Name.PadRight(34) + ' ' + [math]::Round($_.Length / 1KB, 1) + ' KB') }

L ''
L ('DONE analyze failures=' + $script:failures)
Show-Message ('DONE analyze failures=' + $script:failures + ' -> read C:\Tools\DFIR\day2\toolout\analyze_log.txt')
if ($script:failures -gt 0) { exit 1 }

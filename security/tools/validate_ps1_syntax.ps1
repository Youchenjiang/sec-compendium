# validate_ps1_syntax.ps1 -- parse-check guest PowerShell scripts BEFORE uploading.
#
# WHY THIS EXISTS
#   The round trip to debug a broken .ps1 inside the VM costs minutes: upload,
#   run, time out, kill leftover processes, read the retrieved output. Two
#   failures made that obvious:
#     - a missing closing brace in a foreach loop (ParserError, 4 minutes lost)
#     - a function named `Do`, which PowerShell parses as the do/while keyword
#   Both are caught instantly by the host's own parser, so check first.
#
# USAGE (run from the repo root; the host is Windows)
#   powershell -NoProfile -ExecutionPolicy Bypass -File security/tools/validate_ps1_syntax.ps1 security/tools/vm_day1b_*.ps1
#
# Only parses -- it never executes the scripts, so it is safe for anything that
# touches production or the VM. Exit code is the number of files with errors.
param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Files)

if (-not $Files -or $Files.Count -eq 0) {
    Write-Host 'usage: validate_ps1_syntax.ps1 <file.ps1> [more.ps1 ...]'
    exit 0
}

$bad = 0
foreach ($f in $Files) {
    if (-not (Test-Path $f)) { Write-Host "MISSING: $f"; $bad++; continue }
    $err = $null; $tok = $null
    [void][System.Management.Automation.Language.Parser]::ParseFile((Resolve-Path $f).Path, [ref]$tok, [ref]$err)
    if ($err -and $err.Count) {
        Write-Host "SYNTAX ERRORS in $f : $($err.Count)"
        $err | Select-Object -First 12 | ForEach-Object {
            Write-Host ('   line ' + $_.Extent.StartLineNumber + ' col ' + $_.Extent.StartColumnNumber + ' : ' + $_.Message)
        }
        $bad++
    } else {
        Write-Host "PARSE OK: $f"
    }
}
Write-Host "---- files with errors: $bad ----"
exit $bad

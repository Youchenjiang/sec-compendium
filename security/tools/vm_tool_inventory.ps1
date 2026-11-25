# vm_tool_inventory.ps1 - Windows lab VM toolchain inventory
# Purpose: confirm which DFIR / reverse-engineering tools a sandbox VM actually has.
# Run from the host via: vmrun runProgramInGuest cmd /c "powershell -File C:\Windows\Temp\inv.ps1"
# Output is redirected to a file and copied back. Read-only: nothing is installed or changed.
#
# NOTE: keep every string ASCII-only. The guest console codepage (CP950/CP437) corrupts
# non-ASCII output when stdout is redirected by cmd.exe.

$ErrorActionPreference = 'SilentlyContinue'

'### SYSTEM ###'
"Hostname     : $env:COMPUTERNAME"
"User         : $env:USERNAME"
$os = Get-CimInstance Win32_OperatingSystem
"OS           : $($os.Caption) (Build $($os.BuildNumber))"
try {
    $princ = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    "IsAdmin      : $($princ.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator))"
} catch { "IsAdmin      : (query failed)" }
"PSVersion    : $($PSVersionTable.PSVersion)"
"Architecture : $env:PROCESSOR_ARCHITECTURE"

''
'### TOOLS ON PATH ###'
$tools = @(
    'chainsaw','hayabusa','EvtxECmd','MFTECmd','PECmd','AmcacheParser','RECmd',
    'AppCompatCacheParser','SrumECmd','JLECmd','LECmd','SBECmd','RBCmd','EvtxDump',
    'vol.py','vol','volatility3','yara','yara64','capa','floss','die','diec',
    'ghidraRun','ghidra','x64dbg','ida64','dnSpy','pestudio','HxD','ProcessHacker',
    'tshark','dumpcap','python','python3','py','dotnet','java','git','7z','strings',
    'procdump','psexec','log2timeline.py','psort.py','autoruns','sigcheck','rip.exe'
)
foreach ($t in $tools) {
    $c = Get-Command $t -ErrorAction SilentlyContinue
    if ($c) { '{0,-22} FOUND  {1}' -f $t, $c.Source }
}

''
'### KEY DIRECTORIES ###'
foreach ($d in @('C:\Tools', 'C:\ProgramData\chocolatey\bin', 'C:\Program Files\SysinternalsSuite',
                 "$env:USERPROFILE\Tools", "$env:USERPROFILE\Desktop", 'C:\Program Files\Ghidra',
                 'C:\Program Files\Wireshark', 'C:\Program Files\VMware', 'C:\Python313',
                 'C:\Program Files\OpenJDK', 'C:\Program Files\dotnet')) {
    if (Test-Path $d) { "EXISTS  $d" } else { "MISSING $d" }
}

''
'### C:\Tools (full listing) ###'
Get-ChildItem 'C:\Tools' -ErrorAction SilentlyContinue | Sort-Object Name | Select-Object -ExpandProperty Name

''
'### DFIR TOOL HUNT (recursive, name match) ###'
$patterns = @('chainsaw*','hayabusa*','*EvtxECmd*','*MFTECmd*','*PECmd*','*AmcacheParser*',
              '*RECmd*','*Evtx*.exe','volatility*','vol.py','yara*','*capa*','*ghidra*',
              '*sysmon*','*regripper*','*SrumECmd*','*JLECmd*','*TimelineExplorer*')
$roots = @('C:\Tools', 'C:\Program Files', 'C:\Program Files (x86)', "$env:USERPROFILE", 'C:\ProgramData\chocolatey\bin')
foreach ($r in $roots) {
    foreach ($p in $patterns) {
        Get-ChildItem -Path $r -Filter $p -Recurse -Depth 3 -ErrorAction SilentlyContinue |
            Select-Object -First 4 -ExpandProperty FullName
    }
}

''
'### INSTALLED PROGRAMS (filtered) ###'
$keys = @(
    'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*',
    'HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*'
)
Get-ItemProperty $keys -ErrorAction SilentlyContinue |
    Where-Object { $_.DisplayName -match 'sysmon|chocolatey|python|ghidra|wireshark|volatility|7-zip|ida|x64dbg|dnspy|yara|capa|notepad|visual studio|debugging tools' } |
    Select-Object -ExpandProperty DisplayName -Unique | Sort-Object

''
'### SERVICES (key names) ###'
Get-Service -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -match 'Sysmon|Windbg|VGAuth|VMTools|WinRM|ssh|EventLog' } |
    ForEach-Object { '{0,-24} {1}' -f $_.Name, $_.Status }

''
'### SYSMON CONFIG ###'
foreach ($p in @('C:\Windows\sysmon.xml','C:\Windows\sysmonconfig.xml','C:\Tools\sysmon.xml',
                 "$env:USERPROFILE\sysmon.xml","$env:USERPROFILE\Downloads\sysmonconfig.xml")) {
    if (Test-Path $p) { "EXISTS  $p ($((Get-Item $p).Length) bytes)" }
}

''
'### NETWORK ###'
try {
    $dns = [System.Net.Dns]::GetHostAddresses('github.com')
    "DNS github.com : $($dns[0].IPAddressToString)"
} catch { 'DNS github.com : FAIL' }
foreach ($hp in $([pscustomobject]@{H='github.com';P=443}, $([pscustomobject]@{H='pypi.org';P=443}, $([pscustomobject]@{H='1.1.1.1';P=53})))) {
    $c = New-Object System.Net.Sockets.TcpClient
    try {
        $ok = $c.ConnectAsync($hp.H, $hp.P).Wait(4000)
        'TCP {0}:{1} : {2}' -f $hp.H, $hp.P, $ok
    } catch { 'TCP {0}:{1} : FAIL' -f $hp.H, $hp.P } finally { $c.Close() }
}

''
'### PYTHON ###'
$py = (Get-Command python -ErrorAction SilentlyContinue)
if ($py) {
    "python exe : $($py.Source)"
    "version    : $(& $py.Source --version 2>&1)"
    "pip count  : $((& $py.Source -m pip list 2>$null | Measure-Object).Count)"
    foreach ($m in @('pefile','yara','Evtx','dissect','volatility3','capstone','lief','pandas','regipy')) {
        $r = & $py.Source -c "import importlib.util,sys; sys.stdout.write('OK' if importlib.util.find_spec('$m') else 'MISS')" 2>$null
        '{0,-14} {1}' -f $m, $r
    }
} else { '(python not on PATH)' }

''
'### RESOURCES ###'
Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" | ForEach-Object {
    '{0} free {1} GB / total {2} GB' -f $_.DeviceID, [math]::Round($_.FreeSpace / 1GB, 1), [math]::Round($_.Size / 1GB, 1)
}
'RAM total {0} GB' -f [math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 1)

''
'### DONE ###'

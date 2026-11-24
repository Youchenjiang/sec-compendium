[CmdletBinding()]
param(
    [ValidateSet('Status', 'Apply', 'Rollback')]
    [string]$Mode = 'Status',
    [int]$ProcessId,
    [string]$C2IP,
    [string]$TaskName,
    [string]$ServiceName,
    [string]$RunKeyPath,
    [string]$RunValueName,
    [string]$StatePath = "$env:ProgramData\HITCON-Day6\containment-state.json"
)

$ErrorActionPreference = 'Stop'
$FirewallRuleName = if ($C2IP) { "HITCON-Day6-Block-$C2IP" } else { 'HITCON-Day6-Block-Unset' }
$ServiceFilterName = if ($ServiceName) { $ServiceName.Replace("'", "''") } else { $null }

function Write-ContainmentLog([string]$Message) {
    "{0}`t{1}" -f ([DateTime]::UtcNow.ToString('o')), $Message
}

function Get-State {
    if (Test-Path -LiteralPath $StatePath) {
        return Get-Content -LiteralPath $StatePath -Raw | ConvertFrom-Json
    }
    return $null
}

function Save-State([hashtable]$State) {
    $parent = Split-Path -Parent $StatePath
    if ($parent) { New-Item -ItemType Directory -Force -Path $parent | Out-Null }
    $State | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $StatePath -Encoding UTF8
}

function Get-RunValueSnapshot([string]$Path, [string]$Name) {
    $item = Get-ItemProperty -Path $Path -ErrorAction SilentlyContinue
    if (-not $item) {
        return @{ Exists = $false; Data = $null }
    }
    $property = $item.PSObject.Properties[$Name]
    if ($null -eq $property) {
        return @{ Exists = $false; Data = $null }
    }
    return @{ Exists = $true; Data = [string]$property.Value }
}

function Show-Status {
    if ($ProcessId) {
        $proc = Get-Process -Id $ProcessId -ErrorAction SilentlyContinue
        Write-ContainmentLog "process id=$ProcessId present=$([bool]$proc)"
    }
    if ($C2IP) {
        $rule = Get-NetFirewallRule -DisplayName $FirewallRuleName -ErrorAction SilentlyContinue
        Write-ContainmentLog "outbound_block ip=$C2IP present=$([bool]$rule)"
    }
    if ($TaskName) {
        $task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
        Write-ContainmentLog "task name=$TaskName present=$([bool]$task) state=$($task.State)"
    }
    if ($ServiceName) {
        $service = Get-CimInstance Win32_Service -Filter "Name='$ServiceFilterName'" -ErrorAction SilentlyContinue
        if ($service) {
            Write-ContainmentLog "service name=$ServiceName present=True state=$($service.State) start_mode=$($service.StartMode)"
        } else {
            Write-ContainmentLog "service name=$ServiceName present=False"
        }
    }
    if ($RunKeyPath -and $RunValueName) {
        $run = Get-RunValueSnapshot -Path $RunKeyPath -Name $RunValueName
        Write-ContainmentLog "run_value path=$RunKeyPath name=$RunValueName present=$($run.Exists)"
    }
}

function Assert-ApplyScope {
    if (-not ($ProcessId -or $C2IP -or $TaskName -or $ServiceName -or ($RunKeyPath -and $RunValueName))) {
        throw 'Apply requires at least one explicit scope: ProcessId, C2IP, TaskName, ServiceName, or RunKeyPath+RunValueName.'
    }
    if (($RunKeyPath -and -not $RunValueName) -or ($RunValueName -and -not $RunKeyPath)) {
        throw 'RunKeyPath and RunValueName must be supplied together.'
    }
}

function New-PristineState {
    $state = @{
        FirewallAdded = $false
        TaskExisted = $false
        TaskWasEnabled = $false
        ServiceExisted = $false
        ServiceStartMode = $null
        ServiceWasRunning = $false
        RunValueExisted = $false
        RunValueData = $null
        ProcessId = $ProcessId
        C2IP = $C2IP
        TaskName = $TaskName
        ServiceName = $ServiceName
        RunKeyPath = $RunKeyPath
        RunValueName = $RunValueName
    }

    if ($TaskName) {
        $task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
        if ($task) {
            $state.TaskExisted = $true
            $state.TaskWasEnabled = $task.State -ne 'Disabled'
        }
    }

    if ($ServiceName) {
        $service = Get-CimInstance Win32_Service -Filter "Name='$ServiceFilterName'" -ErrorAction SilentlyContinue
        if ($service) {
            $state.ServiceExisted = $true
            $state.ServiceStartMode = [string]$service.StartMode
            $state.ServiceWasRunning = [string]$service.State -eq 'Running'
        }
    }

    if ($RunKeyPath -and $RunValueName) {
        $run = Get-RunValueSnapshot -Path $RunKeyPath -Name $RunValueName
        if ($run.Exists) {
            $state.RunValueExisted = $true
            $state.RunValueData = $run.Data
        }
    }
    return $state
}

function Assert-StateScope($State) {
    $requestedScope = @{
        ProcessId = $ProcessId
        C2IP = $C2IP
        TaskName = $TaskName
        ServiceName = $ServiceName
        RunKeyPath = $RunKeyPath
        RunValueName = $RunValueName
    }
    foreach ($name in $requestedScope.Keys) {
        if ([string]$State.$name -ne [string]$requestedScope[$name]) {
            throw "Existing rollback state scope mismatch for $name. Use the original scope or a different StatePath."
        }
    }
}

function Invoke-FirewallContainment($State, [bool]$FreshApply) {
    $existing = Get-NetFirewallRule -DisplayName $FirewallRuleName -ErrorAction SilentlyContinue
    if (-not $existing) {
        New-NetFirewallRule -DisplayName $FirewallRuleName -Direction Outbound -Action Block -RemoteAddress $C2IP | Out-Null
        if ($FreshApply) {
            $State.FirewallAdded = $true
            Save-State $State
        }
        Write-ContainmentLog "firewall added outbound-only ip=$C2IP rollback=remove script-owned rule"
    } else {
        Write-ContainmentLog "firewall unchanged exact rule already exists"
    }
}

function Invoke-TaskContainment {
    $task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if (-not $task) { return }
    if ($task.State -ne 'Disabled') {
        Disable-ScheduledTask -TaskName $TaskName | Out-Null
        Write-ContainmentLog "task disabled name=$TaskName rollback=restore original enabled state"
    } else {
        Write-ContainmentLog "task unchanged name=$TaskName already disabled"
    }
}

function Invoke-ServiceContainment {
    $service = Get-CimInstance Win32_Service -Filter "Name='$ServiceFilterName'" -ErrorAction SilentlyContinue
    if (-not $service) { return }
    if ([string]$service.State -eq 'Running') {
        Stop-Service -Name $ServiceName -ErrorAction Stop
        Write-ContainmentLog "service stopped name=$ServiceName"
    }
    $service = Get-CimInstance Win32_Service -Filter "Name='$ServiceFilterName'" -ErrorAction SilentlyContinue
    if ([string]$service.StartMode -ne 'Disabled') {
        Set-Service -Name $ServiceName -StartupType Disabled
        Write-ContainmentLog "service disabled name=$ServiceName rollback=restore original start mode"
    } else {
        Write-ContainmentLog "service unchanged name=$ServiceName already disabled"
    }
}

function Invoke-RunValueContainment {
    $run = Get-RunValueSnapshot -Path $RunKeyPath -Name $RunValueName
    if ($run.Exists) {
        Remove-ItemProperty -Path $RunKeyPath -Name $RunValueName
        Write-ContainmentLog "Run value removed path=$RunKeyPath name=$RunValueName rollback=restore exact data"
    } else {
        Write-ContainmentLog "Run value unchanged path=$RunKeyPath name=$RunValueName already absent"
    }
}

function Invoke-ProcessContainment {
    $proc = Get-Process -Id $ProcessId -ErrorAction SilentlyContinue
    if ($proc) {
        # Stop-Process without -Force is the least aggressive generic process action available here.
        Stop-Process -Id $ProcessId
        Start-Sleep -Seconds 1
        Write-ContainmentLog "process stop requested id=$ProcessId"
    } else {
        Write-ContainmentLog "process unchanged id=$ProcessId already absent"
    }
}

function Apply-Containment {
    Assert-ApplyScope

    $existingState = Get-State
    $freshApply = -not $existingState

    if ($freshApply) {
        $state = New-PristineState

        # Save pristine rollback metadata before the first mutation. Repeated
        # Apply calls reuse this state instead of overwriting it with an
        # already-contained snapshot.
        Save-State $state
    } else {
        $state = $existingState
        Assert-StateScope $state
        Write-ContainmentLog "apply idempotent: existing rollback state preserved path=$StatePath"
    }

    if ($C2IP) { Invoke-FirewallContainment $state $freshApply }
    if ($TaskName) { Invoke-TaskContainment }
    if ($ServiceName) { Invoke-ServiceContainment }
    if ($RunKeyPath -and $RunValueName) { Invoke-RunValueContainment }
    if ($ProcessId) { Invoke-ProcessContainment }
}

function Restore-ServiceState($State) {
    $startupType = switch ([string]$State.ServiceStartMode) {
        'Auto' { 'Automatic' }
        'Automatic' { 'Automatic' }
        'Manual' { 'Manual' }
        'Disabled' { 'Disabled' }
        default { $null }
    }
    if ($startupType) {
        Set-Service -Name $State.ServiceName -StartupType $startupType -ErrorAction SilentlyContinue
        Write-ContainmentLog "service rollback start_mode=$startupType name=$($State.ServiceName)"
    }
    if ($State.ServiceWasRunning) {
        Start-Service -Name $State.ServiceName -ErrorAction SilentlyContinue
        Write-ContainmentLog "service rollback running-state requested name=$($State.ServiceName)"
    }
}

function Restore-RunValue($State) {
    if (-not (Test-Path -LiteralPath $State.RunKeyPath)) { New-Item -Path $State.RunKeyPath -Force | Out-Null }
    Set-ItemProperty -Path $State.RunKeyPath -Name $State.RunValueName -Value $State.RunValueData
    Write-ContainmentLog "Run value rollback restored name=$($State.RunValueName)"
}

function Rollback-Containment {
    $state = Get-State
    if (-not $state) {
        Write-ContainmentLog "rollback no saved state"
        return
    }

    if ($state.FirewallAdded -and $state.C2IP) {
        Get-NetFirewallRule -DisplayName "HITCON-Day6-Block-$($state.C2IP)" -ErrorAction SilentlyContinue |
            Remove-NetFirewallRule -ErrorAction SilentlyContinue
        Write-ContainmentLog "firewall rollback complete ip=$($state.C2IP)"
    }

    if ($state.TaskWasEnabled -and $state.TaskName) {
        Enable-ScheduledTask -TaskName $state.TaskName -ErrorAction SilentlyContinue | Out-Null
        Write-ContainmentLog "task rollback enabled name=$($state.TaskName)"
    }

    if ($state.ServiceExisted -and $state.ServiceName) { Restore-ServiceState $state }

    if ($state.RunValueExisted -and $state.RunKeyPath -and $state.RunValueName) { Restore-RunValue $state }

    Remove-Item -LiteralPath $StatePath -Force -ErrorAction SilentlyContinue
    Write-ContainmentLog "rollback state cleared path=$StatePath"
}

switch ($Mode) {
    'Status'   { Show-Status }
    'Apply'    { Apply-Containment }
    'Rollback' { Rollback-Containment }
}

[CmdletBinding()]
param(
    [ValidateSet('Status', 'Apply', 'Rollback')]
    [string]$Mode = 'Status',
    [int]$ProcessId,
    [string]$C2IP,
    [string]$TaskName,
    [string]$RunKeyPath,
    [string]$RunValueName,
    [string]$StatePath = "$env:ProgramData\HITCON-Day6\containment-state.json"
)

$ErrorActionPreference = 'Stop'
$FirewallRuleName = if ($C2IP) { "HITCON-Day6-Block-$C2IP" } else { 'HITCON-Day6-Block-Unset' }

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
    if ($RunKeyPath -and $RunValueName) {
        $value = Get-ItemPropertyValue -Path $RunKeyPath -Name $RunValueName -ErrorAction SilentlyContinue
        Write-ContainmentLog "run_value path=$RunKeyPath name=$RunValueName present=$($null -ne $value)"
    }
}

function Apply-Containment {
    if (-not ($ProcessId -or $C2IP -or $TaskName -or ($RunKeyPath -and $RunValueName))) {
        throw 'Apply requires at least one explicit scope: ProcessId, C2IP, TaskName, or RunKeyPath+RunValueName.'
    }
    if (($RunKeyPath -and -not $RunValueName) -or ($RunValueName -and -not $RunKeyPath)) {
        throw 'RunKeyPath and RunValueName must be supplied together.'
    }

    $state = @{
        FirewallAdded = $false
        TaskWasEnabled = $false
        RunValueExisted = $false
        RunValueData = $null
        ProcessId = $ProcessId
        C2IP = $C2IP
        TaskName = $TaskName
        RunKeyPath = $RunKeyPath
        RunValueName = $RunValueName
    }

    if ($C2IP) {
        $existing = Get-NetFirewallRule -DisplayName $FirewallRuleName -ErrorAction SilentlyContinue
        if (-not $existing) {
            New-NetFirewallRule -DisplayName $FirewallRuleName -Direction Outbound -Action Block -RemoteAddress $C2IP | Out-Null
            $state.FirewallAdded = $true
            Write-ContainmentLog "firewall added outbound-only ip=$C2IP rollback=remove script-owned rule"
        } else {
            Write-ContainmentLog "firewall unchanged exact rule already exists"
        }
    }

    if ($TaskName) {
        $task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
        if ($task) {
            $state.TaskWasEnabled = $task.State -ne 'Disabled'
            if ($state.TaskWasEnabled) { Disable-ScheduledTask -TaskName $TaskName | Out-Null }
            Write-ContainmentLog "task disabled name=$TaskName rollback=restore previous enabled state"
        }
    }

    if ($RunKeyPath -and $RunValueName) {
        $value = Get-ItemPropertyValue -Path $RunKeyPath -Name $RunValueName -ErrorAction SilentlyContinue
        if ($null -ne $value) {
            $state.RunValueExisted = $true
            $state.RunValueData = [string]$value
            Remove-ItemProperty -Path $RunKeyPath -Name $RunValueName
            Write-ContainmentLog "Run value removed path=$RunKeyPath name=$RunValueName rollback=restore exact data"
        }
    }

    # Persist rollback metadata before touching the target process. A process
    # stop can fail independently; firewall/task/RunKey rollback must remain
    # recoverable even if that final action throws.
    Save-State $state

    if ($ProcessId) {
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

    if ($state.RunValueExisted -and $state.RunKeyPath -and $state.RunValueName) {
        if (-not (Test-Path -LiteralPath $state.RunKeyPath)) { New-Item -Path $state.RunKeyPath -Force | Out-Null }
        Set-ItemProperty -Path $state.RunKeyPath -Name $state.RunValueName -Value $state.RunValueData
        Write-ContainmentLog "Run value rollback restored name=$($state.RunValueName)"
    }
}

switch ($Mode) {
    'Status'   { Show-Status }
    'Apply'    { Apply-Containment }
    'Rollback' { Rollback-Containment }
}

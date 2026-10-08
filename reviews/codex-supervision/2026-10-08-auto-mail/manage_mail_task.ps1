param([ValidateSet('Install','Status','Stop','Resume','Run')][string]$Action = 'Status')
$ErrorActionPreference = 'Stop'
$ProjectRoot = (Get-Item -LiteralPath $PSScriptRoot).Parent.Parent.Parent.FullName
if ((Split-Path -Leaf $ProjectRoot) -ne 'Animation-Model-Training') { throw 'Unexpected project path' }
$ConfigPath = Join-Path $PSScriptRoot 'config.json'
$Config = Get-Content -LiteralPath $ConfigPath -Encoding UTF8 -Raw | ConvertFrom-Json
if ($Config.project -ne $ProjectRoot -or $Config.interval_seconds -ne 600) { throw 'Wrong project or cadence' }
$TaskName = $Config.task_name
$PythonPath = Join-Path $ProjectRoot '.venv\Scripts\python.exe'
$WorkerPath = Join-Path $PSScriptRoot 'mail_watch.py'
$RunnerPath = Join-Path $PSScriptRoot 'run_mail_task.ps1'
$PowerShellPath = Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'
$TaskArguments = '-NoLogo -NoProfile -NonInteractive -WindowStyle Hidden -File "' + $RunnerPath + '"'
$Existing = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($Existing) {
    $Actions = @($Existing.Actions)
    if ($Actions.Count -ne 1 -or $Actions[0].Execute -ne $PowerShellPath -or $Actions[0].Arguments -ne $TaskArguments) {
        throw 'Task name belongs to another configuration; refusing to overwrite or control it'
    }
}
switch ($Action) {
    'Install' {
        if (-not $Existing) {
            $TaskAction = New-ScheduledTaskAction -Execute $PowerShellPath -Argument $TaskArguments -WorkingDirectory $ProjectRoot
            $Trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(10) -RepetitionInterval (New-TimeSpan -Minutes 10)
            $TaskSettings = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 2) -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
            $CurrentUser = [Security.Principal.WindowsIdentity]::GetCurrent().Name
            $Principal = New-ScheduledTaskPrincipal -UserId $CurrentUser -LogonType Interactive -RunLevel Limited
            Register-ScheduledTask -TaskName $TaskName -Action $TaskAction -Trigger $Trigger -Settings $TaskSettings -Principal $Principal -Description 'Every 10 minutes, capture Claude mail and queue bounded review in the existing Codex thread.' | Out-Null
        }
    }
    'Stop' {
        & $PythonPath -B $WorkerPath stop
        if ($LASTEXITCODE -ne 0) { throw 'Stop control failed' }
        if ($Existing) { Disable-ScheduledTask -TaskName $TaskName | Out-Null }
    }
    'Resume' {
        if (-not $Existing) { throw 'Task is not installed' }
        & $PythonPath -B $WorkerPath resume
        if ($LASTEXITCODE -ne 0) { throw 'Resume control failed' }
        Enable-ScheduledTask -TaskName $TaskName | Out-Null
    }
    'Run' {
        if (-not $Existing) { throw 'Task is not installed' }
        Start-ScheduledTask -TaskName $TaskName
    }
}
$Task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($Task) {
    $Info = Get-ScheduledTaskInfo -TaskName $TaskName
    [PSCustomObject]@{name=$TaskName;state=[string]$Task.State;interval=$Task.Triggers[0].Repetition.Interval;last_run=$Info.LastRunTime;next_run=$Info.NextRunTime;last_result=$Info.LastTaskResult;logon=$Task.Principal.LogonType;run_level=$Task.Principal.RunLevel} | ConvertTo-Json -Compress
} else {
    [PSCustomObject]@{name=$TaskName;state='NOT_INSTALLED'} | ConvertTo-Json -Compress
}

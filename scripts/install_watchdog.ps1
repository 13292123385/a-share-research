$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$pythonExe = (& python -c 'import sys; print(sys.executable)').Trim()
$watchdogFile = Join-Path $PSScriptRoot 'watchdog_service.py'
$pythonWindowless = Join-Path (Split-Path -Parent $pythonExe) 'pythonw.exe'
$taskAction = New-ScheduledTaskAction -Execute $pythonWindowless -Argument ('"' + $watchdogFile + '"') -WorkingDirectory $repoRoot
$taskTriggers = @()
foreach ($taskTime in @('11:30','11:40','11:50','12:00','12:10','12:20','12:30','12:40','12:50','15:00','15:10','15:20','15:30','15:40','15:50','16:00','16:30','17:00','18:15','21:15')) {
    $taskTriggers += New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday -At $taskTime
}
$taskTriggers += New-ScheduledTaskTrigger -AtLogOn
$taskSettings = New-ScheduledTaskSettingsSet -StartWhenAvailable -MultipleInstances IgnoreNew -ExecutionTimeLimit ([TimeSpan]::Zero) -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
$taskUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
$taskPrincipal = New-ScheduledTaskPrincipal -UserId $taskUser -LogonType Interactive -RunLevel Limited
try {
    Register-ScheduledTask -TaskName 'A-share-research closing watchdog' -Action $taskAction -Trigger $taskTriggers -Settings $taskSettings -Principal $taskPrincipal -Description 'Capture and verify midday/closing full-market snapshots; use existing local login without storing tokens.' -Force | Select-Object TaskName,State
} catch {
    # A user-level login shortcut needs no Task Scheduler/administrator privileges.
    $pythonWindowless = Join-Path (Split-Path -Parent $pythonExe) 'pythonw.exe'
    if (-not (Test-Path -LiteralPath $pythonWindowless)) { throw 'Windowless Python missing; fallback not installed.' }
    $startupFolder = [Environment]::GetFolderPath('Startup')
    $shortcutPath = Join-Path $startupFolder 'A-share-research closing watchdog.lnk'
    $shellLink = New-Object -ComObject WScript.Shell
    $shortcut = $shellLink.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = $pythonWindowless
    $shortcut.Arguments = '"' + (Join-Path $PSScriptRoot 'watchdog_service.py') + '"'
    $shortcut.WorkingDirectory = $repoRoot
    $shortcut.WindowStyle = 7
    $shortcut.Description = 'Current-user backup trigger for the existing A-share GitHub workflow.'
    $shortcut.Save()
    Start-Process -FilePath $pythonWindowless -ArgumentList $shortcut.Arguments -WorkingDirectory $repoRoot -WindowStyle Hidden
    Write-Output 'Task Scheduler access denied; current-user startup backup installed and started.'
    Write-Output $shortcutPath
}

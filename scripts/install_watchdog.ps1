$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$pythonExe = (& python -c 'import sys; print(sys.executable)').Trim()
$watchdogFile = Join-Path $PSScriptRoot 'daily_watchdog.py'
$taskAction = New-ScheduledTaskAction -Execute $pythonExe -Argument ('"' + $watchdogFile + '"') -WorkingDirectory $repoRoot
$taskTriggers = @()
foreach ($taskTime in @('15:12','15:35','16:15','18:15','21:15')) {
    $taskTriggers += New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday -At $taskTime
}
$taskTriggers += New-ScheduledTaskTrigger -AtLogOn
$taskSettings = New-ScheduledTaskSettingsSet -StartWhenAvailable -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Minutes 5) -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
$taskUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
$taskPrincipal = New-ScheduledTaskPrincipal -UserId $taskUser -LogonType Interactive -RunLevel Limited
try {
    Register-ScheduledTask -TaskName 'A-share-research closing watchdog' -Action $taskAction -Trigger $taskTriggers -Settings $taskSettings -Principal $taskPrincipal -Description 'Check current closing archive and trigger original GitHub workflow only if missing; no stored token/password.' -Force | Select-Object TaskName,State
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

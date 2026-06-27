$action = New-ScheduledTaskAction -Execute "C:\Users\22414\dev\juice094\.claude\scripts\auto-push.bat"
$trigger = New-ScheduledTaskTrigger -Once -At "2026-06-28T00:07:00" -RepetitionInterval (New-TimeSpan -Hours 2)
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
Register-ScheduledTask -TaskName "juice094-auto-push" -Action $action -Trigger $trigger -Settings $settings -Force
Write-Host "Task registered: juice094-auto-push (every 2 hours at :07)"

@echo off
setlocal
echo Stopping PC Background Trigger Daemon...

powershell -NoProfile -Command ^
    "$pidFile = '%~dp0..\storage\state\pc_trigger.pid';" ^
    "if (Test-Path $pidFile) {" ^
    "    $p = (Get-Content $pidFile).Trim();" ^
    "    Stop-Process -Id $p -Force -ErrorAction SilentlyContinue;" ^
    "    Remove-Item $pidFile -Force -ErrorAction SilentlyContinue;" ^
    "    Write-Host ('PC Trigger (PID ' + $p + ') stopped.') -ForegroundColor Yellow;" ^
    "}" ^
    "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*pc_auto_trigger.py*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue; Write-Host ('Stopped leftover instance PID ' + $_.ProcessId) -ForegroundColor Yellow; };"

echo Done.

@echo off
setlocal
echo ======================================================
echo   AliExpress Deals - PC Background Trigger Status
echo ======================================================

powershell -NoProfile -Command ^
    "$pidFile = '%~dp0..\storage\state\pc_trigger.pid';" ^
    "if (Test-Path $pidFile) {" ^
    "    $p = (Get-Content $pidFile).Trim();" ^
    "    $proc = Get-Process -Id $p -ErrorAction SilentlyContinue;" ^
    "    if ($proc) {" ^
    "        Write-Host ('Status: RUNNING (PID ' + $p + ' | RAM: ' + [math]::Round($proc.WorkingSet64 / 1MB, 1) + ' MB | CPU: ' + [math]::Round($proc.TotalProcessorTime.TotalSeconds, 2) + 's)') -ForegroundColor Green;" ^
    "    } else {" ^
    "        Write-Host ('Status: NOT RUNNING (stale PID ' + $p + ')') -ForegroundColor Yellow;" ^
    "    }" ^
    "} else {" ^
    "    Write-Host 'Status: NOT RUNNING' -ForegroundColor Red;" ^
    "}"

echo.
set LOG_FILE=%~dp0..\storage\state\pc_trigger.log
if exist "%LOG_FILE%" (
    echo Last 10 log entries:
    echo ------------------------------------------------------
    powershell -NoProfile -Command "Get-Content '%LOG_FILE%' -Tail 10 -ErrorAction SilentlyContinue"
    echo ------------------------------------------------------
) else (
    echo No log entries yet.
)
echo ======================================================

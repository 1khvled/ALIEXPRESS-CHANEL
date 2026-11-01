@echo off
setlocal
set LOG_FILE=%~dp0..\storage\state\pc_trigger.log
set PID_FILE=%~dp0..\storage\state\pc_trigger.pid

echo ======================================================
echo  AliExpress Deals - PC Background Trigger Status
echo ======================================================

if exist "%PID_FILE%" (
    set /p PID=<"%PID_FILE%"
    tasklist /FI "PID eq %PID%" 2>nul | findstr /i "%PID%" >nul
    if errorlevel 1 (
        echo Status: NOT RUNNING (stale PID %PID%)
    ) else (
        echo Status: RUNNING (PID %PID%)
    )
) else (
    echo Status: NOT RUNNING
)

echo.
if exist "%LOG_FILE%" (
    echo Last 10 log entries:
    echo ------------------------------------------------------
    powershell -NoProfile -Command "Get-Content '%LOG_FILE%' -Tail 10 -ErrorAction SilentlyContinue"
    echo ------------------------------------------------------
) else (
    echo No log file generated yet.
)
echo ======================================================

@echo off
setlocal
set PID_FILE=%~dp0..\storage\state\pc_trigger.pid

if exist "%PID_FILE%" (
    set /p PID=<"%PID_FILE%"
    echo Stopping PC Trigger Daemon (PID: %PID%)...
    taskkill /PID %PID% /F >nul 2>&1
    del /f /q "%PID_FILE%" >nul 2>&1
    echo PC Trigger stopped.
) else (
    echo No PID file found. Checking for running pc_auto_trigger instances...
    wmic process where "commandline like '%%pc_auto_trigger.py%%'" call terminate >nul 2>&1
    echo Checked and stopped any running instances.
)

@echo off
setlocal
echo Starting AliExpress Bot PC Trigger Daemon...
start "" "C:\Users\Abdelli\AppData\Local\Python\pythoncore-3.14-64\pythonw.exe" "%~dp0pc_auto_trigger.py"
timeout /t 2 /nobreak >nul
echo Started in background.
call "%~dp0status_trigger.bat"

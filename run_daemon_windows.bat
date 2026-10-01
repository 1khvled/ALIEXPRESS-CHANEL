@echo off
title DealScout 24/7 Autonomous Bot Daemon
cd /d "%~dp0"

echo ======================================================================
echo           DEALSCOUT 24/7 AUTONOMOUS RUNNER (WINDOWS DAEMON)           
echo ======================================================================

:LOOP
echo [%date% %time%] Starting Autonomous DealScout Engine...
python scripts\run_autonomous.py --interval 60
echo [%date% %time%] Engine exited or crashed. Auto-restarting in 5 seconds...
timeout /t 5 /nobreak >nul
goto LOOP

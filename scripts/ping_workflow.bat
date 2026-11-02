@echo off
REM Subtle, ultra-lightweight GitHub Actions trigger script (0% CPU, 0 MB RAM)
REM Triggers the cloud bot workflows on GitHub so your PC does zero heavy lifting.

set REPO=1khvled/ALIEXPRESS-CHANEL

if "%1"=="deals" (
    echo [PING] Triggering Deals Publisher workflow on GitHub...
    gh workflow run bot_cron.yml -R %REPO% -f force=true
) else if "%1"=="fahras" (
    echo [PING] Triggering Tajmi3at / Fahras Publisher on GitHub...
    gh workflow run tajmi3at.yml -R %REPO% -f category=all
) else (
    echo [PING] Triggering both Deals and Fahras on GitHub...
    gh workflow run bot_cron.yml -R %REPO% -f force=true
    gh workflow run tajmi3at.yml -R %REPO% -f category=all
)

echo [OK] Ping dispatched successfully!
timeout /t 3 /nobreak >nul

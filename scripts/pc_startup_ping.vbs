' Silent background trigger for Windows Startup (0% CPU, 0 MB RAM)
' Runs completely invisible in background on PC boot, pings GitHub Actions, and exits.
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "gh workflow run bot_cron.yml -R 1khvled/ALIEXPRESS-CHANEL -f force=true", 0, False
WshShell.Run "gh workflow run tajmi3at.yml -R 1khvled/ALIEXPRESS-CHANEL -f category=all", 0, False

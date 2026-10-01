#!/usr/bin/env bash
# ==============================================================================
# DealScout 24/7 Autonomous Background Service Launcher
# Sets up environment, pulls latest updates, and runs hardened autonomous daemon.
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

mkdir -p storage/logs storage/state storage/downloads storage/generated

echo "======================================================================"
echo "          DEALSCOUT 24/7 AUTONOMOUS RUNNER LAUNCHER                   "
echo "======================================================================"

# Determine Python command
if command -v python3 &>/dev/null; then
    PY_CMD="python3"
elif command -v python &>/dev/null; then
    PY_CMD="python"
else
    echo "[!] Error: python3 not found on system!"
    exit 1
fi

echo "[*] Using Python: $($PY_CMD --version)"

# Pull latest code from GitHub
if [ -d ".git" ]; then
    echo "[*] Syncing latest updates from GitHub..."
    git pull --rebase origin main || true
fi

# Install/verify dependencies
if [ -f "requirements.txt" ]; then
    echo "[*] Checking Python dependencies..."
    $PY_CMD -m pip install -q --upgrade pip
    $PY_CMD -m pip install -q -r requirements.txt || true
fi

echo "[*] Starting DealScout Autonomous Watchdog Daemon..."
echo "[*] Logs will stream to storage/logs/daemon.log"

# Run in an infinite supervisor loop in case of abnormal process termination
while true; do
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting autonomous daemon..."
    $PY_CMD scripts/run_autonomous.py --interval 60 2>&1 | tee -a storage/logs/daemon.log || true
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Daemon stopped or exited. Restarting in 5s..."
    sleep 5
done

import os
import sys
import time
import json
import socket
import subprocess
from pathlib import Path
from datetime import datetime

# Enforce single instance via local socket lock
LOCK_PORT = 49151
try:
    _lock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _lock_socket.bind(("127.0.0.1", LOCK_PORT))
except OSError:
    # Another instance is already running; exit silently
    sys.exit(0)

# Constants & Paths
REPO = "1khvled/dealscout-telegram-deals"
WORKFLOW = "bot_cron.yml"
CHECK_INTERVAL_SECONDS = 180  # Check every 3 minutes
CREATE_NO_WINDOW = 0x08000000  # Suppress console window flashing

LOG_DIR = Path(__file__).resolve().parent.parent / "storage" / "state"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "pc_trigger.log"
PID_FILE = LOG_DIR / "pc_trigger.pid"

# Record current PID for stop script
try:
    PID_FILE.write_text(str(os.getpid()), encoding="utf-8")
except Exception:
    pass


def log(msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}\n"
    try:
        # Rotate log if it exceeds 1000 lines
        if LOG_FILE.exists() and LOG_FILE.stat().st_size > 100_000:
            lines = LOG_FILE.read_text(encoding="utf-8", errors="ignore").splitlines()
            LOG_FILE.write_text("\n".join(lines[-300:]) + "\n", encoding="utf-8")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        pass


def run_command(cmd_list):
    """Executes a command silently without displaying a console window."""
    return subprocess.run(
        cmd_list,
        capture_output=True,
        text=True,
        creationflags=CREATE_NO_WINDOW
    )


def is_run_in_progress() -> bool:
    """Checks whether the bot workflow is currently running or queued."""
    try:
        res = run_command([
            "gh", "run", "list",
            "--workflow", WORKFLOW,
            "--repo", REPO,
            "--limit", "1",
            "--json", "status,conclusion,databaseId"
        ])
        if res.returncode == 0 and res.stdout.strip():
            runs = json.loads(res.stdout)
            if runs:
                status = runs[0].get("status", "")
                run_id = runs[0].get("databaseId", "")
                if status in ("in_progress", "queued", "waiting"):
                    log(f"Active run #{run_id} is currently '{status}'. Skipping trigger.")
                    return True
        return False
    except Exception as e:
        log(f"Warning: Failed to check run status ({e})")
        return False


def dispatch_workflow():
    """Dispatches a manual workflow run on GitHub Actions."""
    try:
        log("Triggering AliExpress Deals Telegram Bot workflow on GitHub Actions...")
        res = run_command([
            "gh", "workflow", "run", WORKFLOW,
            "--repo", REPO,
            "-f", "force=true"
        ])
        if res.returncode == 0:
            log("SUCCESS: Trigger dispatched to GitHub Actions.")
        else:
            err = res.stderr.strip() or res.stdout.strip()
            log(f"Dispatch notice: {err}")
    except Exception as e:
        log(f"Error dispatching workflow: {e}")


def main():
    log(f"PC Background Trigger daemon started (PID: {os.getpid()}). Checking every {CHECK_INTERVAL_SECONDS}s.")
    while True:
        try:
            if not is_run_in_progress():
                dispatch_workflow()
        except Exception as e:
            log(f"Unexpected loop exception: {e}")

        # Sleep with minimal CPU overhead
        time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    try:
        main()
    finally:
        try:
            if PID_FILE.exists():
                PID_FILE.unlink(missing_ok=True)
        except Exception:
            pass

"""
Standalone 24/7 Industrial Autonomous Runner & Watchdog for DealScout
Runs completely hands-free on VMs (Linux/Ubuntu) or local machines (Windows).
Self-healing with automatic crash recovery, signal handling, and PID management.
"""
import asyncio
import os
import signal
import sys
import time
import traceback
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from app.utils.logger import logger
from app.jobs.autonomous_engine import autonomous_engine

PID_FILE = BASE_DIR / "storage" / "state" / "daemon.pid"

def record_pid():
    """Records the running process ID."""
    try:
        PID_FILE.parent.mkdir(parents=True, exist_ok=True)
        PID_FILE.write_text(str(os.getpid()), encoding="utf-8")
    except Exception as e:
        logger.warning(f"Could not write PID file: {e}")

def remove_pid():
    """Cleans up the PID file on exit."""
    try:
        if PID_FILE.exists():
            PID_FILE.unlink()
    except Exception:
        pass

def main():
    record_pid()

    # Parse CLI flags
    interval = 60
    if "--interval" in sys.argv:
        try:
            idx = sys.argv.index("--interval")
            interval = int(sys.argv[idx + 1])
        except (IndexError, ValueError):
            interval = 60
    autonomous_engine.interval = interval

    single_run = "--single-run" in sys.argv or "--once" in sys.argv
    force_run = "--force" in sys.argv or "-f" in sys.argv

    if single_run:
        logger.info("Executing single autonomous run...")
        try:
            published = asyncio.run(autonomous_engine.run_single_cycle(force=force_run))
            logger.info(f"Single run finished: {published} deal(s) published.")
        finally:
            remove_pid()
        return

    print("=" * 70)
    print("   DEALSCOUT AUTONOMOUS DAEMON (24/7 HANDS-OFF ENGINE)")
    print(f"   PID: {os.getpid()} | Check Interval: {interval}s")
    print(f"   Target: @DzAliexpress0 & @francedealsdz")
    print("   Self-healing watchdog: ACTIVE")
    print("=" * 70)

    # Signal handlers for clean shutdown
    shutdown_requested = False

    def handle_exit(signum, frame):
        nonlocal shutdown_requested
        logger.info(f"Received exit signal ({signum}). Initiating graceful shutdown...")
        shutdown_requested = True
        autonomous_engine.stop()

    try:
        signal.signal(signal.SIGINT, handle_exit)
        signal.signal(signal.SIGTERM, handle_exit)
    except Exception:
        pass

    consecutive_crashes = 0
    while not shutdown_requested:
        try:
            asyncio.run(autonomous_engine.run_forever())
            if shutdown_requested:
                break
        except KeyboardInterrupt:
            logger.info("Daemon stopped by user (Ctrl+C).")
            break
        except Exception as fatal_err:
            consecutive_crashes += 1
            logger.critical(f"FATAL ENGINE CRASH #{consecutive_crashes}: {fatal_err}")
            traceback.print_exc()

            if shutdown_requested:
                break

            restart_delay = min(60, 5 * consecutive_crashes)
            logger.info(f"[WATCHDOG] Self-healing restart in {restart_delay}s...")
            time.sleep(restart_delay)

    remove_pid()
    logger.info("Autonomous DealScout Daemon has shut down cleanly.")

if __name__ == "__main__":
    main()

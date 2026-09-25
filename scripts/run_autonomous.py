"""
Standalone 24/7 Autonomous Runner for DealScout
Run this script to let the system operate completely hands-off.
"""
import asyncio
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from app.jobs.autonomous_engine import autonomous_engine

if __name__ == "__main__":
    try:
        asyncio.run(autonomous_engine.run_forever())
    except KeyboardInterrupt:
        autonomous_engine.stop()
        print("\nAutonomous engine stopped by user.")

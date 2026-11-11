"""AWS Lambda entry point for the DealScout publisher runtime.

Deployment shape
----------------
EventBridge Scheduler -> Lambda (container image, eu-north-1) -> S3 state bucket
                         |
                         +-> Telegram channels (@DzAliexpress0 / @francedealsdz)

The handler is intentionally thin: load secrets, pull state, run the exact
same publisher scripts that GitHub Actions runs, push state back.  No business
logic is duplicated here, so local, CI and AWS runs stay identical.

Environment (set by infra/aws/template.yaml)
--------------------------------------------
STATE_BUCKET            private S3 bucket for state/ and db/
DEALSCOUT_SECRET_ARN    optional Secrets Manager ARN containing env vars
INTELLIGENCE_MODE       off | shadow | enforce (default shadow)
"""

from __future__ import annotations

import asyncio
import json
import os
import time
import traceback
from typing import Any, Dict, Optional

try:  # container: /var/task is on sys.path; repo: normal package import
    from . import state_sync
except ImportError:  # pragma: no cover - exercised only inside Lambda
    import state_sync  # type: ignore

_RUNNING = False


def load_secrets() -> Dict[str, Any]:
    """Populate os.environ from Secrets Manager before app modules import."""
    arn = os.environ.get("DEALSCOUT_SECRET_ARN")
    if not arn:
        return {"loaded": False, "reason": "no secret arn"}

    try:
        import boto3

        client = boto3.client("secretsmanager")
        response = client.get_secret_value(SecretId=arn)
        payload = json.loads(response.get("SecretString") or "{}")
        if not isinstance(payload, dict):
            return {"loaded": False, "reason": "secret is not a JSON object"}

        applied = []
        for key, value in payload.items():
            if value is None or isinstance(value, (dict, list)):
                continue
            name = str(key)
            if name not in os.environ:
                os.environ[name] = str(value)
                applied.append(name)
        return {"loaded": True, "applied": sorted(applied)}
    except Exception as exc:  # a secret failure must be loud but not fatal
        print(f"[WARN] Could not load Secrets Manager payload: {exc}")
        return {"loaded": False, "reason": str(exc)}


async def run_publishers() -> Dict[str, int]:
    """Run the same two publishers the GitHub cron runs."""
    from scripts.post_france_deals import collect_and_post_france_deals
    from scripts.post_recent_deals import collect_and_post_last_10_deals

    algeria = await collect_and_post_last_10_deals(force=False, force_tajmi3at=False)
    france = await collect_and_post_france_deals(force=False, force_tajmi3at=False)
    return {"algeria": int(algeria or 0), "france": int(france or 0)}


def handler(event: Optional[Dict[str, Any]] = None, context: Any = None) -> Dict[str, Any]:
    """Lambda entry point. Raises on failure so CloudWatch alarms fire."""
    global _RUNNING
    started = time.time()
    bucket = os.environ.get("STATE_BUCKET")
    state_dir = os.environ.get("STATE_DIR", "storage/state")

    if _RUNNING:
        return {"status": "already-running", "elapsed_seconds": 0}

    _RUNNING = True
    sync_down_result: Dict[str, Any] = {"enabled": False}
    result: Dict[str, Any] = {
        "status": "error",
        "published": {},
        "elapsed_seconds": 0.0,
    }

    try:
        secrets = load_secrets()
        sync_down_result = sync_safely("down", bucket, state_dir)
        if bucket and sync_down_result.get("error"):
            # state is the deduplication memory: never publish blind.
            raise RuntimeError(
                "state download failed; refusing to publish without dedup state"
            )
        published = asyncio.run(run_publishers())
        result.update(status="ok", published=published, secrets=secrets)
    except Exception as exc:
        result.update(
            status="error",
            error=f"{type(exc).__name__}: {exc}",
            traceback=traceback.format_exc()[-4000:],
        )
        print(f"[FATAL] Lambda publisher run failed: {exc}")
        traceback.print_exc()
    finally:
        sync_up_result = sync_safely("up", bucket, state_dir)
        _RUNNING = False
        result["sync_down"] = sync_down_result
        result["sync_up"] = sync_up_result
        result["elapsed_seconds"] = round(time.time() - started, 2)

    if result["status"] != "ok":
        # Raising marks the invocation as failed -> Lambda Errors metric -> alarm.
        raise RuntimeError(result.get("error") or "publisher run failed")

    print(f"[LAMBDA] completed in {result['elapsed_seconds']}s: {result['published']}")
    return result


def sync_safely(direction: str, bucket: Optional[str], state_dir: str) -> Dict[str, Any]:
    if not bucket:
        return {"enabled": False}
    try:
        if direction == "down":
            return state_sync.sync_down(bucket, state_dir)
        return state_sync.sync_up(bucket, state_dir)
    except Exception as exc:
        print(f"[WARN] S3 state sync ({direction}) failed: {exc}")
        return {"enabled": True, "error": str(exc)}

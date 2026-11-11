"""S3 state synchronisation for the AWS Lambda runtime.

The GitHub Actions runtime commits ``storage/state/`` back to git every few
minutes.  On Lambda there is no persistent disk, so the same files are synced
to a private S3 bucket before and after each invocation.  This module is
dependency-light on purpose: ``boto3`` is imported lazily so it can be unit
tested with a fake client.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

STATE_PREFIX = "state/"
DB_PREFIX = "db/"


def _client(client: Any = None):
    if client is not None:
        return client
    import boto3  # provided by the Lambda runtime

    return boto3.client("s3")


def _iter_objects(client: Any, bucket: str, prefix: str) -> Iterable[Dict[str, Any]]:
    paginator = client.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []) or []:
            yield obj


def download_state(
    bucket: str,
    local_dir: str = "storage/state",
    prefix: str = STATE_PREFIX,
    client: Any = None,
) -> List[str]:
    """Download every object under ``prefix`` into ``local_dir``."""
    s3 = _client(client)
    target = Path(local_dir)
    target.mkdir(parents=True, exist_ok=True)
    downloaded: List[str] = []

    for obj in _iter_objects(s3, bucket, prefix):
        key = obj.get("Key", "")
        if not key or key.endswith("/"):
            continue
        relative = key[len(prefix):] if key.startswith(prefix) else key
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        s3.download_file(bucket, key, str(destination))
        downloaded.append(str(destination))

    return downloaded


def upload_state(
    bucket: str,
    local_dir: str = "storage/state",
    prefix: str = STATE_PREFIX,
    client: Any = None,
) -> List[str]:
    """Upload every file under ``local_dir`` to ``prefix`` (flat names kept)."""
    s3 = _client(client)
    source = Path(local_dir)
    if not source.exists():
        return []

    uploaded: List[str] = []
    for path in sorted(source.rglob("*")):
        if not path.is_file() or path.name.endswith(".tmp"):
            continue
        relative = path.relative_to(source).as_posix()
        key = f"{prefix}{relative}"
        s3.upload_file(str(path), bucket, key)
        uploaded.append(key)
    return uploaded


def download_db(bucket: str, local_path: str = "deals.db", client: Any = None) -> bool:
    """Fetch the SQLite audit database if it exists. Missing DB is not an error."""
    s3 = _client(client)
    key = f"{DB_PREFIX}{Path(local_path).name}"
    try:
        s3.head_object(Bucket=bucket, Key=key)
    except Exception:
        return False
    s3.download_file(bucket, key, local_path)
    return True


def upload_db(bucket: str, local_path: str = "deals.db", client: Any = None) -> bool:
    """Push the SQLite audit database if the publisher created or updated it."""
    path = Path(local_path)
    if not path.exists():
        return False
    s3 = _client(client)
    s3.upload_file(str(path), bucket, f"{DB_PREFIX}{path.name}")
    return True


def sync_down(bucket: Optional[str], state_dir: str = "storage/state") -> Dict[str, Any]:
    if not bucket:
        return {"enabled": False}
    return {
        "enabled": True,
        "state_files": download_state(bucket, state_dir),
        "db": download_db(bucket),
    }


def sync_up(bucket: Optional[str], state_dir: str = "storage/state") -> Dict[str, Any]:
    if not bucket:
        return {"enabled": False}
    return {
        "enabled": True,
        "state_files": upload_state(bucket, state_dir),
        "db": upload_db(bucket),
    }

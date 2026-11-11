"""Offline tests for the AWS state-sync helpers and handler safety interlocks."""

import json
from pathlib import Path

import pytest

from infra.aws import lambda_handler, state_sync


class _Paginator:
    def __init__(self, pages):
        self._pages = pages

    def paginate(self, **kwargs):
        return iter(self._pages)


class FakeS3:
    def __init__(self, objects=None):
        self.objects = dict(objects or {})
        self.downloaded = []
        self.uploaded = []

    def get_paginator(self, name):
        assert name == "list_objects_v2"
        contents = [{"Key": key} for key in sorted(self.objects)]
        return _Paginator([{"Contents": contents}])

    def download_file(self, bucket, key, destination):
        self.downloaded.append((bucket, key, destination))
        Path(destination).write_text(self.objects.get(key, ""), encoding="utf-8")

    def upload_file(self, source, bucket, key):
        self.uploaded.append((source, bucket, key))
        self.objects[key] = Path(source).read_text(encoding="utf-8")

    def head_object(self, Bucket, Key):
        if Key not in self.objects:
            raise RuntimeError("404")
        return {"Key": Key}


def test_download_state_writes_files(tmp_path):
    client = FakeS3(
        {
            "state/published_state.json": '{"a": 1}',
            "state/intelligence_model.json": '{"b": 2}',
            "state/sub/nested.json": "{}",
        }
    )
    downloaded = state_sync.download_state(
        "bucket", local_dir=str(tmp_path / "state"), client=client
    )
    assert len(downloaded) == 3
    assert (tmp_path / "state" / "published_state.json").read_text(encoding="utf-8") == '{"a": 1}'
    assert (tmp_path / "state" / "sub" / "nested.json").exists()


def test_upload_state_skips_tmp_files(tmp_path):
    source = tmp_path / "state"
    source.mkdir()
    (source / "published_state.json").write_text("{}", encoding="utf-8")
    (source / "model.json.tmp").write_text("partial", encoding="utf-8")

    client = FakeS3()
    uploaded = state_sync.upload_state("bucket", local_dir=str(source), client=client)

    assert uploaded == ["state/published_state.json"]
    assert "state/model.json.tmp" not in client.objects


def test_download_db_missing_is_not_an_error(tmp_path):
    client = FakeS3()
    assert state_sync.download_db("bucket", local_path=str(tmp_path / "deals.db"), client=client) is False


def test_download_db_existing(tmp_path):
    client = FakeS3({"db/deals.db": "sqlite-bytes"})
    target = tmp_path / "deals.db"
    assert state_sync.download_db("bucket", local_path=str(target), client=client) is True
    assert target.read_text(encoding="utf-8") == "sqlite-bytes"


def test_handler_refuses_to_publish_without_state(monkeypatch):
    monkeypatch.setenv("STATE_BUCKET", "test-bucket")
    monkeypatch.setattr(lambda_handler, "load_secrets", lambda: {"loaded": False})

    calls = []

    def fake_sync(direction, bucket, state_dir):
        calls.append(direction)
        if direction == "down":
            return {"enabled": True, "error": "s3 down"}
        return {"enabled": True}

    ran = []

    async def fake_run():
        ran.append(True)
        return {"algeria": 0, "france": 0}

    monkeypatch.setattr(lambda_handler, "sync_safely", fake_sync)
    monkeypatch.setattr(lambda_handler, "run_publishers", fake_run)

    with pytest.raises(RuntimeError, match="refusing to publish"):
        lambda_handler.handler({}, None)

    assert ran == []
    assert calls == ["down", "up"]


def test_handler_success_path(monkeypatch):
    monkeypatch.setenv("STATE_BUCKET", "test-bucket")
    monkeypatch.setattr(lambda_handler, "load_secrets", lambda: {"loaded": False})
    monkeypatch.setattr(
        lambda_handler,
        "sync_safely",
        lambda direction, bucket, state_dir: {"enabled": True},
    )

    async def fake_run():
        return {"algeria": 2, "france": 1}

    monkeypatch.setattr(lambda_handler, "run_publishers", fake_run)
    result = lambda_handler.handler({}, None)

    assert result["status"] == "ok"
    assert result["published"] == {"algeria": 2, "france": 1}


def test_load_secrets_without_arn(monkeypatch):
    monkeypatch.delenv("DEALSCOUT_SECRET_ARN", raising=False)
    assert lambda_handler.load_secrets()["loaded"] is False


def test_state_sync_disabled_without_bucket():
    assert state_sync.sync_down(None) == {"enabled": False}
    assert state_sync.sync_up(None) == {"enabled": False}

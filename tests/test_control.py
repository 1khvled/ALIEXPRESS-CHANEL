"""Tests for the deterministic closed-loop controller (Phase 3)."""

import json
from pathlib import Path

import pytest

from app.control.controller import (
    BOUNDS,
    apply_proposal,
    assess_health,
    build_control_state,
    collect_metrics,
    propose,
    render_markdown,
)

NOW = 1_800_000_000.0


def _write(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def _state_dir(tmp_path: Path, posts=(1, 2, 3), channel="lodydeals") -> Path:
    state_dir = tmp_path / "state"
    state_dir.mkdir(parents=True, exist_ok=True)
    deals = {}
    for index, age_hours in enumerate(posts):
        deals[f"{channel}:{index}"] = {
            "timestamp": NOW - age_hours * 3600,
            "channel": channel,
            "product_id": str(1000 + index),
        }
    _write(
        state_dir / "published_state.json",
        {
            "channel_published_deals": deals,
            "schedule_config": {"last_sweep_time": NOW - 600},
        },
    )
    return state_dir


def _model(state_dir: Path, counters=None, channels=None, score_sum=0.0):
    counters = counters or {
        "scored": 0,
        "verdict_publish": 0,
        "verdict_hold": 0,
        "verdict_skip": 0,
        "published": 0,
        "skipped": 0,
    }
    _write(
        state_dir / "intelligence_model.json",
        {
            "thresholds": {"publish": 60.0, "skip": 38.0},
            "counters": counters,
            "score_sum": score_sum,
            "channel_stats": channels or {},
        },
    )


def test_collect_metrics_counts_posts(tmp_path):
    state_dir = _state_dir(tmp_path, posts=(1, 2, 30, 200))
    _model(state_dir)
    metrics = collect_metrics(state_dir, now=NOW)

    assert metrics["posts_24h"] == 2
    assert metrics["posts_7d"] == 3
    assert metrics["last_post_age_hours"] == 1.0
    assert metrics["per_channel_7d"] == {"lodydeals": 3}
    assert metrics["thresholds"] == {"publish": 60.0, "skip": 38.0}


def test_health_ok_with_recent_posts(tmp_path):
    state_dir = _state_dir(tmp_path, posts=(1, 2, 3))
    _model(state_dir)
    health = assess_health(collect_metrics(state_dir, now=NOW))
    assert health["status"] == "ok"


def test_health_critical_without_state(tmp_path):
    state_dir = tmp_path / "empty"
    state_dir.mkdir()
    health = assess_health(collect_metrics(state_dir, now=NOW))
    assert health["status"] == "critical"
    assert any("missing" in issue for issue in health["issues"])


def test_health_critical_after_30h(tmp_path):
    state_dir = _state_dir(tmp_path, posts=(40, 50))
    _model(state_dir)
    health = assess_health(collect_metrics(state_dir, now=NOW))
    assert health["status"] == "critical"


def test_health_warn_after_12h(tmp_path):
    state_dir = _state_dir(tmp_path, posts=(13,))
    _model(state_dir)
    health = assess_health(collect_metrics(state_dir, now=NOW))
    assert health["status"] == "warn"


def test_propose_loosens_a_strict_gate(tmp_path):
    state_dir = _state_dir(tmp_path, posts=(1, 2, 3, 4))
    _model(
        state_dir,
        counters={
            "scored": 100,
            "verdict_publish": 10,
            "verdict_hold": 10,
            "verdict_skip": 80,
            "published": 10,
            "skipped": 80,
        },
    )
    metrics = collect_metrics(state_dir, now=NOW)
    proposal = propose(metrics, health=assess_health(metrics), now=NOW)

    assert proposal["action"] == "update"
    assert proposal["proposed"]["publish"] < proposal["current"]["publish"]
    assert proposal["proposed"]["skip"] < proposal["current"]["skip"]
    assert -4.0 <= proposal["delta"]["publish"] <= 4.0


def test_propose_tightens_on_flood(tmp_path):
    state_dir = _state_dir(tmp_path, posts=tuple(i / 10.0 for i in range(160)))
    _model(
        state_dir,
        counters={
            "scored": 200,
            "verdict_publish": 190,
            "verdict_hold": 5,
            "verdict_skip": 5,
            "published": 190,
            "skipped": 5,
        },
    )
    metrics = collect_metrics(state_dir, now=NOW)
    proposal = propose(metrics, health=assess_health(metrics), now=NOW)

    assert proposal["proposed"]["publish"] > proposal["current"]["publish"]
    assert proposal["proposed"]["publish"] <= 64.0  # max +4 per run


def test_proposal_is_bounded(tmp_path):
    state_dir = _state_dir(tmp_path, posts=tuple(i / 10.0 for i in range(200)))
    _model(
        state_dir,
        counters={
            "scored": 500,
            "verdict_publish": 500,
            "verdict_hold": 0,
            "verdict_skip": 0,
            "published": 500,
            "skipped": 0,
        },
    )
    metrics = collect_metrics(state_dir, now=NOW)
    proposal = propose(metrics, health=assess_health(metrics), now=NOW)

    assert BOUNDS["publish"][0] <= proposal["proposed"]["publish"] <= BOUNDS["publish"][1]
    assert BOUNDS["skip"][0] <= proposal["proposed"]["skip"] <= BOUNDS["skip"][1]
    assert proposal["proposed"]["skip"] <= proposal["proposed"]["publish"] - 8.0


def test_proposal_is_noop_when_healthy(tmp_path):
    state_dir = _state_dir(tmp_path, posts=tuple(range(1, 15)))
    _model(
        state_dir,
        counters={
            "scored": 100,
            "verdict_publish": 70,
            "verdict_hold": 10,
            "verdict_skip": 20,
            "published": 70,
            "skipped": 20,
        },
    )
    metrics = collect_metrics(state_dir, now=NOW)
    proposal = propose(metrics, health=assess_health(metrics), now=NOW)
    assert proposal["action"] == "noop"
    assert proposal["proposed"] == proposal["current"]


def test_no_automatic_change_when_critical(tmp_path):
    state_dir = tmp_path / "empty"
    state_dir.mkdir()
    metrics = collect_metrics(state_dir, now=NOW)
    proposal = propose(metrics, health=assess_health(metrics), now=NOW)
    assert proposal["action"] == "noop"
    assert any("critical" in reason for reason in proposal["reasons"])


def test_apply_writes_bounded_control_state(tmp_path):
    state_dir = _state_dir(tmp_path, posts=tuple(i / 10.0 for i in range(160)))
    _model(
        state_dir,
        counters={
            "scored": 200,
            "verdict_publish": 190,
            "verdict_hold": 5,
            "verdict_skip": 5,
            "published": 190,
            "skipped": 5,
        },
    )
    out = tmp_path / "control_state.json"
    result = apply_proposal(state_dir, actor="test", now=NOW, out_path=out)

    assert result["written"] is True
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["enabled"] is True
    assert payload["updated_by"] == "test"
    assert BOUNDS["publish"][0] <= payload["thresholds"]["publish"] <= BOUNDS["publish"][1]
    assert payload["thresholds"]["skip"] <= payload["thresholds"]["publish"] - 8.0


def test_apply_dry_run_does_not_write(tmp_path):
    state_dir = _state_dir(tmp_path, posts=tuple(i / 10.0 for i in range(160)))
    _model(
        state_dir,
        counters={
            "scored": 200,
            "verdict_publish": 190,
            "verdict_hold": 5,
            "verdict_skip": 5,
            "published": 190,
            "skipped": 5,
        },
    )
    out = tmp_path / "control_state.json"
    result = apply_proposal(state_dir, now=NOW, dry_run=True, out_path=out)
    assert result["written"] is False
    assert not out.exists()


def test_build_control_state_and_markdown(tmp_path):
    state_dir = _state_dir(tmp_path, posts=(1, 2, 3, 4))
    _model(
        state_dir,
        channels={
            "lodydeals": {"seen": 30, "published": 25, "skipped": 5, "ewma": 0.82},
        },
    )
    metrics = collect_metrics(state_dir, now=NOW)
    health = assess_health(metrics)
    proposal = propose(metrics, health=health, now=NOW)
    control = build_control_state(proposal, actor="test", now=NOW)
    markdown = render_markdown(metrics, health, proposal)

    assert control["version"] == 1
    assert "thresholds" in control
    assert "DealScout control report" in markdown
    assert "Learned source yield" in markdown
    assert "@lodydeals" in markdown

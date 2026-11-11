"""Closed-loop control for the DealScout runtime.

Phase 3 of the intelligence plan: read production evidence (state + learned
model), produce a health report, and propose *bounded* threshold changes.  It
never publishes, never calls Telegram and never talks to an LLM.

Two ways to apply a proposal:

* ``propose`` writes a candidate ``control_state.json``; the GitHub workflow
  opens a pull request so a human reviews the change before merge.
* ``apply`` writes ``control_state.json`` directly (manual override).

The publisher's intelligence gate reads ``control_state.json`` at runtime and
clamps every value to safe bounds.  A bad proposal therefore cannot disable
deduplication, publishing or the competitor firewall — it can only move the
score thresholds inside ``BOUNDS``.

Usage:
    python -m app.control.controller report --markdown
    python -m app.control.controller propose --out storage/state/control_state.json
    python -m app.control.controller apply --actor operator
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

# Deliberately stdlib-only: the controller must run on a bare GitHub runner
# without installing the publisher's dependencies.
DEFAULT_STATE_DIR = Path(os.environ.get("DEALSCOUT_STATE_DIR", "storage/state"))

DEFAULT_THRESHOLDS = {"publish": 60.0, "skip": 38.0}
BOUNDS: Dict[str, Tuple[float, float]] = {
    "publish": (45.0, 80.0),
    "skip": (20.0, 55.0),
}
MAX_DELTA_PER_RUN = 4.0
MIN_GAP = 8.0

CRITICAL_NO_POST_HOURS = 30.0
WARN_NO_POST_HOURS = 12.0
WARN_STALE_SWEEP_HOURS = 3.0


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------


def _load_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except Exception:
        return default


def _atomic_write(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    os.replace(tmp, path)


def _iso(ts: Optional[float] = None) -> str:
    moment = datetime.fromtimestamp(ts, tz=timezone.utc) if ts else datetime.now(timezone.utc)
    return moment.replace(microsecond=0).isoformat()


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


# ---------------------------------------------------------------------------
# Evidence collection
# ---------------------------------------------------------------------------


def collect_metrics(state_dir: Path = DEFAULT_STATE_DIR, now: Optional[float] = None) -> Dict[str, Any]:
    """Read the committed state and learned model. Read-only, no network."""
    now = time.time() if now is None else float(now)
    state_dir = Path(state_dir)

    state = _load_json(state_dir / "published_state.json", {}) or {}
    model = _load_json(state_dir / "intelligence_model.json", {}) or {}
    control = _load_json(state_dir / "control_state.json", {}) or {}

    deals = state.get("channel_published_deals") or {}
    timestamps: List[float] = []
    per_channel: Dict[str, int] = {}
    cutoff_7d = now - 7 * 86400
    for record in deals.values():
        if not isinstance(record, dict):
            continue
        ts = _as_float(record.get("timestamp"), 0.0)
        if ts <= 0:
            continue
        if ts >= cutoff_7d:
            timestamps.append(ts)
            channel = str(record.get("channel") or "unknown").lower().lstrip("@")
            per_channel[channel] = per_channel.get(channel, 0) + 1

    posts_24h = sum(1 for ts in timestamps if ts >= now - 86400)
    posts_7d = len(timestamps)
    last_post_ts = max(timestamps) if timestamps else None
    last_post_age = (now - last_post_ts) / 3600.0 if last_post_ts else None

    schedule = state.get("schedule_config") or {}
    last_sweep_ts = _as_float(schedule.get("last_sweep_time"), 0.0)
    last_sweep_age = (now - last_sweep_ts) / 3600.0 if last_sweep_ts else None

    counters = model.get("counters") or {}
    scored = int(_as_float(counters.get("scored"), 0))
    verdict_skip = int(_as_float(counters.get("verdict_skip"), 0))
    verdict_hold = int(_as_float(counters.get("verdict_hold"), 0))
    verdict_publish = int(_as_float(counters.get("verdict_publish"), 0))
    enforced_published = int(_as_float(counters.get("published"), 0))
    enforced_skipped = int(_as_float(counters.get("skipped"), 0))
    score_sum = _as_float(model.get("score_sum"), 0.0)

    channel_stats = model.get("channel_stats") or {}
    channel_yield = {}
    for name, stat in channel_stats.items():
        if not isinstance(stat, dict):
            continue
        seen = int(_as_float(stat.get("seen"), 0))
        published = int(_as_float(stat.get("published"), 0))
        channel_yield[str(name)] = {
            "seen": seen,
            "published": published,
            "skipped": int(_as_float(stat.get("skipped"), 0)),
            "yield": round(published / seen, 3) if seen else 0.0,
            "ewma": round(_as_float(stat.get("ewma"), 0.5), 3),
        }

    model_thresholds = model.get("thresholds") or {}
    current = {
        "publish": _as_float(model_thresholds.get("publish"), DEFAULT_THRESHOLDS["publish"]),
        "skip": _as_float(model_thresholds.get("skip"), DEFAULT_THRESHOLDS["skip"]),
    }
    if control.get("enabled") and isinstance(control.get("thresholds"), dict):
        current["publish"] = _as_float(
            control["thresholds"].get("publish"), current["publish"]
        )
        current["skip"] = _as_float(control["thresholds"].get("skip"), current["skip"])

    return {
        "generated_at": _iso(now),
        "state_dir": str(state_dir),
        "state_present": (state_dir / "published_state.json").exists(),
        "model_present": (state_dir / "intelligence_model.json").exists(),
        "control_present": (state_dir / "control_state.json").exists(),
        "posts_24h": posts_24h,
        "posts_7d": posts_7d,
        "last_post_age_hours": round(last_post_age, 2) if last_post_age is not None else None,
        "last_sweep_age_hours": round(last_sweep_age, 2) if last_sweep_age is not None else None,
        "per_channel_7d": dict(sorted(per_channel.items(), key=lambda kv: -kv[1])),
        "decisions": {
            "scored": scored,
            "verdict_publish": verdict_publish,
            "verdict_hold": verdict_hold,
            "verdict_skip": verdict_skip,
            "predicted_skip_rate": round(verdict_skip / scored, 3) if scored else None,
            "published": enforced_published,
            "enforced_skips": enforced_skipped,
            "average_score": round(score_sum / scored, 2) if scored else None,
        },
        "channel_yield": channel_yield,
        "thresholds": current,
        "control_enabled": bool(control.get("enabled")),
    }


def assess_health(metrics: Dict[str, Any]) -> Dict[str, Any]:
    """Turn metrics into ok / warn / critical with explicit reasons."""
    issues: List[str] = []
    status = "ok"

    def warn(message: str) -> None:
        nonlocal status
        issues.append(message)
        if status == "ok":
            status = "warn"

    def critical(message: str) -> None:
        nonlocal status
        issues.append(message)
        status = "critical"

    if not metrics.get("state_present"):
        critical("published_state.json is missing")
    if not metrics.get("model_present"):
        warn("intelligence_model.json is missing; model starts from priors")

    age = metrics.get("last_post_age_hours")
    if age is None:
        critical("no published deal recorded in channel_published_deals")
    elif age >= CRITICAL_NO_POST_HOURS:
        critical(f"no deal published for {age:.1f}h (>= {CRITICAL_NO_POST_HOURS:.0f}h)")
    elif age >= WARN_NO_POST_HOURS:
        warn(f"no deal published for {age:.1f}h")

    if metrics.get("posts_7d", 0) == 0:
        critical("no deals published in the last 7 days")

    sweep_age = metrics.get("last_sweep_age_hours")
    if sweep_age is not None and sweep_age >= WARN_STALE_SWEEP_HOURS:
        warn(f"last sweep was {sweep_age:.1f}h ago")

    decisions = metrics.get("decisions") or {}
    scored = int(decisions.get("scored") or 0)
    skip_rate = decisions.get("predicted_skip_rate")
    if scored >= 40 and skip_rate is not None and skip_rate >= 0.75:
        warn(f"intelligence is skipping {skip_rate:.0%} of candidates")

    average = decisions.get("average_score")
    if scored >= 20 and average is not None and average < 40:
        warn(f"average deal score is low ({average:.1f}/100)")

    channel_yield = metrics.get("channel_yield") or {}
    for name, stat in channel_yield.items():
        if stat.get("seen", 0) >= 20 and stat.get("yield", 0.0) < 0.15:
            warn(f"source @{name} has low yield ({stat['yield']:.0%} of {stat['seen']} candidates)")

    return {"status": status, "issues": issues}


# ---------------------------------------------------------------------------
# Proposal engine
# ---------------------------------------------------------------------------


def _bounded_thresholds(publish: float, skip: float) -> Dict[str, float]:
    publish = _clamp(publish, *BOUNDS["publish"])
    skip = _clamp(skip, *BOUNDS["skip"])
    if skip > publish - MIN_GAP:
        skip = max(BOUNDS["skip"][0], publish - MIN_GAP)
    return {"publish": round(publish, 1), "skip": round(skip, 1)}


def propose(
    metrics: Dict[str, Any],
    health: Optional[Dict[str, Any]] = None,
    now: Optional[float] = None,
) -> Dict[str, Any]:
    """Deterministic, bounded threshold proposal with explicit reasons."""
    health = health or assess_health(metrics)
    current = metrics.get("thresholds") or dict(DEFAULT_THRESHOLDS)
    publish = _as_float(current.get("publish"), DEFAULT_THRESHOLDS["publish"])
    skip = _as_float(current.get("skip"), DEFAULT_THRESHOLDS["skip"])

    decisions = metrics.get("decisions") or {}
    scored = int(decisions.get("scored") or 0)
    skip_rate = decisions.get("predicted_skip_rate")
    posts_24h = int(metrics.get("posts_24h") or 0)
    last_post_age = metrics.get("last_post_age_hours")

    delta_publish = 0.0
    delta_skip = 0.0
    reasons: List[str] = []

    if health.get("status") == "critical":
        reasons.append("health is critical: no automatic threshold change")
    else:
        if scored >= 40 and skip_rate is not None and skip_rate >= 0.60:
            delta_publish -= 3.0
            delta_skip -= 2.0
            reasons.append(
                f"gate is strict: {skip_rate:.0%} of {scored} candidates scored below skip"
            )
        if (
            scored >= 40
            and skip_rate is not None
            and skip_rate <= 0.15
            and posts_24h >= 90
        ):
            delta_publish += 3.0
            reasons.append(
                f"gate is loose and volume is high: {skip_rate:.0%} skip rate, {posts_24h} posts/24h"
            )
        if posts_24h >= 150:
            delta_publish += 3.0
            delta_skip += 2.0
            reasons.append(f"flood control: {posts_24h} posts in 24h exceeds the daily target")
        if posts_24h <= 10 and scored >= 20 and skip_rate is not None and skip_rate <= 0.35:
            delta_publish -= 2.0
            reasons.append(
                f"drought: only {posts_24h} posts/24h while the gate skips {skip_rate:.0%}"
            )
        if (
            last_post_age is not None
            and last_post_age >= 18
            and skip_rate is not None
            and skip_rate >= 0.40
        ):
            delta_publish -= 4.0
            delta_skip -= 2.0
            reasons.append(
                f"no post for {last_post_age:.1f}h and skip rate is {skip_rate:.0%}"
            )

    delta_publish = _clamp(delta_publish, -MAX_DELTA_PER_RUN, MAX_DELTA_PER_RUN)
    delta_skip = _clamp(delta_skip, -MAX_DELTA_PER_RUN, MAX_DELTA_PER_RUN)

    proposed = _bounded_thresholds(publish + delta_publish, skip + delta_skip)
    changed = proposed["publish"] != round(publish, 1) or proposed["skip"] != round(skip, 1)

    if not reasons:
        reasons.append("metrics are inside the healthy band; keep thresholds unchanged")

    return {
        "version": 1,
        "generated_at": _iso(now),
        "action": "update" if changed else "noop",
        "current": {"publish": round(publish, 1), "skip": round(skip, 1)},
        "proposed": proposed,
        "delta": {
            "publish": round(proposed["publish"] - publish, 1),
            "skip": round(proposed["skip"] - skip, 1),
        },
        "bounds": {key: list(value) for key, value in BOUNDS.items()},
        "reasons": reasons,
        "health": health,
        "metrics": {
            "posts_24h": posts_24h,
            "posts_7d": metrics.get("posts_7d"),
            "last_post_age_hours": last_post_age,
            "decisions": decisions,
            "channel_yield": metrics.get("channel_yield"),
        },
    }


def build_control_state(proposal: Dict[str, Any], actor: str = "control-loop", now: Optional[float] = None) -> Dict[str, Any]:
    return {
        "version": 1,
        "enabled": True,
        "updated_at": _iso(now),
        "updated_by": actor,
        "thresholds": dict(proposal["proposed"]),
        "bounds": {key: list(value) for key, value in BOUNDS.items()},
        "reasons": list(proposal.get("reasons") or []),
        "source_metrics": {
            "posts_24h": (proposal.get("metrics") or {}).get("posts_24h"),
            "posts_7d": (proposal.get("metrics") or {}).get("posts_7d"),
            "last_post_age_hours": (proposal.get("metrics") or {}).get("last_post_age_hours"),
            "decisions": (proposal.get("metrics") or {}).get("decisions"),
        },
        "generated_at": proposal.get("generated_at"),
    }


def apply_proposal(
    state_dir: Path = DEFAULT_STATE_DIR,
    actor: str = "control-loop",
    dry_run: bool = False,
    now: Optional[float] = None,
    out_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """Compute and (unless dry-run) persist a bounded control_state.json."""
    metrics = collect_metrics(state_dir, now=now)
    health = assess_health(metrics)
    proposal = propose(metrics, health=health, now=now)
    result = {"proposal": proposal, "written": False}

    if proposal["action"] == "noop":
        result["message"] = "no threshold change needed"
        return result

    control_state = build_control_state(proposal, actor=actor, now=now)
    result["control_state"] = control_state

    if not dry_run:
        destination = Path(out_path) if out_path else Path(state_dir) / "control_state.json"
        _atomic_write(destination, control_state)
        result["written"] = True
        result["path"] = str(destination)

    return result


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def render_markdown(metrics: Dict[str, Any], health: Dict[str, Any], proposal: Dict[str, Any]) -> str:
    decisions = metrics.get("decisions") or {}
    lines = [
        "# DealScout control report",
        "",
        f"Generated: **{metrics.get('generated_at')}**",
        f"Health: **{health.get('status', 'unknown').upper()}**",
        "",
        "## Traffic",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Posts last 24h | {metrics.get('posts_24h')} |",
        f"| Posts last 7d | {metrics.get('posts_7d')} |",
        f"| Last post age | {metrics.get('last_post_age_hours')} h |",
        f"| Last sweep age | {metrics.get('last_sweep_age_hours')} h |",
        f"| Candidates scored | {decisions.get('scored')} |",
        f"| Predicted skip rate | {decisions.get('predicted_skip_rate')} |",
        f"| Enforced skips | {decisions.get('enforced_skips')} |",
        f"| Average score | {decisions.get('average_score')} |",
        "",
        "## Thresholds",
        "",
        "| | Publish | Skip |",
        "|---|---|---|",
        f"| Current | {proposal['current']['publish']} | {proposal['current']['skip']} |",
        f"| Proposed | {proposal['proposed']['publish']} | {proposal['proposed']['skip']} |",
        f"| Delta | {proposal['delta']['publish']:+.1f} | {proposal['delta']['skip']:+.1f} |",
        "",
        "## Why",
        "",
    ]
    lines.extend(f"- {reason}" for reason in proposal.get("reasons") or [])
    lines.append("")

    issues = health.get("issues") or []
    lines.extend(["## Health issues", ""])
    if issues:
        lines.extend(f"- {issue}" for issue in issues)
    else:
        lines.append("- none")
    lines.append("")

    per_channel = metrics.get("per_channel_7d") or {}
    if per_channel:
        lines.extend(["## Published per source (7d)", "", "| Source | Posts |", "|---|---|"])
        lines.extend(f"| @{name} | {count} |" for name, count in per_channel.items())
        lines.append("")

    channel_yield = metrics.get("channel_yield") or {}
    if channel_yield:
        lines.extend(
            [
                "## Learned source yield",
                "",
                "| Source | Seen | Published | Skipped | Yield | EWMA |",
                "|---|---|---|---|---|---|",
            ]
        )
        for name, stat in sorted(channel_yield.items()):
            lines.append(
                f"| @{name} | {stat.get('seen')} | {stat.get('published')} | "
                f"{stat.get('skipped')} | {stat.get('yield')} | {stat.get('ewma')} |"
            )
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _write_text(path: Optional[str], text: str) -> None:
    if not path:
        return
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m app.control.controller",
        description="Deterministic closed-loop control for DealScout (no LLM).",
    )
    parser.add_argument(
        "--state-dir",
        default=str(DEFAULT_STATE_DIR),
        help="directory holding published_state.json / intelligence_model.json",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    report = sub.add_parser("report", help="health + metrics report (read-only)")
    report.add_argument("--json", action="store_true", help="print JSON")
    report.add_argument("--markdown", action="store_true", help="print Markdown")
    report.add_argument("--out", help="write the JSON report to this path")
    report.add_argument("--markdown-out", help="write the Markdown report to this path")
    report.add_argument(
        "--fail-on-critical",
        action="store_true",
        help="exit 2 when health is critical (for scheduled CI checks)",
    )

    prop = sub.add_parser("propose", help="compute a bounded threshold proposal")
    prop.add_argument("--json", action="store_true", help="print JSON")
    prop.add_argument("--markdown", action="store_true", help="print Markdown")
    prop.add_argument("--out", help="write a candidate control_state.json here")
    prop.add_argument("--markdown-out", help="write the Markdown proposal here")
    prop.add_argument("--actor", default="control-loop")
    prop.add_argument("--fail-on-critical", action="store_true")

    apply_cmd = sub.add_parser("apply", help="write control_state.json")
    apply_cmd.add_argument("--actor", default="control-loop")
    apply_cmd.add_argument("--dry-run", action="store_true")
    apply_cmd.add_argument("--json", action="store_true")
    apply_cmd.add_argument(
        "--out",
        help="write control_state.json here (default: <state-dir>/control_state.json)",
    )

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = _build_parser().parse_args(argv)
    state_dir = Path(args.state_dir)

    if args.command == "report":
        metrics = collect_metrics(state_dir)
        health = assess_health(metrics)
        proposal = propose(metrics, health=health)
        payload = {"metrics": metrics, "health": health, "proposal": proposal}
        markdown = render_markdown(metrics, health, proposal)

        if args.out:
            _atomic_write(Path(args.out), payload)
        _write_text(args.markdown_out, markdown)
        if args.json:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        elif args.markdown:
            print(markdown)
        else:
            print(f"health={health['status']} posts_24h={metrics['posts_24h']} "
                  f"proposal={proposal['action']} {proposal['current']} -> {proposal['proposed']}")
            for issue in health.get("issues") or []:
                print(f"  - {issue}")

        if args.fail_on_critical and health["status"] == "critical":
            return 2
        return 0

    if args.command == "propose":
        metrics = collect_metrics(state_dir)
        health = assess_health(metrics)
        proposal = propose(metrics, health=health)
        markdown = render_markdown(metrics, health, proposal)

        if args.out and proposal["action"] == "update":
            _atomic_write(
                Path(args.out),
                build_control_state(proposal, actor=args.actor),
            )
        _write_text(args.markdown_out, markdown)
        if args.json:
            print(json.dumps(proposal, indent=2, ensure_ascii=False))
        elif args.markdown:
            print(markdown)
        else:
            print(f"action={proposal['action']} {proposal['current']} -> {proposal['proposed']}")
            for reason in proposal["reasons"]:
                print(f"  - {reason}")

        if args.fail_on_critical and health["status"] == "critical":
            return 2
        return 0

    result = apply_proposal(
        state_dir,
        actor=args.actor,
        dry_run=args.dry_run,
        out_path=Path(args.out) if args.out else None,
    )
    proposal = result["proposal"]
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(
            f"action={proposal['action']} written={result['written']} "
            f"{proposal['current']} -> {proposal['proposed']}"
        )
        if result.get("message"):
            print(f"  {result['message']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

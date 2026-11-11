"""Publisher integration for the deterministic deal intelligence.

This module is the only place that touches settings, persistent state and the
filesystem.  It is deliberately fail-open: any unexpected error while scoring
returns ``allowed=True`` so the intelligence layer can never stop publishing.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.config.settings import settings
from app.intelligence.scoring import (
    FLOW_WINDOW_HOURS,
    DealFeatures,
    DealIntelligence,
    Decision,
    extract_category,
)
from app.publisher.state_tracker import load_persistent_state
from app.utils.logger import logger

MODE_OFF = "off"
MODE_SHADOW = "shadow"
MODE_ENFORCE = "enforce"
VALID_MODES = {MODE_OFF, MODE_SHADOW, MODE_ENFORCE}


@dataclass
class GateResult:
    """Outcome of the intelligence gate for one candidate deal."""

    allowed: bool
    mode: str
    decision: Optional[Decision] = None
    channel: str = ""
    category: str = "other"
    product_id: Optional[str] = None
    price: Optional[float] = None
    intel: Optional[DealIntelligence] = None
    error: Optional[str] = None

    @property
    def score(self) -> Optional[float]:
        return self.decision.score if self.decision else None

    @property
    def verdict(self) -> str:
        return self.decision.verdict if self.decision else "off"

    def log_line(self) -> str:
        if self.mode == MODE_OFF:
            return "[INTEL] disabled"
        if self.decision is None:
            return f"[INTEL] {self.mode} unavailable ({self.error or 'no decision'})"
        return f"[INTEL] @{self.channel} {self.decision.summary()} mode={self.mode}"


def _state_dir() -> Path:
    return Path(getattr(settings, "BASE_DIR", Path.cwd())) / "storage" / "state"


def _model_path() -> Path:
    override = getattr(settings, "INTELLIGENCE_MODEL_PATH", None)
    if override:
        path = Path(str(override))
        return path if path.is_absolute() else Path(settings.BASE_DIR) / path
    return _state_dir() / "intelligence_model.json"


def _control_path() -> Path:
    override = getattr(settings, "INTELLIGENCE_CONTROL_PATH", None)
    if override:
        path = Path(str(override))
        return path if path.is_absolute() else Path(settings.BASE_DIR) / path
    return _state_dir() / "control_state.json"


def _load_control_overrides() -> Dict[str, Any]:
    path = _control_path()
    if not path.exists():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as handle:
            raw = json.load(handle)
        return raw if isinstance(raw, dict) else {}
    except Exception:
        return {}


def _get_mode() -> str:
    mode = str(getattr(settings, "INTELLIGENCE_MODE", MODE_SHADOW) or MODE_SHADOW)
    mode = mode.strip().lower()
    return mode if mode in VALID_MODES else MODE_SHADOW


def _flow_counts(state: Dict[str, Any]) -> int:
    """Posts published in the last FLOW_WINDOW_HOURS (all channels)."""
    now = time.time()
    cutoff = now - FLOW_WINDOW_HOURS * 3600.0
    deals = state.get("channel_published_deals") or {}
    count = 0
    for record in deals.values():
        if not isinstance(record, dict):
            continue
        try:
            timestamp = float(record.get("timestamp", 0) or 0)
        except (TypeError, ValueError):
            continue
        if timestamp >= cutoff:
            count += 1
    return count


def _recent_titles(state: Dict[str, Any], limit: int = 120) -> tuple:
    """Titles published in the last 72h, newest first."""
    now = time.time()
    cutoff = now - 72 * 3600.0
    timestamps = state.get("published_title_timestamps") or {}
    recent: List[tuple] = []
    for title, timestamp in timestamps.items():
        try:
            ts = float(timestamp)
        except (TypeError, ValueError):
            continue
        if ts >= cutoff:
            recent.append((ts, str(title)))
    recent.sort(reverse=True)
    return tuple(title for _, title in recent[:limit])


def _age_hours(message_dt: Optional[datetime]) -> Optional[float]:
    if message_dt is None:
        return None
    try:
        if message_dt.tzinfo is None:
            message_dt = message_dt.replace(tzinfo=timezone.utc)
        delta = datetime.now(timezone.utc) - message_dt
        return max(0.0, delta.total_seconds() / 3600.0)
    except Exception:
        return None


def _previous_price(state: Dict[str, Any], product_id: Optional[str]) -> Optional[float]:
    if not product_id:
        return None
    try:
        value = (state.get("published_product_prices") or {}).get(str(product_id))
        number = float(value) if value is not None else None
        return number if number and number > 0 else None
    except (TypeError, ValueError):
        return None


def _price_history(
    intel: DealIntelligence, product_id: Optional[str]
) -> tuple:
    if not product_id:
        return ()
    return tuple(intel.model.product_prices.get(str(product_id), []))


def evaluate_deal_gate(
    extracted: Any,
    channel: str,
    raw_text: str = "",
    message_dt: Optional[datetime] = None,
    is_restock: bool = False,
    is_price_drop: bool = False,
    model_path: Optional[Path] = None,
    control_path: Optional[Path] = None,
    persist: bool = True,
) -> GateResult:
    """Score a candidate deal and decide whether the publisher may continue.

    ``off``     -> no scoring at all.
    ``shadow``  -> score and log, always allow (safe rollout).
    ``enforce`` -> block only verdict ``skip``; ``hold`` follows
                   ``INTELLIGENCE_HOLD_ACTION`` (default: publish).
    """
    mode = _get_mode()
    if mode == MODE_OFF:
        return GateResult(allowed=True, mode=mode, channel=channel)

    try:
        state = load_persistent_state()

        path = Path(model_path) if model_path else _model_path()
        if control_path is not None:
            try:
                with open(control_path, "r", encoding="utf-8") as handle:
                    overrides = json.load(handle)
            except Exception:
                overrides = {}
        else:
            overrides = _load_control_overrides()

        intel = DealIntelligence.load(path, overrides=overrides, persist=persist)

        product_id = getattr(extracted, "product_id", None)
        price = getattr(extracted, "current_price", None)
        title = getattr(extracted, "title", "") or ""
        category = extract_category(title)

        features = DealFeatures(
            channel=channel,
            title=title,
            product_id=str(product_id) if product_id else None,
            price=float(price) if price else None,
            previous_price=_previous_price(state, product_id),
            price_history=_price_history(intel, product_id),
            message_age_hours=_age_hours(message_dt),
            has_coupon=bool(
                getattr(extracted, "coupon_code", None)
                or getattr(extracted, "seller_coupon", None)
            ),
            has_points_discount=bool(
                getattr(extracted, "has_points_discount", False)
            ),
            is_restock=bool(is_restock),
            is_price_drop=bool(is_price_drop),
            is_coupon_list=bool(getattr(extracted, "is_coupon_list", False)),
            deal_type=str(getattr(extracted, "deal_type", "coin") or "coin"),
            posts_last_window=_flow_counts(state),
            recent_titles=_recent_titles(state),
            category=category,
        )

        decision = intel.score(features)

        if persist:
            intel.record_decision(decision, features)
            # Count the candidate once; the outcome is attached later.
            intel.observe(channel, category, "seen")

        allowed = True
        if mode == MODE_ENFORCE:
            if decision.verdict == "skip":
                allowed = False
                if persist:
                    intel.observe(channel, category, "skipped", count_seen=False)
            elif decision.verdict == "hold":
                hold_action = str(
                    getattr(settings, "INTELLIGENCE_HOLD_ACTION", "publish")
                ).strip().lower()
                if hold_action == "skip":
                    allowed = False
                    if persist:
                        intel.observe(channel, category, "skipped", count_seen=False)

        result = GateResult(
            allowed=allowed,
            mode=mode,
            decision=decision,
            channel=channel,
            category=category,
            product_id=str(product_id) if product_id else None,
            price=float(price) if price else None,
            intel=intel,
        )

        if allowed:
            logger.info(result.log_line())
        else:
            logger.warning(result.log_line() + " [BLOCKED]")
        return result

    except Exception as exc:  # pragma: no cover - fail-open guard
        logger.warning(f"[INTEL] scoring failed, publishing unchanged: {exc}")
        return GateResult(
            allowed=True,
            mode=mode,
            channel=channel,
            error=str(exc),
        )


def record_published_outcome(result: Optional[GateResult]) -> None:
    """Attach a real publish outcome to the learned channel/category yield."""
    if result is None or result.intel is None or result.decision is None:
        return
    try:
        result.intel.observe(
            result.channel,
            result.category,
            "published",
            count_seen=False,
        )
        result.intel.remember_price(result.product_id, result.price)
    except Exception as exc:  # pragma: no cover - fail-open guard
        logger.debug(f"[INTEL] outcome recording skipped: {exc}")


def record_published_deal(product_id: Optional[str], price: Optional[float]) -> None:
    """Persist the price of a successfully published deal for future edge scoring."""
    try:
        intel = DealIntelligence.load(_model_path(), overrides={}, persist=True)
        intel.remember_price(product_id, price)
    except Exception as exc:  # pragma: no cover - fail-open guard
        logger.debug(f"[INTEL] price history update skipped: {exc}")


def decision_report(result: Optional[GateResult]) -> Dict[str, Any]:
    """Small JSON-friendly record for logs / the control loop."""
    if result is None or result.decision is None:
        return {"mode": result.mode if result else "off", "verdict": "off"}
    return {
        "mode": result.mode,
        "allowed": result.allowed,
        "channel": result.channel,
        "category": result.category,
        "decision": result.decision.to_dict(),
    }

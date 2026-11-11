"""Deterministic, explainable deal intelligence.

There is no LLM, no network call and no external service in this module.
Every decision is a pure function of (a) the candidate deal's features and
(b) a small JSON model that is updated with simple, auditable statistics.

Why this design
---------------
An LLM would add latency, cost, non-determinism and a new failure mode to a
publisher that must never stop.  Instead the scorer combines the signals the
pipeline already has:

* freshness of the source post,
* price versus the same product's history,
* source-channel yield (EWMA learned from real outcomes),
* category yield (same),
* title quality (length, model number, spam markers),
* coupon / coins incentive,
* novelty versus recently published titles,
* channel saturation / flood pressure,
* explicit restock and price-drop exceptions.

The result is a 0-100 logistic score plus a signed contribution per signal,
so an operator can read exactly *why* a deal was published, held or skipped.
The model learns only from observed outcomes and stores bounded aggregates;
it never grows with traffic volume.

Public API
----------
``DealFeatures``      input dataclass
``IntelligenceModel`` persisted weights + learned statistics
``DealIntelligence``  score, record, observe, save/load
``extract_category``  title -> coarse category
"""

from __future__ import annotations

import json
import math
import os
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

MODEL_VERSION = "1.0.0"

# ---------------------------------------------------------------------------
# Tunables.  Persisted in the model file so a control loop can inspect them,
# but only the thresholds are ever changed automatically (see app/control).
# ---------------------------------------------------------------------------

DEFAULT_WEIGHTS: Dict[str, float] = {
    "freshness": 1.40,
    "price_edge": 1.30,
    "channel_reliability": 0.70,
    "category_value": 0.50,
    "title_quality": 0.80,
    "incentive": 0.60,
    "novelty": 0.90,
    "flow_pressure": 0.70,
    "restock_bonus": 0.50,
    "price_drop_bonus": 0.80,
    "coupon_list_bonus": 0.40,
}

DEFAULT_THRESHOLDS: Dict[str, float] = {
    "publish": 60.0,
    "skip": 38.0,
}

DEFAULT_TEMPERATURE = 2.2
DEFAULT_BIAS = 0.0
FLOW_WINDOW_HOURS = 6.0
FLOW_TARGET = 24.0  # posts per window that count as full saturation

# EWMA learning rate for channel / category yield.
EWMA_ALPHA = 0.08
# Number of pseudo-observations of the 0.5 prior (keeps small samples honest).
PRIOR_STRENGTH = 5.0

MAX_PRODUCT_PRICE_HISTORY = 10
MAX_PRODUCT_ENTRIES = 500
MAX_RECENT_DECISIONS = 200
MAX_TITLE_HISTORY = 200

_CATEGORY_KEYWORDS: Tuple[Tuple[str, Tuple[str, ...]], ...] = (
    ("phones", (
        "phone", "smartphone", "mobile", "xiaomi", "redmi", "poco", "realme",
        "samsung", "galaxy", "iphone", "oppo", "vivo", "infinix", "tecno",
        "honor", "oneplus", "5g", "هاتف", "جوال", "هواتف",
    )),
    ("audio", (
        "headphone", "headset", "earphone", "earbud", "airpod", "tws",
        "speaker", "soundbar", "microphone", "mic ", "سماعة", "سماعات",
    )),
    ("pc", (
        "laptop", "notebook", "ssd", "hdd", "ram ", "ddr", "gpu", "graphics",
        "rtx", "gtx", "radeon", "cpu", "processor", "motherboard", "monitor",
        "keyboard", "mouse", "gaming", "pc ", "لابتوب", "كمبيوتر",
    )),
    ("accessories", (
        "charger", "charging", "cable", "power bank", "powerbank", "adapter",
        "case", "cover", "protector", "hub", "dock", "stand", "شاحن", "كابل",
    )),
    ("home", (
        "vacuum", "robot", "kitchen", "blender", "air fryer", "fan", "heater",
        "lamp", "led ", "tool", "drill", "camera", "watch", "ساعة", "كاميرا",
    )),
)

_SPAM_MARKERS = (
    "giveaway", "freebie", "click here", "join now", "whatsapp",
    "telegram.me", "t.me/", "promo code in bio", "100% free",
    "مسابقة", "مجانا", "مجاناً",
)

_MODEL_TOKEN_RE = re.compile(
    r"\b(?:[A-Za-z]{1,5}[- ]?\d{1,5}[A-Za-z]{0,3}|\d{1,3}(?:\.\d+)?\s?(?:gb|tb|mah|w|hz|inch|\"))\b",
    re.IGNORECASE,
)

_WORD_RE = re.compile(r"[a-z0-9\u0600-\u06FF]+", re.IGNORECASE)


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def extract_category(title: str) -> str:
    """Map a product title to a coarse category. Deterministic keyword scan."""
    text = f" {(title or '').lower()} "
    for category, keywords in _CATEGORY_KEYWORDS:
        for keyword in keywords:
            if keyword in text:
                return category
    return "other"


def _tokens(text: str) -> set:
    return {t.lower() for t in _WORD_RE.findall(text or "") if len(t) > 1}


def title_similarity(title_a: str, title_b: str) -> float:
    """Jaccard similarity over word tokens, used for novelty only."""
    a, b = _tokens(title_a), _tokens(title_b)
    if not a or not b:
        return 0.0
    return len(a & b) / float(len(a | b))


def novelty_score(title: str, recent_titles: Sequence[str]) -> float:
    """1.0 = completely new, 0.0 = identical to a recently published title."""
    if not title or not recent_titles:
        return 1.0
    worst = 0.0
    for previous in recent_titles[:MAX_TITLE_HISTORY]:
        worst = max(worst, title_similarity(title, previous))
        if worst >= 0.999:
            break
    return _clamp(1.0 - worst)


def title_quality(title: str) -> float:
    """Heuristic 0-1 quality of a product title.

    Rewards descriptive length and a recognisable model/spec token, penalises
    shouty or spammy titles.  Never returns 0 for a non-empty title.
    """
    cleaned = (title or "").strip()
    if not cleaned:
        return 0.0

    length = _clamp(len(cleaned) / 45.0)
    model_bonus = 1.0 if _MODEL_TOKEN_RE.search(cleaned) else 0.25

    words = _WORD_RE.findall(cleaned)
    token_score = _clamp(len(words) / 8.0)

    lower = cleaned.lower()
    spam_hits = sum(1 for marker in _SPAM_MARKERS if marker in lower)
    spam_penalty = _clamp(spam_hits * 0.35)

    letters = [c for c in cleaned if c.isalpha()]
    caps_ratio = (
        sum(1 for c in letters if c.isupper()) / float(len(letters))
        if letters else 0.0
    )
    caps_penalty = 0.4 if caps_ratio > 0.7 and len(letters) > 12 else 0.0

    score = (
        0.35 * length
        + 0.30 * model_bonus
        + 0.20 * token_score
        + 0.15 * (1.0 - spam_penalty)
        - caps_penalty
    )
    return _clamp(score)


def price_edge(
    price: Optional[float],
    previous_price: Optional[float] = None,
    history: Optional[Sequence[float]] = None,
) -> float:
    """0-1 signal where 1 means "unusually good price".

    * With a previous price for the same product, a large drop scores high and
      a price increase scores low.
    * Otherwise, position inside the product's own price history is used.
    * With no history the signal is neutral (0.5).
    """
    if price is None or price <= 0:
        return 0.5

    if previous_price is not None and previous_price > 0:
        change = (previous_price - price) / previous_price
        # -40% .. +40% maps to 0 .. 1 around a neutral 0.5
        return _clamp(0.5 + change / 0.8)

    cleaned = sorted(
        float(p) for p in (history or []) if p is not None and float(p) > 0
    )
    if len(cleaned) < 2:
        return 0.5

    # Fraction of historical prices at or above the current price.
    at_or_above = sum(1 for p in cleaned if p >= price)
    percentile = at_or_above / float(len(cleaned))
    return _clamp(0.25 + 0.75 * percentile)


@dataclass(frozen=True)
class DealFeatures:
    """Everything the scorer is allowed to see. No I/O, no hidden state."""

    channel: str = ""
    title: str = ""
    product_id: Optional[str] = None
    price: Optional[float] = None
    previous_price: Optional[float] = None
    price_history: Tuple[float, ...] = ()
    message_age_hours: Optional[float] = None
    has_coupon: bool = False
    has_points_discount: bool = False
    is_restock: bool = False
    is_price_drop: bool = False
    is_coupon_list: bool = False
    deal_type: str = "coin"
    posts_last_window: int = 0
    recent_titles: Tuple[str, ...] = ()
    category: str = "other"


@dataclass
class Reason:
    code: str
    label: str
    impact: float
    detail: str = ""

    def as_text(self) -> str:
        sign = "+" if self.impact >= 0 else ""
        base = f"{self.code} {sign}{self.impact:.2f}"
        return f"{base} ({self.detail})" if self.detail else base

    def to_dict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "label": self.label,
            "impact": round(self.impact, 4),
            "detail": self.detail,
        }


@dataclass
class Decision:
    score: float
    verdict: str  # publish | hold | skip
    reasons: List[Reason] = field(default_factory=list)
    features: Dict[str, float] = field(default_factory=dict)
    model_version: str = MODEL_VERSION
    thresholds: Dict[str, float] = field(default_factory=dict)

    def summary(self) -> str:
        parts = " | ".join(r.as_text() for r in self.reasons)
        return (
            f"score={self.score:.1f} verdict={self.verdict} "
            f"(publish>={self.thresholds.get('publish', 0):.0f}, "
            f"skip<{self.thresholds.get('skip', 0):.0f}) | {parts}"
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "score": round(self.score, 2),
            "verdict": self.verdict,
            "reasons": [r.to_dict() for r in self.reasons],
            "features": {k: round(v, 4) for k, v in self.features.items()},
            "model_version": self.model_version,
            "thresholds": {k: round(v, 2) for k, v in self.thresholds.items()},
        }


@dataclass
class _Stat:
    seen: int = 0
    published: int = 0
    skipped: int = 0
    ewma: float = 0.5

    def reliability(self) -> float:
        """EWMA shrunk toward the 0.5 prior for small samples."""
        return (
            self.ewma * self.seen + 0.5 * PRIOR_STRENGTH
        ) / float(self.seen + PRIOR_STRENGTH)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "seen": self.seen,
            "published": self.published,
            "skipped": self.skipped,
            "ewma": round(self.ewma, 4),
        }

    @classmethod
    def from_dict(cls, raw: Dict[str, Any]) -> "_Stat":
        return cls(
            seen=max(0, int(raw.get("seen", 0) or 0)),
            published=max(0, int(raw.get("published", 0) or 0)),
            skipped=max(0, int(raw.get("skipped", 0) or 0)),
            ewma=_clamp(float(raw.get("ewma", 0.5) or 0.5)),
        )


class IntelligenceModel:
    """Persisted weights, thresholds and bounded learned statistics."""

    def __init__(self, data: Optional[Dict[str, Any]] = None):
        data = data or {}
        self.version: str = str(data.get("version") or MODEL_VERSION)
        self.weights: Dict[str, float] = dict(DEFAULT_WEIGHTS)
        for key, value in (data.get("weights") or {}).items():
            if key in self.weights:
                try:
                    self.weights[key] = float(value)
                except (TypeError, ValueError):
                    pass
        self.thresholds: Dict[str, float] = dict(DEFAULT_THRESHOLDS)
        for key, value in (data.get("thresholds") or {}).items():
            if key in self.thresholds:
                try:
                    self.thresholds[key] = float(value)
                except (TypeError, ValueError):
                    pass
        self.temperature: float = max(
            0.5, float(data.get("temperature", DEFAULT_TEMPERATURE) or DEFAULT_TEMPERATURE)
        )
        self.bias: float = float(data.get("bias", DEFAULT_BIAS) or DEFAULT_BIAS)
        self.flow_target: float = max(
            1.0, float(data.get("flow_target", FLOW_TARGET) or FLOW_TARGET)
        )
        self.channel_stats: Dict[str, _Stat] = {
            str(k): _Stat.from_dict(v)
            for k, v in (data.get("channel_stats") or {}).items()
            if isinstance(v, dict)
        }
        self.category_stats: Dict[str, _Stat] = {
            str(k): _Stat.from_dict(v)
            for k, v in (data.get("category_stats") or {}).items()
            if isinstance(v, dict)
        }
        self.product_prices: Dict[str, List[float]] = {}
        for key, values in (data.get("product_prices") or {}).items():
            if isinstance(values, list):
                cleaned = []
                for value in values[-MAX_PRODUCT_PRICE_HISTORY:]:
                    try:
                        number = float(value)
                    except (TypeError, ValueError):
                        continue
                    if number > 0:
                        cleaned.append(number)
                if cleaned:
                    self.product_prices[str(key)] = cleaned
        self.counters: Dict[str, int] = {
            "scored": int((data.get("counters") or {}).get("scored", 0) or 0),
            "verdict_publish": int((data.get("counters") or {}).get("verdict_publish", 0) or 0),
            "verdict_hold": int((data.get("counters") or {}).get("verdict_hold", 0) or 0),
            "verdict_skip": int((data.get("counters") or {}).get("verdict_skip", 0) or 0),
            "published": int((data.get("counters") or {}).get("published", 0) or 0),
            "skipped": int((data.get("counters") or {}).get("skipped", 0) or 0),
        }
        self.score_sum: float = float(data.get("score_sum", 0.0) or 0.0)
        self.recent_decisions: List[Dict[str, Any]] = [
            d for d in (data.get("recent_decisions") or []) if isinstance(d, dict)
        ][-MAX_RECENT_DECISIONS:]
        self.updated_at: float = float(data.get("updated_at", 0.0) or 0.0)

        self._normalise_thresholds()

    # -- persistence -------------------------------------------------------

    @classmethod
    def load(cls, path: Path) -> "IntelligenceModel":
        """Load a model, falling back to defaults on any corruption."""
        if not path.exists():
            return cls()
        try:
            with open(path, "r", encoding="utf-8") as handle:
                raw = json.load(handle)
            if not isinstance(raw, dict):
                return cls()
            return cls(raw)
        except Exception:
            return cls()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "weights": {k: round(v, 4) for k, v in self.weights.items()},
            "thresholds": {k: round(v, 2) for k, v in self.thresholds.items()},
            "temperature": round(self.temperature, 4),
            "bias": round(self.bias, 4),
            "flow_target": round(self.flow_target, 2),
            "channel_stats": {k: v.to_dict() for k, v in self.channel_stats.items()},
            "category_stats": {k: v.to_dict() for k, v in self.category_stats.items()},
            "product_prices": {
                k: [round(p, 4) for p in v] for k, v in self.product_prices.items()
            },
            "counters": dict(self.counters),
            "score_sum": round(self.score_sum, 2),
            "recent_decisions": self.recent_decisions[-MAX_RECENT_DECISIONS:],
            "updated_at": self.updated_at,
        }

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".tmp")
        with open(tmp, "w", encoding="utf-8") as handle:
            json.dump(self.to_dict(), handle, indent=2, ensure_ascii=False)
        os.replace(tmp, path)

    # -- thresholds --------------------------------------------------------

    def _normalise_thresholds(self) -> None:
        publish = _clamp(float(self.thresholds.get("publish", 60.0)), 40.0, 90.0)
        skip = _clamp(float(self.thresholds.get("skip", 38.0)), 10.0, 85.0)
        if skip > publish - 5.0:
            skip = max(10.0, publish - 5.0)
        self.thresholds = {"publish": publish, "skip": skip}

    def apply_overrides(self, overrides: Optional[Dict[str, Any]]) -> None:
        """Apply bounded runtime overrides from the Phase-3 control loop."""
        if not overrides or not overrides.get("enabled", True):
            return
        thresholds = overrides.get("thresholds") or {}
        if not isinstance(thresholds, dict):
            return
        if "publish" in thresholds:
            try:
                self.thresholds["publish"] = float(thresholds["publish"])
            except (TypeError, ValueError):
                pass
        if "skip" in thresholds:
            try:
                self.thresholds["skip"] = float(thresholds["skip"])
            except (TypeError, ValueError):
                pass
        if "flow_target" in thresholds:
            try:
                self.flow_target = max(1.0, float(thresholds["flow_target"]))
            except (TypeError, ValueError):
                pass
        self._normalise_thresholds()

    # -- feature stats -----------------------------------------------------

    def _stat(self, mapping: Dict[str, _Stat], key: str) -> _Stat:
        clean = (key or "unknown").strip().lower().lstrip("@") or "unknown"
        return mapping.setdefault(clean, _Stat())

    def channel_reliability(self, channel: str) -> float:
        return self._stat(self.channel_stats, channel).reliability()

    def category_value(self, category: str) -> float:
        return self._stat(self.category_stats, category).reliability()

    def remember_price(self, product_id: Optional[str], price: Optional[float]) -> None:
        if not product_id or price is None or price <= 0:
            return
        key = str(product_id)
        history = self.product_prices.setdefault(key, [])
        history.append(float(price))
        self.product_prices[key] = history[-MAX_PRODUCT_PRICE_HISTORY:]
        if len(self.product_prices) > MAX_PRODUCT_ENTRIES:
            # Drop the oldest inserted keys (dicts preserve insertion order).
            excess = len(self.product_prices) - MAX_PRODUCT_ENTRIES
            for old_key in list(self.product_prices.keys())[:excess]:
                self.product_prices.pop(old_key, None)


class DealIntelligence:
    """Scores deals and learns bounded channel/category statistics."""

    def __init__(
        self,
        model: Optional[IntelligenceModel] = None,
        model_path: Optional[Path] = None,
        persist: bool = True,
    ):
        self.model = model or IntelligenceModel()
        self.model_path = Path(model_path) if model_path else None
        self.persist = bool(persist and self.model_path)

    # -- scoring -----------------------------------------------------------

    def score(self, features: DealFeatures) -> Decision:
        model = self.model
        weights = model.weights

        category_key = features.category if features.category else ""
        if not category_key or category_key == "other":
            category_key = extract_category(features.title)

        freshness = (
            0.7
            if features.message_age_hours is None
            else _clamp(1.0 - max(0.0, float(features.message_age_hours)) / 18.0)
        )
        edge = price_edge(
            features.price, features.previous_price, features.price_history
        )
        reliability = model.channel_reliability(features.channel)
        category = model.category_value(category_key)
        quality = title_quality(features.title)
        novelty = novelty_score(features.title, features.recent_titles)

        incentive = 0.0
        if features.is_coupon_list:
            incentive = 0.8
        else:
            if features.has_coupon:
                incentive += 0.5
            if features.has_points_discount:
                incentive += 0.5
        incentive = _clamp(incentive)

        pressure = _clamp(
            max(0.0, float(features.posts_last_window)) / model.flow_target
        )

        values = {
            "freshness": freshness,
            "price_edge": edge,
            "channel_reliability": reliability,
            "category_value": category,
            "title_quality": quality,
            "incentive": incentive,
            "novelty": novelty,
            "flow_pressure": pressure,
        }

        reasons: List[Reason] = []

        def symmetric(code: str, label: str, value: float, detail: str = "") -> None:
            impact = weights[code] * (2.0 * value - 1.0)
            reasons.append(Reason(code, label, impact, detail))

        age_detail = (
            "unknown age"
            if features.message_age_hours is None
            else f"{max(0.0, features.message_age_hours):.1f}h old"
        )
        symmetric("freshness", "freshness", freshness, age_detail)

        if features.previous_price and features.price and features.previous_price > 0:
            change = (features.previous_price - features.price) / features.previous_price
            price_detail = (
                f"${features.previous_price:.2f} -> ${features.price:.2f} "
                f"({change:+.0%})"
            )
        elif features.price_history:
            price_detail = f"${features.price:.2f} vs {len(features.price_history)} prior"
        else:
            price_detail = "no price history"
        symmetric("price_edge", "price edge", edge, price_detail)

        symmetric(
            "channel_reliability",
            "channel yield",
            reliability,
            f"@{features.channel or 'unknown'}",
        )
        symmetric("category_value", "category value", category, category_key)
        symmetric("title_quality", "title quality", quality)
        symmetric("incentive", "incentive", incentive)
        symmetric("novelty", "novelty", novelty)

        flow_impact = -weights["flow_pressure"] * pressure
        reasons.append(
            Reason(
                "flow_pressure",
                "saturation",
                flow_impact,
                f"{features.posts_last_window} posts/{FLOW_WINDOW_HOURS:.0f}h",
            )
        )

        if features.is_restock:
            reasons.append(
                Reason("restock_bonus", "restock", weights["restock_bonus"], "announced")
            )
        if features.is_price_drop:
            reasons.append(
                Reason(
                    "price_drop_bonus",
                    "price drop",
                    weights["price_drop_bonus"],
                    "exception",
                )
            )
        if features.is_coupon_list:
            reasons.append(
                Reason(
                    "coupon_list_bonus",
                    "coupon list",
                    weights["coupon_list_bonus"],
                    "bulletin",
                )
            )

        z = model.bias + sum(reason.impact for reason in reasons)
        raw = 100.0 / (1.0 + math.exp(-z / model.temperature))
        score = round(_clamp(raw, 0.0, 100.0), 2)

        if score >= model.thresholds["publish"]:
            verdict = "publish"
        elif score < model.thresholds["skip"]:
            verdict = "skip"
        else:
            verdict = "hold"

        reasons.sort(key=lambda r: abs(r.impact), reverse=True)
        return Decision(
            score=score,
            verdict=verdict,
            reasons=reasons,
            features=values,
            model_version=model.version,
            thresholds=dict(model.thresholds),
        )

    # -- learning ----------------------------------------------------------

    def record_decision(
        self,
        decision: Decision,
        features: DealFeatures,
    ) -> None:
        """Counters + bounded decision log used by the Phase-3 control loop."""
        model = self.model
        model.counters["scored"] += 1
        model.score_sum += decision.score
        if decision.verdict == "publish":
            model.counters["verdict_publish"] += 1
        elif decision.verdict == "skip":
            model.counters["verdict_skip"] += 1
        else:
            model.counters["verdict_hold"] += 1

        model.recent_decisions.append(
            {
                "ts": int(time.time()),
                "channel": (features.channel or "").lower().lstrip("@"),
                "category": features.category,
                "product_id": str(features.product_id) if features.product_id else None,
                "score": decision.score,
                "verdict": decision.verdict,
            }
        )
        model.recent_decisions = model.recent_decisions[-MAX_RECENT_DECISIONS:]
        model.updated_at = time.time()
        self.save()

    def observe(
        self,
        channel: str,
        category: str,
        outcome: str,
        count_seen: bool = True,
    ) -> None:
        """Update learned yield. ``outcome`` is published/skipped/seen.

        ``count_seen`` lets the gate count each candidate exactly once and then
        attach the real outcome later without inflating the sample size.
        """
        clean_channel = (channel or "unknown").strip().lower().lstrip("@") or "unknown"
        clean_category = (category or "other").strip().lower() or "other"
        target: Optional[float] = None
        if outcome == "published":
            target = 1.0
        elif outcome == "skipped":
            target = 0.0

        for mapping, key in (
            (self.model.channel_stats, clean_channel),
            (self.model.category_stats, clean_category),
        ):
            stat = mapping.setdefault(key, _Stat())
            if count_seen:
                stat.seen += 1
            if target is not None:
                if target >= 1.0:
                    stat.published += 1
                else:
                    stat.skipped += 1
                stat.ewma = _clamp((1.0 - EWMA_ALPHA) * stat.ewma + EWMA_ALPHA * target)

        if outcome == "published":
            self.model.counters["published"] += 1
        elif outcome == "skipped":
            self.model.counters["skipped"] += 1

        self.model.updated_at = time.time()
        self.save()

    def remember_price(self, product_id: Optional[str], price: Optional[float]) -> None:
        self.model.remember_price(product_id, price)
        self.save()

    # -- persistence -------------------------------------------------------

    def save(self) -> None:
        if not self.persist or self.model_path is None:
            return
        try:
            self.model.save(self.model_path)
        except Exception:
            # A learning write must never break publishing.
            pass

    @classmethod
    def load(
        cls,
        model_path: Optional[Path] = None,
        overrides: Optional[Dict[str, Any]] = None,
        persist: bool = True,
    ) -> "DealIntelligence":
        path = Path(model_path) if model_path else None
        model = IntelligenceModel.load(path) if path else IntelligenceModel()
        model.apply_overrides(overrides)
        return cls(model=model, model_path=path, persist=persist)

    def snapshot(self) -> Dict[str, Any]:
        model = self.model
        scored = max(1, model.counters["scored"])
        return {
            "version": model.version,
            "thresholds": dict(model.thresholds),
            "counters": dict(model.counters),
            "average_score": round(model.score_sum / scored, 2),
            "channels": {k: v.to_dict() for k, v in model.channel_stats.items()},
            "categories": {k: v.to_dict() for k, v in model.category_stats.items()},
            "updated_at": model.updated_at,
        }

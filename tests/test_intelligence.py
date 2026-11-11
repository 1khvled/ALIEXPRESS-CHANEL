"""Tests for the deterministic deal intelligence (no LLM, no network).

Every test is offline and uses a temporary model path, so the suite can never
dirty ``storage/state/intelligence_model.json`` or the production state file.
"""

import json
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from pathlib import Path

import pytest

from app.intelligence import gate as gate_module
from app.intelligence.gate import GateResult, evaluate_deal_gate, record_published_outcome
from app.intelligence.scoring import (
    DEFAULT_WEIGHTS,
    DealFeatures,
    DealIntelligence,
    IntelligenceModel,
    extract_category,
    novelty_score,
    price_edge,
    title_quality,
)


# ---------------------------------------------------------------------------
# Feature helpers
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "title, expected",
    [
        ("Xiaomi Redmi Note 13 Pro 5G 8GB 256GB", "phones"),
        ("Samsung Galaxy S24 Ultra 12GB 512GB", "phones"),
        ("Bluetooth TWS Earbuds Airpods Pro 2", "audio"),
        ("RTX 4060 Gaming Laptop 16GB DDR5", "pc"),
        ("65W GaN Charger USB C Cable", "accessories"),
        ("Robot Vacuum Cleaner Smart Home", "home"),
        ("Stainless Steel Water Bottle 1L", "other"),
        ("", "other"),
    ],
)
def test_extract_category(title, expected):
    assert extract_category(title) == expected


def test_title_quality_rewards_model_numbers():
    detailed = "Xiaomi Redmi Note 13 Pro 5G 8GB 256GB Global Version"
    vague = "HOT SALE!!! CLICK NOW"
    assert title_quality(detailed) > title_quality(vague)
    assert 0.0 <= title_quality("") <= 1.0
    assert 0.0 <= title_quality(vague) <= 1.0


def test_title_quality_penalises_spam_markers():
    clean = "Samsung Galaxy S24 Ultra 12GB 512GB Smartphone"
    spam = "Samsung Galaxy S24 Ultra 12GB 512GB Smartphone giveaway click here"
    assert title_quality(clean) > title_quality(spam)


def test_novelty_is_zero_for_identical_title():
    title = "Xiaomi Redmi Note 13 Pro 5G 8GB 256GB"
    assert novelty_score(title, [title]) == pytest.approx(0.0, abs=1e-6)
    assert novelty_score(title, []) == 1.0
    assert novelty_score(title, ["Completely different product title here"]) > 0.5


def test_price_edge_prefers_a_drop_over_an_increase():
    assert price_edge(80.0, previous_price=100.0) > 0.5
    assert price_edge(120.0, previous_price=100.0) < 0.5
    assert price_edge(None) == 0.5
    assert price_edge(100.0, previous_price=None, history=[]) == 0.5


def test_price_edge_uses_history_percentile():
    cheapest = price_edge(50.0, history=[50.0, 80.0, 100.0])
    most_expensive = price_edge(100.0, history=[50.0, 80.0, 100.0])
    assert cheapest > most_expensive


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------


def _good_features(**overrides):
    base = dict(
        channel="lodydeals",
        title="Xiaomi Redmi Note 13 Pro 5G 8GB 256GB Global Version",
        product_id="1005001",
        price=199.0,
        previous_price=259.0,
        message_age_hours=0.5,
        has_coupon=True,
        has_points_discount=True,
        posts_last_window=1,
        recent_titles=("Some other phone deal",),
        category="phones",
    )
    base.update(overrides)
    return DealFeatures(**base)


def test_score_is_deterministic():
    engine = DealIntelligence()
    features = _good_features()
    first = engine.score(features)
    second = engine.score(features)
    assert first.score == second.score
    assert first.verdict == second.verdict
    assert [r.code for r in first.reasons] == [r.code for r in second.reasons]


def test_fresh_strong_deal_beats_stale_weak_deal():
    engine = DealIntelligence()
    strong = engine.score(_good_features())
    weak = engine.score(
        DealFeatures(
            channel="unknown",
            title="HOT SALE!!! CLICK NOW",
            price=99.0,
            previous_price=100.0,
            message_age_hours=17.5,
            has_coupon=False,
            has_points_discount=False,
            posts_last_window=40,
            recent_titles=("HOT SALE!!! CLICK NOW",),
        )
    )
    assert strong.score > weak.score
    assert strong.verdict == "publish"
    assert weak.verdict == "skip"


def test_flow_pressure_lowers_score():
    engine = DealIntelligence()
    quiet = engine.score(_good_features(posts_last_window=0))
    flooded = engine.score(_good_features(posts_last_window=48))
    assert flooded.score < quiet.score
    assert any(r.code == "flow_pressure" for r in flooded.reasons)


def test_identical_recent_title_lowers_novelty_score():
    engine = DealIntelligence()
    fresh_title = engine.score(_good_features(recent_titles=()))
    repeated_title = engine.score(
        _good_features(recent_titles=(_good_features().title,))
    )
    assert repeated_title.score < fresh_title.score


def test_restock_and_price_drop_add_bonuses():
    engine = DealIntelligence()
    plain = engine.score(_good_features(is_restock=False, is_price_drop=False))
    boosted = engine.score(_good_features(is_restock=True, is_price_drop=True))
    assert boosted.score > plain.score
    codes = {r.code for r in boosted.reasons}
    assert "restock_bonus" in codes
    assert "price_drop_bonus" in codes


def test_score_always_within_bounds():
    engine = DealIntelligence()
    cases = [
        DealFeatures(),
        DealFeatures(title="x" * 500, price=0.01, message_age_hours=1000),
        DealFeatures(price=-5, previous_price=0, posts_last_window=10**6),
        _good_features(posts_last_window=0, price_history=(10.0, 20.0)),
    ]
    for features in cases:
        decision = engine.score(features)
        assert 0.0 <= decision.score <= 100.0
        assert decision.verdict in {"publish", "hold", "skip"}


def test_thresholds_produce_verdicts():
    model = IntelligenceModel()
    model.thresholds = {"publish": 90.0, "skip": 85.0}
    model._normalise_thresholds()
    engine = DealIntelligence(model=model)
    assert engine.score(_good_features()).verdict in {"hold", "skip"}

    model.thresholds = {"publish": 40.0, "skip": 10.0}
    model._normalise_thresholds()
    assert engine.score(_good_features()).verdict == "publish"


# ---------------------------------------------------------------------------
# Model persistence and learning
# ---------------------------------------------------------------------------


def test_model_persists_and_reloads(tmp_path):
    path = tmp_path / "model.json"
    engine = DealIntelligence(model_path=path)
    engine.observe("lodydeals", "phones", "published")
    engine.remember_price("1005001", 199.0)
    engine.record_decision(engine.score(_good_features()), _good_features())

    assert path.exists()
    reloaded = DealIntelligence.load(path)
    assert reloaded.model.counters["published"] == 1
    assert reloaded.model.product_prices["1005001"] == [199.0]
    assert reloaded.model.channel_stats["lodydeals"].published == 1


def test_corrupt_model_falls_back_to_defaults(tmp_path):
    path = tmp_path / "model.json"
    path.write_text("{not valid json", encoding="utf-8")
    model = IntelligenceModel.load(path)
    assert model.weights == DEFAULT_WEIGHTS
    assert model.thresholds["publish"] == 60.0


def test_learning_raises_channel_reliability():
    engine = DealIntelligence()
    before = engine.model.channel_reliability("lodydeals")
    for _ in range(20):
        engine.observe("lodydeals", "phones", "published")
    after = engine.model.channel_reliability("lodydeals")
    assert after > before


def test_learning_lowers_reliability_for_skipped_channel():
    engine = DealIntelligence()
    for _ in range(20):
        engine.observe("noisy", "other", "skipped")
    assert engine.model.channel_reliability("noisy") < 0.5


def test_control_overrides_are_bounded():
    model = IntelligenceModel()
    model.apply_overrides({"enabled": True, "thresholds": {"publish": 500, "skip": -20}})
    assert model.thresholds["publish"] == 90.0
    assert model.thresholds["skip"] >= 10.0
    assert model.thresholds["skip"] <= model.thresholds["publish"] - 5.0

    model.apply_overrides({"enabled": False, "thresholds": {"publish": 45}})
    assert model.thresholds["publish"] == 90.0


def test_model_storage_is_bounded(tmp_path):
    path = tmp_path / "model.json"
    engine = DealIntelligence(model_path=path)
    for index in range(600):
        engine.remember_price(f"pid-{index}", 10.0 + index)
    assert len(engine.model.product_prices) <= 500
    assert len(engine.model.product_prices["pid-599"]) == 1


# ---------------------------------------------------------------------------
# Publisher gate
# ---------------------------------------------------------------------------


def _extracted(**overrides):
    base = dict(
        product_id="1005001",
        title="Xiaomi Redmi Note 13 Pro 5G 8GB 256GB Global Version",
        current_price=199.0,
        coupon_code="DZ10",
        seller_coupon=None,
        has_points_discount=True,
        is_coupon_list=False,
        deal_type="coin",
    )
    base.update(overrides)
    return SimpleNamespace(**base)


def _write_model(path: Path, publish=60.0, skip=38.0):
    model = IntelligenceModel()
    model.thresholds = {"publish": publish, "skip": skip}
    model._normalise_thresholds()
    path.write_text(json.dumps(model.to_dict()), encoding="utf-8")


@pytest.fixture
def gate_env(tmp_path, monkeypatch):
    monkeypatch.setattr(gate_module, "load_persistent_state", lambda: {})
    monkeypatch.setattr(gate_module.settings, "INTELLIGENCE_MODE", "shadow")
    model_path = tmp_path / "model.json"
    control_path = tmp_path / "control.json"
    monkeypatch.setattr(gate_module.settings, "INTELLIGENCE_MODEL_PATH", str(model_path))
    monkeypatch.setattr(gate_module.settings, "INTELLIGENCE_CONTROL_PATH", str(control_path))
    return model_path, control_path


def test_gate_shadow_always_allows(gate_env):
    model_path, _ = gate_env
    _write_model(model_path, publish=95.0, skip=90.0)
    result = evaluate_deal_gate(
        extracted=_extracted(),
        channel="lodydeals",
        message_dt=datetime.now(timezone.utc) - timedelta(hours=1),
        persist=True,
    )
    assert result.mode == "shadow"
    assert result.allowed is True
    assert result.decision is not None
    assert result.verdict == "skip"  # scored low, but shadow does not enforce


def test_gate_enforce_blocks_skip(gate_env, monkeypatch):
    model_path, _ = gate_env
    _write_model(model_path, publish=95.0, skip=90.0)
    monkeypatch.setattr(gate_module.settings, "INTELLIGENCE_MODE", "enforce")

    result = evaluate_deal_gate(
        extracted=_extracted(),
        channel="lodydeals",
        message_dt=datetime.now(timezone.utc) - timedelta(hours=1),
        persist=True,
    )
    assert result.allowed is False
    assert result.verdict == "skip"


def test_gate_enforce_hold_action_can_skip(gate_env, monkeypatch):
    model_path, _ = gate_env
    # A wide band guarantees "hold" for the good fixture deal.
    _write_model(model_path, publish=99.0, skip=1.0)
    monkeypatch.setattr(gate_module.settings, "INTELLIGENCE_MODE", "enforce")
    monkeypatch.setattr(gate_module.settings, "INTELLIGENCE_HOLD_ACTION", "skip")

    result = evaluate_deal_gate(
        extracted=_extracted(),
        channel="lodydeals",
        message_dt=datetime.now(timezone.utc) - timedelta(hours=1),
        persist=True,
    )
    assert result.verdict == "hold"
    assert result.allowed is False


def test_gate_fails_open_on_state_error(gate_env, monkeypatch):
    monkeypatch.setattr(
        gate_module,
        "load_persistent_state",
        lambda: (_ for _ in ()).throw(RuntimeError("state unavailable")),
    )
    result = evaluate_deal_gate(extracted=_extracted(), channel="lodydeals")
    assert result.allowed is True
    assert result.decision is None
    assert "state unavailable" in (result.error or "")


def test_gate_off_does_not_score(gate_env, monkeypatch):
    monkeypatch.setattr(gate_module.settings, "INTELLIGENCE_MODE", "off")
    result = evaluate_deal_gate(extracted=_extracted(), channel="lodydeals")
    assert result.allowed is True
    assert result.decision is None
    assert result.mode == "off"


def test_record_published_outcome_updates_model(gate_env):
    model_path, _ = gate_env
    result = evaluate_deal_gate(
        extracted=_extracted(),
        channel="lodydeals",
        message_dt=datetime.now(timezone.utc) - timedelta(hours=1),
        persist=True,
    )
    assert isinstance(result, GateResult)
    record_published_outcome(result)

    reloaded = DealIntelligence.load(model_path)
    assert reloaded.model.counters["published"] == 1
    assert reloaded.model.product_prices["1005001"] == [199.0]
    assert reloaded.model.channel_stats["lodydeals"].published == 1

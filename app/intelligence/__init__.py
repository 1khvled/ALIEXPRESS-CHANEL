"""Deterministic deal intelligence package.

No LLM, no network, no external inference service.  See ``scoring`` for the
pure algorithm and ``gate`` for the publisher integration.
"""

from app.intelligence.scoring import (  # noqa: F401
    DEFAULT_THRESHOLDS,
    DEFAULT_WEIGHTS,
    MODEL_VERSION,
    DealFeatures,
    DealIntelligence,
    Decision,
    IntelligenceModel,
    Reason,
    extract_category,
    novelty_score,
    price_edge,
    title_quality,
)

__all__ = [
    "DEFAULT_THRESHOLDS",
    "DEFAULT_WEIGHTS",
    "MODEL_VERSION",
    "DealFeatures",
    "DealIntelligence",
    "Decision",
    "IntelligenceModel",
    "Reason",
    "extract_category",
    "novelty_score",
    "price_edge",
    "title_quality",
]

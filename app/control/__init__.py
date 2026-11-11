"""Deterministic closed-loop control for the DealScout runtime.

The public helpers live in :mod:`app.control.controller`.  Nothing is imported
eagerly here on purpose: the module is also the documented CLI entry point
(``python -m app.control.controller``), and an eager import makes ``runpy``
emit a "found in sys.modules" warning.  ``__getattr__`` keeps the convenient
``from app.control import propose`` form working without that side effect.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "BOUNDS",
    "apply_proposal",
    "assess_health",
    "build_control_state",
    "collect_metrics",
    "propose",
    "render_markdown",
]


def __getattr__(name: str) -> Any:  # pragma: no cover - trivial delegation
    if name in __all__:
        from app.control import controller

        return getattr(controller, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

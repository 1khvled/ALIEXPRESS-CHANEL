"""Static gate: shipped code must not contain undefined names.

Why this exists
---------------
Two production outages were plain ``NameError``s that every existing test
missed, because the failing call sat inside a ``except Exception`` that
swallowed the error and left the feature silently doing nothing:

1. Oct 2026, ``fb7cbfe``: ``Tuple``/``Any`` used in annotations without
   being imported. Both publishers crashed at import time on every cron
   run for three days while Actions stayed green (see
   ``.agents/rules/publish_safety.md``).
2. Nov 2026: ``scripts/post_recent_deals.py`` called ``json.dumps`` and
   incremented ``deals_published_this_run`` without ever importing or
   defining them. The coupon-restock publisher therefore never posted
   anything, and a roundup that *did* publish would have killed the run.

``python -m py_compile`` cannot catch either — they are runtime name
lookups, not syntax errors. ``pyflakes`` resolves names statically, so it
catches them in milliseconds with no network, no tokens and no database.

Only ``undefined name`` diagnostics are fatal here. Unused imports and
similar style findings are reported by pyflakes but deliberately not
gated, so this test cannot fail for cosmetic reasons.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGETS = ["app", "api", "scripts", "infra"]


def _run_pyflakes():
    return subprocess.run(
        [sys.executable, "-m", "pyflakes", *TARGETS],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def test_pyflakes_is_available():
    """The gate is useless if the checker is missing; fail loudly instead."""
    result = subprocess.run(
        [sys.executable, "-m", "pyflakes", "--version"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        "pyflakes is not installed. It is required by this gate "
        "(and by CI via requirements.txt)."
    )


def test_no_undefined_names_in_shipped_code():
    result = _run_pyflakes()

    # Never accept a crash of the checker itself as a pass.
    assert "No module named pyflakes" not in (result.stderr or ""), (
        "pyflakes could not be executed:\n" + (result.stderr or "")
    )

    undefined = [
        line for line in (result.stdout or "").splitlines()
        if "undefined name" in line
    ]

    assert not undefined, (
        "Undefined names found in shipped code. Each one is a latent "
        "NameError that will be swallowed by the try/except blocks in the "
        "publisher loops:\n  " + "\n  ".join(undefined)
    )

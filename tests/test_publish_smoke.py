"""Regression tests for the Oct 11-14 2026 outage (bot posted nothing for 3 days).

Catches without network or Telegram tokens:
1. Fatal NameError on import (missing `Tuple` in urls.py, missing `Any` in parser.py).
2. Undefined `target_channel` in scripts/post_france_deals.py (must be TARGET_FRANCE_CHANNEL).
3. Typing imports not covering annotations in critical modules.
4. Publisher scripts must at least byte-compile.
5. Fatal publisher crashes must alert the admin AND exit nonzero (so the
   workflow alert step can see the failure instead of staying silently green).
6. bot_cron.yml must keep the workflow-level admin alert step (catches
   import-time crashes that in-process code can never reach).
"""
import ast
import py_compile
from pathlib import Path

import pytest

BASE_DIR = Path(__file__).resolve().parent.parent

TYPING_NAMES = {"List", "Dict", "Tuple", "Optional", "Any", "Set", "Union"}


def _typing_imports(tree: ast.AST) -> set:
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "typing":
            for a in node.names:
                if a.name in TYPING_NAMES:
                    imported.add(a.name)
    return imported


def _annotation_names(tree: ast.AST) -> set:
    used = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id in TYPING_NAMES:
            used.add(node.id)
    return used


def test_core_modules_import():
    # Would have raised NameError: Tuple / Any before the fix.
    from app.aliexpress.urls import check_competitor_contamination  # noqa: F401
    from app.aliexpress.parser import is_spam_or_non_deal  # noqa: F401
    from app.aliexpress.product import product_extractor  # noqa: F401
    from app.aliexpress.affiliate import affiliate_service  # noqa: F401
    from app.ai.validator import caption_validator  # noqa: F401
    from app.publisher.publisher import telegram_publisher  # noqa: F401
    from app.publisher.state_tracker import load_persistent_state  # noqa: F401


def test_contamination_checker_runs():
    from app.aliexpress.urls import check_competitor_contamination
    ok, reason = check_competitor_contamination(
        caption="deal @Alilo07BOT @DzAliexpress0",
        url="https://s.click.aliexpress.com/e/_c3F40Fvf",
    )
    assert ok is False
    bad, _ = check_competitor_contamination(
        url="https://s.click.aliexpress.com/e/_c38iyTZR"
    )
    assert bad is True


def test_typing_imports_cover_annotations():
    for rel in ["app/aliexpress/urls.py", "app/aliexpress/parser.py"]:
        tree = ast.parse((BASE_DIR / rel).read_text(encoding="utf-8"))
        missing = _annotation_names(tree) - _typing_imports(tree)
        assert not missing, f"{rel} uses {sorted(missing)} without importing them"


def test_no_undefined_target_channel_in_france_publisher():
    src = (BASE_DIR / "scripts/post_france_deals.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    bare = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name) and n.id == "target_channel"}
    assert not bare, "scripts/post_france_deals.py still references undefined 'target_channel'"


def test_publisher_scripts_compile():
    for rel in ["scripts/post_recent_deals.py", "scripts/post_france_deals.py",
                "app/aliexpress/urls.py", "app/aliexpress/parser.py"]:
        py_compile.compile(str(BASE_DIR / rel), doraise=True)


def _main_except_body(rel: str) -> str:
    """Source of the __main__ try/except block of a publisher script."""
    tree = ast.parse((BASE_DIR / rel).read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.If) and any(
            isinstance(t, ast.Compare) and any(
                isinstance(c, ast.Constant) and c.value == "__main__"
                for c in [t.left, *t.comparators]
            ) for t in [node.test] if isinstance(t, ast.Compare)
        ):
            return ast.unparse(node)
    raise AssertionError(f"{rel}: no if __name__ == '__main__' block found")


def test_publisher_fatal_errors_alert_admin_and_exit_nonzero():
    # Oct 2026 lesson: Algeria exited 0 on FATAL with no alert -> the failure
    # was invisible. Both publishers must notify the admin and exit nonzero.
    for rel in ["scripts/post_recent_deals.py", "scripts/post_france_deals.py"]:
        body = _main_except_body(rel)
        assert "notify_admin_error" in body, f"{rel}: FATAL path must call notify_admin_error"
        assert "sys.exit(1)" in body, f"{rel}: FATAL path must exit nonzero (sys.exit(1))"
        assert "sys.exit(0)" not in body.split("except")[1], \
            f"{rel}: FATAL path must not exit 0"


def test_workflow_has_admin_failure_alert():
    yaml = pytest.importorskip("yaml")
    wf = yaml.safe_load((BASE_DIR / ".github/workflows/bot_cron.yml").read_text(encoding="utf-8"))
    steps = wf["jobs"]["run-deals-collector"]["steps"]
    by_name = {s.get("name"): s for s in steps}
    alg = by_name.get("Run Algeria Deals Publisher (@DzAliexpress0)", {})
    fr = by_name.get("Run France Deals Publisher (@francedealsdz)", {})
    alert = by_name.get("Notify admin on publisher failure")
    assert alg.get("id") == "algeria", "Algeria publisher step needs id: algeria"
    assert fr.get("id") == "france", "France publisher step needs id: france"
    assert alert is not None, "bot_cron.yml lost the admin failure alert step"
    cond = alert.get("if", "")
    assert "steps.algeria.outcome" in cond and "steps.france.outcome" in cond, \
        "alert step must check both publisher step outcomes"
    assert "ADMIN_BOT_TOKEN" in alert.get("run", "") and "ADMIN_USER_ID" in alert.get("run", ""), \
        "alert step must message the admin via ADMIN_BOT_TOKEN/ADMIN_USER_ID"


def test_workflow_has_test_alert_button():
    yaml = pytest.importorskip("yaml")
    wf = yaml.safe_load((BASE_DIR / ".github/workflows/bot_cron.yml").read_text(encoding="utf-8"))
    # NOTE: YAML 1.1 parses the unquoted `on:` key as boolean True.
    on = wf.get("on", wf.get(True))
    inputs = on["workflow_dispatch"]["inputs"]
    assert "test_alert" in inputs, "workflow_dispatch lost the test_alert input"
    steps = wf["jobs"]["run-deals-collector"]["steps"]
    by_name = {s.get("name"): s for s in steps}
    t = by_name.get("Send test admin alert (manual verification)")
    assert t is not None, "bot_cron.yml lost the test alert step"
    assert "test_alert" in t.get("if", ""), "test step must be gated on the test_alert input"
    assert '"ok":true' in t.get("run", ""), "test step must verify Telegram returned ok:true"

"""Regression tests for the Oct 11-14 2026 outage (bot posted nothing for 3 days).

Catches without network or Telegram tokens:
1. Fatal NameError on import (missing `Tuple` in urls.py, missing `Any` in parser.py).
2. Undefined `target_channel` in scripts/post_france_deals.py (must be TARGET_FRANCE_CHANNEL).
3. Typing imports not covering annotations in critical modules.
4. Publisher scripts must at least byte-compile.
"""
import ast
import py_compile
from pathlib import Path

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

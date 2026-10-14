---
trigger: always_on
description: Mandatory publish-safety rules learned from the Oct 11-14 2026 outage (bot posted nothing for 3 days).
---

# Publish-Safety Rules (MUST follow on every change)

## Incident (do NOT repeat)
- Oct 11 2026, commit `fb7cbfe` added `check_competitor_contamination()` to
  `app/aliexpress/urls.py` using `Tuple` in its signature, but the file only
  imported `from typing import List, Optional`. Result: `NameError: Tuple`
  on **every** `import app.aliexpress` -> BOTH publishers
  (`scripts/post_recent_deals.py`, `scripts/post_france_deals.py`) crashed
  with exit 1 on **every** scheduled run.
- Same era: `app/aliexpress/parser.py` used `Dict[str, Any]` without importing
  `Any` -> same fatal `NameError` once the first one was fixed.
- Same era: `scripts/post_france_deals.py:703` used undefined
  `channel_id=target_channel` (should be `TARGET_FRANCE_CHANNEL`) ->
  `NameError` whenever a coupon bulletin was processed during an active promo.
- `bot_cron.yml` had `continue-on-error: true`, so Actions stayed green
  (`success`) while both publishers exited 1. No state was written, no
  `Auto-update deals database` commits happened after Oct 11, head SHA froze.
- Fix commits: `712e681`. Trigger run `#2071 --force` + auto-commit `6a9c78a`
  proved recovery.

## Rules
1. **Typing imports MUST cover annotations.** If a signature uses
   `List/Dict/Tuple/Optional/Any/Set/Union`, that name MUST be in the
   `from typing import ...` line of the SAME file. Never assume it comes
   transitively from another module.
2. **No undefined / half-renamed variables.** After any rename (e.g.
   `target_channel` -> `TARGET_FRANCE_CHANNEL`), grep the file for the old
   name. `scripts/post_france_deals.py` and `scripts/post_recent_deals.py`
   must never reference a bare name that is not defined in that scope.
3. **Publisher crash = silent channel death.** Both publishers run
   unattended on cron. Any import-time `NameError` kills ALL posting.
   Treat `app/aliexpress/__init__.py`, `app/aliexpress/urls.py`,
   `app/aliexpress/parser.py` as critical path: they must import cleanly
   with zero side effects.
4. **Do NOT mask failures to stay green.** `continue-on-error: true` on the
   publisher steps hides exit 1. Keep it ONLY if a separate `pr_checks`
   workflow fails loudly on push/PR. If you touch `bot_cron.yml`, preserve
   loud failure semantics.
5. **Mandatory pre-commit checks** (run ALL of these before every commit
   touching `app/`, `api/`, or `scripts/`):
   - `python -m py_compile` on every changed `.py` file.
   - Import smoke: `from app.aliexpress.urls import
     check_competitor_contamination`, `from app.aliexpress.parser import
     is_spam_or_non_deal`, `from app.aliexpress.product import
     product_extractor`.
   - `pytest tests/test_publish_smoke.py -q` (fast, no network, no tokens).
   - Full `pytest tests/ -q` before merging anything that touches the
     firewall, validator, or publishers.
6. **Local `--force` runs need `python-aliexpress-api`.** CI installs it
   explicitly (`pip install python-aliexpress-api`). `api/coin_bot.py`
   imports `aliexpress_api` at module top; without the package every channel
   sweep logs `[ERROR] No module named 'aliexpress_api'`. Never remove that
   install step.
7. **Local test runs dirty `storage/state/*.json` + `deals.db`.** Always
   `git checkout -- storage` and delete `deals.db` / `*.tmp` after a local
   publisher run. Never commit local test state.

# Workspace Guidelines & Absolute Rules

## CRITICAL RULE: ZERO COMPETITOR LINKS OR HANDLES
Under NO circumstances may any post, message, caption, button, or link published to our Telegram channels (`@DzAliexpress0`, `@francedealsdz`) contain:
1. **Competitor Affiliate Links / Shortcodes**: E.g., `_c38iyTZR` or any external affiliate shortlink. Every single link MUST be monetized exclusively using our Portals API or our tracking ID (`dzkhvled16`).
2. **Competitor Telegram Channels / Handles**: E.g., `@ECKSDEAL`, `@lodydeals`, `@zedstoreonline`, `@aniscoupons`, `@pcgamingpart`, `@bnddeals`, `@megaprix`, `@francecp`, `@alifrdrop`, etc.
3. **Competitor Telegram Invite / Post Links**: E.g., `t.me/ecksdeal/...`, `t.me/lodydeals/...`, etc.
4. **Unauthorized External Bots**: The only authorized bot is our own `@Alilo07BOT`. Never promote or link other bots (e.g. coinbot GitHub links, dzgamingcoinbot, etc.).

All incoming posts from competitor channels MUST be scraped solely for raw deal information (product ID, prices, coupons) and MUST be 100% sanitized and re-monetized before publishing.
Violations are automatically rejected by the `caption_validator` and blocked by the channel publication firewall in `TelegramPublisher`.

## PUBLISH-SAFETY (Oct 11-14 2026 outage — never repeat)
Missing `Tuple`/`Any` typing imports + undefined `target_channel` crashed BOTH
publishers on every cron run for 3 days while `continue-on-error` kept Actions
green. Mandatory rules live in `.agents/rules/publish_safety.md`. CI gate:
`.github/workflows/pr_checks.yml` (strict, no `continue-on-error`).
Regression tests: `tests/test_publish_smoke.py`. Run them before every commit
touching `app/`, `api/`, or `scripts/`.

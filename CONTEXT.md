# DealScout — CONTEXT, ARCHITECTURE & CHANGELOG

> **Repository:** `D:\Projects\dealscout-telegram-bot` → <https://github.com/1khvled/dealscout-telegram-deals>
> **Production site:** <https://dealscoutgreen.vercel.app>
> **Primary channel:** `@DzAliexpress0` · **France channel:** `@francedealsdz` · **Coin bot:** `@Alilo07BOT`
> **Last verified:** 11 November 2026 (code, tests and production state all checked against this document)
> **Supersedes:** the Oct 2026 version of this file, which described the retired `D:\Projects\TELEGRAM_REPO` layout and a Telethon-based collector that the cron path no longer uses.

This document is the single source of truth for **what runs, where, and why**. It is written to be read by a human operator and by an AI agent picking the project up cold. If code and this file disagree, the code wins — fix the file.

---

## 1. What this is

An autonomous AliExpress deal pipeline for Algeria (and France). It watches competitor Telegram deal channels, extracts the real deal (product, price, coupon, country restriction), rewrites every link into our own affiliate link, rebuilds the post in the competitor's own layout, renders the image, and publishes to our channel — unattended, every few minutes, for free, on GitHub Actions.

Alongside the pipeline there is a public bilingual web portal (FastAPI on Vercel), an admin dashboard, a coin-discount bot, and a set of engagement automations (promo calendars, reminders, card-affiliate posts).

**The one non-negotiable rule** (`.agents/rules/no_competitor_links.md`, `GEMINI.md`): a published post may never contain a competitor handle, competitor affiliate shortcode, competitor invite link, or any bot other than `@Alilo07BOT`. Every outgoing URL is re-monetised with tracking ID `dzkhvled16`.

---

## 2. Production surface

| Asset | Handle / URL | Notes |
|---|---|---|
| Algeria channel | `@DzAliexpress0` | Primary. Arabic (RTL), USD pricing with DZD conversion on the site. |
| France channel | `@francedealsdz` | French copy, EUR pricing, separate publisher and state file. |
| Coin bot | `@Alilo07BOT` | Coin-discount link generator. Production runtime is the Cloudflare Worker in `worker/` (`POST /telegram`); `api/coin_bot.py` keeps the same logic for local polling. |
| Website | `dealscoutgreen.vercel.app` | FastAPI + embedded HTML, Vercel `services` deploy. |
| Admin dashboard | `/admin` | Cookie-signed login, manual reformat/publish, Facebook publish. |
| Facebook page | `1451244491398196` | Optional cross-post (`FACEBOOK_AUTO_POST_ENABLED`), separate state file. |

**Monitored sources** (`CHANNELS` in `scripts/post_recent_deals.py`): `lodydeals`, `ECKSDEAL`, `zedstoreonline`, `aniscoupons`, `BNDDEALS`.
**Not** scraped by the cron path: `megaphonna`, `Pcgamingpart`, `megaprix`, `alidealsdz` (present in `app/config/channels.yaml` / state but disabled or unused).

---

## 3. Runtime topology

There are two independent publishers, each a standalone script, each invoked as its own GitHub Actions step:

```
.github/workflows/bot_cron.yml        cron '*/5 * * * *' + workflow_dispatch
├── step: Run Algeria Deals Publisher   → scripts/post_recent_deals.py  → @DzAliexpress0
├── step: Run France Deals Publisher    → scripts/post_france_deals.py  → @francedealsdz
├── step: Send test admin alert         (manual, input test_alert=true)
├── step: Notify admin on failure       (always(), inspects step outcomes)
└── step: Commit and push state         (always(), commits storage/state/)
```

Properties worth knowing before you change anything:

- **`continue-on-error: true` on both publisher steps.** A crashed publisher does *not* fail the job. This is deliberate (one channel's failure must not block the other) and only safe because (a) `pr_checks.yml` runs the suite on every push, (b) the in-process `FATAL` handler DMs the admin, and (c) the workflow's `Notify admin on publisher failure` step inspects `steps.<id>.outcome`. **Never delete the step ids `algeria` / `france`** — the alert condition is keyed on them.
- **`concurrency: telegram-deals-cron`, `cancel-in-progress: false`** — runs queue instead of overlapping.
- **The last step commits `storage/state/` back to `main`** with rebase-retry, message `Auto-update deals database [skip ci] [skip vercel] [vercel skip]`. Vercel skips those commits (`scripts/ignore_build.sh`), so state churn costs no builds.
- **Night pause:** 00:00–08:00 Africa/Algiers the scheduler stops collecting deals; sweeps continue at 60-minute intervals. Daytime interval is 5 minutes.
- **The coin bot is not part of this workflow.** `@Alilo07BOT` runs as a Cloudflare Worker (`worker/`, deployed with `npx wrangler deploy`, webhook `https://alilo07bot.<subdomain>.workers.dev/telegram`). It is a pure webhook — no cron, no polling, no KV/D1 — so it costs one request per Telegram update. Vercel's `402` killed the old `/api/webhook`; do not point the bot back at it.

---

## 4. The Algeria pipeline, step by step

`scripts/post_recent_deals.py::collect_and_post_last_10_deals` is the whole story. Order matters — each guard exists because something leaked once.

**0. Pre-flight automations** (run before deal collection, each independently try/except'd)
promo-calendar transitions → 14-day region disclaimer pin → promo era alerts → coin reminder → card-affiliate post → France cross-promo → religious reminders → expired-deal rewriter → pre-11.11 advisory. Tajmi3at compilations run **only** with `--tajmi3at`.

**1. Scheduler gate.** `is_deal_posting_due("algeria")` returns `(due, message, interval)`. Not due → the run exits 0 without touching the channel. `--force` bypasses.

**2. Pacing.** During a warm-up/11.11/festival event: 60 deals per channel, 100 per run. Otherwise 15/10 per channel (peak/off-peak) and 30/20 per run. Peak hours are 12:00–14:00 and 18:00–23:30 Algiers time.

**3. Channel sweep.** Each channel's public preview `https://t.me/s/<channel>` is fetched (max 6 pages, `?before=<min_id>` pagination, 3 retries). If the preview returns nothing, it falls back to probing individual posts via `https://t.me/<channel>/<id>?embed=1`. **No Telethon, no user session, no bot membership** — this is why the cron runs anywhere with no credentials beyond the bot token.

**4. Freshness pre-filter.** Anything older than 18h is marked handled and skipped, so a channel that goes quiet doesn't cost quota. In-loop freshness is also 18h (`validate_deal_freshness`), plus expired-campaign detection.

**5. Message-type routing**, in this order:
   - multi-deal roundup / compilation → skipped unless `--tajmi3at`
   - coupon-claim / restock announcement → `publish_incoming_coupon_claim_post` (once per day, branded banner, inline keyboard)
   - spam / non-deal → handled & skipped
   - France-only drop (`عروض ففرنسا`, `Livraison France`, …) → forwarded to `scripts/post_france_deals.publish_extracted_deal_to_france`

**6. Extraction** (`app/aliexpress/product.py::ProductExtractor`). Resolves every candidate URL, scores each against the post title (`compute_title_compatibility`), and **rejects** a deal whose API title shares no token with the post title (the "frankenstein post" guard). Coupon bulletins (≥2 tiered coupons or ≥3 codes) branch into `is_coupon_list` handling.

**7. Deal-type decision.** Everything single-product on the Algeria channel is forced to `coin` (the highest-discount link type); `bundle` is preserved only when explicitly detected. Coupon lists use the campaign landing link.

**8. Affiliate conversion.** `affiliate_service.create_affiliate_link(...)` then `api.coin_bot.ensure_affiliate(...)`. Competitor-exclusive shortcodes (`_c38iyTZR`) are remapped to our own campaign link. A post that depends on a competitor's affiliate-exclusive coupon is rejected outright.

**9. Deduplication** — four independent layers, all of which must allow the post:
   - `is_post_already_published(channel, msg_id)` — exact source post
   - `is_recent_cross_channel_duplicate(product_id, …)` — same product from another channel within `DUPLICATE_COOLDOWN_HOURS`, with *restock* and *price-drop* exceptions
   - same product ID already published this run
   - similar title already published this run (`is_same_deal_title`, token/model-aware)

**10. Caption.** Channel-specific 1:1 formatters (`format_lodydeals_caption_1to1`, `format_competitor_to_lody_1to1`) mirror the competitor's layout, strip their handles/bot ads, normalise the price line, and repair truncated word boundaries. `caption_validator` then re-checks title, prices, coupon, points flag and affiliate URL — a validation failure rejects the deal and marks it handled.

**11. Image.** Official AliExpress studio photo only (`_fetch_clean_aliexpress_image`); Telegram CDN images are treated as competitor-watermarked. No clean photo → the deal is left **for retry**, not published degraded. Coupon bulletins render a branded card instead.

**12. Publish + record.** `telegram_publisher.publish_deal(...)`, then `record_post_published(...)` (post key, title, product, price, price-drop history, channel message id), coupon-bulletin bookkeeping, `record_deal_posted_time()`, and the watchlist price-drop notifier.

A publish failure calls `notify_admin_error` and moves on. A per-channel exception is caught, reported, and the next channel continues. The high-water mark (`record_monitored_channel_last_id`) advances only up to what was actually processed, so paced deals are not lost.

---

## 4.5. Deterministic deal intelligence (no LLM)

Added 11 Nov 2026. There is **no model provider, no network call and no
inference service** anywhere in this feature. The scorer is a pure function of
the candidate's features and a small JSON model (`storage/state/intelligence_model.json`).

**Where it sits:** after all four dedup layers, before the image fetch and
caption build (`scripts/post_recent_deals.py`, step 6.5). A blocked deal is
marked handled and the sweep continues.

### Signals and direction

| Signal | Range | Meaning |
|---|---|---|
| `freshness` | 0–1 | 1 at 0 h, 0 at 18 h (the pipeline's hard freshness limit) |
| `price_edge` | 0–1 | drop vs the same product's last price, else percentile in its price history |
| `channel_reliability` | 0–1 | EWMA of published vs skipped outcomes per source channel |
| `category_value` | 0–1 | same EWMA per coarse category (phones, audio, pc, accessories, home) |
| `title_quality` | 0–1 | length + model/spec token + word count − spam/all-caps penalties |
| `incentive` | 0–1 | coupon, coins, or both |
| `novelty` | 0–1 | 1 − best title similarity against 72 h of published titles |
| `flow_pressure` | 0–1 | posts in the last 6 h / `flow_target`; only penalises |
| bonuses | — | restock, price-drop exception, coupon bulletin |

Each symmetric signal becomes `weight * (2x - 1)`, so a neutral 0.5 contributes
zero. `z = bias + Σ contributions`, then `score = 100 / (1 + exp(-z / 2.2))`.
Verdict: `publish >= threshold`, `skip < threshold`, otherwise `hold`.
Every decision carries a signed, human-readable reason list, e.g.:

```
score=73.2 verdict=publish (publish>=60, skip<38) | freshness +1.24 (1.0h old)
| novelty -0.90 | title_quality +0.70 | price_edge +0.65 ($249.00 -> $199.00 (+20%))
| incentive +0.60 | flow_pressure -0.09 (3 posts/6h) | ...
```

### Modes (`INTELLIGENCE_MODE`)

| Mode | Behaviour |
|---|---|
| `off` | No scoring, no model writes. |
| `shadow` (default) | Score + log + learn, **always publish**. Safe rollout. |
| `enforce` | Block only `skip`. `hold` follows `INTELLIGENCE_HOLD_ACTION` (`publish` by default, `skip` optional). |

`INTELLIGENCE_HOLD_ACTION=publish` is deliberate: a mid-band deal is still
published, because dropping it is worse than posting it. Only clearly bad
deals are suppressed.

### Learning

`observe()` updates a bounded EWMA (`alpha=0.08`, shrunk toward a 0.5 prior
with 5 pseudo-observations) for the source channel and category. Candidates
count `seen` once; the real `published` / `skipped` outcome is attached later,
so the sample cannot be inflated. The model also keeps the last 10 prices per
product (max 500 products) and the last 200 decisions. Everything is bounded:
the file does not grow with traffic.

**Fail-open:** any error inside the gate logs a warning and returns
`allowed=True`. The intelligence layer can never stop publishing.

---

## 5. Repository map

```
api/                     Vercel serverless surface (FastAPI)
  index.py               All HTTP routes + /api/deals live channel scraper
  user_site.py           Public portal (embedded HTML/CSS/JS, ~6.3k lines)
  admin_dashboard.py     Obsidian-dark editorial dashboard
  admin_login.py         Login page
  admin_bot.py           Interactive Telegram admin bot
  coin_bot.py            Coin-discount bot + affiliate helpers (get_live_usdt_rate, ensure_affiliate)
  blog_guide.py          Long-form SEO guide page
  geo_llms.py            llms.txt / llms-full.txt / ai-summary payloads
  parcel_tracker.py      Parcel tracking page helper

app/
  aliexpress/
    parser.py            Text→structured deal: prices, coupons, country, title, spam, routing flags
    product.py           ProductExtractor + ExtractedProduct dataclass
    resolver.py          Short-link/URL resolution, product-id canonicalisation
    urls.py              URL extraction, competitor-contamination firewall, product-id helpers
    affiliate.py         Provider abstraction (portals / direct / custom network)
    promos.py            PromoEvent, promo calendar, event sniffing, coupon tiers
  ai/
    generator.py         Algeria captions: generic + 1:1 formatters + validation helpers
    generator_fr.py      France captions
    validator.py         CaptionValidator (post-generation hard gate)
    prompts.py           Editorial rules
    category_firewall.py Category whitelist/blacklist
  publisher/
    publisher.py         TelegramPublisher — the only code that calls sendPhoto on the Algeria channel
    state_tracker.py     Persistent state, dedup, schedules, eligibility for every automation
    promo_calendar.py, promo_notifiers.py, promo_notifiers_fr.py
    region_disclaimer.py, religious_reminders.py, bot_ad.py
    card_affiliates.py, france_cross_promo.py, website_promo.py
    regrouper.py, regrouper_fr.py, watchlist.py, admin_alerts.py, facebook.py
  media/                 downloader.py (fetch), renderer.py (cards, watermark scrub)
  db/                    models.py (SQLAlchemy), session.py (async engine)
  intelligence/
    scoring.py           Pure deterministic scorer + learned model (no network)
    gate.py              Publisher integration, fail-open, mode enforcement
  control/
    controller.py        Phase-3 health report + bounded threshold proposals (stdlib only)
  config/settings.py     Pydantic Settings — every env var lives here

scripts/                 One entry point per job (see §3); all add repo root to sys.path
infra/aws/               Phase-2 runtime: CloudFormation, Dockerfile, Lambda handler, deploy scripts
tests/                   pytest suite (286 tests, offline)
storage/state/           Committed JSON state (see §6)
assets/                  Brand banners used by the publishers
deals.db                 LOCAL ONLY — gitignored and excluded from Vercel (§7)
.github/workflows/       bot_cron.yml, pr_checks.yml, tajmi3at.yml, control.yml, deploy_aws.yml
```

---

## 6. State and database

**`storage/state/published_state.json`** is the deduplication memory. It is committed, so it survives across ephemeral runners. Key fields:

| Key | Meaning | Cap |
|---|---|---|
| `published_post_keys` | `channel:message_id` already published | 1000 (rolling) |
| `handled_post_keys` | seen and intentionally skipped | 1000 (rolling) |
| `channel_published_deals` | full audit record incl. target message id & price | unbounded |
| `published_product_ids` / `_timestamps` / `_channels` / `_prices` | cross-channel dedup + price-drop detection | — |
| `published_titles` / `_timestamps` | near-duplicate title detection | — |
| `published_coupon_bulletins` | one bulletin per promo/coupon-set | — |
| `monitored_channels` | per-channel high-water message id | — |
| `schedule_config` | day/night intervals, pause flag, last sweep/post times | — |
| feature timers | disclaimers, card posts, cross-promo, reminders, advisories | — |

`france_published_state.json`, `facebook_published_state.json`, `watchlist.json`, `dynamic_events.json` and `recent_deals.json` are separate.

**Intelligence state (added 11 Nov 2026):**

| File | Purpose | Cap |
|---|---|---|
| `intelligence_model.json` | weights, thresholds, channel/category EWMA, product price history, last 200 decisions | 500 products × 10 prices, 200 decisions |
| `control_state.json` | Phase-3 bounded threshold overrides (`enabled`, `thresholds`) | tiny |
| `control_report.json` | last health report (optional, not committed) | — |

`control_state.json` is read by the gate at runtime and clamped to
`publish ∈ [45, 80]`, `skip ∈ [20, 55]`, with at least an 8-point gap. A bad
proposal cannot disable publishing or deduplication.

**Note on the rolling caps:** both post-key lists are truncated to the newest 1000 entries. During a high-volume festival this window can be shorter than the 18h freshness window, which would allow an old-but-still-fresh post to be re-processed. It is mitigated by the per-channel high-water mark. If you ever see a duplicate post, this is the first thing to inspect.

**`deals.db` (SQLite)** — `channels`, `deals`, `source_messages`, `generated_posts`, `telegram_posts`, `system_logs`, `click_events`, `redirect_links`. Written by the publisher for audit/analytics; **not** required for the cron to work, **not** committed, **not** deployed.

---

## 7. Deployment — what actually ships

- **Vercel** builds from `main` via `vercel.json` (`services` + catch-all rewrite). `scripts/ignore_build.sh` skips builds unless the commit touches `api/`, `main.py`, `vercel.json`, `requirements.txt` or `assets/logo*`, unless the message contains `[deploy]` / `[force deploy]`.
- **`.vercelignore` excludes** `deals.db`, `storage/downloads`, `storage/generated`, most `assets/*.png`, all of `scripts/`, `tests/`, and the runtime state files (`published_state.json`, `france_published_state.json`, `facebook_published_state.json`).
- **Consequence:** on Vercel, `/api/deals` cannot use its SQLite fallback (no DB) and `published_state.json` does not exist. The only bundled offline fallback is `storage/state/recent_deals.json` (40 entries), consumed by `/api/deals` and `/api/channel-posts`. If that JSON path breaks, the site shows nothing whenever Telegram scraping fails — which is exactly the bug fixed on 11 Nov (§11).
- **GitHub Actions** installs `requirements.txt` **plus** `python-aliexpress-api` (kept separate on purpose; `api/coin_bot.py` imports it at module scope).
- **Local runs** need `.env` (gitignored). CI gets everything from repository secrets; nothing else is baked in.

### Optional AWS runtime (Phase 2, built but **not deployed**)

`infra/aws/` contains a CloudFormation stack + container Lambda + EventBridge
Scheduler + private S3 state bucket. It runs the same publisher scripts as the
cron. Deploying is a separate manual action:

```powershell
aws login --region eu-north-1 --profile agent-toolkit
.\infra\aws\deploy.ps1                       # dry run (build + push only)
.\infra\aws\deploy.ps1 -ConfirmDeploy -SecretArn "arn:..."
```

After AWS is healthy, set repository variable `DEALSCOUT_RUNTIME=aws`; the
GitHub cron job then skips its schedule (`bot_cron.yml` has the interlock).
Manual `workflow_dispatch` still works as a fallback. See `infra/aws/README.md`
for costs, IAM and rollback. Nothing is created until you pass `-ConfirmDeploy`.

### Configuration reality check

`.env` is not committed, so **CI and local runs do not share values**. Known divergences as of 11 Nov 2026:

| Setting | `.env` (local) | CI (default from `settings.py`) |
|---|---|---|
| `DUPLICATE_COOLDOWN_HOURS` | 24 | **4** |
| `EUR_USD_RATE` | 0.92 | 0.92 |
| `PUBLISH_MODE` | auto | auto (`bot_cron` does not set it; `settings` default is `approval`, so verify before relying on it) |

The README's "30–45 minute festival cooldown" describes neither environment. Treat `settings.py` as the truth for CI, `.env` as the truth for your machine.

---

## 8. Operations runbook

```bash
# Local publish (needs .env + python-aliexpress-api)
python scripts/post_recent_deals.py --force
python scripts/post_france_deals.py --force

# Restore state after any local run — MANDATORY (pytest also dirties state)
git checkout -- storage/

# Admin alerts end-to-end
#   Actions → AliExpress Deals Telegram Bot → Run workflow → test_alert: true

# Delete a bad channel post
python -c "import httpx,os; httpx.post(f\"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}/deleteMessage\", json={'chat_id':'@DzAliexpress0','message_id':MSG_ID})"

# Force a re-post: remove the key from published_post_keys / channel_published_deals
# in storage/state/published_state.json, or dispatch the workflow with force=true.

# Intelligence gate
python -c "from app.intelligence.gate import decision_report, evaluate_deal_gate; print('see logs for [INTEL] lines')"
# Shadow (default): score + log + learn, always publish.
# Enforce: set INTELLIGENCE_MODE=enforce in .env / repo variables.
# A model reset = delete storage/state/intelligence_model.json (starts from priors).

# Phase-3 control loop (stdlib only, no dependencies)
python -m app.control.controller report --markdown          # read-only health
python -m app.control.controller propose --json             # bounded proposal
python -m app.control.controller apply --dry-run            # preview write
python -m app.control.controller apply --actor "$USER"      # write control_state.json

# Or from GitHub: Actions → DealScout Control Loop → action = report|propose|apply
```

---

## 9. Testing and quality gates

**286 tests, all offline** (no network, no tokens, no DB writes required) — `python -m pytest tests/ -q` runs in ~37s.

Two CI gates:

1. `pr_checks.yml` — strict, no `continue-on-error`. Byte-compiles the two publishers, the `aliexpress` critical path and the new intelligence/control/AWS modules, runs an import smoke test, then the full suite. Triggers on changes to `app/`, `api/`, `scripts/`, `tests/`, `requirements.txt`.
2. `bot_cron.yml` — the runtime itself, with the admin-alert safety net described in §3.

**`tests/test_undefined_names.py`** (added 11 Nov 2026) runs `pyflakes` over `app/`, `api/`, `scripts/`, `infra/` and fails on any `undefined name`. This is the gate for the outage class in §10: a `NameError` inside a `try/except` is invisible to `py_compile` and to every behavioural test. `pyflakes` is pinned in `requirements.txt` so CI always has it.

New in the intelligence work: `tests/test_intelligence.py` (32 tests, pure scorer + gate modes + persistence + fail-open), `tests/test_control.py` (controller metrics/health/proposals/bounds), `tests/test_aws_runtime.py` (state sync + handler fail-closed interlock). All use `tmp_path`; none touch production state.

**Before committing anything under `app/`, `api/`, `scripts/` or `infra/`:** `pytest tests/test_undefined_names.py tests/test_publish_smoke.py -q`, then the full suite. See `.agents/rules/publish_safety.md`.

---

## 10. Changelog

### 11 Nov 2026 — deterministic intelligence, AWS runtime, closed loop

**Phase 1 — intelligence (no LLM, no network).** Added `app/intelligence/`:
a deterministic multi-signal scorer (freshness, price edge, learned channel
and category yield, title quality, incentive, novelty, saturation, restock and
price-drop bonuses), a 0–100 logistic score with signed explanations, three
modes (`off`/`shadow`/`enforce`), and a bounded JSON model that learns from
real publish/skip outcomes. Integrated at step 6.5 of the Algeria pipeline
behind `INTELLIGENCE_MODE=shadow` (default). Fail-open: scoring errors never
block publishing. Added `INTELLIGENCE_MODE`, `INTELLIGENCE_HOLD_ACTION`,
`INTELLIGENCE_MODEL_PATH`, `INTELLIGENCE_CONTROL_PATH` settings.

**Phase 2 — AWS runtime (built, not deployed).** Added `infra/aws/`:
CloudFormation (private versioned S3 state bucket, container Lambda with
reserved concurrency 1, EventBridge Scheduler, CloudWatch alarms + SNS),
Dockerfile, `lambda_handler.py` (S3 sync → run publishers → sync), and
`deploy.ps1`/`deploy.sh` that are dry-run by default. State download is
fail-closed so the runtime never publishes without dedup memory. Added
`DEALSCOUT_RUNTIME=aws` interlock to `bot_cron.yml` and a manual OIDC
`deploy_aws.yml` workflow. **Nothing was deployed.**

**Phase 3 — closed loop.** Added `app/control/controller.py` (stdlib only):
health report from production state + learned model, bounded threshold
proposals with explicit reasons, and `apply` that writes
`storage/state/control_state.json`. Added `.github/workflows/control.yml`
(6-hourly read-only health check; manual `report`/`propose`/`apply`; `propose`
opens a PR for review). The gate clamps overrides to hard bounds.

Tests: 232 → **286**.

### 11 Nov 2026 — coupon-claim wall incident (post-deploy fix)

The first run after the undefined-name sweep posted one Arabic coupon wall to
`@DzAliexpress0` (message #2276, source `@zedstoreonline` #39827). Cause: the
`json` import restored in `scripts/post_recent_deals.py` revived
`publish_incoming_coupon_claim_post`, a dormant "claim center" path that had
been silently failing with `NameError` inside its `except`. It was never
disabled on purpose by the earlier coupon-wall cleanup, because that cleanup
only touched `ensure_active_promo_coupons_pinned`.

Fix: `COUPON_CLAIM_POSTS_ENABLED` (default **false**). When false the branch
marks the source post handled and skips it entirely — it never falls through to
normal extraction, so it cannot be republished as a coupon list. The incident
message was deleted. No other posting path was affected: the remaining fixed
names touch the web API, the admin bot, France card images and a manual helper.

### 11 Nov 2026 — silent-failure sweep
Nine undefined-name defects fixed across four files. None could be caught by `py_compile`; each was a latent `NameError` inside a handler that swallowed it.

| File | Defect | Impact |
|---|---|---|
| `scripts/post_recent_deals.py` | `json` never imported, used in `publish_incoming_coupon_claim_post` | Coupon-claim/restock publisher **never posted anything** since it was added |
| `scripts/post_recent_deals.py` | `deals_published_this_run` never defined | Would have killed the entire cron run the first time a roundup or claim actually published |
| `api/index.py` | `json` never imported (2 sites) | Offline fallback for `/api/deals` and `/api/channel-posts` silently dead |
| `api/index.py` | `logger` never defined (3 sites) | `/api/reformat-deal` raised instead of logging |
| `api/index.py` | `settings` not in scope in `api_publish_deal` | Manual admin publish path raised `NameError` |
| `api/index.py` | `Path` imported inside a `try` guarded by optional `python-dotenv` | If dotenv were absent, `Path` was never bound → fallbacks dead |
| `api/admin_bot.py` | `logger` never defined | Photo-download error handler itself raised |
| `app/publisher/promo_notifiers_fr.py` | `Path` never imported | France coupon notifier crashed on the launch-poster branch |
| `scripts/post_2_deals.py` | `raw_text` used but never assigned (4 sites) | Manual helper script could not work at all |

Added `tests/test_undefined_names.py` + `pyflakes` to `requirements.txt`.

### Nov 2026 — 1:1 competitor mirroring
Replaced AI rewrites with `format_*_1to1` formatters; competitor handles and bot spam are scrubbed by regex; `_render_framed_deal` (empty neon frames) disabled in favour of `_render_deal_card`; watermark scrubbing on light backgrounds; cooldowns shortened for 11.11; truncated-title boundary repair; auto-Tajmi3at and coupon pinning disabled; admin DM leak removed.

### Oct 2026 — portal, gamification and the outage
Phases 1–11 as previously documented: secret hardening, bilingual portal, scraping resilience, financial tools, gamification, anti-AI-slop editorial pass, SEO/GEO, community integration, admin redesign, parcel tracking, multi-coupon parsing and country-hallucination repair.

**The outage (Oct 11–14):** `fb7cbfe` used `Tuple`/`Any` without importing them, `parser.py` used `Any` without importing it, and `post_france_deals.py` referenced an undefined `target_channel`. Both publishers exited 1 on every run for three days while `continue-on-error` kept Actions green. Fix `712e681`; the rules in `.agents/rules/publish_safety.md` and today's static gate exist because of it.

---

## 11. Known issues / open items

1. **Cooldown config drift** — README claims 0.5h, `.env` says 24h, CI runs the 4h default. Pick one and state it in one place.
2. **`python-dotenv` is imported but not declared** in `requirements.txt` or `api/requirements.txt`. Harmless now that `Path` is module-level, but `.env` will not be auto-loaded on a clean machine.
3. **Rolling 1000-key dedup window** — see §6. Time-based expiry would be safer at festival volumes.
4. **`scripts/*` is excluded from Vercel** but `api/coin_bot.py` is imported by both worlds; keep that in mind when moving helpers.
5. **`storage/state/recent_deals.json` is stale** (last written 6 Nov). It is the site's only offline fallback; regenerate it whenever the pipeline changes.
6. **AWS runtime is not deployed.** `infra/aws/` is complete but requires `aws login --profile agent-toolkit`, a spend-limit review and `-ConfirmDeploy`. The current AWS session was expired when this was written, so no cloud check was possible.
7. **After an AWS cutover, set `DEALSCOUT_STATE_BUCKET`** (stack output) together with `DEALSCOUT_RUNTIME=aws`; otherwise the control loop reads stale git state instead of S3.
8. **Intelligence defaults to `shadow`.** `enforce` changes what reaches the channel; do not enable it without at least a week of shadow logs and a review of the `[INTEL]` lines.
9. **The control loop is intentionally slow** (±4 points per run, hard bounds). It corrects drift, not emergencies; use `workflow_dispatch` with `force=true` for emergencies.

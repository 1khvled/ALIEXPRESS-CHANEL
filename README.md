# ⚡ AliExpress Deals Telegram Automation (DealScout DZ & FR)

[![Telegram Channel DZ](https://img.shields.io/badge/Telegram-Channel%20%40DzAliexpress0-blue?logo=telegram)](https://t.me/DzAliexpress0)
[![Telegram Channel FR](https://img.shields.io/badge/Telegram-Channel%20%40francedealsdz-blue?logo=telegram)](https://t.me/francedealsdz)
[![Coin Deals Bot](https://img.shields.io/badge/Telegram-Bot%20%40Alilo07BOT-green?logo=telegram)](https://t.me/Alilo07BOT)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)

An autonomous, end-to-end deal intelligence, normalization, and multi-channel publishing engine. Monitors top competitor Telegram deal channels in real-time, extracts verified AliExpress deals, converts all links to high-converting affiliate URLs with active coin discounts, scrubs competitor watermarks and bot ads, and mirrors clean 1:1 deal posts to your target channels.

---

## 📌 Production Channels & Current Status

| Channel | Handle | Target Audience | Currency & Rules | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Algeria Deals** | [`@DzAliexpress0`](https://t.me/DzAliexpress0) | Algerian Shoppers 🇩🇿 | USD ($), Coin Discount links (Canada/Australia settings), 1:1 clean Arabic format | **ACTIVE (5-min Cron)** |
| **France Deals** | [`@francedealsdz`](https://t.me/francedealsdz) | France / Eurozone 🇫🇷 | EUR (€), Fast European delivery, Clean French layout | **ACTIVE (5-min Cron)** |
| **Coin Bot** | `@Alilo07BOT` | Coin discount generator | Instant coin link conversions & bundle deals | **ACTIVE** |

---

## 🚀 Recent Major Overhaul & Changelog (November 2026)

### 1. 1:1 Competitor Mirroring ("Just Copy Them")
* **Direct Mirroring Architecture**: Replaced aggressive AI rewrites with `format_competitor_to_lody_1to1` and `format_lodydeals_caption_1to1`. The bot now accurately reflects the layout, emojis, seller vouchers, and discount tiers posted by top competitor channels (`aniscoupons`, `zedstoreonline`, `bnddeals`, `ecksdeal`, `lodydeals`).
* **Zero Competitor Leaks**: Built-in regex filters thoroughly purge all competitor usernames (`@aniscoupons`, `@zedstoreonline`, `@bnddeals`, `@ecksdeal`, `@lodydeals`, `@ZedStoreSve_bot`, etc.) and promotional bot spam (`بوت مطور لشراء بأفضل سعر`, `لا تنسى استخدام البوت للشراء بأقل الأسعار`, `تتبع الطرود`).
* **Clean DealScout Signatures**: Every mirrored post signs off cleanly with our official channel handle `📢 @DzAliexpress0` and verified affiliate links.

### 2. Media Pipeline Modernization & Broken Frame Elimination
* **Eliminated Empty Neon Frame Bug**: Permanently disabled `_render_framed_deal` which was outputting an empty `1254x1254` neon template frame with a transparent checkerboard center when images were missing or failed resizing.
* **Studio Product Photos**: Switched exclusively to `_render_deal_card` in `app/media/renderer.py`. Every deal now features the full natural product photo (in native 800×800 or 1000×1000 resolution) with a subtle DealScout circular badge and modern glassmorphic price pill.
* **Watermark Scrubber**: `_clean_source_watermark` scans and removes competitor corner watermarks on light/white backgrounds before publishing.
* **Channel Purge**: Removed all historic broken frame posts (`#1930`, `#1932`, `#1934`, `#1935`, `#1940`, `#1941`, `#1942`) from `@DzAliexpress0`.

### 3. Short Cooldown Debounce for Festival Season (11.11)
* **Debounce Window**: Lowered `DUPLICATE_COOLDOWN_HOURS` from an overly aggressive 12 hours down to an agile **30–45 minute** window (`0.5h` - `0.75h`).
* **Same-Channel Re-posts**: Aligned `same_channel_min_cooldown` to allow deal bumps, reminders, and price drops from monitored channels after 30 minutes, preventing our bot from skipping hot trending deals (like the `Realme C100D`).
* **Anti-Flood Protection**: Retains short 5–15 minute deduplication to prevent posting identical deals simultaneously if multiple competitor channels post at the exact same minute.

> ⚠️ **Correction (11 Nov 2026):** this section describes intent, not the configured value. `.env` currently sets `DUPLICATE_COOLDOWN_HOURS=24`, and CI runs the `settings.py` default of **4 hours** because `.env` is not committed. See `CONTEXT.md` §7 before tuning this again.

### 4. Arabic Title & Text Formatting Sanitization
* **Truncated Title Fix**: Added `_clean_title_boundary` to remove dangling truncated words (e.g. `والأل` at line endings) caused by arbitrary character cuts.
* **Boundary Cleaners**: Strips orphan punctuation, dangling prepositions (`لـ`, `في`, `من`), and isolated emoji lines.
* **Price Line Normalization**: Enforces standardized RTL Arabic pricing lines (`السعر : $XX.XX 🔥`).

### 5. Deactivation of Spontaneous Promo Coupon Walls
* **Disabled Auto-Tajmi3at**: Removed the automated cron trigger in `.github/workflows/tajmi3at.yml`. Multi-deal roundups and coupon compilations only run on manual workflow dispatch.
* **Disabled Scraper Coupon Pinning**: Removed `ensure_active_promo_coupons_pinned` from the background scraper loop in `app/publisher/promo_notifiers.py` to prevent spontaneous spam of repetitive coupon bulletin posters.

### 6. Admin Chat Isolation & Security
* **Zero DM Leaks**: Removed any debug inspection scripts forwarding test channel messages to the user's private Telegram bot chat (`ADMIN_USER_ID`).
* **Safe State Management**: State persistence in `storage/state/published_state.json` accurately logs every channel message ID and prevents duplicate processing across workflow runs.

### 7. Deterministic Deal Intelligence (no LLM)
* **No model provider, no network call, no inference service.** Scoring is a pure function of the candidate's features plus a small bounded JSON model (`storage/state/intelligence_model.json`).
* **Nine signals** feed a 0–100 logistic score: freshness, price edge (vs. last price and the product's own price history), learned source-channel yield, learned category value, title quality, incentive (coupon / coins), novelty vs. 72h of published titles, saturation pressure (posts in the last 6h) and restock / price-drop bonuses.
* **Explainable by construction.** Every decision logs a signed reason list, e.g. `score=73.2 verdict=publish | freshness +1.24 | price_edge +0.65 ($249.00 -> $199.00 (+20%)) | flow_pressure -0.09`.
* **Three modes** via `INTELLIGENCE_MODE`: `off`, `shadow` (default — score, log and learn but always publish) and `enforce` (block only `skip`; `hold` publishes by default through `INTELLIGENCE_HOLD_ACTION`).
* **Fail-open.** Any scoring error logs a warning and lets the deal through; the intelligence layer can never stop publishing.
* **Placement:** after all four dedup layers and before the image fetch, so it cannot interfere with deduplication or retries.

### 8. Optional AWS Runtime (built, not deployed)
* `infra/aws/` contains a CloudFormation stack (private versioned encrypted S3 state bucket, container Lambda with reserved concurrency 1, EventBridge Scheduler, CloudWatch error/throttle alarms + SNS), a Dockerfile, and a Lambda handler that syncs state down, runs the **same** publisher scripts, then syncs state up.
* **State download is fail-closed:** if S3 is unreachable the run aborts instead of publishing without dedup memory.
* Deploys are manual and dry-run by default; nothing is created until `-ConfirmDeploy` / `--confirm`.
* Repository variable `DEALSCOUT_RUNTIME=aws` disables the GitHub cron schedule once AWS is healthy; manual dispatch still works as a rollback path.

### 9. Closed-Loop Control (GitHub Actions)
* `app/control/controller.py` (stdlib only) reads production state and the learned model, reports health, and proposes **bounded** threshold changes with explicit reasons.
* `control.yml` runs a read-only health report every 6 hours; manual `report` / `propose` (opens a PR) / `apply` (commits `control_state.json`) actions are available.
* Changes are deliberately slow: ±4 points per run, `publish ∈ [45, 80]`, `skip ∈ [20, 55]`, minimum 8-point gap. A bad proposal cannot disable publishing or deduplication.

---

## 🏗 Architecture & Pipeline

```text
Monitored Channels (Telegram)
[aniscoupons, zedstoreonline, bnddeals, ecksdeal, lodydeals]
                         │
                         ▼ (Every 5 minutes via GitHub Actions)
          Public Web-Preview Scraper
   (t.me/s/<channel> + ?embed=1 fallback; no Telethon, no user session)
                         │
                         ▼
        State Tracker & 4-Layer Deduplication
   (post keys, product ids, titles, cooldown + high-water marks)
                         │
                         ▼
    Deterministic Deal Intelligence Gate (step 6.5)
 (score 0–100 + reasons; off | shadow | enforce, fail-open)
                         │
                         ▼
       AliExpress Product & URL Canonicalization
  (Extracts item ID, clean title, seller coupons, coin rules)
                         │
                         ▼
       Affiliate Conversion Engine (Tag: dzkhvled16)
 (Generates high-commission short links with active coin discount)
                         │
                         ▼
      1:1 Format Generator & Competitor Leak Scrubber
(Mirrors competitor structure, strips bot ads & handles, fixes boundaries)
                         │
                         ▼
             Media Downloader & Renderer
 (Fetches official AliExpress studio photo, scrubs watermarks, adds sleek card)
                         │
                         ▼
        Telegram Channel Publisher (@DzAliexpress0)
```

---

## ⚙️ Configuration & Environment Variables

Key parameters in `.env`:

```ini
# Telegram Bot & Channel
TELEGRAM_BOT_TOKEN="8900887118:AAG..."
TARGET_CHANNEL_ID="@DzAliexpress0"
FRANCE_TARGET_CHANNEL_ID="@francedealsdz"
ADMIN_BOT_TOKEN="8900887118:AAG..."
ADMIN_USER_ID="5625295907"

# Publishing Settings
PUBLISH_MODE="auto"
POLL_INTERVAL_SECONDS=300
MAX_POSTS_PER_HOUR=25
MAX_POSTS_PER_DAY=200
COOLDOWN_MINUTES=0
DUPLICATE_COOLDOWN_HOURS=0.5

# Affiliate Configuration
ALIEXPRESS_AFFILIATE_PROVIDER="portals"
ALIEXPRESS_AFFILIATE_TRACKING_ID="dzkhvled16"
ALIEXPRESS_AFFILIATE_APP_KEY="526622"
ALIEXPRESS_AFFILIATE_APP_SECRET="..."

# Currency & Rates
EUR_USD_RATE=1.08
```

---

## 🤖 GitHub Actions Automation

The automation runs 24/7 on GitHub Actions with zero server maintenance costs:

1. **`bot_cron.yml`**:
   - Triggers every **5 minutes** (`*/5 * * * *`).
   - Runs `scripts/post_recent_deals.py` for Algeria (`@DzAliexpress0`).
   - Runs `scripts/post_france_deals.py` for France (`@francedealsdz`).
   - Auto-commits updated state files (`published_state.json`, `france_published_state.json`) with `[skip ci]`.
   - Supports manual trigger via `workflow_dispatch` with `--force` flag.

2. **`tajmi3at.yml`**:
   - Set to manual trigger only. Publishes multi-deal roundups and coupon compilations on demand.

3. **`control.yml`** (Phase 3 closed loop):
   - Read-only health report every 6 hours (posts/24h, last post age, sweep age, learned source yield, skip rate).
   - Manual `report`, `propose` (opens a pull request) and `apply` (commits `storage/state/control_state.json`).
   - Works in AWS mode: set `DEALSCOUT_RUNTIME=aws` + `DEALSCOUT_STATE_BUCKET` and the workflow syncs S3 state into a temp directory instead of reading git.

4. **`deploy_aws.yml`** (Phase 2, optional):
   - Manual only, OIDC, requires typing `DEPLOY`; builds the Lambda image and updates the CloudFormation stack in `eu-north-1`.

### Intelligence configuration

```ini
# Deterministic scorer — no LLM, no network
INTELLIGENCE_MODE="shadow"          # off | shadow | enforce
INTELLIGENCE_HOLD_ACTION="publish"  # enforce: what to do with mid-band "hold" deals
```

Local control-loop commands (no dependencies beyond the stdlib):

```bash
python -m app.control.controller report --markdown
python -m app.control.controller propose --json
python -m app.control.controller apply --dry-run
python -m app.control.controller apply --actor "$USER"
```

---

## 🧪 Testing & Verification

Run the full pytest suite locally:

```bash
# Run all unit and integration tests
python -m pytest tests/test_deal_formatting_and_france.py -v

# Run duplicate detection and cooldown tests
python -m pytest tests/test_duplicates.py -v

# Run the complete test suite (285 tests, fully offline, ~37s)
python -m pytest tests/ -v

# Static gate: fails on any undefined name in app/, api/, scripts/, infra/
python -m pytest tests/test_undefined_names.py -v
```

> Every commit touching `app/`, `api/`, `scripts/` or `infra/` must pass `tests/test_undefined_names.py` and `tests/test_publish_smoke.py` **before** it is pushed — see `.agents/rules/publish_safety.md` for why.

---

## 📋 Troubleshooting & Maintenance

* **Channel Post Removal**: If an accidental post needs removal, use `deleteMessage` with the bot token and channel ID:
  ```python
  import httpx
  httpx.post(f"https://api.telegram.org/bot{TOKEN}/deleteMessage", json={"chat_id": "@DzAliexpress0", "message_id": MSG_ID})
  ```
* **Forcing a Deal Re-post**: If a deal needs to be reposted immediately despite recent publication, delete its entry from `published_post_keys` and `channel_published_deals` in `storage/state/published_state.json` or trigger the GitHub Action with the `force: true` input.
* **Checking Bot Connectivity**:
  ```bash
  python -c "from app.utils.network import enforce_ipv4; enforce_ipv4(); import httpx; print(httpx.get('https://api.telegram.org/bot' + TOKEN + '/getMe').json())"
  ```

# AliExpress Deals Telegram Automation (DealScout DZ & FR)

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

---

## 🏗 Architecture & Pipeline

```text
Monitored Channels (Telegram)
[aniscoupons, zedstoreonline, bnddeals, ecksdeal, lodydeals]
                         │
                         ▼ (Every 5 minutes via GitHub Actions)
          Telethon / Web Scraper Collector
                         │
                         ▼
        State Tracker & 30-min Anti-Spam Debounce
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

---

## 🧪 Testing & Verification

Run the full pytest suite locally:

```bash
# Run all unit and integration tests
python -m pytest tests/test_deal_formatting_and_france.py -v

# Run duplicate detection and cooldown tests
python -m pytest tests/test_duplicates.py -v

# Run the complete test suite (224+ tests)
python -m pytest tests/ -v
```

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

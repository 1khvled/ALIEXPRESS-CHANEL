# DealScout DZ — Telegram Deal Posting Errors, Lifecycle & Fixes Guide

> **Audience:** Future AI Agents, Maintainers, and DevOps Engineers  
> **Repository:** `1khvled/ALIEXPRESS-CHANEL`  
> **Last Updated:** October 2026 (Winter Offers Era)  
> **Target Channels:**  
> - 🇩🇿 **Algeria:** `@DzAliexpress0` (Primary Channel)  
> - 🇫🇷 **France / Diaspora:** `@francedealsdz` (Secondary Channel)  
> - 🌐 **Web Platform:** [dealscoutgreen.vercel.app](https://dealscoutgreen.vercel.app/)

---

## 1. System Architecture & Lifecycle Overview

DealScout DZ operates an autonomous pipeline that monitors 8 top competitor Algerian Telegram deal channels, filters spam and expired codes, resolves and deep-links affiliate URLs, generates bilingual Arabic/French promotional captions, and publishes deals directly to Telegram channels and the web frontend.

```
+----------------------------------------------------------------------------------+
|                             MONITORED SOURCE CHANNELS                           |
|  @lodydeals  |  @zedstoreonline  |  @ECKSDEAL     |  @Pcgamingpart               |
|  @BNDDEALS   |  @megaphonna      |  @aniscoupons  |  @CouponsGlobal              |
+----------------------------------------------------------------------------------+
                                        |
                                        v
                    +---------------------------------------+
                    |    HTTP Scraping & Widget Parsing     |
                    |      (t.me/s/<channel> HTML)          |
                    +---------------------------------------+
                                        |
       +--------------------------------+--------------------------------+
       |                                |                                |
       v                                v                                v
[1. Freshness & Promo]       [2. Spam / Non-Deal]           [3. France Geo Filter]
- Message age <= 18h         - Phone giveaways, customs     - "عروض ففرنسا", "خاص بفرنسا"
- No expired event codes       notices, personal chatter    - Auto-routed to @francedealsdz
       |                                |                                |
       +--------------------------------+--------------------------------+
                                        |
                                        v
                    +---------------------------------------+
                    |   Link Expansion & Product Resolver   |
                    |   - s.click.aliexpress.com -> item ID |
                    |   - Enforce IPv4 (bypass cloud drops) |
                    |   - Extract title, price, coupon      |
                    +---------------------------------------+
                                        |
                                        v
                    +---------------------------------------+
                    | Cross-Channel Deduplication & Pacing  |
                    | - published_product_ids & titles      |
                    | - Price drop arbitrage check          |
                    | - Max deals per channel pacing        |
                    +---------------------------------------+
                                        |
                                        v
                    +---------------------------------------+
                    | Caption Generation & Telegram Publish |
                    | - @DzAliexpress0 (sendPhoto API)      |
                    | - Record to published_state.json      |
                    +---------------------------------------+
```

---

## 2. Catalog of Known Posting Failures & Root Cause Solutions

### Error Case 1: "A channel posted a deal 10-15 minutes ago, but our bot hasn't posted it yet"

* **Symptom:**  
  User reports: *"Lody / BND posted a new deal 12 minutes ago, why haven't we posted it?"*
* **Root Causes:**
  1. **GitHub Actions Schedule Jitter (Primary Cause):**  
     In `.github/workflows/bot_cron.yml`, the scheduled trigger is `cron: '*/5 6-23 * * *'`.  
     GitHub Actions crons run on shared public compute runners. GitHub documentation explicitly notes that cron triggers may experience queuing delays of **10 to 30+ minutes** during peak hours (especially around `:00`, `:15`, `:30`, `:45`).
  2. **Tajmi3at Bulletin Execution Delay:**  
     Between 21:30 and 23:45 Algiers time, the pipeline runs daily category roundups (`tajmi3at`). Publishing 4 photo compilations with 5-second Telegram rate-limit pauses takes ~25 seconds before individual channel scanning commences.
* **Diagnostics:**
  - Check the last commit timestamp on `main` to see when GitHub Actions last ran.
  - Check `get_monitored_channel_last_id('lodydeals')` in `storage/state/published_state.json`. If `last_message_id` is lower than the new message, the bot simply hasn't executed its sweep cycle yet.
* **Fixes & Mitigations:**
  - **Instant Manual / Webhook Trigger:** Call the endpoint `/api/trigger-deals?force=true&secret=<ADMIN_PASSWORD>` on Vercel. It immediately dispatches the GitHub Actions workflow via `POST https://api.github.com/repos/1khvled/ALIEXPRESS-CHANEL/actions/workflows/bot_cron.yml/dispatches`.
  - **One-Click Admin Dashboard Button:** Navigate to `/admin` and click **"🚀 تشغيل فحص العروض الآن"**.
  - **External Ping Cron:** Setup a free external cron monitor (e.g. [cron-job.org](https://cron-job.org) or UptimeRobot) calling `https://dealscoutgreen.vercel.app/api/trigger-deals?secret=YOUR_ADMIN_PASSWORD` every 5 minutes. This completely bypasses GitHub's delayed cron scheduler.

---

### Error Case 2: "Several channels posted the same deal (e.g. Realme P3 Lite), why did we only post once?"

* **Symptom:**  
  Competitors `@lodydeals`, `@BNDDEALS`, and `@aniscoupons` all shared the same phone or item within 15 minutes. DealScout DZ only published one post.
* **Root Cause: Intended Cross-Channel Deduplication (Anti-Spam Feature)**  
  When `@lodydeals` posted Realme P3 Lite 4G (`1005010210432531`), our bot resolved the link, generated our affiliate link, and published it as message `#862`.  
  Immediately after, when scanning `@BNDDEALS` and `@aniscoupons`, the bot encountered the same product ID `1005010210432531`.  
  The state tracker executed `is_recent_cross_channel_duplicate(product_id="1005010210432531")` and flagged:  
  `[CROSS-CHANNEL DUPLICATE BLOCKED] Product ID 1005010210432531 was already posted 0.0h ago from @lodydeals`.
* **Why This is Critical:**  
  If DealScout DZ posted the identical product 4 times in 20 minutes just because 4 different channels shared it, subscribers would mute and leave the channel due to spam.
* **Allowed Exceptions:**
  1. **Significant Price Drop (Arbitrage):** If a subsequent post drops the price by ≥ 5-10% (e.g. new coupon code), the bot allows it under `[📉 PRICE-DROP EXCEPTION]` and posts the updated deal.
  2. **Same-Channel Repeat Post (Restock):** If the *same* channel re-shares an offer after 8+ hours (cooldown elapsed), it is permitted.

---

### Error Case 3: "Transient Extraction Failure" & Lookback Window

* **Symptom:**  
  Log output: `[TRANSIENT EXTRACTION FAILURE] Post #8407 has AliExpress link but extraction was incomplete. Leaving for retry.`
* **Root Causes:**
  - AliExpress redirect timeout on `s.click.aliexpress.com`.
  - AliExpress anti-bot captcha challenge on cloud IPs.
  - Cloudflare/network transient packet loss.
* **Design Decision & Fix:**  
  - If a message contains an AliExpress link (`s.click.aliexpress.com` or `aliexpress.com/item/`), the scraper **DOES NOT** call `record_post_handled(ch, msg_id)`.
  - The lookback cutoff in `scripts/post_recent_deals.py`:
    ```python
    lookback_cutoff = max(0, last_seen_id - 20)
    ```
    This ensures that in the very next cycle, the bot will re-attempt link expansion for the unhandled message.

---

### Error Case 4: IPv6 Connection Drops on AliExpress Short Links

* **Symptom:**  
  `httpx.ConnectTimeout` or `Network is unreachable` when resolving `s.click.aliexpress.com`.
* **Root Cause:**  
  AliExpress CDN edges frequently fail or drop TCP handshakes over IPv6 when accessed from cloud data centers (GitHub Actions Ubuntu runners or AWS/Vercel).
* **Fix (Implemented in `app/utils/network.py`):**
  ```python
  from app.utils.network import enforce_ipv4
  enforce_ipv4()
  ```
  Monkey-patches Python socket resolution to `AF_INET` only, completely preventing broken IPv6 connection attempts.

---

### Error Case 5: Expired Promotional Codes from Past Festivals

* **Symptom:**  
  Log output: `[EXPIRED / STALE SKIPPED] Expired festival coupon code 'OTPRD08' from ended event 'Party Ready Sale'`
* **Root Cause:**  
  Sellers or competing channels recycle promotional copy from months ago containing invalid festival promo codes (e.g. `OTPRD`, `FRPRD`, `BDQT`).
* **Fix (`app/aliexpress/promos.py`):**  
  `validate_deal_freshness()` checks active events against the system promo calendar (`PROMO_CALENDAR`). Any post referencing coupon codes from past events is automatically rejected and marked as handled.

---

### Error Case 6: Contaminated or Clickbait Post Titles

* **Symptom:**  
  Log output: `Rejecting contaminated deal: post title 'أررررررررررررررض أجررررررررررري ©️' completely conflicts with resolved product '...'`
* **Root Cause:**  
  Competitor channel owners sometimes write pure slang without product names. When resolved against AliExpress API, the resolved product title must match title similarity metrics or it is rejected to maintain high channel credibility.

---

### Error Case 7: France Deals Auto-Routing (`@francedealsdz`)

* **Symptom:**  
  Post appears in source Algerian channel, but is not posted to `@DzAliexpress0`.
* **Explanation:**  
  If the post text includes France indicators (`عروض ففرنسا`, `خاص بفرنسا`, `Livraison France`), `is_france_deal()` triggers and routes the deal to the France channel `@francedealsdz` instead of cluttering Algerian subscribers.

---

### Error Case 8: Manually Deleted Posts from Channel

* **Symptom:**  
  Admin deletes a post from `@DzAliexpress0` and wants the bot to be able to repost it if competitors share a restock.
* **Fix (`sync_deleted_channel_posts`):**  
  At the beginning of each run, `sync_deleted_channel_posts()` queries Telegram embed status for recent channel posts. If Telegram reports `tgme_widget_message_error` or `Post not found`, the state tracker cleans the record from `published_post_keys`, allowing clean reposting.

---

## 3. Quick Reference: Environment Variables for Vercel & GitHub Actions

| Variable | Target | Purpose | Example |
| :--- | :--- | :--- | :--- |
| `ADMIN_PASSWORD` | Vercel | Protects `/admin` dashboard and authorizes `/api/trigger-deals` | `YourSecurePassword2026` |
| `GITHUB_TOKEN` | Vercel | Allows `/admin` and `/api/trigger-deals` to dispatch GitHub Actions workflows | `ghp_xxxxxxxxxxxxxxxxxxxx` |
| `TELEGRAM_BOT_TOKEN` | GitHub Secrets & Vercel | Telegram bot API token for publishing posts | `8900887118:AA...` |
| `TARGET_CHANNEL_ID` | GitHub Secrets | Main Algerian Telegram channel | `@DzAliexpress0` |
| `FRANCE_TARGET_CHANNEL_ID` | GitHub Secrets | Diaspora France Telegram channel | `@francedealsdz` |
| `ALIEXPRESS_AFFILIATE_TRACKING_ID` | GitHub Secrets | Affiliate tracking sub-ID | `dzkhvled16` |

---

## 4. Verification & Testing Commands

To verify deal scraper and publisher locally or in CI:

```bash
# Test extraction and publisher dry-run
python -c "
import asyncio
from scripts.post_recent_deals import collect_and_post_last_10_deals
# Runs full collector loop
asyncio.run(collect_and_post_last_10_deals(force=True))
"

# Run unit and integration tests (160 tests)
pytest -q
```

# AliExpress Deals Telegram Automation

An automated, end-to-end deal intelligence and publishing system that monitors **10 Telegram deal channels** every **3 minutes**, extracts AliExpress deals, converts them to verified affiliate links, ensures multi-layer deduplication and quality scoring, formats clean Arabic posts, and publishes them automatically to your target Telegram channel.

---

## 📌 Architecture Overview

```text
10 Source Channels (Telegram)
           ↓ every 180s
Telethon MTProto Collector
           ↓
Source Message Storage (Deduplication Layer 1)
           ↓
URL Resolver & Canonical Normalizer
           ↓
Affiliate Conversion & Smart Redirect (/d/{slug})
           ↓
Product Extractor & Multi-Layer Deduplication Engine
           ↓
Deal Quality Scorer (0 - 100)
           ↓
AI Arabic Post Generator & Validation Engine
           ↓
Media Downloader & Visual Renderer
           ↓
Telegram Bot Publisher (Auto / Approval / Dry-Run Modes)
           ↓
Our Telegram Channel + Tracking & Live Web Dashboard
```

---

## 🌟 Key Features

1. **Telegram Collector (Telethon MTProto)**:
   - Polls 10 configured deal channels every 180 seconds.
   - Maintains a persistent cursor (`last_message_id`) to only process new deals.
2. **Deal Extractor & Canonical Resolver**:
   - Follows short links (`s.click.aliexpress.com`, `a.aliexpress.com`, `bit.ly`, etc.) to canonical `/item/{product_id}.html`.
   - Cleans all tracking spam parameters.
   - Extracts title, USD & EUR prices, coupon codes, and points discounts (`خصم النقاط`).
3. **Multi-Layer Deduplication**:
   - Source message ID check.
   - AliExpress `product_id` check.
   - Normalized URL hash.
   - Title + Product ID hash.
   - 24-hour time-window protection cooldown.
4. **Exact Arabic Channel Format**:
   - Zero hallucination guarantee: AI and generator strictly maintain verified factual values.
   ```text
   العرض مستمر 🚨
   تخفيض لـ {PRODUCT_TITLE}
   السعر : {USD_PRICE}$ ({EUR_PRICE}€)🔥
   رابط {AFFILIATE_URL}
   {COUPON_LINE}
   {POINTS_LINE}

   لا تنسى استخدام البوت للشراء بأقل الأسعار
   ```
5. **Smart Tracking Redirect**:
   - Deals can be published with `/d/{slug}` links which log click metadata (timestamp, IP, referer) before 302 redirecting to your affiliate link.
6. **Publishing Modes & Anti-Spam**:
   - `AUTO`: Deals scoring $\ge 85$ with approved validation are published immediately.
   - `APPROVAL`: Deals enter `PENDING_REVIEW` queue for operator 1-click approval.
   - `DRY_RUN`: Test full pipeline without posting to Telegram.
   - Cooldown timer & rate limiting (max posts/hour and per day).
7. **Interactive Web Dashboard & Live Tester**:
   - Access at `http://localhost:8000/`.
   - Real-time metrics, live deal approvals, 10-channel cursor statuses, and a sandbox tester to paste any post text or link and preview instant parsing and Arabic post generation.

---

## 🚀 Quick Start Guide

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Fill in your configuration:
- `TELEGRAM_API_ID` & `TELEGRAM_API_HASH`: Get from [my.telegram.org/apps](https://my.telegram.org/apps)
- `TELEGRAM_BOT_TOKEN`: Get from [@BotFather](https://t.me/BotFather)
- `TARGET_CHANNEL_ID`: Your Telegram channel (e.g. `@MyDealsChannel` or channel ID)
- `PUBLISH_MODE`: `approval` (default), `auto`, or `dry_run`

### 3. Authenticate Telethon Collector Session (First Time Only)

Run the interactive authentication script:

```bash
python scripts/auth_telegram.py
```

This logs into your Telegram account and creates a secure session in `sessions/deals_collector.session`.

### 4. Initialize Database & Seed Channels

```bash
python scripts/init_db.py
```

### 5. Run the Application

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open your browser to:
- **Dashboard**: [http://localhost:8000/](http://localhost:8000/)
- **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

---

## 🧪 Running Tests

Run the full pytest suite:

```bash
pytest tests/ -v
```

---

## 🐳 Docker Deployment

To run in Docker with PostgreSQL:

```bash
docker compose up -d --build
```

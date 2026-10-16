# DealScout / AliExpress Deals Automation Platform — CONTEXT & CHANGELOG

> **Repository:** `D:\Projects\TELEGRAM_REPO`  
> **Production URL:** [dealscoutgreen.vercel.app](https://dealscoutgreen.vercel.app)  
> **Telegram Channel:** Deals / Promo Scout  
> **Last Updated:** October 16, 2026  
> **Document Purpose:** Complete chronological, step-by-step documentation of all engineering work, architectural changes, bug fixes, UI/UX overhauls, database repairs, and test verifications performed across the project.

---

## Table of Contents
1. [Project Overview & Architecture](#1-project-overview--architecture)
2. [Chronological Step-by-Step Changelog (By Date & Phase)](#2-chronological-step-by-step-changelog-by-date--phase)
   - [Phase 1: Security Hardening & Secret Management](#phase-1-security-hardening--secret-management)
   - [Phase 2: Bilingual UI Portal & Multi-Page Architecture](#phase-2-bilingual-ui-portal--multi-page-architecture)
   - [Phase 3: Resilient Telegram Scraping & Client Syntax Fixes](#phase-3-resilient-telegram-scraping--client-syntax-fixes)
   - [Phase 4: Financial Tools, Cards Referral & Coin Calculators](#phase-4-financial-tools-cards-referral--coin-calculators)
   - [Phase 5: Gamification Suite & Engagement Engine](#phase-5-gamification-suite--engagement-engine)
   - [Phase 6: Anti-AI Slop & Editorial UI/UX Modernization](#phase-6-anti-ai-slop--editorial-uiux-modernization)
   - [Phase 7: Search Engine & Generative Engine Optimization (SEO & GEO)](#phase-7-search-engine--generative-engine-optimization-seo--geo)
   - [Phase 8: Contact, Community & Channel Integration](#phase-8-contact-community--channel-integration)
   - [Phase 9: Admin Dashboard Redesign & Publishing Tools](#phase-9-admin-dashboard-redesign--publishing-tools)
   - [Phase 10: Native Parcel Tracking Suite (17TRACK & Postal Ninja)](#phase-10-native-parcel-tracking-suite-17track--postal-ninja)
   - [Phase 11: Multi-Coupon Parsing & Country Hallucination Resolution](#phase-11-multi-coupon-parsing--country-hallucination-resolution)
3. [Component & File Directory Architecture](#3-component--file-directory-architecture)
4. [Database & State Architecture (`deals.db`)](#4-database--state-architecture-dealsdb)
5. [Testing Suite & Verification Standards](#5-testing-suite--verification-standards)
6. [Git Commit Audit History](#6-git-commit-audit-history)

---

## 1. Project Overview & Architecture

The DealScout platform is a high-throughput, automated deal discovery, curation, publishing, and e-commerce portal tailored primarily for Algerian and MENA consumers buying from AliExpress.

### Core System Components:
1. **Scraping & Ingestion Layer (`app/aliexpress/`, `api/index.py`):**
   - Ingests deals from Telegram channels, competitor channels, and AliExpress feeds.
   - Normalizes pricing (USD to Algerian Dinar DZD, official vs. parallel square market exchange rates).
   - Extracts product titles, cleaned descriptions, discount tiers, coupon codes, and target shipping country restrictions.
2. **AI Caption Generator (`app/ai/generator.py`):**
   - Synthesizes clean, high-conversion Arabic Telegram captions formatted with Telegram HTML blockquotes.
   - Removes cringe slang, cleans marketing hype, and formats store codes, spend thresholds, and direct affiliate links.
3. **Web API & User Frontend (`api/index.py`, `api/user_site.py`):**
   - Ultra-fast FastAPI backend deployed on Vercel serverless.
   - Vanilla JS frontend with zero heavyweight frameworks, utilizing a resilient embedded Tailwind design system.
   - Fully bilingual (Arabic RTL primary, English LTR secondary) with instantaneous dark/light mode toggling.
4. **Admin Management Dashboard (`api/admin_dashboard.py`):**
   - Obsidian Dark UI for reviewing crawled posts, manual publishing, queue management, editing captions, and auditing database states.
5. **Database & Persistence (`storage/deals.db`, `storage/state/`):**
   - SQLite relational storage storing `deals`, `source_messages`, `generated_posts`, and channel logs.

---

## 2. Chronological Step-by-Step Changelog (By Date & Phase)

### Phase 1: Security Hardening & Secret Management
**Date:** October 12, 2026  
**Commit:** `9c5940a`  
- **Objective:** Eliminate security risks and protect administrative endpoints.
- **Actions Taken:**
  - Removed all hardcoded fallback credentials and demo passwords from `api/admin_dashboard.py` and configuration files.
  - Enforced strict retrieval of sensitive secrets (`ADMIN_PASSWORD`, `TELEGRAM_BOT_TOKEN`, `CHANNEL_ID`, `DATABASE_URL`) from environment variables.
  - Implemented secure HTTP-only cookies and cryptographic session signatures for dashboard authentication.

---

### Phase 2: Bilingual UI Portal & Multi-Page Architecture
**Date:** October 12, 2026  
**Commits:** `ef4ecba`, `a788aa7`, `fe2672a`, `a302f2e`  
- **Objective:** Create a serious, modern bilingual portal with reliable modal and rendering lifecycle.
- **Actions Taken:**
  - Designed responsive RTL/LTR layouts with seamless switching between Arabic and English.
  - Replaced unstable external CDN Tailwind scripts with a resilient static embedded CSS system (`api/user_site.py`) to prevent layout shifts and CSS dropouts on mobile browsers.
  - Resolved deal modal initialization bugs: guaranteed modal is hidden on initial DOM load with defensive CSS `.hidden` classes and fail-safe escape key listeners.
  - Added official brand iconography and high-density SVG vectors.

---

### Phase 3: Resilient Telegram Scraping & Client Syntax Fixes
**Date:** October 13, 2026  
**Commits:** `f79097b`, `e991dc7`, `a03ace6`, `add876b`  
- **Objective:** Fix silent JavaScript crashes that broke deal rendering in Safari and mobile webviews.
- **Actions Taken:**
  - Identified root cause of client-side break: deal text strings containing unescaped raw newlines injected into client-side JS template literals caused `SyntaxError: unterminated string literal`.
  - Replaced faulty string splitting with robust regex `/\r?\n/` and JSON encoding of deal payloads.
  - Implemented dual client/server caching strategy: IndexedDB/localStorage client caching paired with 60-second edge HTTP caching to reduce serverless invocations on Vercel.
  - Fixed theme toggle flickering: eliminated blocking toast notifications when toggling light/dark mode and safeguarded `localStorage.getItem('theme')` initialization.

---

### Phase 4: Financial Tools, Cards Referral & Coin Calculators
**Date:** October 13, 2026  
**Commits:** `bcef37d`, `a27b248`, `f760c95`  
- **Objective:** Provide Algerian buyers with vital purchasing utilities for international checkout.
- **Actions Taken:**
  - Created Cards Referral & Payment Guide (`/cards`): Step-by-step activation guides for Bybit Virtual Card, RedotPay Visa, and Binance P2P funding methods.
  - Built the **Square Dinar Exchange Calculator**: Dynamic real-time converter translating USD prices directly to parallel market cash rates (Square Port Said DZD).
  - Built the **AliExpress Coins Link Generator**: Automated deep-link generator unlocking up to 70% additional discount via AliExpress Coins portal.

---

### Phase 5: Gamification Suite & Engagement Engine
**Date:** October 14, 2026  
**Commit:** `d7278b3`  
- **Objective:** Increase user retention and viral repeat visits.
- **Actions Taken:**
  - Built **Deal Roulette**: Interactive random deal picker allowing users to spin for curated flash sales.
  - Implemented **Daily Streak Tracker**: Rewards consistent daily visitors with gamified shopper ranks (Novice Hunter, Deal Scout, Pro Catcher, Master Bargainer).
  - Integrated **Tactile Haptic Favorites**: Local-first wishlist saving deals to offline storage with subtle vibration feedback on supported mobile devices.

---

### Phase 6: Anti-AI Slop & Editorial UI/UX Modernization
**Date:** October 14, 2026  
**Commits:** `b381edf`, `af05e59`, `87e58fd`  
- **Objective:** Purge cringe marketing slang, eliminate generic AI-generated aesthetic clutter, and elevate brand credibility.
- **Actions Taken:**
  - Removed tacky neon gradients, excessive emoji headers, and low-effort copy across all generated Telegram posts and web interfaces.
  - Upgraded typography stack:
    - Primary Arabic: `Readex Pro` & `Cairo`
    - Primary English / UI: `Plus Jakarta Sans`
    - Monospace / Promo Codes: `JetBrains Mono`
  - Normalized post footers with direct site links to `dealscoutgreen.vercel.app` and updated channel bios.

---

### Phase 7: Search Engine & Generative Engine Optimization (SEO & GEO)
**Date:** October 14, 2026  
**Commits:** `8157c0d`, `3a02f4b`, `a1034cf`  
- **Objective:** Dominate Algerian search queries for AliExpress deals and optimize for AI search agents (ChatGPT, Perplexity, Gemini).
- **Actions Taken:**
  - Engineered clean H1-H3 semantic document structure across all viewports.
  - Injected structured JSON-LD data: `FAQPage`, `WebApplication`, `BreadcrumbList`, and `speakable` schema specifications.
  - Implemented Generative Engine Optimization:
    - Created machine-readable `/llms.txt` and `/ai-summary`.
    - Added custom AI crawler directives in `robots.txt` granting access to GPTBot, PerplexityBot, and Google-Extended.
  - Authored comprehensive Algerian customs and shipping FAQ covering Yalidine, EMS, and parcel thresholds.

---

### Phase 8: Contact, Community & Channel Integration
**Date:** October 14, 2026  
**Commit:** `b6ecbd1`  
- **Objective:** Provide responsive community support without requiring complex bot server infrastructure.
- **Actions Taken:**
  - Replaced broken admin bot with direct Telegram Discussion Group integration (`t.me/deals_scout_community`).
  - Added streamlined feedback and error reporting options directly from deal modals.

---

### Phase 9: Admin Dashboard Redesign & Publishing Tools
**Date:** October 15, 2026  
**Commits:** `0b8a718`, `ac904e1`, `ac4b4b4`  
- **Objective:** Empower channel editors with a lightning-fast dark management workstation.
- **Actions Taken:**
  - Rebuilt `api/admin_dashboard.py` in Obsidian Dark palette (`#0B0F17`, `#111827`, `#059669`).
  - Implemented Arabic Tatweel (Kashida) normalization: Fixed regex failures caused by elongated letters (e.g., `الســــعودية` vs `السعودية`).
  - Stripped redundant `خلي البلد` country directives from public product titles, moving them cleanly to dedicated country alert tags.
  - Added dedicated missed deals manual publishing queue.

---

### Phase 10: Native Parcel Tracking Suite (17TRACK & Postal Ninja)
**Date:** October 15, 2026  
**Commits:** `ff8266c`, `6d18fdd`  
- **Objective:** Resolve user frustration with non-functional app-only Trackit iframe embeds by delivering a native web tracking solution.
- **Actions Taken:**
  - Analyzed Trackit.dz limitations: confirmed Trackit does not provide an open web API or embeddable iframe without requiring mobile app installation.
  - Replaced unusable iframe with a pristine, native carrier tracking dashboard:
    - Carrier selection tabs: **17TRACK** (Global / Yalidine / PostDZ), **Postal Ninja** (Detailed transit checkpoints), and **Official PostDZ**.
    - Embedded direct 1-click clipboard paste button for tracking numbers.
    - Added quick-status detection explaining Algerian customs statuses (Centre de Dédouanement Alger, Tri Postal Birtouta).

---

### Phase 11: Multi-Coupon Parsing & Country Hallucination Resolution
**Date:** October 15–16, 2026  
**Commits / Work in Progress:** `tests/test_multi_coupon.py`, `app/aliexpress/parser.py`, `api/index.py`, `api/user_site.py`, `app/ai/generator.py`  
- **User Problem Identified:**
  - When Telegram channels posted deals with multiple coupons (e.g., store coupons + AliExpress anniversary codes like `WOAE02`, `WOAE06`, `WOAE12`), only the first coupon was extracted.
  - Country hallucination bug: When a deal explicitly specified Saudi Arabia (`ضع البلد السعودية 🇸🇦`), the system erroneously defaulted to `كندا 🇨🇦` (Canada) and dropped coupons.
- **Root Cause Analysis:**
  1. `app/aliexpress/parser.py` -> `extract_country_instruction()` only checked Canada, Korea, Algeria, France, Spain, Ukraine, and Australia. When `ضع البلد السعودية 🇸🇦` appeared, it fell through to default: `return "كندا 🇨🇦"`.
  2. Multi-code lines with dollar tiers like `كوبون $2/15$: WOAE02` or multiple codes on one line `WOAE06 / WOAE12` were not parsed into an array.
  3. `deals.db` stored records that inherited this fallback.
- **Comprehensive Solution Executed:**
  1. **New Multi-Coupon Extraction Engine (`app/aliexpress/parser.py`):**
     - Extracts all coupons into `coupons: List[str]` and structured `coupon_details: List[Dict[str, str]]`.
     - Supports tier thresholds (`2/15$`, `6/49$`), store codes, and promo tags.
     - Built brand firewall: filtered out device model specs and brands (`realme`, `vivo`, `iqoo`, `8gb`, `ram`, `rom`, `used`) to eliminate false positives.
     - Added clean description parser stripping telegram tags and URLs to preserve specs like `خيار الشاحن لوحده 21.70$`.
  2. **Full Country & GCC Support:**
     - Added comprehensive detection for Saudi Arabia (`السعودية 🇸🇦`), UAE (`الإمارات 🇦🇪`), Qatar (`قطر 🇶🇦`), Kuwait (`الكويت 🇰🇼`), Bahrain (`البحرين 🇧🇭`), Oman (`عمان 🇴🇲`), Spain (`إسبانيا 🇪🇸`), and Ukraine (`أوكرانيا 🇺🇦`) across backend parser, AI caption generator, API endpoints, and client-side JS.
  3. **Deal Modal UI Upgrade (`api/user_site.py`):**
     - Added `#modal-multi-coupons`: renders each coupon as an interactive chip with its tier label and a dedicated 1-click copy button with checkmark feedback.
     - Added `#modal-country-alert`: displays prominent banner with country flag and instructions.
     - Added `#modal-desc-wrap`: cleanly presents product specifications and purchase notes.
  4. **Database Migration & Repair (`deals.db`):**
     - Scanned all records in `deals`, `source_messages`, and `generated_posts`.
     - Re-extracted accurate coupons and corrected all hallucinated `كندا 🇨🇦` entries back to their true countries.
  5. **Automated Testing Suite:**
     - Created `tests/test_multi_coupon.py` with 25 test cases covering complex Arabic formats, tatweel characters, multiple codes, and competitor filtering.

---

## 3. Component & File Directory Architecture

```
D:\Projects\TELEGRAM_REPO\
├── api/
│   ├── index.py                  # Serverless entry point; deal feed parser & telegram scraper
│   ├── user_site.py              # Main consumer website UI, deal modal, tracking suite & CSS
│   ├── admin_dashboard.py        # Obsidian dark editorial dashboard & manual publisher
│   ├── cards.py                  # Bybit / RedotPay / Binance P2P guide & referral page
│   ├── dinar.py                  # Parallel market Dinar exchange calculator
│   └── coins.py                  # AliExpress coins link generator & deep links
├── app/
│   ├── aliexpress/
│   │   ├── parser.py             # Multi-coupon engine, country extractor & title cleaner
│   │   └── client.py             # AliExpress API client & deep link resolver
│   ├── ai/
│   │   ├── generator.py          # Telegram HTML caption generator with blockquotes
│   │   └── prompts.py            # Strict editorial guidelines (no slang, no AI slop)
│   └── core/
│       ├── config.py             # Environment configuration & secret validator
│       └── database.py           # SQLite connection pool & ORM models
├── storage/
│   ├── deals.db                  # Primary relational SQLite database
│   └── state/
│       └── published_state.json  # Deduplication state & telegram message ID registry
├── tests/
│   ├── test_multi_coupon.py      # Multi-coupon & country extraction test suite (25 tests)
│   ├── test_parser.py            # Product link and title parsing tests
│   └── test_ai_generator.py      # Caption generation format tests
└── CONTEXT.md                    # This master project history and documentation
```

---

## 4. Database & State Architecture (`deals.db`)

### Schema Overview:
- **`deals` Table:**
  - `id`: Auto-incrementing primary key.
  - `product_title`: Cleaned, tatweel-normalized product title.
  - `original_price` / `sale_price`: Pricing in USD and normalized DZD.
  - `coupon_code`: Primary coupon code.
  - `country`: Target shipping restriction (e.g., `السعودية 🇸🇦`, `كندا 🇨🇦`, `الجزائر 🇩🇿`).
  - `url`: Direct AliExpress product URL.
  - `created_at`: Ingestion timestamp.
- **`source_messages` Table:**
  - `id`: Unique source message ID.
  - `raw_text`: Complete, unmodified post text from ingested channel.
  - `channel_name`: Origin channel handle.
- **`generated_posts` Table:**
  - `id`: Reference ID.
  - `caption`: Final generated Telegram post text with HTML blockquotes.
  - `is_published`: Publishing status flag.

---

## 5. Testing Suite & Verification Standards

All code modifications are verified against automated unit and integration tests using `pytest`.

### Key Verification Commands:
```bash
# Run multi-coupon and country detection suite
python -m pytest tests/test_multi_coupon.py -v

# Run full project test suite
python -m pytest -q
```

### Coverage Criteria:
- Zero false positives on product hardware specifications (RAM, ROM, phone models).
- Exact match on Gulf country emojis (🇸🇦, 🇦🇪, 🇶🇦, 🇰🇼, 🇧🇭, 🇴🇲).
- Strict adherence to 1-click clipboard copy UX standards with feedback toasts.

---

## 6. Git Commit Audit History

| Commit Hash | Date | Scope & Description |
|:---|:---|:---|
| `f4732ee` | 2026-10-16 | Fix card titles: display genuine product names, reject countries/hooks as titles |
| `aadc3b8` | 2026-10-16 | Fix JS syntax breaks (escaped regexes/newlines) & safeguard deal processor |
| `09cec25` | 2026-10-16 | Eliminate Auto-Canada bug, restore multi-coupons & strict country detection |
| `6d18fdd` | 2026-10-15 | Redesign tracking page with native UI, 17TRACK & Postal Ninja |
| `ff8266c` | 2026-10-15 | Integrate Trackit.dz live view and declutter UI/UX |
| `ac4b4b4` | 2026-10-15 | Eliminate 'خلي البلد' from deal titles; clean Algerian tracking |
| `ac904e1` | 2026-10-15 | Fix country tag extraction (tatweel normalization) & admin dark UI |
| `0b8a718` | 2026-10-15 | Publish missed Realme P3 Lite deal & admin UI redesign |
| `b6ecbd1` | 2026-10-14 | Replace admin bot with official discussion group; parcel tracker |
| `a1034cf` | 2026-10-14 | Generative Engine Optimization (llms.txt, ai-summary, schema) |
| `3a02f4b` | 2026-10-14 | Semantic H1-H3 hierarchy & Algerian buyer FAQ |
| `8157c0d` | 2026-10-14 | Organic search keywords & clean Telegram popup |
| `f760c95` | 2026-10-13 | Coins deal link generator & universal mobile viewport |
| `a27b248` | 2026-10-13 | Square Dinar calculator & mobile viewport polish |
| `d7278b3` | 2026-10-13 | Gamification suite: deal roulette, streak tracker, hunter ranks |
| `b381edf` | 2026-10-13 | Eliminate AI slop, gradients, and emoji clutter |
| `87e58fd` | 2026-10-13 | Correct website URL, clean slang, and prioritize newest deals |
| `af05e59` | 2026-10-13 | Upgrade typography with Readex Pro, Cairo, Plus Jakarta Sans |
| `add876b` | 2026-10-12 | Fix theme toggle blocking toast & protect storage |
| `a03ace6` | 2026-10-12 | Fix regex line split for Telegram post text |
| `e991dc7` | 2026-10-12 | Escape newlines in text.split to resolve JS syntax error |
| `bcef37d` | 2026-10-12 | Filter non-deal posts and add cards referral page |
| `a302f2e` | 2026-10-12 | Ensure modal is hidden on load with fail-safe display toggles |
| `fe2672a` | 2026-10-12 | Add resilient static Tailwind stylesheet & image bounds |
| `f79097b` | 2026-10-12 | Resolve JS syntax errors, dual client/server caching |
| `a788aa7` | 2026-10-12 | Official logo, title extraction fix, prominent coupon display |
| `ef4ecba` | 2026-10-12 | Bilingual portal with multi-page structure & mobile ergonomics |
| `9c5940a` | 2026-10-12 | Remove hardcoded passwords; enforce strict environment secrets |

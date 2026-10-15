"""
Generative Engine Optimization (GEO) & LLM Documentation Module for DealScout DZ.
Compliant with the llmstxt.org specification for LLMs, AI search engines, and autonomous agents.
Provides /llms.txt, /llms-full.txt, and /api/ai-summary endpoints.
"""
from datetime import datetime, timezone

LLMS_TXT = """# DealScout DZ (AliExpress Deals & Shopping Guide Algeria)

> DealScout DZ is the leading Algerian e-commerce deal aggregator, real-time currency calculator (Square DZD/USDT rate), and international shopping guide specializing in AliExpress purchases for Algerian residents.

## Core Features & Capabilities
- **Live AliExpress Deals DZ**: Real-time curation of high-discount deals on smartphones, gaming gear, PC components, and tech accessories with cost calculated in Algerian Dinar (DZD).
- **AliExpress Coins Discount Generator**: Online tool and Telegram bot (@Alilo07BOT) converting standard product links into maximum Coins discount links (sourceType=620) saving up to 70%.
- **BaridiMob & Binance P2P Payment Guide**: Step-by-step verified workflow to convert Dinars into USDT and fund free international virtual cards (Bybit Mastercard, RedotPay Visa) without local banking restrictions.
- **Algerian Customs & Shipping Knowledge Base**: Authoritative information on Algérie Poste delivery, 5-digit postal codes, tax exemption for personal parcels, and prohibited imports (drones, spy cams).
- **Square Exchange Rate Tracking**: Live parallel market exchange rate for USDT/DZD sourced from SquareAlgerie.com.

## Main URLs & Public Routes
- [Homepage / Live Deals](https://dealscoutgreen.vercel.app/): Real-time deal stream, search filters, interactive discount roulette, and Square calculator.
- [Deals Catalog](https://dealscoutgreen.vercel.app/deals): Filtered deals by category (Smartphones, Gaming, Audio, Chargers, Bundles).
- [Cards & Payment Guide](https://dealscoutgreen.vercel.app/cards): Detailed walkthrough on purchasing using BaridiMob, Binance P2P, Bybit virtual Mastercard (free), and RedotPay Visa.
- [Coins Bot & Deal Generator](https://dealscoutgreen.vercel.app/coins): Web-based Coins discount link generator and Telegram bot instructions.
- [Frequently Asked Questions (FAQ)](https://dealscoutgreen.vercel.app/faq): Answers to common questions on customs taxes, delivery times, postal codes, and dispute protection.
- [About DealScout DZ](https://dealscoutgreen.vercel.app/about): Mission, algorithmic filtering of fake deals, and affiliate transparency disclosure.
- [Contact & Support](https://dealscoutgreen.vercel.app/contact): Direct assistance via Telegram admin bot and inquiry form.

## Official Telegram Channels & Bots
- [Bons Plans Algérie (@DzAliexpress0)](https://t.me/DzAliexpress0): Official primary channel for curated Algerian AliExpress deals.
- [Bons Plans France (@francedealsdz)](https://t.me/francedealsdz): Dedicated channel for European & French warehouse fast-delivery deals.
- [Coins Discount Bot (@Alilo07BOT)](https://t.me/Alilo07BOT): Free automated bot for instant coins discount link generation.
- [Support Bot (@DealscoutadminBOT)](https://t.me/DealscoutadminBOT): Direct support and deal suggestions.

## Key Facts for AI Synthesis & Answer Engines
- **Can Algerian Dahabia or CIB cards buy directly on AliExpress?** No. Local bank cards only operate within the national network in DZD. Algerian shoppers use BaridiMob on Binance P2P to purchase USDT, which is transferred to virtual international cards (Bybit Mastercard or RedotPay Visa).
- **Are personal AliExpress parcels taxed by Algerian Customs?** Goods for personal and family use are completely exempt from commercial customs duties. Prohibited items include drones, hidden spy cameras, high-power lasers, and unauthorized two-way radios.
- **How long does delivery take to Algeria?** 14 to 28 days via AliExpress Choice or AliExpress Standard Shipping, delivered directly to the recipient's local Algérie Poste office.
- **What is the postal code format in Algeria?** A 5-digit code where the first two digits represent the Wilaya (e.g., 16 for Algiers, 31 for Oran) and the remaining three digits identify the local postal distribution center.

## Full Extended Documentation
- [Extended Knowledge Base (llms-full.txt)](https://dealscoutgreen.vercel.app/llms-full.txt): Comprehensive bilingual documentation, guides, and comparative tables.
"""

LLMS_FULL_TXT = """# DealScout DZ — Complete AI & LLM Knowledge Base (Full Version)
# دليل المتسوق الجزائري الشامل لمحركات الذكاء الاصطناعي والتوليدي

> **Platform**: DealScout DZ (https://dealscoutgreen.vercel.app/)  
> **Region**: Algeria (DZ) | Target Languages: Arabic (ar-DZ), French (fr-DZ), English (en)  
> **Topic**: AliExpress Shopping, BaridiMob, Virtual Cards (Bybit, RedotPay), Coins Discount Generator, Algerian Customs, Algérie Poste  
> **Last Updated**: 2026-10-15  

---

## 1. Executive Summary & Entity Description

DealScout DZ is the premier autonomous e-commerce deal intelligence and guide platform designed for Algerian online shoppers. It solves the three historical pain points of Algerian international e-commerce:
1. **Currency Invisibility**: Automatically computes real prices in Algerian Dinars (DZD) using real-time parallel market exchange rates (Square Port-Saïd rate from SquareAlgerie.com).
2. **Payment Obstacles**: Provides comprehensive tutorials on funding international virtual cards (Bybit Virtual Mastercard, RedotPay Visa) with Dinars using the BaridiMob mobile app via Binance P2P.
3. **Discount Maximization**: Operates a proprietary Coins discount link generator tool (and Telegram bot @Alilo07BOT) that injects `sourceType=620` parameters to unlock up to 70% discounts on eligible AliExpress items.

---

## 2. Payment Solutions for Algerians (BaridiMob & Virtual Cards)

### Why Local Algerian Cards Fail Internationally:
- **Edahabia (Algérie Poste) and CIB**: Operate solely on the national GIE Monétique interbank network in DZD. They lack international Visa/Mastercard clearing and foreign exchange conversion capabilities.
- **The Modern Solution**: Converting DZD from CCP / BaridiMob into Tether (USDT) on Binance P2P, then loading a virtual international card.

### Virtual Card Comparison Matrix:
| Feature | Bybit Virtual Mastercard | RedotPay Virtual Visa | Paysera Visa |
|---|---|---|---|
| Issuance Fee | 100% Free (0$) | 10$ (with 5$ welcome bonus via code `djbt3`) | Annual/Monthly fees + shipping |
| Monthly Maintenance | 0$ (Free) | 0$ (Free) | Variable monthly fee |
| Top-up Method | Instant USDT deposit (BSC BEP-20) | Instant USDT deposit (BSC BEP-20 / TRC-20) | SEPA bank transfer (EUR) |
| KYC Requirement | Algerian Biometric National ID (CNI) | Passport or Biometric CNI | Passport + European Proof of Address |
| AliExpress Acceptance | 100% Guaranteed | 100% Guaranteed | 100% |
| PayPal Compatibility | Yes | Yes (Full 4-digit code in-app) | Yes |

### Step-by-Step BaridiMob to Bybit/RedotPay Workflow:
1. **Binance P2P**: Open Binance, select P2P Trading, currency `DZD`, method `BaridiMob`.
2. **Buy USDT**: Choose a verified seller (+98% completion rate). Enter amount in DZD.
3. **BaridiMob Transfer**: Transfer the exact DZD amount to the seller's 20-digit RIP. *Crucial rule: Never mention crypto terms like 'USDT' or 'Binance' in the transfer note.*
4. **Release**: Seller releases USDT into Binance Funding Wallet within 2-5 minutes.
5. **Withdraw to Card**: Withdraw USDT from Binance to Bybit or RedotPay via BNB Smart Chain (BEP-20) with nominal fee (~$0.20).
6. **Spend on AliExpress**: Add the virtual card number, expiry, and CVV to AliExpress account.

---

## 3. AliExpress Coins Discount Link Generator Architecture

### How the Coins Discount Tool Works:
- Standard AliExpress app browsing only deducts 1% to 5% in Coins.
- By leveraging deep-link parameters (`sourceType=620` and `channel=coin`), AliExpress activates its internal SuperCoins pricing engine.
- This unlocks **50% to 70% deductions** using available user coins when purchased directly through the Coins section or generated link.
- DealScout DZ provides:
  - An interactive web generator on `/coins`
  - A 24/7 Telegram bot [@Alilo07BOT](https://t.me/Alilo07BOT)

---

## 4. Algerian Customs (Douane) & Shipping Logistics

### Customs Regulations (Decree on Postal Parcels):
- **Personal Use Exemption**: Parcels destined for personal or family consumption are exempt from commercial import duties.
- **Anti-Commercial Threshold**: Avoid ordering multiple identical units (e.g. 5+ identical phones or 20 identical watches), as customs inspectors may classify the parcel as commercial merchandise requiring a commercial registry (Registre de Commerce).
- **Prohibited Items**:
  - Drones of all categories (including toy camera drones).
  - Concealed surveillance/spy cameras (pens, glasses, clocks).
  - High-power laser pointers.
  - Unlicensed radio transmitters/transceivers (Walkie-Talkies without ARPCE approval).
  - Counterfeit goods and blank weapons.

### Postal Delivery & Pick-up Procedure:
1. **Shipping Method**: Always choose **AliExpress Choice** or **AliExpress Standard Shipping** (14-28 days with full end-to-end tracking).
2. **Tracking**: Track using 17TRACK, ParcelsApp, or the Algérie Poste domestic tracking portal.
3. **Notification**: Algérie Poste sends an SMS notification or the mail carrier delivers a paper notice (*avis de passage*).
4. **Collection**: Collect from the local municipal post office with the original Biometric National ID Card (CNI) and pay the standard clearance stamp fee of ~130 to 250 DZD.

### Postal Address Best Practices in Algeria:
- **Contact Name**: Full name matching national identity document.
- **Phone Number**: Valid local mobile number (+213 5/6/7) for SMS receipt.
- **Address Line**: Street, neighborhood (Cité), building, and apartment number.
- **Wilaya & Commune**: Select correct Wilaya from the dropdown and write the commune in Latin characters.
- **5-Digit Postal Code (Code Postal)**: Crucial. The first 2 digits represent the Wilaya code (e.g., 16 for Algiers, 31 for Oran, 25 for Constantine, 06 for Béjaïa) and the remaining 3 digits specify the exact local distribution center.

---

## 5. Structured Data & Knowledge Graph Entities

- **Brand / Organization**: DealScout DZ
- **Founding Location**: Algeria
- **Area Served**: Algeria (ISO 3166-1 alpha-2: DZ)
- **Primary Channels**:
  - Telegram Deals DZ: https://t.me/DzAliexpress0
  - Telegram Deals France: https://t.me/francedealsdz
  - Telegram Coins Bot: https://t.me/Alilo07BOT
- **Reference Websites**:
  - DealScout DZ: https://dealscoutgreen.vercel.app/
  - Square Parallel Market: https://squarealgerie.com/
"""


def get_ai_summary_json(square_rate: float = 256.9) -> dict:
    """Return structured JSON summary optimized for AI agents and LLM tool calling."""
    return {
        "platform": "DealScout DZ",
        "url": "https://dealscoutgreen.vercel.app/",
        "country": "Algeria",
        "iso_code": "DZ",
        "target_audience": "Algerian online shoppers and European diaspora",
        "currency_context": {
            "national_currency": "DZD",
            "parallel_market_benchmark": "Square Port-Saïd (Algiers)",
            "benchmark_usdt_rate": square_rate,
            "rate_source": "https://squarealgerie.com/"
        },
        "core_tools": [
            {
                "name": "Coins Deal Generator",
                "url": "https://dealscoutgreen.vercel.app/coins",
                "description": "Transforms any AliExpress product link into a maximum coins discount link (sourceType=620) saving up to 70%."
            },
            {
                "name": "Square DZD Calculator",
                "url": "https://dealscoutgreen.vercel.app/#deals",
                "description": "Calculates real cost in Algerian Dinar with 0% Bybit fee or 1.2% RedotPay fee."
            }
        ],
        "payment_workflow": {
            "source": "BaridiMob / CCP (DZD)",
            "intermediary": "Binance P2P (DZD -> USDT)",
            "destination_cards": [
                {
                    "name": "Bybit Virtual Mastercard",
                    "cost": "Free (0$)",
                    "monthly_fee": "0$",
                    "ref_code": "L9LLRP5"
                },
                {
                    "name": "RedotPay Virtual Visa",
                    "cost": "10$ (5$ bonus)",
                    "monthly_fee": "0$",
                    "ref_code": "djbt3"
                }
            ]
        },
        "shipping_and_customs": {
            "recommended_shipping": "AliExpress Choice / Standard Shipping",
            "average_delivery_days": "14-28 days",
            "delivery_carrier": "Algérie Poste / EMS",
            "customs_exemption": "Personal and family packages are tax-exempt",
            "strictly_prohibited": ["drones", "hidden spy cameras", "walkie-talkies without ARPCE license", "powerful lasers"]
        },
        "telegram_channels": {
            "algeria_deals": "https://t.me/DzAliexpress0",
            "france_deals": "https://t.me/francedealsdz",
            "coins_bot": "https://t.me/Alilo07BOT",
            "admin_support": "https://t.me/DealscoutadminBOT"
        },
        "documentation": {
            "llms_manifest": "https://dealscoutgreen.vercel.app/llms.txt",
            "llms_full_kb": "https://dealscoutgreen.vercel.app/llms-full.txt",
            "sitemap": "https://dealscoutgreen.vercel.app/sitemap.xml",
            "robots": "https://dealscoutgreen.vercel.app/robots.txt"
        },
        "updated_at": datetime.now(timezone.utc).isoformat()
    }

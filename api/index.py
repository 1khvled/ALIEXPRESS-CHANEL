"""
Vercel Serverless Entry Point — DealScout Modern PWA Dashboard
Features:
- Progressive Web App (PWA) installable on Android, iOS, Windows, and Mac
- Mobile-first responsive glassmorphic UI with bottom navigation
- Live SquareAlgerie.com USDT exchange rate integration
- In-Dashboard Instant AliExpress Deal Scout tool
- Channel post monitor with photos and direct affiliate links
"""
import os
import re
import time
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any, List

try:
    from dotenv import load_dotenv
    from pathlib import Path
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except Exception:
    pass
from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse, Response, FileResponse
import httpx
import copy
import hashlib
import hmac
from bs4 import BeautifulSoup
from api.user_site import USER_WEBSITE_HTML
from api.admin_login import ADMIN_LOGIN_HTML
from api.admin_dashboard import DASHBOARD_HTML
from api.geo_llms import LLMS_TXT, LLMS_FULL_TXT, get_ai_summary_json
from api.blog_guide import get_blog_guide_html

app = FastAPI(title="DealScout DZ — AliExpress Deals & Live Telegram Content", version="2.5.0")

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    if request.url.scheme == "https" or request.headers.get("x-forwarded-proto") == "https":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

# ── Manifest JSON ───────────────────────────────────────────────
MANIFEST_JSON = """{
  "name": "DealScout DZ — AliExpress Deals & Coin Discounts",
  "short_name": "DealScout",
  "description": "Algeria's #1 AliExpress Deals, Coin Discounts & Live SquareAlgerie USDT Rates Tracker",
  "start_url": "/",
  "display": "standalone",
  "orientation": "portrait-primary",
  "background_color": "#020617",
  "theme_color": "#e11d48",
  "icons": [
    {
      "src": "/icon.svg",
      "sizes": "any",
      "type": "image/svg+xml",
      "purpose": "any maskable"
    }
  ]
}"""

# ── Service Worker ──────────────────────────────────────────────
SW_JS = """// DealScout PWA Service Worker
const CACHE_NAME = 'dealscout-v2';
const STATIC_ASSETS = [
  '/',
  '/manifest.json',
  '/icon.svg',
  'https://cdn.tailwindcss.com',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(STATIC_ASSETS)).catch(() => {})
  );
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (e) => {
  if (e.request.method !== 'GET') return;
  // Network first with cache fallback
  e.respondWith(
    fetch(e.request)
      .then((response) => {
        if (response && response.status === 200 && response.type === 'basic') {
          const resClone = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(e.request, resClone));
        }
        return response;
      })
      .catch(() => caches.match(e.request))
  );
});
"""

# ── App Icon SVG ────────────────────────────────────────────────
ICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#e11d48"/>
      <stop offset="50%" stop-color="#f59e0b"/>
      <stop offset="100%" stop-color="#020617"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="8" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <rect width="512" height="512" rx="128" fill="url(#bg)"/>
  <rect x="16" y="16" width="480" height="480" rx="112" fill="#090d16" fill-opacity="0.88"/>
  <path d="M280 48L140 280h100L220 464l172-256H280z" fill="#f43f5e" filter="url(#glow)"/>
  <path d="M270 64L160 270h90L234 430l138-206H270z" fill="#fbbf24"/>
</svg>"""

# ── Modern Responsive PWA Dashboard HTML ─────────────────────────
# DASHBOARD_HTML is modularly imported from api.admin_dashboard


def get_active_event_seo_html() -> str:
    """Injects real-time active promotional event keywords, deals, and descriptions into HTML for instant SEO indexing."""
    html = USER_WEBSITE_HTML
    try:
        from app.aliexpress.promos import promo_tracker
        now = datetime.now(timezone.utc)
        ev = promo_tracker.get_active_promo(now)
        if ev:
            active_codes = ", ".join([t["code"] for t in (ev.coupon_tiers or []) if "code" in t])
            top_deals = "Honor X70 5G, realme 15T 5G, OPPO A6 Pro, iQOO Z11s 5G, realme Watch 5, AMD Ryzen 5 8400F, Redmi Note 12 5G, CUSU SSD 512GB, Blackview Wave 10C"
            event_kw = f"{ev.name}, {ev.name_ar}, {ev.name_fr}, تخفيضات {ev.name_ar}, كود خصم {ev.name}, {active_codes}, {top_deals}"
            html = re.sub(
                r'<meta name="keywords" content="[^"]*">',
                f'<meta name="keywords" content="{event_kw}, aliexpressdz, aliexpress deals dz, aliexpress deald dz, عروض علي اكسبراس, شراء من علي اكسبراس في الجزائر, علي اكسبراس الجزائر, تخفيضات علي اكسبراس, كود تخفيض علي اكسبراس الجزائر, aliexpress algerie, شراء من علي اكسبرس بريدي موب, بطاقة بايبايت في الجزائر, تخفيضات AliExpress الجزائر">',
                html,
                count=1
            )
            active_desc = f"عروض وتخفيضات {ev.name_ar} الحصرية على AliExpress بالدينار الجزائري. صفقات فعالة مع أكواد الخصم ({active_codes}) لأجهزة {top_deals} والدفع بـ BaridiMob."
            html = re.sub(
                r'<meta name="description" id="meta-description" content="[^"]*">',
                f'<meta name="description" id="meta-description" content="{active_desc}">',
                html,
                count=1
            )
            event_title = f"{ev.name_ar} — أحدث صفقات وتخفيضات AliExpress بالدينار الجزائري | DealScout DZ"
            html = re.sub(
                r'<meta property="og:title" id="og-title" content="[^"]*">',
                f'<meta property="og:title" id="og-title" content="{event_title}">',
                html,
                count=1
            )
    except Exception:
        pass
    return html


# ── Web App & PWA Routes ─────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
@app.get("/deals", response_class=HTMLResponse)
@app.get("/tracking", response_class=HTMLResponse)
@app.get("/cards", response_class=HTMLResponse)
@app.get("/coins", response_class=HTMLResponse)
@app.get("/faq", response_class=HTMLResponse)
@app.get("/contact", response_class=HTMLResponse)
@app.get("/about", response_class=HTMLResponse)
async def user_website():
    """Serves the modern user-facing AliExpress deals website with live Telegram feed and dynamic active event SEO."""
    return HTMLResponse(content=get_active_event_seo_html())


@app.get("/blog/aliexpress-algeria-guide-dz", response_class=HTMLResponse)
@app.get("/guide", response_class=HTMLResponse)
@app.get("/blog", response_class=HTMLResponse)
async def blog_guide_page():
    """Serves the comprehensive AliExpress Algeria 2026 native guide blog article."""
    return HTMLResponse(content=get_blog_guide_html(), status_code=200)


ADMIN_SESSION_COOKIE = "dealscout_admin_session"
_login_failed_attempts: Dict[str, List[float]] = {}
MAX_FAILED_ATTEMPTS = 5
LOCKOUT_DURATION_SECONDS = 900  # 15 minutes


def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "127.0.0.1"


def check_login_rate_limit(client_ip: str) -> Optional[int]:
    """Returns seconds remaining if locked out, or None if allowed."""
    now = time.time()
    attempts = _login_failed_attempts.get(client_ip, [])
    recent = [t for t in attempts if now - t < LOCKOUT_DURATION_SECONDS]
    _login_failed_attempts[client_ip] = recent
    if len(recent) >= MAX_FAILED_ATTEMPTS:
        oldest_relevant = recent[0]
        remaining = int(LOCKOUT_DURATION_SECONDS - (now - oldest_relevant))
        return max(1, remaining)
    return None


def record_failed_login(client_ip: str):
    now = time.time()
    if client_ip not in _login_failed_attempts:
        _login_failed_attempts[client_ip] = []
    _login_failed_attempts[client_ip].append(now)


def reset_login_attempts(client_ip: str):
    _login_failed_attempts.pop(client_ip, None)


def get_admin_auth_secret() -> Optional[str]:
    """
    Retrieves the admin password strictly from environment variables.
    Checks ADMIN_PASSWORD, ADMIN_BOT_TOKEN, or TELEGRAM_BOT_TOKEN.
    Zero hardcoded passwords in code or HTML.
    """
    for env_var in ["ADMIN_PASSWORD", "ADMIN_BOT_TOKEN", "TELEGRAM_BOT_TOKEN"]:
        val = os.getenv(env_var)
        if val and val.strip():
            return val.strip()
    return None


def get_expected_admin_token() -> Optional[str]:
    secret = get_admin_auth_secret()
    if not secret:
        return None
    return hashlib.sha256(f"dealscout:{secret}".encode()).hexdigest()


def is_admin_authenticated(request: Request) -> bool:
    """Checks if request has a valid admin session cookie, token, or bearer header."""
    expected_token = get_expected_admin_token()
    secret = get_admin_auth_secret()
    if not expected_token or not secret:
        return False

    # 1. Check session cookie
    token = request.cookies.get(ADMIN_SESSION_COOKIE)
    if token and hmac.compare_digest(token, expected_token):
        return True

    # 2. Check query param ?key=... or ?token=... or ?pass=...
    key = request.query_params.get("key") or request.query_params.get("token") or request.query_params.get("pass")
    if key and (hmac.compare_digest(key, secret) or hmac.compare_digest(key, expected_token)):
        return True

    # 3. Check Authorization header
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        bearer = auth_header.replace("Bearer ", "").strip()
        if hmac.compare_digest(bearer, secret) or hmac.compare_digest(bearer, expected_token):
            return True

    return False


@app.get("/robots.txt", response_class=Response)
async def robots_txt():
    """Generative Engine Optimization (GEO) & Search Engine Optimization robots.txt"""
    content = """User-agent: *
Allow: /
Allow: /deals
Allow: /tracking
Allow: /cards
Allow: /coins
Allow: /faq
Allow: /about
Allow: /contact
Allow: /blog
Allow: /blog/aliexpress-algeria-guide-dz
Allow: /guide
Allow: /llms.txt
Allow: /llms-full.txt
Allow: /manifest.json
Allow: /icon.svg
Allow: /sw.js
Disallow: /admin
Disallow: /dashboard
Disallow: /api/

# Generative AI, LLM & Answer Engine Crawlers (GEO)
User-agent: GPTBot
Allow: /
Allow: /llms.txt
Allow: /llms-full.txt

User-agent: ChatGPT-User
Allow: /
Allow: /llms.txt
Allow: /llms-full.txt

User-agent: PerplexityBot
Allow: /
Allow: /llms.txt
Allow: /llms-full.txt

User-agent: ClaudeBot
Allow: /
Allow: /llms.txt
Allow: /llms-full.txt

User-agent: Claude-Web
Allow: /
Allow: /llms.txt
Allow: /llms-full.txt

User-agent: Google-Extended
Allow: /
Allow: /llms.txt
Allow: /llms-full.txt

User-agent: Applebot-Extended
Allow: /
Allow: /llms.txt
Allow: /llms-full.txt

User-agent: cohere-ai
Allow: /
Allow: /llms.txt
Allow: /llms-full.txt

Sitemap: https://dealscoutgreen.vercel.app/sitemap.xml
"""
    return Response(
        content=content,
        media_type="text/plain",
        headers={"Cache-Control": "public, max-age=86400"}
    )


@app.get("/llms.txt", response_class=Response)
async def get_llms_txt():
    """
    Standard llms.txt endpoint for LLMs, Generative AI engines, and AI agents.
    Provides concise, structured markdown manifest with key URLs, capabilities, and guidance.
    Reference: https://llmstxt.org/
    """
    return Response(
        content=LLMS_TXT,
        media_type="text/plain; charset=utf-8",
        headers={"Cache-Control": "public, max-age=3600"}
    )


@app.get("/llms-full.txt", response_class=Response)
async def get_llms_full_txt():
    """
    Complete extended knowledge base for LLMs and Generative Search engines.
    Provides in-depth Algerian shopping guides, customs rules, address format, and comparison tables.
    """
    return Response(
        content=LLMS_FULL_TXT,
        media_type="text/plain; charset=utf-8",
        headers={"Cache-Control": "public, max-age=3600"}
    )


@app.get("/api/ai-summary")
async def get_ai_summary():
    """
    Structured JSON endpoint for AI agents, generative reasoning models, and search indexers.
    Returns live rates, active tools, verified payment workflows, and FAQ facts.
    """
    rate = 256.9
    try:
        from storage.deal_storage import get_square_rate
        stored_rate = get_square_rate()
        if stored_rate and stored_rate > 100:
            rate = float(stored_rate)
    except Exception:
        pass
    return JSONResponse(
        content=get_ai_summary_json(square_rate=rate),
        headers={"Cache-Control": "public, max-age=300"}
    )


@app.get("/api/track-parcel")
async def api_track_parcel(num: str = ""):
    """
    Parcel tracking endpoint for Algerian AliExpress shoppers.
    Supports Cainiao, Algérie Poste, SunYou, Yanwen, and international UPU codes.
    """
    cleaned_param = (num or "").strip()
    if not cleaned_param or len(cleaned_param) < 3:
        return JSONResponse(
            status_code=400,
            content={"ok": False, "error": "يرجى إدخال رقم تتبع صالح / Numéro de suivi invalide"}
        )
    from api.parcel_tracker import track_algeria_parcel
    result = await track_algeria_parcel(cleaned_param)
    return JSONResponse(
        content=result,
        headers={"Cache-Control": "public, max-age=60"}
    )


@app.get("/sitemap.xml", response_class=Response)
async def sitemap_xml():
    """Dynamic Search Engine Sitemap with multilingual and image metadata"""
    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
  <url>
    <loc>https://dealscoutgreen.vercel.app/</loc>
    <xhtml:link rel="alternate" hreflang="ar" href="https://dealscoutgreen.vercel.app/"/>
    <xhtml:link rel="alternate" hreflang="ar-DZ" href="https://dealscoutgreen.vercel.app/"/>
    <xhtml:link rel="alternate" hreflang="fr" href="https://dealscoutgreen.vercel.app/"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://dealscoutgreen.vercel.app/"/>
    <lastmod>{datetime.now(timezone.utc).strftime("%Y-%m-%d")}</lastmod>
    <changefreq>hourly</changefreq>
    <priority>1.0</priority>
    <image:image>
      <image:loc>https://dealscoutgreen.vercel.app/icon.svg</image:loc>
      <image:title>DealScout DZ — صفقات وتخفيضات AliExpress بالدينار الجزائري</image:title>
    </image:image>
  </url>
  <url>
    <loc>https://dealscoutgreen.vercel.app/deals</loc>
    <xhtml:link rel="alternate" hreflang="ar" href="https://dealscoutgreen.vercel.app/deals"/>
    <xhtml:link rel="alternate" hreflang="ar-DZ" href="https://dealscoutgreen.vercel.app/deals"/>
    <xhtml:link rel="alternate" hreflang="fr" href="https://dealscoutgreen.vercel.app/deals"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://dealscoutgreen.vercel.app/deals"/>
  </url>
  <url>
    <loc>https://dealscoutgreen.vercel.app/tracking</loc>
    <xhtml:link rel="alternate" hreflang="ar" href="https://dealscoutgreen.vercel.app/tracking"/>
    <xhtml:link rel="alternate" hreflang="ar-DZ" href="https://dealscoutgreen.vercel.app/tracking"/>
    <xhtml:link rel="alternate" hreflang="fr" href="https://dealscoutgreen.vercel.app/tracking"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://dealscoutgreen.vercel.app/tracking"/>
    <lastmod>{datetime.now(timezone.utc).strftime("%Y-%m-%d")}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://dealscoutgreen.vercel.app/cards</loc>
    <xhtml:link rel="alternate" hreflang="ar" href="https://dealscoutgreen.vercel.app/cards"/>
    <xhtml:link rel="alternate" hreflang="ar-DZ" href="https://dealscoutgreen.vercel.app/cards"/>
    <xhtml:link rel="alternate" hreflang="fr" href="https://dealscoutgreen.vercel.app/cards"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://dealscoutgreen.vercel.app/cards"/>
    <lastmod>{datetime.now(timezone.utc).strftime("%Y-%m-%d")}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
    <image:image>
      <image:loc>https://dealscoutgreen.vercel.app/logo.png</image:loc>
      <image:title>بطاقات الشراء من AliExpress بالدينار الجزائري — Bybit و RedotPay و BaridiMob</image:title>
    </image:image>
  </url>
  <url>
    <loc>https://dealscoutgreen.vercel.app/coins</loc>
    <xhtml:link rel="alternate" hreflang="ar" href="https://dealscoutgreen.vercel.app/coins"/>
    <xhtml:link rel="alternate" hreflang="ar-DZ" href="https://dealscoutgreen.vercel.app/coins"/>
    <xhtml:link rel="alternate" hreflang="fr" href="https://dealscoutgreen.vercel.app/coins"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://dealscoutgreen.vercel.app/coins"/>
    <lastmod>{datetime.now(timezone.utc).strftime("%Y-%m-%d")}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://dealscoutgreen.vercel.app/faq</loc>
    <xhtml:link rel="alternate" hreflang="ar" href="https://dealscoutgreen.vercel.app/faq"/>
    <xhtml:link rel="alternate" hreflang="ar-DZ" href="https://dealscoutgreen.vercel.app/faq"/>
    <xhtml:link rel="alternate" hreflang="fr" href="https://dealscoutgreen.vercel.app/faq"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://dealscoutgreen.vercel.app/faq"/>
    <lastmod>{datetime.now(timezone.utc).strftime("%Y-%m-%d")}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>https://dealscoutgreen.vercel.app/about</loc>
    <xhtml:link rel="alternate" hreflang="ar" href="https://dealscoutgreen.vercel.app/about"/>
    <xhtml:link rel="alternate" hreflang="ar-DZ" href="https://dealscoutgreen.vercel.app/about"/>
    <xhtml:link rel="alternate" hreflang="fr" href="https://dealscoutgreen.vercel.app/about"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://dealscoutgreen.vercel.app/about"/>
    <lastmod>{datetime.now(timezone.utc).strftime("%Y-%m-%d")}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
  <url>
    <loc>https://dealscoutgreen.vercel.app/contact</loc>
    <xhtml:link rel="alternate" hreflang="ar" href="https://dealscoutgreen.vercel.app/contact"/>
    <xhtml:link rel="alternate" hreflang="ar-DZ" href="https://dealscoutgreen.vercel.app/contact"/>
    <xhtml:link rel="alternate" hreflang="fr" href="https://dealscoutgreen.vercel.app/contact"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://dealscoutgreen.vercel.app/contact"/>
    <lastmod>{datetime.now(timezone.utc).strftime("%Y-%m-%d")}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
  <url>
    <loc>https://dealscoutgreen.vercel.app/blog/aliexpress-algeria-guide-dz</loc>
    <xhtml:link rel="alternate" hreflang="ar" href="https://dealscoutgreen.vercel.app/blog/aliexpress-algeria-guide-dz"/>
    <xhtml:link rel="alternate" hreflang="ar-DZ" href="https://dealscoutgreen.vercel.app/blog/aliexpress-algeria-guide-dz"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://dealscoutgreen.vercel.app/blog/aliexpress-algeria-guide-dz"/>
    <lastmod>{datetime.now(timezone.utc).strftime("%Y-%m-%d")}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
    <image:image>
      <image:loc>https://dealscoutgreen.vercel.app/logo.png</image:loc>
      <image:title>دليل الشراء من AliExpress في الجزائر 2026: الشحن والجمارك والدفع بالدينار</image:title>
    </image:image>
  </url>
  <url>
    <loc>https://dealscoutgreen.vercel.app/llms.txt</loc>
    <lastmod>{datetime.now(timezone.utc).strftime("%Y-%m-%d")}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://dealscoutgreen.vercel.app/llms-full.txt</loc>
    <lastmod>{datetime.now(timezone.utc).strftime("%Y-%m-%d")}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>"""
    return Response(
        content=xml_content,
        media_type="application/xml",
        headers={"Cache-Control": "public, max-age=3600"}
    )


@app.get("/admin", response_class=HTMLResponse)
@app.get("/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    """Serves the administrative management and deal publishing dashboard behind password protection."""
    if not is_admin_authenticated(request):
        return HTMLResponse(content=ADMIN_LOGIN_HTML)
    return HTMLResponse(content=DASHBOARD_HTML)


@app.post("/api/admin/login")
async def admin_login(request: Request):
    """Authenticates admin password strictly from environment variables with brute-force rate limiting."""
    client_ip = get_client_ip(request)
    lockout_remaining = check_login_rate_limit(client_ip)
    if lockout_remaining:
        mins = max(1, lockout_remaining // 60)
        return JSONResponse({
            "success": False,
            "error": f"تم حظر تسجيل الدخول مؤقتاً لكثرة المحاولات الخاطئة. يرجى المحاولة بعد {mins} دقيقة."
        }, status_code=429)

    secret = get_admin_auth_secret()
    if not secret:
        return JSONResponse({
            "success": False,
            "error": "لم يتم ضبط كلمة مرور الأدمن (ADMIN_PASSWORD) في متغيرات البيئة. يرجى إضافتها في إعدادات Vercel."
        }, status_code=500)

    try:
        data = await request.json()
        password = str(data.get("password", "")).strip()
    except Exception:
        password = ""

    if not password:
        return JSONResponse({"success": False, "error": "يرجى إدخال كلمة المرور"}, status_code=400)

    if hmac.compare_digest(password, secret):
        reset_login_attempts(client_ip)
        expected_token = get_expected_admin_token()
        resp = JSONResponse({"success": True, "message": "تم تسجيل الدخول بنجاح"})
        resp.set_cookie(
            key=ADMIN_SESSION_COOKIE,
            value=expected_token,
            max_age=60 * 60 * 24 * 7,  # 7 days
            httponly=True,
            samesite="lax"
        )
        return resp

    record_failed_login(client_ip)
    return JSONResponse({"success": False, "error": "كلمة المرور غير صحيحة!"}, status_code=401)


@app.get("/api/admin/logout")
@app.post("/api/admin/logout")
async def admin_logout():
    """Logs out admin and redirects back to admin login page."""
    from fastapi.responses import RedirectResponse
    resp = RedirectResponse(url="/admin", status_code=303)
    resp.delete_cookie(ADMIN_SESSION_COOKIE)
    return resp


# In-memory deals cache with 60s TTL
_DEALS_CACHE = {}


def parse_telegram_deal_block(block, clean_ch: str, usdt_rate: float = 249.0):
    """Parses a Telegram web preview widget into a structured Deal object."""
    text_div = block.find("div", class_="tgme_widget_message_text")
    if not text_div:
        return None

    tdiv_clone = copy.copy(text_div)
    for br in tdiv_clone.find_all("br"):
        br.replace_with("\n")
    raw_text = tdiv_clone.get_text().strip()
    if not raw_text:
        return None

    data_post = block.get("data-post", "")
    msg_id = data_post.split("/")[-1] if "/" in data_post else ""
    telegram_url = f"https://t.me/{data_post}" if data_post else f"https://t.me/{clean_ch}"

    photo_url = None
    photo_wrap = block.find("a", class_="tgme_widget_message_photo_wrap")
    if photo_wrap and photo_wrap.get("style"):
        m = re.search(r"url\('([^']+)'\)", photo_wrap["style"])
        if m:
            photo_url = m.group(1)
    if not photo_url:
        img_tag = block.find("img")
        if img_tag and img_tag.get("src"):
            photo_url = img_tag["src"]

    date_str = ""
    time_el = block.find("time")
    if time_el and time_el.get("datetime"):
        try:
            dt = datetime.fromisoformat(time_el["datetime"].replace("Z", "+00:00"))
            date_str = dt.strftime("%Y-%m-%d %H:%M")
        except Exception:
            date_str = time_el.get("datetime", "")

    link_m = re.search(r'https?://s\.click\.aliexpress\.com/e/[A-Za-z0-9_-]+', raw_text)
    affiliate_url = link_m.group(0) if link_m else telegram_url

    is_tajmi3at = any(k in raw_text for k in ["تجميعة", "أقوى عروض", "Récapitulatif", "Meilleurs Bons Plans"])

    title = None
    title_m = re.search(r'✅\s*([^\n]+)', raw_text)
    if title_m:
        title = title_m.group(1).strip()
    elif "تخفيض لـ" in raw_text:
        t_m = re.search(r'تخفيض لـ\s*([^\n]+)', raw_text)
        if t_m:
            title = t_m.group(1).strip()
    elif is_tajmi3at:
        title = raw_text.split("\n")[0].replace("📱", "").replace("🎮", "").replace("🔥", "").strip()
    else:
        for line in raw_text.split("\n"):
            line_s = line.strip()
            if line_s and not any(p in line_s for p in ["📍", "خلي", "http", "بوت", "📢", "@", "💰", "🎟️"]):
                title = line_s
                break
    coupons = []
    coupon_details = []
    clean_description = ""
    coupon_code = None
    try:
        from app.aliexpress.parser import extract_clean_title, extract_multi_coupons
        multi = extract_multi_coupons(raw_text)
        coupon_code = multi.get("coupon_code")
        coupons = multi.get("coupons", [])
        coupon_details = multi.get("coupon_details", [])
        clean_description = multi.get("description", "")
        t_found = extract_clean_title(raw_text)
        if t_found and len(t_found) >= 4:
            title = t_found
    except Exception:
        pass

    if not title:
        title = "AliExpress Deal"

    currency = "EUR" if "france" in clean_ch.lower() else "USD"
    price_val = None
    price_m = re.search(r'(?:السعر|Prix)\s*:\s*[\$€]?\s*([\d\.]+)', raw_text, re.IGNORECASE)
    if not price_m:
        price_m = re.search(r'[\$💰]\s*([\d\.]+)|([\d\.]+)\s*[\$€]', raw_text)
    if price_m:
        try:
            raw_val = price_m.group(1) or price_m.group(2)
            price_val = float(raw_val)
        except Exception:
            pass

    price_usd = price_val if currency == "USD" else (round(price_val * 1.08, 2) if price_val else None)
    price_eur = price_val if currency == "EUR" else (round(price_val * 0.92, 2) if price_val else None)
    price_dzd = None
    if price_usd:
        price_dzd = int(round(price_usd * usdt_rate, -1))
    elif price_eur:
        price_dzd = int(round(price_eur * usdt_rate * 1.09, -1))

    # Fallback single coupon regex if not already found
    if not coupon_code:
        c_m = re.search(r'(?:كـ?وبون|Code promo|Coupon)[^\n:]*[:\s]+([A-Za-z0-9_-]{4,15})', raw_text, re.IGNORECASE)
        if c_m:
            coupon_code = c_m.group(1).strip()
            if coupon_code not in coupons:
                coupons.append(coupon_code)
                coupon_details.append({"code": coupon_code, "tier": "", "label": "كود الخصم"})

    country = None
    clean_country_text = re.sub(r'[\u0640]', '', raw_text)
    low_c = clean_country_text.lower()
    if any(k in low_c for k in ["سعودية", "السعودية", "🇸🇦", "saudi", "ksa", "sar"]):
        country = "السعودية 🇸🇦"
    elif any(k in low_c for k in ["إمارات", "الامارات", "الإمارات", "🇦🇪", "uae", "emirates", "aed"]):
        country = "الإمارات 🇦🇪"
    elif any(k in low_c for k in ["قطر", "🇶🇦", "qatar", "qar"]):
        country = "قطر 🇶🇦"
    elif any(k in low_c for k in ["كويت", "الكويت", "🇰🇼", "kuwait", "kwd"]):
        country = "الكويت 🇰🇼"
    elif any(k in low_c for k in ["بحرين", "البحرين", "🇧🇭", "bahrain", "bhd"]):
        country = "البحرين 🇧🇭"
    elif any(k in low_c for k in ["عمان", "عُمان", "🇴🇲", "oman", "omr"]):
        country = "عمان 🇴🇲"
    elif any(k in low_c for k in ["كندا", "🇨🇦", "canada"]):
        country = "كندا 🇨🇦"
    elif any(k in low_c for k in ["كوريا", "🇰🇷", "korea"]):
        country = "كوريا 🇰🇷"
    elif any(k in low_c for k in ["الجزائر", "🇩🇿", "algeria"]):
        country = "الجزائر 🇩🇿"
    elif any(k in low_c for k in ["فرنسا", "🇫🇷", "france"]):
        country = "فرنسا 🇫🇷"
    elif any(k in low_c for k in ["أوكرانيا", "اوكرانيا", "🇺🇦", "ukraine"]):
        country = "أوكرانيا 🇺🇦"
    elif any(k in low_c for k in ["استراليا", "أستراليا", "🇦🇺", "australia"]):
        country = "أستراليا 🇦🇺"
    elif any(k in low_c for k in ["إسبانيا", "اسبانيا", "🇪🇸", "spain"]):
        country = "إسبانيا 🇪🇸"
    elif any(k in low_c for k in ["خلي البلد", "بلد الحساب", "ضع البلد"]):
        country = "كندا 🇨🇦"

    has_coins = any(k in raw_text for k in ["عملات", "نقاط", "pièces", "coins", "Alilo07BOT", "🪙"])

    comb = f"{title} {raw_text}".lower()
    if is_tajmi3at:
        cat = "tajmi3at"
        cat_lbl = "تجميعة عروض 📦"
    elif any(k in comb for k in ["phone", "smartphone", "poco", "redmi", "realme", "xiaomi", "honor", "samsung", "infinix", "oppo", "vivo", "iphone", "blackview", "cubot", "oukitel", "doogee", "tecno", "itel", "oneplus", "nubia", "zte", "motorola", "iqoo", "pad", "tablet", "هاتف", "تابلت", "لوحي"]):
        cat = "smartphones"
        cat_lbl = "هواتف ذكية 📱"
    elif any(k in comb for k in ["mouse", "mice", "keyboard", "controller", "gamepad", "gaming", "attack shark", "ajazz", "aula", "vgn", "scyrox", "zaopin", "machenike", "gamesir", "darmoshark", "fantech", "ماوس", "كيبورد", "فارة", "قيمنق", "تحكم", "يد تحكم"]):
        cat = "gaming"
        cat_lbl = "قيمنق وإلكترونيات 🎮"
    elif any(k in comb for k in ["earbuds", "earbud", "earphone", "earphones", "headphone", "headphones", "headset", "tws", "audio", "soundcore", "qcy", "haylou", "edifier", "lenovo lp", "lenovo xt", "moondrop", "iem", "سماعات", "سماعة", "صوتيات", "ايربودز"]):
        cat = "audio"
        cat_lbl = "سماعات وصوتيات 🎧"
    elif any(k in comb for k in ["charger", "gan", "cable", "ssd", "nvme", "powerbank", "watch", "smartwatch", "wifi", "router", "repeater", "adapter", "stand", "laser", "shaver", "trimmer", "anker", "ugreen", "baseus", "toocki", "rocoren", "essager", "cusu", "walram", "شاحن", "كابل", "ساعة", "تخزين", "حلاقة", "بطارية"]):
        cat = "tech"
        cat_lbl = "شواحن وملحقات ⚡"
    else:
        cat = "other"
        cat_lbl = "عروض منوعة 🏷️"

    return {
        "id": data_post or f"deal_{msg_id}",
        "msg_id": msg_id,
        "title": title,
        "price_usd": price_usd,
        "price_eur": price_eur,
        "price_dzd": price_dzd,
        "currency": currency,
        "coupon_code": coupon_code,
        "coupon": coupon_code,
        "coupons": coupons,
        "coupon_details": coupon_details,
        "description": clean_description,
        "country": country,
        "has_coins": has_coins,
        "affiliate_url": affiliate_url,
        "telegram_url": telegram_url,
        "photo_url": photo_url,
        "category": cat,
        "category_label": cat_lbl,
        "date": date_str,
        "is_tajmi3at": is_tajmi3at,
        "raw_text": raw_text
    }


@app.get("/api/deals")
async def get_deals(channel: str = "@DzAliexpress0", force: bool = False):
    """
    Returns real-time structured AliExpress deals from Telegram channel with live DZD pricing.
    """
    clean_ch = channel.replace("@", "").strip() or "DzAliexpress0"
    now_ts = datetime.now(timezone.utc).timestamp()

    # Get live USDT rate
    try:
        from api.coin_bot import get_live_usdt_rate
        usdt_rate = await get_live_usdt_rate()
    except Exception:
        usdt_rate = 249.0

    # 1. Check in-memory cache (60s TTL)
    if not force and clean_ch in _DEALS_CACHE:
        cache_ts, cached_deals = _DEALS_CACHE[clean_ch]
        if now_ts - cache_ts < 60:
            return {
                "deals": cached_deals,
                "count": len(cached_deals),
                "usdt_rate": usdt_rate,
                "channel": f"@{clean_ch}"
            }

    # 2. Fetch Telegram public preview
    deals = []
    try:
        async with httpx.AsyncClient(timeout=12.0, follow_redirects=True) as client:
            resp = await client.get(
                f"https://t.me/s/{clean_ch}",
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            )
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            blocks = soup.find_all("div", class_="tgme_widget_message")
            for block in reversed(blocks):
                parsed = parse_telegram_deal_block(block, clean_ch, usdt_rate)
                if parsed:
                    deals.append(parsed)
    except Exception as e:
        pass

    # 3. Fallback to local SQLite database if telegram preview fails
    if not deals:
        try:
            import sqlite3
            from pathlib import Path
            db_path = Path(__file__).resolve().parent.parent / "deals.db"
            if db_path.exists():
                conn = sqlite3.connect(str(db_path))
                c = conn.cursor()
                c.execute("SELECT product_id, title, current_price, current_price_eur, coupon_code, has_points_discount, affiliate_url, image_url, created_at FROM deals ORDER BY id DESC LIMIT 20")
                for row in c.fetchall():
                    pid, title, p_usd, p_eur, coupon, coins, aff_link, img_url, dt = row
                    p_dzd = int(round(p_usd * usdt_rate, -1)) if p_usd else None
                    deals.append({
                        "id": f"db_{pid}",
                        "msg_id": str(pid),
                        "title": title or "AliExpress Deal",
                        "price_usd": p_usd,
                        "price_eur": p_eur,
                        "price_dzd": p_dzd,
                        "currency": "USD",
                        "coupon_code": coupon,
                        "coupon": coupon,
                        "coupons": [coupon] if coupon else [],
                        "coupon_details": [{"code": coupon, "tier": "", "label": "كود الخصم"}] if coupon else [],
                        "description": title or "",
                        "country": "الجزائر 🇩🇿",
                        "has_coins": bool(coins),
                        "affiliate_url": aff_link or "https://t.me/DzAliexpress0",
                        "telegram_url": "https://t.me/DzAliexpress0",
                        "photo_url": img_url,
                        "category": "smartphones" if any(k in (title or '').lower() for k in ['poco', 'redmi', 'realme', 'phone']) else "tech",
                        "category_label": "صفقة مختارة 🔥",
                        "date": str(dt)[:16] if dt else "",
                        "is_tajmi3at": False,
                        "raw_text": title or ""
                    })
                conn.close()
        except Exception:
            pass

    if deals:
        _DEALS_CACHE[clean_ch] = (now_ts, deals)

    return {
        "deals": deals,
        "count": len(deals),
        "usdt_rate": usdt_rate,
        "channel": f"@{clean_ch}"
    }


@app.get("/manifest.json")
async def manifest():
    """Web App Manifest for PWA installation."""
    return Response(content=MANIFEST_JSON, media_type="application/manifest+json")


@app.get("/sw.js")
async def service_worker():
    """Service Worker for offline support and PWA caching."""
    return Response(content=SW_JS, media_type="application/javascript")


@app.get("/icon.svg")
async def app_icon():
    """Vector PWA application icon."""
    return Response(content=ICON_SVG, media_type="image/svg+xml")


@app.get("/logo.png")
async def get_logo():
    """Official DealScout Brand Logo."""
    logo_path = Path(__file__).resolve().parent.parent / "assets" / "logo.png"
    if logo_path.exists():
        return FileResponse(logo_path, media_type="image/png", headers={"Cache-Control": "public, max-age=604800"})
    return Response(status_code=404)


@app.get("/logo_circular.png")
async def get_logo_circular():
    """Official DealScout Circular Brand Logo."""
    logo_path = Path(__file__).resolve().parent.parent / "assets" / "logo_circular.png"
    if logo_path.exists():
        return FileResponse(logo_path, media_type="image/png", headers={"Cache-Control": "public, max-age=604800"})
    return Response(status_code=404)


@app.get("/api/rates")
async def live_rates():
    """Returns live USDT rate from SquareAlgerie.com."""
    from api.coin_bot import get_live_usdt_rate
    rate = await get_live_usdt_rate()
    return {"rate": rate, "currency": "USDT", "source": "SquareAlgerie.com"}


@app.get("/api/stats")
async def get_dashboard_stats():
    """Returns real-time ecosystem stats (watchlist items, schedule, rates)."""
    try:
        from app.publisher.watchlist import get_total_watchlist_count
        from app.publisher.state_tracker import get_schedule_config
        from api.coin_bot import get_live_usdt_rate

        rate = await get_live_usdt_rate()
        wl_count = get_total_watchlist_count()
        cfg = get_schedule_config()

        return {
            "ok": True,
            "usdt_rate": rate,
            "watchlist_active_count": wl_count,
            "schedule": {
                "day_interval": cfg.get("day_interval_minutes", 40),
                "night_interval": cfg.get("night_interval_minutes", 0),
                "is_paused": cfg.get("is_paused", False)
            }
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


@app.get("/api/schedule")
async def get_schedule():
    """Returns current automated posting schedule configuration."""
    try:
        from app.publisher.state_tracker import get_schedule_config
        config = get_schedule_config()
        now_utc = datetime.now(timezone.utc)
        algeria_hour = (now_utc.hour + 1) % 24
        is_night = (algeria_hour >= config.get("night_start_hour_dz", 0) and algeria_hour < config.get("night_end_hour_dz", 8))
        return {
            "ok": True,
            "config": config,
            "is_night": is_night,
            "algeria_hour": algeria_hour
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


@app.post("/api/schedule")
async def update_schedule(request: Request):
    """Updates automated posting schedule configuration."""
    if not is_admin_authenticated(request):
        return JSONResponse({"ok": False, "error": "غير مصرح: يرجى تسجيل الدخول كأدمن أولاً"}, status_code=401)
    try:
        data = await request.json()
        from app.publisher.state_tracker import update_schedule_config
        updated = update_schedule_config(data)
        return {"ok": True, "config": updated}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@app.get("/api/scout")
async def scout_endpoint(url: str = Query(...)):
    """In-Dashboard Deal Scout resolver with full algorithm caption and verified /e/ links."""
    try:
        from api.coin_bot import resolve_any_ali_link, generate_coin_discount_response, get_live_usdt_rate, ensure_affiliate
        from app.aliexpress.parser import detect_deal_type, is_france_deal
        from app.aliexpress.affiliate import affiliate_service
        from app.ai.generator import caption_generator
        from app.ai.generator_fr import france_caption_generator
        from app.config.settings import settings

        pid = await resolve_any_ali_link(url)
        if not pid:
            return {"ok": False, "error": "لم يتم التعرف على كود المنتج"}

        res = await generate_coin_discount_response(pid, raw_user_text=url)
        rate = await get_live_usdt_rate()
        price = res.get("price") or 0.0
        eur_rate = float(getattr(settings, "EUR_USD_RATE", 0.92))
        eur_price = round(price * eur_rate, 2) if price else None
        dzd = int(price * rate) if price else None
        deal_type = detect_deal_type(url)

        # Official /e/ affiliate link
        target_product_url = f"https://www.aliexpress.com/item/{pid}.html"
        direct_aff_link = await affiliate_service.generate_affiliate_link(target_product_url, product_id=pid, deal_type="item")
        coin_aff_link = await affiliate_service.generate_affiliate_link(target_product_url, product_id=pid, deal_type="coin")
        preferred_link = coin_aff_link or res.get("coin_link") or direct_aff_link or res.get("product_link")

        # Caption generation (France or Algeria)
        is_fr = is_france_deal(url)
        if is_fr:
            caption = await france_caption_generator.generate(
                title=res.get("title") or "AliExpress Deal",
                usd_price=price,
                eur_price=eur_price,
                affiliate_url=preferred_link,
                has_points_discount=True,
                deal_type=deal_type,
                raw_text=url
            )
        else:
            caption = await caption_generator.generate(
                title=res.get("title") or "منتج مميز من AliExpress",
                usd_price=price,
                eur_price=eur_price,
                affiliate_url=preferred_link,
                has_points_discount=True,
                country_info="كوريا 🇰🇷",
                deal_type=deal_type,
                raw_text=url
            )

        return {
            "ok": True,
            "deal": {
                "product_id": pid,
                "title": res.get("title"),
                "price": price,
                "price_eur": eur_price,
                "price_dzd": dzd,
                "image_url": res.get("image_url"),
                "product_link": direct_aff_link or res.get("product_link"),
                "coin_link": coin_aff_link or res.get("coin_link"),
                "deal_link": preferred_link,
                "caption": caption
            }
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


@app.get("/api/resolve-coin-link")
async def resolve_coin_link_endpoint(url: str = Query(...)):
    """Resolves any AliExpress URL (including shortlinks like a.aliexpress.com or s.click) to product ID and generates coin deal links."""
    try:
        from api.coin_bot import resolve_any_ali_link, extract_pid_from_string
        from app.config.settings import settings

        tracking_id = getattr(settings, "ALIEXPRESS_AFFILIATE_TRACKING_ID", "dzkhvled16") or "dzkhvled16"
        pid = extract_pid_from_string(url)
        if not pid:
            pid = await resolve_any_ali_link(url)

        if not pid:
            return JSONResponse({"ok": False, "error": "لم يتم التعرف على كود المنتج"}, status_code=400)

        coin_link = f"https://www.aliexpress.com/item/{pid}.html?sourceType=620&channel=coin&aff_fcid={tracking_id}"
        super_link = f"https://www.aliexpress.com/item/{pid}.html?sourceType=561&channel=superdeal&aff_fcid={tracking_id}"
        bundle_link = f"https://www.aliexpress.com/ssr/300000512/BundleDeals2?disableNav=YES&pha_manifest=ssr&_immersiveMode=true&productIds={pid}&aff_fcid={tracking_id}"
        direct_link = f"https://www.aliexpress.com/item/{pid}.html?aff_fcid={tracking_id}"

        return {
            "ok": True,
            "product_id": pid,
            "coin_link": coin_link,
            "super_link": super_link,
            "bundle_link": bundle_link,
            "direct_link": direct_link
        }
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)}, status_code=500)


@app.post("/api/reformat-deal")
async def api_reformat_deal(request: Request):
    """Reformat raw Telegram deal post and prepare clean Algerian channel caption using the official algorithm."""
    if not is_admin_authenticated(request):
        return JSONResponse({"ok": False, "error": "غير مصرح: يرجى تسجيل الدخول كأدمن أولاً"}, status_code=401)
    try:
        data = await request.json()
        raw_text = (data.get("text") or "").strip()
        if not raw_text:
            return {"ok": False, "error": "يرجى لصق نص المنشور"}

        from api.coin_bot import resolve_any_ali_link, generate_coin_discount_response, get_live_usdt_rate, ensure_affiliate
        from app.aliexpress.parser import (
            extract_prices, extract_coupon, extract_seller_coupon,
            extract_country_instruction, detect_deal_type, detect_restock_deal,
            detect_price_drop_deal, is_france_deal,
            extract_clean_title, detect_points_discount, extract_multi_coupons
        )
        from app.aliexpress.affiliate import affiliate_service
        from app.ai.generator import caption_generator
        from app.ai.generator_fr import france_caption_generator
        from app.config.settings import settings

        pid = await resolve_any_ali_link(raw_text)
        if not pid:
            return {"ok": False, "error": "لم يتم العثور على رابط منتج AliExpress صالح في النص"}

        deal_info = await generate_coin_discount_response(pid, raw_user_text=raw_text)

        # 1. Price extraction with EUR support
        parsed_usd, parsed_eur = extract_prices(raw_text)
        price = parsed_usd or deal_info.get("price") or 0.0
        eur_rate = float(getattr(settings, "EUR_USD_RATE", 0.92))
        eur_price = parsed_eur or (round(price * eur_rate, 2) if price else 0.0)

        rate = await get_live_usdt_rate()
        dzd_price = int(price * rate) if price else 0

        title = extract_clean_title(raw_text) or deal_info.get("title") or "منتج مميز من AliExpress"
        multi = extract_multi_coupons(raw_text)
        coupon = multi.get("coupon_code")
        coupons = multi.get("coupons", [])
        coupon_details = multi.get("coupon_details", [])
        clean_description = multi.get("description", "")
        seller_coupon = extract_seller_coupon(raw_text)
        country = extract_country_instruction(raw_text, title=title)
        deal_type = detect_deal_type(raw_text)
        is_restock = detect_restock_deal(raw_text)
        is_price_drop = detect_price_drop_deal(raw_text)
        has_points = detect_points_discount(raw_text)

        # Detect if deal is specifically for France channel
        is_fr = is_france_deal(raw_text, country_info=country)
        target_channel = "@francedealsdz" if is_fr else "@DzAliexpress0"

        # 2. Official /e/ affiliate link generation
        target_product_url = f"https://www.aliexpress.com/item/{pid}.html"
        deal_link = await affiliate_service.generate_affiliate_link(
            target_product_url,
            product_id=pid,
            deal_type=deal_type
        )
        if not deal_link or "aliexpress.com" not in deal_link:
            preferred = deal_info.get("bundle_link") if deal_type == "bundle" else (deal_info.get("coin_link") or deal_info.get("product_link"))
            deal_link = ensure_affiliate(preferred, fallback_link=deal_info.get("product_link"), pid=pid)

        # 3. Caption generation using target channel generator
        if is_fr:
            caption = await france_caption_generator.generate(
                title=title,
                usd_price=price,
                eur_price=eur_price,
                affiliate_url=deal_link,
                coupon_code=coupon,
                seller_coupon=seller_coupon,
                has_points_discount=has_points,
                is_price_drop=is_price_drop,
                is_restock=is_restock,
                deal_type=deal_type,
                country_info=country,
                raw_text=raw_text
            )
        else:
            caption = await caption_generator.generate(
                title=title,
                usd_price=price,
                eur_price=eur_price,
                affiliate_url=deal_link,
                coupon_code=coupon,
                seller_coupon=seller_coupon,
                has_points_discount=has_points,
                country_info=country,
                is_price_drop=is_price_drop,
                is_restock=is_restock,
                deal_type=deal_type,
                raw_text=raw_text
            )

        images = deal_info.get("images", [])
        main_img = deal_info.get("image_url")
        if main_img and main_img not in images:
            images.insert(0, main_img)

        return {
            "ok": True,
            "product_id": pid,
            "title": title,
            "price": price,
            "price_eur": eur_price,
            "price_dzd": dzd_price,
            "coupon": coupon,
            "coupon_code": coupon,
            "coupons": coupons,
            "coupon_details": coupon_details,
            "description": clean_description,
            "seller_coupon": seller_coupon,
            "deal_type": deal_type,
            "country": country,
            "is_france": is_fr,
            "target_channel": target_channel,
            "is_price_drop": is_price_drop,
            "is_restock": is_restock,
            "image_url": main_img,
            "images": images[:8],
            "deal_link": deal_link,
            "caption": caption
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


@app.post("/api/publish-deal")
async def api_publish_deal(request: Request):
    """Publish reformatted deal post directly to target channel (@DzAliexpress0 or @francedealsdz)."""
    if not is_admin_authenticated(request):
        return JSONResponse({"ok": False, "error": "غير مصرح: يرجى تسجيل الدخول كأدمن أولاً"}, status_code=401)
    try:
        data = await request.json()
        caption = (data.get("caption") or "").strip()
        image_url = (data.get("image_url") or "").strip() or None
        deal_link = (data.get("deal_link") or "").strip()
        product_id = data.get("product_id", "")
        price = data.get("price")
        target_ch = (data.get("target_channel") or "").strip()

        if not caption:
            return {"ok": False, "error": "نص المنشور فارغ"}

        # Target channel auto-detection if not explicitly passed
        if not target_ch:
            if "@francedealsdz" in caption or "Livraison : France" in caption or "Livraison en France" in caption or "Livré en France" in caption:
                target_ch = "@francedealsdz"
            else:
                target_ch = os.getenv("TARGET_CHANNEL_ID", "@DzAliexpress0")

        is_france = (target_ch == "@francedealsdz")
        target_clean = str(target_ch).lstrip("@")

        import os
        from api.coin_bot import TELEGRAM_BOT_TOKEN, ADMIN_BOT_TOKEN, ensure_affiliate

        token = os.getenv("TELEGRAM_BOT_TOKEN", "") or TELEGRAM_BOT_TOKEN or ADMIN_BOT_TOKEN
        if not token:
            return {"ok": False, "error": "توكن البوت غير مهيأ"}

        tracked_deal_link = ensure_affiliate(deal_link, pid=product_id)

        if is_france:
            channel_reply_markup = {
                "inline_keyboard": [
                    [
                        {"text": "🛒 Voir le bon plan sur AliExpress ➔", "url": tracked_deal_link or "https://s.click.aliexpress.com/e/_oEN3d53"}
                    ],
                    [
                        {"text": "🪙 Bot Pièces AliExpress (Coins)", "url": "https://t.me/Alilo07BOT"}
                    ]
                ]
            }
        else:
            channel_reply_markup = {
                "inline_keyboard": [
                    [
                        {"text": "🪙 فتح بوت تخفيض العملات", "url": "https://t.me/Alilo07BOT"}
                    ],
                    [
                        {"text": "📢 قناة الصفقات المعتمدة", "url": f"https://t.me/{target_clean}"}
                    ]
                ]
            }

        api_url = f"https://api.telegram.org/bot{token}"
        async with httpx.AsyncClient(timeout=15.0) as client:
            if image_url:
                resp = await client.post(
                    f"{api_url}/sendPhoto",
                    json={
                        "chat_id": target_ch,
                        "photo": image_url,
                        "caption": caption[:1024],
                        "parse_mode": "HTML",
                        "reply_markup": channel_reply_markup
                    }
                )
            else:
                resp = await client.post(
                    f"{api_url}/sendMessage",
                    json={
                        "chat_id": target_ch,
                        "text": caption,
                        "parse_mode": "HTML",
                        "reply_markup": channel_reply_markup
                    }
                )

            res = resp.json()
            if resp.status_code == 200 and res.get("ok"):
                msg_id = res["result"]["message_id"]
                clean_title = caption.splitlines()[0] if caption else ""

                if is_france:
                    try:
                        from scripts.post_france_deals import load_france_state, record_france_deal_published
                        f_state = load_france_state()
                        record_france_deal_published(
                            state=f_state,
                            product_id=str(product_id) if product_id else None,
                            title=clean_title,
                            price_eur=price,
                            channel_msg_id=msg_id
                        )
                    except Exception:
                        pass
                else:
                    try:
                        from app.publisher.state_tracker import record_post_published
                        record_post_published(
                            channel_username="dashboard_admin",
                            message_id=msg_id,
                            product_id=str(product_id) if product_id else None,
                            title=clean_title,
                            channel_msg_id=msg_id,
                            price=price
                        )
                    except Exception:
                        pass

                return {
                    "ok": True,
                    "message_id": msg_id,
                    "channel": target_ch,
                    "post_url": f"https://t.me/{target_clean}/{msg_id}"
                }
            else:
                return {"ok": False, "error": res.get("description", f"Telegram API error {resp.status_code}")}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "service": "DealScout DZ Dashboard",
        "channel": "@DzAliexpress0",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.get("/api/active-event")
async def get_active_event_api():
    """Returns the currently active official AliExpress promo event with active coupons and keywords."""
    from app.aliexpress.promos import promo_tracker
    now = datetime.now(timezone.utc)
    ev = promo_tracker.get_active_promo(now)
    if not ev:
        return {"active": False, "event": None}
    event_data = {
        "name": ev.name,
        "name_ar": ev.name_ar,
        "name_fr": ev.name_fr or ev.name,
        "banner_tag": ev.banner_tag,
        "start_date": ev.start_date.isoformat(),
        "end_date": ev.end_date.isoformat(),
        "coupon_tiers": ev.coupon_tiers or [],
        "coupon_tiers_fr": ev.coupon_tiers_fr or [],
        "codes": [t["code"] for t in (ev.coupon_tiers or []) if "code" in t]
    }
    return {
        "active": True,
        "event": event_data,
        "active_event": event_data
    }


_CHANNEL_POSTS_CACHE: Dict[str, Any] = {}


@app.get("/api/channel-posts")
async def channel_posts(channel: str = "@DzAliexpress0", force: bool = False):
    """Fetch recent posts from @DzAliexpress0 or @francedealsdz with server-side caching & fallback."""
    clean_ch = channel.replace("@", "").strip() or "DzAliexpress0"
    now_ts = time.time()

    # Get active promo event details
    active_ev_data = None
    try:
        from app.aliexpress.promos import promo_tracker
        now_dt = datetime.now(timezone.utc)
        ev = promo_tracker.get_active_promo(now_dt)
        if ev:
            active_ev_data = {
                "name": ev.name,
                "name_ar": ev.name_ar,
                "name_fr": ev.name_fr or ev.name,
                "banner_tag": ev.banner_tag,
                "start_date": ev.start_date.isoformat(),
                "end_date": ev.end_date.isoformat(),
                "coupon_tiers": ev.coupon_tiers or [],
                "coupon_tiers_fr": ev.coupon_tiers_fr or [],
                "codes": [t["code"] for t in (ev.coupon_tiers or []) if "code" in t],
                "status": "active"
            }
        else:
            all_promos = promo_tracker.get_all_promos(now_dt)
            past_promos = [p for p in all_promos if p.end_date <= now_dt]
            if past_promos:
                past_promos.sort(key=lambda p: p.end_date, reverse=True)
                last_p = past_promos[0]
                active_ev_data = {
                    "name": last_p.name,
                    "name_ar": last_p.name_ar,
                    "name_fr": last_p.name_fr or last_p.name,
                    "banner_tag": last_p.banner_tag,
                    "start_date": last_p.start_date.isoformat(),
                    "end_date": last_p.end_date.isoformat(),
                    "coupon_tiers": last_p.coupon_tiers or [],
                    "coupon_tiers_fr": last_p.coupon_tiers_fr or [],
                    "codes": [t["code"] for t in (last_p.coupon_tiers or []) if "code" in t],
                    "status": "ended"
                }
    except Exception:
        pass

    # 1. Return fresh cached response if available (60s TTL) and not forced
    if not force and clean_ch in _CHANNEL_POSTS_CACHE:
        cache_ts, cached_posts = _CHANNEL_POSTS_CACHE[clean_ch]
        if now_ts - cache_ts < 60 and cached_posts:
            return JSONResponse(
                {"posts": cached_posts, "count": len(cached_posts), "cached": True, "active_event": active_ev_data},
                headers={"Cache-Control": "public, max-age=60"}
            )

    # 2. Fetch from Telegram public web preview (with pagination to guarantee 25-30 deals)
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        all_blocks = []
        before = None
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            for _ in range(3):
                url = f"https://t.me/s/{clean_ch}" + (f"?before={before}" if before else "")
                resp = await client.get(url, headers=headers)
                if resp.status_code != 200:
                    break
                soup = BeautifulSoup(resp.text, "html.parser")
                blocks = soup.find_all("div", class_="tgme_widget_message")
                if not blocks:
                    break
                all_blocks = blocks + all_blocks
                more_btn = soup.find("a", class_=re.compile(r"js-messages_more"))
                if more_btn and more_btn.get("data-before"):
                    before = more_btn["data-before"]
                else:
                    break
                if len(all_blocks) >= 50:
                    break

        if all_blocks:
            posts = []
            for block in reversed(all_blocks):
                text_div = block.find("div", class_="tgme_widget_message_text")
                if text_div:
                    from app.aliexpress.parser import extract_telegram_html_text
                    text = extract_telegram_html_text(text_div)
                else:
                    text = ""

                if not text:
                    continue

                # Filter out expired month campaigns if any
                if any(m in text.lower() for m in ["سبتمبر", "september"]):
                    continue

                # Deal must contain an AliExpress link
                has_ali_link = bool(re.search(r"https?://(?:s\.click\.aliexpress\.com/e/[A-Za-z0-9_-]+|(?:[a-z0-9-]+\.)?aliexpress\.com/(?:item|p)/[A-Za-z0-9_.-]+)", text, re.I))
                if not has_ali_link:
                    continue

                # Filter out religious adhkars
                if any(r in text for r in ["وَتَوَكَّلْ", "وتوكل", "سبحان الله", "الحمد لله", "الله أكبر", "صلى الله", "عليه وسلم", "سورة", "القرآن", "أذكار", "دعاء", "استغفر الله", "لا إله إلا الله"]):
                    continue

                photo_url = None
                photo_wrap = (
                    block.find("a", class_="tgme_widget_message_photo_wrap")
                    or block.find(class_=re.compile(r"tgme_widget_message_photo_wrap"))
                    or block.find("i", class_=re.compile(r"link_preview_image|link_preview_right_image"))
                    or block.find("i", class_=re.compile(r"tgme_widget_message_video_thumb"))
                )
                if photo_wrap and photo_wrap.get("style"):
                    m = re.search(r"url\(['\"]?([^'\")]+)['\"]?\)", photo_wrap["style"])
                    if m:
                        photo_url = m.group(1)
                elif block.find("img") and block.find("img").get("src"):
                    photo_url = block.find("img")["src"]

                date_str = ""
                date_el = block.find("time")
                if date_el and date_el.get("datetime"):
                    try:
                        dt = datetime.fromisoformat(date_el["datetime"].replace("Z", "+00:00"))
                        date_str = dt.strftime("%Y-%m-%d %H:%M")
                    except Exception:
                        date_str = date_el.get("datetime", "")

                data_post = block.get("data-post", "")
                link = f"https://t.me/{data_post}" if data_post else ""

                try:
                    from app.aliexpress.parser import extract_multi_coupons, extract_clean_title
                    multi = extract_multi_coupons(text)
                    clean_desc = multi.get("description", "")
                    c_list = multi.get("coupons", [])
                    c_details = multi.get("coupon_details", [])
                    c_primary = multi.get("coupon_code")
                    extracted_title = extract_clean_title(text) or ""
                except Exception:
                    clean_desc = ""
                    c_list = []
                    c_details = []
                    c_primary = None
                    extracted_title = ""

                posts.append({
                    "text": text,
                    "title": extracted_title,
                    "description": clean_desc,
                    "coupons": c_list,
                    "coupon_details": c_details,
                    "coupon_code": c_primary,
                    "coupon": c_primary,
                    "photo_url": photo_url,
                    "date": date_str,
                    "link": link
                })

                if len(posts) >= 30:
                    break

            if posts:
                _CHANNEL_POSTS_CACHE[clean_ch] = (now_ts, posts)
                return JSONResponse(
                    {"posts": posts, "count": len(posts), "cached": False, "active_event": active_ev_data},
                    headers={"Cache-Control": "public, max-age=60"}
                )
    except Exception:
        pass

    # 3. Graceful Fallback: If Telegram failed or timed out, serve cached posts even if older!
    if clean_ch in _CHANNEL_POSTS_CACHE:
        cache_ts, cached_posts = _CHANNEL_POSTS_CACHE[clean_ch]
        if cached_posts:
            return JSONResponse(
                {"posts": cached_posts, "count": len(cached_posts), "cached": True, "stale": True, "active_event": active_ev_data},
                headers={"Cache-Control": "public, max-age=30"}
            )

    return JSONResponse(
        {"error": "Temporary connection timeout to Telegram channel", "posts": [], "cached": False},
        status_code=503
    )


@app.get("/api/image-proxy")
async def image_proxy(url: str = Query(...)):
    """Proxies Telegram and CDN images to prevent client hotlink blocking and CORS issues."""
    allowed = any(domain in url for domain in ["telesco.pe", "telegram.org", "aliexpress.com", "alicdn.com", "t.me"])
    if not allowed or not url.startswith("https://"):
        return JSONResponse({"error": "Forbidden image host"}, status_code=403)
    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            resp = await client.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
            if resp.status_code == 200:
                media_type = resp.headers.get("content-type", "image/jpeg")
                return Response(
                    content=resp.content,
                    media_type=media_type,
                    headers={"Cache-Control": "public, max-age=86400"}
                )
            return Response(status_code=resp.status_code)
    except Exception:
        return Response(status_code=502)


# ── Telegram Webhook Handlers ────────────────────────────────────
@app.post("/api/webhook")
async def telegram_webhook(request: Request):
    """Serverless Telegram Coin & Discount Bot webhook (@Alilo07BOT)."""
    try:
        update = await request.json()
        from api.coin_bot import handle_update
        await handle_update(update)
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@app.post("/api/admin-webhook")
async def telegram_admin_webhook(request: Request):
    """Serverless Telegram Admin Scout & Publisher Bot webhook (@DealscoutadminBOT)."""
    try:
        update = await request.json()
        from api.admin_bot import handle_admin_update
        await handle_admin_update(update)
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@app.get("/api/set-webhook")
async def set_telegram_webhook(request: Request):
    """Sets the public Coin bot webhook to this Vercel deployment URL."""
    try:
        from api.coin_bot import TELEGRAM_BOT_TOKEN as _C_TOKEN
        token = os.getenv("TELEGRAM_BOT_TOKEN", "") or _C_TOKEN
        base_url = os.getenv("PUBLIC_BASE_URL", "").strip().rstrip("/")
        if not base_url:
            host = request.headers.get("x-forwarded-host") or request.headers.get("host") or ""
            proto = request.headers.get("x-forwarded-proto") or "https"
            base_url = f"{proto}://{host}" if host else "https://dealscoutgreen.vercel.app"
        webhook_url = f"{base_url}/api/webhook"
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"https://api.telegram.org/bot{token}/setWebhook",
                json={"url": webhook_url, "drop_pending_updates": True}
            )
            return resp.json()
    except Exception as e:
        return {"ok": False, "error": str(e)}


@app.get("/api/set-admin-webhook")
async def set_admin_telegram_webhook(request: Request):
    """Sets the dedicated Admin bot webhook to this Vercel deployment URL."""
    try:
        from api.admin_bot import ADMIN_BOT_TOKEN as _A_TOKEN
        admin_token = os.getenv("ADMIN_BOT_TOKEN", "") or _A_TOKEN
        base_url = os.getenv("PUBLIC_BASE_URL", "").strip().rstrip("/")
        if not base_url:
            host = request.headers.get("x-forwarded-host") or request.headers.get("host") or ""
            proto = request.headers.get("x-forwarded-proto") or "https"
            base_url = f"{proto}://{host}" if host else "https://dealscoutgreen.vercel.app"
        webhook_url = f"{base_url}/api/admin-webhook"
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"https://api.telegram.org/bot{admin_token}/setWebhook",
                json={"url": webhook_url, "drop_pending_updates": True}
            )
            return resp.json()
    except Exception as e:
        return {"ok": False, "error": str(e)}


@app.get("/api/test-bot")
async def test_bot_connectivity():
    """Tests bot connectivity and returns bot profile from Telegram API."""
    from api.coin_bot import TELEGRAM_BOT_TOKEN as _C_TOKEN
    coin_token = (os.getenv("TELEGRAM_BOT_TOKEN", "") or _C_TOKEN).strip()
    if not coin_token:
        return {"ok": False, "error": "TELEGRAM_BOT_TOKEN is not configured on Vercel."}
    async with httpx.AsyncClient(timeout=10.0) as client:
        r1 = await client.get(f"https://api.telegram.org/bot{coin_token}/getMe")
        r2 = await client.get(f"https://api.telegram.org/bot{coin_token}/getWebhookInfo")
        return {"getMe": r1.json(), "webhook": r2.json()}


@app.api_route("/api/trigger-deals", methods=["GET", "POST"])
async def trigger_deals_collector(request: Request, force: bool = False):
    """
    Webhook endpoint to trigger GitHub Actions collector workflow.
    Can be called by external cron services (with ?key= or ?secret=) or authenticated admin.
    
    Smart Scheduling:
      - Daytime (07:00 - 01:00 UTC+1): Every 5 minutes
      - Nighttime (01:00 - 07:00 UTC+1): Throttled to every 30 minutes
    Pass ?force=true to bypass night mode throttling.
    """
    secret = get_admin_auth_secret()
    trigger_secret = os.getenv("TRIGGER_SECRET", "").strip() or secret
    req_secret = (
        request.query_params.get("secret")
        or request.query_params.get("key")
        or request.query_params.get("token")
        or request.headers.get("x-trigger-secret")
    )
    is_authed = is_admin_authenticated(request) or (
        trigger_secret and req_secret and hmac.compare_digest(req_secret, trigger_secret)
    )
    if not is_authed:
        return JSONResponse(
            {"ok": False, "error": "غير مصرح: يرجى تمرير مفتاح المصادقة الصحيح (?key= أو ?secret=)"},
            status_code=401
        )
    dz_tz = timezone(timedelta(hours=1))
    now_dz = datetime.now(dz_tz)
    hour = now_dz.hour
    minute = now_dz.minute

    # Night hours: 01:00 to 06:59 Algeria time (UTC+1)
    is_night = 1 <= hour < 7
    if is_night and not force:
        # In night mode, only trigger around :00 and :30 (window of first 5 mins)
        in_run_window = (0 <= minute < 5) or (30 <= minute < 35)
        if not in_run_window:
            next_min = "30" if minute < 30 else "00"
            next_hr = hour if minute < 30 else (hour + 1) % 24
            return {
                "ok": True,
                "status": "night_mode_skipped",
                "message": f"Night mode active (01:00-07:00 DZ time). Autonomous sweep throttled to every 30 mins to preserve resources.",
                "local_time": now_dz.strftime("%H:%M:%S UTC+1"),
                "next_run": f"{next_hr:02d}:{next_min} UTC+1"
            }

    github_token = os.getenv("GITHUB_TOKEN", "").strip()
    if not github_token:
        return {
            "ok": False,
            "error": "GITHUB_TOKEN is missing. Please add GITHUB_TOKEN to your Vercel project environment variables."
        }
    repo = "1khvled/ALIEXPRESS-CHANEL"
    url = f"https://api.github.com/repos/{repo}/actions/workflows/bot_cron.yml/dispatches"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "DealScout-Trigger"
    }
    payload = {
        "ref": "main",
        "inputs": {"force": "true" if force else "false"}
    }
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(url, headers=headers, json=payload)
            if resp.status_code == 204:
                return {
                    "ok": True,
                    "status": "dispatched",
                    "mode": "night_30m" if is_night else "day_5m",
                    "local_time": now_dz.strftime("%H:%M:%S UTC+1"),
                    "message": "AliExpress Deals workflow triggered successfully on GitHub Actions!"
                }
            return {
                "ok": False,
                "status_code": resp.status_code,
                "error": resp.text
            }
    except Exception as e:
        return {"ok": False, "error": str(e)}



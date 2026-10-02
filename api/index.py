"""
Vercel Serverless Entry Point — DealScout Modern PWA Dashboard
Features:
- Progressive Web App (PWA) installable on Android, iOS, Windows, and Mac
- Mobile-first responsive glassmorphic UI with bottom navigation
- Live SquareAlgerie.com USDT exchange rate integration
- In-Dashboard Instant AliExpress Deal Scout tool
- Channel post monitor with photos and direct affiliate links
"""
import re
from datetime import datetime, timezone
from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse, Response
import httpx
from bs4 import BeautifulSoup

app = FastAPI(title="DealScout DZ Dashboard", version="2.0.0")

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
DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="ar" dir="rtl" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>DealScout DZ — صفقات علي اكسبرس وتخفيضات العملات</title>
  
  <!-- PWA Metadata -->
  <link rel="manifest" href="/manifest.json">
  <link rel="icon" type="image/svg+xml" href="/icon.svg">
  <link rel="apple-touch-icon" href="/icon.svg">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="DealScout">
  <meta name="theme-color" content="#e11d48">
  <meta name="mobile-web-app-capable" content="yes">

  <!-- Tailwind & Icons -->
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">

  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            tajawal: ['Tajawal', 'sans-serif'],
            inter: ['Inter', 'sans-serif']
          }
        }
      }
    }
  </script>

  <style>
    body {
      font-family: 'Tajawal', sans-serif;
      background-color: #030712;
      color: #f1f5f9;
      -webkit-tap-highlight-color: transparent;
    }
    .glass-panel {
      background: rgba(15, 23, 42, 0.75);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .glass-glow {
      box-shadow: 0 0 25px -5px rgba(225, 29, 72, 0.15);
    }
    .card-hover {
      transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .card-hover:hover {
      transform: translateY(-2px);
      border-color: rgba(244, 63, 94, 0.3);
      box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5);
    }
    .pb-safe {
      padding-bottom: calc(5rem + env(safe-area-inset-bottom, 0px));
    }
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: #030712; }
    ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
  </style>
</head>
<body class="min-h-screen bg-slate-950 text-slate-100 flex flex-col justify-between selection:bg-rose-500 selection:text-white">

  <!-- Ambient Glow Background -->
  <div class="fixed top-0 left-1/2 -translate-x-1/2 w-full max-w-7xl h-96 bg-gradient-to-b from-rose-600/10 via-amber-500/5 to-transparent blur-3xl pointer-events-none -z-10"></div>

  <!-- Header -->
  <header class="glass-panel sticky top-0 z-40 border-b border-slate-800/80 px-4 py-3">
    <div class="max-w-7xl mx-auto flex items-center justify-between">
      <div class="flex items-center space-x-3 space-x-reverse">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-rose-600 via-rose-500 to-amber-500 flex items-center justify-center font-bold text-white shadow-lg shadow-rose-500/30">
          <i class="fa-solid fa-bolt text-lg"></i>
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="font-extrabold text-lg text-white font-inter tracking-tight">DealScout<span class="text-rose-500">DZ</span></h1>
            <span class="bg-rose-500/10 text-rose-400 text-[10px] font-bold px-2 py-0.5 rounded-full border border-rose-500/20">LIVE</span>
          </div>
          <p class="text-[11px] text-slate-400">@DzAliexpress0 • تتبع الصفقات والعملات</p>
        </div>
      </div>

      <!-- Action buttons -->
      <div class="flex items-center space-x-2 space-x-reverse">
        <!-- Live USDT Badge -->
        <a href="https://squarealgerie.com" target="_blank" class="hidden md:flex items-center gap-1.5 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs px-3 py-1.5 rounded-xl hover:bg-emerald-500/20 transition">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>1 USDT ≈ <b id="header-usdt-rate">249.0</b> دج</span>
        </a>

        <!-- Install PWA Button (Hidden until prompt available) -->
        <button id="pwa-install-btn" class="hidden bg-gradient-to-r from-rose-600 to-amber-600 hover:from-rose-500 hover:to-amber-500 text-white text-xs px-3.5 py-1.5 rounded-xl font-bold shadow-lg shadow-rose-600/25 flex items-center gap-1.5 transition active:scale-95">
          <i class="fa-solid fa-download"></i>
          <span>تثبيت التطبيق</span>
        </button>

        <!-- Refresh Button -->
        <button onclick="refreshDashboard()" id="refresh-btn" class="bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs px-3 py-1.5 rounded-xl border border-slate-700 flex items-center gap-1.5 transition active:scale-95">
          <i class="fa-solid fa-arrows-rotate" id="refresh-icon"></i>
          <span class="hidden sm:inline">تحديث</span>
        </button>
      </div>
    </div>
  </header>

  <!-- Main Container -->
  <main class="max-w-7xl mx-auto px-4 py-5 space-y-6 pb-safe w-full">

    <!-- Interactive Deal Scout Tool (Instant Link Inspector) -->
    <div class="glass-panel glass-glow rounded-2xl p-4 sm:p-5 border border-rose-500/20">
      <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 mb-3">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 rounded-lg bg-rose-500/10 flex items-center justify-center text-rose-400">
            <i class="fa-solid fa-magnifying-glass-dollar text-sm"></i>
          </div>
          <h2 class="text-sm sm:text-base font-bold text-white">فاحص ومحول روابط AliExpress الفوري 🔍</h2>
        </div>
        <span class="text-[11px] text-slate-400 bg-slate-800/80 px-2.5 py-1 rounded-lg">يدعم روابط التطبيق، المتصفح، أو رقم المنتج</span>
      </div>

      <div class="flex flex-col sm:flex-row gap-2">
        <input 
          type="text" 
          id="scout-url-input" 
          placeholder="ألصق أي رابط أو كود منتج من AliExpress هنا..." 
          dir="ltr"
          class="flex-1 bg-slate-900 border border-slate-700/80 rounded-xl px-4 py-2.5 text-xs sm:text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500"
        />
        <button 
          onclick="scoutDeal()" 
          id="scout-submit-btn" 
          class="bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs sm:text-sm px-5 py-2.5 rounded-xl shadow-lg shadow-rose-600/30 flex items-center justify-center gap-2 transition active:scale-95"
        >
          <i class="fa-solid fa-wand-magic-sparkles"></i>
          <span>فحص العرض</span>
        </button>
      </div>

      <!-- Scout Result Card -->
      <div id="scout-result" class="hidden mt-4 pt-4 border-t border-slate-800/80">
        <div class="bg-slate-900/90 rounded-xl p-4 border border-slate-800 flex flex-col md:flex-row items-start gap-4">
          <div id="scout-img-box" class="w-24 h-24 rounded-lg bg-slate-800 border border-slate-700 flex-shrink-0 overflow-hidden flex items-center justify-center">
            <i class="fa-solid fa-image text-slate-600 text-2xl"></i>
          </div>
          <div class="flex-1 min-w-0 space-y-2">
            <h4 id="scout-title" class="font-bold text-sm text-white line-clamp-2"></h4>
            <div class="flex flex-wrap items-center gap-3 text-xs">
              <span id="scout-price-usd" class="text-emerald-400 font-bold bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 rounded-md"></span>
              <span id="scout-price-dzd" class="text-amber-400 font-bold bg-amber-500/10 border border-amber-500/20 px-2 py-0.5 rounded-md"></span>
              <span id="scout-pid" class="text-slate-400 text-[11px]"></span>
            </div>
            <div class="flex flex-wrap gap-2 pt-1">
              <a id="scout-direct-link" href="#" target="_blank" class="bg-slate-800 hover:bg-slate-700 border border-slate-700 text-white text-xs px-3 py-1.5 rounded-lg flex items-center gap-1.5">
                <i class="fa-solid fa-cart-shopping text-rose-400"></i>
                <span>رابط الشراء المباشر</span>
              </a>
              <a id="scout-coin-link" href="#" target="_blank" class="bg-rose-600 hover:bg-rose-500 text-white text-xs px-3 py-1.5 rounded-lg flex items-center gap-1.5">
                <i class="fa-solid fa-coins text-amber-300"></i>
                <span>رابط تخفيض العملات</span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Telegram Post Reformatter & 1-Tap Publisher Tool -->
    <div class="glass-panel glass-glow rounded-3xl p-5 sm:p-6 mb-6 card-hover border border-rose-500/30">
      <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-4 pb-3 border-b border-slate-800/80">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-2xl bg-gradient-to-tr from-amber-500 to-rose-600 flex items-center justify-center text-white shadow-lg shadow-rose-600/30">
            <i class="fa-solid fa-wand-magic-sparkles text-lg"></i>
          </div>
          <div>
            <h3 class="font-bold text-base sm:text-lg text-white flex items-center gap-2">
              <span>إعادة تنسيق ونشر عروض التيليجرام ⚡</span>
              <span class="text-[10px] px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-300 border border-rose-500/30 font-bold">VIP للأدمن</span>
            </h3>
            <p class="text-xs text-slate-400">ألصق منشور أي قناة وسيقوم النظام فوراً باستخراج المنتج وتوليد الروابط التابعة وإعادة الصياغة باللهجة الجزائرية ثم النشر بضغطة زر!</p>
          </div>
        </div>
      </div>

      <div class="space-y-3">
        <textarea 
          id="reformat-input" 
          rows="4" 
          placeholder="ألصق هنا المنشور كما هو من قناة التيليجرام (يحتوي على رابط AliExpress، السعر، الكوبون...)" 
          dir="auto"
          class="w-full bg-slate-900 border border-slate-700/80 rounded-2xl p-3.5 text-xs sm:text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500 font-sans leading-relaxed"
        ></textarea>

        <div class="flex flex-wrap items-center justify-between gap-2">
          <button 
            onclick="reformatTelegramPost()" 
            id="reformat-submit-btn" 
            class="bg-gradient-to-r from-rose-600 to-amber-600 hover:from-rose-500 hover:to-amber-500 text-white font-bold text-xs sm:text-sm px-6 py-2.5 rounded-xl shadow-lg shadow-rose-600/30 flex items-center justify-center gap-2 transition active:scale-95"
          >
            <i class="fa-solid fa-arrows-rotate"></i>
            <span>إعادة التنسيق والمعاينة</span>
          </button>
          <button 
            onclick="document.getElementById('reformat-input').value=''; document.getElementById('reformat-result').classList.add('hidden');" 
            class="text-xs text-slate-400 hover:text-slate-200 px-3 py-1.5 rounded-lg border border-slate-800 hover:bg-slate-800 transition"
          >
            مسح الحقل
          </button>
        </div>
      </div>

      <!-- Reformatted Result Card -->
      <div id="reformat-result" class="hidden mt-5 pt-5 border-t border-slate-800/80 space-y-4">
        <div class="bg-slate-950/80 rounded-2xl p-4 border border-slate-800 flex flex-col md:flex-row items-start gap-4">
          <!-- Image Box & Selectors -->
          <div class="flex flex-col items-center gap-2 w-full md:w-auto">
            <div id="reformat-img-box" class="w-32 h-32 rounded-xl bg-slate-900 border border-slate-700 overflow-hidden flex items-center justify-center flex-shrink-0">
              <i class="fa-solid fa-image text-slate-600 text-3xl"></i>
            </div>
            <div id="reformat-gallery" class="flex flex-wrap gap-1 max-w-[140px] justify-center"></div>
          </div>

          <!-- Content Details & Editable Caption -->
          <div class="flex-1 min-w-0 w-full space-y-3">
            <div class="flex flex-wrap items-center justify-between gap-2">
              <span id="reformat-pid" class="text-xs font-mono bg-slate-800 text-slate-300 px-2.5 py-0.5 rounded-md border border-slate-700"></span>
              <div class="flex items-center gap-2">
                <span id="reformat-price-usd" class="text-emerald-400 font-bold bg-emerald-500/10 border border-emerald-500/20 px-2.5 py-0.5 rounded-md text-xs"></span>
                <span id="reformat-price-dzd" class="text-amber-400 font-bold bg-amber-500/10 border border-amber-500/20 px-2.5 py-0.5 rounded-md text-xs"></span>
              </div>
            </div>

            <!-- Editable Caption Box -->
            <div>
              <div class="flex items-center justify-between mb-1">
                <label class="text-[11px] font-bold text-slate-300">نص المنشور الجزائري المنسق (يمكنك التعديل عليه قبل النشر):</label>
                <span class="text-[10px] text-slate-500 font-mono" id="reformat-char-count"></span>
              </div>
              <textarea 
                id="reformat-caption" 
                rows="8" 
                dir="rtl"
                class="w-full bg-slate-900 border border-slate-800 rounded-xl p-3 text-xs sm:text-sm text-slate-100 focus:outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500 font-sans leading-relaxed"
              ></textarea>
            </div>

            <!-- Actions Row -->
            <div class="flex flex-wrap items-center justify-between gap-3 pt-1">
              <a id="reformat-deal-link" href="#" target="_blank" class="text-xs text-rose-400 hover:text-rose-300 flex items-center gap-1.5 font-bold">
                <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                <span>فحص الرابط التابع</span>
              </a>

              <button 
                onclick="publishReformattedDeal()" 
                id="reformat-publish-btn" 
                class="bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs sm:text-sm px-6 py-2.5 rounded-xl shadow-lg shadow-emerald-600/30 flex items-center justify-center gap-2 transition active:scale-95"
              >
                <i class="fa-solid fa-paper-plane"></i>
                <span>نشر في القناة الآن (@DzAliexpress0)</span>
              </button>
            </div>

            <!-- Feedback Notification Box -->
            <div id="reformat-feedback" class="hidden p-3 rounded-xl text-xs font-medium"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Auto-Publishing Speed & Schedule Control Panel -->
    <div class="glass-panel rounded-3xl p-5 sm:p-6 mb-6 card-hover border border-rose-500/20">
      <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-4 pb-3 border-b border-slate-800/80">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-rose-600 to-amber-500 flex items-center justify-center text-white shadow-lg shadow-rose-600/30">
            <i class="fa-solid fa-gauge-high"></i>
          </div>
          <div>
            <h3 class="font-bold text-sm sm:text-base text-white flex items-center gap-2">
              <span>سرعة وتوقيت النشر التلقائي</span>
              <span id="sched-badge-status" class="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-bold">نشط</span>
            </h3>
            <p class="text-[11px] text-slate-400">تحكم فوري في الفاصل الزمني بين كل منشور (نهاراً وليلاً)</p>
          </div>
        </div>
        <div id="sched-current-summary" class="text-xs text-rose-300 font-bold bg-slate-900/80 border border-slate-800 px-3 py-1.5 rounded-xl">
          كل 5 دقائق ☀️
        </div>
      </div>

      <!-- Quick Speed Buttons -->
      <div class="space-y-3">
        <div class="text-xs font-semibold text-slate-300">الفاصل الزمني النهاري:</div>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
          <button onclick="setSpeed(5)" id="btn-speed-5" class="speed-btn bg-rose-600 text-white font-bold text-xs py-2 px-3 rounded-xl border border-rose-500 transition flex items-center justify-center gap-1.5 active:scale-95 shadow-md shadow-rose-600/20">
            <i class="fa-solid fa-bolt"></i>
            <span>كل 5 دقائق</span>
          </button>
          <button onclick="setSpeed(10)" id="btn-speed-10" class="speed-btn bg-slate-800/80 hover:bg-slate-700 text-slate-300 font-bold text-xs py-2 px-3 rounded-xl border border-slate-700 transition flex items-center justify-center gap-1.5 active:scale-95">
            <i class="fa-solid fa-rocket"></i>
            <span>كل 10 دقائق</span>
          </button>
          <button onclick="setSpeed(15)" id="btn-speed-15" class="speed-btn bg-slate-800/80 hover:bg-slate-700 text-slate-300 font-bold text-xs py-2 px-3 rounded-xl border border-slate-700 transition flex items-center justify-center gap-1.5 active:scale-95">
            <i class="fa-solid fa-scale-balanced"></i>
            <span>كل 15 دقيقة</span>
          </button>
          <button onclick="setSpeed(30)" id="btn-speed-30" class="speed-btn bg-slate-800/80 hover:bg-slate-700 text-slate-300 font-bold text-xs py-2 px-3 rounded-xl border border-slate-700 transition flex items-center justify-center gap-1.5 active:scale-95">
            <i class="fa-solid fa-clock"></i>
            <span>كل 30 دقيقة</span>
          </button>
        </div>

        <!-- Mode Switches -->
        <div class="flex flex-wrap items-center justify-between gap-3 pt-3 border-t border-slate-800/60 text-xs">
          <button onclick="toggleNightMode()" id="btn-night-mode" class="bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 px-3 py-1.5 rounded-xl flex items-center gap-2 transition active:scale-95">
            <i class="fa-solid fa-moon text-indigo-400"></i>
            <span id="text-night-mode">الوضع الليلي: مفعّل (30د بعد منتصف الليل)</span>
          </button>
          <button onclick="togglePauseAuto()" id="btn-pause-auto" class="bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 px-3 py-1.5 rounded-xl flex items-center gap-2 transition active:scale-95">
            <i id="icon-pause-auto" class="fa-solid fa-pause text-amber-400"></i>
            <span id="text-pause-auto">إيقاف النشر مؤقتاً</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Quick Stats Cards -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
      <div class="glass-panel rounded-2xl p-4 card-hover">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span>عروض القناة الحية</span>
          <i class="fa-solid fa-bullhorn text-rose-400"></i>
        </div>
        <div id="stat-total" class="text-xl sm:text-2xl font-black text-rose-400">--</div>
        <span class="text-[10px] text-slate-500 mt-1 block">تحديث دوري من القناة</span>
      </div>

      <div class="glass-panel rounded-2xl p-4 card-hover">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span>عروض بالصور HD</span>
          <i class="fa-solid fa-image text-emerald-400"></i>
        </div>
        <div id="stat-photos" class="text-xl sm:text-2xl font-black text-emerald-400">--</div>
        <span class="text-[10px] text-slate-500 mt-1 block">صور المنتجات الأصلية</span>
      </div>

      <div class="glass-panel rounded-2xl p-4 card-hover">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span>سعر صرف الـ USDT 🇩🇿</span>
          <i class="fa-solid fa-arrow-trend-up text-amber-400"></i>
        </div>
        <div id="stat-usdt" class="text-xl sm:text-2xl font-black text-amber-400">249.0 دج</div>
        <a href="https://squarealgerie.com" target="_blank" class="text-[10px] text-slate-400 hover:text-amber-400 mt-1 block">SquareAlgerie.com</a>
      </div>

      <div class="glass-panel rounded-2xl p-4 card-hover">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span>حالة البوتات</span>
          <i class="fa-solid fa-robot text-blue-400"></i>
        </div>
        <div class="text-sm sm:text-base font-bold text-emerald-400 flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>تعمل بكفاءة 100%</span>
        </div>
        <span class="text-[10px] text-slate-500 mt-1 block">@Alilo07BOT • @DealscoutadminBOT</span>
      </div>
    </div>

    <!-- Main Content Layout -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

      <!-- Left 2 Cols: Posts Feed -->
      <div class="lg:col-span-2 space-y-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <h3 class="font-bold text-base text-white">آخر العروض المنشورة في القناة</h3>
            <span id="posts-badge" class="bg-slate-800 text-slate-400 text-xs px-2 py-0.5 rounded-full border border-slate-700">0</span>
          </div>
          <span id="last-update" class="text-xs text-slate-500"></span>
        </div>

        <!-- Skeleton Loading -->
        <div id="skeleton-container" class="space-y-3">
          <div class="glass-panel rounded-2xl p-4 space-y-3 animate-pulse">
            <div class="flex gap-3"><div class="w-20 h-20 bg-slate-800 rounded-xl"></div><div class="flex-1 space-y-2"><div class="h-4 bg-slate-800 rounded w-3/4"></div><div class="h-3 bg-slate-800 rounded w-1/2"></div></div></div>
          </div>
          <div class="glass-panel rounded-2xl p-4 space-y-3 animate-pulse">
            <div class="flex gap-3"><div class="w-20 h-20 bg-slate-800 rounded-xl"></div><div class="flex-1 space-y-2"><div class="h-4 bg-slate-800 rounded w-2/3"></div><div class="h-3 bg-slate-800 rounded w-1/3"></div></div></div>
          </div>
        </div>

        <!-- Posts Feed Container -->
        <div id="posts-container" class="space-y-3 hidden"></div>

        <!-- Error State -->
        <div id="error-state" class="hidden glass-panel rounded-2xl p-6 text-center text-rose-400">
          <i class="fa-solid fa-triangle-exclamation text-2xl mb-2"></i>
          <p id="error-message" class="text-xs"></p>
        </div>
      </div>

      <!-- Right 1 Col: Quick Links & Bots Guide -->
      <div class="space-y-4">

        <!-- Bots Card -->
        <div class="glass-panel rounded-2xl p-4 space-y-3">
          <h4 class="font-bold text-sm text-white flex items-center gap-2">
            <i class="fa-solid fa-paper-plane text-rose-400"></i>
            <span>بوتات التيليجرام الرسمية</span>
          </h4>
          
          <div class="space-y-2 text-xs">
            <a href="https://t.me/Alilo07BOT" target="_blank" class="block p-3 rounded-xl bg-slate-900 hover:bg-slate-800/80 border border-slate-800 transition">
              <div class="flex items-center justify-between mb-1">
                <span class="font-bold text-rose-400">🪙 بوت العملات للجميع</span>
                <span class="text-[10px] text-slate-500">@Alilo07BOT</span>
              </div>
              <p class="text-[11px] text-slate-400">مخصص لجميع المشتركين لزيادة تخفيض العملات حتى 70% وتوليد الروابط المباشرة.</p>
            </a>

            <a href="https://t.me/DealscoutadminBOT" target="_blank" class="block p-3 rounded-xl bg-slate-900 hover:bg-slate-800/80 border border-slate-800 transition">
              <div class="flex items-center justify-between mb-1">
                <span class="font-bold text-amber-400">👑 بوت الإدارة والنشر المباشر</span>
                <span class="text-[10px] text-slate-500">@DealscoutadminBOT</span>
              </div>
              <p class="text-[11px] text-slate-400">مخصص للأدمن فقط لفحص المنتجات، اختيار أفضل الصور، والنشر الفوري في القناة.</p>
            </a>
          </div>
        </div>

        <!-- SquareAlgerie Rate Card -->
        <div class="glass-panel rounded-2xl p-4 space-y-2.5">
          <div class="flex items-center justify-between">
            <h4 class="font-bold text-sm text-white flex items-center gap-2">
              <i class="fa-solid fa-chart-line text-emerald-400"></i>
              <span>سعر الصرف الموازي (السكوار)</span>
            </h4>
            <span class="text-[10px] text-slate-400">مباشر</span>
          </div>
          <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-between">
            <div>
              <span class="text-xs text-slate-400 block">سعر 1 USDT (الدولار الرقمي)</span>
              <span id="card-usdt-rate" class="text-lg font-black text-emerald-400">249.0 دج</span>
            </div>
            <a href="https://squarealgerie.com" target="_blank" class="text-xs bg-slate-800 hover:bg-slate-700 text-slate-200 px-3 py-1.5 rounded-lg border border-slate-700 transition">
              SquareAlgerie 🇩🇿
            </a>
          </div>
        </div>

        <!-- Country Hint Notice -->
        <div class="glass-panel rounded-2xl p-4 space-y-2">
          <div class="flex items-center gap-2 text-rose-400 font-bold text-xs">
            <i class="fa-solid fa-location-dot"></i>
            <span>تذكير مهم للمشترين 🇰🇷</span>
          </div>
          <p class="text-xs text-slate-300 leading-relaxed">
            لا تنسى تحويل دولة التطبيق إلى <b>كوريا 🇰🇷 📍</b> من إعدادات تطبيق AliExpress للحصول على أقصى نسبة تخفيض عملات وأسعار أقل!
          </p>
        </div>

      </div>
    </div>
  </main>

  <!-- Mobile Bottom Sticky Navigation -->
  <nav class="lg:hidden fixed bottom-0 left-0 right-0 glass-panel border-t border-slate-800/90 z-50 px-6 py-2.5 flex items-center justify-around text-xs">
    <button onclick="scrollToFeed()" class="flex flex-col items-center gap-1 text-rose-400 focus:outline-none">
      <i class="fa-solid fa-bolt text-base"></i>
      <span class="text-[10px] font-bold">العروض</span>
    </button>
    <button onclick="focusScout()" class="flex flex-col items-center gap-1 text-slate-400 hover:text-white focus:outline-none">
      <i class="fa-solid fa-magnifying-glass text-base"></i>
      <span class="text-[10px]">فاحص الرابط</span>
    </button>
    <a href="https://t.me/DzAliexpress0" target="_blank" class="flex flex-col items-center gap-1 text-slate-400 hover:text-white">
      <i class="fa-solid fa-paper-plane text-base"></i>
      <span class="text-[10px]">القناة</span>
    </a>
    <a href="https://squarealgerie.com" target="_blank" class="flex flex-col items-center gap-1 text-slate-400 hover:text-white">
      <i class="fa-solid fa-chart-simple text-base"></i>
      <span class="text-[10px]">السكوار</span>
    </a>
  </nav>

  <script>
    // PWA Service Worker Registration
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js').catch(err => console.log('SW registration error:', err));
      });
    }

    // PWA Install Prompt Handler
    let deferredPrompt;
    const installBtn = document.getElementById('pwa-install-btn');

    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault();
      deferredPrompt = e;
      if (installBtn) {
        installBtn.classList.remove('hidden');
      }
    });

    if (installBtn) {
      installBtn.addEventListener('click', async () => {
        if (!deferredPrompt) return;
        deferredPrompt.prompt();
        const { outcome } = await deferredPrompt.userChoice;
        if (outcome === 'accepted') {
          installBtn.classList.add('hidden');
        }
        deferredPrompt = null;
      });
    }

    // Live Feed Loader
    let isLoading = false;

    async function refreshDashboard() {
      if (isLoading) return;
      isLoading = true;

      const refreshIcon = document.getElementById('refresh-icon');
      if (refreshIcon) refreshIcon.classList.add('animate-spin');

      const skeleton = document.getElementById('skeleton-container');
      const container = document.getElementById('posts-container');
      const errorDiv = document.getElementById('error-state');

      if (skeleton) skeleton.classList.remove('hidden');
      if (container) container.classList.add('hidden');
      if (errorDiv) errorDiv.classList.add('hidden');

      try {
        // Fetch posts
        const res = await fetch('/api/channel-posts');
        const data = await res.json();

        // Fetch live USDT rate
        fetch('/api/rates').then(r => r.json()).then(rData => {
          if (rData && rData.rate) {
            const formatted = rData.rate.toFixed(1) + ' دج';
            const hRate = document.getElementById('header-usdt-rate');
            const sRate = document.getElementById('stat-usdt');
            const cRate = document.getElementById('card-usdt-rate');
            if (hRate) hRate.innerText = formatted;
            if (sRate) sRate.innerText = formatted;
            if (cRate) cRate.innerText = formatted;
          }
        }).catch(() => {});

        if (skeleton) skeleton.classList.add('hidden');

        if (!data.posts || data.posts.length === 0) {
          if (container) {
            container.innerHTML = '<div class="glass-panel rounded-2xl p-8 text-center text-slate-400">لا توجد منشورات حالياً في القناة.</div>';
            container.classList.remove('hidden');
          }
          return;
        }

        const posts = data.posts;
        document.getElementById('stat-total').innerText = posts.length;
        document.getElementById('stat-photos').innerText = posts.filter(p => p.photo_url).length;
        document.getElementById('posts-badge').innerText = posts.length;
        document.getElementById('last-update').innerText = 'تم التحديث ' + new Date().toLocaleTimeString('ar-DZ');

        container.innerHTML = posts.map(p => `
          <div class="glass-panel rounded-2xl p-4 card-hover space-y-3">
            <div class="flex items-start gap-3">
              ${p.photo_url ? `
                <div class="w-20 h-20 sm:w-24 sm:h-24 rounded-xl bg-slate-900 border border-slate-800 flex-shrink-0 overflow-hidden">
                  <img src="${p.photo_url}" class="w-full h-full object-cover" loading="lazy">
                </div>
              ` : `
                <div class="w-20 h-20 rounded-xl bg-slate-900 border border-slate-800 flex-shrink-0 flex items-center justify-center">
                  <i class="fa-solid fa-tag text-slate-700 text-xl"></i>
                </div>
              `}
              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between text-[11px] text-slate-500 mb-1">
                  <span>${p.date || ''}</span>
                  ${p.link ? `<a href="${p.link}" target="_blank" class="text-rose-400 hover:text-rose-300 flex items-center gap-1 font-bold"><span>فتح بالتيليجرام</span><i class="fa-solid fa-arrow-up-left-from-circle text-[10px]"></i></a>` : ''}
                </div>
                <div class="text-xs text-slate-200 whitespace-pre-wrap leading-relaxed font-sans line-clamp-6">${p.text}</div>
              </div>
            </div>
          </div>
        `).join('');

        container.classList.remove('hidden');
      } catch (err) {
        if (skeleton) skeleton.classList.add('hidden');
        if (errorDiv) {
          errorDiv.classList.remove('hidden');
          document.getElementById('error-message').innerText = 'تعذر تحميل المنشورات: ' + err.message;
        }
      } finally {
        isLoading = false;
        if (refreshIcon) refreshIcon.classList.remove('animate-spin');
      }
    }

    // In-Dashboard Deal Scout Action
    async function scoutDeal() {
      const input = document.getElementById('scout-url-input');
      const btn = document.getElementById('scout-submit-btn');
      const resBox = document.getElementById('scout-result');
      const val = (input.value || '').trim();

      if (!val) {
        input.focus();
        return;
      }

      btn.disabled = true;
      btn.innerHTML = '<i class="fa-solid fa-spinner animate-spin"></i><span>جاري الفحص...</span>';

      try {
        const resp = await fetch('/api/scout?url=' + encodeURIComponent(val));
        const data = await resp.json();

        if (data.ok && data.deal) {
          const d = data.deal;
          document.getElementById('scout-title').innerText = d.title || 'منتج مميز من AliExpress';
          document.getElementById('scout-price-usd').innerText = d.price ? '$' + d.price.toFixed(2) : 'سعر مميز';
          document.getElementById('scout-price-dzd').innerText = d.price_dzd ? '~ ' + d.price_dzd.toLocaleString() + ' دج' : '';
          document.getElementById('scout-pid').innerText = 'ID: ' + d.product_id;
          
          if (d.image_url) {
            document.getElementById('scout-img-box').innerHTML = `<img src="${d.image_url}" class="w-full h-full object-cover">`;
          }

          document.getElementById('scout-direct-link').href = d.product_link;
          document.getElementById('scout-coin-link').href = d.coin_link;

          resBox.classList.remove('hidden');
        } else {
          alert('تعذر استخراج بيانات المنتج من الرابط: ' + (data.error || 'تأكد من الرابط'));
        }
      } catch (e) {
        alert('حدث خطأ أثناء فحص الرابط: ' + e.message);
      } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles"></i><span>فحص العرض</span>';
      }
    }

    // Telegram Post Reformatter & 1-Tap Publisher Handlers
    let currentReformattedDeal = null;

    async function reformatTelegramPost() {
      const input = document.getElementById('reformat-input');
      const btn = document.getElementById('reformat-submit-btn');
      const resBox = document.getElementById('reformat-result');
      const feedback = document.getElementById('reformat-feedback');
      const val = (input.value || '').trim();

      if (!val) {
        input.focus();
        return;
      }

      btn.disabled = true;
      btn.innerHTML = '<i class="fa-solid fa-spinner animate-spin"></i><span>جاري المعالجة وإعادة التنسيق...</span>';
      if (feedback) feedback.classList.add('hidden');

      try {
        const resp = await fetch('/api/reformat-deal', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: val })
        });
        const data = await resp.json();

        if (data.ok) {
          currentReformattedDeal = data;
          document.getElementById('reformat-pid').innerText = 'ID: ' + data.product_id;
          document.getElementById('reformat-price-usd').innerText = data.price ? '$' + data.price.toFixed(2) : 'سعر خاص';
          document.getElementById('reformat-price-dzd').innerText = data.price_dzd ? '~ ' + data.price_dzd.toLocaleString() + ' دج' : '';

          const captionArea = document.getElementById('reformat-caption');
          captionArea.value = data.caption || '';
          updateCaptionCharCount();
          captionArea.oninput = updateCaptionCharCount;

          // Main image
          const imgBox = document.getElementById('reformat-img-box');
          if (data.image_url) {
            imgBox.innerHTML = `<img id="reformat-active-img" src="${data.image_url}" class="w-full h-full object-cover">`;
          } else {
            imgBox.innerHTML = '<i class="fa-solid fa-image text-slate-600 text-3xl"></i>';
          }

          // Gallery thumbnails
          const gallery = document.getElementById('reformat-gallery');
          if (data.images && data.images.length > 1) {
            gallery.innerHTML = data.images.map((img) => `
              <div onclick="selectReformatImage('${img}')" class="w-8 h-8 rounded-md bg-slate-800 border border-slate-700 overflow-hidden cursor-pointer hover:border-rose-500 transition">
                <img src="${img}" class="w-full h-full object-cover">
              </div>
            `).join('');
          } else {
            gallery.innerHTML = '';
          }

          document.getElementById('reformat-deal-link').href = data.deal_link || '#';
          resBox.classList.remove('hidden');
          resBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        } else {
          alert('تعذر استخراج بيانات العرض: ' + (data.error || 'تأكد من وجود رابط AliExpress في المنشور'));
        }
      } catch (e) {
        alert('حدث خطأ أثناء معالجة المنشور: ' + e.message);
      } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fa-solid fa-arrows-rotate"></i><span>إعادة التنسيق والمعاينة</span>';
      }
    }

    function selectReformatImage(imgUrl) {
      if (!currentReformattedDeal) return;
      currentReformattedDeal.image_url = imgUrl;
      const imgBox = document.getElementById('reformat-img-box');
      imgBox.innerHTML = `<img id="reformat-active-img" src="${imgUrl}" class="w-full h-full object-cover">`;
    }

    function updateCaptionCharCount() {
      const area = document.getElementById('reformat-caption');
      const countEl = document.getElementById('reformat-char-count');
      if (area && countEl) {
        const len = area.value.length;
        countEl.innerText = len + ' / 1024 حرف';
        countEl.className = len > 1024 ? 'text-[10px] text-rose-400 font-bold' : 'text-[10px] text-slate-500 font-mono';
      }
    }

    async function publishReformattedDeal() {
      if (!currentReformattedDeal) return;

      const btn = document.getElementById('reformat-publish-btn');
      const feedback = document.getElementById('reformat-feedback');
      const caption = document.getElementById('reformat-caption').value.trim();

      if (!caption) {
        alert('نص المنشور فارغ!');
        return;
      }

      if (!confirm('هل أنت متأكد من نشر هذا المنشور في القناة @DzAliexpress0 الآن؟')) {
        return;
      }

      btn.disabled = true;
      btn.innerHTML = '<i class="fa-solid fa-spinner animate-spin"></i><span>جاري النشر في القناة...</span>';
      if (feedback) feedback.classList.add('hidden');

      try {
        const resp = await fetch('/api/publish-deal', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            product_id: currentReformattedDeal.product_id,
            caption: caption,
            image_url: currentReformattedDeal.image_url,
            deal_link: currentReformattedDeal.deal_link
          })
        });
        const data = await resp.json();

        if (data.ok) {
          feedback.className = 'p-3 rounded-xl text-xs font-medium bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 flex items-center justify-between';
          feedback.innerHTML = `
            <div class="flex items-center gap-2">
              <i class="fa-solid fa-circle-check text-emerald-400 text-sm"></i>
              <span>تم نشر المنشور في القناة بنجاح! (#${data.message_id})</span>
            </div>
            ${data.post_url ? `<a href="${data.post_url}" target="_blank" class="bg-emerald-600 hover:bg-emerald-500 text-white px-2.5 py-1 rounded-lg text-[11px] font-bold">عرض بالتيليجرام</a>` : ''}
          `;
          feedback.classList.remove('hidden');
          setTimeout(refreshDashboard, 2000);
        } else {
          feedback.className = 'p-3 rounded-xl text-xs font-medium bg-rose-500/10 border border-rose-500/20 text-rose-300';
          feedback.innerText = 'فشل النشر: ' + (data.error || 'خطأ غير معروف');
          feedback.classList.remove('hidden');
        }
      } catch (e) {
        alert('حدث خطأ أثناء النشر: ' + e.message);
      } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fa-solid fa-paper-plane"></i><span>نشر في القناة الآن (@DzAliexpress0)</span>';
      }
    }

    function scrollToFeed() {
      window.scrollTo({ top: 350, behavior: 'smooth' });
    }

    function focusScout() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
      document.getElementById('scout-url-input').focus();
    }

    let currentSchedule = { current_interval_minutes: 5, night_mode_enabled: true, is_paused: false, is_night: false };

    async function loadSchedule() {
      try {
        const resp = await fetch('/api/schedule');
        const data = await resp.json();
        if (data.ok && data.config) {
          currentSchedule = { ...data.config, is_night: data.is_night };
          updateScheduleUI();
        }
      } catch (e) {}
    }

    function updateScheduleUI() {
      const cur = currentSchedule.current_interval_minutes || 5;
      const isNight = currentSchedule.is_night;
      const nightOn = currentSchedule.night_mode_enabled;
      const paused = currentSchedule.is_paused;

      [5, 10, 15, 30].forEach(m => {
        const btn = document.getElementById('btn-speed-' + m);
        if (btn) {
          if (m === cur) {
            btn.className = 'speed-btn bg-rose-600 text-white font-bold text-xs py-2 px-3 rounded-xl border border-rose-500 transition flex items-center justify-center gap-1.5 active:scale-95 shadow-md shadow-rose-600/20';
          } else {
            btn.className = 'speed-btn bg-slate-800/80 hover:bg-slate-700 text-slate-300 font-bold text-xs py-2 px-3 rounded-xl border border-slate-700 transition flex items-center justify-center gap-1.5 active:scale-95';
          }
        }
      });

      const summary = document.getElementById('sched-current-summary');
      if (summary) {
        if (paused) {
          summary.innerText = '⏸️ النشر متوقف مؤقتاً';
          summary.className = 'text-xs text-amber-300 font-bold bg-amber-500/10 border border-amber-500/20 px-3 py-1.5 rounded-xl';
        } else if (isNight && nightOn) {
          summary.innerText = 'كل ' + (currentSchedule.night_interval_minutes || 30) + ' دقيقة (ليلي 🌙)';
          summary.className = 'text-xs text-indigo-300 font-bold bg-indigo-500/10 border border-indigo-500/20 px-3 py-1.5 rounded-xl';
        } else {
          summary.innerText = 'كل ' + cur + ' دقائق (نهاري ☀️)';
          summary.className = 'text-xs text-rose-300 font-bold bg-slate-900/80 border border-slate-800 px-3 py-1.5 rounded-xl';
        }
      }

      const badge = document.getElementById('sched-badge-status');
      if (badge) {
        badge.innerText = paused ? 'متوقف مؤقتاً' : 'نشط';
        badge.className = paused
          ? 'text-[10px] px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-400 border border-amber-500/30 font-bold'
          : 'text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-bold';
      }

      const nightText = document.getElementById('text-night-mode');
      if (nightText) {
        nightText.innerText = nightOn ? 'الوضع الليلي: مفعّل (30د بعد منتصف الليل)' : 'الوضع الليلي: معطّل';
      }

      const pauseText = document.getElementById('text-pause-auto');
      const pauseIcon = document.getElementById('icon-pause-auto');
      if (pauseText) {
        pauseText.innerText = paused ? 'استئناف النشر التلقائي' : 'إيقاف النشر مؤقتاً';
      }
      if (pauseIcon) {
        pauseIcon.className = paused ? 'fa-solid fa-play text-emerald-400' : 'fa-solid fa-pause text-amber-400';
      }
    }

    async function setSpeed(mins) {
      currentSchedule.current_interval_minutes = mins;
      currentSchedule.day_interval_minutes = mins;
      currentSchedule.is_paused = false;
      updateScheduleUI();
      try {
        await fetch('/api/schedule', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ current_interval_minutes: mins, day_interval_minutes: mins, is_paused: false })
        });
      } catch (e) {}
    }

    async function toggleNightMode() {
      currentSchedule.night_mode_enabled = !currentSchedule.night_mode_enabled;
      updateScheduleUI();
      try {
        await fetch('/api/schedule', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ night_mode_enabled: currentSchedule.night_mode_enabled })
        });
      } catch (e) {}
    }

    async function togglePauseAuto() {
      currentSchedule.is_paused = !currentSchedule.is_paused;
      updateScheduleUI();
      try {
        await fetch('/api/schedule', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ is_paused: currentSchedule.is_paused })
        });
      } catch (e) {}
    }

    // Auto-load
    refreshDashboard();
    loadSchedule();
    setInterval(refreshDashboard, 60000);
    setInterval(loadSchedule, 30000);
  </script>
</body>
</html>"""


# ── Web App & PWA Routes ─────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Serves the modern responsive installable dashboard."""
    return HTMLResponse(content=DASHBOARD_HTML)


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
                "day_interval": cfg.get("day_interval_minutes", 5),
                "night_interval": cfg.get("night_interval_minutes", 30),
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
    try:
        data = await request.json()
        from app.publisher.state_tracker import update_schedule_config
        updated = update_schedule_config(data)
        return {"ok": True, "config": updated}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@app.get("/api/scout")
async def scout_endpoint(url: str = Query(...)):
    """In-Dashboard Deal Scout resolver."""
    try:
        from api.coin_bot import resolve_any_ali_link, generate_coin_discount_response, get_live_usdt_rate
        pid = await resolve_any_ali_link(url)
        if not pid:
            return {"ok": False, "error": "لم يتم التعرف على كود المنتج"}

        res = await generate_coin_discount_response(pid, raw_user_text=url)
        rate = await get_live_usdt_rate()
        price = res.get("price") or 0.0
        dzd = int(price * rate) if price else None

        return {
            "ok": True,
            "deal": {
                "product_id": pid,
                "title": res.get("title"),
                "price": price,
                "price_dzd": dzd,
                "image_url": res.get("image_url"),
                "product_link": res.get("product_link"),
                "coin_link": res.get("coin_link"),
            }
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


@app.post("/api/reformat-deal")
async def api_reformat_deal(request: Request):
    """Reformat raw Telegram deal post and prepare clean Algerian channel caption."""
    try:
        data = await request.json()
        raw_text = (data.get("text") or "").strip()
        if not raw_text:
            return {"ok": False, "error": "يرجى لصق نص المنشور"}

        from api.coin_bot import resolve_any_ali_link, generate_coin_discount_response, get_live_usdt_rate
        from api.admin_bot import parse_user_deal_submission, build_exact_deal_caption

        pid = await resolve_any_ali_link(raw_text)
        if not pid:
            return {"ok": False, "error": "لم يتم العثور على رابط منتج AliExpress صالح في النص"}

        parsed = parse_user_deal_submission(raw_text)
        deal_info = await generate_coin_discount_response(pid, raw_user_text=raw_text)

        title = parsed.get("custom_title") or deal_info.get("title") or "منتج مميز من AliExpress"
        price = parsed.get("user_price") or deal_info.get("price") or 0.0
        rate = await get_live_usdt_rate()
        dzd_price = int(price * rate) if price else 0

        coupon = parsed.get("coupon")
        seller_coupon = parsed.get("seller_coupon")
        coins_text = parsed.get("coins_text")
        country = parsed.get("country")

        from api.coin_bot import ensure_affiliate
        is_bundle = any(k in (raw_text or "").lower() for k in ["bundle", "حزم", "حزمة", "3 بـ", "3 منتجات", "3 قطع"])
        preferred_link = deal_info.get("bundle_link") if is_bundle else (deal_info.get("coin_link") or deal_info.get("product_link"))
        deal_link = ensure_affiliate(preferred_link, fallback_link=deal_info.get("product_link"), pid=pid)

        caption = await build_exact_deal_caption(
            title=title,
            price=price,
            affiliate_url=deal_link,
            coupon_code=coupon,
            seller_coupon=seller_coupon,
            coins_text=coins_text,
            country=country
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
            "price_dzd": dzd_price,
            "coupon": coupon,
            "seller_coupon": seller_coupon,
            "coins_text": coins_text,
            "country": country,
            "image_url": main_img,
            "images": images[:8],
            "deal_link": deal_link,
            "caption": caption
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


@app.post("/api/publish-deal")
async def api_publish_deal(request: Request):
    """Publish reformatted deal post directly to @DzAliexpress0."""
    try:
        data = await request.json()
        caption = (data.get("caption") or "").strip()
        image_url = (data.get("image_url") or "").strip() or None
        deal_link = (data.get("deal_link") or "").strip()
        product_id = data.get("product_id", "")

        if not caption:
            return {"ok": False, "error": "نص المنشور فارغ"}

        import os
        from api.admin_bot import ADMIN_BOT_TOKEN, TARGET_CHANNEL_ID, PUBLIC_BOT_USERNAME
        from api.coin_bot import ensure_affiliate

        token = ADMIN_BOT_TOKEN or os.getenv("TELEGRAM_BOT_TOKEN", "")
        if not token:
            return {"ok": False, "error": "توكن البوت غير مهيأ"}

        tracked_deal_link = ensure_affiliate(deal_link, pid=product_id)
        channel_reply_markup = {
            "inline_keyboard": [
                [
                    {"text": "🛒 رابط الشراء من AliExpress", "url": tracked_deal_link}
                ],
                [
                    {"text": "🪙 بوت تخفيض العملات DealScoutDz", "url": f"https://t.me/{PUBLIC_BOT_USERNAME}"}
                ]
            ]
        }

        api_url = f"https://api.telegram.org/bot{token}"
        async with httpx.AsyncClient(timeout=15.0) as client:
            if image_url:
                resp = await client.post(
                    f"{api_url}/sendPhoto",
                    json={
                        "chat_id": TARGET_CHANNEL_ID,
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
                        "chat_id": TARGET_CHANNEL_ID,
                        "text": caption,
                        "parse_mode": "HTML",
                        "reply_markup": channel_reply_markup
                    }
                )

            res = resp.json()
            if resp.status_code == 200 and res.get("ok"):
                msg_id = res["result"]["message_id"]
                try:
                    from app.publisher.state_tracker import record_post_published
                    record_post_published("manual_admin", msg_id, str(product_id), caption.splitlines()[0] if caption else "")
                except Exception:
                    pass

                ch_clean = str(TARGET_CHANNEL_ID).lstrip("@")
                return {
                    "ok": True,
                    "message_id": msg_id,
                    "channel": TARGET_CHANNEL_ID,
                    "post_url": f"https://t.me/{ch_clean}/{msg_id}"
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


@app.get("/api/channel-posts")
async def channel_posts():
    """Fetch recent posts from @DzAliexpress0 via public web preview."""
    try:
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            resp = await client.get(
                "https://t.me/s/DzAliexpress0",
                headers={"User-Agent": "Mozilla/5.0 (compatible; DealScoutBot/2.0)"}
            )

        if resp.status_code != 200:
            return JSONResponse(
                {"error": f"Telegram returned HTTP {resp.status_code}", "posts": []},
                status_code=502
            )

        soup = BeautifulSoup(resp.text, "html.parser")
        blocks = soup.find_all("div", class_="tgme_widget_message")

        posts = []
        for block in reversed(blocks):
            text_div = block.find("div", class_="tgme_widget_message_text")
            text = text_div.get_text(separator="\n").strip() if text_div else ""

            photo_url = None
            photo_wrap = block.find("a", class_="tgme_widget_message_photo_wrap")
            if photo_wrap and photo_wrap.get("style"):
                m = re.search(r"url\('([^']+)'\)", photo_wrap["style"])
                if m:
                    photo_url = m.group(1)

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

            posts.append({
                "text": text,
                "photo_url": photo_url,
                "date": date_str,
                "link": link
            })

        return {"posts": posts, "count": len(posts)}

    except httpx.TimeoutException:
        return JSONResponse(
            {"error": "Timeout fetching channel", "posts": []},
            status_code=504
        )
    except Exception as e:
        return JSONResponse(
            {"error": str(e), "posts": []},
            status_code=500
        )


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
async def set_telegram_webhook():
    """Sets the public Coin bot webhook to this Vercel deployment URL."""
    try:
        token = "8900887118:AAELbFHyV2joUO-4EJ0fPSoZurkQNuENbfY"
        webhook_url = "https://dealscout-green.vercel.app/api/webhook"
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"https://api.telegram.org/bot{token}/setWebhook",
                json={"url": webhook_url, "drop_pending_updates": True}
            )
            return resp.json()
    except Exception as e:
        return {"ok": False, "error": str(e)}


@app.get("/api/set-admin-webhook")
async def set_admin_telegram_webhook():
    """Sets the dedicated Admin bot webhook to this Vercel deployment URL."""
    try:
        admin_token = "8708965924:AAH7SoSX7VV3Nx_yI_J39VzWjlsc-XPgXAQ"
        webhook_url = "https://dealscout-green.vercel.app/api/admin-webhook"
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
    coin_token = "8900887118:AAELbFHyV2joUO-4EJ0fPSoZurkQNuENbfY"
    async with httpx.AsyncClient(timeout=10.0) as client:
        r1 = await client.get(f"https://api.telegram.org/bot{coin_token}/getMe")
        r2 = await client.get(f"https://api.telegram.org/bot{coin_token}/getWebhookInfo")
        return {"getMe": r1.json(), "webhook": r2.json()}


@app.api_route("/api/trigger-deals", methods=["GET", "POST"])
async def trigger_deals_collector(force: bool = False):
    """Triggers the AliExpress Deals collector workflow on GitHub Actions."""
    github_token = "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"
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
                    "message": "AliExpress Deals workflow triggered successfully on GitHub Actions!"
                }
            return {
                "ok": False,
                "status_code": resp.status_code,
                "error": resp.text
            }
    except Exception as e:
        return {"ok": False, "error": str(e)}


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

    function scrollToFeed() {
      window.scrollTo({ top: 350, behavior: 'smooth' });
    }

    function focusScout() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
      document.getElementById('scout-url-input').focus();
    }

    // Auto-load
    refreshDashboard();
    setInterval(refreshDashboard, 60000);
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
        from app.config.settings import settings
        token = settings.TELEGRAM_BOT_TOKEN
        if not token:
            return {"ok": False, "error": "TELEGRAM_BOT_TOKEN not configured"}

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
        admin_token = "8708965924:AAGi9HgLDxKsvaOzPOnCDRhI4c9WAfUvkOk"
        webhook_url = "https://dealscout-green.vercel.app/api/admin-webhook"
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"https://api.telegram.org/bot{admin_token}/setWebhook",
                json={"url": webhook_url, "drop_pending_updates": True}
            )
            return resp.json()
    except Exception as e:
        return {"ok": False, "error": str(e)}

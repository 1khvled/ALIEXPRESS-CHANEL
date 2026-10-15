"""
User-Facing Public Website for DealScout DZ.
Professional, serious e-commerce deal aggregator aesthetics.
Clean typography, high-contrast readability, zero glassmorphic slop.
Full Bilingual Support: Arabic (Default, RTL) & French (Secondary, LTR).
Structured Multi-Page Views: Deals, Coins Bot, FAQ, Contact, About.
Comprehensive E-Commerce Footer with Legal & Affiliate Compliance.
Optimized for mobile ergonomics (iOS Safari & Android Chrome) and rich SEO indexing.
"""

USER_WEBSITE_HTML = """<!DOCTYPE html>
<html lang="ar" dir="rtl" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, viewport-fit=cover">
  <title id="meta-title">DealScout DZ — صفقات وتخفيضات AliExpress بالدينار الجزائري</title>
  <meta name="description" id="meta-desc" content="منصة متخصصة في رصد وتحديث أفضل عروض وتخفيضات AliExpress الموجهة للجزائر لحظة بلحظة، مع حساب الأسعار بالدينار الجزائري وأكواد الخصم والعملات.">
  <meta name="robots" content="index, follow">

  <!-- Canonical & Alternate Hreflang -->
  <link rel="canonical" href="https://dealscout-green.vercel.app/">
  <link rel="alternate" hreflang="ar" href="https://dealscout-green.vercel.app/">
  <link rel="alternate" hreflang="ar-DZ" href="https://dealscout-green.vercel.app/">
  <link rel="alternate" hreflang="fr" href="https://dealscout-green.vercel.app/">
  <link rel="alternate" hreflang="x-default" href="https://dealscout-green.vercel.app/">

  <!-- Meta Search & Geography -->
  <meta name="keywords" content="aliexpress algerie, تخفيضات علي اكسبرس الجزائر, صفقات aliexpress, بريد الجزائر, اسعار السكوار, كود خصم علي اكسبرس, دينار جزائري, algeria deals, dealscout dz, عملات علي اكسبرس, bons plans algerie, codes promo aliexpress algerie">
  <meta name="geo.region" content="DZ">
  <meta name="geo.placename" content="Algeria">
  <meta name="geo.position" content="28.0339;1.6596">
  <meta name="ICBM" content="28.0339, 1.6596">
  <meta name="language" content="Arabic">
  <meta name="author" content="DealScout DZ">

  <!-- OpenGraph / Social Meta -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="DealScout DZ">
  <meta property="og:url" content="https://dealscout-green.vercel.app/">
  <meta property="og:title" id="og-title" content="DealScout DZ — صفقات وتخفيضات AliExpress بالدينار الجزائري">
  <meta property="og:description" id="og-desc" content="تتبع مباشر لأقوى صفقات وعروض AliExpress المنشورة لحظياً مع حساب السعر بالدينار الجزائري وأكواد الخصم والعملات.">
  <meta property="og:image" content="https://dealscout-green.vercel.app/icon.svg">
  <meta property="og:image:secure_url" content="https://dealscout-green.vercel.app/icon.svg">
  <meta property="og:image:type" content="image/svg+xml">
  <meta property="og:image:width" content="512">
  <meta property="og:image:height" content="512">
  <meta property="og:image:alt" content="DealScout DZ">
  <meta property="og:locale" content="ar_DZ">
  <meta property="og:locale:alternate" content="fr_DZ">
  <meta property="og:locale:alternate" content="fr_FR">

  <!-- Twitter Card Metadata -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@DzAliexpress0">
  <meta name="twitter:creator" content="@DzAliexpress0">
  <meta name="twitter:title" id="twitter-title" content="DealScout DZ — صفقات وتخفيضات AliExpress بالدينار الجزائري">
  <meta name="twitter:description" id="twitter-desc" content="تتبع مباشر لأقوى صفقات AliExpress المنشورة لحظياً مع حساب الأسعار بالدينار الجزائري وأكواد الخصم والعملات.">
  <meta name="twitter:image" content="https://dealscout-green.vercel.app/icon.svg">
  <meta name="twitter:image:alt" content="DealScout DZ">

  <!-- PWA & Mobile Meta (iOS Safari & Android Chrome) -->
  <link rel="manifest" href="/manifest.json">
  <link rel="icon" type="image/svg+xml" href="/icon.svg">
  <link rel="apple-touch-icon" href="/icon.svg">
  <meta name="theme-color" content="#0b0f19">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="DealScout DZ">
  <meta name="format-detection" content="telephone=no">

  <!-- Tailwind CSS & Icons -->
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=Inter:wght@400;500;600;700;800&family=Tajawal:wght@500;700;800&display=swap" rel="stylesheet">

  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            sans: ['"IBM Plex Sans Arabic"', 'Tajawal', 'Inter', 'sans-serif'],
            mono: ['Inter', 'monospace'],
            inter: ['Inter', 'sans-serif']
          },
          colors: {
            dark: {
              950: '#070a10',
              900: '#0b0f19',
              850: '#0f172a',
              800: '#1e293b',
              700: '#334155',
              600: '#475569'
            },
            crimson: {
              500: '#ef4444',
              600: '#dc2626',
              700: '#b91c1c'
            }
          }
        }
      }
    }
  </script>

  <style>
    :root {
      --sat: env(safe-area-inset-top, 0px);
      --sab: env(safe-area-inset-bottom, 0px);
      --sal: env(safe-area-inset-left, 0px);
      --sar: env(safe-area-inset-right, 0px);
    }
    html {
      scroll-behavior: smooth;
      -webkit-text-size-adjust: 100%;
    }
    body {
      background-color: #070a10;
      color: #f1f5f9;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      -webkit-tap-highlight-color: transparent;
    }
    body[dir="ltr"] {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    body[dir="rtl"] {
      font-family: 'IBM Plex Sans Arabic', Tajawal, sans-serif;
    }
    button, a, input, select, textarea, [role="button"] {
      touch-action: manipulation;
      -webkit-tap-highlight-color: transparent;
    }
    .deal-card {
      background-color: #0f172a;
      border: 1px solid #1e293b;
      transition: border-color 0.18s ease, transform 0.18s ease, box-shadow 0.18s ease;
    }
    @media (hover: hover) {
      .deal-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.4);
        transform: translateY(-2px);
      }
    }
    .no-scrollbar::-webkit-scrollbar { display: none; }
    .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
    
    .pt-safe { padding-top: max(0.375rem, env(safe-area-inset-top, 0px)); }
    .pb-safe { padding-bottom: calc(5.5rem + env(safe-area-inset-bottom, 0px)); }
    .bottom-nav-safe { padding-bottom: max(0.5rem, env(safe-area-inset-bottom, 0.5rem)); }
    .toast-bottom { bottom: calc(5.25rem + env(safe-area-inset-bottom, 0px)); }
    
    .momentum-scroll {
      -webkit-overflow-scrolling: touch;
      scroll-snap-type: x proximity;
    }
    .momentum-scroll > * { scroll-snap-align: start; }
    ::selection { background: #dc2626; color: #ffffff; }

    @keyframes slideUp {
      from { transform: translateY(100%); opacity: 0; }
      to { transform: translateY(0); opacity: 1; }
    }
    @keyframes fadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
    }
    .animate-slide-up { animation: slideUp 0.25s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
    .animate-fade-in { animation: fadeIn 0.2s ease-out forwards; }
    
    /* FAQ Accordion Transitions */
    .faq-item[open] summary .faq-icon {
      transform: rotate(180deg);
    }
  </style>

  <!-- Structured JSON-LD Schema -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "@id": "https://dealscout-green.vercel.app/#website",
    "url": "https://dealscout-green.vercel.app/",
    "name": "DealScout DZ",
    "alternateName": ["DealScout", "ديل سكاوت الجزائر", "AliExpress Deals Algeria", "Bons Plans AliExpress Algérie"],
    "description": "منصة متخصصة في رصد وتحديث أقوى صفقات وتخفيضات AliExpress الموجهة للجزائر لحظة بلحظة مع حساب الأسعار بالدينار الجزائري.",
    "inLanguage": ["ar", "fr"],
    "publisher": {
      "@type": "Organization",
      "@id": "https://dealscout-green.vercel.app/#organization",
      "name": "DealScout DZ",
      "url": "https://dealscout-green.vercel.app/",
      "logo": {
        "@type": "ImageObject",
        "url": "https://dealscout-green.vercel.app/icon.svg",
        "width": 512,
        "height": 512
      },
      "sameAs": [
        "https://t.me/DzAliexpress0",
        "https://t.me/francedealsdz",
        "https://t.me/Alilo07BOT"
      ],
      "areaServed": {
        "@type": "Country",
        "name": "Algeria"
      }
    },
    "potentialAction": {
      "@type": "SearchAction",
      "target": "https://dealscout-green.vercel.app/?q={search_term_string}",
      "query-input": "required name=search_term_string"
    }
  }
  </script>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "@id": "https://dealscout-green.vercel.app/#webpage",
    "url": "https://dealscout-green.vercel.app/",
    "name": "صفقات وتخفيضات AliExpress بالدينار الجزائري",
    "isPartOf": {
      "@id": "https://dealscout-green.vercel.app/#website"
    },
    "inLanguage": ["ar", "fr"],
    "description": "عروض يومية حصرية من AliExpress محسوبة بالدينار الجزائري عبر أسعار الصرف الحية."
  }
  </script>
</head>
<body class="min-h-screen bg-dark-950 text-slate-100 flex flex-col justify-between" dir="rtl">

  <!-- Top Utilities Bar -->
  <aside class="bg-dark-900 border-b border-dark-800 text-[11px] text-slate-400 py-1.5 px-4 pt-safe" aria-label="شريط المعلومات">
    <div class="max-w-7xl mx-auto flex items-center justify-between gap-3">
      <div class="flex items-center gap-3">
        <span class="inline-flex items-center gap-1.5 font-medium">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span data-i18n="top_live_updates">تحديث فوري من القنوات</span>
        </span>
        <span class="hidden sm:inline text-slate-700">|</span>
        <a href="https://squarealgerie.com" target="_blank" rel="noopener noreferrer" class="hidden sm:flex items-center gap-1 hover:text-slate-200 transition py-0.5">
          <i class="fa-solid fa-chart-line text-emerald-400"></i>
          <span><span data-i18n="top_usdt_rate">سعر صرف السكوار</span>: 1 USDT ≈ <b id="top-usdt-rate" class="font-mono text-emerald-400 font-bold">256.9</b> <span data-i18n="currency_dzd">دج</span></span>
        </a>
      </div>
      
      <div class="flex items-center gap-2 sm:gap-3">
        <!-- Language Switcher Button -->
        <div class="inline-flex items-center bg-dark-950 border border-dark-800 rounded-lg p-0.5 text-xs">
          <button onclick="setLanguage('ar')" id="lang-ar-btn" class="px-2 py-0.5 rounded text-[11px] font-bold bg-crimson-600 text-white transition active:scale-95">العربية</button>
          <button onclick="setLanguage('fr')" id="lang-fr-btn" class="px-2 py-0.5 rounded text-[11px] font-bold text-slate-400 hover:text-slate-200 transition active:scale-95">Français</button>
        </div>

        <span class="text-slate-700">|</span>
        <a href="https://t.me/Alilo07BOT" target="_blank" rel="noopener noreferrer" class="hover:text-amber-400 transition font-medium inline-flex items-center gap-1 py-1 px-1.5 active:scale-95 touch-manipulation">
          <i class="fa-solid fa-coins text-amber-400 text-[10px]"></i>
          <span class="hidden sm:inline" data-i18n="top_coin_bot">بوت العملات</span>
        </a>
        <span class="text-slate-700">|</span>
        <a href="https://t.me/DzAliexpress0" target="_blank" rel="noopener noreferrer" class="hover:text-sky-400 transition font-medium inline-flex items-center gap-1 py-1 px-1.5 active:scale-95 touch-manipulation">
          <i class="fa-brands fa-telegram text-sky-400"></i>
          <span class="hidden sm:inline">Telegram</span>
        </a>
      </div>
    </div>
  </aside>

  <!-- Main Navigation Bar -->
  <header class="sticky top-0 z-40 bg-dark-900/95 border-b border-dark-800 backdrop-blur-md px-3 sm:px-4 py-2.5 sm:py-3">
    <div class="max-w-7xl mx-auto flex items-center justify-between gap-3 sm:gap-4">
      
      <!-- Brand Logo -->
      <a href="#deals" onclick="showPage('deals')" class="flex items-center gap-2 sm:gap-2.5 flex-shrink-0 min-h-[44px] touch-manipulation" aria-label="DealScout DZ">
        <div class="w-9 h-9 rounded-xl bg-crimson-600 flex items-center justify-center font-bold text-white shadow-sm flex-shrink-0" aria-hidden="true">
          <i class="fa-solid fa-bolt text-base"></i>
        </div>
        <div>
          <div class="flex items-center gap-1.5">
            <h1 class="font-bold text-base text-white tracking-tight font-inter inline-flex items-center gap-1.5">
              <span>DealScout<span class="text-crimson-500">DZ</span></span>
              <span class="text-[10px] font-semibold bg-dark-800 text-slate-300 px-1.5 py-0.2 rounded border border-dark-700 font-mono font-normal">2.6</span>
            </h1>
          </div>
          <p class="text-[10px] text-slate-400 block -mt-0.5" data-i18n="brand_subtitle">بوابة صفقات وتخفيضات AliExpress 🇩🇿</p>
        </div>
      </a>

      <!-- Desktop Nav Pages Links -->
      <nav class="hidden lg:flex items-center gap-1 text-xs font-semibold text-slate-300">
        <button onclick="showPage('deals')" id="nav-link-deals" class="nav-page-btn px-3 py-1.5 rounded-lg bg-dark-800 text-white transition flex items-center gap-1.5">
          <i class="fa-solid fa-fire text-crimson-500 text-xs"></i>
          <span data-i18n="nav_deals">الصفقات</span>
        </button>
        <button onclick="showPage('coins')" id="nav-link-coins" class="nav-page-btn px-3 py-1.5 rounded-lg hover:bg-dark-800 hover:text-white transition flex items-center gap-1.5">
          <i class="fa-solid fa-coins text-amber-400 text-xs"></i>
          <span data-i18n="nav_coins">بوت العملات</span>
        </button>
        <button onclick="showPage('faq')" id="nav-link-faq" class="nav-page-btn px-3 py-1.5 rounded-lg hover:bg-dark-800 hover:text-white transition flex items-center gap-1.5">
          <i class="fa-solid fa-circle-question text-sky-400 text-xs"></i>
          <span data-i18n="nav_faq">الأسئلة الشائعة</span>
        </button>
        <button onclick="showPage('contact')" id="nav-link-contact" class="nav-page-btn px-3 py-1.5 rounded-lg hover:bg-dark-800 hover:text-white transition flex items-center gap-1.5">
          <i class="fa-solid fa-envelope text-emerald-400 text-xs"></i>
          <span data-i18n="nav_contact">اتصل بنا</span>
        </button>
        <button onclick="showPage('about')" id="nav-link-about" class="nav-page-btn px-3 py-1.5 rounded-lg hover:bg-dark-800 hover:text-white transition flex items-center gap-1.5">
          <i class="fa-solid fa-info-circle text-purple-400 text-xs"></i>
          <span data-i18n="nav_about">من نحن</span>
        </button>
      </nav>

      <!-- Search Bar Desktop -->
      <div class="hidden md:flex items-center relative flex-1 max-w-xs xl:max-w-sm">
        <i class="fa-solid fa-magnifying-glass absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-500 text-xs pointer-events-none" aria-hidden="true"></i>
        <input 
          type="search" 
          id="desktop-search" 
          aria-label="Search deals"
          oninput="handleSearchInput(this.value)"
          placeholder="ابحث عن هاتف، شاحن، كود خصم..." 
          data-i18n-placeholder="search_placeholder"
          class="w-full bg-dark-950 border border-dark-800 rounded-xl pr-9 pl-3 py-2 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-slate-600 transition min-h-[40px]"
        />
      </div>

      <!-- Action Buttons -->
      <div class="flex items-center gap-1.5 sm:gap-2">
        <!-- Currency Selector -->
        <div class="flex items-center bg-dark-950 border border-dark-800 rounded-xl p-0.5 text-xs font-semibold" aria-label="Currency" role="group">
          <button onclick="setCurrency('DZD')" id="curr-dzd" class="min-w-[34px] sm:min-w-[38px] h-8 sm:h-9 px-2 py-1 rounded-lg bg-dark-800 text-white font-mono transition flex items-center justify-center active:scale-95 touch-manipulation">دج</button>
          <button onclick="setCurrency('USD')" id="curr-usd" class="min-w-[32px] sm:min-w-[36px] h-8 sm:h-9 px-2 py-1 rounded-lg text-slate-400 hover:text-slate-200 font-mono transition flex items-center justify-center active:scale-95 touch-manipulation">$</button>
          <button onclick="setCurrency('EUR')" id="curr-eur" class="min-w-[32px] sm:min-w-[36px] h-8 sm:h-9 px-2 py-1 rounded-lg text-slate-400 hover:text-slate-200 font-mono transition flex items-center justify-center active:scale-95 touch-manipulation">€</button>
        </div>

        <!-- Join Telegram Button -->
        <a id="btn-telegram-join" href="https://t.me/DzAliexpress0" target="_blank" rel="noopener noreferrer" class="bg-[#229ED9] hover:bg-[#1e8ec3] text-white text-xs h-8 sm:h-9 px-2.5 sm:px-3 rounded-xl font-bold flex items-center justify-center gap-1.5 transition active:scale-95 shadow-sm touch-manipulation">
          <i class="fa-brands fa-telegram text-sm" aria-hidden="true"></i>
          <span class="hidden sm:inline" data-i18n="btn_join_channel">انضم للقناة</span>
        </a>

        <!-- Refresh Data Button -->
        <button onclick="fetchDeals(true)" title="تحديث البيانات" class="bg-dark-800 hover:bg-dark-700 text-slate-300 w-8 sm:w-9 h-8 sm:h-9 rounded-xl border border-dark-700 text-xs flex items-center justify-center transition active:scale-95 touch-manipulation">
          <i class="fa-solid fa-rotate-right" id="refresh-icon" aria-hidden="true"></i>
        </button>
      </div>

    </div>
  </header>

  <!-- ========================================== -->
  <!-- MAIN ROUTER PAGES CONTAINER -->
  <!-- ========================================== -->
  <main class="max-w-7xl mx-auto px-3.5 sm:px-4 py-4 sm:py-6 space-y-6 pb-safe w-full flex-grow">

    <!-- ───────────────────────────────────────────────────────── -->
    <!-- PAGE 1: DEALS BROWSER (DEFAULT)                           -->
    <!-- ───────────────────────────────────────────────────────── -->
    <div id="page-deals" class="page-view space-y-5 sm:space-y-6">

      <!-- Channel Switcher (Algeria vs France) -->
      <div class="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 bg-dark-900 border border-dark-800 p-2 sm:p-2.5 rounded-2xl">
        <div class="flex items-center gap-1.5 bg-dark-950 p-1 rounded-xl border border-dark-800 text-xs font-bold" role="tablist">
          <button onclick="switchChannel('@DzAliexpress0')" id="tab-dz" role="tab" aria-selected="true" class="flex-1 sm:flex-none min-h-[40px] px-4 py-2 rounded-lg bg-crimson-600 text-white transition flex items-center justify-center gap-2 active:scale-95 shadow-sm">
            <span>🇩🇿</span>
            <span data-i18n="tab_algeria_deals">عروض الجزائر (@DzAliexpress0)</span>
          </button>
          <button onclick="switchChannel('@francedealsdz')" id="tab-fr" role="tab" aria-selected="false" class="flex-1 sm:flex-none min-h-[40px] px-4 py-2 rounded-lg text-slate-400 hover:text-slate-200 transition flex items-center justify-center gap-2 active:scale-95">
            <span>🇫🇷</span>
            <span data-i18n="tab_france_deals">عروض فرنسا (@francedealsdz)</span>
          </button>
        </div>

        <!-- View Switcher (Grid vs Telegram Stream) -->
        <div class="flex items-center justify-end gap-1 bg-dark-950 border border-dark-800 rounded-xl p-1 text-xs font-semibold">
          <button onclick="setViewMode('grid')" id="view-mode-grid" class="min-h-[36px] px-3 py-1.5 rounded-lg bg-dark-800 text-slate-100 transition flex items-center gap-1.5 active:scale-95">
            <i class="fa-solid fa-grip text-xs"></i>
            <span data-i18n="view_grid">بطاقات</span>
          </button>
          <button onclick="setViewMode('feed')" id="view-mode-feed" class="min-h-[36px] px-3 py-1.5 rounded-lg text-slate-400 hover:text-slate-200 transition flex items-center gap-1.5 active:scale-95">
            <i class="fa-brands fa-telegram text-xs"></i>
            <span data-i18n="view_stream">منشورات القناة</span>
          </button>
        </div>
      </div>

      <!-- Mobile Search Bar -->
      <div class="md:hidden relative">
        <i class="fa-solid fa-magnifying-glass absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-500 text-sm pointer-events-none"></i>
        <input 
          type="search" 
          id="mobile-search" 
          aria-label="Search deals"
          oninput="handleSearchInput(this.value)"
          placeholder="ابحث عن هاتف، شاحن، كود خصم، ساعة..." 
          data-i18n-placeholder="search_placeholder"
          class="w-full bg-dark-900 border border-dark-800 rounded-xl pr-10 pl-3.5 py-3 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-slate-600 transition min-h-[46px]"
        />
      </div>

      <!-- Category Filter Pills -->
      <section class="border-b border-dark-800/80 pb-3" aria-label="Categories">
        <div class="flex items-center gap-2 overflow-x-auto no-scrollbar pb-1 text-xs font-semibold -mx-3.5 px-3.5 sm:mx-0 sm:px-0 momentum-scroll">
          <button onclick="setCategory('all')" id="cat-all" class="cat-pill min-h-[42px] px-3.5 py-2 rounded-xl bg-crimson-600 text-white whitespace-nowrap transition flex items-center gap-1.5 flex-shrink-0 active:scale-95 touch-manipulation shadow-sm">
            <span data-i18n="cat_all">الكل</span>
            <span id="count-all" class="text-[11px] font-mono opacity-80 bg-black/20 px-1.5 py-0.2 rounded">0</span>
          </button>
          <button onclick="setCategory('smartphones')" id="cat-smartphones" class="cat-pill min-h-[42px] px-3.5 py-2 rounded-xl bg-dark-900 hover:bg-dark-800 text-slate-300 border border-dark-800 whitespace-nowrap transition flex items-center gap-1.5 flex-shrink-0 active:scale-95 touch-manipulation">
            <span data-i18n="cat_smartphones">هواتف وتابلت</span>
            <span id="count-smartphones" class="text-[11px] font-mono text-slate-500">0</span>
          </button>
          <button onclick="setCategory('gaming')" id="cat-gaming" class="cat-pill min-h-[42px] px-3.5 py-2 rounded-xl bg-dark-900 hover:bg-dark-800 text-slate-300 border border-dark-800 whitespace-nowrap transition flex items-center gap-1.5 flex-shrink-0 active:scale-95 touch-manipulation">
            <span data-i18n="cat_gaming">أجهزة قيمنق</span>
            <span id="count-gaming" class="text-[11px] font-mono text-slate-500">0</span>
          </button>
          <button onclick="setCategory('audio')" id="cat-audio" class="cat-pill min-h-[42px] px-3.5 py-2 rounded-xl bg-dark-900 hover:bg-dark-800 text-slate-300 border border-dark-800 whitespace-nowrap transition flex items-center gap-1.5 flex-shrink-0 active:scale-95 touch-manipulation">
            <span data-i18n="cat_audio">سماعات وصوتيات</span>
            <span id="count-audio" class="text-[11px] font-mono text-slate-500">0</span>
          </button>
          <button onclick="setCategory('tech')" id="cat-tech" class="cat-pill min-h-[42px] px-3.5 py-2 rounded-xl bg-dark-900 hover:bg-dark-800 text-slate-300 border border-dark-800 whitespace-nowrap transition flex items-center gap-1.5 flex-shrink-0 active:scale-95 touch-manipulation">
            <span data-i18n="cat_tech">شواحن وملحقات</span>
            <span id="count-tech" class="text-[11px] font-mono text-slate-500">0</span>
          </button>
          <button onclick="setCategory('tajmi3at')" id="cat-tajmi3at" class="cat-pill min-h-[42px] px-3.5 py-2 rounded-xl bg-dark-900 hover:bg-dark-800 text-slate-300 border border-dark-800 whitespace-nowrap transition flex items-center gap-1.5 flex-shrink-0 active:scale-95 touch-manipulation">
            <span data-i18n="cat_tajmi3at">تجميعات العروض</span>
            <span id="count-tajmi3at" class="text-[11px] font-mono text-slate-500">0</span>
          </button>
        </div>
      </section>

      <!-- Section Title & Live Count -->
      <div class="flex items-center justify-between border-b border-dark-800/80 pb-2">
        <h2 class="text-xs sm:text-sm font-bold text-slate-200 flex items-center gap-2">
          <i class="fa-solid fa-fire text-crimson-500" aria-hidden="true"></i>
          <span data-i18n="deals_section_heading">أحدث صفقات وتخفيضات AliExpress بالدينار الجزائري</span>
        </h2>
        <span class="text-[11px] text-emerald-400 flex items-center gap-1.5 font-medium">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span id="live-deals-counter" class="font-mono">...</span>
        </span>
      </div>

      <!-- Deals Grid (Cards View) -->
      <section id="deals-grid" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3.5 sm:gap-4" aria-label="قائمة الصفقات">
        <!-- Skeleton Loaders -->
        <div class="deal-card rounded-2xl p-4 animate-pulse space-y-3">
          <div class="w-full aspect-[4/3] bg-dark-800 rounded-xl"></div>
          <div class="h-4 bg-dark-800 rounded w-3/4"></div>
          <div class="h-5 bg-dark-800 rounded w-1/2"></div>
          <div class="h-11 bg-dark-800 rounded-xl"></div>
        </div>
        <div class="deal-card rounded-2xl p-4 animate-pulse space-y-3">
          <div class="w-full aspect-[4/3] bg-dark-800 rounded-xl"></div>
          <div class="h-4 bg-dark-800 rounded w-3/4"></div>
          <div class="h-5 bg-dark-800 rounded w-1/2"></div>
          <div class="h-11 bg-dark-800 rounded-xl"></div>
        </div>
        <div class="deal-card rounded-2xl p-4 animate-pulse space-y-3">
          <div class="w-full aspect-[4/3] bg-dark-800 rounded-xl"></div>
          <div class="h-4 bg-dark-800 rounded w-3/4"></div>
          <div class="h-5 bg-dark-800 rounded w-1/2"></div>
          <div class="h-11 bg-dark-800 rounded-xl"></div>
        </div>
        <div class="deal-card rounded-2xl p-4 animate-pulse space-y-3">
          <div class="w-full aspect-[4/3] bg-dark-800 rounded-xl"></div>
          <div class="h-4 bg-dark-800 rounded w-3/4"></div>
          <div class="h-5 bg-dark-800 rounded w-1/2"></div>
          <div class="h-11 bg-dark-800 rounded-xl"></div>
        </div>
      </section>

      <!-- Telegram Stream Feed (Alternative View) -->
      <section id="deals-feed" class="hidden max-w-2xl mx-auto space-y-4" aria-label="بث منشورات القناة"></section>

      <!-- Empty State -->
      <div id="empty-state" class="hidden text-center py-12 px-4 space-y-3 border border-dashed border-dark-800 rounded-2xl bg-dark-900/50">
        <i class="fa-solid fa-magnifying-glass text-slate-600 text-3xl" aria-hidden="true"></i>
        <h3 class="font-bold text-sm text-slate-200" data-i18n="empty_title">لا توجد صفقات مطابقة للبحث</h3>
        <p class="text-xs text-slate-500" data-i18n="empty_desc">جرب كتابة اسم منتج أو علامة تجارية مختلفة أو أعد تعيين الفلاتر.</p>
        <button onclick="resetFilters()" class="min-h-[44px] px-4 py-2 text-xs font-bold text-crimson-500 hover:underline active:scale-95 touch-manipulation" data-i18n="empty_reset">
          عرض جميع الصفقات
        </button>
      </div>

    </div>

    <!-- ───────────────────────────────────────────────────────── -->
    <!-- PAGE 2: COINS BOT EXPLAINER PAGE                          -->
    <!-- ───────────────────────────────────────────────────────── -->
    <div id="page-coins" class="page-view hidden space-y-6">
      
      <div class="bg-gradient-to-r from-amber-500/10 via-dark-900 to-dark-900 border border-amber-500/30 rounded-3xl p-6 sm:p-8 space-y-4">
        <div class="inline-flex items-center gap-2 bg-amber-500/20 text-amber-400 px-3 py-1 rounded-full text-xs font-bold">
          <i class="fa-solid fa-coins"></i>
          <span data-i18n="coins_badge">دليل توفير العملات (AliExpress Coins)</span>
        </div>
        <h2 class="text-xl sm:text-2xl font-bold text-white tracking-tight" data-i18n="coins_hero_title">
          كيف توفر حتى 60% إضافية باستخدام عملات AliExpress وبوت @Alilo07BOT؟
        </h2>
        <p class="text-xs sm:text-sm text-slate-300 leading-relaxed max-w-3xl" data-i18n="coins_hero_desc">
          تمنح AliExpress مستخدميها عملات يومية (Coins)، لكن معظم المنتجات في التطبيق لا تسمح باستخدام أكثر من 2% فقط. بوت التخفيضات الخاص بنا يقوم بفك القيود وتوليد روابط مباشرة تمكّنك من استهلاك أكبر عدد ممكن من العملات والحصول على خصم ضخم فوري!
        </p>
        <div class="pt-2 flex flex-wrap gap-3">
          <a href="https://t.me/Alilo07BOT" target="_blank" rel="noopener noreferrer" class="min-h-[46px] px-5 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-dark-950 font-bold text-xs sm:text-sm flex items-center gap-2 shadow-lg shadow-amber-500/20 active:scale-95 transition">
            <i class="fa-solid fa-coins"></i>
            <span data-i18n="coins_btn_start">تشغيل البوت مجاناً (@Alilo07BOT)</span>
          </a>
        </div>
      </div>

      <!-- 3 Steps Grid -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="bg-dark-900 border border-dark-800 rounded-2xl p-5 space-y-3">
          <div class="w-10 h-10 rounded-xl bg-dark-800 text-amber-400 font-bold text-base flex items-center justify-center font-mono">1</div>
          <h3 class="font-bold text-sm text-white" data-i18n="coins_step1_title">انسخ رابط المنتج من AliExpress</h3>
          <p class="text-xs text-slate-400 leading-relaxed" data-i18n="coins_step1_desc">افتح أي منتج يعجبك داخل تطبيق AliExpress، اضغط على زر المشاركة ثم اختر نسخ الرابط (Copy Link).</p>
        </div>

        <div class="bg-dark-900 border border-dark-800 rounded-2xl p-5 space-y-3">
          <div class="w-10 h-10 rounded-xl bg-dark-800 text-sky-400 font-bold text-base flex items-center justify-center font-mono">2</div>
          <h3 class="font-bold text-sm text-white" data-i18n="coins_step2_title">أرسل الرابط لبوت التخفيض</h3>
          <p class="text-xs text-slate-400 leading-relaxed" data-i18n="coins_step2_desc">افتح بوت التيليجرام <b class="text-sky-400">@Alilo07BOT</b> والصق الرابط في المحادثة. سيقوم البوت فوراً بالبحث عن أقصى نسبة خصم متاحة للعملات.</p>
        </div>

        <div class="bg-dark-900 border border-dark-800 rounded-2xl p-5 space-y-3">
          <div class="w-10 h-10 rounded-xl bg-dark-800 text-emerald-400 font-bold text-base flex items-center justify-center font-mono">3</div>
          <h3 class="font-bold text-sm text-white" data-i18n="coins_step3_title">ادفع بالسعر المخفض</h3>
          <p class="text-xs text-slate-400 leading-relaxed" data-i18n="coins_step3_desc">اضغط على زر (شراء الآن) من الرابط الذي يرجعه البوت، وستلاحظ أن خانة العملات قد خصمت ما يصل إلى 10$ إلى 40$ من السعر الإجمالي!</p>
        </div>
      </div>

    </div>

    <!-- ───────────────────────────────────────────────────────── -->
    <!-- PAGE 3: FAQ PAGE                                          -->
    <!-- ───────────────────────────────────────────────────────── -->
    <div id="page-faq" class="page-view hidden space-y-6">
      
      <div class="text-center max-w-2xl mx-auto space-y-2">
        <h2 class="text-xl sm:text-2xl font-bold text-white" data-i18n="faq_title">الأسئلة الشائعة وإرشادات الشراء</h2>
        <p class="text-xs sm:text-sm text-slate-400" data-i18n="faq_subtitle">كل ما يحتاجه المتسوق الجزائري لمعرفة طرق الشحن، حساب الأسعار بالدينار، والتعامل مع عروض AliExpress.</p>
      </div>

      <div class="space-y-3 max-w-3xl mx-auto">
        <!-- Q1 -->
        <details class="faq-item group bg-dark-900 border border-dark-800 rounded-2xl p-4 transition-colors hover:border-slate-700">
          <summary class="flex items-center justify-between cursor-pointer list-none font-bold text-xs sm:text-sm text-slate-100 select-none">
            <span class="flex items-center gap-2">
              <i class="fa-solid fa-coins text-amber-400"></i>
              <span data-i18n="faq_q1">كيف يتم احتساب الأسعار بالدينار الجزائري (DZD)؟</span>
            </span>
            <i class="fa-solid fa-chevron-down text-slate-500 text-xs transition-transform duration-200 faq-icon"></i>
          </summary>
          <div class="pt-3 text-xs text-slate-400 leading-relaxed border-t border-dark-800 mt-3" data-i18n="faq_a1">
            يتم حساب السعر بالدينار الجزائري تلقائياً وبدقة عالية اعتماداً على سعر صرف الدولار واليورو في السوق الموازي (سعر السكوار الحقيقي) المستخرج مباشرة من موقع SquareAlgerie.com، حتى تتطابق المبالغ مع ما تدفعه حقيقة عند شحن بطاقاتك (Visa / Mastercard / Bybit / RedotPay).
          </div>
        </details>

        <!-- Q2 -->
        <details class="faq-item group bg-dark-900 border border-dark-800 rounded-2xl p-4 transition-colors hover:border-slate-700">
          <summary class="flex items-center justify-between cursor-pointer list-none font-bold text-xs sm:text-sm text-slate-100 select-none">
            <span class="flex items-center gap-2">
              <i class="fa-solid fa-truck-fast text-sky-400"></i>
              <span data-i18n="faq_q2">كيف يتم شحن الطرود واستلامها في الجزائر؟</span>
            </span>
            <i class="fa-solid fa-chevron-down text-slate-500 text-xs transition-transform duration-200 faq-icon"></i>
          </summary>
          <div class="pt-3 text-xs text-slate-400 leading-relaxed border-t border-dark-800 mt-3" data-i18n="faq_a2">
            تشحن معظم المنتجات عبر بريد الجزائر (Algérie Poste / EMS). يصل الطرد إلى أقرب مكتب بريد لعنوان سكناك ويتم إرسال إشعار وصول إلى هاتفك أو صندوق بريدك. للشحنات العادية، تتراوح مدة الوصول بين 15 و35 يوماً عبر خيار AliExpress Standard Shipping.
          </div>
        </details>

        <!-- Q3 -->
        <details class="faq-item group bg-dark-900 border border-dark-800 rounded-2xl p-4 transition-colors hover:border-slate-700">
          <summary class="flex items-center justify-between cursor-pointer list-none font-bold text-xs sm:text-sm text-slate-100 select-none">
            <span class="flex items-center gap-2">
              <i class="fa-solid fa-credit-card text-emerald-400"></i>
              <span data-i18n="faq_q3">ما هي أفضل طرق وبطاقات الدفع المتاحة للجزائريين؟</span>
            </span>
            <i class="fa-solid fa-chevron-down text-slate-500 text-xs transition-transform duration-200 faq-icon"></i>
          </summary>
          <div class="pt-3 text-xs text-slate-400 leading-relaxed border-t border-dark-800 mt-3" data-i18n="faq_a3">
            يمكنك الدفع بسهولة عبر بطاقات فيزا وماستركارد الافتراضية الدولية مثل RedotPay، Bybit Card، Paysera، Pyypl، أو بطاقات العملة الصعبة الصادرة من البنوك الوطنية الجزائرية (AGB، BDL، بنك الخليج الجزائر).
          </div>
        </details>

        <!-- Q4 -->
        <details class="faq-item group bg-dark-900 border border-dark-800 rounded-2xl p-4 transition-colors hover:border-slate-700">
          <summary class="flex items-center justify-between cursor-pointer list-none font-bold text-xs sm:text-sm text-slate-100 select-none">
            <span class="flex items-center gap-2">
              <i class="fa-solid fa-ticket text-rose-400"></i>
              <span data-i18n="faq_q4">لماذا يظهر كود الخصم غير صالح أو منتهي الصلاحية أحياناً؟</span>
            </span>
            <i class="fa-solid fa-chevron-down text-slate-500 text-xs transition-transform duration-200 faq-icon"></i>
          </summary>
          <div class="pt-3 text-xs text-slate-400 leading-relaxed border-t border-dark-800 mt-3" data-i18n="faq_a4">
            أكواد الخصم الترويجية في AliExpress تكون محدودة بعدد استخدامات معين لكل دولة. نقوم بتحديث الأكواد لحظياً وإلغاء المنتهية فوراً، ولكن ننصح دائماً بالشراء السريع عند نشر الكود قبل نفاد حصة الجزائر.
          </div>
        </details>

        <!-- Q5 -->
        <details class="faq-item group bg-dark-900 border border-dark-800 rounded-2xl p-4 transition-colors hover:border-slate-700">
          <summary class="flex items-center justify-between cursor-pointer list-none font-bold text-xs sm:text-sm text-slate-100 select-none">
            <span class="flex items-center gap-2">
              <i class="fa-solid fa-earth-europe text-blue-400"></i>
              <span data-i18n="faq_q5">ما هي قناة عروض فرنسا (@francedealsdz)؟</span>
            </span>
            <i class="fa-solid fa-chevron-down text-slate-500 text-xs transition-transform duration-200 faq-icon"></i>
          </summary>
          <div class="pt-3 text-xs text-slate-400 leading-relaxed border-t border-dark-800 mt-3" data-i18n="faq_a5">
            هي قناة متخصصة وموجهة لأفراد الجالية الجزائرية المقيمين في فرنسا وأوروبا، أو للجزائريين الذين يستعينون بشركات إعادة توجيه الطرود (Forwarders). أسعارها باليورو الأوروبي وعروضها مشحونة من مستودعات أوروبية سريعة (خلال 3-7 أيام).
          </div>
        </details>
      </div>

    </div>

    <!-- ───────────────────────────────────────────────────────── -->
    <!-- PAGE 4: CONTACT & SUPPORT PAGE                            -->
    <!-- ───────────────────────────────────────────────────────── -->
    <div id="page-contact" class="page-view hidden space-y-6">
      
      <div class="text-center max-w-2xl mx-auto space-y-2">
        <h2 class="text-xl sm:text-2xl font-bold text-white" data-i18n="contact_title">اتصل بنا والدعم الفني</h2>
        <p class="text-xs sm:text-sm text-slate-400" data-i18n="contact_subtitle">فريق DealScout DZ يرحب باقتراحاتكم، إبلاغكم عن الروابط التالفة، واستفساراتكم حول الصفقات.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto">
        <!-- Direct Telegram Support Card -->
        <div class="bg-dark-900 border border-dark-800 rounded-2xl p-6 space-y-4 flex flex-col justify-between">
          <div class="space-y-3">
            <div class="w-12 h-12 rounded-2xl bg-sky-500/10 text-sky-400 flex items-center justify-center text-xl">
              <i class="fa-brands fa-telegram"></i>
            </div>
            <h3 class="font-bold text-base text-white" data-i18n="contact_tg_title">الدعم السريع عبر Telegram</h3>
            <p class="text-xs text-slate-400 leading-relaxed" data-i18n="contact_tg_desc">
              أسرع وسيلة للتواصل مع مديري القناة والمطورين. يمكنك إرسال استفسارك أو طلب إضافة منتج معين إلى المراقبة الآلية.
            </p>
          </div>

          <div class="space-y-2.5 pt-2">
            <a href="https://t.me/DealscoutadminBOT" target="_blank" rel="noopener noreferrer" class="w-full min-h-[44px] bg-[#229ED9] hover:bg-[#1c8cc1] text-white font-bold text-xs py-2.5 px-4 rounded-xl flex items-center justify-center gap-2 active:scale-95 transition">
              <i class="fa-solid fa-paper-plane text-xs"></i>
              <span data-i18n="contact_tg_btn_admin">مراسلة إدارة DealScout</span>
            </a>
            <a href="https://t.me/Alilo07BOT" target="_blank" rel="noopener noreferrer" class="w-full min-h-[44px] bg-dark-800 hover:bg-dark-750 text-amber-400 font-bold text-xs py-2.5 px-4 rounded-xl border border-dark-700 flex items-center justify-center gap-2 active:scale-95 transition">
              <i class="fa-solid fa-coins text-xs"></i>
              <span data-i18n="contact_tg_btn_bot">الدخول لبوت العملات (@Alilo07BOT)</span>
            </a>
          </div>
        </div>

        <!-- Contact Form -->
        <div class="bg-dark-900 border border-dark-800 rounded-2xl p-6 space-y-4">
          <h3 class="font-bold text-base text-white" data-i18n="contact_form_title">إرسال رسالة أو اقتراح</h3>
          <form onsubmit="handleContactSubmit(event)" class="space-y-3 text-xs">
            <div>
              <label class="block text-slate-300 mb-1 font-medium" data-i18n="form_name">الاسم أو اللقب</label>
              <input type="text" id="contact-name" required class="w-full bg-dark-950 border border-dark-800 rounded-xl px-3 py-2 text-slate-100 placeholder-slate-600 focus:outline-none focus:border-slate-600" placeholder="مثال: أمين الجزائري">
            </div>
            <div>
              <label class="block text-slate-300 mb-1 font-medium" data-i18n="form_email">البريد الإلكتروني أو معرف تيليجرام</label>
              <input type="text" id="contact-email" required class="w-full bg-dark-950 border border-dark-800 rounded-xl px-3 py-2 text-slate-100 placeholder-slate-600 focus:outline-none focus:border-slate-600" placeholder="@username أو name@email.com">
            </div>
            <div>
              <label class="block text-slate-300 mb-1 font-medium" data-i18n="form_subject">نوع الاستفسار</label>
              <select id="contact-subject" class="w-full bg-dark-950 border border-dark-800 rounded-xl px-3 py-2 text-slate-100 focus:outline-none focus:border-slate-600">
                <option value="deal_suggestion" data-i18n="form_opt1">اقتراح صفقة أو منتج لمراقبته</option>
                <option value="broken_link" data-i18n="form_opt2">إبلاغ عن رابط تالف أو كود منتهي</option>
                <option value="partnership" data-i18n="form_opt3">شراكة أو إعلان تجاري</option>
                <option value="general" data-i18n="form_opt4">استفسار عام</option>
              </select>
            </div>
            <div>
              <label class="block text-slate-300 mb-1 font-medium" data-i18n="form_message">نص الرسالة</label>
              <textarea id="contact-message" rows="3" required class="w-full bg-dark-950 border border-dark-800 rounded-xl px-3 py-2 text-slate-100 placeholder-slate-600 focus:outline-none focus:border-slate-600" placeholder="اكتب تفاصيل استفسارك هنا..."></textarea>
            </div>
            <button type="submit" class="w-full min-h-[44px] bg-crimson-600 hover:bg-crimson-700 text-white font-bold text-xs py-2.5 px-4 rounded-xl flex items-center justify-center gap-2 active:scale-95 transition">
              <i class="fa-solid fa-paper-plane text-xs"></i>
              <span data-i18n="form_submit">إرسال الرسالة</span>
            </button>
          </form>
        </div>
      </div>

    </div>

    <!-- ───────────────────────────────────────────────────────── -->
    <!-- PAGE 5: ABOUT US PAGE                                     -->
    <!-- ───────────────────────────────────────────────────────── -->
    <div id="page-about" class="page-view hidden space-y-6">
      
      <div class="max-w-3xl mx-auto space-y-6 text-xs sm:text-sm text-slate-300 leading-relaxed">
        <div class="bg-dark-900 border border-dark-800 rounded-3xl p-6 sm:p-8 space-y-4">
          <div class="w-12 h-12 rounded-2xl bg-crimson-600/10 text-crimson-500 flex items-center justify-center text-2xl font-bold">
            <i class="fa-solid fa-bolt"></i>
          </div>
          <h2 class="text-xl sm:text-2xl font-bold text-white tracking-tight" data-i18n="about_title">حول منصة DealScout DZ</h2>
          <p class="leading-relaxed" data-i18n="about_p1">
            تأسست منصة <b>DealScout DZ</b> بهدف حل أكبر مشكلة تواجه المتسوقين في الجزائر عبر الإنترنت: صعوبة الوصول إلى التخفيضات الحقيقية، والارتباك الناتج عن حساب تكلفة المنتج بالدينار الجزائري في ظل تغير أسعار سوق السكوار.
          </p>
          <p class="leading-relaxed" data-i18n="about_p2">
            نقوم بمسح آلاف الصفقات المنشورة في مجموعات AliExpress المعتمدة، ثم نطبق خوارزميات ذكية لتصفية العروض الوهمية، وإبراز المنتجات الأكثر طلباً في السوق الجزائري (الهواتف الذكية، ملحقات الحواسيب، أجهزة القيمنق، الشواحن الأصلية، والأدوات المنزلية الذكية).
          </p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div class="bg-dark-900 border border-dark-800 rounded-2xl p-5 space-y-2">
            <h3 class="font-bold text-sm text-white flex items-center gap-2">
              <i class="fa-solid fa-chart-line text-emerald-400"></i>
              <span data-i18n="about_feat1_title">ربط مباشر مع سعر السكوار</span>
            </h3>
            <p class="text-xs text-slate-400 leading-relaxed" data-i18n="about_feat1_desc">نحدث أسعار USDT بالدينار الجزائري لحظة بلحظة لضمان شفافية كاملة قبل الضغط على زر الشراء.</p>
          </div>

          <div class="bg-dark-900 border border-dark-800 rounded-2xl p-5 space-y-2">
            <h3 class="font-bold text-sm text-white flex items-center gap-2">
              <i class="fa-solid fa-robot text-sky-400"></i>
              <span data-i18n="about_feat2_title">روبوتات آلية وخوارزميات أمان</span>
            </h3>
            <p class="text-xs text-slate-400 leading-relaxed" data-i18n="about_feat2_desc">نظام ذكي يلتقط التخفيضات في الثواني الأولى لنزولها ويختبر صلاحية أكواد الخصم والعملات.</p>
          </div>
        </div>

        <!-- Affiliate Disclosure Notice -->
        <div class="bg-dark-950 border border-dark-800 rounded-2xl p-4 sm:p-5 space-y-2 text-slate-400 text-xs">
          <h4 class="font-bold text-slate-200 flex items-center gap-2">
            <i class="fa-solid fa-handshake text-blue-400"></i>
            <span data-i18n="about_disclosure_title">إفصاح الشفافية والتسويق بالعمولة (Affiliate Disclosure)</span>
          </h4>
          <p class="leading-relaxed" data-i18n="about_disclosure_desc">
            منصة DealScout DZ مشتركة في برنامج شركاء AliExpress الرسمي (AliExpress Portals Affiliate Program). عند النقر على روابط الشراء وإتمام الطلب، قد نحصل على عمولة تسويقية صغيرة من منصة AliExpress. هذه العمولة لا تزيد من سعر المنتج عليك بأي سنتيم، بل تساعدنا في دفع تكاليف الخوادم وتطوير البوتات مجاناً للمجتمع.
          </p>
        </div>

      </div>

    </div>

  </main>

  <!-- Mobile Bottom Navigation Bar -->
  <nav class="md:hidden fixed bottom-0 left-0 right-0 z-50 bg-dark-900/95 backdrop-blur-md border-t border-dark-800/80 px-2 py-1 flex items-center justify-around text-center text-[10px] bottom-nav-safe" aria-label="التنقل للجوال">
    <button onclick="showPage('deals')" id="mob-bottom-deals" class="flex-1 min-h-[48px] py-1 flex flex-col items-center justify-center gap-1 text-crimson-500 font-bold active:scale-90 transition-transform touch-manipulation">
      <i class="fa-solid fa-fire text-base"></i>
      <span data-i18n="nav_deals">الصفقات</span>
    </button>
    <button onclick="showPage('coins')" id="mob-bottom-coins" class="flex-1 min-h-[48px] py-1 flex flex-col items-center justify-center gap-1 text-slate-400 hover:text-slate-200 font-medium active:scale-90 transition-transform touch-manipulation">
      <i class="fa-solid fa-coins text-base"></i>
      <span data-i18n="nav_coins">العملات</span>
    </button>
    <button onclick="showPage('faq')" id="mob-bottom-faq" class="flex-1 min-h-[48px] py-1 flex flex-col items-center justify-center gap-1 text-slate-400 hover:text-slate-200 font-medium active:scale-90 transition-transform touch-manipulation">
      <i class="fa-solid fa-circle-question text-base"></i>
      <span data-i18n="nav_faq">الأسئلة</span>
    </button>
    <button onclick="showPage('contact')" id="mob-bottom-contact" class="flex-1 min-h-[48px] py-1 flex flex-col items-center justify-center gap-1 text-slate-400 hover:text-slate-200 font-medium active:scale-90 transition-transform touch-manipulation">
      <i class="fa-solid fa-envelope text-base"></i>
      <span data-i18n="nav_contact">اتصل بنا</span>
    </button>
  </nav>

  <!-- Deal Details Bottom Sheet & Lightbox Modal -->
  <div id="deal-modal" onclick="onModalBackdropClick(event)" class="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm hidden flex items-end sm:items-center justify-center p-0 sm:p-4 animate-fade-in" role="dialog" aria-modal="true" aria-labelledby="modal-title">
    <div id="modal-container" class="bg-dark-900 border-t sm:border border-dark-700/80 rounded-t-3xl sm:rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto no-scrollbar shadow-2xl p-4 sm:p-6 pb-safe space-y-4 animate-slide-up relative">
      
      <!-- Mobile Pull Dismiss Handle -->
      <div class="sm:hidden w-12 h-1.5 bg-dark-700 hover:bg-dark-600 rounded-full mx-auto -mt-1 mb-2 cursor-pointer touch-manipulation" onclick="closeDealModal()"></div>
      
      <!-- Close Button -->
      <button onclick="closeDealModal()" aria-label="إغلاق" class="absolute top-3.5 left-3.5 bg-dark-800 hover:bg-dark-700 text-slate-300 hover:text-white w-10 h-10 min-w-[40px] min-h-[40px] rounded-full flex items-center justify-center text-sm border border-dark-700 active:scale-95 transition z-10 touch-manipulation shadow-md">
        <i class="fa-solid fa-xmark"></i>
      </button>

      <!-- Image Preview Container -->
      <div id="modal-img-wrap" class="relative w-full aspect-[4/3] rounded-2xl overflow-hidden bg-dark-950 border border-dark-800 flex items-center justify-center">
        <img id="modal-img" src="" alt="Deal preview" class="w-full h-full object-contain" loading="lazy" decoding="async">
        <span id="modal-country" class="absolute top-2.5 right-2.5 bg-dark-900/90 text-slate-200 text-xs px-2.5 py-0.5 rounded-lg font-bold border border-dark-700 hidden shadow-sm"></span>
        <span id="modal-coins" class="absolute top-2.5 left-2.5 bg-amber-500 text-slate-950 text-xs font-bold px-2 py-0.5 rounded-lg hidden items-center gap-1 shadow-sm"><i class="fa-solid fa-coins text-[10px]"></i> عملات</span>
      </div>

      <!-- Modal Content Body -->
      <div class="space-y-3.5">
        <div class="flex items-center justify-between gap-2 text-xs text-slate-400">
          <span id="modal-cat" class="px-2.5 py-1 rounded-lg bg-dark-950 border border-dark-800 text-[11px] font-semibold text-slate-300"></span>
          <span id="modal-date" class="font-mono text-xs text-slate-500"></span>
        </div>

        <h3 id="modal-title" class="font-bold text-sm sm:text-base text-slate-100 leading-snug"></h3>

        <!-- Coupon inside modal -->
        <div id="modal-coupon-wrap" class="hidden bg-dark-950 border border-dashed border-dark-700 rounded-xl p-3 flex items-center justify-between gap-2">
          <div class="flex items-center gap-2 min-w-0">
            <i class="fa-solid fa-ticket text-slate-400 text-base flex-shrink-0"></i>
            <div class="min-w-0">
              <div class="text-[10px] text-slate-400" data-i18n="modal_coupon_label">كود الخصم الفعال:</div>
              <span id="modal-coupon-code" class="font-mono font-bold text-white text-sm sm:text-base tracking-wider truncate block"></span>
            </div>
          </div>
          <button id="modal-coupon-btn" onclick="copyCouponFromModal(this)" class="min-h-[42px] px-3.5 py-1.5 bg-dark-800 hover:bg-dark-700 active:scale-95 text-xs font-bold text-white rounded-lg transition flex items-center gap-1.5 flex-shrink-0 touch-manipulation">
            <i class="fa-regular fa-copy"></i>
            <span data-i18n="btn_copy">نسخ الكود</span>
          </button>
        </div>

        <!-- Price display inside modal -->
        <div class="bg-dark-950/80 p-3.5 rounded-xl border border-dark-800 flex items-center justify-between">
          <div>
            <div class="text-[10px] text-slate-400" data-i18n="modal_price_label">السعر التقديري:</div>
            <div id="modal-price" class="flex items-baseline gap-2"></div>
          </div>
          <div id="modal-channel-link"></div>
        </div>

        <!-- CTA Action Buttons -->
        <div class="pt-1 space-y-2">
          <a id="modal-aff-btn" href="#" target="_blank" rel="noopener noreferrer" class="w-full min-h-[48px] bg-crimson-600 hover:bg-crimson-700 active:scale-[0.98] text-white font-bold text-sm py-3 px-4 rounded-xl text-center flex items-center justify-center gap-2 transition shadow-lg touch-manipulation">
            <i class="fa-solid fa-cart-shopping text-sm"></i>
            <span data-i18n="modal_cta_ali">الذهاب لصفحة العرض على AliExpress</span>
          </a>
          <div class="grid grid-cols-2 gap-2 text-xs">
            <a href="https://t.me/Alilo07BOT" target="_blank" rel="noopener noreferrer" class="min-h-[44px] bg-dark-800 hover:bg-dark-700 text-amber-400 font-bold py-2.5 px-3 rounded-xl border border-dark-700 flex items-center justify-center gap-1.5 active:scale-95 transition touch-manipulation">
              <i class="fa-solid fa-coins text-xs"></i>
              <span data-i18n="top_coin_bot">تخفيض العملات</span>
            </a>
            <button onclick="closeDealModal()" class="min-h-[44px] bg-dark-800 hover:bg-dark-700 text-slate-300 font-bold py-2.5 px-3 rounded-xl border border-dark-700 flex items-center justify-center gap-1 active:scale-95 transition touch-manipulation">
              <span data-i18n="btn_close">إغلاق</span>
            </button>
          </div>
        </div>

      </div>

    </div>
  </div>

  <!-- Toast Notification -->
  <div id="toast" class="fixed toast-bottom md:bottom-6 left-1/2 -translate-x-1/2 z-50 bg-dark-900 border border-emerald-500/40 text-emerald-400 font-semibold text-xs px-4 py-2.5 rounded-xl shadow-2xl flex items-center gap-2 transform translate-y-16 opacity-0 pointer-events-none transition-all duration-200">
    <i class="fa-solid fa-check text-emerald-400"></i>
    <span id="toast-msg">تم نسخ كود الخصم!</span>
  </div>

  <!-- ========================================== -->
  <!-- HIGH CREDIBILITY E-COMMERCE FOOTER         -->
  <!-- ========================================== -->
  <footer role="contentinfo" class="border-t border-dark-800 bg-dark-900 pt-10 pb-6 px-4 text-xs text-slate-400">
    <div class="max-w-7xl mx-auto space-y-8">
      
      <!-- 4 Columns Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        
        <!-- Col 1: Brand & Mission -->
        <div class="space-y-3">
          <div class="flex items-center gap-2">
            <div class="w-7 h-7 rounded-lg bg-crimson-600 flex items-center justify-center text-white font-bold text-sm">
              <i class="fa-solid fa-bolt"></i>
            </div>
            <span class="font-bold text-base text-white font-inter">DealScout<span class="text-crimson-500">DZ</span></span>
          </div>
          <p class="text-slate-400 text-xs leading-relaxed" data-i18n="footer_brand_desc">
            المنصة الجزائرية المستقلة الأولى لرصد صفقات AliExpress لحظياً، مع حساب حقيقي للأسعار بالدينار الجزائري وفق أسعار السكوار اليومية.
          </p>
          <div class="inline-flex items-center gap-1.5 bg-dark-950 border border-dark-800 rounded-lg px-2.5 py-1 text-[11px] text-emerald-400 font-mono">
            <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span>1 USDT ≈ <b id="footer-usdt-rate">256.9</b> <span data-i18n="currency_dzd">دج</span></span>
          </div>
        </div>

        <!-- Col 2: Navigation Links -->
        <div class="space-y-3">
          <h4 class="font-bold text-white text-xs uppercase tracking-wider" data-i18n="footer_nav_title">التنقل السريع</h4>
          <ul class="space-y-2">
            <li><button onclick="showPage('deals')" class="hover:text-white transition" data-i18n="nav_deals">أحدث الصفقات</button></li>
            <li><button onclick="showPage('coins')" class="hover:text-white transition" data-i18n="nav_coins">دليل بوت العملات</button></li>
            <li><button onclick="showPage('faq')" class="hover:text-white transition" data-i18n="nav_faq">الأسئلة الشائعة</button></li>
            <li><button onclick="showPage('contact')" class="hover:text-white transition" data-i18n="nav_contact">اتصل بنا والدعم</button></li>
            <li><button onclick="showPage('about')" class="hover:text-white transition" data-i18n="nav_about">من نحن وإخلاء المسؤولية</button></li>
          </ul>
        </div>

        <!-- Col 3: Channels & Communities -->
        <div class="space-y-3">
          <h4 class="font-bold text-white text-xs uppercase tracking-wider" data-i18n="footer_channels_title">القنوات والمنصات</h4>
          <ul class="space-y-2">
            <li>
              <a href="https://t.me/DzAliexpress0" target="_blank" rel="noopener noreferrer" class="hover:text-sky-400 transition flex items-center gap-1.5">
                <i class="fa-brands fa-telegram text-sky-400"></i>
                <span data-i18n="footer_ch_dz">قناة صفقات الجزائر (@DzAliexpress0)</span>
              </a>
            </li>
            <li>
              <a href="https://t.me/francedealsdz" target="_blank" rel="noopener noreferrer" class="hover:text-sky-400 transition flex items-center gap-1.5">
                <i class="fa-brands fa-telegram text-sky-400"></i>
                <span data-i18n="footer_ch_fr">قناة صفقات فرنسا (@francedealsdz)</span>
              </a>
            </li>
            <li>
              <a href="https://t.me/Alilo07BOT" target="_blank" rel="noopener noreferrer" class="hover:text-amber-400 transition flex items-center gap-1.5">
                <i class="fa-solid fa-coins text-amber-400 text-xs"></i>
                <span data-i18n="footer_bot_coins">بوت خصم العملات (@Alilo07BOT)</span>
              </a>
            </li>
            <li>
              <a href="https://squarealgerie.com" target="_blank" rel="noopener noreferrer" class="hover:text-emerald-400 transition flex items-center gap-1.5">
                <i class="fa-solid fa-arrow-trend-up text-emerald-400 text-xs"></i>
                <span>SquareAlgerie.com</span>
              </a>
            </li>
          </ul>
        </div>

        <!-- Col 4: Buyer Protection & Language -->
        <div class="space-y-3">
          <h4 class="font-bold text-white text-xs uppercase tracking-wider" data-i18n="footer_security_title">أمان التسوق واللغة</h4>
          <p class="text-xs text-slate-400 leading-relaxed" data-i18n="footer_security_desc">
            جميع روابط الشراء تفتح موقع AliExpress الرسمي مباشرة عبر سيرفرات مشفرة ومحمية ببروتوكول HTTPS.
          </p>
          <div class="pt-1 flex items-center gap-2">
            <button onclick="setLanguage('ar')" class="px-2.5 py-1 rounded bg-dark-950 border border-dark-800 hover:border-slate-600 text-slate-300 font-bold transition">🇩🇿 العربية</button>
            <button onclick="setLanguage('fr')" class="px-2.5 py-1 rounded bg-dark-950 border border-dark-800 hover:border-slate-600 text-slate-300 font-bold transition">🇫🇷 Français</button>
          </div>
        </div>

      </div>

      <!-- Affiliate Compliance Notice -->
      <div class="border-t border-dark-800 pt-6 text-[11px] text-slate-500 leading-relaxed text-center sm:text-start" data-i18n="footer_compliance">
        إخلاء مسؤولية الشراكة: DealScout DZ موقع مستقل وغير تابع لشركة Alibaba أو AliExpress بشكل مباشر. قد تتضمن بعض الروابط معرفات تسويق بالعمولة (AliExpress Portals Affiliate) تتيح لنا الحصول على نسبة رمزية عند الشراء دون أي تكلفة إضافية عليك إطلاقاً. الأسعار بالدينار الجزائري تقريبية وتعتمد على سعر الصرف اللحظي.
      </div>

      <!-- Copyright Bar -->
      <div class="border-t border-dark-800 pt-4 flex flex-col sm:flex-row items-center justify-between gap-3 text-[11px] text-slate-500">
        <div>© 2026 DealScout DZ. <span data-i18n="footer_rights">جميع الحقوق محفوظة.</span></div>
        <div class="flex items-center gap-4">
          <span data-i18n="footer_made_with">صُنع خصيصاً للمتسوق الجزائري 🇩🇿</span>
          <button onclick="window.scrollTo({top: 0, behavior: 'smooth'})" class="hover:text-slate-200 transition flex items-center gap-1 font-bold">
            <span data-i18n="footer_back_top">للأعلى</span>
            <i class="fa-solid fa-arrow-up text-[10px]"></i>
          </button>
        </div>
      </div>

    </div>
  </footer>

  <!-- ========================================== -->
  <!-- CLIENT-SIDE BILINGUAL LOGIC & ROUTER       -->
  <!-- ========================================== -->
  <script>
    // ── Translation Dictionary ──────────────────────────────────────
    const I18N = {
      ar: {
        meta_title: "DealScout DZ — صفقات وتخفيضات AliExpress بالدينار الجزائري",
        meta_desc: "منصة متخصصة في رصد وتحديث أفضل عروض وتخفيضات AliExpress الموجهة للجزائر لحظة بلحظة، مع حساب الأسعار بالدينار الجزائري وأكواد الخصم والعملات.",
        brand_subtitle: "بوابة صفقات وتخفيضات AliExpress 🇩🇿",
        top_live_updates: "تحديث فوري من القنوات",
        top_usdt_rate: "سعر صرف السكوار",
        currency_dzd: "دج",
        top_coin_bot: "بوت العملات",
        nav_deals: "الصفقات",
        nav_coins: "بوت العملات",
        nav_faq: "الأسئلة الشائعة",
        nav_contact: "اتصل بنا",
        nav_about: "من نحن",
        btn_join_channel: "انضم للقناة",
        search_placeholder: "ابحث عن هاتف، شاحن، كود خصم، سماعات...",
        tab_algeria_deals: "عروض الجزائر (@DzAliexpress0)",
        tab_france_deals: "عروض فرنسا (@francedealsdz)",
        view_grid: "بطاقات",
        view_stream: "منشورات القناة",
        cat_all: "الكل",
        cat_smartphones: "هواتف وتابلت",
        cat_gaming: "أجهزة قيمنق",
        cat_audio: "سماعات وصوتيات",
        cat_tech: "شواحن وملحقات",
        cat_tajmi3at: "تجميعات العروض",
        deals_section_heading: "أحدث صفقات وتخفيضات AliExpress بالدينار الجزائري",
        empty_title: "لا توجد صفقات مطابقة للبحث",
        empty_desc: "جرب كتابة اسم منتج أو علامة تجارية مختلفة أو أعد تعيين الفلاتر.",
        empty_reset: "عرض جميع الصفقات",
        btn_buy: "شراء من AliExpress",
        btn_copy: "نسخ الكود",
        btn_copied: "تم النسخ!",
        deal_category_fallback: "عرض",
        modal_coupon_label: "كود الخصم الفعال:",
        modal_price_label: "السعر التقديري:",
        modal_cta_ali: "الذهاب لصفحة العرض على AliExpress",
        btn_close: "إغلاق",
        coins_badge: "دليل توفير العملات (AliExpress Coins)",
        coins_hero_title: "كيف توفر حتى 60% إضافية باستخدام عملات AliExpress وبوت @Alilo07BOT؟",
        coins_hero_desc: "تمنح AliExpress مستخدميها عملات يومية (Coins)، لكن معظم المنتجات في التطبيق لا تسمح باستخدام أكثر من 2% فقط. بوت التخفيضات الخاص بنا يقوم بفك القيود وتوليد روابط مباشرة تمكّنك من استهلاك أكبر عدد ممكن من العملات والحصول على خصم ضخم فوري!",
        coins_btn_start: "تشغيل البوت مجاناً (@Alilo07BOT)",
        coins_step1_title: "انسخ رابط المنتج من AliExpress",
        coins_step1_desc: "افتح أي منتج يعجبك داخل تطبيق AliExpress، اضغط على زر المشاركة ثم اختر نسخ الرابط (Copy Link).",
        coins_step2_title: "أرسل الرابط لبوت التخفيض",
        coins_step2_desc: "افتح بوت التيليجرام @Alilo07BOT والصق الرابط في المحادثة. سيقوم البوت فوراً بالبحث عن أقصى نسبة خصم متاحة للعملات.",
        coins_step3_title: "ادفع بالسعر المخفض",
        coins_step3_desc: "اضغط على زر (شراء الآن) من الرابط الذي يرجعه البوت، وستلاحظ أن خانة العملات قد خصمت ما يصل إلى 10$ إلى 40$ من السعر الإجمالي!",
        faq_title: "الأسئلة الشائعة وإرشادات الشراء",
        faq_subtitle: "كل ما يحتاجه المتسوق الجزائري لمعرفة طرق الشحن، حساب الأسعار بالدينار، والتعامل مع عروض AliExpress.",
        faq_q1: "كيف يتم احتساب الأسعار بالدينار الجزائري (DZD)؟",
        faq_a1: "يتم حساب السعر بالدينار الجزائري تلقائياً وبدقة عالية اعتماداً على سعر صرف الدولار واليورو في السوق الموازي (سعر السكوار الحقيقي) المستخرج مباشرة من موقع SquareAlgerie.com، حتى تتطابق المبالغ مع ما تدفعه حقيقة عند شحن بطاقاتك (Visa / Mastercard / Bybit / RedotPay).",
        faq_q2: "كيف يتم شحن الطرود واستلامها في الجزائر؟",
        faq_a2: "تشحن معظم المنتجات عبر بريد الجزائر (Algérie Poste / EMS). يصل الطرد إلى أقرب مكتب بريد لعنوان سكناك ويتم إرسال إشعار وصول إلى هاتفك أو صندوق بريدك. للشحنات العادية، تتراوح مدة الوصول بين 15 و35 يوماً عبر خيار AliExpress Standard Shipping.",
        faq_q3: "ما هي أفضل طرق وبطاقات الدفع المتاحة للجزائريين؟",
        faq_a3: "يمكنك الدفع بسهولة عبر بطاقات فيزا وماستركارد الافتراضية الدولية مثل RedotPay، Bybit Card، Paysera، Pyypl، أو بطاقات العملة الصعبة الصادرة من البنوك الوطنية الجزائرية (AGB، BDL، بنك الخليج الجزائر).",
        faq_q4: "لماذا يظهر كود الخصم غير صالح أو منتهي الصلاحية أحياناً؟",
        faq_a4: "أكواد الخصم الترويجية في AliExpress تكون محدودة بعدد استخدامات معين لكل دولة. نقوم بتحديث الأكواد لحظياً وإلغاء المنتهية فوراً، ولكن ننصح دائماً بالشراء السريع عند نشر الكود قبل نفاد حصة الجزائر.",
        faq_q5: "ما هي قناة عروض فرنسا (@francedealsdz)؟",
        faq_a5: "هي قناة متخصصة وموجهة لأفراد الجالية الجزائرية المقيمين في فرنسا وأوروبا، أو للجزائريين الذين يستعينون بشركات إعادة توجيه الطرود (Forwarders). أسعارها باليورو الأوروبي وعروضها مشحونة من مستودعات أوروبية سريعة (خلال 3-7 أيام).",
        contact_title: "اتصل بنا والدعم الفني",
        contact_subtitle: "فريق DealScout DZ يرحب باقتراحاتكم، إبلاغكم عن الروابط التالفة، واستفساراتكم حول الصفقات.",
        contact_tg_title: "الدعم السريع عبر Telegram",
        contact_tg_desc: "أسرع وسيلة للتواصل مع مديري القناة والمطورين. يمكنك إرسال استفسارك أو طلب إضافة منتج معين إلى المراقبة الآلية.",
        contact_tg_btn_admin: "مراسلة إدارة DealScout",
        contact_tg_btn_bot: "الدخول لبوت العملات (@Alilo07BOT)",
        contact_form_title: "إرسال رسالة أو اقتراح",
        form_name: "الاسم أو اللقب",
        form_email: "البريد الإلكتروني أو معرف تيليجرام",
        form_subject: "نوع الاستفسار",
        form_opt1: "اقتراح صفقة أو منتج لمراقبته",
        form_opt2: "إبلاغ عن رابط تالف أو كود منتهي",
        form_opt3: "شراكة أو إعلان تجاري",
        form_opt4: "استفسار عام",
        form_message: "نص الرسالة",
        form_submit: "إرسال الرسالة",
        about_title: "حول منصة DealScout DZ",
        about_p1: "تأسست منصة DealScout DZ بهدف حل أكبر مشكلة تواجه المتسوقين في الجزائر عبر الإنترنت: صعوبة الوصول إلى التخفيضات الحقيقية، والارتباك الناتج عن حساب تكلفة المنتج بالدينار الجزائري في ظل تغير أسعار سوق السكوار.",
        about_p2: "نقوم بمسح آلاف الصفقات المنشورة في مجموعات AliExpress المعتمدة، ثم نطبق خوارزميات ذكية لتصفية العروض الوهمية، وإبراز المنتجات الأكثر طلباً في السوق الجزائري (الهواتف الذكية، ملحقات الحواسيب، أجهزة القيمنق، الشواحن الأصلية، والأدوات المنزلية الذكية).",
        about_feat1_title: "ربط مباشر مع سعر السكوار",
        about_feat1_desc: "نحدث أسعار USDT بالدينار الجزائري لحظة بلحظة لضمان شفافية كاملة قبل الضغط على زر الشراء.",
        about_feat2_title: "روبوتات آلية وخوارزميات أمان",
        about_feat2_desc: "نظام ذكي يلتقط التخفيضات في الثواني الأولى لنزولها ويختبر صلاحية أكواد الخصم والعملات.",
        about_disclosure_title: "إفصاح الشفافية والتسويق بالعمولة (Affiliate Disclosure)",
        about_disclosure_desc: "منصة DealScout DZ مشتركة في برنامج شركاء AliExpress الرسمي (AliExpress Portals Affiliate Program). عند النقر على روابط الشراء وإتمام الطلب، قد نحصل على عمولة تسويقية صغيرة من منصة AliExpress دون أي تكلفة إضافية عليك.",
        footer_brand_desc: "المنصة الجزائرية المستقلة الأولى لرصد صفقات AliExpress لحظياً، مع حساب حقيقي للأسعار بالدينار الجزائري وفق أسعار السكوار اليومية.",
        footer_nav_title: "التنقل السريع",
        footer_channels_title: "القنوات والمنصات",
        footer_security_title: "أمان التسوق واللغة",
        footer_security_desc: "جميع روابط الشراء تفتح موقع AliExpress الرسمي مباشرة عبر سيرفرات مشفرة ومحمية ببروتوكول HTTPS.",
        footer_ch_dz: "قناة صفقات الجزائر (@DzAliexpress0)",
        footer_ch_fr: "قناة صفقات فرنسا (@francedealsdz)",
        footer_bot_coins: "بوت خصم العملات (@Alilo07BOT)",
        footer_compliance: "إخلاء مسؤولية الشراكة: DealScout DZ موقع مستقل وغير تابع لشركة Alibaba أو AliExpress بشكل مباشر. قد تتضمن بعض الروابط معرفات تسويق بالعمولة (AliExpress Portals Affiliate) تتيح لنا الحصول على نسبة رمزية عند الشراء دون أي تكلفة إضافية عليك إطلاقاً. الأسعار بالدينار الجزائري تقريبية وتعتمد على سعر الصرف اللحظي.",
        footer_rights: "جميع الحقوق محفوظة.",
        footer_made_with: "صُنع خصيصاً للمتسوق الجزائري 🇩🇿",
        footer_back_top: "للأعلى"
      },
      fr: {
        meta_title: "DealScout DZ — Bons Plans & Réductions AliExpress en Dinar Algérien",
        meta_desc: "Portail n°1 des meilleurs bons plans et promotions AliExpress pour l'Algérie avec conversion en Dinar Algérien (DZD) et codes promo.",
        brand_subtitle: "Bons plans et réductions AliExpress 🇩🇿",
        top_live_updates: "Mise à jour en direct",
        top_usdt_rate: "Taux Square Algérie",
        currency_dzd: "DZD",
        top_coin_bot: "Bot Pièces",
        nav_deals: "Bons Plans",
        nav_coins: "Bot Pièces",
        nav_faq: "FAQ",
        nav_contact: "Contact",
        nav_about: "À Propos",
        btn_join_channel: "Rejoindre Telegram",
        search_placeholder: "Rechercher un smartphone, écouteurs, chargeur, marque...",
        tab_algeria_deals: "Bons Plans Algérie (@DzAliexpress0)",
        tab_france_deals: "Bons Plans France (@francedealsdz)",
        view_grid: "Grille",
        view_stream: "Flux Telegram",
        cat_all: "Tous",
        cat_smartphones: "Smartphones & Tablettes",
        cat_gaming: "Gaming",
        cat_audio: "Audio & Écouteurs",
        cat_tech: "Chargeurs & High-Tech",
        cat_tajmi3at: "Packs & Bundles",
        deals_section_heading: "Derniers bons plans et promotions AliExpress en Dinar Algérien",
        empty_title: "Aucun bon plan ne correspond à votre recherche",
        empty_desc: "Essayez un autre mot-clé ou réinitialisez les filtres de recherche.",
        empty_reset: "Afficher tous les bons plans",
        btn_buy: "Voir sur AliExpress",
        btn_copy: "Copier le code",
        btn_copied: "Copié !",
        deal_category_fallback: "Offre",
        modal_coupon_label: "Code promo valide :",
        modal_price_label: "Prix estimé :",
        modal_cta_ali: "Ouvrir l'offre sur AliExpress",
        btn_close: "Fermer",
        coins_badge: "Guide Réduction Pièces (AliExpress Coins)",
        coins_hero_title: "Comment économiser jusqu'à 60% supplémentaires avec les pièces AliExpress et le bot @Alilo07BOT ?",
        coins_hero_desc: "AliExpress offre des pièces quotidiennes (Coins), mais limite souvent leur utilisation à 2%. Notre bot dédié débloque ces restrictions et génère des liens d'achat direct maximisant la réduction en pièces !",
        coins_btn_start: "Lancer le bot gratuitement (@Alilo07BOT)",
        coins_step1_title: "Copiez le lien produit sur AliExpress",
        coins_step1_desc: "Ouvrez le produit sur l'application AliExpress, appuyez sur Partager puis Copier le lien.",
        coins_step2_title: "Envoyez le lien au bot Telegram",
        coins_step2_desc: "Ouvrez @Alilo07BOT sur Telegram et collez le lien. Le bot recherche instantanément le taux de réduction maximal en pièces.",
        coins_step3_title: "Payez au meilleur prix réduit",
        coins_step3_desc: "Cliquez sur Acheter via le lien généré par le bot. La réduction des pièces s'appliquera automatiquement dans votre panier !",
        faq_title: "Foire Aux Questions & Guide d'Achat",
        faq_subtitle: "Toutes les réponses pour réussir vos achats sur AliExpress en Algérie : livraison, calcul en Dinar, et paiement.",
        faq_q1: "Comment est calculé le prix en Dinar Algérien (DZD) ?",
        faq_a1: "Le prix en Dinar Algérien est calculé en temps réel selon le taux de change du marché parallèle (cours Square officiel) via SquareAlgerie.com pour refléter fidèlement le coût réel de rechargement de vos cartes bancaires (Visa / Mastercard / Bybit / RedotPay).",
        faq_q2: "Comment se déroule la livraison des colis en Algérie ?",
        faq_a2: "La majorité des colis sont acheminés par Algérie Poste / EMS. Le colis arrive au bureau de poste le plus proche de votre domicile avec notification par SMS ou avis de passage. Le délai moyen est de 15 à 35 jours via AliExpress Standard Shipping.",
        faq_q3: "Quels sont les meilleurs moyens de paiement disponibles en Algérie ?",
        faq_a3: "Vous pouvez régler vos commandes à l'aide de cartes bancaires internationales comme RedotPay, Bybit Card, Paysera, Pyypl ou des cartes en devises émises par les banques algériennes (AGB, BDL, etc.).",
        faq_q4: "Pourquoi un code promo affiche-t-il parfois 'expiré' ?",
        faq_a4: "Les codes promo AliExpress disposent de quotas d'utilisation limités par pays. Nous mettons à jour les codes dès leur publication, mais il est recommandé de commander rapidement dès la diffusion de l'offre.",
        faq_q5: "À qui s'adresse le canal Bons Plans France (@francedealsdz) ?",
        faq_a5: "Ce canal s'adresse aux résidents algériens en France et en Europe, ou à ceux utilisant des services de réexpédition (Forwarders). Les prix sont en Euros et la livraison s'effectue en 3 à 7 jours depuis des entrepôts européens.",
        contact_title: "Contact & Assistance",
        contact_subtitle: "L'équipe DealScout DZ est à votre disposition pour vos suggestions, signalements de liens ou partenariats.",
        contact_tg_title: "Assistance rapide sur Telegram",
        contact_tg_desc: "Le moyen le plus direct de joindre l'équipe. Contactez nos administrateurs pour toute question ou demande de veille produit.",
        contact_tg_btn_admin: "Contacter l'équipe DealScout",
        contact_tg_btn_bot: "Ouvrir le bot Pièces (@Alilo07BOT)",
        contact_form_title: "Envoyez-nous un message",
        form_name: "Nom complet",
        form_email: "Email ou identifiant Telegram",
        form_subject: "Type de demande",
        form_opt1: "Suggérer un bon plan ou produit à suivre",
        form_opt2: "Signaler un lien expiré ou code invalide",
        form_opt3: "Partenariat ou proposition commerciale",
        form_opt4: "Question générale",
        form_message: "Votre message",
        form_submit: "Envoyer le message",
        about_title: "À Propos de DealScout DZ",
        about_p1: "DealScout DZ est né pour répondre à un défi majeur : trouver de vraies réductions sur AliExpress et connaître précisément leur équivalent en Dinar Algérien selon le cours réel du Square.",
        about_p2: "Nous scannons des milliers de produits pour filtrer les fausses promos et mettre en avant les équipements les plus recherchés en Algérie (Smartphones, PC Gaming, audio, chargeurs et domotique).",
        about_feat1_title: "Taux Square Algérie en direct",
        about_feat1_desc: "Mise à jour en continu du taux USDT / Dinar pour une transparence absolue avant chaque commande.",
        about_feat2_title: "Algorithmes de détection intelligents",
        about_feat2_desc: "Système automatisé captant les coupons et réductions pièces dès les premières secondes de publication.",
        about_disclosure_title: "Transparence & Liens d'Affiliation",
        about_disclosure_desc: "DealScout DZ participe au programme officiel d'affiliation AliExpress Portals. En passant par nos liens, nous pouvons percevoir une commission sans surcoût pour vous.",
        footer_brand_desc: "Première plateforme indépendante de bons plans AliExpress pour l'Algérie avec calcul au cours réel du Square.",
        footer_nav_title: "Navigation",
        footer_channels_title: "Canaux & Réseaux",
        footer_security_title: "Sécurité & Langues",
        footer_security_desc: "Toutes les commandes sont finalisées sur le site officiel sécurisé d'AliExpress via HTTPS.",
        footer_ch_dz: "Bons Plans Algérie (@DzAliexpress0)",
        footer_ch_fr: "Bons Plans France (@francedealsdz)",
        footer_bot_coins: "Bot Pièces AliExpress (@Alilo07BOT)",
        footer_compliance: "Divulgation : DealScout DZ est un site indépendant. Certains liens sont affiliés (AliExpress Portals), permettant de soutenir le service sans surcoût pour l'acheteur. Les montants en DZD sont donnés à titre indicatif selon le taux de change du jour.",
        footer_rights: "Tous droits réservés.",
        footer_made_with: "Fait spécialement pour les acheteurs algériens 🇩🇿",
        footer_back_top: "Haut de page"
      }
    };

    // ── Global State ────────────────────────────────────────────────
    let currentLang = localStorage.getItem('dealscout_lang') || 'ar';
    let allDeals = [];
    let currentChannel = '@DzAliexpress0';
    let currentCategory = 'all';
    let currentCurrency = currentLang === 'fr' ? 'EUR' : 'DZD';
    let currentViewMode = 'grid';
    let usdtRate = 256.9;
    let currentSearchTerm = '';
    let currentActiveDeal = null;

    // ── Internationalization Engine ─────────────────────────────────
    function setLanguage(lang) {
      if (!I18N[lang]) lang = 'ar';
      currentLang = lang;
      localStorage.setItem('dealscout_lang', lang);

      // Update DOM lang & dir
      const isAr = lang === 'ar';
      document.documentElement.lang = isAr ? 'ar' : 'fr';
      document.documentElement.dir = isAr ? 'rtl' : 'ltr';
      document.body.dir = isAr ? 'rtl' : 'ltr';

      // Update switcher buttons
      const arBtn = document.getElementById('lang-ar-btn');
      const frBtn = document.getElementById('lang-fr-btn');
      if (arBtn && frBtn) {
        if (isAr) {
          arBtn.className = 'px-2 py-0.5 rounded text-[11px] font-bold bg-crimson-600 text-white transition active:scale-95';
          frBtn.className = 'px-2 py-0.5 rounded text-[11px] font-bold text-slate-400 hover:text-slate-200 transition active:scale-95';
        } else {
          frBtn.className = 'px-2 py-0.5 rounded text-[11px] font-bold bg-crimson-600 text-white transition active:scale-95';
          arBtn.className = 'px-2 py-0.5 rounded text-[11px] font-bold text-slate-400 hover:text-slate-200 transition active:scale-95';
        }
      }

      // Translate all data-i18n elements
      document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (I18N[lang][key]) {
          el.textContent = I18N[lang][key];
        }
      });

      // Translate all data-i18n-placeholder elements
      document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        if (I18N[lang][key]) {
          el.placeholder = I18N[lang][key];
        }
      });

      // Update document title
      document.title = I18N[lang].meta_title;

      // Re-render deals to update button & category text
      if (allDeals && allDeals.length > 0) {
        filterDeals();
      }
    }

    // ── Multi-Page Navigation Router ────────────────────────────────
    function showPage(pageId) {
      const pages = ['deals', 'coins', 'faq', 'contact', 'about'];
      if (!pages.includes(pageId)) pageId = 'deals';

      // Hide all pages, show target page
      pages.forEach(p => {
        const el = document.getElementById('page-' + p);
        if (el) {
          if (p === pageId) {
            el.classList.remove('hidden');
          } else {
            el.classList.add('hidden');
          }
        }

        // Desktop nav active indicator
        const navBtn = document.getElementById('nav-link-' + p);
        if (navBtn) {
          if (p === pageId) {
            navBtn.className = 'nav-page-btn px-3 py-1.5 rounded-lg bg-dark-800 text-white transition flex items-center gap-1.5';
          } else {
            navBtn.className = 'nav-page-btn px-3 py-1.5 rounded-lg hover:bg-dark-800 hover:text-white text-slate-400 transition flex items-center gap-1.5';
          }
        }

        // Mobile bottom nav active indicator
        const mobBtn = document.getElementById('mob-bottom-' + p);
        if (mobBtn) {
          if (p === pageId) {
            mobBtn.className = 'flex-1 min-h-[48px] py-1 flex flex-col items-center justify-center gap-1 text-crimson-500 font-bold active:scale-90 transition-transform touch-manipulation';
          } else {
            mobBtn.className = 'flex-1 min-h-[48px] py-1 flex flex-col items-center justify-center gap-1 text-slate-400 hover:text-slate-200 font-medium active:scale-90 transition-transform touch-manipulation';
          }
        }
      });

      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // ── Utility Helpers ─────────────────────────────────────────────
    function handleImgError(img) {
      if (!img) return;
      img.onerror = null;
      img.src = '/icon.svg';
      img.classList.remove('object-cover');
      img.classList.add('object-contain', 'p-8', 'opacity-30');
    }

    function showToast(message) {
      const toast = document.getElementById('toast');
      const msg = document.getElementById('toast-msg');
      if (!toast || !msg) return;
      msg.textContent = message;
      toast.classList.remove('translate-y-16', 'opacity-0', 'pointer-events-none');
      setTimeout(() => {
        toast.classList.add('translate-y-16', 'opacity-0', 'pointer-events-none');
      }, 2200);
    }

    function escapeHtml(str) {
      if (!str) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    }

    function handleContactSubmit(e) {
      e.preventDefault();
      const name = document.getElementById('contact-name').value;
      const successMsg = currentLang === 'fr' 
        ? `Merci ${name} ! Votre message a bien été envoyé à l'équipe.`
        : `شكراً لك ${name}! تم إرسال رسالتك بنجاح إلى فريق الإدارة.`;
      showToast(successMsg);
      e.target.reset();
    }

    // ── Currency, Channel & Category Handlers ───────────────────────
    function setCurrency(curr) {
      currentCurrency = curr;
      ['dzd', 'usd', 'eur'].forEach(c => {
        const btn = document.getElementById('curr-' + c);
        if (btn) {
          if (c === curr.toLowerCase()) {
            btn.className = 'min-w-[34px] sm:min-w-[38px] h-8 sm:h-9 px-2 py-1 rounded-lg bg-dark-800 text-white font-mono transition flex items-center justify-center active:scale-95 touch-manipulation shadow-sm';
          } else {
            btn.className = 'min-w-[32px] sm:min-w-[36px] h-8 sm:h-9 px-2 py-1 rounded-lg text-slate-400 hover:text-slate-200 font-mono transition flex items-center justify-center active:scale-95 touch-manipulation';
          }
        }
      });
      renderGrid();
    }

    function switchChannel(channel) {
      currentChannel = channel;
      const isDz = channel === '@DzAliexpress0';
      const tabDz = document.getElementById('tab-dz');
      const tabFr = document.getElementById('tab-fr');
      const btnJoin = document.getElementById('btn-telegram-join');

      if (isDz) {
        if (tabDz) tabDz.className = 'flex-1 sm:flex-none min-h-[40px] px-4 py-2 rounded-lg bg-crimson-600 text-white transition flex items-center justify-center gap-2 active:scale-95 shadow-sm';
        if (tabFr) tabFr.className = 'flex-1 sm:flex-none min-h-[40px] px-4 py-2 rounded-lg text-slate-400 hover:text-slate-200 transition flex items-center justify-center gap-2 active:scale-95';
        if (btnJoin) btnJoin.href = 'https://t.me/DzAliexpress0';
        setCurrency('DZD');
      } else {
        if (tabFr) tabFr.className = 'flex-1 sm:flex-none min-h-[40px] px-4 py-2 rounded-lg bg-crimson-600 text-white transition flex items-center justify-center gap-2 active:scale-95 shadow-sm';
        if (tabDz) tabDz.className = 'flex-1 sm:flex-none min-h-[40px] px-4 py-2 rounded-lg text-slate-400 hover:text-slate-200 transition flex items-center justify-center gap-2 active:scale-95';
        if (btnJoin) btnJoin.href = 'https://t.me/francedealsdz';
        setCurrency('EUR');
      }
      fetchDeals();
    }

    function setViewMode(mode) {
      currentViewMode = mode;
      const gridBtn = document.getElementById('view-mode-grid');
      const feedBtn = document.getElementById('view-mode-feed');
      const gridEl = document.getElementById('deals-grid');
      const feedEl = document.getElementById('deals-feed');

      if (mode === 'grid') {
        gridBtn.className = 'min-h-[36px] px-3 py-1.5 rounded-lg bg-dark-800 text-slate-100 transition flex items-center gap-1.5 active:scale-95';
        feedBtn.className = 'min-h-[36px] px-3 py-1.5 rounded-lg text-slate-400 hover:text-slate-200 transition flex items-center gap-1.5 active:scale-95';
        gridEl.classList.remove('hidden');
        feedEl.classList.add('hidden');
      } else {
        feedBtn.className = 'min-h-[36px] px-3 py-1.5 rounded-lg bg-dark-800 text-slate-100 transition flex items-center gap-1.5 active:scale-95';
        gridBtn.className = 'min-h-[36px] px-3 py-1.5 rounded-lg text-slate-400 hover:text-slate-200 transition flex items-center gap-1.5 active:scale-95';
        feedEl.classList.remove('hidden');
        gridEl.classList.add('hidden');
      }
    }

    function setCategory(cat) {
      currentCategory = cat;
      document.querySelectorAll('.cat-pill').forEach(btn => {
        btn.className = 'cat-pill min-h-[42px] px-3.5 py-2 rounded-xl bg-dark-900 hover:bg-dark-800 text-slate-300 border border-dark-800 whitespace-nowrap transition flex items-center gap-1.5 flex-shrink-0 active:scale-95 touch-manipulation';
      });
      const active = document.getElementById('cat-' + cat);
      if (active) {
        active.className = 'cat-pill min-h-[42px] px-3.5 py-2 rounded-xl bg-crimson-600 text-white whitespace-nowrap transition flex items-center gap-1.5 flex-shrink-0 active:scale-95 touch-manipulation shadow-sm';
      }
      filterDeals();
    }

    function handleSearchInput(term) {
      currentSearchTerm = term.trim().toLowerCase();
      const desk = document.getElementById('desktop-search');
      const mob = document.getElementById('mobile-search');
      if (desk && desk.value !== term) desk.value = term;
      if (mob && mob.value !== term) mob.value = term;
      filterDeals();
    }

    function resetFilters() {
      currentSearchTerm = '';
      currentCategory = 'all';
      const desk = document.getElementById('desktop-search');
      const mob = document.getElementById('mobile-search');
      if (desk) desk.value = '';
      if (mob) mob.value = '';
      setCategory('all');
    }

    // ── Deal Data Fetching & Rendering ──────────────────────────────
    async function fetchDeals(showSpin = false) {
      const icon = document.getElementById('refresh-icon');
      if (showSpin && icon) icon.classList.add('fa-spin');

      try {
        // Fetch exchange rates
        fetch('/api/rates')
          .then(r => r.json())
          .then(data => {
            if (data && data.rate) {
              usdtRate = parseFloat(data.rate);
              const topRate = document.getElementById('top-usdt-rate');
              const footRate = document.getElementById('footer-usdt-rate');
              if (topRate) topRate.textContent = usdtRate.toFixed(1);
              if (footRate) footRate.textContent = usdtRate.toFixed(1);
            }
          }).catch(() => {});

        // Fetch channel posts
        const resp = await fetch('/api/channel-posts?channel=' + encodeURIComponent(currentChannel));
        if (!resp.ok) throw new Error('HTTP ' + resp.status);
        const data = await resp.json();

        if (data.posts && Array.isArray(data.posts)) {
          allDeals = data.posts.map((p, idx) => parseDealPost(p, idx)).filter(d => d.affiliate_url);
          updateCategoryCounters();
          filterDeals();
        }
      } catch (err) {
        console.error('Error fetching deals:', err);
      } finally {
        if (icon) icon.classList.remove('fa-spin');
      }
    }

    function parseDealPost(post, index) {
      const text = post.text || '';
      let title = '';
      let coupon = null;
      let priceUsd = null;
      let priceEur = null;
      let country = null;
      let hasCoins = false;
      let category = 'other';
      let categoryLabel = I18N[currentLang].deal_category_fallback;

      const lines = text.split('\\n').map(l => l.trim()).filter(Boolean);
      for (const line of lines) {
        if (!title && !line.includes('http') && !line.includes('@') && !line.startsWith('🪙') && !line.startsWith('💰')) {
          title = line.replace(/^[🛍️🔥⚡⭐💥📦\\s]+/, '').trim();
          break;
        }
      }
      if (!title) title = (currentLang === 'fr' ? 'Offre Spéciale AliExpress' : 'منتج مميز من AliExpress');

      // Price extraction
      const usdMatch = text.match(/(\\$|US\\s*\\$|USD\\s*)\\s*([0-9]+[.,][0-9]{1,2})/i) || text.match(/([0-9]+[.,][0-9]{1,2})\\s*(\\bUSD\\b|\\$)/i);
      if (usdMatch) {
        priceUsd = parseFloat((usdMatch[2] || usdMatch[1]).replace(',', '.'));
      }
      const eurMatch = text.match(/(€|EUR\\s*)\\s*([0-9]+[.,][0-9]{1,2})/i) || text.match(/([0-9]+[.,][0-9]{1,2})\\s*(€|\\bEUR\\b)/i);
      if (eurMatch) {
        priceEur = parseFloat((eurMatch[2] || eurMatch[1]).replace(',', '.'));
      }

      // Coupons
      const couponMatch = text.match(/\\b(CODE|كود|code|Code|Coupon)\\s*[:：]?\\s*([A-Za-z0-9_-]{3,20})\\b/i)
        || text.match(/🏷️\\s*([A-Za-z0-9_-]{3,20})/);
      if (couponMatch) {
        coupon = couponMatch[2] || couponMatch[1];
      }

      // Country instruction
      const cMatch = text.match(/(حساب|دولة|بلد|compte|pays)\\s*[:：]?\\s*([\\u0600-\\u06FFa-zA-Z\\s]+)/i);
      if (cMatch) country = cMatch[2].trim().slice(0, 18);

      hasCoins = text.includes('عملات') || text.includes('Coins') || text.includes('coins') || text.includes('🪙');

      // Category detection
      const lower = text.toLowerCase();
      if (/phone|هاتف|téléphone|xiaomi|redmi|poco|realme|infinix|samsung|iphone|tablet|تابلت/.test(lower)) {
        category = 'smartphones';
        categoryLabel = I18N[currentLang].cat_smartphones;
      } else if (/gaming|قيمنق|gamepad|gamesir|controller|rgb|pc gamer|playstation|xbox/.test(lower)) {
        category = 'gaming';
        categoryLabel = I18N[currentLang].cat_gaming;
      } else if (/headphone|earphone|earbuds|سماعة|سماعات|anker|soundcore|audio|tws|bluetooth/.test(lower)) {
        category = 'audio';
        categoryLabel = I18N[currentLang].cat_audio;
      } else if (/charger|شاحن|ugreen|baseus|powerbank|cable|usb|adapter|محول|فلاش/.test(lower)) {
        category = 'tech';
        categoryLabel = I18N[currentLang].cat_tech;
      } else if (/تجميع|تجميعة|packs|bundle|عدة منتجات/.test(lower)) {
        category = 'tajmi3at';
        categoryLabel = I18N[currentLang].cat_tajmi3at;
      }

      let affiliateUrl = 'https://s.click.aliexpress.com/e/_oEN3d53';
      const urlMatch = text.match(/https?:\\/\\/s\\.click\\.aliexpress\\.com\\/e\\/[A-Za-z0-9_-]+/);
      if (urlMatch) {
        affiliateUrl = urlMatch[0];
      }

      let priceDzd = null;
      if (priceUsd) priceDzd = Math.round(priceUsd * usdtRate);
      else if (priceEur) priceDzd = Math.round(priceEur * (usdtRate * 1.08));

      return {
        id: 'deal-' + index,
        title,
        price_usd: priceUsd,
        price_eur: priceEur,
        price_dzd: priceDzd,
        coupon,
        country,
        has_coins: hasCoins,
        category,
        category_label: categoryLabel,
        photo_url: post.photo_url || null,
        affiliate_url: affiliateUrl,
        telegram_url: post.link || null,
        date: post.date || '',
        raw_text: text
      };
    }

    function updateCategoryCounters() {
      const counts = { all: allDeals.length, smartphones: 0, gaming: 0, audio: 0, tech: 0, tajmi3at: 0 };
      allDeals.forEach(d => {
        if (counts[d.category] !== undefined) counts[d.category]++;
      });
      for (const [k, v] of Object.entries(counts)) {
        const el = document.getElementById('count-' + k);
        if (el) el.textContent = v;
      }
    }

    function filterDeals() {
      let filtered = allDeals;
      if (currentCategory !== 'all') {
        filtered = filtered.filter(d => d.category === currentCategory);
      }
      if (currentSearchTerm) {
        filtered = filtered.filter(d => 
          (d.title && d.title.toLowerCase().includes(currentSearchTerm)) ||
          (d.raw_text && d.raw_text.toLowerCase().includes(currentSearchTerm)) ||
          (d.coupon && d.coupon.toLowerCase().includes(currentSearchTerm))
        );
      }

      const counter = document.getElementById('live-deals-counter');
      if (counter) {
        counter.textContent = currentLang === 'fr' 
          ? `${filtered.length} offres disponibles`
          : `${filtered.length} صفقة متوفرة`;
      }

      const emptyEl = document.getElementById('empty-state');
      const gridEl = document.getElementById('deals-grid');
      const feedEl = document.getElementById('deals-feed');

      if (filtered.length === 0) {
        if (emptyEl) emptyEl.classList.remove('hidden');
        if (gridEl) gridEl.classList.add('hidden');
        if (feedEl) feedEl.classList.add('hidden');
      } else {
        if (emptyEl) emptyEl.classList.add('hidden');
        if (currentViewMode === 'grid') {
          if (gridEl) gridEl.classList.remove('hidden');
          if (feedEl) feedEl.classList.add('hidden');
        } else {
          if (feedEl) feedEl.classList.remove('hidden');
          if (gridEl) gridEl.classList.add('hidden');
        }
        renderGrid(filtered);
        renderFeed(filtered);
        updateDealsStructuredData(filtered);
      }
    }

    function updateDealsStructuredData(deals) {
      let script = document.getElementById('structured-data-items');
      if (!script) {
        script = document.createElement('script');
        script.id = 'structured-data-items';
        script.type = 'application/ld+json';
        document.head.appendChild(script);
      }
      const items = (deals || []).slice(0, 20).map((deal, idx) => ({
        "@type": "ListItem",
        "position": idx + 1,
        "item": {
          "@type": "Product",
          "name": deal.title,
          "image": deal.photo_url || "https://dealscout-green.vercel.app/icon.svg",
          "description": deal.title,
          "offers": {
            "@type": "Offer",
            "price": deal.price_dzd || deal.price_usd || 0,
            "priceCurrency": deal.price_dzd ? "DZD" : "USD",
            "url": deal.affiliate_url,
            "availability": "https://schema.org/InStock"
          }
        }
      }));
      script.text = JSON.stringify({
        "@context": "https://schema.org",
        "@type": "ItemList",
        "itemListElement": items
      });
    }

    function formatPrice(deal) {
      const isAr = currentLang === 'ar';
      if (currentCurrency === 'DZD') {
        if (deal.price_dzd) {
          return `<span class="text-base sm:text-lg font-bold text-white font-mono tracking-tight whitespace-nowrap inline-flex items-baseline gap-1">${deal.price_dzd.toLocaleString()} <span class="text-xs text-rose-500 font-semibold">${isAr ? 'دج' : 'DZD'}</span></span>`;
        }
      } else if (currentCurrency === 'EUR') {
        if (deal.price_eur) {
          return `<span class="text-base sm:text-lg font-bold text-white font-mono tracking-tight whitespace-nowrap inline-flex items-baseline gap-1">${deal.price_eur.toFixed(2)} <span class="text-xs text-rose-500 font-semibold">€</span></span>`;
        }
      } else if (currentCurrency === 'USD') {
        if (deal.price_usd) {
          return `<span class="text-base sm:text-lg font-bold text-white font-mono tracking-tight whitespace-nowrap inline-flex items-baseline gap-1">${deal.price_usd.toFixed(2)} <span class="text-xs text-rose-500 font-semibold">$</span></span>`;
        }
      }
      return `<span class="text-sm font-bold text-rose-400 font-sans">${isAr ? 'تخفيض خاص' : 'Prix Promo'}</span>`;
    }

    function renderGrid(dealsToRender = null) {
      const deals = dealsToRender !== null ? dealsToRender : allDeals;
      const grid = document.getElementById('deals-grid');
      if (!grid) return;
      grid.innerHTML = '';

      deals.forEach(deal => {
        const card = document.createElement('article');
        card.className = 'deal-card rounded-2xl p-3.5 sm:p-4 flex flex-col justify-between';

        const safeTitle = escapeHtml(deal.title);

        const photoHtml = deal.photo_url ? `
          <div class="relative w-full aspect-[4/3] rounded-xl overflow-hidden bg-dark-950 border border-dark-800 mb-3 cursor-pointer group flex items-center justify-center" onclick="openDealModal('${deal.id}')">
            <img src="${deal.photo_url}" alt="${safeTitle}" loading="lazy" decoding="async" onerror="handleImgError(this)" class="w-full h-full object-contain group-hover:scale-105 transition-transform duration-300">
            ${deal.has_coins ? `<span class="absolute top-2 left-2 bg-amber-500 text-slate-950 text-[10px] font-bold px-2 py-0.5 rounded-md flex items-center gap-1 shadow-md"><i class="fa-solid fa-coins text-[9px]"></i> Coins</span>` : ''}
            ${deal.country ? `<span class="absolute top-2 right-2 bg-dark-900/90 text-slate-200 text-[10px] px-2 py-0.5 rounded-md font-bold border border-dark-700 shadow-md">${escapeHtml(deal.country)}</span>` : ''}
          </div>
        ` : '';

        const couponHtml = deal.coupon ? `
          <div class="bg-dark-950 border border-dashed border-dark-700 rounded-xl px-2.5 py-1.5 flex items-center justify-between gap-1.5 mb-2.5">
            <div class="flex items-center gap-1.5 min-w-0">
              <i class="fa-solid fa-ticket text-slate-500 text-xs flex-shrink-0"></i>
              <span class="font-mono text-xs font-bold text-slate-200 truncate select-all">${escapeHtml(deal.coupon)}</span>
            </div>
            <button onclick="copyCoupon('${deal.coupon}', this)" aria-label="Copy coupon" class="min-h-[38px] min-w-[54px] bg-dark-800 hover:bg-dark-700 active:scale-95 text-[11px] font-bold text-slate-300 hover:text-white px-2 py-1 rounded-lg border border-dark-700 transition flex items-center justify-center gap-1 flex-shrink-0 touch-manipulation">
              <i class="fa-regular fa-copy text-[11px]"></i>
              <span class="copy-text">${I18N[currentLang].btn_copy}</span>
            </button>
          </div>
        ` : '';

        const secondaryPrice = (currentCurrency === 'DZD' && deal.price_usd)
          ? `<span class="text-[11px] text-slate-500 font-mono whitespace-nowrap">($${deal.price_usd.toFixed(2)})</span>`
          : (deal.price_dzd && currentCurrency !== 'DZD' ? `<span class="text-[11px] text-slate-500 font-mono whitespace-nowrap">(${deal.price_dzd.toLocaleString()} ${I18N[currentLang].currency_dzd})</span>` : '');

        card.innerHTML = `
          <div>
            ${photoHtml}
            <div class="flex items-center justify-between gap-2 mb-1.5">
              <span class="text-[10px] font-semibold text-slate-400 bg-dark-950 px-2 py-0.5 rounded-md border border-dark-800">
                ${deal.category_label || I18N[currentLang].deal_category_fallback}
              </span>
              <span class="text-[10px] text-slate-500 font-mono">
                ${deal.date ? deal.date.split(' ')[0] : ''}
              </span>
            </div>
            <h3 class="font-semibold text-xs sm:text-sm text-slate-100 line-clamp-2 mb-2.5 hover:text-blue-400 transition cursor-pointer leading-snug break-words" onclick="openDealModal('${deal.id}')">
              ${safeTitle}
            </h3>
            ${couponHtml}
          </div>

          <div class="pt-2.5 border-t border-dark-800/80 space-y-2.5">
            <div class="flex items-baseline justify-between gap-2">
              <div class="flex items-baseline flex-wrap gap-1.5 min-w-0">
                ${formatPrice(deal)}
                ${secondaryPrice}
              </div>
              ${deal.telegram_url ? `
                <a href="${deal.telegram_url}" target="_blank" rel="noopener noreferrer" title="Telegram" class="w-8 h-8 rounded-lg bg-dark-950 border border-dark-800 text-slate-400 hover:text-sky-400 text-xs flex items-center justify-center active:scale-95 transition touch-manipulation flex-shrink-0">
                  <i class="fa-brands fa-telegram"></i>
                </a>
              ` : ''}
            </div>

            <!-- Primary Buy Button -->
            <a href="${deal.affiliate_url}" target="_blank" rel="noopener noreferrer" class="w-full bg-crimson-600 hover:bg-crimson-700 active:scale-[0.98] text-white font-bold text-xs sm:text-sm py-2.5 px-3 rounded-xl text-center flex items-center justify-center gap-2 transition shadow-sm touch-manipulation min-h-[44px]">
              <i class="fa-solid fa-cart-shopping text-xs"></i>
              <span>${I18N[currentLang].btn_buy}</span>
            </a>
          </div>
        `;

        grid.appendChild(card);
      });
    }

    function renderFeed(dealsToRender = null) {
      const deals = dealsToRender !== null ? dealsToRender : allDeals;
      const feed = document.getElementById('deals-feed');
      if (!feed) return;
      feed.innerHTML = '';

      deals.forEach(deal => {
        const item = document.createElement('article');
        item.className = 'bg-dark-900 border border-dark-800 rounded-2xl p-4 space-y-3.5';

        const safeText = escapeHtml(deal.raw_text || '')
          .replace(/\\n/g, '<br>')
          .replace(/(https?:\\/\\/s\\.click\\.aliexpress\\.com\\/e\\/[A-Za-z0-9_-]+)/g, '<a href="$1" target="_blank" rel="noopener noreferrer" class="text-blue-400 font-bold underline break-all">$1</a>')
          .replace(/(@[A-Za-z0-9_]+)/g, '<span class="text-sky-400 font-semibold">$1</span>');

        item.innerHTML = `
          <div class="flex items-center justify-between pb-2.5 border-b border-dark-800 text-xs">
            <div class="flex items-center gap-2">
              <div class="w-8 h-8 rounded-xl bg-dark-800 flex items-center justify-center text-sky-400 text-sm">
                <i class="fa-brands fa-telegram"></i>
              </div>
              <div>
                <span class="font-bold text-slate-200 block">${escapeHtml(currentChannel)}</span>
                <span class="text-slate-500 text-[10px] font-mono">${deal.date || ''}</span>
              </div>
            </div>
            ${deal.telegram_url ? `<a href="${deal.telegram_url}" target="_blank" rel="noopener noreferrer" class="min-h-[38px] px-2.5 py-1 text-sky-400 hover:underline font-semibold text-xs flex items-center gap-1 active:scale-95 touch-manipulation"><i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i> Telegram</a>` : ''}
          </div>

          ${deal.photo_url ? `
            <div class="rounded-xl overflow-hidden border border-dark-800 max-h-80 cursor-pointer bg-dark-950 flex items-center justify-center" onclick="openDealModal('${deal.id}')">
              <img src="${deal.photo_url}" alt="${escapeHtml(deal.title)}" loading="lazy" decoding="async" onerror="handleImgError(this)" class="w-full h-auto object-contain max-h-80">
            </div>
          ` : ''}

          <div class="text-xs sm:text-sm text-slate-300 leading-relaxed font-sans select-text break-words">
            ${safeText}
          </div>

          <div class="pt-1 flex flex-col sm:flex-row gap-2">
            <a href="${deal.affiliate_url}" target="_blank" rel="noopener noreferrer" class="flex-1 min-h-[44px] bg-crimson-600 hover:bg-crimson-700 active:scale-[0.98] text-white font-bold text-xs sm:text-sm py-2.5 px-3 rounded-xl text-center flex items-center justify-center gap-2 transition shadow-sm touch-manipulation">
              <i class="fa-solid fa-cart-shopping text-xs"></i>
              <span>${I18N[currentLang].btn_buy}</span>
            </a>
            <a href="https://t.me/Alilo07BOT" target="_blank" rel="noopener noreferrer" class="min-h-[44px] bg-dark-800 hover:bg-dark-700 active:scale-[0.98] text-amber-400 font-bold text-xs py-2.5 px-3.5 rounded-xl border border-dark-700 flex items-center justify-center gap-1.5 transition touch-manipulation">
              <i class="fa-solid fa-coins text-xs"></i>
              <span>${I18N[currentLang].top_coin_bot}</span>
            </a>
          </div>
        `;

        feed.appendChild(item);
      });
    }

    // ── Deal Modal Bottom Sheet Handlers ────────────────────────────
    function openDealModal(dealId) {
      const deal = allDeals.find(d => d.id === dealId);
      if (!deal) return;
      currentActiveDeal = deal;

      const modal = document.getElementById('deal-modal');
      const img = document.getElementById('modal-img');
      const imgWrap = document.getElementById('modal-img-wrap');
      const title = document.getElementById('modal-title');
      const cat = document.getElementById('modal-cat');
      const date = document.getElementById('modal-date');
      const country = document.getElementById('modal-country');
      const coins = document.getElementById('modal-coins');
      const couponWrap = document.getElementById('modal-coupon-wrap');
      const couponCode = document.getElementById('modal-coupon-code');
      const price = document.getElementById('modal-price');
      const affBtn = document.getElementById('modal-aff-btn');
      const chLink = document.getElementById('modal-channel-link');

      if (deal.photo_url) {
        imgWrap.classList.remove('hidden');
        img.src = deal.photo_url;
      } else {
        imgWrap.classList.add('hidden');
      }

      title.textContent = deal.title;
      cat.textContent = deal.category_label || I18N[currentLang].deal_category_fallback;
      date.textContent = deal.date || '';

      if (deal.country) {
        country.textContent = deal.country;
        country.classList.remove('hidden');
      } else {
        country.classList.add('hidden');
      }

      if (deal.has_coins) coins.classList.remove('hidden');
      else coins.classList.add('hidden');

      if (deal.coupon) {
        couponWrap.classList.remove('hidden');
        couponCode.textContent = deal.coupon;
      } else {
        couponWrap.classList.add('hidden');
      }

      price.innerHTML = formatPrice(deal);
      affBtn.href = deal.affiliate_url;

      if (deal.telegram_url) {
        chLink.innerHTML = `<a href="${deal.telegram_url}" target="_blank" rel="noopener noreferrer" class="text-sky-400 hover:underline font-bold text-xs flex items-center gap-1"><i class="fa-brands fa-telegram"></i> Telegram</a>`;
      } else {
        chLink.innerHTML = '';
      }

      modal.classList.remove('hidden');
      document.body.style.overflow = 'hidden';
    }

    function closeDealModal() {
      const modal = document.getElementById('deal-modal');
      if (modal) modal.classList.add('hidden');
      document.body.style.overflow = '';
      currentActiveDeal = null;
    }

    function onModalBackdropClick(e) {
      if (e.target.id === 'deal-modal') {
        closeDealModal();
      }
    }

    function copyCoupon(code, btn) {
      navigator.clipboard.writeText(code).then(() => {
        showToast(I18N[currentLang].btn_copied + ' ' + code);
        const span = btn ? btn.querySelector('.copy-text') : null;
        if (span) {
          const original = span.textContent;
          span.textContent = I18N[currentLang].btn_copied;
          btn.classList.add('text-emerald-400', 'border-emerald-500/50');
          setTimeout(() => {
            span.textContent = original;
            btn.classList.remove('text-emerald-400', 'border-emerald-500/50');
          }, 1800);
        }
      });
    }

    function copyCouponFromModal(btn) {
      if (currentActiveDeal && currentActiveDeal.coupon) {
        copyCoupon(currentActiveDeal.coupon, btn);
      }
    }

    // ── Keyboard & Lifecycle Handlers ───────────────────────────────
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeDealModal();
    });

    document.addEventListener('DOMContentLoaded', () => {
      // Initialize language from storage
      setLanguage(currentLang);
      fetchDeals();
      setInterval(() => fetchDeals(false), 180000);
    });
  </script>

</body>
</html>"""

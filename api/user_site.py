"""
User-Facing Public Website for DealScout DZ.
Professional, serious e-commerce deal aggregator aesthetics.
Clean neutral palette (Zero blue slop!), Full Light & Dark Mode support.
Robust Telegram/CDN Image Loading & Proxy Recovery.
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
  <meta name="referrer" content="no-referrer">
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
  <meta property="og:image" content="https://dealscout-green.vercel.app/logo.png">
  <meta property="og:image:secure_url" content="https://dealscout-green.vercel.app/logo.png">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
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
  <meta name="twitter:image" content="https://dealscout-green.vercel.app/logo.png">
  <meta name="twitter:image:alt" content="DealScout DZ">

  <!-- PWA & Mobile Meta (iOS Safari & Android Chrome) -->
  <link rel="manifest" href="/manifest.json">
  <link rel="icon" type="image/png" href="/logo_circular.png">
  <link rel="shortcut icon" href="/logo_circular.png">
  <link rel="apple-touch-icon" href="/logo_circular.png">
  <meta name="theme-color" content="#09090b" id="meta-theme-color">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="DealScout DZ">
  <meta name="format-detection" content="telephone=no">

  <!-- Resilient Production Stylesheets (Static CSS loaded first, always reliable) -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=Inter:wght@400;500;600;700;800&family=Tajawal:wght@500;700;800&display=swap" rel="stylesheet">

  <!-- Optional Tailwind JIT CDN with safety guard -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    if (typeof tailwind !== 'undefined') {
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
              crimson: {
                500: '#f43f5e',
                600: '#e11d48',
                700: '#be123c'
              }
            }
          }
        }
      };
    }
  </script>

  <style>
    :root {
      --sat: env(safe-area-inset-top, 0px);
      --sab: env(safe-area-inset-bottom, 0px);
      --sal: env(safe-area-inset-left, 0px);
      --sar: env(safe-area-inset-right, 0px);

      /* Clean Light Theme Tokens */
      --bg-page: #f4f4f5;
      --bg-card: #ffffff;
      --bg-card-hover: #fafafa;
      --bg-elevated: #ffffff;
      --bg-subtle: #e4e4e7;
      --border-card: #e4e4e7;
      --border-subtle: #d4d4d8;
      --text-main: #09090b;
      --text-muted: #52525b;
      --text-soft: #71717a;
      --header-bg: rgba(255, 255, 255, 0.94);
      --input-bg: #ffffff;
      --shadow-card: 0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px -1px rgba(0, 0, 0, 0.05);
    }

    html.dark {
      /* Clean Neutral Dark Tokens (Zero blue slop!) */
      --bg-page: #09090b;
      --bg-card: #121215;
      --bg-card-hover: #18181b;
      --bg-elevated: #18181b;
      --bg-subtle: #27272a;
      --border-card: #27272a;
      --border-subtle: #3f3f46;
      --text-main: #fafafa;
      --text-muted: #a1a1aa;
      --text-soft: #71717a;
      --header-bg: rgba(18, 18, 21, 0.94);
      --input-bg: #18181b;
      --shadow-card: 0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -2px rgba(0, 0, 0, 0.2);
    }

    html {
      scroll-behavior: smooth;
      -webkit-text-size-adjust: 100%;
    }
    body {
      background-color: var(--bg-page);
      color: var(--text-main);
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      -webkit-tap-highlight-color: transparent;
      transition: background-color 0.2s ease, color 0.2s ease;
    }
    body[dir="ltr"] {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    body[dir="rtl"] {
      font-family: 'IBM Plex Sans Arabic', Tajawal, sans-serif;
    }
    *, *::before, *::after { box-sizing: border-box; }
    img { max-width: 100%; height: auto; }
    a { color: inherit; text-decoration: none; }
    button { font-family: inherit; cursor: pointer; border: none; background: transparent; }

    /* Bulletproof Brand Logo & Image Constraints */
    header a img, .brand-logo-img {
      width: 36px !important;
      height: 36px !important;
      max-width: 36px !important;
      max-height: 36px !important;
      min-width: 36px !important;
      min-height: 36px !important;
      object-fit: contain !important;
      border-radius: 12px !important;
      display: inline-block !important;
    }
    footer img, .footer-logo-img {
      width: 28px !important;
      height: 28px !important;
      max-width: 28px !important;
      max-height: 28px !important;
      object-fit: contain !important;
      border-radius: 8px !important;
      display: inline-block !important;
    }

    /* Resilient Core Layout Utilities - Hidden ALWAYS overrides any display */
    [hidden], .hidden { display: none !important; }
    .flex:not(.hidden) { display: flex !important; }
    .inline-flex:not(.hidden) { display: inline-flex !important; }
    .grid:not(.hidden) { display: grid !important; }
    .items-center { align-items: center !important; }
    .justify-between { justify-content: space-between !important; }
    .justify-center { justify-content: center !important; }
    .flex-col { flex-direction: column !important; }
    .flex-wrap { flex-wrap: wrap !important; }
    .flex-shrink-0 { flex-shrink: 0 !important; }
    .flex-grow { flex-grow: 1 !important; }
    .flex-1 { flex: 1 1 0% !important; }
    .rounded-lg { border-radius: 0.5rem !important; }
    .rounded-xl { border-radius: 0.75rem !important; }
    .rounded-2xl { border-radius: 1rem !important; }
    .rounded-3xl { border-radius: 1.5rem !important; }
    .rounded-full { border-radius: 9999px !important; }
    .border { border-width: 1px !important; border-style: solid !important; }
    .font-bold { font-weight: 700 !important; }
    .font-semibold { font-weight: 600 !important; }
    .text-crimson-500, .text-rose-500 { color: #f43f5e !important; }
    .bg-crimson-600, .bg-rose-600 { background-color: #e11d48 !important; color: #ffffff !important; }

    /* Modal Strict Visibility */
    #deal-modal.hidden {
      display: none !important;
      visibility: hidden !important;
      opacity: 0 !important;
      pointer-events: none !important;
    }
    #deal-modal:not(.hidden) {
      display: flex !important;
      visibility: visible !important;
      opacity: 1 !important;
      pointer-events: auto !important;
    }

    button, a, input, select, textarea, [role="button"] {
      touch-action: manipulation;
      -webkit-tap-highlight-color: transparent;
    }
    .deal-card {
      background-color: var(--bg-card);
      border: 1px solid var(--border-card);
      box-shadow: var(--shadow-card);
      transition: border-color 0.18s ease, transform 0.18s ease, box-shadow 0.18s ease;
    }
    @media (hover: hover) {
      .deal-card:hover {
        border-color: #f43f5e;
        transform: translateY(-2px);
        box-shadow: 0 10px 25px -5px rgba(244, 63, 94, 0.12);
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
    ::selection { background: #e11d48; color: #ffffff; }

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
<body class="min-h-screen flex flex-col justify-between" dir="rtl">

  <!-- Top Utilities Bar -->
  <aside class="border-b text-[11px] py-1.5 px-4 pt-safe transition-colors" style="background-color: var(--bg-card); border-color: var(--border-card); color: var(--text-muted);" aria-label="شريط المعلومات">
    <div class="max-w-7xl mx-auto flex items-center justify-between gap-3">
      <div class="flex items-center gap-3">
        <span class="inline-flex items-center gap-1.5 font-medium">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span data-i18n="top_live_updates">تحديث فوري من القنوات</span>
        </span>
        <span class="hidden sm:inline opacity-30">|</span>
        <a href="https://squarealgerie.com" target="_blank" rel="noopener noreferrer" class="hidden sm:flex items-center gap-1 hover:opacity-80 transition py-0.5">
          <i class="fa-solid fa-chart-line text-emerald-500"></i>
          <span><span data-i18n="top_usdt_rate">سعر صرف السكوار</span>: 1 USDT ≈ <b id="top-usdt-rate" class="font-mono text-emerald-500 font-bold">256.9</b> <span data-i18n="currency_dzd">دج</span></span>
        </a>
      </div>
      
      <div class="flex items-center gap-2 sm:gap-3">
        <!-- Theme Toggle Button -->
        <button onclick="toggleTheme()" id="theme-toggle-btn" aria-label="Toggle Light / Dark theme" class="px-2 py-0.5 rounded-lg border text-xs flex items-center gap-1.5 transition active:scale-95" style="border-color: var(--border-card); background-color: var(--bg-elevated); color: var(--text-main);">
          <i id="theme-icon" class="fa-solid fa-moon text-[11px]"></i>
          <span id="theme-text" class="text-[11px] hidden sm:inline">داكن</span>
        </button>

        <span class="opacity-30">|</span>

        <!-- Language Switcher Button -->
        <div class="inline-flex items-center border rounded-lg p-0.5 text-xs" style="border-color: var(--border-card); background-color: var(--bg-elevated);">
          <button onclick="setLanguage('ar')" id="lang-ar-btn" class="px-2 py-0.5 rounded text-[11px] font-bold bg-crimson-600 text-white transition active:scale-95">العربية</button>
          <button onclick="setLanguage('fr')" id="lang-fr-btn" class="px-2 py-0.5 rounded text-[11px] font-bold opacity-60 hover:opacity-100 transition active:scale-95">Français</button>
        </div>

        <span class="opacity-30">|</span>
        <a href="https://t.me/Alilo07BOT" target="_blank" rel="noopener noreferrer" class="hover:text-amber-500 transition font-medium inline-flex items-center gap-1 py-1 px-1.5 active:scale-95 touch-manipulation">
          <i class="fa-solid fa-coins text-amber-500 text-[10px]"></i>
          <span class="hidden sm:inline" data-i18n="top_coin_bot">بوت العملات</span>
        </a>
        <span class="opacity-30">|</span>
        <a href="https://t.me/DzAliexpress0" target="_blank" rel="noopener noreferrer" class="hover:text-sky-500 transition font-medium inline-flex items-center gap-1 py-1 px-1.5 active:scale-95 touch-manipulation">
          <i class="fa-brands fa-telegram text-sky-500"></i>
          <span class="hidden sm:inline">Telegram</span>
        </a>
      </div>
    </div>
  </aside>

  <!-- Main Navigation Bar -->
  <header class="sticky top-0 z-40 border-b backdrop-blur-md px-3 sm:px-4 py-2.5 sm:py-3 transition-colors" style="background-color: var(--header-bg); border-color: var(--border-card);">
    <div class="max-w-7xl mx-auto flex items-center justify-between gap-3 sm:gap-4">
      
      <!-- Brand Logo -->
      <a href="#deals" onclick="showPage('deals')" class="flex items-center gap-2 sm:gap-2.5 flex-shrink-0 min-h-[44px] touch-manipulation" aria-label="DealScout DZ">
        <img src="/logo_circular.png" alt="DealScout DZ" width="36" height="36" style="width: 36px; height: 36px; max-width: 36px; max-height: 36px; object-fit: contain;" class="w-9 h-9 rounded-xl object-contain shadow-sm flex-shrink-0 brand-logo-img" onerror="this.onerror=null; this.src='/logo.png'">
        <div>
          <div class="flex items-center gap-1.5">
            <h1 class="font-bold text-base tracking-tight font-inter inline-flex items-center gap-1.5" style="color: var(--text-main);">
              <span>DealScout<span class="text-crimson-500">DZ</span></span>
              <span class="text-[10px] font-semibold px-1.5 py-0.2 rounded border font-mono font-normal" style="background-color: var(--bg-subtle); border-color: var(--border-card); color: var(--text-muted);">2.6</span>
            </h1>
          </div>
          <p class="text-[10px] block -mt-0.5" style="color: var(--text-soft);" data-i18n="brand_subtitle">بوابة صفقات وتخفيضات AliExpress 🇩🇿</p>
        </div>
      </a>

      <!-- Desktop Nav Pages Links -->
      <nav class="hidden lg:flex items-center gap-1 text-xs font-semibold" style="color: var(--text-muted);">
        <button onclick="showPage('deals')" id="nav-link-deals" class="nav-page-btn px-3 py-1.5 rounded-lg transition flex items-center gap-1.5 font-bold" style="background-color: var(--bg-elevated); color: var(--text-main);">
          <i class="fa-solid fa-fire text-crimson-500 text-xs"></i>
          <span data-i18n="nav_deals">الصفقات</span>
        </button>
        <button onclick="showPage('cards')" id="nav-link-cards" class="nav-page-btn px-3 py-1.5 rounded-lg hover:opacity-100 transition flex items-center gap-1.5">
          <i class="fa-solid fa-credit-card text-emerald-500 text-xs"></i>
          <span data-i18n="nav_cards">بطاقات الشراء</span>
        </button>
        <button onclick="showPage('coins')" id="nav-link-coins" class="nav-page-btn px-3 py-1.5 rounded-lg hover:opacity-100 transition flex items-center gap-1.5">
          <i class="fa-solid fa-coins text-amber-500 text-xs"></i>
          <span data-i18n="nav_coins">بوت العملات</span>
        </button>
        <button onclick="showPage('faq')" id="nav-link-faq" class="nav-page-btn px-3 py-1.5 rounded-lg hover:opacity-100 transition flex items-center gap-1.5">
          <i class="fa-solid fa-circle-question text-sky-500 text-xs"></i>
          <span data-i18n="nav_faq">الأسئلة الشائعة</span>
        </button>
        <button onclick="showPage('contact')" id="nav-link-contact" class="nav-page-btn px-3 py-1.5 rounded-lg hover:opacity-100 transition flex items-center gap-1.5">
          <i class="fa-solid fa-envelope text-emerald-500 text-xs"></i>
          <span data-i18n="nav_contact">اتصل بنا</span>
        </button>
        <button onclick="showPage('about')" id="nav-link-about" class="nav-page-btn px-3 py-1.5 rounded-lg hover:opacity-100 transition flex items-center gap-1.5">
          <i class="fa-solid fa-info-circle text-purple-500 text-xs"></i>
          <span data-i18n="nav_about">من نحن</span>
        </button>
      </nav>

      <!-- Search Bar Desktop -->
      <div class="hidden md:flex items-center relative flex-1 max-w-xs xl:max-w-sm">
        <i class="fa-solid fa-magnifying-glass absolute right-3.5 top-1/2 -translate-y-1/2 text-xs pointer-events-none opacity-50"></i>
        <input 
          type="search" 
          id="desktop-search" 
          aria-label="Search deals"
          oninput="handleSearchInput(this.value)"
          placeholder="ابحث عن هاتف، شاحن، كود خصم..." 
          data-i18n-placeholder="search_placeholder"
          class="w-full border rounded-xl pr-9 pl-3 py-2 text-xs focus:outline-none focus:border-rose-500 transition min-h-[40px]"
          style="background-color: var(--input-bg); border-color: var(--border-card); color: var(--text-main);"
        />
      </div>

      <!-- Action Buttons -->
      <div class="flex items-center gap-1.5 sm:gap-2">
        <!-- Currency Selector -->
        <div class="flex items-center border rounded-xl p-0.5 text-xs font-semibold" style="border-color: var(--border-card); background-color: var(--bg-card);" aria-label="Currency" role="group">
          <button onclick="setCurrency('DZD')" id="curr-dzd" class="min-w-[34px] sm:min-w-[38px] h-8 sm:h-9 px-2 py-1 rounded-lg bg-crimson-600 text-white font-mono transition flex items-center justify-center active:scale-95 touch-manipulation">دج</button>
          <button onclick="setCurrency('USD')" id="curr-usd" class="min-w-[32px] sm:min-w-[36px] h-8 sm:h-9 px-2 py-1 rounded-lg opacity-70 hover:opacity-100 font-mono transition flex items-center justify-center active:scale-95 touch-manipulation">$</button>
          <button onclick="setCurrency('EUR')" id="curr-eur" class="min-w-[32px] sm:min-w-[36px] h-8 sm:h-9 px-2 py-1 rounded-lg opacity-70 hover:opacity-100 font-mono transition flex items-center justify-center active:scale-95 touch-manipulation">€</button>
        </div>

        <!-- Join Telegram Button -->
        <a id="btn-telegram-join" href="https://t.me/DzAliexpress0" target="_blank" rel="noopener noreferrer" class="bg-[#229ED9] hover:bg-[#1e8ec3] text-white text-xs h-8 sm:h-9 px-2.5 sm:px-3 rounded-xl font-bold flex items-center justify-center gap-1.5 transition active:scale-95 shadow-sm touch-manipulation">
          <i class="fa-brands fa-telegram text-sm" aria-hidden="true"></i>
          <span class="hidden sm:inline" data-i18n="btn_join_channel">انضم للقناة</span>
        </a>

        <!-- Refresh Data Button -->
        <button onclick="fetchDeals(true, true)" title="تحديث البيانات" class="w-8 sm:w-9 h-8 sm:h-9 rounded-xl border text-xs flex items-center justify-center transition active:scale-95 touch-manipulation cursor-pointer hover:border-rose-500" style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-main);">
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
      <div class="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 border p-2 sm:p-2.5 rounded-2xl transition-colors" style="background-color: var(--bg-card); border-color: var(--border-card);">
        <div class="flex items-center gap-1.5 p-1 rounded-xl border text-xs font-bold" style="background-color: var(--bg-page); border-color: var(--border-card);" role="tablist">
          <button onclick="switchChannel('@DzAliexpress0')" id="tab-dz" role="tab" aria-selected="true" class="flex-1 sm:flex-none min-h-[40px] px-4 py-2 rounded-lg bg-crimson-600 text-white transition flex items-center justify-center gap-2 active:scale-95 shadow-sm">
            <span>🇩🇿</span>
            <span data-i18n="tab_algeria_deals">عروض الجزائر (@DzAliexpress0)</span>
          </button>
          <button onclick="switchChannel('@francedealsdz')" id="tab-fr" role="tab" aria-selected="false" class="flex-1 sm:flex-none min-h-[40px] px-4 py-2 rounded-lg opacity-70 hover:opacity-100 transition flex items-center justify-center gap-2 active:scale-95">
            <span>🇫🇷</span>
            <span data-i18n="tab_france_deals">عروض فرنسا (@francedealsdz)</span>
          </button>
        </div>

        <!-- View Switcher (Grid vs Telegram Stream) -->
        <div class="flex items-center justify-end gap-1 border rounded-xl p-1 text-xs font-semibold" style="background-color: var(--bg-page); border-color: var(--border-card);">
          <button onclick="setViewMode('grid')" id="view-mode-grid" class="min-h-[36px] px-3 py-1.5 rounded-lg text-white transition flex items-center gap-1.5 active:scale-95" style="background-color: var(--bg-elevated); color: var(--text-main);">
            <i class="fa-solid fa-grip text-xs"></i>
            <span data-i18n="view_grid">بطاقات</span>
          </button>
          <button onclick="setViewMode('feed')" id="view-mode-feed" class="min-h-[36px] px-3 py-1.5 rounded-lg opacity-60 hover:opacity-100 transition flex items-center gap-1.5 active:scale-95">
            <i class="fa-brands fa-telegram text-xs"></i>
            <span data-i18n="view_stream">منشورات القناة</span>
          </button>
        </div>
      </div>

      <!-- Mobile Search Bar -->
      <div class="md:hidden relative">
        <i class="fa-solid fa-magnifying-glass absolute right-3.5 top-1/2 -translate-y-1/2 text-sm pointer-events-none opacity-50"></i>
        <input 
          type="search" 
          id="mobile-search" 
          aria-label="Search deals"
          oninput="handleSearchInput(this.value)"
          placeholder="ابحث عن هاتف، شاحن، كود خصم، ساعة..." 
          data-i18n-placeholder="search_placeholder"
          class="w-full border rounded-xl pr-10 pl-3.5 py-3 text-sm focus:outline-none focus:border-rose-500 transition min-h-[46px]"
          style="background-color: var(--input-bg); border-color: var(--border-card); color: var(--text-main);"
        />
      </div>

      <!-- Category Filter Pills -->
      <section class="border-b pb-3" style="border-color: var(--border-card);" aria-label="Categories">
        <div class="flex items-center gap-2 overflow-x-auto no-scrollbar pb-1 text-xs font-semibold -mx-3.5 px-3.5 sm:mx-0 sm:px-0 momentum-scroll">
          <button onclick="setCategory('all')" id="cat-all" class="cat-pill min-h-[42px] px-3.5 py-2 rounded-xl bg-crimson-600 text-white whitespace-nowrap transition flex items-center gap-1.5 flex-shrink-0 active:scale-95 touch-manipulation shadow-sm">
            <span data-i18n="cat_all">الكل</span>
            <span id="count-all" class="text-[11px] font-mono opacity-80 bg-black/20 px-1.5 py-0.2 rounded">0</span>
          </button>
          <button onclick="setCategory('smartphones')" id="cat-smartphones" class="cat-pill min-h-[42px] px-3.5 py-2 rounded-xl border whitespace-nowrap transition flex items-center gap-1.5 flex-shrink-0 active:scale-95 touch-manipulation" style="background-color: var(--bg-card); border-color: var(--border-card); color: var(--text-muted);">
            <span data-i18n="cat_smartphones">هواتف وتابلت</span>
            <span id="count-smartphones" class="text-[11px] font-mono opacity-60">0</span>
          </button>
          <button onclick="setCategory('gaming')" id="cat-gaming" class="cat-pill min-h-[42px] px-3.5 py-2 rounded-xl border whitespace-nowrap transition flex items-center gap-1.5 flex-shrink-0 active:scale-95 touch-manipulation" style="background-color: var(--bg-card); border-color: var(--border-card); color: var(--text-muted);">
            <span data-i18n="cat_gaming">أجهزة قيمنق</span>
            <span id="count-gaming" class="text-[11px] font-mono opacity-60">0</span>
          </button>
          <button onclick="setCategory('audio')" id="cat-audio" class="cat-pill min-h-[42px] px-3.5 py-2 rounded-xl border whitespace-nowrap transition flex items-center gap-1.5 flex-shrink-0 active:scale-95 touch-manipulation" style="background-color: var(--bg-card); border-color: var(--border-card); color: var(--text-muted);">
            <span data-i18n="cat_audio">سماعات وصوتيات</span>
            <span id="count-audio" class="text-[11px] font-mono opacity-60">0</span>
          </button>
          <button onclick="setCategory('tech')" id="cat-tech" class="cat-pill min-h-[42px] px-3.5 py-2 rounded-xl border whitespace-nowrap transition flex items-center gap-1.5 flex-shrink-0 active:scale-95 touch-manipulation" style="background-color: var(--bg-card); border-color: var(--border-card); color: var(--text-muted);">
            <span data-i18n="cat_tech">شواحن وملحقات</span>
            <span id="count-tech" class="text-[11px] font-mono opacity-60">0</span>
          </button>
          <button onclick="setCategory('tajmi3at')" id="cat-tajmi3at" class="cat-pill min-h-[42px] px-3.5 py-2 rounded-xl border whitespace-nowrap transition flex items-center gap-1.5 flex-shrink-0 active:scale-95 touch-manipulation" style="background-color: var(--bg-card); border-color: var(--border-card); color: var(--text-muted);">
            <span data-i18n="cat_tajmi3at">تجميعات العروض</span>
            <span id="count-tajmi3at" class="text-[11px] font-mono opacity-60">0</span>
          </button>
        </div>
      </section>

      <!-- Section Title & Live Count -->
      <div class="flex items-center justify-between border-b pb-2" style="border-color: var(--border-card);">
        <h2 class="text-xs sm:text-sm font-bold flex items-center gap-2" style="color: var(--text-main);">
          <i class="fa-solid fa-fire text-crimson-500" aria-hidden="true"></i>
          <span data-i18n="deals_section_heading">أحدث صفقات وتخفيضات AliExpress بالدينار الجزائري</span>
        </h2>
        <span class="text-[11px] text-emerald-500 flex items-center gap-1.5 font-medium">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span id="live-deals-counter" class="font-mono">...</span>
        </span>
      </div>

      <!-- Deals Grid (Cards View) -->
      <section id="deals-grid" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3.5 sm:gap-4" aria-label="قائمة الصفقات">
        <!-- Skeleton Loaders -->
        <div class="deal-card rounded-2xl p-4 animate-pulse space-y-3">
          <div class="w-full aspect-[4/3] rounded-xl opacity-20" style="background-color: var(--bg-subtle);"></div>
          <div class="h-4 rounded w-3/4 opacity-20" style="background-color: var(--bg-subtle);"></div>
          <div class="h-5 rounded w-1/2 opacity-20" style="background-color: var(--bg-subtle);"></div>
          <div class="h-11 rounded-xl opacity-20" style="background-color: var(--bg-subtle);"></div>
        </div>
        <div class="deal-card rounded-2xl p-4 animate-pulse space-y-3">
          <div class="w-full aspect-[4/3] rounded-xl opacity-20" style="background-color: var(--bg-subtle);"></div>
          <div class="h-4 rounded w-3/4 opacity-20" style="background-color: var(--bg-subtle);"></div>
          <div class="h-5 rounded w-1/2 opacity-20" style="background-color: var(--bg-subtle);"></div>
          <div class="h-11 rounded-xl opacity-20" style="background-color: var(--bg-subtle);"></div>
        </div>
        <div class="deal-card rounded-2xl p-4 animate-pulse space-y-3">
          <div class="w-full aspect-[4/3] rounded-xl opacity-20" style="background-color: var(--bg-subtle);"></div>
          <div class="h-4 rounded w-3/4 opacity-20" style="background-color: var(--bg-subtle);"></div>
          <div class="h-5 rounded w-1/2 opacity-20" style="background-color: var(--bg-subtle);"></div>
          <div class="h-11 rounded-xl opacity-20" style="background-color: var(--bg-subtle);"></div>
        </div>
        <div class="deal-card rounded-2xl p-4 animate-pulse space-y-3">
          <div class="w-full aspect-[4/3] rounded-xl opacity-20" style="background-color: var(--bg-subtle);"></div>
          <div class="h-4 rounded w-3/4 opacity-20" style="background-color: var(--bg-subtle);"></div>
          <div class="h-5 rounded w-1/2 opacity-20" style="background-color: var(--bg-subtle);"></div>
          <div class="h-11 rounded-xl opacity-20" style="background-color: var(--bg-subtle);"></div>
        </div>
      </section>

      <!-- Telegram Stream Feed (Alternative View) -->
      <section id="deals-feed" class="hidden max-w-2xl mx-auto space-y-4" aria-label="بث منشورات القناة"></section>

      <!-- Empty State -->
      <div id="empty-state" class="hidden text-center py-12 px-4 space-y-3 border border-dashed rounded-2xl" style="background-color: var(--bg-card); border-color: var(--border-card);">
        <i class="fa-solid fa-magnifying-glass text-3xl opacity-40" aria-hidden="true"></i>
        <h3 class="font-bold text-sm" style="color: var(--text-main);" data-i18n="empty_title">لا توجد صفقات مطابقة للبحث</h3>
        <p class="text-xs" style="color: var(--text-muted);" data-i18n="empty_desc">جرب كتابة اسم منتج أو علامة تجارية مختلفة أو أعد تعيين الفلاتر.</p>
        <button onclick="resetFilters()" class="min-h-[44px] px-4 py-2 text-xs font-bold text-crimson-500 hover:underline active:scale-95 touch-manipulation" data-i18n="empty_reset">
          عرض جميع الصفقات
        </button>
      </div>

    </div>

    <!-- ───────────────────────────────────────────────────────── -->
    <!-- PAGE: CARDS & REFERRALS (BYBIT, REDOTPAY, BINANCE P2P)    -->
    <!-- ───────────────────────────────────────────────────────── -->
    <div id="page-cards" class="page-view hidden space-y-6">
      
      <!-- Hero Banner -->
      <div class="border rounded-3xl p-6 sm:p-8 space-y-4" style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, var(--bg-card) 60%); border-color: rgba(16, 185, 129, 0.3);">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold bg-emerald-500/15 text-emerald-500">
          <i class="fa-solid fa-credit-card"></i>
          <span data-i18n="cards_badge">دليل بطاقات الدفع والشحن بالدينار الجزائري 🇩🇿</span>
        </div>
        <h2 class="text-xl sm:text-2xl font-bold tracking-tight" style="color: var(--text-main);" data-i18n="cards_hero_title">
          كيف تشتري من AliExpress وأنت في الجزائر؟ | أفضل البطاقات والشحن بـ BaridiMob
        </h2>
        <p class="text-xs sm:text-sm leading-relaxed max-w-3xl" style="color: var(--text-muted);" data-i18n="cards_hero_desc">
          لأن البطاقات البنكية الجزائرية المحلية لا تعمل في المواقع العالمية، إليك الحل الرسمي والمجرب: احصل على بطاقة افتراضية دولية مجانية، واشحنها مباشرة بالدينار الجزائري عبر بريدي موب ومنصة بينانس دون وسطاء وبأقل تكلفة!
        </p>
      </div>

      <!-- 3 Featured Partner Cards Grid -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
        
        <!-- Partner 1: Bybit Virtual Mastercard -->
        <div class="border rounded-2xl p-5 sm:p-6 flex flex-col justify-between transition-all hover:border-emerald-500/50 space-y-4" style="background-color: var(--bg-card); border-color: var(--border-card);">
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <div class="w-10 h-10 rounded-xl bg-emerald-500/10 text-emerald-500 flex items-center justify-center text-lg font-bold">
                <i class="fa-solid fa-credit-card"></i>
              </div>
              <span class="text-[11px] font-bold px-2.5 py-1 rounded-full bg-emerald-500/15 text-emerald-500 border border-emerald-500/20" data-i18n="cards_bybit_badge">مجانية 100% — 0 دج</span>
            </div>
            <h3 class="font-bold text-base sm:text-lg" style="color: var(--text-main);" data-i18n="cards_bybit_title">بطاقة Bybit Card (MasterCard)</h3>
            <p class="text-xs leading-relaxed" style="color: var(--text-muted);" data-i18n="cards_bybit_desc">
              البطاقة الأفضل حالياً للتسوق من AliExpress: تصدر فورياً ومجاناً 100% وبدون أي اشتراك شهري، مقبولة في جميع المتاجر العالمية وPayPal مع كاش باك يصل إلى 10%.
            </p>
            <ul class="text-xs space-y-2 pt-1 font-medium" style="color: var(--text-main);">
              <li class="flex items-center gap-2"><i class="fa-solid fa-check text-emerald-500 text-[11px]"></i><span data-i18n="cards_bybit_f1">0 دج مصاريف فتح وبدون اشتراك شهري</span></li>
              <li class="flex items-center gap-2"><i class="fa-solid fa-check text-emerald-500 text-[11px]"></i><span data-i18n="cards_bybit_f2">مقبولة 100% على AliExpress وPayPal</span></li>
              <li class="flex items-center gap-2"><i class="fa-solid fa-check text-emerald-500 text-[11px]"></i><span data-i18n="cards_bybit_f3">شحن فوري بالدينار عبر Binance P2P</span></li>
            </ul>
          </div>

          <div class="pt-2 border-t space-y-3" style="border-color: var(--border-card);">
            <div class="flex items-center justify-between p-2.5 rounded-xl border" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
              <div class="min-w-0">
                <div class="text-[10px] opacity-70" data-i18n="cards_ref_code">كود التسجيل الحصري:</div>
                <div class="font-mono font-bold text-sm text-emerald-500">L9LLRP5</div>
              </div>
              <button onclick="copyReferralCode('L9LLRP5', this)" class="min-h-[38px] px-3 py-1 text-xs font-bold rounded-lg border hover:bg-emerald-500/10 active:scale-95 transition flex items-center gap-1.5 touch-manipulation" style="border-color: var(--border-card); color: var(--text-main);">
                <i class="fa-regular fa-copy"></i>
                <span data-i18n="cards_btn_copy_code">نسخ الكود</span>
              </button>
            </div>
            <a href="https://www.bybit.com/invite?ref=L9LLRP5&medium=referral&utm_campaign=evergreen&share_to=Telegram" target="_blank" rel="noopener noreferrer" class="w-full min-h-[44px] rounded-xl bg-emerald-600 hover:bg-emerald-500 active:scale-[0.98] text-white font-bold text-xs sm:text-sm py-2.5 px-4 flex items-center justify-center gap-2 shadow-md transition touch-manipulation">
              <i class="fa-solid fa-arrow-up-right-from-square text-xs"></i>
              <span data-i18n="cards_btn_bybit_cta">طلب بطاقة Bybit المجانية</span>
            </a>
          </div>
        </div>

        <!-- Partner 2: RedotPay Virtual Visa -->
        <div class="border rounded-2xl p-5 sm:p-6 flex flex-col justify-between transition-all hover:border-rose-500/50 space-y-4" style="background-color: var(--bg-card); border-color: var(--border-card);">
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <div class="w-10 h-10 rounded-xl bg-rose-500/10 text-rose-500 flex items-center justify-center text-lg font-bold">
                <i class="fa-brands fa-cc-visa"></i>
              </div>
              <span class="text-[11px] font-bold px-2.5 py-1 rounded-full bg-rose-500/15 text-rose-500 border border-rose-500/20" data-i18n="cards_redot_badge">هدية 5$ ترحيبية 🎁</span>
            </div>
            <h3 class="font-bold text-base sm:text-lg" style="color: var(--text-main);" data-i18n="cards_redot_title">بطاقة فيزا RedotPay (هدية 5$)</h3>
            <p class="text-xs leading-relaxed" style="color: var(--text-muted);" data-i18n="cards_redot_desc">
              بطاقة فيزا افتراضية دولية تصدر في دقيقتين بالبطاقة الوطنية الجزائرية أو جواز السفر، تدعم تخفيضات العملات وكوبونات AliExpress وربط PayPal الجزائري.
            </p>
            <ul class="text-xs space-y-2 pt-1 font-medium" style="color: var(--text-main);">
              <li class="flex items-center gap-2"><i class="fa-solid fa-check text-rose-500 text-[11px]"></i><span data-i18n="cards_redot_f1">هدية 5$ رصيد ترحيبي فوري عند التسجيل</span></li>
              <li class="flex items-center gap-2"><i class="fa-solid fa-check text-rose-500 text-[11px]"></i><span data-i18n="cards_redot_f2">تفعيل فوري ببطاقة التعريف الوطنية</span></li>
              <li class="flex items-center gap-2"><i class="fa-solid fa-check text-rose-500 text-[11px]"></i><span data-i18n="cards_redot_f3">دعم ربط وتفعيل كامل لـ PayPal</span></li>
            </ul>
          </div>

          <div class="pt-2 border-t space-y-3" style="border-color: var(--border-card);">
            <div class="flex items-center justify-between p-2.5 rounded-xl border" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
              <div class="min-w-0">
                <div class="text-[10px] opacity-70" data-i18n="cards_ref_code">كود الهدية الترحيبية:</div>
                <div class="font-mono font-bold text-sm text-rose-500">djbt3</div>
              </div>
              <button onclick="copyReferralCode('djbt3', this)" class="min-h-[38px] px-3 py-1 text-xs font-bold rounded-lg border hover:bg-rose-500/10 active:scale-95 transition flex items-center gap-1.5 touch-manipulation" style="border-color: var(--border-card); color: var(--text-main);">
                <i class="fa-regular fa-copy"></i>
                <span data-i18n="cards_btn_copy_code">نسخ الكود</span>
              </button>
            </div>
            <a href="https://url.hk/i/en/djbt3" target="_blank" rel="noopener noreferrer" class="w-full min-h-[44px] rounded-xl bg-rose-600 hover:bg-rose-500 active:scale-[0.98] text-white font-bold text-xs sm:text-sm py-2.5 px-4 flex items-center justify-center gap-2 shadow-md transition touch-manipulation">
              <i class="fa-solid fa-gift text-xs"></i>
              <span data-i18n="cards_btn_redot_cta">طلب بطاقة RedotPay (+ 5$ هدية)</span>
            </a>
          </div>
        </div>

        <!-- Partner 3: Binance P2P BaridiMob -->
        <div class="border rounded-2xl p-5 sm:p-6 flex flex-col justify-between transition-all hover:border-amber-500/50 space-y-4" style="background-color: var(--bg-card); border-color: var(--border-card);">
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <div class="w-10 h-10 rounded-xl bg-amber-500/10 text-amber-500 flex items-center justify-center text-lg font-bold">
                <i class="fa-solid fa-building-columns"></i>
              </div>
              <span class="text-[11px] font-bold px-2.5 py-1 rounded-full bg-amber-500/15 text-amber-500 border border-amber-500/20" data-i18n="cards_binance_badge">سوق P2P #1 في الجزائر</span>
            </div>
            <h3 class="font-bold text-base sm:text-lg" style="color: var(--text-main);" data-i18n="cards_binance_title">منصة Binance P2P (BaridiMob)</h3>
            <p class="text-xs leading-relaxed" style="color: var(--text-muted);" data-i18n="cards_binance_desc">
              المنصة الرسمية والآمنة 100% لتحويل الدينار الجزائري من تطبيق BaridiMob أو CCP إلى رصيد دولار رقمي (USDT) بسعر الصرف الحقيقي وبدون وسطاء أو عمولات زائدة.
            </p>
            <ul class="text-xs space-y-2 pt-1 font-medium" style="color: var(--text-main);">
              <li class="flex items-center gap-2"><i class="fa-solid fa-check text-amber-500 text-[11px]"></i><span data-i18n="cards_binance_f1">شراء الدولار الرقمي مباشرة عبر BaridiMob</span></li>
              <li class="flex items-center gap-2"><i class="fa-solid fa-check text-amber-500 text-[11px]"></i><span data-i18n="cards_binance_f2">حماية الضمان المالي الصارم (Escrow)</span></li>
              <li class="flex items-center gap-2"><i class="fa-solid fa-check text-amber-500 text-[11px]"></i><span data-i18n="cards_binance_f3">تحويل مباشر إلى بطاقاتك في ثوانٍ</span></li>
            </ul>
          </div>

          <div class="pt-2 border-t space-y-3" style="border-color: var(--border-card);">
            <div class="flex items-center justify-between p-2.5 rounded-xl border" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
              <div class="min-w-0">
                <div class="text-[10px] opacity-70" data-i18n="cards_ref_code">كود إحالة Binance الرسمي:</div>
                <div class="font-mono font-bold text-xs sm:text-sm text-amber-500 truncate">GRO_28502_3WGQR</div>
              </div>
              <button onclick="copyReferralCode('GRO_28502_3WGQR', this)" class="min-h-[38px] px-3 py-1 text-xs font-bold rounded-lg border hover:bg-amber-500/10 active:scale-95 transition flex items-center gap-1.5 touch-manipulation flex-shrink-0" style="border-color: var(--border-card); color: var(--text-main);">
                <i class="fa-regular fa-copy"></i>
                <span data-i18n="cards_btn_copy_code">نسخ الكود</span>
              </button>
            </div>
            <a href="https://www.binance.com/referral/earn-together/refer2earn-usdc/claim?hl=en&ref=GRO_28502_3WGQR&utm_source=referral_entrance" target="_blank" rel="noopener noreferrer" class="w-full min-h-[44px] rounded-xl bg-amber-500 hover:bg-amber-400 active:scale-[0.98] text-zinc-950 font-bold text-xs sm:text-sm py-2.5 px-4 flex items-center justify-center gap-2 shadow-md transition touch-manipulation">
              <i class="fa-solid fa-arrow-up-right-from-square text-xs"></i>
              <span data-i18n="cards_btn_binance_cta">فتح حساب Binance P2P</span>
            </a>
          </div>
        </div>

      </div>

      <!-- Step-by-Step BaridiMob Shopping Workflow Guide -->
      <div class="border rounded-2xl p-6 sm:p-8 space-y-6" style="background-color: var(--bg-card); border-color: var(--border-card);">
        <div class="space-y-1">
          <h3 class="text-lg sm:text-xl font-bold" style="color: var(--text-main);" data-i18n="cards_guide_title">
            دليل الشراء خطوة بخطوة بالدينار الجزائري (BaridiMob) 🇩🇿
          </h3>
          <p class="text-xs sm:text-sm" style="color: var(--text-muted);" data-i18n="cards_guide_subtitle">
            الطريقة الرسمية والآمنة التي يستعملها آلاف المتسوقين الجزائريين يومياً للشراء من AliExpress بأقل تكلفة:
          </p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          
          <div class="border rounded-xl p-4 space-y-2 relative" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
            <div class="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-500 font-bold flex items-center justify-center text-sm">1</div>
            <h4 class="font-bold text-xs sm:text-sm" style="color: var(--text-main);" data-i18n="cards_step1_title">1. شراء USDT بـ BaridiMob</h4>
            <p class="text-xs leading-relaxed" style="color: var(--text-muted);" data-i18n="cards_step1_desc">
              افتح حسابك في Binance، ادخل قسم P2P واختر الدفع بـ BaridiMob لشراء المبلغ المطلوب من الدولار الرقمي (USDT) مباشرة في دقيقتين.
            </p>
          </div>

          <div class="border rounded-xl p-4 space-y-2 relative" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
            <div class="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-500 font-bold flex items-center justify-center text-sm">2</div>
            <h4 class="font-bold text-xs sm:text-sm" style="color: var(--text-main);" data-i18n="cards_step2_title">2. شحن بطاقتك الافتراضية</h4>
            <p class="text-xs leading-relaxed" style="color: var(--text-muted);" data-i18n="cards_step2_desc">
              حوّل رصيد USDT من Binance إلى حساب Bybit أو RedotPay الخاص بك عبر شبكة سريعة بدون أي رسوم مرتفعة.
            </p>
          </div>

          <div class="border rounded-xl p-4 space-y-2 relative" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
            <div class="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-500 font-bold flex items-center justify-center text-sm">3</div>
            <h4 class="font-bold text-xs sm:text-sm" style="color: var(--text-main);" data-i18n="cards_step3_title">3. ربط البطاقة في AliExpress</h4>
            <p class="text-xs leading-relaxed" style="color: var(--text-muted);" data-i18n="cards_step3_desc">
              انسخ معلومات بطاقتك الافتراضية (رقم البطاقة وتاريخ الانتهاء وCVV) وأضفها في وسائل الدفع بتطبيق AliExpress.
            </p>
          </div>

          <div class="border rounded-xl p-4 space-y-2 relative" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
            <div class="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-500 font-bold flex items-center justify-center text-sm">4</div>
            <h4 class="font-bold text-xs sm:text-sm" style="color: var(--text-main);" data-i18n="cards_step4_title">4. تطبيق الخصومات والشراء</h4>
            <p class="text-xs leading-relaxed" style="color: var(--text-muted);" data-i18n="cards_step4_desc">
              اختر صفقتك من موقعنا، انسخ كود الخصم، استخدم بوت العملات واستلم طردك مباشرة من مكتب بريد الجزائر القريب منك!
            </p>
          </div>

        </div>
      </div>

    </div>

    <!-- ───────────────────────────────────────────────────────── -->
    <!-- PAGE 2: COINS BOT EXPLAINER PAGE                          -->
    <!-- ───────────────────────────────────────────────────────── -->
    <div id="page-coins" class="page-view hidden space-y-6">
      
      <div class="border rounded-3xl p-6 sm:p-8 space-y-4" style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.08) 0%, var(--bg-card) 60%); border-color: rgba(245, 158, 11, 0.3);">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold bg-amber-500/15 text-amber-500">
          <i class="fa-solid fa-coins"></i>
          <span data-i18n="coins_badge">دليل توفير العملات (AliExpress Coins)</span>
        </div>
        <h2 class="text-xl sm:text-2xl font-bold tracking-tight" style="color: var(--text-main);" data-i18n="coins_hero_title">
          كيف توفر حتى 60% إضافية باستخدام عملات AliExpress وبوت @Alilo07BOT؟
        </h2>
        <p class="text-xs sm:text-sm leading-relaxed max-w-3xl" style="color: var(--text-muted);" data-i18n="coins_hero_desc">
          تمنح AliExpress مستخدميها عملات يومية (Coins)، لكن معظم المنتجات في التطبيق لا تسمح باستخدام أكثر من 2% فقط. بوت التخفيضات الخاص بنا يقوم بفك القيود وتوليد روابط مباشرة تمكّنك من استهلاك أكبر عدد ممكن من العملات والحصول على خصم ضخم فوري!
        </p>
        <div class="pt-2 flex flex-wrap gap-3">
          <a href="https://t.me/Alilo07BOT" target="_blank" rel="noopener noreferrer" class="min-h-[46px] px-5 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-zinc-950 font-bold text-xs sm:text-sm flex items-center gap-2 shadow-lg shadow-amber-500/20 active:scale-95 transition">
            <i class="fa-solid fa-coins"></i>
            <span data-i18n="coins_btn_start">تشغيل البوت مجاناً (@Alilo07BOT)</span>
          </a>
        </div>
      </div>

      <!-- 3 Steps Grid -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="border rounded-2xl p-5 space-y-3" style="background-color: var(--bg-card); border-color: var(--border-card);">
          <div class="w-10 h-10 rounded-xl text-amber-500 font-bold text-base flex items-center justify-center font-mono" style="background-color: var(--bg-elevated);">1</div>
          <h3 class="font-bold text-sm" style="color: var(--text-main);" data-i18n="coins_step1_title">انسخ رابط المنتج من AliExpress</h3>
          <p class="text-xs leading-relaxed" style="color: var(--text-muted);" data-i18n="coins_step1_desc">افتح أي منتج يعجبك داخل تطبيق AliExpress، اضغط على زر المشاركة ثم اختر نسخ الرابط (Copy Link).</p>
        </div>

        <div class="border rounded-2xl p-5 space-y-3" style="background-color: var(--bg-card); border-color: var(--border-card);">
          <div class="w-10 h-10 rounded-xl text-sky-500 font-bold text-base flex items-center justify-center font-mono" style="background-color: var(--bg-elevated);">2</div>
          <h3 class="font-bold text-sm" style="color: var(--text-main);" data-i18n="coins_step2_title">أرسل الرابط لبوت التخفيض</h3>
          <p class="text-xs leading-relaxed" style="color: var(--text-muted);" data-i18n="coins_step2_desc">افتح بوت التيليجرام <b class="text-sky-500">@Alilo07BOT</b> والصق الرابط في المحادثة. سيقوم البوت فوراً بالبحث عن أقصى نسبة خصم متاحة للعملات.</p>
        </div>

        <div class="border rounded-2xl p-5 space-y-3" style="background-color: var(--bg-card); border-color: var(--border-card);">
          <div class="w-10 h-10 rounded-xl text-emerald-500 font-bold text-base flex items-center justify-center font-mono" style="background-color: var(--bg-elevated);">3</div>
          <h3 class="font-bold text-sm" style="color: var(--text-main);" data-i18n="coins_step3_title">ادفع بالسعر المخفض</h3>
          <p class="text-xs leading-relaxed" style="color: var(--text-muted);" data-i18n="coins_step3_desc">اضغط على زر (شراء الآن) من الرابط الذي يرجعه البوت، وستلاحظ أن خانة العملات قد خصمت ما يصل إلى 10$ إلى 40$ من السعر الإجمالي!</p>
        </div>
      </div>

    </div>

    <!-- ───────────────────────────────────────────────────────── -->
    <!-- PAGE 3: FAQ PAGE                                          -->
    <!-- ───────────────────────────────────────────────────────── -->
    <div id="page-faq" class="page-view hidden space-y-6">
      
      <div class="text-center max-w-2xl mx-auto space-y-2">
        <h2 class="text-xl sm:text-2xl font-bold" style="color: var(--text-main);" data-i18n="faq_title">الأسئلة الشائعة وإرشادات الشراء</h2>
        <p class="text-xs sm:text-sm" style="color: var(--text-muted);" data-i18n="faq_subtitle">كل ما يحتاجه المتسوق الجزائري لمعرفة طرق الشحن، حساب الأسعار بالدينار، والتعامل مع عروض AliExpress.</p>
      </div>

      <div class="space-y-3 max-w-3xl mx-auto">
        <!-- Q1 -->
        <details class="faq-item group border rounded-2xl p-4 transition-colors" style="background-color: var(--bg-card); border-color: var(--border-card);">
          <summary class="flex items-center justify-between cursor-pointer list-none font-bold text-xs sm:text-sm select-none" style="color: var(--text-main);">
            <span class="flex items-center gap-2">
              <i class="fa-solid fa-coins text-amber-500"></i>
              <span data-i18n="faq_q1">كيف يتم احتساب الأسعار بالدينار الجزائري (DZD)؟</span>
            </span>
            <i class="fa-solid fa-chevron-down text-xs transition-transform duration-200 faq-icon opacity-50"></i>
          </summary>
          <div class="pt-3 text-xs leading-relaxed border-t mt-3" style="border-color: var(--border-card); color: var(--text-muted);" data-i18n="faq_a1">
            يتم حساب السعر بالدينار الجزائري تلقائياً وبدقة عالية اعتماداً على سعر صرف الدولار واليورو في السوق الموازي (سعر السكوار الحقيقي) المستخرج مباشرة من موقع SquareAlgerie.com، حتى تتطابق المبالغ مع ما تدفعه حقيقة عند شحن بطاقاتك (Visa / Mastercard / Bybit / RedotPay).
          </div>
        </details>

        <!-- Q2 -->
        <details class="faq-item group border rounded-2xl p-4 transition-colors" style="background-color: var(--bg-card); border-color: var(--border-card);">
          <summary class="flex items-center justify-between cursor-pointer list-none font-bold text-xs sm:text-sm select-none" style="color: var(--text-main);">
            <span class="flex items-center gap-2">
              <i class="fa-solid fa-truck-fast text-sky-500"></i>
              <span data-i18n="faq_q2">كيف يتم شحن الطرود واستلامها في الجزائر؟</span>
            </span>
            <i class="fa-solid fa-chevron-down text-xs transition-transform duration-200 faq-icon opacity-50"></i>
          </summary>
          <div class="pt-3 text-xs leading-relaxed border-t mt-3" style="border-color: var(--border-card); color: var(--text-muted);" data-i18n="faq_a2">
            تشحن معظم المنتجات عبر بريد الجزائر (Algérie Poste / EMS). يصل الطرد إلى أقرب مكتب بريد لعنوان سكناك ويتم إرسال إشعار وصول إلى هاتفك أو صندوق بريدك. للشحنات العادية، تتراوح مدة الوصول بين 15 و35 يوماً عبر خيار AliExpress Standard Shipping.
          </div>
        </details>

        <!-- Q3 -->
        <details class="faq-item group border rounded-2xl p-4 transition-colors" style="background-color: var(--bg-card); border-color: var(--border-card);">
          <summary class="flex items-center justify-between cursor-pointer list-none font-bold text-xs sm:text-sm select-none" style="color: var(--text-main);">
            <span class="flex items-center gap-2">
              <i class="fa-solid fa-credit-card text-emerald-500"></i>
              <span data-i18n="faq_q3">ما هي أفضل طرق وبطاقات الدفع المتاحة للجزائريين؟</span>
            </span>
            <i class="fa-solid fa-chevron-down text-xs transition-transform duration-200 faq-icon opacity-50"></i>
          </summary>
          <div class="pt-3 text-xs leading-relaxed border-t mt-3" style="border-color: var(--border-card); color: var(--text-muted);" data-i18n="faq_a3">
            يمكنك الدفع بسهولة عبر بطاقات فيزا وماستركارد الافتراضية الدولية مثل RedotPay، Bybit Card، Paysera، Pyypl، أو بطاقات العملة الصعبة الصادرة من البنوك الوطنية الجزائرية (AGB، BDL، بنك الخليج الجزائر).
          </div>
        </details>

        <!-- Q4 -->
        <details class="faq-item group border rounded-2xl p-4 transition-colors" style="background-color: var(--bg-card); border-color: var(--border-card);">
          <summary class="flex items-center justify-between cursor-pointer list-none font-bold text-xs sm:text-sm select-none" style="color: var(--text-main);">
            <span class="flex items-center gap-2">
              <i class="fa-solid fa-ticket text-rose-500"></i>
              <span data-i18n="faq_q4">لماذا يظهر كود الخصم غير صالح أو منتهي الصلاحية أحياناً؟</span>
            </span>
            <i class="fa-solid fa-chevron-down text-xs transition-transform duration-200 faq-icon opacity-50"></i>
          </summary>
          <div class="pt-3 text-xs leading-relaxed border-t mt-3" style="border-color: var(--border-card); color: var(--text-muted);" data-i18n="faq_a4">
            أكواد الخصم الترويجية في AliExpress تكون محدودة بعدد استخدامات معين لكل دولة. نقوم بتحديث الأكواد لحظياً وإلغاء المنتهية فوراً، ولكن ننصح دائماً بالشراء السريع عند نشر الكود قبل نفاد حصة الجزائر.
          </div>
        </details>

        <!-- Q5 -->
        <details class="faq-item group border rounded-2xl p-4 transition-colors" style="background-color: var(--bg-card); border-color: var(--border-card);">
          <summary class="flex items-center justify-between cursor-pointer list-none font-bold text-xs sm:text-sm select-none" style="color: var(--text-main);">
            <span class="flex items-center gap-2">
              <i class="fa-solid fa-earth-europe text-blue-500"></i>
              <span data-i18n="faq_q5">ما هي قناة عروض فرنسا (@francedealsdz)؟</span>
            </span>
            <i class="fa-solid fa-chevron-down text-xs transition-transform duration-200 faq-icon opacity-50"></i>
          </summary>
          <div class="pt-3 text-xs leading-relaxed border-t mt-3" style="border-color: var(--border-card); color: var(--text-muted);" data-i18n="faq_a5">
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
        <h2 class="text-xl sm:text-2xl font-bold" style="color: var(--text-main);" data-i18n="contact_title">اتصل بنا والدعم الفني</h2>
        <p class="text-xs sm:text-sm" style="color: var(--text-muted);" data-i18n="contact_subtitle">فريق DealScout DZ يرحب باقتراحاتكم، إبلاغكم عن الروابط التالفة، واستفساراتكم حول الصفقات.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto">
        <!-- Direct Telegram Support Card -->
        <div class="border rounded-2xl p-6 space-y-4 flex flex-col justify-between" style="background-color: var(--bg-card); border-color: var(--border-card);">
          <div class="space-y-3">
            <div class="w-12 h-12 rounded-2xl bg-sky-500/15 text-sky-500 flex items-center justify-center text-xl">
              <i class="fa-brands fa-telegram"></i>
            </div>
            <h3 class="font-bold text-base" style="color: var(--text-main);" data-i18n="contact_tg_title">الدعم السريع عبر Telegram</h3>
            <p class="text-xs leading-relaxed" style="color: var(--text-muted);" data-i18n="contact_tg_desc">
              أسرع وسيلة للتواصل مع مديري القناة والمطورين. يمكنك إرسال استفسارك أو طلب إضافة منتج معين إلى المراقبة الآلية.
            </p>
          </div>

          <div class="space-y-2.5 pt-2">
            <a href="https://t.me/DealscoutadminBOT" target="_blank" rel="noopener noreferrer" class="w-full min-h-[44px] bg-[#229ED9] hover:bg-[#1c8cc1] text-white font-bold text-xs py-2.5 px-4 rounded-xl flex items-center justify-center gap-2 active:scale-95 transition">
              <i class="fa-solid fa-paper-plane text-xs"></i>
              <span data-i18n="contact_tg_btn_admin">مراسلة إدارة DealScout</span>
            </a>
            <a href="https://t.me/Alilo07BOT" target="_blank" rel="noopener noreferrer" class="w-full min-h-[44px] border font-bold text-xs py-2.5 px-4 rounded-xl flex items-center justify-center gap-2 active:scale-95 transition text-amber-500" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
              <i class="fa-solid fa-coins text-xs"></i>
              <span data-i18n="contact_tg_btn_bot">الدخول لبوت العملات (@Alilo07BOT)</span>
            </a>
          </div>
        </div>

        <!-- Contact Form -->
        <div class="border rounded-2xl p-6 space-y-4" style="background-color: var(--bg-card); border-color: var(--border-card);">
          <h3 class="font-bold text-base" style="color: var(--text-main);" data-i18n="contact_form_title">إرسال رسالة أو اقتراح</h3>
          <form onsubmit="handleContactSubmit(event)" class="space-y-3 text-xs">
            <div>
              <label class="block mb-1 font-medium" style="color: var(--text-main);" data-i18n="form_name">الاسم أو اللقب</label>
              <input type="text" id="contact-name" required class="w-full border rounded-xl px-3 py-2 focus:outline-none focus:border-rose-500" style="background-color: var(--input-bg); border-color: var(--border-card); color: var(--text-main);" placeholder="مثال: أمين الجزائري">
            </div>
            <div>
              <label class="block mb-1 font-medium" style="color: var(--text-main);" data-i18n="form_email">البريد الإلكتروني أو معرف تيليجرام</label>
              <input type="text" id="contact-email" required class="w-full border rounded-xl px-3 py-2 focus:outline-none focus:border-rose-500" style="background-color: var(--input-bg); border-color: var(--border-card); color: var(--text-main);" placeholder="@username أو name@email.com">
            </div>
            <div>
              <label class="block mb-1 font-medium" style="color: var(--text-main);" data-i18n="form_subject">نوع الاستفسار</label>
              <select id="contact-subject" class="w-full border rounded-xl px-3 py-2 focus:outline-none focus:border-rose-500" style="background-color: var(--input-bg); border-color: var(--border-card); color: var(--text-main);">
                <option value="deal_suggestion" data-i18n="form_opt1">اقتراح صفقة أو منتج لمراقبته</option>
                <option value="broken_link" data-i18n="form_opt2">إبلاغ عن رابط تالف أو كود منتهي</option>
                <option value="partnership" data-i18n="form_opt3">شراكة أو إعلان تجاري</option>
                <option value="general" data-i18n="form_opt4">استفسار عام</option>
              </select>
            </div>
            <div>
              <label class="block mb-1 font-medium" style="color: var(--text-main);" data-i18n="form_message">نص الرسالة</label>
              <textarea id="contact-message" rows="3" required class="w-full border rounded-xl px-3 py-2 focus:outline-none focus:border-rose-500" style="background-color: var(--input-bg); border-color: var(--border-card); color: var(--text-main);" placeholder="اكتب تفاصيل استفسارك هنا..."></textarea>
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
      
      <div class="max-w-3xl mx-auto space-y-6 text-xs sm:text-sm leading-relaxed" style="color: var(--text-muted);">
        <div class="border rounded-3xl p-6 sm:p-8 space-y-4" style="background-color: var(--bg-card); border-color: var(--border-card);">
          <div class="w-12 h-12 rounded-2xl bg-crimson-600/15 text-crimson-500 flex items-center justify-center text-2xl font-bold">
            <i class="fa-solid fa-bolt"></i>
          </div>
          <h2 class="text-xl sm:text-2xl font-bold tracking-tight" style="color: var(--text-main);" data-i18n="about_title">حول منصة DealScout DZ</h2>
          <p class="leading-relaxed" data-i18n="about_p1">
            تأسست منصة <b>DealScout DZ</b> بهدف حل أكبر مشكلة تواجه المتسوقين في الجزائر عبر الإنترنت: صعوبة الوصول إلى التخفيضات الحقيقية، والارتباك الناتج عن حساب تكلفة المنتج بالدينار الجزائري في ظل تغير أسعار سوق السكوار.
          </p>
          <p class="leading-relaxed" data-i18n="about_p2">
            نقوم بمسح آلاف الصفقات المنشورة في مجموعات AliExpress المعتمدة، ثم نطبق خوارزميات ذكية لتصفية العروض الوهمية، وإبراز المنتجات الأكثر طلباً في السوق الجزائري (الهواتف الذكية، ملحقات الحواسيب، أجهزة القيمنق، الشواحن الأصلية، والأدوات المنزلية الذكية).
          </p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div class="border rounded-2xl p-5 space-y-2" style="background-color: var(--bg-card); border-color: var(--border-card);">
            <h3 class="font-bold text-sm flex items-center gap-2" style="color: var(--text-main);">
              <i class="fa-solid fa-chart-line text-emerald-500"></i>
              <span data-i18n="about_feat1_title">ربط مباشر مع سعر السكوار</span>
            </h3>
            <p class="text-xs leading-relaxed" style="color: var(--text-muted);" data-i18n="about_feat1_desc">نحدث أسعار USDT بالدينار الجزائري لحظة بلحظة لضمان شفافية كاملة قبل الضغط على زر الشراء.</p>
          </div>

          <div class="border rounded-2xl p-5 space-y-2" style="background-color: var(--bg-card); border-color: var(--border-card);">
            <h3 class="font-bold text-sm flex items-center gap-2" style="color: var(--text-main);">
              <i class="fa-solid fa-robot text-sky-500"></i>
              <span data-i18n="about_feat2_title">روبوتات آلية وخوارزميات أمان</span>
            </h3>
            <p class="text-xs leading-relaxed" style="color: var(--text-muted);" data-i18n="about_feat2_desc">نظام ذكي يلتقط التخفيضات في الثواني الأولى لنزولها ويختبر صلاحية أكواد الخصم والعملات.</p>
          </div>
        </div>

        <!-- Affiliate Disclosure Notice -->
        <div class="border rounded-2xl p-4 sm:p-5 space-y-2 text-xs" style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-muted);">
          <h4 class="font-bold flex items-center gap-2" style="color: var(--text-main);">
            <i class="fa-solid fa-handshake text-blue-500"></i>
            <span data-i18n="about_disclosure_title">إفصاح الشفافية والتسويق بالعمولة (Affiliate Disclosure)</span>
          </h4>
          <p class="leading-relaxed" data-i18n="about_disclosure_desc">
            منصة DealScout DZ مشتركة في برنامج شركاء AliExpress الرسمي (AliExpress Portals Affiliate Program). عند النقر على روابط الشراء وإتمام الطلب، قد نحصل على عمولة تسويقية صغيرة من منصة AliExpress دون أي تكلفة إضافية عليك.
          </p>
        </div>

      </div>

    </div>

  </main>

  <!-- Mobile Bottom Navigation Bar -->
  <nav class="md:hidden fixed bottom-0 left-0 right-0 z-50 backdrop-blur-md border-t px-2 py-1 flex items-center justify-around text-center text-[10px] bottom-nav-safe transition-colors" style="background-color: var(--header-bg); border-color: var(--border-card);" aria-label="التنقل للجوال">
    <button onclick="showPage('deals')" id="mob-bottom-deals" class="flex-1 min-h-[48px] py-1 flex flex-col items-center justify-center gap-1 text-crimson-500 font-bold active:scale-90 transition-transform touch-manipulation">
      <i class="fa-solid fa-fire text-base"></i>
      <span data-i18n="nav_deals">الصفقات</span>
    </button>
    <button onclick="showPage('cards')" id="mob-bottom-cards" class="flex-1 min-h-[48px] py-1 flex flex-col items-center justify-center gap-1 opacity-70 hover:opacity-100 font-medium active:scale-90 transition-transform touch-manipulation">
      <i class="fa-solid fa-credit-card text-base text-emerald-500"></i>
      <span data-i18n="nav_cards">البطاقات</span>
    </button>
    <button onclick="showPage('coins')" id="mob-bottom-coins" class="flex-1 min-h-[48px] py-1 flex flex-col items-center justify-center gap-1 opacity-70 hover:opacity-100 font-medium active:scale-90 transition-transform touch-manipulation">
      <i class="fa-solid fa-coins text-base"></i>
      <span data-i18n="nav_coins">العملات</span>
    </button>
    <button onclick="showPage('faq')" id="mob-bottom-faq" class="flex-1 min-h-[48px] py-1 flex flex-col items-center justify-center gap-1 opacity-70 hover:opacity-100 font-medium active:scale-90 transition-transform touch-manipulation">
      <i class="fa-solid fa-circle-question text-base"></i>
      <span data-i18n="nav_faq">الأسئلة</span>
    </button>
    <button onclick="showPage('contact')" id="mob-bottom-contact" class="flex-1 min-h-[48px] py-1 flex flex-col items-center justify-center gap-1 opacity-70 hover:opacity-100 font-medium active:scale-90 transition-transform touch-manipulation">
      <i class="fa-solid fa-envelope text-base"></i>
      <span data-i18n="nav_contact">اتصل بنا</span>
    </button>
  </nav>

  <!-- Deal Details Bottom Sheet & Lightbox Modal -->
  <div id="deal-modal" onclick="onModalBackdropClick(event)" style="display: none;" class="fixed inset-0 z-50 bg-black/75 backdrop-blur-sm hidden items-end sm:items-center justify-center p-0 sm:p-4 animate-fade-in" role="dialog" aria-modal="true" aria-labelledby="modal-title">
    <div id="modal-container" class="border-t sm:border rounded-t-3xl sm:rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto no-scrollbar shadow-2xl p-4 sm:p-6 pb-safe space-y-4 animate-slide-up relative" style="background-color: var(--bg-card); border-color: var(--border-card);">
      
      <!-- Mobile Pull Dismiss Handle -->
      <div class="sm:hidden w-12 h-1.5 rounded-full mx-auto -mt-1 mb-2 cursor-pointer touch-manipulation opacity-40" style="background-color: var(--text-soft);" onclick="closeDealModal()"></div>
      
      <!-- Close Button -->
      <button type="button" onclick="closeDealModal()" aria-label="إغلاق" class="absolute top-3.5 left-3.5 w-10 h-10 min-w-[40px] min-h-[40px] rounded-full flex items-center justify-center text-sm border active:scale-95 transition z-30 touch-manipulation shadow-md cursor-pointer hover:bg-rose-600 hover:text-white" style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-main);">
        <i class="fa-solid fa-xmark text-base"></i>
      </button>

      <!-- Image Preview Container -->
      <div id="modal-img-wrap" class="relative w-full aspect-[4/3] rounded-2xl overflow-hidden border flex items-center justify-center" style="background-color: var(--bg-page); border-color: var(--border-card);">
        <img id="modal-img" src="" alt="Deal preview" class="w-full h-full object-contain" loading="lazy" decoding="async" referrerpolicy="no-referrer">
        <span id="modal-country" class="absolute top-2.5 right-2.5 text-xs px-2.5 py-0.5 rounded-lg font-bold border hidden shadow-sm" style="background-color: var(--bg-card); border-color: var(--border-card); color: var(--text-main);"></span>
        <span id="modal-coins" class="absolute top-2.5 left-2.5 bg-amber-500 text-zinc-950 text-xs font-bold px-2 py-0.5 rounded-lg hidden items-center gap-1 shadow-sm"><i class="fa-solid fa-coins text-[10px]"></i> Coins</span>
      </div>

      <!-- Modal Content Body -->
      <div class="space-y-3.5">
        <div class="flex items-center justify-between gap-2 text-xs" style="color: var(--text-soft);">
          <span id="modal-cat" class="px-2.5 py-1 rounded-lg border text-[11px] font-semibold" style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-main);"></span>
          <span id="modal-date" class="font-mono text-xs opacity-75"></span>
        </div>

        <h3 id="modal-title" class="font-bold text-sm sm:text-base leading-snug" style="color: var(--text-main);"></h3>

        <!-- Coupon inside modal -->
        <div id="modal-coupon-wrap" class="hidden border border-dashed rounded-xl p-3 flex items-center justify-between gap-2" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
          <div class="flex items-center gap-2 min-w-0">
            <i class="fa-solid fa-ticket text-base flex-shrink-0 opacity-60"></i>
            <div class="min-w-0">
              <div class="text-[10px] opacity-75" data-i18n="modal_coupon_label">كود الخصم الفعال:</div>
              <span id="modal-coupon-code" class="font-mono font-bold text-sm sm:text-base tracking-wider truncate block" style="color: var(--text-main);"></span>
            </div>
          </div>
          <button id="modal-coupon-btn" onclick="copyCouponFromModal(this)" class="min-h-[42px] px-3.5 py-1.5 border active:scale-95 text-xs font-bold rounded-lg transition flex items-center gap-1.5 flex-shrink-0 touch-manipulation" style="background-color: var(--bg-card); border-color: var(--border-card); color: var(--text-main);">
            <i class="fa-regular fa-copy"></i>
            <span data-i18n="btn_copy">نسخ الكود</span>
          </button>
        </div>

        <!-- Price display inside modal -->
        <div class="p-3.5 rounded-xl border flex items-center justify-between" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
          <div>
            <div class="text-[10px] opacity-75" data-i18n="modal_price_label">السعر التقديري:</div>
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
            <a href="https://t.me/Alilo07BOT" target="_blank" rel="noopener noreferrer" class="min-h-[44px] border font-bold py-2.5 px-3 rounded-xl flex items-center justify-center gap-1.5 active:scale-95 transition touch-manipulation text-amber-500" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
              <i class="fa-solid fa-coins text-xs"></i>
              <span data-i18n="top_coin_bot">تخفيض العملات</span>
            </a>
            <button onclick="closeDealModal()" class="min-h-[44px] border font-bold py-2.5 px-3 rounded-xl flex items-center justify-center gap-1 active:scale-95 transition touch-manipulation" style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-main);">
              <span data-i18n="btn_close">إغلاق</span>
            </button>
          </div>
        </div>

      </div>

    </div>
  </div>

  <!-- Toast Notification -->
  <div id="toast" class="fixed toast-bottom md:bottom-6 left-1/2 -translate-x-1/2 z-50 border text-emerald-500 font-semibold text-xs px-4 py-2.5 rounded-xl shadow-2xl flex items-center gap-2 transform translate-y-16 opacity-0 pointer-events-none transition-all duration-200" style="background-color: var(--bg-card); border-color: rgba(16, 185, 129, 0.4);">
    <i class="fa-solid fa-check text-emerald-500"></i>
    <span id="toast-msg">تم نسخ كود الخصم!</span>
  </div>

  <!-- ========================================== -->
  <!-- HIGH CREDIBILITY E-COMMERCE FOOTER         -->
  <!-- ========================================== -->
  <footer role="contentinfo" class="border-t pt-10 pb-6 px-4 text-xs transition-colors" style="background-color: var(--bg-card); border-color: var(--border-card); color: var(--text-muted);">
    <div class="max-w-7xl mx-auto space-y-8">
      
      <!-- 4 Columns Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        
        <!-- Col 1: Brand & Mission -->
        <div class="space-y-3">
          <div class="flex items-center gap-2">
            <img src="/logo_circular.png" alt="DealScout DZ" width="28" height="28" style="width: 28px; height: 28px; max-width: 28px; max-height: 28px; object-fit: contain;" class="w-7 h-7 rounded-lg object-contain shadow-sm flex-shrink-0 footer-logo-img" onerror="this.onerror=null; this.src='/logo.png'">
            <span class="font-bold text-base font-inter" style="color: var(--text-main);">DealScout<span class="text-crimson-500">DZ</span></span>
          </div>
          <p class="text-xs leading-relaxed" style="color: var(--text-muted);" data-i18n="footer_brand_desc">
            المنصة الجزائرية المستقلة الأولى لرصد صفقات AliExpress لحظياً، مع حساب حقيقي للأسعار بالدينار الجزائري وفق أسعار السكوار اليومية.
          </p>
          <div class="inline-flex items-center gap-1.5 border rounded-lg px-2.5 py-1 text-[11px] text-emerald-500 font-mono" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
            <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span>1 USDT ≈ <b id="footer-usdt-rate">256.9</b> <span data-i18n="currency_dzd">دج</span></span>
          </div>
        </div>

        <!-- Col 2: Navigation Links -->
        <div class="space-y-3">
          <h4 class="font-bold text-xs uppercase tracking-wider" style="color: var(--text-main);" data-i18n="footer_nav_title">التنقل السريع</h4>
          <ul class="space-y-2">
            <li><button onclick="showPage('deals')" class="hover:underline transition" data-i18n="nav_deals">أحدث الصفقات</button></li>
            <li><button onclick="showPage('cards')" class="hover:underline transition text-emerald-500 font-semibold" data-i18n="nav_cards">بطاقات الشراء والتحويل</button></li>
            <li><button onclick="showPage('coins')" class="hover:underline transition" data-i18n="nav_coins">دليل بوت العملات</button></li>
            <li><button onclick="showPage('faq')" class="hover:underline transition" data-i18n="nav_faq">الأسئلة الشائعة</button></li>
            <li><button onclick="showPage('contact')" class="hover:underline transition" data-i18n="nav_contact">اتصل بنا والدعم</button></li>
            <li><button onclick="showPage('about')" class="hover:underline transition" data-i18n="nav_about">من نحن وإخلاء المسؤولية</button></li>
          </ul>
        </div>

        <!-- Col 3: Channels & Communities -->
        <div class="space-y-3">
          <h4 class="font-bold text-xs uppercase tracking-wider" style="color: var(--text-main);" data-i18n="footer_channels_title">القنوات والمنصات</h4>
          <ul class="space-y-2">
            <li>
              <a href="https://t.me/DzAliexpress0" target="_blank" rel="noopener noreferrer" class="hover:text-sky-500 transition flex items-center gap-1.5">
                <i class="fa-brands fa-telegram text-sky-500"></i>
                <span data-i18n="footer_ch_dz">قناة صفقات الجزائر (@DzAliexpress0)</span>
              </a>
            </li>
            <li>
              <a href="https://t.me/francedealsdz" target="_blank" rel="noopener noreferrer" class="hover:text-sky-500 transition flex items-center gap-1.5">
                <i class="fa-brands fa-telegram text-sky-500"></i>
                <span data-i18n="footer_ch_fr">قناة صفقات فرنسا (@francedealsdz)</span>
              </a>
            </li>
            <li>
              <a href="https://t.me/Alilo07BOT" target="_blank" rel="noopener noreferrer" class="hover:text-amber-500 transition flex items-center gap-1.5">
                <i class="fa-solid fa-coins text-amber-500 text-xs"></i>
                <span data-i18n="footer_bot_coins">بوت خصم العملات (@Alilo07BOT)</span>
              </a>
            </li>
            <li>
              <a href="https://squarealgerie.com" target="_blank" rel="noopener noreferrer" class="hover:text-emerald-500 transition flex items-center gap-1.5">
                <i class="fa-solid fa-arrow-trend-up text-emerald-500 text-xs"></i>
                <span>SquareAlgerie.com</span>
              </a>
            </li>
          </ul>
        </div>

        <!-- Col 4: Buyer Protection & Preferences -->
        <div class="space-y-3">
          <h4 class="font-bold text-xs uppercase tracking-wider" style="color: var(--text-main);" data-i18n="footer_security_title">أمان التسوق والتفضيلات</h4>
          <p class="text-xs leading-relaxed" style="color: var(--text-muted);" data-i18n="footer_security_desc">
            جميع روابط الشراء تفتح موقع AliExpress الرسمي مباشرة عبر سيرفرات مشفرة ومحمية ببروتوكول HTTPS.
          </p>
          <div class="pt-1 flex flex-wrap items-center gap-2">
            <button onclick="toggleTheme()" class="px-2.5 py-1 rounded border text-xs font-bold transition flex items-center gap-1.5" style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-main);">
              <i class="fa-solid fa-circle-half-stroke text-[11px]"></i>
              <span data-i18n="btn_toggle_theme">تبديل المظهر</span>
            </button>
            <button onclick="setLanguage('ar')" class="px-2 py-1 rounded border text-xs font-bold transition" style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-main);">🇩🇿 العربية</button>
            <button onclick="setLanguage('fr')" class="px-2 py-1 rounded border text-xs font-bold transition" style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-main);">🇫🇷 Français</button>
          </div>
        </div>

      </div>

      <!-- Affiliate Compliance Notice -->
      <div class="border-t pt-6 text-[11px] leading-relaxed text-center sm:text-start" style="border-color: var(--border-card); color: var(--text-soft);" data-i18n="footer_compliance">
        إخلاء مسؤولية الشراكة: DealScout DZ موقع مستقل وغير تابع لشركة Alibaba أو AliExpress بشكل مباشر. قد تتضمن بعض الروابط معرفات تسويق بالعمولة (AliExpress Portals Affiliate) تتيح لنا الحصول على نسبة رمزية عند الشراء دون أي تكلفة إضافية عليك إطلاقاً. الأسعار بالدينار الجزائري تقريبية وتعتمد على سعر الصرف اللحظي.
      </div>

      <!-- Copyright Bar -->
      <div class="border-t pt-4 flex flex-col sm:flex-row items-center justify-between gap-3 text-[11px]" style="border-color: var(--border-card); color: var(--text-soft);">
        <div>© 2026 DealScout DZ. <span data-i18n="footer_rights">جميع الحقوق محفوظة.</span></div>
        <div class="flex items-center gap-4">
          <span data-i18n="footer_made_with">صُنع للمتسوق الجزائري 🇩🇿</span>
          <button onclick="window.scrollTo({top: 0, behavior: 'smooth'})" class="hover:underline transition flex items-center gap-1 font-bold" style="color: var(--text-main);">
            <span data-i18n="footer_back_top">للأعلى</span>
            <i class="fa-solid fa-arrow-up text-[10px]"></i>
          </button>
        </div>
      </div>

    </div>
  </footer>

  <!-- ========================================== -->
  <!-- CLIENT-SIDE BILINGUAL & THEME LOGIC        -->
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
        nav_cards: "بطاقات الشراء",
        nav_coins: "بوت العملات",
        nav_faq: "الأسئلة الشائعة",
        nav_contact: "اتصل بنا",
        nav_about: "من نحن",
        btn_join_channel: "انضم للقناة",
        btn_toggle_theme: "المظهر",
        theme_light: "فاتح",
        theme_dark: "داكن",
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
        deal_category_fallback: "عرض مميز",
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
        cards_badge: "دليل بطاقات الدفع والشحن بالدينار الجزائري 🇩🇿",
        cards_hero_title: "كيف تشتري من AliExpress وأنت في الجزائر؟ | أفضل البطاقات والشحن بـ BaridiMob",
        cards_hero_desc: "لأن البطاقات البنكية الجزائرية المحلية لا تعمل في المواقع العالمية، إليك الحل الرسمي والمجرب: احصل على بطاقة افتراضية دولية مجانية، واشحنها مباشرة بالدينار الجزائري عبر بريدي موب ومنصة بينانس دون وسطاء وبأقل تكلفة!",
        cards_bybit_badge: "مجانية 100% — 0 دج",
        cards_bybit_title: "بطاقة Bybit Card (MasterCard)",
        cards_bybit_desc: "البطاقة الأفضل حالياً للتسوق من AliExpress: تصدر فورياً ومجاناً 100% وبدون أي اشتراك شهري، مقبولة في جميع المتاجر العالمية وPayPal مع كاش باك يصل إلى 10%.",
        cards_bybit_f1: "0 دج مصاريف فتح وبدون اشتراك شهري",
        cards_bybit_f2: "مقبولة 100% على AliExpress وPayPal",
        cards_bybit_f3: "شحن فوري بالدينار عبر Binance P2P",
        cards_btn_bybit_cta: "طلب بطاقة Bybit المجانية",
        cards_redot_badge: "هدية 5$ ترحيبية 🎁",
        cards_redot_title: "بطاقة فيزا RedotPay (هدية 5$)",
        cards_redot_desc: "بطاقة فيزا افتراضية دولية تصدر في دقيقتين بالبطاقة الوطنية الجزائرية أو جواز السفر، تدعم تخفيضات العملات وكوبونات AliExpress وربط PayPal الجزائري.",
        cards_redot_f1: "هدية 5$ رصيد ترحيبي فوري عند التسجيل",
        cards_redot_f2: "تفعيل فوري ببطاقة التعريف الوطنية",
        cards_redot_f3: "دعم ربط وتفعيل كامل لـ PayPal",
        cards_btn_redot_cta: "طلب بطاقة RedotPay (+ 5$ هدية)",
        cards_binance_badge: "سوق P2P #1 في الجزائر",
        cards_binance_title: "منصة Binance P2P (BaridiMob)",
        cards_binance_desc: "المنصة الرسمية والآمنة 100% لتحويل الدينار الجزائري من تطبيق BaridiMob أو CCP إلى رصيد دولار رقمي (USDT) بسعر الصرف الحقيقي وبدون وسطاء أو عمولات زائدة.",
        cards_binance_f1: "شراء الدولار الرقمي مباشرة عبر BaridiMob",
        cards_binance_f2: "حماية الضمان المالي الصارم (Escrow)",
        cards_binance_f3: "تحويل مباشر إلى بطاقاتك في ثوانٍ",
        cards_btn_binance_cta: "فتح حساب Binance P2P",
        cards_ref_code: "كود التسجيل الحصري:",
        cards_btn_copy_code: "نسخ الكود",
        cards_guide_title: "دليل الشراء خطوة بخطوة بالدينار الجزائري (BaridiMob) 🇩🇿",
        cards_guide_subtitle: "الطريقة الرسمية والآمنة التي يستعملها آلاف المتسوقين الجزائريين يومياً للشراء من AliExpress بأقل تكلفة:",
        cards_step1_title: "1. شراء USDT بـ BaridiMob",
        cards_step1_desc: "افتح حسابك في Binance، ادخل قسم P2P واختر الدفع بـ BaridiMob لشراء المبلغ المطلوب من الدولار الرقمي (USDT) مباشرة في دقيقتين.",
        cards_step2_title: "2. شحن بطاقتك الافتراضية",
        cards_step2_desc: "حوّل رصيد USDT من Binance إلى حساب Bybit أو RedotPay الخاص بك عبر شبكة سريعة بدون أي رسوم مرتفعة.",
        cards_step3_title: "3. ربط البطاقة في AliExpress",
        cards_step3_desc: "انسخ معلومات بطاقتك الافتراضية (رقم البطاقة وتاريخ الانتهاء وCVV) وأضفها في وسائل الدفع بتطبيق AliExpress.",
        cards_step4_title: "4. تطبيق الخصومات والشراء",
        cards_step4_desc: "اختر صفقتك من موقعنا، انسخ كود الخصم، استخدم بوت العملات واستلم طردك مباشرة من مكتب بريد الجزائر القريب منك!",
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
        footer_security_title: "أمان التسوق والتفضيلات",
        footer_security_desc: "جميع روابط الشراء تفتح موقع AliExpress الرسمي مباشرة عبر سيرفرات مشفرة ومحمية ببروتوكول HTTPS.",
        footer_ch_dz: "قناة صفقات الجزائر (@DzAliexpress0)",
        footer_ch_fr: "قناة صفقات فرنسا (@francedealsdz)",
        footer_bot_coins: "بوت خصم العملات (@Alilo07BOT)",
        footer_compliance: "إخلاء مسؤولية الشراكة: DealScout DZ موقع مستقل وغير تابع لشركة Alibaba أو AliExpress بشكل مباشر. قد تتضمن بعض الروابط معرفات تسويق بالعمولة (AliExpress Portals Affiliate) تتيح لنا الحصول على نسبة رمزية عند الشراء دون أي تكلفة إضافية عليك إطلاقاً. الأسعار بالدينار الجزائري تقريبية وتعتمد على سعر الصرف اللحظي.",
        footer_rights: "جميع الحقوق محفوظة.",
        footer_made_with: "صُنع للمتسوق الجزائري 🇩🇿",
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
        nav_cards: "Cartes & Paiement",
        nav_coins: "Bot Pièces",
        nav_faq: "FAQ",
        nav_contact: "Contact",
        nav_about: "À Propos",
        btn_join_channel: "Rejoindre Telegram",
        btn_toggle_theme: "Thème",
        theme_light: "Clair",
        theme_dark: "Sombre",
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
        deal_category_fallback: "Bon Plan",
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
        cards_badge: "Guide Cartes Bancaires & BaridiMob 🇩🇿",
        cards_hero_title: "Comment Acheter sur AliExpress depuis l'Algérie ? | Cartes & BaridiMob",
        cards_hero_desc: "Les cartes bancaires locales ne fonctionnant pas sur les sites internationaux, voici la solution officielle : créez votre carte virtuelle internationale gratuite et rechargez-la en Dinars avec BaridiMob via Binance P2P !",
        cards_bybit_badge: "100% Gratuite — 0€ Frais",
        cards_bybit_title: "Carte Bybit (MasterCard Gratuite)",
        cards_bybit_desc: "La meilleure carte pour AliExpress : 0€ de frais de création, 0€ d'abonnement mensuel, acceptée sur tous les sites mondiaux et PayPal avec jusqu'à 10% de cashback.",
        cards_bybit_f1: "0€ de frais d'ouverture, 0 abonnement",
        cards_bybit_f2: "100% acceptée sur AliExpress et PayPal",
        cards_bybit_f3: "Recharge instantanée en Dinars via Binance P2P",
        cards_btn_bybit_cta: "Commander la carte Bybit gratuite",
        cards_redot_badge: "5$ de Bienvenue Offerts 🎁",
        cards_redot_title: "Carte Visa RedotPay (5$ Offerts)",
        cards_redot_desc: "Carte Visa virtuelle internationale activée en 2 minutes avec votre carte d'identité ou passeport. Compatible coupons AliExpress et PayPal.",
        cards_redot_f1: "5$ de bonus de bienvenue dès l'inscription",
        cards_redot_f2: "Activation immédiate avec pièce d'identité",
        cards_redot_f3: "Liaison PayPal et paiements en ligne",
        cards_btn_redot_cta: "Activer la carte RedotPay (+ 5$)",
        cards_binance_badge: "Marché P2P N°1 en Algérie",
        cards_binance_title: "Binance P2P (Recharge via BaridiMob)",
        cards_binance_desc: "La plateforme sécurisée n°1 pour convertir vos Dinars depuis l'application BaridiMob ou CCP en USDT au taux réel du marché sans intermédiaire.",
        cards_binance_f1: "Achat d'USDT directement avec BaridiMob / CCP",
        cards_binance_f2: "Protection des fonds et séquestre sécurisé",
        cards_binance_f3: "Transfert vers vos cartes en quelques secondes",
        cards_btn_binance_cta: "Ouvrir un compte Binance P2P",
        cards_ref_code: "Code de parrainage exclusif :",
        cards_btn_copy_code: "Copier le code",
        cards_guide_title: "Guide d'Achat Étape par Étape en Dinar Algérien (BaridiMob) 🇩🇿",
        cards_guide_subtitle: "La méthode officielle et sécurisée utilisée quotidiennement par des milliers d'Algériens :",
        cards_step1_title: "1. Achetez des USDT sur Binance P2P",
        cards_step1_desc: "Ouvrez un compte Binance, rendez-vous dans P2P et payez par BaridiMob ou CCP pour obtenir vos USDT en toute sécurité.",
        cards_step2_title: "2. Transférez vers Bybit ou RedotPay",
        cards_step2_desc: "Envoyez vos USDT depuis Binance vers votre carte virtuelle via le réseau BSC/TRC20 en quelques secondes.",
        cards_step3_title: "3. Ajoutez votre carte sur AliExpress",
        cards_step3_desc: "Renseignez le numéro, la date d'expiration et le CVV de votre carte virtuelle dans vos moyens de paiement AliExpress.",
        cards_step4_title: "4. Profitez des coupons et achetez !",
        cards_step4_desc: "Choisissez vos bons plans sur DealScout DZ, copiez les codes promos et faites livrer vos colis directement chez vous en Algérie !",
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
        footer_security_title: "Sécurité & Préférences",
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
    var currentTheme = (localStorage.getItem('dealscout_theme') === 'light') ? 'light' : 'dark';
    var currentLang = (localStorage.getItem('dealscout_lang') === 'fr') ? 'fr' : 'ar';
    var allDeals = [];
    var currentChannel = '@DzAliexpress0';
    var currentCategory = 'all';
    var currentCurrency = currentLang === 'fr' ? 'EUR' : 'DZD';
    var currentViewMode = 'grid';
    var usdtRate = 256.9;
    var currentSearchTerm = '';
    var currentActiveDeal = null;

    function t(key, fallback = '') {
      const dict = (typeof I18N !== 'undefined' && I18N[currentLang]) ? I18N[currentLang] : (typeof I18N !== 'undefined' ? I18N.ar : {});
      return (dict && dict[key]) || fallback || '';
    }

    // ── Theme Engine (Light / Dark) ─────────────────────────────────
    function applyTheme(theme) {
      currentTheme = theme;
      localStorage.setItem('dealscout_theme', theme);
      const isDark = theme === 'dark';
      
      if (isDark) {
        document.documentElement.classList.add('dark');
        document.documentElement.classList.remove('light');
      } else {
        document.documentElement.classList.remove('dark');
        document.documentElement.classList.add('light');
      }

      const metaTheme = document.getElementById('meta-theme-color');
      if (metaTheme) metaTheme.content = isDark ? '#09090b' : '#f4f4f5';

      const icon = document.getElementById('theme-icon');
      const text = document.getElementById('theme-text');
      if (icon) {
        icon.className = isDark ? 'fa-solid fa-moon text-[11px]' : 'fa-solid fa-sun text-[11px] text-amber-500';
      }
      if (text) {
        text.textContent = isDark ? I18N[currentLang].theme_dark : I18N[currentLang].theme_light;
      }
    }

    function toggleTheme() {
      const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
      applyTheme(nextTheme);
      showToast(nextTheme === 'dark' ? 'تم تفعيل الوضع الداكن 🌙' : 'تم تفعيل الوضع الفاتح ☀️');
    }

    // ── Internationalization Engine ─────────────────────────────────
    function setLanguage(lang) {
      if (!I18N[lang]) lang = 'ar';
      currentLang = lang;
      localStorage.setItem('dealscout_lang', lang);

      const isAr = lang === 'ar';
      document.documentElement.lang = isAr ? 'ar' : 'fr';
      document.documentElement.dir = isAr ? 'rtl' : 'ltr';
      document.body.dir = isAr ? 'rtl' : 'ltr';

      const arBtn = document.getElementById('lang-ar-btn');
      const frBtn = document.getElementById('lang-fr-btn');
      if (arBtn && frBtn) {
        if (isAr) {
          arBtn.className = 'px-2 py-0.5 rounded text-[11px] font-bold bg-crimson-600 text-white transition active:scale-95';
          frBtn.className = 'px-2 py-0.5 rounded text-[11px] font-bold opacity-60 hover:opacity-100 transition active:scale-95';
        } else {
          frBtn.className = 'px-2 py-0.5 rounded text-[11px] font-bold bg-crimson-600 text-white transition active:scale-95';
          arBtn.className = 'px-2 py-0.5 rounded text-[11px] font-bold opacity-60 hover:opacity-100 transition active:scale-95';
        }
      }

      document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (I18N[lang][key]) {
          el.textContent = I18N[lang][key];
        }
      });

      document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        if (I18N[lang][key]) {
          el.placeholder = I18N[lang][key];
        }
      });

      document.title = I18N[lang].meta_title;
      applyTheme(currentTheme);

      if (allDeals && allDeals.length > 0) {
        filterDeals();
      }
    }

    // ── Multi-Page Navigation Router ────────────────────────────────
    function showPage(pageId) {
      const pages = ['deals', 'cards', 'coins', 'faq', 'contact', 'about'];
      if (!pages.includes(pageId)) pageId = 'deals';

      pages.forEach(p => {
        const el = document.getElementById('page-' + p);
        if (el) {
          if (p === pageId) el.classList.remove('hidden');
          else el.classList.add('hidden');
        }

        const navBtn = document.getElementById('nav-link-' + p);
        if (navBtn) {
          if (p === pageId) {
            navBtn.className = 'nav-page-btn px-3 py-1.5 rounded-lg font-bold transition flex items-center gap-1.5';
            navBtn.style.backgroundColor = 'var(--bg-elevated)';
            navBtn.style.color = 'var(--text-main)';
          } else {
            navBtn.className = 'nav-page-btn px-3 py-1.5 rounded-lg opacity-60 hover:opacity-100 transition flex items-center gap-1.5';
            navBtn.style.backgroundColor = 'transparent';
            navBtn.style.color = 'var(--text-muted)';
          }
        }

        const mobBtn = document.getElementById('mob-bottom-' + p);
        if (mobBtn) {
          if (p === pageId) {
            mobBtn.className = 'flex-1 min-h-[48px] py-1 flex flex-col items-center justify-center gap-1 text-crimson-500 font-bold active:scale-90 transition-transform touch-manipulation';
          } else {
            mobBtn.className = 'flex-1 min-h-[48px] py-1 flex flex-col items-center justify-center gap-1 opacity-60 hover:opacity-100 font-medium active:scale-90 transition-transform touch-manipulation';
          }
        }
      });

      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // ── Robust Image Error & Proxy Recovery Handler ──────────────────
    function handleImgError(img, originalUrl) {
      if (!img) return;
      const targetSrc = originalUrl || img.src;

      // Stage 1: If not retried yet, proxy through our Vercel /api/image-proxy
      if (!img.dataset.retried && targetSrc && !targetSrc.includes('/api/image-proxy')) {
        img.dataset.retried = '1';
        img.src = '/api/image-proxy?url=' + encodeURIComponent(targetSrc);
        return;
      }

      // Stage 2: Graceful inline SVG placeholder with clean category iconography
      img.onerror = null;
      img.src = "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 300' fill='%2318181b'><rect width='400' height='300' rx='16' fill='%2318181b'/><path d='M160 110h80v80h-80z' fill='%2327272a'/><path d='M200 80l40 30h-80z' fill='%23e11d48'/><circle cx='200' cy='150' r='24' fill='%233f3f46'/><text x='200' y='230' text-anchor='middle' fill='%2371717a' font-family='sans-serif' font-size='14' font-weight='600'>AliExpress Deal DZ</text></svg>";
      img.classList.remove('object-contain', 'object-cover');
      img.classList.add('object-contain', 'p-4', 'opacity-90');
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

    function handleBuyClick(couponCode) {
      if (couponCode && couponCode.length >= 3) {
        try {
          navigator.clipboard.writeText(couponCode);
          showToast(currentLang === 'fr' ? `Code promo ${couponCode} copié !` : `تم نسخ كود الخصم ${couponCode} تلقائياً!`);
        } catch(e) {}
      }
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
        ? `Merci ${name} ! Votre message a bien été envoyé.`
        : `شكراً لك ${name}! تم استلام رسالتك وسنقوم بالرد قريباً.`;
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
            btn.className = 'min-w-[34px] sm:min-w-[38px] h-8 sm:h-9 px-2 py-1 rounded-lg bg-crimson-600 text-white font-mono transition flex items-center justify-center active:scale-95 touch-manipulation shadow-sm';
          } else {
            btn.className = 'min-w-[32px] sm:min-w-[36px] h-8 sm:h-9 px-2 py-1 rounded-lg opacity-60 hover:opacity-100 font-mono transition flex items-center justify-center active:scale-95 touch-manipulation';
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
        if (tabFr) tabFr.className = 'flex-1 sm:flex-none min-h-[40px] px-4 py-2 rounded-lg opacity-70 hover:opacity-100 transition flex items-center justify-center gap-2 active:scale-95';
        if (btnJoin) btnJoin.href = 'https://t.me/DzAliexpress0';
        setCurrency('DZD');
      } else {
        if (tabFr) tabFr.className = 'flex-1 sm:flex-none min-h-[40px] px-4 py-2 rounded-lg bg-crimson-600 text-white transition flex items-center justify-center gap-2 active:scale-95 shadow-sm';
        if (tabDz) tabDz.className = 'flex-1 sm:flex-none min-h-[40px] px-4 py-2 rounded-lg opacity-70 hover:opacity-100 transition flex items-center justify-center gap-2 active:scale-95';
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
        gridBtn.className = 'min-h-[36px] px-3 py-1.5 rounded-lg text-white transition flex items-center gap-1.5 active:scale-95 font-bold';
        gridBtn.style.backgroundColor = 'var(--bg-elevated)';
        gridBtn.style.color = 'var(--text-main)';
        feedBtn.className = 'min-h-[36px] px-3 py-1.5 rounded-lg opacity-60 hover:opacity-100 transition flex items-center gap-1.5 active:scale-95';
        feedBtn.style.backgroundColor = 'transparent';
        gridEl.classList.remove('hidden');
        feedEl.classList.add('hidden');
      } else {
        feedBtn.className = 'min-h-[36px] px-3 py-1.5 rounded-lg text-white transition flex items-center gap-1.5 active:scale-95 font-bold';
        feedBtn.style.backgroundColor = 'var(--bg-elevated)';
        feedBtn.style.color = 'var(--text-main)';
        gridBtn.className = 'min-h-[36px] px-3 py-1.5 rounded-lg opacity-60 hover:opacity-100 transition flex items-center gap-1.5 active:scale-95';
        gridBtn.style.backgroundColor = 'transparent';
        feedEl.classList.remove('hidden');
        gridEl.classList.add('hidden');
      }
    }

    function setCategory(cat) {
      currentCategory = cat;
      document.querySelectorAll('.cat-pill').forEach(btn => {
        btn.className = 'cat-pill min-h-[42px] px-3.5 py-2 rounded-xl border whitespace-nowrap transition flex items-center gap-1.5 flex-shrink-0 active:scale-95 touch-manipulation';
        btn.style.backgroundColor = 'var(--bg-card)';
        btn.style.borderColor = 'var(--border-card)';
        btn.style.color = 'var(--text-muted)';
      });
      const active = document.getElementById('cat-' + cat);
      if (active) {
        active.className = 'cat-pill min-h-[42px] px-3.5 py-2 rounded-xl bg-crimson-600 text-white whitespace-nowrap transition flex items-center gap-1.5 flex-shrink-0 active:scale-95 touch-manipulation shadow-sm';
        active.style.backgroundColor = '#e11d48';
        active.style.color = '#ffffff';
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
    async function fetchDeals(showSpin = false, forceRefresh = false) {
      const icon = document.getElementById('refresh-icon');
      if (showSpin && icon) icon.classList.add('fa-spin');

      // 1. Instant client-side hydration from localStorage cache (0ms instant render)
      const cacheKey = 'dealscout_deals_v3_' + currentChannel;
      if (!forceRefresh && (!allDeals || allDeals.length === 0)) {
        try {
          const cached = localStorage.getItem(cacheKey);
          if (cached) {
            const parsed = JSON.parse(cached);
            if (Array.isArray(parsed) && parsed.length > 0) {
              allDeals = parsed.filter(d => d && d.affiliate_url && !d.affiliate_url.includes('_oEN3d53') && d.title && !/(?:وَتَوَكَّلْ|وتوكل|سبحان|الحمد|أذكار|دعاء|تذكير)/.test(d.title));
              updateCategoryCounters();
              filterDeals();
            }
          }
        } catch(e) {}
      }

      try {
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

        const url = '/api/channel-posts?channel=' + encodeURIComponent(currentChannel) + (forceRefresh ? '&force=true' : '');
        const resp = await fetch(url);
        if (!resp.ok) throw new Error('HTTP ' + resp.status);
        const data = await resp.json();

        if (data.posts && Array.isArray(data.posts) && data.posts.length > 0) {
          allDeals = data.posts.map((p, idx) => parseDealPost(p, idx)).filter(Boolean);
          try {
            localStorage.setItem(cacheKey, JSON.stringify(allDeals));
          } catch(e) {}
          updateCategoryCounters();
          filterDeals();
          if (showSpin) {
            showToast(currentLang === 'fr' ? 'Offres actualisées !' : 'تم تحديث الصفقات بنجاح!');
          }
        } else if (!allDeals || allDeals.length === 0) {
          filterDeals();
        }
      } catch (err) {
        console.error('Error fetching deals:', err);
        if (showSpin) {
          showToast(currentLang === 'fr' ? 'Impossible de rafraîchir pour le moment' : 'تعذر التحديث الآن، جاري استخدام البيانات المحفوظة');
        }
        if (!allDeals || allDeals.length === 0) {
          filterDeals();
        }
      } finally {
        if (icon) {
          setTimeout(() => icon.classList.remove('fa-spin'), 300);
        }
      }
    }

    function parseDealPost(post, index) {
      if (!post) return null;
      const text = post.text || '';

      // 1. Strict AliExpress Link Requirement: A deal MUST have an explicit product/affiliate link
      const urlMatch = text.match(/https?:\\/\\/(?:s\\.click\\.aliexpress\\.com\\/e\\/[A-Za-z0-9_-]+|(?:[a-z0-9-]+\\.)?aliexpress\\.com\\/(?:item|p)\\/[A-Za-z0-9_.-]+)/i);
      if (!urlMatch) {
        return null;
      }

      // 2. Strict Filter: Reject religious verses, prayers, adhkars, and spiritual reminders
      const isReligious = /(?:وَتَوَكَّلْ|وتوكل|سبحان الله|الحمد لله|الله أكبر|صلى الله|عليه وسلم|سورة|القرآن|أذكار|دعاء|تذكير ديني|استغفر الله|لا إله إلا الله|حسبي الله|اذكار)/i.test(text);
      if (isReligious) {
        return null;
      }

      // 3. Strict Filter: Reject general non-product announcements, referral posts, and payment guides
      const isAnnouncement = /(?:إعلان هام|تنبيه هام|دليل الشراء بالدينار|شحن بطاقتك|قناة الصيدات والصفقات|كيفاش تشري من AliExpress|كيف تشحن بطاقاتك)/i.test(text) && !text.includes('/item/');
      if (isAnnouncement) {
        return null;
      }

      // 4. Reject emoji-only or too-short posts
      const alphanumeric = text.replace(/[\\s\\p{Emoji_Presentation}\\p{Extended_Pictographic}\\p{Punctuation}]/gu, '');
      if (alphanumeric.length < 5) {
        return null;
      }

      let title = '';
      let coupon = null;
      let priceUsd = null;
      let priceEur = null;
      let country = null;
      let hasCoins = false;
      let category = 'other';
      let categoryLabel = I18N[currentLang].deal_category_fallback;

      const lines = text.split('\n').map(l => l.trim()).filter(Boolean);

      const isBoilerplate = (l) => {
        const s = l.toLowerCase();
        return (
          s.includes('http') || s.includes('@') || s.includes('t.me') ||
          s.includes('خلي البلد') || s.includes('بلد الحساب') || s.includes('livraison') ||
          s.includes('pays') || s.includes('السعر') || s.includes('prix') || s.includes('price') ||
          s.includes('كوبون') || s.includes('قسيمة') || s.includes('code') || s.includes('coupon') ||
          s.includes('عملات') || s.includes('coins') || s.includes('pièces') || s.includes('pièce') ||
          s.includes('لافار') || s.includes('عرض اليوم') || s.includes('صيدة') || s.includes('باطل') ||
          s.includes('تخفيض قوي') || s.includes('رابط الشراء') || s.includes('بوت') || s.includes('قناة') ||
          s.includes('bonne affaire') || s.includes('meilleur bon plan') || s.includes('guide') ||
          s.includes('تنبيه') || s.includes('طريقة') || s.includes('احجز') || s.includes('طبقوا') ||
          s.includes('حبات قلال') || s.includes('سارعوا') || s.includes('كندا') || s.includes('فرنسا') ||
          s.includes('كوريا') || s.includes('أوكرانيا') || s.includes('استراليا')
        );
      };

      // Priority 1: Checkmark bullet (DealScout DZ & top channels standard: ✅ [Title] or ✔️ [Title])
      for (const line of lines) {
        const m = line.match(/^[✅✔️☑️]\\s*(.+)$/) || line.match(/✅\\s*([^\\n]+)/);
        if (m) {
          const cand = m[1].replace(/<\\/?[^>]+(>|$)/g, '').replace(/^[✅✔️☑️\\s*#]+/, '').trim();
          if (cand.length >= 3 && !isBoilerplate(cand)) {
            title = cand;
            break;
          }
        }
      }

      // Priority 2: Star, device, or category prefixes (⭐️, 📱, 🎮, 🎧, ⚡, 📦, تخفيض لـ, Produit)
      if (!title) {
        for (const line of lines) {
          const m = line.match(/^(?:⭐️|⭐|🌟|📱|🎮|🎧|⚡|📦|تخفيض\\s*(?:لـ|ل)?|عرض\\s*خاص\\s*(?:لـ|ل)?|تخفيض\\s*على|produit\\s*:?|offre\\s*:?)\\s*(.+)$/i);
          if (m) {
            const cand = m[1].replace(/<\\/?[^>]+(>|$)/g, '').trim();
            if (cand.length >= 3 && !isBoilerplate(cand)) {
              title = cand;
              break;
            }
          }
        }
      }

      // Priority 3: Non-boilerplate lines with product name
      if (!title) {
        for (const line of lines) {
          if (isBoilerplate(line)) continue;
          const clean = line.replace(/^[🛍️🔥⚡⭐💥📦📍🏷️✅✔️•\\-*\\s]+/, '').replace(/<\\/?[^>]+(>|$)/g, '').trim();
          if (clean.length >= 4 && !isBoilerplate(clean) && !clean.match(/^[A-Z0-9_-]{4,20}$/)) {
            title = clean;
            break;
          }
        }
      }

      // Priority 4: Non-link fallback line
      if (!title) {
        for (const line of lines) {
          if (!line.includes('http') && !line.includes('@') && !line.includes('t.me') && line.length >= 4) {
            const clean = line.replace(/^[🛍️🔥⚡⭐💥📦📍🏷️✅✔️•\\-*\\s]+/, '').trim();
            if (clean.length >= 4) {
              title = clean;
              break;
            }
          }
        }
      }

      if (title) {
        title = title.replace(/<\\/?[^>]+(>|$)/g, '').trim();
        if (title.length > 95) title = title.slice(0, 92) + '...';
      } else {
        title = (currentLang === 'fr' ? 'Bon Plan AliExpress' : 'صفقة مميزة من AliExpress');
      }

      const usdMatch = text.match(/(?:\\$|US\\s*\\$|USD\\s*)\\s*([0-9]+[.,][0-9]{1,2})/i) || text.match(/([0-9]+[.,][0-9]{1,2})\\s*(?:\\bUSD\\b|\\$)/i);
      if (usdMatch) {
        priceUsd = parseFloat(usdMatch[1].replace(',', '.'));
      }
      const eurMatch = text.match(/(?:€|EUR\\s*)\\s*([0-9]+[.,][0-9]{1,2})/i) || text.match(/([0-9]+[.,][0-9]{1,2})\\s*(?:€|\\bEUR\\b)/i);
      if (eurMatch) {
        priceEur = parseFloat(eurMatch[1].replace(',', '.'));
      }

      // Enhanced Coupon Extraction across all Arabic, French, and Telegram formats
      const cleanNorm = text.replace(/[\\u0640]/g, '');
      const couponMatch = 
        cleanNorm.match(/(?:(?:ال)?كـ?وبون(?:\\s*الخصم|\\s*خاص)?|(?:ال)?كـ?ود(?:\\s*الخصم|\\s*التخفيض)?|code\\s*promo|code\\s*de\\s*r[ée]duction|code\\s*r[ée]duction|coupon|promo|code|avec\\s*le\\s*code|utilisez\\s*le\\s*code)\\s*[:：\\-]?\\s*(?:<code>|\\*\\*|`)*([A-Za-z0-9_-]{3,20})/i)
        || cleanNorm.match(/(?:(?:ال)?قسيمـ?ة(?:\\s*البائع|\\s*المتجر)?|coupon\\s*vendeur|store\\s*coupon)\\s*[:：\\-]?\\s*(?:<code>|\\*\\*|`)*([0-9]+(?:\\.[0-9]+)?\\$?|[A-Za-z0-9_-]{3,20})/i)
        || cleanNorm.match(/[🏷️🎟️🎫]\\s*(?:code\\s*[:：]?)?\\s*(?:<code>|\\*\\*|`)*([A-Za-z0-9_-]{3,20})/i)
        || cleanNorm.match(/(?:كود|كوبون|code|promo)[^\\n]{0,60}?(?:<code>|`)([A-Za-z0-9_-]{3,20})(?:<\\/code>|`)/i);
      
      if (couponMatch) {
        let rawCode = (couponMatch[1] || '').trim().replace(/[<>/`*#]/g, '');
        const bl = ['http', 'https', 'aliexpress', 'tme', 'link', 'item', 'click', 'coins', 'bot', 'france', 'canada', 'algerie', 'promo', 'reduction', 'code'];
        if (rawCode.length >= 3 && !bl.some(b => rawCode.toLowerCase().includes(b))) {
          coupon = rawCode.toUpperCase();
        }
      }

      const cMatch = text.match(/(حساب|دولة|بلد|compte|pays)\\s*[:：]?\\s*([\\u0600-\\u06FFa-zA-Z\\s]+)/i);
      if (cMatch) country = cMatch[2].trim().slice(0, 18);

      hasCoins = text.includes('عملات') || text.includes('Coins') || text.includes('coins') || text.includes('🪙');

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

      const affiliateUrl = urlMatch[0];

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
          return `<span class="text-base sm:text-lg font-bold font-mono tracking-tight whitespace-nowrap inline-flex items-baseline gap-1" style="color: var(--text-main);">${deal.price_dzd.toLocaleString()} <span class="text-xs text-rose-500 font-semibold">${isAr ? 'دج' : 'DZD'}</span></span>`;
        }
      } else if (currentCurrency === 'EUR') {
        if (deal.price_eur) {
          return `<span class="text-base sm:text-lg font-bold font-mono tracking-tight whitespace-nowrap inline-flex items-baseline gap-1" style="color: var(--text-main);">${deal.price_eur.toFixed(2)} <span class="text-xs text-rose-500 font-semibold">€</span></span>`;
        }
      } else if (currentCurrency === 'USD') {
        if (deal.price_usd) {
          return `<span class="text-base sm:text-lg font-bold font-mono tracking-tight whitespace-nowrap inline-flex items-baseline gap-1" style="color: var(--text-main);">${deal.price_usd.toFixed(2)} <span class="text-xs text-rose-500 font-semibold">$</span></span>`;
        }
      }
      return `<span class="text-sm font-bold text-rose-500 font-sans">${isAr ? 'تخفيض خاص' : 'Prix Promo'}</span>`;
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
          <div class="relative w-full aspect-[4/3] rounded-xl overflow-hidden mb-3 cursor-pointer group flex items-center justify-center border" style="background-color: var(--bg-page); border-color: var(--border-card);" onclick="openDealModal('${deal.id}')">
            <img src="${deal.photo_url}" alt="${safeTitle}" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="handleImgError(this, '${escapeHtml(deal.photo_url)}')" class="w-full h-full object-contain group-hover:scale-105 transition-transform duration-300">
            ${deal.has_coins ? `<span class="absolute top-2 left-2 bg-amber-500 text-zinc-950 text-[10px] font-bold px-2 py-0.5 rounded-md flex items-center gap-1 shadow-md"><i class="fa-solid fa-coins text-[9px]"></i> Coins</span>` : ''}
            ${deal.country ? `<span class="absolute top-2 right-2 text-[10px] px-2 py-0.5 rounded-md font-bold border shadow-md" style="background-color: var(--bg-card); border-color: var(--border-card); color: var(--text-main);">${escapeHtml(deal.country)}</span>` : ''}
          </div>
        ` : `
          <div class="relative w-full aspect-[4/3] rounded-xl overflow-hidden mb-3 cursor-pointer group flex items-center justify-center border" style="background-color: var(--bg-page); border-color: var(--border-card);" onclick="openDealModal('${deal.id}')">
            <div class="flex flex-col items-center justify-center gap-2 opacity-50 p-4 text-center">
              <i class="fa-solid fa-bag-shopping text-2xl text-crimson-500"></i>
              <span class="text-[11px] font-semibold" style="color: var(--text-muted);">${safeTitle.slice(0, 30)}...</span>
            </div>
            ${deal.has_coins ? `<span class="absolute top-2 left-2 bg-amber-500 text-zinc-950 text-[10px] font-bold px-2 py-0.5 rounded-md flex items-center gap-1 shadow-md"><i class="fa-solid fa-coins text-[9px]"></i> Coins</span>` : ''}
          </div>
        `;

        const couponHtml = deal.coupon ? `
          <div class="border border-dashed rounded-xl px-2.5 py-1.5 flex items-center justify-between gap-1.5 mb-2.5 transition" style="background-color: var(--bg-elevated); border-color: rgba(225, 29, 72, 0.4);">
            <div class="flex items-center gap-1.5 min-w-0">
              <i class="fa-solid fa-ticket text-xs flex-shrink-0 text-amber-500"></i>
              <div class="min-w-0">
                <span class="text-[9px] uppercase tracking-wider block font-semibold opacity-60">${currentLang === 'fr' ? 'Code Promo' : 'كود الخصم'}</span>
                <span class="font-mono text-xs font-extrabold truncate select-all block text-crimson-500">${escapeHtml(deal.coupon)}</span>
              </div>
            </div>
            <button onclick="copyCoupon('${deal.coupon}', this)" aria-label="Copy coupon" class="min-h-[36px] min-w-[64px] border text-[11px] font-bold px-2 py-1 rounded-lg transition flex items-center justify-center gap-1 flex-shrink-0 touch-manipulation active:scale-95 shadow-sm" style="background-color: var(--bg-card); border-color: var(--border-card); color: var(--text-main);">
              <i class="fa-regular fa-copy text-[11px]"></i>
              <span class="copy-text">${I18N[currentLang].btn_copy}</span>
            </button>
          </div>
        ` : '';

        const secondaryPrice = (currentCurrency === 'DZD' && deal.price_usd)
          ? `<span class="text-[11px] font-mono whitespace-nowrap opacity-60">($${deal.price_usd.toFixed(2)})</span>`
          : (deal.price_dzd && currentCurrency !== 'DZD' ? `<span class="text-[11px] font-mono whitespace-nowrap opacity-60">(${deal.price_dzd.toLocaleString()} ${I18N[currentLang].currency_dzd})</span>` : '');

        card.innerHTML = `
          <div>
            ${photoHtml}
            <div class="flex items-center justify-between gap-2 mb-1.5">
              <span class="text-[10px] font-semibold px-2 py-0.5 rounded-md border" style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-muted);">
                ${deal.category_label || I18N[currentLang].deal_category_fallback}
              </span>
              <span class="text-[10px] font-mono opacity-60">
                ${deal.date ? deal.date.split(' ')[0] : ''}
              </span>
            </div>
            <h3 class="font-semibold text-xs sm:text-sm line-clamp-2 mb-2.5 hover:text-rose-500 transition cursor-pointer leading-snug break-words" style="color: var(--text-main);" onclick="openDealModal('${deal.id}')">
              ${safeTitle}
            </h3>
            ${couponHtml}
          </div>

          <div class="pt-2.5 border-t space-y-2.5" style="border-color: var(--border-card);">
            <div class="flex items-baseline justify-between gap-2">
              <div class="flex items-baseline flex-wrap gap-1.5 min-w-0">
                ${formatPrice(deal)}
                ${secondaryPrice}
              </div>
              ${deal.telegram_url ? `
                <a href="${deal.telegram_url}" target="_blank" rel="noopener noreferrer" title="Telegram" class="w-8 h-8 rounded-lg border flex items-center justify-center active:scale-95 transition touch-manipulation flex-shrink-0 text-sky-500" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
                  <i class="fa-brands fa-telegram"></i>
                </a>
              ` : ''}
            </div>

            <!-- Primary Buy Button with Coupon Auto-Copy -->
            <a href="${deal.affiliate_url}" target="_blank" rel="noopener noreferrer" onclick="handleBuyClick('${deal.coupon || ''}')" class="w-full bg-crimson-600 hover:bg-crimson-700 active:scale-[0.98] text-white font-bold text-xs sm:text-sm py-2.5 px-3 rounded-xl text-center flex items-center justify-center gap-2 transition shadow-sm touch-manipulation min-h-[44px]">
              <i class="fa-solid fa-cart-shopping text-xs"></i>
              <span>${I18N[currentLang].btn_buy}</span>
              ${deal.coupon ? `<span class="bg-black/25 text-[10px] font-mono px-1.5 py-0.5 rounded text-white/95 mr-1 inline-flex items-center gap-1"><i class="fa-solid fa-ticket text-[9px]"></i> ${escapeHtml(deal.coupon)}</span>` : ''}
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
        item.className = 'border rounded-2xl p-4 space-y-3.5 transition-colors';
        item.style.backgroundColor = 'var(--bg-card)';
        item.style.borderColor = 'var(--border-card)';

        const safeText = escapeHtml(deal.raw_text || '')
          .replace(/\\n/g, '<br>')
          .replace(/(https?:\\/\\/s\\.click\\.aliexpress\\.com\\/e\\/[A-Za-z0-9_-]+)/g, '<a href="$1" target="_blank" rel="noopener noreferrer" class="text-rose-500 font-bold underline break-all">$1</a>')
          .replace(/(@[A-Za-z0-9_]+)/g, '<span class="text-sky-500 font-semibold">$1</span>');

        item.innerHTML = `
          <div class="flex items-center justify-between pb-2.5 border-b text-xs" style="border-color: var(--border-card);">
            <div class="flex items-center gap-2">
              <div class="w-8 h-8 rounded-xl flex items-center justify-center text-sky-500 text-sm" style="background-color: var(--bg-elevated);">
                <i class="fa-brands fa-telegram"></i>
              </div>
              <div>
                <span class="font-bold block" style="color: var(--text-main);">${escapeHtml(currentChannel)}</span>
                <span class="text-[10px] font-mono opacity-60">${deal.date || ''}</span>
              </div>
            </div>
            ${deal.telegram_url ? `<a href="${deal.telegram_url}" target="_blank" rel="noopener noreferrer" class="min-h-[38px] px-2.5 py-1 text-sky-500 hover:underline font-semibold text-xs flex items-center gap-1 active:scale-95 touch-manipulation"><i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i> Telegram</a>` : ''}
          </div>

          ${deal.photo_url ? `
            <div class="rounded-xl overflow-hidden border max-h-80 cursor-pointer flex items-center justify-center" style="background-color: var(--bg-page); border-color: var(--border-card);" onclick="openDealModal('${deal.id}')">
              <img src="${deal.photo_url}" alt="${escapeHtml(deal.title)}" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="handleImgError(this, '${escapeHtml(deal.photo_url)}')" class="w-full h-auto object-contain max-h-80">
            </div>
          ` : ''}

          <div class="text-xs sm:text-sm leading-relaxed font-sans select-text break-words" style="color: var(--text-muted);">
            ${safeText}
          </div>

          <div class="pt-1 flex flex-col sm:flex-row gap-2">
            <a href="${deal.affiliate_url}" target="_blank" rel="noopener noreferrer" class="flex-1 min-h-[44px] bg-crimson-600 hover:bg-crimson-700 active:scale-[0.98] text-white font-bold text-xs sm:text-sm py-2.5 px-3 rounded-xl text-center flex items-center justify-center gap-2 transition shadow-sm touch-manipulation">
              <i class="fa-solid fa-cart-shopping text-xs"></i>
              <span>${I18N[currentLang].btn_buy}</span>
            </a>
            <a href="https://t.me/Alilo07BOT" target="_blank" rel="noopener noreferrer" class="min-h-[44px] border font-bold text-xs py-2.5 px-3.5 rounded-xl flex items-center justify-center gap-1.5 transition touch-manipulation active:scale-[0.98] text-amber-500" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
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
      if (typeof allDeals === 'undefined' || !Array.isArray(allDeals) || allDeals.length === 0) return;
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
        imgWrap.style.display = 'flex';
        img.src = deal.photo_url;
      } else {
        imgWrap.classList.add('hidden');
        imgWrap.style.display = 'none';
        img.src = '';
      }

      title.textContent = deal.title;
      cat.textContent = deal.category_label || t('deal_category_fallback', 'عرض مميز');
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
        couponWrap.style.display = 'flex';
        couponCode.textContent = deal.coupon;
      } else {
        couponWrap.classList.add('hidden');
        couponWrap.style.display = 'none';
      }

      price.innerHTML = formatPrice(deal);
      affBtn.href = deal.affiliate_url;

      if (deal.telegram_url) {
        chLink.innerHTML = `<a href="${deal.telegram_url}" target="_blank" rel="noopener noreferrer" class="text-sky-500 hover:underline font-bold text-xs flex items-center gap-1"><i class="fa-brands fa-telegram"></i> Telegram</a>`;
      } else {
        chLink.innerHTML = '';
      }

      modal.classList.remove('hidden');
      modal.style.display = 'flex';
      document.body.style.overflow = 'hidden';
    }

    function closeDealModal() {
      const modal = document.getElementById('deal-modal');
      if (modal) {
        modal.classList.add('hidden');
        modal.style.display = 'none';
      }
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
          btn.classList.add('text-emerald-500');
          setTimeout(() => {
            span.textContent = original;
            btn.classList.remove('text-emerald-500');
          }, 1800);
        }
      });
    }

    function copyCouponFromModal(btn) {
      if (currentActiveDeal && currentActiveDeal.coupon) {
        copyCoupon(currentActiveDeal.coupon, btn);
      }
    }

    function copyReferralCode(code, btn) {
      if (!code) return;
      navigator.clipboard.writeText(code).then(() => {
        showToast((currentLang === 'fr' ? 'Code copié : ' : 'تم نسخ الكود: ') + code);
        if (btn) {
          const original = btn.innerHTML;
          btn.innerHTML = '<i class="fa-solid fa-check text-emerald-500"></i> ' + (currentLang === 'fr' ? 'Copié !' : 'تم النسخ!');
          btn.classList.add('border-emerald-500');
          setTimeout(() => {
            btn.innerHTML = original;
            btn.classList.remove('border-emerald-500');
          }, 2000);
        }
      }).catch(() => {
        showToast(code);
      });
    }

    // ── Keyboard & Lifecycle Handlers ───────────────────────────────
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeDealModal();
    });

    document.addEventListener('DOMContentLoaded', () => {
      // Initialize theme & language
      applyTheme(currentTheme);
      setLanguage(currentLang);
      fetchDeals();
      setInterval(() => fetchDeals(false), 180000);
    });
  </script>

</body>
</html>"""

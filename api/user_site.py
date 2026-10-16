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
  <script>
    (function() {
      try {
        var t = localStorage.getItem('dealscout_theme');
        if (t === 'light') {
          document.documentElement.classList.remove('dark');
          document.documentElement.classList.add('light');
        } else {
          document.documentElement.classList.add('dark');
          document.documentElement.classList.remove('light');
        }
      } catch(e) {}
    })();
  </script>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, viewport-fit=cover">
  <meta name="referrer" content="no-referrer">
  <title id="meta-title">DealScout DZ — عروض وتخفيضات علي اكسبراس في الجزائر | AliExpress Deals DZ</title>
  <meta name="robots" content="index, follow">
  <meta name="googlebot" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">

  <!-- Canonical & Alternate Hreflang -->
  <link rel="canonical" href="https://dealscoutgreen.vercel.app/">
  <link rel="alternate" hreflang="ar" href="https://dealscoutgreen.vercel.app/">
  <link rel="alternate" hreflang="ar-DZ" href="https://dealscoutgreen.vercel.app/">
  <link rel="alternate" hreflang="fr" href="https://dealscoutgreen.vercel.app/">
  <link rel="alternate" hreflang="x-default" href="https://dealscoutgreen.vercel.app/">

  <!-- Generative Engine Optimization (GEO) & LLM Resource Manifests -->
  <link rel="alternate" type="text/plain" href="https://dealscoutgreen.vercel.app/llms.txt" title="LLMs manifest">
  <link rel="alternate" type="text/plain" href="https://dealscoutgreen.vercel.app/llms-full.txt" title="LLMs full documentation">

  <!-- Meta Search & Geography -->
  <meta name="keywords" content="aliexpressdz, aliexpress deals dz, aliexpress deald dz, عروض علي اكسبراس, شراء من علي اكسبراس في الجزائر, علي اكسبراس الجزائر, تخفيضات علي اكسبراس, كود تخفيض علي اكسبراس الجزائر, كوبونات علي اكسبراس الجزائر, صفقات علي اكسبراس, عملات علي اكسبراس, بوت تخفيض العملات علي اكسبراس, الشراء من علي اكسبراس في الجزائر بريدي موب, توصيل علي اكسبراس الجزائر, بريد الجزائر, اسعار السكوار, قناة تيليجرام صفقات علي اكسبراس الجزائر, عروض الشتاء Winter Offers AliExpress, تخفيضات عروض الشتاء 2026, كود خصم Winter Offers, WOAE23, WOAE35, WOAE06, WOAE12, Honor X70 5G, realme 15T 5G, OPPO A6 Pro, iQOO Z11s 5G, realme Watch 5, AMD Ryzen 5 8400F, Redmi Note 12 5G, CUSU SSD 512GB, Blackview Wave 10C, aliexpress algerie, شراء من علي اكسبرس بريدي موب, بطاقة بايبايت في الجزائر, بطاقة bybit مجانية, بطاقة redotpay الجزائر, كود خصم redotpay, شحن redotpay بريدي موب, شراء usdt بالدينار الجزائري, بطاقة فيزا للشراء من الانترنت الجزائر, بطاقة ماستركارد افتراضية الجزائر, تفعيل بايبال بالجزائر, binance p2p baridimob algerie, carte bybit algerie, carte redotpay algerie, acheter sur aliexpress baridimob, carte bancaire internationale algerie, تخفيضات علي اكسبرس الجزائر, صفقات aliexpress, algeria deals, dealscout dz, bons plans algerie">
  <meta name="geo.region" content="DZ">
  <meta name="geo.placename" content="Algeria">
  <meta name="geo.position" content="28.0339;1.6596">
  <meta name="ICBM" content="28.0339, 1.6596">
  <meta name="language" content="Arabic">
  <meta name="author" content="DealScout DZ">

  <!-- OpenGraph / Social Meta -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="DealScout DZ">
  <meta property="og:url" content="https://dealscoutgreen.vercel.app/">
  <meta property="og:title" id="og-title" content="DealScout DZ — عروض وتخفيضات علي اكسبراس في الجزائر | AliExpress Deals DZ">
  <meta property="og:description" id="og-desc" content="تتبع مباشر لأقوى عروض وتخفيضات علي اكسبراس في الجزائر (AliExpress Deals DZ). صفقات aliexpressdz، كود تخفيض علي اكسبراس، روابط خصم العملات، وتنبيهات قناة التيليجرام الفورية.">
  <meta property="og:image" content="https://dealscoutgreen.vercel.app/logo.png">
  <meta property="og:image:secure_url" content="https://dealscoutgreen.vercel.app/logo.png">
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
  <meta name="twitter:title" id="twitter-title" content="DealScout DZ — عروض وتخفيضات علي اكسبراس في الجزائر | AliExpress Deals DZ">
  <meta name="twitter:description" id="twitter-desc" content="تتبع مباشر لأقوى عروض وتخفيضات علي اكسبراس في الجزائر (AliExpress Deals DZ). صفقات aliexpressdz، كود تخفيض علي اكسبراس، روابط خصم العملات، وتنبيهات قناة التيليجرام الفورية.">
  <meta name="twitter:image" content="https://dealscoutgreen.vercel.app/logo.png">
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
  <link href="https://fonts.googleapis.com/css2?family=Alexandria:wght@300;400;500;600;700;800&family=Cairo:wght@400;600;700&family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Readex+Pro:wght@400;500;600;700&display=swap" rel="stylesheet">

  <!-- Optional Tailwind JIT CDN with safety guard -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    if (typeof tailwind !== 'undefined') {
      tailwind.config = {
        darkMode: 'class',
        theme: {
          extend: {
            fontFamily: {
              sans: ['"IBM Plex Sans Arabic"', '"Alexandria"', '"Plus Jakarta Sans"', '-apple-system', 'sans-serif'],
              heading: ['"Alexandria"', '"IBM Plex Sans Arabic"', '"Plus Jakarta Sans"', 'sans-serif'],
              mono: ['"JetBrains Mono"', 'ui-monospace', 'monospace'],
              inter: ['"Plus Jakarta Sans"', '"IBM Plex Sans Arabic"', 'sans-serif']
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

      /* Clean Crisp Light Theme Tokens */
      --bg-page: #f8fafc;
      --bg-card: rgba(255, 255, 255, 0.95);
      --bg-card-hover: #ffffff;
      --bg-elevated: #f1f5f9;
      --bg-subtle: #e2e8f0;
      --border-card: #e2e8f0;
      --border-subtle: #cbd5e1;
      --text-main: #0f172a;
      --text-muted: #475569;
      --text-soft: #64748b;
      --header-bg: rgba(255, 255, 255, 0.92);
      --input-bg: #ffffff;
      --shadow-card: 0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px -1px rgba(0, 0, 0, 0.03);
    }

    html.dark {
      /* Deep Obsidian Slate Dark Tokens with Architectural Textures */
      --bg-page: #06080d;
      --bg-card: rgba(14, 18, 27, 0.92);
      --bg-card-hover: rgba(20, 26, 40, 0.98);
      --bg-elevated: rgba(20, 26, 40, 0.95);
      --bg-subtle: rgba(30, 41, 59, 0.7);
      --border-card: rgba(255, 255, 255, 0.09);
      --border-subtle: rgba(255, 255, 255, 0.16);
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-soft: #64748b;
      --header-bg: rgba(9, 12, 19, 0.9);
      --input-bg: rgba(13, 17, 26, 0.95);
      --shadow-card: 0 4px 12px -2px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.06);
    }

    html {
      scroll-behavior: smooth;
      -webkit-text-size-adjust: 100%;
      overflow-x: hidden !important;
      width: 100% !important;
      max-width: 100vw !important;
    }
    body {
      background-color: var(--bg-page);
      background-image: radial-gradient(rgba(0, 0, 0, 0.05) 1px, transparent 1px);
      background-size: 24px 24px;
      color: var(--text-main);
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      -webkit-tap-highlight-color: transparent;
      transition: background-color 0.2s ease, color 0.2s ease;
      overflow-x: hidden !important;
      width: 100% !important;
      max-width: 100vw !important;
      position: relative;
    }
    html.dark body {
      background-image: radial-gradient(rgba(255, 255, 255, 0.07) 1px, transparent 1px);
      background-size: 24px 24px;
    }
    body[dir="ltr"] {
      font-family: 'Plus Jakarta Sans', 'IBM Plex Sans Arabic', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    body[dir="rtl"] {
      font-family: 'IBM Plex Sans Arabic', 'Alexandria', 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    h1, h2, h3, h4, .font-heading {
      font-family: 'Alexandria', 'IBM Plex Sans Arabic', 'Plus Jakarta Sans', sans-serif !important;
      letter-spacing: -0.02em;
    }
    .font-mono, code, .price-num {
      font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
      font-feature-settings: 'tnum' 1;
      font-variant-numeric: tabular-nums;
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

    /* Resilient Core Layout Utilities */
    [hidden] { display: none !important; }
    .hidden { display: none; }
    .flex { display: flex; }
    .inline-flex { display: inline-flex; }
    .grid { display: grid; }
    @media (min-width: 640px) {
      .sm\\:inline { display: inline !important; }
      .sm\\:inline-flex { display: inline-flex !important; }
      .sm\\:flex { display: flex !important; }
    }
    @media (min-width: 768px) {
      .md\\:flex { display: flex !important; }
      .md\\:hidden { display: none !important; }
    }
    @media (min-width: 1024px) {
      .lg\\:flex { display: flex !important; }
      .lg\\:hidden { display: none !important; }
    }
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
    #deal-modal.hidden, #telegram-modal.hidden, #roulette-modal.hidden, #gamification-modal.hidden {
      display: none !important;
      visibility: hidden !important;
      opacity: 0 !important;
      pointer-events: none !important;
    }
    #deal-modal:not(.hidden), #telegram-modal:not(.hidden), #roulette-modal:not(.hidden), #gamification-modal:not(.hidden) {
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
      border-radius: 16px;
      box-shadow: var(--shadow-card);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      transition: border-color 0.18s ease, transform 0.18s ease, box-shadow 0.18s ease;
      position: relative;
    }
    html.dark .deal-card {
      box-shadow: 0 4px 12px -2px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }
    @media (hover: hover) {
      .deal-card:hover {
        border-color: #e11d48;
        transform: translateY(-2px);
        box-shadow: 0 8px 20px -4px rgba(0, 0, 0, 0.08);
      }
      html.dark .deal-card:hover {
        border-color: rgba(225, 29, 72, 0.8);
        box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.5);
      }
    }

    /* Anti-Slop: Editorial Promo Showcase Banner (Clean Neutral Surface, Zero Rainbow Mesh) */
    #active-event-banner {
      background-color: var(--bg-card) !important;
      border: 1px solid var(--border-card) !important;
      border-right: 4px solid #e11d48 !important;
      border-radius: 14px !important;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
    }
    [dir="ltr"] #active-event-banner {
      border-right: 1px solid var(--border-card) !important;
      border-left: 4px solid #e11d48 !important;
    }
    html.dark #active-event-banner {
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
    }

    /* Anti-Slop: Solid, Confident AliExpress Action CTA (No Glowing Neon Gradients) */
    .btn-ali-primary {
      background-color: #e11d48 !important;
      color: #ffffff !important;
      border: 1px solid transparent;
      box-shadow: 0 1px 2px rgba(225, 29, 72, 0.2);
      transition: background-color 0.15s ease, transform 0.15s ease, filter 0.15s ease;
    }
    .btn-ali-primary:hover {
      background-color: #be123c !important;
      transform: translateY(-1px);
    }
    .btn-ali-primary:active {
      transform: scale(0.98);
      background-color: #9f1239 !important;
    }

    .coupon-chip {
      transition: all 0.18s ease;
    }
    .coupon-chip:hover {
      border-color: #f43f5e !important;
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(225, 29, 72, 0.2);
    }
    .coupon-chip:active {
      transform: scale(0.96);
    }

    .deal-kw-pill {
      transition: all 0.18s ease;
    }
    .deal-kw-pill:hover {
      border-color: #f43f5e !important;
      background-color: var(--bg-elevated) !important;
      transform: translateY(-1px);
    }
    .deal-kw-pill:active {
      transform: scale(0.95);
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
    @keyframes heartPop {
      0% { transform: scale(1); }
      40% { transform: scale(1.35); }
      100% { transform: scale(1); }
    }
    @keyframes slotRoll {
      0% { transform: translateY(0); filter: blur(0); }
      50% { transform: translateY(-24px); filter: blur(1.5px); }
      100% { transform: translateY(0); filter: blur(0); }
    }
    .animate-slide-up { animation: slideUp 0.25s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
    .animate-fade-in { animation: fadeIn 0.2s ease-out forwards; }
    .animate-heart-pop { animation: heartPop 0.35s cubic-bezier(0.17, 0.89, 0.32, 1.49); }
    .animate-slot-roll { animation: slotRoll 0.25s ease-in-out infinite; }
    .bottom-18 { bottom: 4.75rem; }
    
    .faq-item[open] summary .faq-icon {
      transform: rotate(180deg);
    }
    #toast {
      pointer-events: none !important;
      user-select: none !important;
    }
  </style>

  <!-- Structured JSON-LD Schema -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "@id": "https://dealscoutgreen.vercel.app/#website",
    "url": "https://dealscoutgreen.vercel.app/",
    "name": "DealScout DZ",
    "alternateName": ["DealScout", "aliexpressdz", "aliexpress deals dz", "aliexpress deald dz", "عروض علي اكسبراس الجزائر", "شراء من علي اكسبراس في الجزائر", "AliExpress Deals Algeria", "Bons Plans AliExpress Algérie"],
    "description": "منصة متخصصة في رصد وتحديث أقوى عروض وتخفيضات علي اكسبراس في الجزائر (AliExpress Deals DZ) لحظة بلحظة مع حساب الأسعار بالدينار الجزائري.",
    "inLanguage": ["ar", "fr"],
    "publisher": {
      "@type": "Organization",
      "@id": "https://dealscoutgreen.vercel.app/#organization",
      "name": "DealScout DZ",
      "url": "https://dealscoutgreen.vercel.app/",
      "logo": {
        "@type": "ImageObject",
        "url": "https://dealscoutgreen.vercel.app/icon.svg",
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
      },
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "4.9",
        "reviewCount": "3420",
        "bestRating": "5",
        "worstRating": "1"
      }
    },
    "potentialAction": {
      "@type": "SearchAction",
      "target": "https://dealscoutgreen.vercel.app/?q={search_term_string}",
      "query-input": "required name=search_term_string"
    }
  }
  </script>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "@id": "https://dealscoutgreen.vercel.app/#webpage",
    "url": "https://dealscoutgreen.vercel.app/",
    "name": "صفقات وتخفيضات AliExpress بالدينار الجزائري",
    "isPartOf": {
      "@id": "https://dealscoutgreen.vercel.app/#website"
    },
    "inLanguage": ["ar", "fr"],
    "description": "عروض يومية حصرية من AliExpress محسوبة بالدينار الجزائري عبر أسعار الصرف الحية."
  }
  </script>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "@id": "https://dealscoutgreen.vercel.app/#breadcrumbs",
    "itemListElement": [
      {
        "@type": "ListItem",
        "position": 1,
        "name": "الرئيسية",
        "item": "https://dealscoutgreen.vercel.app/"
      },
      {
        "@type": "ListItem",
        "position": 2,
        "name": "عروض وتخفيضات AliExpress",
        "item": "https://dealscoutgreen.vercel.app/#deals"
      },
      {
        "@type": "ListItem",
        "position": 3,
        "name": "حاسبة أسعار السكوار",
        "item": "https://dealscoutgreen.vercel.app/#calculator"
      }
    ]
  }
  </script>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HowTo",
    "@id": "https://dealscoutgreen.vercel.app/#howto-cards",
    "name": "كيف تشتري من AliExpress في الجزائر وتدفع بـ BaridiMob",
    "description": "دليل شامل لشراء وشحن بطاقات فيزا وماستركارد الافتراضية الدولية (Bybit, RedotPay) بالدينار الجزائري عبر منصة Binance P2P وبريدي موب للتسوق من AliExpress.",
    "inLanguage": ["ar", "fr"],
    "totalTime": "PT10M",
    "step": [
      {
        "@type": "HowToStep",
        "position": 1,
        "name": "شراء USDT بالدينار الجزائري عبر Binance P2P",
        "text": "افتح حسابك في منصة Binance، توجه إلى قسم تداول P2P واختر الدفع بواسطة BaridiMob أو CCP لشراء الدولار الرقمي (USDT) بالدينار الجزائري مباشرة وبأمان تام."
      },
      {
        "@type": "HowToStep",
        "position": 2,
        "name": "شحن بطاقتك الافتراضية (Bybit أو RedotPay)",
        "text": "حوّل رصيد USDT من محفظة Binance إلى حساب بطاقة Bybit Card المجانية أو بطاقة فيزا RedotPay في دقائق بدون رسوم إضافية."
      },
      {
        "@type": "HowToStep",
        "position": 3,
        "name": "إضافة البطاقة لحساب AliExpress",
        "text": "انسخ بيانات البطاقة الافتراضية (رقم البطاقة وتاريخ الانتهاء وCVV) وأضفها في وسائل الدفع بتطبيق AliExpress."
      },
      {
        "@type": "HowToStep",
        "position": 4,
        "name": "تطبيق أكواد الخصم والعملات والشراء",
        "text": "اختر العرض من DealScout DZ، انسخ كود التخفيض، استخدم بوت العملات واستلم طردك مباشرة في مكتب بريد الجزائر القريب منك."
      }
    ]
  }
  </script>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "@id": "https://dealscoutgreen.vercel.app/#faq",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "كيف يتم احتساب الأسعار بالدينار الجزائري (DZD)؟",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "يتم حساب السعر بالدينار الجزائري تلقائياً وبدقة عالية اعتماداً على سعر صرف الدولار واليورو في السوق الموازي (سعر السكوار الحقيقي) المستخرج مباشرة من موقع SquareAlgerie.com."
        }
      },
      {
        "@type": "Question",
        "name": "كيف يتم شحن الطرود واستلامها في الجزائر؟",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "تشحن معظم المنتجات عبر بريد الجزائر (Algérie Poste / EMS). يصل الطرد إلى أقرب مكتب بريد لعنوان سكناك ويتم إرسال إشعار وصول SMS إلى هاتفك. تستغرق مدة الوصول بين 15 و28 يوماً مع AliExpress Choice وStandard Shipping."
        }
      },
      {
        "@type": "Question",
        "name": "كيف أشتري من AliExpress باستخدام تطبيق بريدي موب (BaridiMob)؟",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "تتم العملية بفتح حساب على منصة Binance واستخدام سوق P2P لشراء رصيد USDT بالدينار الجزائري والدفع عبر BaridiMob لبائع موثوق، ثم سحب الرصيد إلى بطاقة Bybit ماستركارد المجانية أو بطاقة RedotPay في دقائق معدودة."
        }
      },
      {
        "@type": "Question",
        "name": "ما هي قوانين الجمارك الجزائرية للطرود البريدية؟ وما هي السلع الممنوعة؟",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "الطرود البريدية المخصصة للاستخدام الشخصي والعائلي معفاة تماماً من الرسوم الجمركية في الجزائر بشرط عدم استيراد كميات تجارية متكررة. ويحظر استيراد طائرات الدرون، كاميرات التجسس المخفية، وأجهزة اللاسلكي بدون رخصة."
        }
      },
      {
        "@type": "Question",
        "name": "كيف أحصل على أقصى تخفيض لعملات AliExpress Coins (حتى 70%)؟",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "باستخدام أداة مولد روابط العملات على منصة DealScout DZ أو بوت @Alilo07BOT، يتم توليد رابط مخصص يرفع نسبة قبول العملات على نفس السلعة من 2% حتى 70% عند الشراء مباشرة من قسم العملات."
        }
      },
      {
        "@type": "Question",
        "name": "كيف أكتب العنوان الجزائري والرمز البريدي (Code Postal) بشكل صحيح؟",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "اكتب اسمك المطابق للهوية الوطنية ورقم هاتفك الفعال. أدخل الرمز البريدي الدقيق المكون من 5 أرقام (رقمان للولاية و3 أرقام لمركز التوزيع البريدي لبلديتك) لضمان وصول الطرد مباشرة لمكتب البريد المحلي."
        }
      }
    ]
  }
  </script>
  <!-- Schema.org WebApplication (Coins Deal Generator for AI Agents & Search Engines) -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebApplication",
    "@id": "https://dealscoutgreen.vercel.app/#coins-tool",
    "name": "AliExpress Coins Deal Discount Link Generator Algeria",
    "alternateName": "مولد روابط تخفيض عملات علي إكسبرس في الجزائر",
    "url": "https://dealscoutgreen.vercel.app/#coins-generator",
    "applicationCategory": "ShoppingApplication",
    "operatingSystem": "All",
    "browserRequirements": "Requires JavaScript. Requires HTML5.",
    "offers": {
      "@type": "Offer",
      "price": "0",
      "priceCurrency": "DZD"
    },
    "description": "أداة مجانية لتحويل أي رابط منتج من AliExpress إلى رابط تخفيض العملات المباشر (Coins Discount Link) بخصومات تصل حتى 70% للمتسوقين في الجزائر مع تتبع العملات وأسعار الدينار الجزائري.",
    "inLanguage": ["ar", "fr"]
  }
  </script>
  <!-- Schema.org SpeakableSpecification for AI Voice Overviews & Answer Engines -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebPage",
    "@id": "https://dealscoutgreen.vercel.app/#speakable",
    "url": "https://dealscoutgreen.vercel.app/",
    "name": "صفقات علي إكسبرس ودليل الشراء في الجزائر",
    "speakable": {
      "@type": "SpeakableSpecification",
      "cssSelector": ["#ai-overview-facts", "#seo-shopping-guide", "#page-faq"]
    }
  }
  </script>
</head>
<body class="min-h-screen flex flex-col justify-between" dir="rtl">

  <!-- Top Utilities Bar -->
  <aside class="border-b text-[11px] py-1.5 px-3 sm:px-4 pt-safe transition-colors w-full overflow-hidden" style="background-color: var(--bg-card); border-color: var(--border-card); color: var(--text-muted);" aria-label="شريط المعلومات">
    <div class="max-w-7xl mx-auto flex items-center justify-between gap-2 sm:gap-3">
      <div class="flex items-center gap-2 sm:gap-3 min-w-0">
        <span class="inline-flex items-center gap-1.5 font-medium text-[10px] sm:text-[11px] truncate">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse flex-shrink-0"></span>
          <span data-i18n="top_live_updates" class="truncate">تحديث فوري من القنوات</span>
        </span>
        <span class="hidden sm:inline opacity-30">|</span>
        <a href="https://squarealgerie.com" target="_blank" rel="noopener noreferrer" class="hidden sm:flex items-center gap-1 hover:opacity-80 transition py-0.5">
          <i class="fa-solid fa-chart-line text-emerald-500"></i>
          <span><span data-i18n="top_usdt_rate">سعر صرف السكوار</span>: 1 USDT ≈ <b id="top-usdt-rate" class="font-mono text-emerald-500 font-bold">256.9</b> <span data-i18n="currency_dzd">دج</span></span>
        </a>
      </div>
      
      <div class="flex items-center gap-1 sm:gap-2.5 flex-shrink-0">
        <!-- Tools & Square Calculator Hub Button -->
        <button onclick="openGamificationHub()" id="streak-header-btn" aria-label="Square Calculator & Tools" class="px-2 py-1 rounded-lg border text-xs flex items-center gap-1.5 transition active:scale-95 touch-manipulation cursor-pointer font-bold" style="border-color: var(--border-card); background-color: var(--bg-elevated); color: var(--text-main);" title="حاسبة السكوار والأدوات">
          <i class="fa-solid fa-calculator text-emerald-500 text-[11px]"></i>
          <span id="streak-header-text" class="text-[11px] font-semibold hidden sm:inline" data-i18n="tools_header">حاسبة السكوار</span>
        </button>

        <span class="opacity-30">|</span>

        <!-- Theme Toggle Button -->
        <button onclick="toggleTheme()" id="theme-toggle-btn" aria-label="Toggle Light / Dark theme" class="px-2 py-1 rounded-lg border text-xs flex items-center gap-1.5 transition active:scale-95 touch-manipulation cursor-pointer" style="border-color: var(--border-card); background-color: var(--bg-elevated); color: var(--text-main);">
          <i id="theme-icon" class="fa-solid fa-sun text-[11px] text-amber-500"></i>
          <span id="theme-text" class="text-[11px] font-semibold hidden sm:inline">فاتح</span>
        </button>

        <span class="opacity-30">|</span>

        <!-- Language Switcher Button -->
        <div class="inline-flex items-center border rounded-lg p-0.5 text-xs" style="border-color: var(--border-card); background-color: var(--bg-elevated);">
          <button onclick="setLanguage('ar')" id="lang-ar-btn" class="px-1.5 sm:px-2 py-0.5 rounded text-[10px] sm:text-[11px] font-bold bg-crimson-600 text-white transition active:scale-95">العربية</button>
          <button onclick="setLanguage('fr')" id="lang-fr-btn" class="px-1.5 sm:px-2 py-0.5 rounded text-[10px] sm:text-[11px] font-bold opacity-60 hover:opacity-100 transition active:scale-95">Français</button>
        <span class="hidden sm:inline opacity-30">|</span>
        <a id="top-telegram-link" href="https://t.me/DzAliexpress0" target="_blank" rel="noopener noreferrer" class="hidden sm:inline-flex hover:text-sky-400 text-sky-500 transition font-bold items-center gap-1 py-1 px-1.5 active:scale-95 touch-manipulation text-xs" title="قناة التيليجرام الرسمية">
          <i class="fa-brands fa-telegram text-sky-500 text-sm"></i>
          <span class="text-[11px] font-bold">Telegram</span>
        </a>
        </div>
      </div>
    </div>
  </aside>

  <!-- Main Navigation Bar -->
  <header class="sticky top-0 z-40 border-b backdrop-blur-md px-3 sm:px-4 py-2 sm:py-2.5 transition-colors" style="background-color: var(--header-bg); border-color: var(--border-card);">
    <div class="max-w-7xl mx-auto flex items-center justify-between gap-3 sm:gap-4">
      
      <!-- Brand Logo -->
      <a href="#deals" onclick="showPage('deals')" class="flex items-center gap-2 sm:gap-2.5 flex-shrink-0 min-h-[44px] touch-manipulation" aria-label="DealScout DZ">
        <img src="/logo_circular.png" alt="DealScout DZ" width="34" height="34" style="width: 34px; height: 34px; max-width: 34px; max-height: 34px; object-fit: contain;" class="w-8.5 h-8.5 rounded-xl object-contain shadow-sm flex-shrink-0 brand-logo-img" onerror="this.onerror=null; this.src='/logo.png'">
        <div>
          <div class="flex items-center gap-1.5">
            <div class="font-bold text-sm sm:text-base tracking-tight font-inter inline-flex items-center gap-1" style="color: var(--text-main);">
              <span>DealScout<span class="text-crimson-500">DZ</span></span>
            </div>
          </div>
          <p class="text-[9px] hidden sm:block -mt-0.5 opacity-60" style="color: var(--text-muted);" data-i18n="brand_subtitle">بوابة صفقات وتخفيضات AliExpress 🇩🇿</p>
        </div>
      </a>

      <!-- Desktop Nav Pages Links (Clean 5-Item Focused Navigation) -->
      <nav class="hidden md:flex items-center gap-1 text-xs font-semibold" style="color: var(--text-muted);">
        <button onclick="showPage('deals')" id="nav-link-deals" class="nav-page-btn px-2.5 py-1.5 rounded-lg transition flex items-center gap-1.5 font-bold text-xs" style="background-color: var(--bg-elevated); color: var(--text-main);">
          <i class="fa-solid fa-fire text-crimson-500 text-xs"></i>
          <span data-i18n="nav_deals">الصفقات</span>
        </button>
        <button onclick="showPage('tracking')" id="nav-link-tracking" class="nav-page-btn px-2.5 py-1.5 rounded-lg hover:opacity-100 transition flex items-center gap-1.5 text-xs">
          <i class="fa-solid fa-truck-fast text-blue-500 text-xs"></i>
          <span data-i18n="nav_tracking">تتبع الطرود</span>
        </button>
        <button onclick="showPage('coins')" id="nav-link-coins" class="nav-page-btn px-2.5 py-1.5 rounded-lg hover:opacity-100 transition flex items-center gap-1.5 text-xs">
          <i class="fa-solid fa-coins text-amber-500 text-xs"></i>
          <span data-i18n="nav_coins">بوت العملات</span>
        </button>
        <button onclick="showPage('cards')" id="nav-link-cards" class="nav-page-btn px-2.5 py-1.5 rounded-lg hover:opacity-100 transition flex items-center gap-1.5 text-xs">
          <i class="fa-solid fa-credit-card text-emerald-500 text-xs"></i>
          <span data-i18n="nav_cards">بطاقات الشراء</span>
        </button>
        <a href="/blog/aliexpress-algeria-guide-dz" class="nav-page-btn px-2.5 py-1.5 rounded-lg hover:opacity-100 transition flex items-center gap-1.5 text-xs text-amber-400 font-bold hover:bg-amber-500/10" title="دليل الشراء من AliExpress في الجزائر 2026">
          <i class="fa-solid fa-book-open text-amber-400 text-xs"></i>
          <span>دليل 2026</span>
        </a>
      </nav>

      <!-- Search Bar Desktop (Visible on Large Screens) -->
      <div class="hidden lg:flex items-center relative flex-1 max-w-xs xl:max-w-sm">
        <i class="fa-solid fa-magnifying-glass absolute right-3.5 top-1/2 -translate-y-1/2 text-xs pointer-events-none opacity-50"></i>
        <input 
          type="search" 
          id="desktop-search" 
          aria-label="Search deals"
          oninput="handleSearchInput(this.value)"
          placeholder="ابحث عن هاتف، شاحن، كود خصم..." 
          data-i18n-placeholder="search_placeholder"
          class="w-full border rounded-xl pr-9 pl-14 py-2 text-xs focus:outline-none focus:border-rose-500 transition min-h-[40px]"
          style="background-color: var(--input-bg); border-color: var(--border-card); color: var(--text-main);"
        />
        <div class="absolute left-2.5 top-1/2 -translate-y-1/2 flex items-center gap-1">
          <button id="desktop-search-clear" onclick="resetFilters()" class="hidden text-xs opacity-50 hover:opacity-100 p-1 cursor-pointer" title="مسح">
            <i class="fa-solid fa-xmark"></i>
          </button>
          <kbd class="pointer-events-none hidden xl:inline-block px-1.5 py-0.5 text-[9px] font-mono border rounded opacity-50" style="background-color: var(--bg-card); border-color: var(--border-card);">Ctrl K</kbd>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex items-center gap-1 sm:gap-2 flex-shrink-0">
        <!-- Currency Selector -->
        <div class="flex items-center border rounded-xl p-0.5 text-xs font-semibold" style="border-color: var(--border-card); background-color: var(--bg-card);" aria-label="Currency" role="group">
          <button onclick="setCurrency('DZD')" id="curr-dzd" class="min-w-[26px] sm:min-w-[34px] h-8 sm:h-9 px-1.5 sm:px-2 py-1 rounded-lg bg-crimson-600 text-white font-mono transition flex items-center justify-center active:scale-95 touch-manipulation text-[11px] sm:text-xs">دج</button>
          <button onclick="setCurrency('USD')" id="curr-usd" class="min-w-[24px] sm:min-w-[30px] h-8 sm:h-9 px-1 sm:px-2 py-1 rounded-lg opacity-70 hover:opacity-100 font-mono transition flex items-center justify-center active:scale-95 touch-manipulation text-[11px] sm:text-xs">$</button>
          <button onclick="setCurrency('EUR')" id="curr-eur" class="min-w-[24px] sm:min-w-[30px] h-8 sm:h-9 px-1 sm:px-2 py-1 rounded-lg opacity-70 hover:opacity-100 font-mono transition flex items-center justify-center active:scale-95 touch-manipulation text-[11px] sm:text-xs">€</button>
        </div>

        <!-- Join Telegram Button -->
        <a id="btn-telegram-join" href="https://t.me/DzAliexpress0" target="_blank" rel="noopener noreferrer" class="bg-[#229ED9] hover:bg-[#1e8ec3] text-white text-xs h-8 sm:h-9 px-2.5 sm:px-3 rounded-xl font-bold flex items-center justify-center gap-1.5 transition active:scale-95 shadow-sm touch-manipulation" aria-label="قناة التيليجرام">
          <i class="fa-brands fa-telegram text-sm" aria-hidden="true"></i>
          <span class="text-[11px] font-bold hidden lg:inline" data-i18n="btn_join_channel">تيليجرام</span>
        </a>

        <!-- Refresh Data Button -->
        <button onclick="fetchDeals(true, true)" title="تحديث البيانات" class="w-8 sm:w-9 h-8 sm:h-9 rounded-xl border text-xs flex items-center justify-center transition active:scale-95 touch-manipulation cursor-pointer hover:border-rose-500 flex-shrink-0" style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-main);">
          <i class="fa-solid fa-rotate-right" id="refresh-icon" aria-hidden="true"></i>
        </button>
      </div>

    </div>
  </header>

  <!-- ========================================== -->
  <!-- MAIN ROUTER PAGES CONTAINER -->
  <!-- ========================================== -->
  <main class="max-w-7xl mx-auto px-3 sm:px-4 md:px-6 py-3.5 sm:py-5 space-y-4 sm:space-y-6 pb-safe w-full flex-grow">

    <!-- ───────────────────────────────────────────────────────── -->
    <!-- PAGE 1: DEALS BROWSER (DEFAULT)                           -->
    <!-- ───────────────────────────────────────────────────────── -->
    <div id="page-deals" class="page-view space-y-4 sm:space-y-6">

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

      <!-- Direct Official Telegram Channel Access Banner (Preserved hidden to prevent duplicate clutter) -->
      <aside id="channel-telegram-banner" class="hidden border rounded-xl px-3.5 py-2.5 items-center justify-between gap-3 transition-all shadow-sm" style="background-color: var(--bg-card); border-color: var(--border-card);" aria-label="رابط القناة الرسمي">
        <div class="flex items-center gap-2.5 min-w-0">
          <div class="w-8 h-8 rounded-lg bg-[#229ED9]/15 text-[#229ED9] flex items-center justify-center text-lg flex-shrink-0">
            <i class="fa-brands fa-telegram"></i>
          </div>
          <div class="min-w-0">
            <div class="flex items-center gap-2">
              <h2 id="channel-banner-name" class="font-bold text-xs truncate" style="color: var(--text-main);">قناة التيليجرام الرسمية (@DzAliexpress0)</h2>
              <span class="inline-flex items-center gap-1 text-[9px] font-bold px-1.5 py-0.2 rounded bg-emerald-500/10 text-emerald-500 border border-emerald-500/20">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                <span data-i18n="channel_banner_live">تحديثات فورية</span>
              </span>
            </div>
            <p id="channel-banner-desc" class="text-[10px] truncate opacity-75" style="color: var(--text-muted);" data-i18n="channel_banner_desc">
              تابع الصفقات والتخفيضات وكوبونات التخفيض الحصرية لحظة بلحظة فور نزولها في القناة.
            </p>
          </div>
        </div>
        <a id="channel-banner-btn" href="https://t.me/DzAliexpress0" target="_blank" rel="noopener noreferrer" class="bg-[#229ED9] hover:bg-[#1e8ec3] text-white text-xs font-bold h-8 px-3 rounded-lg flex items-center justify-center gap-1.5 shadow-sm transition active:scale-95 touch-manipulation flex-shrink-0">
          <i class="fa-brands fa-telegram text-sm"></i>
          <span id="channel-banner-btn-text" class="text-[11px]" data-i18n="channel_banner_btn">فتح القناة</span>
          <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
        </a>
      </aside>

      <!-- Mobile & Tablet Search Bar -->
      <div class="lg:hidden relative">
        <i class="fa-solid fa-magnifying-glass absolute right-3.5 top-1/2 -translate-y-1/2 text-sm pointer-events-none opacity-50"></i>
        <input 
          type="search" 
          id="mobile-search" 
          aria-label="Search deals"
          oninput="handleSearchInput(this.value)"
          placeholder="ابحث عن هاتف، شاحن، كود خصم، ساعة..." 
          data-i18n-placeholder="search_placeholder"
          class="w-full border rounded-xl pr-10 pl-9 py-2.5 text-xs focus:outline-none focus:border-rose-500 transition min-h-[42px]"
          style="background-color: var(--input-bg); border-color: var(--border-card); color: var(--text-main);"
        />
        <button id="mobile-search-clear" onclick="resetFilters()" class="hidden absolute left-3 top-1/2 -translate-y-1/2 text-xs opacity-50 hover:opacity-100 p-1 cursor-pointer" title="مسح">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>

      <!-- Active Promo Event Showcase Banner (Streamlined Minimal Strip) -->
      <section id="active-event-banner" class="p-2.5 sm:p-3 rounded-xl relative transition-all border flex flex-col md:flex-row md:items-center justify-between gap-2.5" aria-label="الحدث الترويجي الفعال" style="background-color: var(--bg-card); border-color: var(--border-card);">
        <div class="flex items-center gap-2 min-w-0">
          <div class="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-bold bg-rose-500/10 text-rose-500 flex-shrink-0">
            <span class="w-1.5 h-1.5 rounded-full bg-rose-500 animate-pulse"></span>
            <span id="active-event-badge" data-i18n="active_event_badge">حدث رسمي</span>
          </div>
          <h3 id="active-event-title" class="text-xs sm:text-sm font-bold tracking-tight truncate" style="color: var(--text-main);" data-i18n="active_event_title">
            تخفيضات عروض الشتاء Winter Offers 2026
          </h3>
          <p id="active-event-desc" class="hidden">عروض وتخفيضات رسمية نشطة حالياً مع أكواد حصرية مخصصة للجزائر وفرنسا — الأسعار بالدينار الجزائري وفق سعر السكوار الحقيقي.</p>
        </div>

        <!-- Active Event Coupon Chips with 1-click copy -->
        <div class="flex items-center gap-1.5 flex-wrap" id="active-event-coupons">
          <button onclick="copyReferralCode('WOAE06', this)" class="border border-dashed rounded-lg px-2 py-1 text-[11px] font-mono font-bold flex items-center gap-1 active:scale-95 transition touch-manipulation cursor-pointer hover:border-rose-500" style="background-color: var(--bg-elevated); border-color: var(--border-subtle); color: var(--text-main);" title="نسخ الكود WOAE06">
            <i class="fa-solid fa-ticket text-rose-500 text-[10px]"></i>
            <span>WOAE06</span>
            <span class="text-[10px] font-sans font-medium text-rose-500">(-6$)</span>
          </button>
          <button onclick="copyReferralCode('WOAE12', this)" class="border border-dashed rounded-lg px-2 py-1 text-[11px] font-mono font-bold flex items-center gap-1 active:scale-95 transition touch-manipulation cursor-pointer hover:border-rose-500" style="background-color: var(--bg-elevated); border-color: var(--border-subtle); color: var(--text-main);" title="نسخ الكود WOAE12">
            <i class="fa-solid fa-ticket text-rose-500 text-[10px]"></i>
            <span>WOAE12</span>
            <span class="text-[10px] font-sans font-medium text-rose-500">(-12$)</span>
          </button>
          <button onclick="copyReferralCode('WOAE23', this)" class="border border-dashed rounded-lg px-2 py-1 text-[11px] font-mono font-bold flex items-center gap-1 active:scale-95 transition touch-manipulation cursor-pointer hover:border-rose-500" style="background-color: var(--bg-elevated); border-color: var(--border-subtle); color: var(--text-main);" title="نسخ الكود WOAE23">
            <i class="fa-solid fa-ticket text-rose-500 text-[10px]"></i>
            <span>WOAE23</span>
            <span class="text-[10px] font-sans font-medium text-rose-500">(-23$)</span>
          </button>
          <button onclick="copyReferralCode('WOAE35', this)" class="border border-dashed rounded-lg px-2 py-1 text-[11px] font-mono font-bold flex items-center gap-1 active:scale-95 transition touch-manipulation cursor-pointer hover:border-rose-500" style="background-color: var(--bg-elevated); border-color: var(--border-subtle); color: var(--text-main);" title="نسخ الكود WOAE35">
            <i class="fa-solid fa-ticket text-rose-500 text-[10px]"></i>
            <span>WOAE35</span>
            <span class="text-[10px] font-sans font-medium text-rose-500">(-35$)</span>
          </button>
        </div>

        <div id="active-deals-keywords" class="hidden">
          <button onclick="handleSearchInput('Honor X70')">Honor X70 5G</button>
          <button onclick="handleSearchInput('realme 15T')">realme 15T 5G</button>
          <button onclick="handleSearchInput('OPPO A6 Pro')">OPPO A6 Pro</button>
          <button onclick="handleSearchInput('iQOO Z11s')">iQOO Z11s</button>
          <button onclick="handleSearchInput('Ryzen 5 8400F')">Ryzen 5 8400F</button>
          <button onclick="handleSearchInput('realme Watch 5')">realme Watch 5</button>
        </div>
      </section>

      <!-- Category Filter Pills -->
      <section class="border-b pb-3 w-full overflow-hidden" style="border-color: var(--border-card);" aria-label="Categories">
        <div class="flex items-center gap-2 overflow-x-auto no-scrollbar pb-1 text-xs font-semibold px-0.5 momentum-scroll w-full">
          <button onclick="setCategory('all')" id="cat-all" class="cat-pill min-h-[42px] px-3.5 py-2 rounded-xl bg-crimson-600 text-white whitespace-nowrap transition flex items-center gap-1.5 flex-shrink-0 active:scale-95 touch-manipulation shadow-sm">
            <span data-i18n="cat_all">الكل</span>
            <span id="count-all" class="text-[11px] font-mono opacity-80 bg-black/20 px-1.5 py-0.2 rounded">0</span>
          </button>
          <button onclick="setCategory('favs')" id="cat-favs" class="cat-pill min-h-[42px] px-3.5 py-2 rounded-xl border whitespace-nowrap transition flex items-center gap-1.5 flex-shrink-0 active:scale-95 touch-manipulation cursor-pointer" style="background-color: var(--bg-card); border-color: var(--border-card); color: var(--text-muted);">
            <i class="fa-solid fa-heart text-rose-500 text-xs"></i>
            <span data-i18n="cat_favs">المفضلة</span>
            <span id="count-favs" class="text-[11px] font-mono opacity-60">0</span>
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

      <!-- Country Filter Quick Pills (Ultra-High UX for Algerian Shoppers) -->
      <section class="pt-1.5 pb-1 w-full overflow-hidden" aria-label="Country Filter">
        <div class="flex items-center gap-1.5 overflow-x-auto no-scrollbar pb-1 text-xs font-semibold px-0.5 momentum-scroll w-full">
          <span class="text-[11px] font-bold flex items-center gap-1 pl-1 flex-shrink-0" style="color: var(--text-soft);">
            <i class="fa-solid fa-earth-americas text-[10px] text-emerald-500"></i>
            <span data-i18n="country_filter_label">تصفية حسب البلد:</span>
          </span>
          <button onclick="setCountryFilter('all')" id="country-all" class="country-pill min-h-[32px] px-3 py-1 rounded-lg text-xs font-bold transition flex items-center gap-1 flex-shrink-0 active:scale-95 touch-manipulation border" style="background-color: var(--text-main); color: var(--bg-page); border-color: var(--text-main);">
            <span data-i18n="country_all">كل البلدان 🌍</span>
          </button>
          <button onclick="setCountryFilter('canada')" id="country-canada" class="country-pill min-h-[32px] px-2.5 py-1 rounded-lg text-xs font-semibold transition flex items-center gap-1 flex-shrink-0 active:scale-95 touch-manipulation border" style="background-color: var(--bg-card); border-color: var(--border-card); color: var(--text-muted);">
            <span>كندا 🇨🇦</span>
          </button>
          <button onclick="setCountryFilter('korea')" id="country-korea" class="country-pill min-h-[32px] px-2.5 py-1 rounded-lg text-xs font-semibold transition flex items-center gap-1 flex-shrink-0 active:scale-95 touch-manipulation border" style="background-color: var(--bg-card); border-color: var(--border-card); color: var(--text-muted);">
            <span>كوريا 🇰🇷</span>
          </button>
          <button onclick="setCountryFilter('algeria')" id="country-algeria" class="country-pill min-h-[32px] px-2.5 py-1 rounded-lg text-xs font-semibold transition flex items-center gap-1 flex-shrink-0 active:scale-95 touch-manipulation border" style="background-color: var(--bg-card); border-color: var(--border-card); color: var(--text-muted);">
            <span>الجزائر 🇩🇿</span>
          </button>
          <button onclick="setCountryFilter('france')" id="country-france" class="country-pill min-h-[32px] px-2.5 py-1 rounded-lg text-xs font-semibold transition flex items-center gap-1 flex-shrink-0 active:scale-95 touch-manipulation border" style="background-color: var(--bg-card); border-color: var(--border-card); color: var(--text-muted);">
            <span>فرنسا 🇫🇷</span>
          </button>
        </div>
      </section>

      <!-- Section Title, Live Count & Sorting UX -->
      <div class="flex flex-wrap items-center justify-between gap-2 border-b pb-2.5 pt-1" style="border-color: var(--border-card);">
        <div class="flex items-center gap-2">
          <h1 class="text-xs sm:text-sm font-bold flex items-center gap-1.5 font-heading" style="color: var(--text-main);">
            <i class="fa-solid fa-fire text-rose-500" aria-hidden="true"></i>
            <span data-i18n="deals_section_heading">أحدث صفقات وتخفيضات AliExpress بالدينار الجزائري</span>
          </h1>
          <span class="text-[11px] text-emerald-500 flex items-center gap-1.5 font-medium">
            <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span id="live-deals-counter" class="font-mono">...</span>
          </span>
        </div>

        <!-- Sort Selector -->
        <div class="flex items-center gap-1.5 text-xs">
          <label for="deal-sort-select" class="text-[11px] font-medium" style="color: var(--text-muted);" data-i18n="sort_label">ترتيب:</label>
          <select id="deal-sort-select" onchange="setDealSort(this.value)" class="text-xs font-semibold rounded-lg px-2 py-1 border outline-none cursor-pointer transition" style="background-color: var(--bg-card); border-color: var(--border-card); color: var(--text-main);">
            <option value="newest" data-i18n="sort_newest">الأحدث أولاً 🕒</option>
            <option value="price_asc" data-i18n="sort_price_asc">الأقل سعراً 📉</option>
            <option value="price_desc" data-i18n="sort_price_desc">الأعلى سعراً 📈</option>
          </select>
        </div>
      </div>

      <!-- Deals Grid (Cards View) -->
      <section id="deals-grid" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3 sm:gap-3.5 md:gap-4 lg:gap-5" aria-label="قائمة الصفقات">
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

      <!-- ========================================== -->
      <!-- HIGH-RANKING SEMANTIC SEO SHOPPING GUIDE   -->
      <!-- ========================================== -->
      <section id="seo-shopping-guide" class="border rounded-2xl transition-colors mt-8 overflow-hidden" style="background-color: var(--bg-card); border-color: var(--border-card);">
        <details class="group" id="seo-details">
          <summary class="p-4 sm:p-5 flex items-center justify-between cursor-pointer list-none select-none hover:bg-white/[0.02] transition">
            <div class="flex items-center gap-2.5">
              <div class="w-8 h-8 rounded-lg bg-crimson-500/10 text-crimson-500 flex items-center justify-center text-sm font-bold flex-shrink-0">
                <i class="fa-solid fa-book-open"></i>
              </div>
              <div>
                <h2 class="text-xs sm:text-sm font-bold" style="color: var(--text-main);" data-i18n="seo_guide_title">
                  عروض وتخفيضات علي اكسبراس في الجزائر — AliExpress Deals DZ
                </h2>
                <p class="text-[11px] opacity-75" style="color: var(--text-muted);" data-i18n="seo_guide_subtitle">
                  دليل التسوق، بريدي موب، الشحن والجمارك بالجزائر (اضغط لعرض الدليل الشامل)
                </p>
              </div>
            </div>
            <div class="flex items-center gap-2 text-xs font-bold text-crimson-500 flex-shrink-0">
              <span class="hidden sm:inline text-[11px]">عرض الدليل</span>
              <i class="fa-solid fa-chevron-down group-open:rotate-180 transition-transform text-xs"></i>
            </div>
          </summary>

          <div class="p-5 sm:p-7 border-t space-y-6" style="border-color: var(--border-card);">
            <div class="space-y-2 border-b pb-4" style="border-color: var(--border-card);">
              <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold bg-crimson-500/10 text-crimson-500 border border-crimson-500/20">
                <i class="fa-solid fa-bullhorn text-xs"></i>
                <span data-i18n="seo_badge">دليل المتسوق الجزائري 🇩🇿</span>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6 text-xs sm:text-sm leading-relaxed" style="color: var(--text-muted);">
              
              <!-- SEO Block 1: Deals & Discounts -->
              <div class="space-y-2 p-4 rounded-xl border" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
                <h3 class="font-bold text-sm sm:text-base flex items-center gap-2" style="color: var(--text-main);">
                  <i class="fa-solid fa-fire text-crimson-500"></i>
                  <span data-i18n="seo_block1_h">أقوى عروض علي اكسبراس في الجزائر (AliExpress DZ)</span>
                </h3>
                <p data-i18n="seo_block1_p">
                  يقوم موقع DealScout DZ بمتابعة وتحديث عروض علي اكسبراس يومياً، بما يشمل عروض السوبر ديلز (SuperDeals)، التخفيضات الموسمية، وتجميعات المنتجات الأكثر طلباً في الجزائر مع حساب التكلفة الفعلية بالدينار الجزائري (DZD) حسب سعر صرف السكوار المحدث.
                </p>
              </div>

          <!-- SEO Block 2: Buying in Algeria -->
          <div class="space-y-2 p-4 rounded-xl border" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
            <h3 class="font-bold text-sm sm:text-base flex items-center gap-2" style="color: var(--text-main);">
              <i class="fa-solid fa-credit-card text-emerald-500"></i>
              <span data-i18n="seo_block2_h">طريقة الشراء من علي اكسبراس في الجزائر والدفع ببريدي موب</span>
            </h3>
            <p data-i18n="seo_block2_p">
              لإتمام عملية شراء من علي اكسبراس في الجزائر، يمكنك شحن بطاقتك البنكية الدولية (مثل Bybit أو RedotPay أو Paysera) بالدينار الجزائري عبر تطبيق BaridiMob من خلال منصات P2P المعتمدة (Binance P2P)، ثم طلب المنتجات مباشرة مع التوصيل إلى مكتب بريد الجزائر الأقرب إليك.
            </p>
          </div>

          <!-- SEO Block 3: Coins & Promo Codes -->
          <div class="space-y-2 p-4 rounded-xl border" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
            <h3 class="font-bold text-sm sm:text-base flex items-center gap-2" style="color: var(--text-main);">
              <i class="fa-solid fa-coins text-amber-500"></i>
              <span data-i18n="seo_block3_h">تخفيض عملات وكوبونات علي اكسبراس الجزائر (Coins & Coupons)</span>
            </h3>
            <p data-i18n="seo_block3_p">
              استفد من أداة توليد روابط العملات الحصرية على موقعنا لتحويل أي رابط منتج إلى رابط خصم العملات الأقصى (Coins Discount) لتوفير ما يصل إلى 70% من السعر، بالإضافة إلى نسخ أكواد الخصم والبرومو كود الترويجية الفعالة فور صدورها.
            </p>
          </div>

          <!-- SEO Block 4: Telegram Channel Conversion CTA -->
          <div class="space-y-2 p-4 rounded-xl border" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
            <h3 class="font-bold text-sm sm:text-base flex items-center gap-2" style="color: var(--text-main);">
              <i class="fa-brands fa-telegram text-[#229ED9]"></i>
              <span data-i18n="seo_block4_h">قناة التيليجرام لعروض علي اكسبراس في الجزائر</span>
            </h3>
            <p data-i18n="seo_block4_p">
              الهدف الرئيسي من منصتنا هو إيصال أفضل التخفيضات إليك في الثواني الأولى. نظراً لأن الصفقات القوية تنفد كمياتها بسرعة، ننصحك بالانضمام فوراً إلى قناة التيليجرام الرسمية (@DzAliexpress0) لتصلك الإشعارات اللحظية بروابط الشراء المباشرة.
            </p>
            <div class="pt-1.5">
              <a href="https://t.me/DzAliexpress0" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-2 min-h-[40px] px-4 py-2 rounded-xl bg-[#229ED9] hover:bg-[#1c8cc1] text-white font-bold text-xs shadow-md transition active:scale-95 touch-manipulation cursor-pointer">
                <i class="fa-brands fa-telegram text-sm"></i>
                <span data-i18n="seo_block4_btn">انضم لقناة صفقات الجزائر (@DzAliexpress0)</span>
              </a>
            </div>
          </div>

        </div>

        <!-- AI Overview / GEO Quick Fact Sheet for Answer Engines (Perplexity, SearchGPT, Gemini) -->
        <div id="ai-overview-facts" class="border rounded-xl p-4 sm:p-5 space-y-3" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
          <div class="flex items-center justify-between flex-wrap gap-2 border-b pb-2.5" style="border-color: var(--border-card);">
            <div class="inline-flex items-center gap-2 px-2.5 py-0.5 rounded text-xs font-bold bg-sky-500/10 text-sky-500 border border-sky-500/20">
              <i class="fa-solid fa-robot text-xs"></i>
              <span data-i18n="geo_badge">ملخص الذكاء الاصطناعي والإجابات المباشرة (AI Overview & GEO)</span>
            </div>
            <span class="text-[11px] font-mono opacity-70">llms.txt compliant</span>
          </div>
          <h3 class="font-bold text-sm" style="color: var(--text-main);" data-i18n="geo_summary_title">
            حقائق سريعة لـ DealScout DZ والمحركات الذكية
          </h3>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs leading-relaxed" style="color: var(--text-muted);">
            <div class="p-3 rounded-lg border" style="background-color: var(--bg-card); border-color: var(--border-card);">
              <b class="text-emerald-500 block text-xs mb-1" data-i18n="geo_fact_currency_title">العملة وأسعار الصرف:</b>
              <span data-i18n="geo_fact_currency_desc">الدينار الجزائري (DZD) محسوب بسعر السكوار اللحظي (SquareAlgerie.com).</span>
            </div>
            <div class="p-3 rounded-lg border" style="background-color: var(--bg-card); border-color: var(--border-card);">
              <b class="text-amber-500 block text-xs mb-1" data-i18n="geo_fact_payment_title">طريقة الدفع الرسمية:</b>
              <span data-i18n="geo_fact_payment_desc">BaridiMob / CCP ← منصة Binance P2P ← بطاقة Bybit ماستركارد أو RedotPay.</span>
            </div>
            <div class="p-3 rounded-lg border" style="background-color: var(--bg-card); border-color: var(--border-card);">
              <b class="text-sky-500 block text-xs mb-1" data-i18n="geo_fact_shipping_title">التوصيل والاستلام:</b>
              <span data-i18n="geo_fact_shipping_desc">بريد الجزائر (Algérie Poste / EMS)، إعفاء تام للطرود الشخصية غير التجارية.</span>
            </div>
            <div class="p-3 rounded-lg border" style="background-color: var(--bg-card); border-color: var(--border-card);">
              <b class="text-purple-500 block text-xs mb-1" data-i18n="geo_fact_coins_title">أداة العملات (Coins):</b>
              <span data-i18n="geo_fact_coins_desc">مولد روابط مجاني لتفعيل خصم 50% إلى 70% بدلاً من 2% القياسية.</span>
            </div>
          </div>
        </div>

        <!-- Internal Navigation & Cross-Links (Prevent Orphan Pages & Boost PageRank) -->
        <div class="border-t pt-4 grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs" style="border-color: var(--border-card);">
          <a href="#cards" onclick="showPage('cards')" class="p-3 rounded-xl border flex items-center gap-2.5 transition hover:border-emerald-500/50" style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-main);">
            <div class="w-8 h-8 rounded-lg bg-emerald-500/15 text-emerald-500 flex items-center justify-center flex-shrink-0 text-sm">
              <i class="fa-solid fa-credit-card"></i>
            </div>
            <div class="min-w-0">
              <div class="font-bold text-xs truncate" data-i18n="crosslink_cards_title">دليل بطاقات الدفع وبريدي موب</div>
              <div class="text-[10px] opacity-75 truncate" data-i18n="crosslink_cards_sub">Bybit مجانية وRedotPay</div>
            </div>
          </a>
          <a href="#coins" onclick="showPage('coins')" class="p-3 rounded-xl border flex items-center gap-2.5 transition hover:border-amber-500/50" style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-main);">
            <div class="w-8 h-8 rounded-lg bg-amber-500/15 text-amber-500 flex items-center justify-center flex-shrink-0 text-sm">
              <i class="fa-solid fa-coins"></i>
            </div>
            <div class="min-w-0">
              <div class="font-bold text-xs truncate" data-i18n="crosslink_coins_title">بوت ومولد تخفيض العملات Coins</div>
              <div class="text-[10px] opacity-75 truncate" data-i18n="crosslink_coins_sub">وفر حتى 70% من السعر</div>
            </div>
          </a>
          <a href="#faq" onclick="showPage('faq')" class="p-3 rounded-xl border flex items-center gap-2.5 transition hover:border-sky-500/50" style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-main);">
            <div class="w-8 h-8 rounded-lg bg-sky-500/15 text-sky-500 flex items-center justify-center flex-shrink-0 text-sm">
              <i class="fa-solid fa-circle-question"></i>
            </div>
            <div class="min-w-0">
              <div class="font-bold text-xs truncate" data-i18n="crosslink_faq_title">الأسئلة الشائعة وقوانين الجمارك</div>
              <div class="text-[10px] opacity-75 truncate" data-i18n="crosslink_faq_sub">الشحن واستلام الطرود بالبريد</div>
            </div>
          </a>
        </div>

        <!-- Popular Algerian Search Keywords Tags Cloud -->
        <div class="border-t pt-4 space-y-2 text-xs" style="border-color: var(--border-card);">
          <div class="font-bold text-xs uppercase tracking-wider flex items-center gap-1.5" style="color: var(--text-main);">
            <i class="fa-solid fa-tags text-rose-500"></i>
            <span data-i18n="seo_tags_title">الكلمات الأكثر بحثاً في الجزائر:</span>
          </div>
          <div class="flex items-center gap-1.5 flex-wrap text-[11px]">
            <span class="px-2 py-0.5 rounded border" style="background-color: var(--bg-elevated); border-color: var(--border-card);">aliexpressdz</span>
            <span class="px-2 py-0.5 rounded border" style="background-color: var(--bg-elevated); border-color: var(--border-card);">aliexpress deals dz</span>
            <span class="px-2 py-0.5 rounded border" style="background-color: var(--bg-elevated); border-color: var(--border-card);">عروض علي اكسبراس</span>
            <span class="px-2 py-0.5 rounded border" style="background-color: var(--bg-elevated); border-color: var(--border-card);">شراء من علي اكسبراس في الجزائر</span>
            <span class="px-2 py-0.5 rounded border" style="background-color: var(--bg-elevated); border-color: var(--border-card);">تخفيضات علي اكسبراس الجزائر</span>
            <span class="px-2 py-0.5 rounded border" style="background-color: var(--bg-elevated); border-color: var(--border-card);">كوبونات علي اكسبراس</span>
            <span class="px-2 py-0.5 rounded border" style="background-color: var(--bg-elevated); border-color: var(--border-card);">الشراء من بريدي موب</span>
            <span class="px-2 py-0.5 rounded border" style="background-color: var(--bg-elevated); border-color: var(--border-card);">عملات علي اكسبراس</span>
            <span class="px-2 py-0.5 rounded border" style="background-color: var(--bg-elevated); border-color: var(--border-card);">aliexpress algerie dzd</span>
            <span class="px-2 py-0.5 rounded border" style="background-color: var(--bg-elevated); border-color: var(--border-card);">code promo aliexpress algerie</span>
          </div>
          </div>
        </details>
      </section>

    </div>

    <!-- ───────────────────────────────────────────────────────── -->
    <!-- PAGE: PARCEL TRACKER (SUIVI COLIS DZ)                     -->
    <!-- ───────────────────────────────────────────────────────── -->
    <div id="page-tracking" class="page-view hidden space-y-6 max-w-4xl mx-auto">

      <!-- Tracker Search Console -->
      <div class="border rounded-2xl p-6 sm:p-8 space-y-5 transition-all relative" style="background-color: var(--bg-card); border-color: var(--border-card); box-shadow: var(--shadow-card);">
        
        <!-- Header -->
        <div class="space-y-1.5 text-right">
          <div class="inline-flex items-center gap-2 px-2.5 py-1 rounded-md text-[11px] font-mono font-medium border" style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-muted);">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
            <span data-i18n="tracking_badge">شبكة التتبع اللوجستي • الجزائر 🇩🇿</span>
          </div>
          <h2 class="text-xl sm:text-2xl font-black tracking-tight" style="color: var(--text-main);" data-i18n="tracking_hero_title">
            تتبع الشحنات والطرود البريدية
          </h2>
          <p class="text-xs sm:text-sm leading-relaxed opacity-75 max-w-2xl" style="color: var(--text-muted);" data-i18n="tracking_hero_desc">
            تتبع مباشر لشحنات AliExpress Choice وشبكة بريد الجزائر مع كشف الرقم الفرعي ومحطات الشحن.
          </p>
        </div>

        <!-- Search Input Bar -->
        <div class="space-y-3 pt-1">
          <div class="flex flex-col sm:flex-row items-stretch gap-2">
            <div class="relative flex-1">
              <i class="fa-solid fa-barcode absolute right-4 top-1/2 -translate-y-1/2 text-sm opacity-40 pointer-events-none"></i>
              <input 
                type="text" 
                id="tracking-input-num" 
                placeholder="أدخل رقم التتبع (LP006... أو RE...DZ أو CP...AE)" 
                class="w-full border rounded-xl pr-11 pl-20 py-3.5 text-xs sm:text-sm focus:outline-none focus:ring-1 focus:ring-zinc-400 dark:focus:ring-zinc-500 transition min-h-[50px] font-mono tracking-wider"
                style="background-color: var(--input-bg); border-color: var(--border-card); color: var(--text-main);"
                onkeydown="if(event.key==='Enter') submitTracking()"
              />
              <button 
                type="button" 
                onclick="pasteToTrackingInput()" 
                id="tracking-paste-btn"
                title="لصق من الحافظة"
                class="absolute left-2.5 top-1/2 -translate-y-1/2 px-2.5 py-1.5 rounded-lg border text-[11px] font-semibold flex items-center gap-1.5 transition active:scale-95 touch-manipulation cursor-pointer hover:border-zinc-400"
                style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-muted);"
              >
                <i class="fa-regular fa-paste text-xs"></i>
                <span data-i18n="btn_paste">لصق</span>
              </button>
            </div>

            <button 
              type="button" 
              onclick="submitTracking()" 
              id="tracking-submit-btn"
              class="min-h-[50px] px-6 py-3.5 rounded-xl font-bold text-xs sm:text-sm flex items-center justify-center gap-2 active:scale-95 transition cursor-pointer flex-shrink-0 shadow-sm"
              style="background-color: var(--text-main); color: var(--bg-page);"
            >
              <i class="fa-solid fa-magnifying-glass text-xs"></i>
              <span data-i18n="btn_track_parcel">تتبع الشحنة</span>
            </button>
          </div>

          <!-- Quick Samples & Recent History -->
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pt-1 text-xs" style="color: var(--text-muted);">
            <div class="flex items-center gap-1.5 flex-wrap">
              <span class="text-[11px] opacity-60 font-semibold" data-i18n="tracking_quick_examples">أمثلة:</span>
              <button type="button" onclick="setTrackingSample('CP032359951AE')" class="font-mono text-[11px] px-2 py-0.5 rounded border hover:border-zinc-400 transition active:scale-95 cursor-pointer" style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-main);">CP...AE (UPU)</button>
              <button type="button" onclick="setTrackingSample('LP00685412978432')" class="font-mono text-[11px] px-2 py-0.5 rounded border hover:border-zinc-400 transition active:scale-95 cursor-pointer" style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-main);">LP006... (Choice)</button>
              <button type="button" onclick="setTrackingSample('RE984125874DZ')" class="font-mono text-[11px] px-2 py-0.5 rounded border hover:border-zinc-400 transition active:scale-95 cursor-pointer" style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-main);">RE...DZ (بريد الجزائر)</button>
            </div>
            <div id="tracking-recent-wrap" class="hidden flex items-center gap-1.5 flex-wrap">
              <span class="text-[11px] opacity-60 flex items-center gap-1 font-semibold"><i class="fa-solid fa-clock-rotate-left text-[10px]"></i> السجل:</span>
              <div id="tracking-recent-list" class="flex items-center gap-1 flex-wrap"></div>
            </div>
          </div>

          <div id="tracking-error" class="hidden text-xs text-rose-500 flex items-center gap-1.5 pt-1">
            <i class="fa-solid fa-circle-exclamation text-xs"></i>
            <span id="tracking-error-text">يرجى إدخال رقم تتبع صالح.</span>
          </div>
        </div>
      </div>

      <!-- Tracking Results Card (Clean Architecture) -->
      <div id="tracking-result-card" class="hidden border rounded-2xl p-5 sm:p-7 space-y-6 transition-all" style="background-color: var(--bg-card); border-color: var(--border-card); box-shadow: var(--shadow-card);">
        
        <!-- Header Info Bar -->
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b pb-5" style="border-color: var(--border-card);">
          <div class="space-y-2">
            <div class="flex items-center gap-2 flex-wrap">
              <span id="tracking-carrier-badge" class="px-2.5 py-1 rounded-lg text-xs font-semibold border flex items-center gap-1.5" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
                <span id="tracking-carrier-flag" class="text-sm">🌐</span>
                <span id="tracking-carrier-name" style="color: var(--text-main);">AliExpress Choice / Cainiao</span>
              </span>
              <span id="tracking-status-badge" class="px-2.5 py-1 rounded-lg text-xs font-semibold bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20 flex items-center gap-1.5">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                <span id="tracking-status-text">في مسار الشحن الدولي</span>
              </span>
            </div>

            <!-- Trajectory Path -->
            <div class="flex items-center gap-2 text-xs font-medium" style="color: var(--text-muted);">
              <span class="flex items-center gap-1 font-bold" style="color: var(--text-main);">
                <span id="tracking-route-origin-flag">🇨🇳</span>
                <span id="tracking-route-origin">الصين</span>
              </span>
              <i class="fa-solid fa-arrow-left-long text-xs opacity-50 px-1"></i>
              <span class="flex items-center gap-1 font-bold" style="color: var(--text-main);">
                <span>🇩🇿</span>
                <span>الجزائر (بريد بلديتك)</span>
              </span>
            </div>

            <!-- Number Display with 1-click Copy -->
            <div class="flex items-center gap-2 pt-1">
              <span class="text-xs opacity-60 font-medium" style="color: var(--text-muted);">رقم الشحنة:</span>
              <span id="tracking-result-num" class="font-mono font-bold text-sm sm:text-base tracking-wider px-2.5 py-0.5 rounded border" style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-main);">...</span>
              <button onclick="copyTrackingNum()" class="text-xs px-2.5 py-1 rounded-lg border flex items-center gap-1 transition active:scale-95 cursor-pointer hover:border-zinc-400" style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-main);">
                <i class="fa-regular fa-copy text-xs" id="tracking-copy-icon"></i>
                <span id="tracking-copy-text">نسخ</span>
              </button>
            </div>
          </div>

          <!-- Quick Metrics Grid -->
          <div class="grid grid-cols-2 sm:grid-cols-1 gap-2 sm:min-w-[200px] text-xs">
            <div class="border p-2.5 rounded-xl space-y-0.5" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
              <div class="text-[10px] opacity-60" style="color: var(--text-muted);">المدة المقدرة:</div>
              <div id="tracking-est-time" class="font-bold text-xs font-mono" style="color: var(--text-main);">14 - 25 يوماً</div>
            </div>
            <div class="border p-2.5 rounded-xl space-y-0.5" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
              <div class="text-[10px] opacity-60" style="color: var(--text-muted);">الخدمة:</div>
              <div id="tracking-service-badge" class="font-bold text-xs truncate" style="color: var(--text-main);">AliExpress Choice رسمي</div>
            </div>
          </div>
        </div>

        <!-- Guidance Note (Non-slop alert) -->
        <div id="tracking-advisory-card" class="rounded-xl p-3.5 border flex items-start gap-3 transition" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
          <i class="fa-solid fa-circle-info text-sm opacity-60 mt-0.5" id="tracking-advisory-icon" style="color: var(--text-main);"></i>
          <div class="space-y-0.5 flex-1 text-xs">
            <h4 id="tracking-advisory-title" class="font-bold text-xs sm:text-sm" style="color: var(--text-main);">
              الشحنة مسجلة حديثاً — بانتظار أول فحص فيزيائي لدى الناقل
            </h4>
            <p id="tracking-advisory-body" class="leading-relaxed opacity-75 text-[11px] sm:text-xs" style="color: var(--text-muted);">
              قام البائع بتوليد بوليصة الشحن. يستغرق تسجيل أول محطة فعلية عادة بين 24 إلى 72 ساعة.
            </p>
          </div>
        </div>

        <!-- Minimalist 5-Step Algerian Delivery Journey -->
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <h4 class="font-bold text-xs uppercase tracking-wider flex items-center gap-2" style="color: var(--text-main);">
              <i class="fa-solid fa-route text-xs opacity-60"></i>
              <span>مراحل التوصيل في الجزائر:</span>
            </h4>
            <span class="text-[11px] font-mono opacity-80" style="color: var(--text-muted);" id="tracking-journey-progress">المرحلة 1 من 5</span>
          </div>

          <!-- Sleek Horizontal Pipeline -->
          <div id="tracking-stages-container" class="grid grid-cols-1 sm:grid-cols-5 gap-2 text-xs">
            <!-- Stage 1 -->
            <div id="track-step-1" class="p-3 rounded-xl border space-y-1 relative transition" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
              <div class="flex items-center justify-between">
                <span class="w-5 h-5 rounded-full bg-emerald-500 text-white font-bold text-[10px] flex items-center justify-center">1</span>
                <i class="fa-solid fa-box text-xs opacity-50"></i>
              </div>
              <div class="font-bold text-xs pt-1" style="color: var(--text-main);">1. المستودع</div>
              <p class="text-[10px] opacity-60" style="color: var(--text-muted);">انطلاق الطرد</p>
            </div>
            <!-- Stage 2 -->
            <div id="track-step-2" class="p-3 rounded-xl border space-y-1 relative transition" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
              <div class="flex items-center justify-between">
                <span class="w-5 h-5 rounded-full bg-zinc-600 text-white font-bold text-[10px] flex items-center justify-center">2</span>
                <i class="fa-solid fa-plane text-xs opacity-50"></i>
              </div>
              <div class="font-bold text-xs pt-1" style="color: var(--text-main);">2. الشحن الجوي</div>
              <p class="text-[10px] opacity-60" style="color: var(--text-muted);">ترانزيت دولي</p>
            </div>
            <!-- Stage 3 -->
            <div id="track-step-3" class="p-3 rounded-xl border space-y-1 relative transition" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
              <div class="flex items-center justify-between">
                <span class="w-5 h-5 rounded-full bg-zinc-600 text-white font-bold text-[10px] flex items-center justify-center">3</span>
                <i class="fa-solid fa-warehouse text-xs opacity-50"></i>
              </div>
              <div class="font-bold text-xs pt-1" style="color: var(--text-main);">3. فرز CTN الجزائر</div>
              <p class="text-[10px] opacity-60" style="color: var(--text-muted);">مطار العاصمة</p>
            </div>
            <!-- Stage 4 -->
            <div id="track-step-4" class="p-3 rounded-xl border space-y-1 relative transition" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
              <div class="flex items-center justify-between">
                <span class="w-5 h-5 rounded-full bg-zinc-600 text-white font-bold text-[10px] flex items-center justify-center">4</span>
                <i class="fa-solid fa-stamp text-xs opacity-50"></i>
              </div>
              <div class="font-bold text-xs pt-1" style="color: var(--text-main);">4. الجمارك</div>
              <p class="text-[10px] opacity-60" style="color: var(--text-muted);">معفى للاستعمال الشخصي</p>
            </div>
            <!-- Stage 5 -->
            <div id="track-step-5" class="p-3 rounded-xl border space-y-1 relative transition" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
              <div class="flex items-center justify-between">
                <span class="w-5 h-5 rounded-full bg-zinc-600 text-white font-bold text-[10px] flex items-center justify-center">5</span>
                <i class="fa-solid fa-envelope text-xs opacity-50"></i>
              </div>
              <div class="font-bold text-xs pt-1" style="color: var(--text-main);">5. بريد بلديتك</div>
              <p class="text-[10px] opacity-60" style="color: var(--text-muted);">جاهز للاستلام</p>
            </div>
          </div>
        </div>

        <!-- Checkpoints Timeline Feed -->
        <div id="tracking-checkpoints-wrap" class="space-y-3 pt-3 border-t hidden" style="border-color: var(--border-card);">
          <h4 class="font-bold text-xs uppercase tracking-wider flex items-center gap-2" style="color: var(--text-main);">
            <i class="fa-solid fa-clock-rotate-left text-xs opacity-60"></i>
            <span>سجل المحطات (Checkpoints):</span>
          </h4>
          <div id="tracking-checkpoints-list" class="space-y-2 text-xs border-r pr-3 mr-1" style="border-color: var(--border-subtle);">
            <!-- Dynamic checkpoints injected here -->
          </div>
        </div>

        <!-- External Verification Portals (Minimalist row) -->
        <div class="space-y-2.5 pt-4 border-t" style="border-color: var(--border-card);">
          <div class="flex items-center justify-between flex-wrap gap-2">
            <h4 class="text-xs font-bold" style="color: var(--text-main);">
              فحص مباشر برقمك على منصات التتبع العالمية:
            </h4>
            <span class="text-[10px] font-mono opacity-60" style="color: var(--text-muted);">تفتح بالرقم مباشرة ↗</span>
          </div>
          
          <div class="grid grid-cols-2 sm:grid-cols-5 gap-2 text-xs">
            <!-- 1. 17TRACK -->
            <a id="btn-portal-17track" href="https://t.17track.net/ar" target="_blank" rel="noopener noreferrer" class="p-2.5 rounded-xl border flex items-center justify-between gap-1.5 font-semibold transition hover:border-zinc-400 active:scale-95 touch-manipulation" style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-main);">
              <span>17TRACK</span>
              <span class="opacity-40 text-[10px]">↗</span>
            </a>
            
            <!-- 2. Postal Ninja -->
            <a id="btn-portal-ninja" href="https://postal.ninja/ar" target="_blank" rel="noopener noreferrer" class="p-2.5 rounded-xl border flex items-center justify-between gap-1.5 font-semibold transition hover:border-zinc-400 active:scale-95 touch-manipulation" style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-main);">
              <span>Postal Ninja</span>
              <span class="opacity-40 text-[10px]">↗</span>
            </a>

            <!-- 3. Cainiao Official -->
            <a id="btn-portal-cainiao" href="https://global.cainiao.com" target="_blank" rel="noopener noreferrer" class="p-2.5 rounded-xl border flex items-center justify-between gap-1.5 font-semibold transition hover:border-zinc-400 active:scale-95 touch-manipulation" style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-main);">
              <span>Cainiao Global</span>
              <span class="opacity-40 text-[10px]">↗</span>
            </a>

            <!-- 4. ParcelsApp -->
            <a id="btn-portal-parcels" href="https://parcelsapp.com/en" target="_blank" rel="noopener noreferrer" class="p-2.5 rounded-xl border flex items-center justify-between gap-1.5 font-semibold transition hover:border-zinc-400 active:scale-95 touch-manipulation" style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-main);">
              <span>ParcelsApp</span>
              <span class="opacity-40 text-[10px]">↗</span>
            </a>

            <!-- 5. Algérie Poste -->
            <a id="btn-portal-poste" href="https://t.17track.net/ar" target="_blank" rel="noopener noreferrer" class="p-2.5 rounded-xl border flex items-center justify-between gap-1.5 font-semibold transition hover:border-emerald-500 active:scale-95 touch-manipulation col-span-2 sm:col-span-1" style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-main);">
              <span>بريد الجزائر</span>
              <span class="opacity-40 text-[10px]">↗</span>
            </a>
          </div>
        </div>

      </div>

      <!-- Minimalist Delivery Guide (Clean Monochrome / Restrained) -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
        <div class="border rounded-xl p-4 space-y-1.5 transition" style="background-color: var(--bg-card); border-color: var(--border-card);">
          <div class="font-bold text-xs" style="color: var(--text-main);" data-i18n="track_card1_title">مدة وصول الشحنات</div>
          <p class="text-[11px] leading-relaxed opacity-75" style="color: var(--text-muted);" data-i18n="track_card1_desc">
            تستغرق شحنات AliExpress Choice من 14 إلى 25 يوماً للجزائر، بينما الشحن الاقتصادي العادي بين 25 و35 يوماً عبر بريد الجزائر.
          </p>
        </div>

        <div class="border rounded-xl p-4 space-y-1.5 transition" style="background-color: var(--bg-card); border-color: var(--border-card);">
          <div class="font-bold text-xs" style="color: var(--text-main);" data-i18n="track_card2_title">الجمارك والطرود الشخصية</div>
          <p class="text-[11px] leading-relaxed opacity-75" style="color: var(--text-muted);" data-i18n="track_card2_desc">
            الطرود للاستعمال الشخصي معفاة من الرسوم الجمركية. تجنب طلب أكثر من 3 قطع من نفس السلعة في شحنة واحدة لتفادي الصفة التجارية.
          </p>
        </div>

        <div class="border rounded-xl p-4 space-y-1.5 transition" style="background-color: var(--bg-card); border-color: var(--border-card);">
          <div class="font-bold text-xs" style="color: var(--text-main);" data-i18n="track_card3_title">استلام الطرد من البريد</div>
          <p class="text-[11px] leading-relaxed opacity-75" style="color: var(--text-muted);" data-i18n="track_card3_desc">
            عند وصول الطرد لبريد بلديتك، توجه مصحوباً ببطاقة التعريف الوطنية ودفع رسم التخليص البريدي الرمزي (130-250 دج).
          </p>
        </div>
      </div>

      <!-- Legacy container stub kept hidden for compatibility -->
      <div id="YQContainer" class="hidden"></div>

    </div>

    <!-- ───────────────────────────────────────────────────────── -->
    <!-- PAGE: CARDS & REFERRALS (BYBIT, REDOTPAY, BINANCE P2P)    -->
    <!-- ───────────────────────────────────────────────────────── -->
    <div id="page-cards" class="page-view hidden space-y-6">
      
      <!-- Hero Banner -->
      <div class="border rounded-xl p-5 sm:p-6 space-y-3" style="background-color: var(--bg-card); border-color: var(--border-card);">
        <div class="inline-flex items-center gap-2 px-2.5 py-1 rounded text-xs font-bold bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20">
          <i class="fa-solid fa-credit-card"></i>
          <span data-i18n="cards_badge">دليل بطاقات الدفع والشحن بالدينار الجزائري 🇩🇿</span>
        </div>
        <h1 class="text-lg sm:text-xl font-bold tracking-tight" style="color: var(--text-main);" data-i18n="cards_hero_title">
          كيف تشتري من AliExpress وأنت في الجزائر؟ | أفضل البطاقات والشحن بـ BaridiMob
        </h1>
        <p class="text-xs sm:text-sm leading-relaxed max-w-3xl" style="color: var(--text-muted);" data-i18n="cards_hero_desc">
          لأن البطاقات البنكية الجزائرية المحلية لا تعمل في المواقع العالمية، إليك الحل الرسمي والمجرب: احصل على بطاقة افتراضية دولية مجانية، واشحنها مباشرة بالدينار الجزائري عبر بريدي موب ومنصة بينانس دون وسطاء وبأقل تكلفة!
        </p>
      </div>

      <!-- 3 Featured Partner Cards Grid -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        
        <!-- Partner 1: Bybit Virtual Mastercard -->
        <div class="border rounded-xl p-5 flex flex-col justify-between transition-colors hover:border-emerald-500/50 space-y-4" style="background-color: var(--bg-card); border-color: var(--border-card);">
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <div class="w-9 h-9 rounded-lg bg-emerald-500/10 text-emerald-500 flex items-center justify-center text-base font-bold">
                <i class="fa-solid fa-credit-card"></i>
              </div>
              <span class="text-[11px] font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20" data-i18n="cards_bybit_badge">مجانية 100% — 0 دج</span>
            </div>
            <h3 class="font-bold text-sm sm:text-base" style="color: var(--text-main);" data-i18n="cards_bybit_title">بطاقة Bybit Card (MasterCard)</h3>
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
            <div class="flex items-center justify-between p-2.5 rounded-lg border" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
              <div class="min-w-0">
                <div class="text-[10px] opacity-70" data-i18n="cards_ref_code">كود التسجيل الحصري:</div>
                <div class="font-mono font-bold text-sm text-emerald-500">L9LLRP5</div>
              </div>
              <button onclick="copyReferralCode('L9LLRP5', this)" class="min-h-[36px] px-2.5 py-1 text-xs font-bold rounded border hover:bg-emerald-500/10 active:scale-95 transition flex items-center gap-1.5 touch-manipulation cursor-pointer" style="border-color: var(--border-card); color: var(--text-main);">
                <i class="fa-regular fa-copy"></i>
                <span data-i18n="cards_btn_copy_code">نسخ الكود</span>
              </button>
            </div>
            <a href="https://www.bybit.com/invite?ref=L9LLRP5&medium=referral&utm_campaign=evergreen&share_to=Telegram" target="_blank" rel="noopener noreferrer" class="w-full min-h-[40px] rounded-lg bg-emerald-600 hover:bg-emerald-500 active:scale-[0.98] text-white font-bold text-xs sm:text-sm py-2 px-3 flex items-center justify-center gap-2 shadow-sm transition touch-manipulation">
              <i class="fa-solid fa-arrow-up-right-from-square text-xs"></i>
              <span data-i18n="cards_btn_bybit_cta">طلب بطاقة Bybit المجانية</span>
            </a>
          </div>
        </div>

        <!-- Partner 2: RedotPay Virtual Visa -->
        <div class="border rounded-xl p-5 flex flex-col justify-between transition-colors hover:border-rose-500/50 space-y-4" style="background-color: var(--bg-card); border-color: var(--border-card);">
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <div class="w-9 h-9 rounded-lg bg-rose-500/10 text-rose-500 flex items-center justify-center text-base font-bold">
                <i class="fa-brands fa-cc-visa"></i>
              </div>
              <span class="text-[11px] font-bold px-2 py-0.5 rounded bg-rose-500/10 text-rose-600 dark:text-rose-400 border border-rose-500/20" data-i18n="cards_redot_badge">هدية 5$ ترحيبية</span>
            </div>
            <h3 class="font-bold text-sm sm:text-base" style="color: var(--text-main);" data-i18n="cards_redot_title">بطاقة فيزا RedotPay (هدية 5$)</h3>
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
            <div class="flex items-center justify-between p-2.5 rounded-lg border" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
              <div class="min-w-0">
                <div class="text-[10px] opacity-70" data-i18n="cards_ref_code">كود الهدية الترحيبية:</div>
                <div class="font-mono font-bold text-sm text-rose-500">djbt3</div>
              </div>
              <button onclick="copyReferralCode('djbt3', this)" class="min-h-[36px] px-2.5 py-1 text-xs font-bold rounded border hover:bg-rose-500/10 active:scale-95 transition flex items-center gap-1.5 touch-manipulation cursor-pointer" style="border-color: var(--border-card); color: var(--text-main);">
                <i class="fa-regular fa-copy"></i>
                <span data-i18n="cards_btn_copy_code">نسخ الكود</span>
              </button>
            </div>
            <a href="https://url.hk/i/en/djbt3" target="_blank" rel="noopener noreferrer" class="w-full min-h-[40px] rounded-lg bg-rose-600 hover:bg-rose-500 active:scale-[0.98] text-white font-bold text-xs sm:text-sm py-2 px-3 flex items-center justify-center gap-2 shadow-sm transition touch-manipulation">
              <i class="fa-solid fa-gift text-xs"></i>
              <span data-i18n="cards_btn_redot_cta">طلب بطاقة RedotPay (+ 5$ هدية)</span>
            </a>
          </div>
        </div>

        <!-- Partner 3: Binance P2P BaridiMob -->
        <div class="border rounded-xl p-5 flex flex-col justify-between transition-colors hover:border-amber-500/50 space-y-4" style="background-color: var(--bg-card); border-color: var(--border-card);">
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <div class="w-9 h-9 rounded-lg bg-amber-500/10 text-amber-500 flex items-center justify-center text-base font-bold">
                <i class="fa-solid fa-building-columns"></i>
              </div>
              <span class="text-[11px] font-bold px-2 py-0.5 rounded bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20" data-i18n="cards_binance_badge">سوق P2P #1 في الجزائر</span>
            </div>
            <h3 class="font-bold text-sm sm:text-base" style="color: var(--text-main);" data-i18n="cards_binance_title">منصة Binance P2P (BaridiMob)</h3>
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
            <div class="flex items-center justify-between p-2.5 rounded-lg border" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
              <div class="min-w-0">
                <div class="text-[10px] opacity-70" data-i18n="cards_ref_code">كود إحالة Binance الرسمي:</div>
                <div class="font-mono font-bold text-xs sm:text-sm text-amber-500 truncate">GRO_28502_3WGQR</div>
              </div>
              <button onclick="copyReferralCode('GRO_28502_3WGQR', this)" class="min-h-[36px] px-2.5 py-1 text-xs font-bold rounded border hover:bg-amber-500/10 active:scale-95 transition flex items-center gap-1.5 touch-manipulation flex-shrink-0 cursor-pointer" style="border-color: var(--border-card); color: var(--text-main);">
                <i class="fa-regular fa-copy"></i>
                <span data-i18n="cards_btn_copy_code">نسخ الكود</span>
              </button>
            </div>
            <a href="https://www.binance.com/referral/earn-together/refer2earn-usdc/claim?hl=en&ref=GRO_28502_3WGQR&utm_source=referral_entrance" target="_blank" rel="noopener noreferrer" class="w-full min-h-[40px] rounded-lg bg-amber-500 hover:bg-amber-400 active:scale-[0.98] text-zinc-950 font-bold text-xs sm:text-sm py-2 px-3 flex items-center justify-center gap-2 shadow-sm transition touch-manipulation">
              <i class="fa-solid fa-arrow-up-right-from-square text-xs"></i>
              <span data-i18n="cards_btn_binance_cta">فتح حساب Binance P2P</span>
            </a>
          </div>
        </div>

      </div>

      <!-- Step-by-Step BaridiMob Shopping Workflow Guide -->
      <div class="border rounded-xl p-5 sm:p-6 space-y-5" style="background-color: var(--bg-card); border-color: var(--border-card);">
        <div class="space-y-1">
          <h2 class="text-lg sm:text-xl font-bold" style="color: var(--text-main);" data-i18n="cards_guide_title">
            دليل الشراء خطوة بخطوة بالدينار الجزائري (BaridiMob) 🇩🇿
          </h2>
          <p class="text-xs sm:text-sm" style="color: var(--text-muted);" data-i18n="cards_guide_subtitle">
            الطريقة الرسمية والآمنة التي يستعملها آلاف المتسوقين الجزائريين يومياً للشراء من AliExpress بأقل تكلفة:
          </p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          
          <div class="border rounded-xl p-4 space-y-2 relative" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
            <div class="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-500 font-bold flex items-center justify-center text-sm">1</div>
            <h3 class="font-bold text-xs sm:text-sm" style="color: var(--text-main);" data-i18n="cards_step1_title">1. شراء USDT بـ BaridiMob</h3>
            <p class="text-xs leading-relaxed" style="color: var(--text-muted);" data-i18n="cards_step1_desc">
              افتح حسابك في Binance، ادخل قسم P2P واختر الدفع بـ BaridiMob لشراء المبلغ المطلوب من الدولار الرقمي (USDT) مباشرة في دقيقتين.
            </p>
          </div>

          <div class="border rounded-xl p-4 space-y-2 relative" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
            <div class="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-500 font-bold flex items-center justify-center text-sm">2</div>
            <h3 class="font-bold text-xs sm:text-sm" style="color: var(--text-main);" data-i18n="cards_step2_title">2. شحن بطاقتك الافتراضية</h3>
            <p class="text-xs leading-relaxed" style="color: var(--text-muted);" data-i18n="cards_step2_desc">
              حوّل رصيد USDT من Binance إلى حساب Bybit أو RedotPay الخاص بك عبر شبكة سريعة بدون أي رسوم مرتفعة.
            </p>
          </div>

          <div class="border rounded-xl p-4 space-y-2 relative" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
            <div class="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-500 font-bold flex items-center justify-center text-sm">3</div>
            <h3 class="font-bold text-xs sm:text-sm" style="color: var(--text-main);" data-i18n="cards_step3_title">3. ربط البطاقة في AliExpress</h3>
            <p class="text-xs leading-relaxed" style="color: var(--text-muted);" data-i18n="cards_step3_desc">
              انسخ معلومات بطاقتك الافتراضية (رقم البطاقة وتاريخ الانتهاء وCVV) وأضفها في وسائل الدفع بتطبيق AliExpress.
            </p>
          </div>

          <div class="border rounded-xl p-4 space-y-2 relative" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
            <div class="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-500 font-bold flex items-center justify-center text-sm">4</div>
            <h3 class="font-bold text-xs sm:text-sm" style="color: var(--text-main);" data-i18n="cards_step4_title">4. تطبيق الخصومات والشراء</h3>
            <p class="text-xs leading-relaxed" style="color: var(--text-muted);" data-i18n="cards_step4_desc">
              اختر صفقتك من موقعنا، انسخ كود الخصم، استخدم بوت العملات واستلم طردك مباشرة من مكتب بريد الجزائر القريب منك!
            </p>
          </div>

        </div>
      </div>

      <!-- In-Depth Algerian Shipping & Customs Guide Section -->
      <div class="border rounded-2xl p-6 sm:p-8 space-y-6" style="background-color: var(--bg-card); border-color: var(--border-card);">
        <div class="space-y-1 border-b pb-4" style="border-color: var(--border-card);">
          <div class="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-emerald-500/15 text-emerald-500">
            <i class="fa-solid fa-map-location-dot text-xs"></i>
            <span data-i18n="cards_post_badge">إرشادات الشحن والجمارك في الجزائر 2026</span>
          </div>
          <h2 class="text-base sm:text-lg font-bold" style="color: var(--text-main);" data-i18n="cards_post_title">
            ضبط العنوان الجزائري، قوانين الجمارك (Douane)، واستلام الطرد من البريد
          </h2>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs leading-relaxed" style="color: var(--text-muted);">
          <!-- Block A: Address & Postal Code -->
          <div class="border rounded-xl p-4 space-y-2" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
            <h3 class="font-bold text-sm flex items-center gap-2" style="color: var(--text-main);">
              <i class="fa-solid fa-envelopes-bulk text-sky-500"></i>
              <span data-i18n="cards_addr_h">1. ضبط الرمز البريدي والعنوان</span>
            </h3>
            <p data-i18n="cards_addr_p">
              اكتب اسمك المطابق لبطاقة الهوية ورقم هاتفك الفعال لتلقي SMS. تأكد من إدخال الرمز البريدي الدقيق المكون من 5 أرقام (أول رقمين هما رقم ولايتك، والـ 3 أرقام التالية هي مركز التوزيع البريدي لبلديتك).
            </p>
          </div>

          <!-- Block B: Algerian Customs Rules -->
          <div class="border rounded-xl p-4 space-y-2" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
            <h3 class="font-bold text-sm flex items-center gap-2" style="color: var(--text-main);">
              <i class="fa-solid fa-shield-halved text-amber-500"></i>
              <span data-i18n="cards_customs_h">2. الجمارك الجزائرية والطرود</span>
            </h3>
            <p data-i18n="cards_customs_p">
              الطرود الشخصية معفاة من الرسوم الجمركية. تجنب طلب كميات تجارية من نفس الصنف لتفادي الحجز. يُمنع منعاً باتاً استيراد طائرات الدرون، كاميرات المراقبة التجسسية المخفية، وأجهزة اللاسلكي غير المرخصة.
            </p>
          </div>

          <!-- Block C: Tracking & Delivery -->
          <div class="border rounded-xl p-4 space-y-2" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
            <h3 class="font-bold text-sm flex items-center gap-2" style="color: var(--text-main);">
              <i class="fa-solid fa-box-open text-emerald-500"></i>
              <span data-i18n="cards_pickup_h">3. التتبع والاستلام من البريد</span>
            </h3>
            <p data-i18n="cards_pickup_p">
              تتبع شحنتك عبر 17track وموقع بريد الجزائر بمجرد وصولها. عند وصول إشعار SMS أو Avis de passage، توجه إلى مكتب البريد مصحوباً ببطاقتك الوطنية، وادفع رسم التخليص البريدي الرمزي (~130 إلى 250 دج) واستلم طردك.
            </p>
          </div>
        </div>

        <!-- Cross-Link Actions from Cards Page -->
        <div class="pt-2 border-t flex flex-wrap items-center justify-between gap-3 text-xs" style="border-color: var(--border-card);">
          <div class="font-bold flex items-center gap-1.5" style="color: var(--text-main);">
            <i class="fa-solid fa-arrow-right-arrow-left text-emerald-500"></i>
            <span data-i18n="cards_crosslink_heading">انتقل إلى أقسام الموقع الأخرى:</span>
          </div>
          <div class="flex items-center gap-2">
            <a href="#deals" onclick="showPage('deals')" class="px-3 py-1.5 rounded-lg border font-bold hover:bg-crimson-500/10 transition active:scale-95" style="border-color: var(--border-card); color: var(--text-main);">
              <i class="fa-solid fa-fire text-crimson-500 mr-1"></i>
              <span data-i18n="nav_deals">الصفقات المباشرة</span>
            </a>
            <a href="#coins" onclick="showPage('coins')" class="px-3 py-1.5 rounded-lg border font-bold hover:bg-amber-500/10 transition active:scale-95" style="border-color: var(--border-card); color: var(--text-main);">
              <i class="fa-solid fa-coins text-amber-500 mr-1"></i>
              <span data-i18n="nav_coins">مولد العملات Coins</span>
            </a>
            <a href="#faq" onclick="showPage('faq')" class="px-3 py-1.5 rounded-lg border font-bold hover:bg-sky-500/10 transition active:scale-95" style="border-color: var(--border-card); color: var(--text-main);">
              <i class="fa-solid fa-circle-question text-sky-500 mr-1"></i>
              <span data-i18n="nav_faq">الأسئلة الشائعة</span>
            </a>
          </div>
        </div>
      </div>

      <!-- Cards & Payment Frequently Asked Questions (FAQ) for Instant Google Search Snippets -->
      <div class="border rounded-2xl p-6 sm:p-8 space-y-5" style="background-color: var(--bg-card); border-color: var(--border-card);">
        <div class="space-y-1">
          <div class="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-sky-500/15 text-sky-500">
            <i class="fa-solid fa-circle-question text-xs"></i>
            <span data-i18n="cards_faq_badge">أسئلة شائعة حول البطاقات والشحن</span>
          </div>
          <h2 class="text-base sm:text-lg font-bold" style="color: var(--text-main);" data-i18n="cards_faq_title">
            أهم الأسئلة الشائعة حول الدفع والشراء بالدينار الجزائري
          </h2>
        </div>

        <div class="space-y-3 text-xs sm:text-sm">
          <div class="border rounded-xl p-4 space-y-1.5" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
            <h3 class="font-bold flex items-center gap-2" style="color: var(--text-main);">
              <i class="fa-solid fa-chevron-left text-emerald-500 text-[10px]"></i>
              <span data-i18n="cards_faq_q1">هل بطاقة Bybit Card مجانية حقاً وبدون اشتراك شهري؟</span>
            </h3>
            <p class="text-xs leading-relaxed opacity-80" style="color: var(--text-muted);" data-i18n="cards_faq_a1">
              نعم، بطاقة Bybit ماستركارد الافتراضية مجانية 100% بدون أي مصاريف فتح وبدون اقتطاع شهري أو سنوي. تدعم الدفع المباشر على AliExpress وPayPal وتحصل معها على كاش باك يصل إلى 10%.
            </p>
          </div>

          <div class="border rounded-xl p-4 space-y-1.5" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
            <h3 class="font-bold flex items-center gap-2" style="color: var(--text-main);">
              <i class="fa-solid fa-chevron-left text-emerald-500 text-[10px]"></i>
              <span data-i18n="cards_faq_q2">كيف أشحن بطاقة RedotPay أو Bybit باستخدام بريدي موب (BaridiMob)؟</span>
            </h3>
            <p class="text-xs leading-relaxed opacity-80" style="color: var(--text-muted);" data-i18n="cards_faq_a2">
              تتم العملية عبر منصة Binance P2P: تشتري الدولار الرقمي (USDT) بالدينار الجزائري مباشرة من بائعين جزائريين موثوقين وتدفع عبر تطبيق BaridiMob، ثم تسحب الرصيد إلى بطاقة RedotPay أو Bybit في ثوانٍ عبر شبكة BSC أو TRC20.
            </p>
          </div>

          <div class="border rounded-xl p-4 space-y-1.5" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
            <h3 class="font-bold flex items-center gap-2" style="color: var(--text-main);">
              <i class="fa-solid fa-chevron-left text-emerald-500 text-[10px]"></i>
              <span data-i18n="cards_faq_q3">هل تقبل بطاقة RedotPay و Bybit التفعيل مع حساب PayPal الجزائري؟</span>
            </h3>
            <p class="text-xs leading-relaxed opacity-80" style="color: var(--text-muted);" data-i18n="cards_faq_a3">
              نعم، كلاً من بطاقة RedotPay وبطاقة Bybit تقبل الربط مع PayPal الجزائري أو الأجنبي، وتصل رسالة رمز التفعيل (4 أرقام) فورياً داخل تطبيق البطاقة.
            </p>
          </div>

          <div class="border rounded-xl p-4 space-y-1.5" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
            <h3 class="font-bold flex items-center gap-2" style="color: var(--text-main);">
              <i class="fa-solid fa-chevron-left text-emerald-500 text-[10px]"></i>
              <span data-i18n="cards_faq_q4">ما هو كود الحصول على هدية 5$ المجانية في RedotPay؟</span>
            </h3>
            <p class="text-xs leading-relaxed opacity-80" style="color: var(--text-muted);" data-i18n="cards_faq_a4">
              عند التسجيل في RedotPay، أدخل كود الإحالة الحصري djbt3 لتحصل فوراً على بونص 5$ رصيد ترحيبي في حسابك بمجرد إكمال تأكيد الهوية ببطاقة التعريف الوطنية.
            </p>
          </div>
        </div>
      </div>

    </div>

    <!-- ───────────────────────────────────────────────────────── -->
    <!-- PAGE 2: COINS BOT EXPLAINER PAGE                          -->
    <!-- ───────────────────────────────────────────────────────── -->
    <div id="page-coins" class="page-view hidden space-y-6">
      
      <div class="border rounded-xl p-5 sm:p-6 space-y-3" style="background-color: var(--bg-card); border-color: var(--border-card);">
        <div class="inline-flex items-center gap-2 px-2.5 py-1 rounded text-xs font-bold bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20">
          <i class="fa-solid fa-coins"></i>
          <span data-i18n="coins_badge">دليل توفير العملات (AliExpress Coins)</span>
        </div>
        <h1 class="text-lg sm:text-xl font-bold tracking-tight" style="color: var(--text-main);" data-i18n="coins_hero_title">
          كيف توفر حتى 60% إضافية باستخدام عملات AliExpress وبوت @Alilo07BOT؟
        </h1>
        <p class="text-xs sm:text-sm leading-relaxed max-w-3xl" style="color: var(--text-muted);" data-i18n="coins_hero_desc">
          تمنح AliExpress مستخدميها عملات يومية (Coins)، لكن معظم المنتجات في التطبيق لا تسمح باستخدام أكثر من 2% فقط. بوت التخفيضات الخاص بنا يقوم بفك القيود وتوليد روابط مباشرة تمكّنك من استهلاك أكبر عدد ممكن من العملات والحصول على خصم ضخم فوري!
        </p>
        <div class="pt-1 flex flex-wrap gap-3">
          <a href="https://t.me/Alilo07BOT" target="_blank" rel="noopener noreferrer" class="min-h-[40px] px-4 py-2 rounded-lg bg-amber-500 hover:bg-amber-400 text-zinc-950 font-bold text-xs sm:text-sm flex items-center gap-2 shadow-sm active:scale-95 transition cursor-pointer">
            <i class="fa-solid fa-coins"></i>
            <span data-i18n="coins_btn_start">تشغيل البوت مجاناً (@Alilo07BOT)</span>
          </a>
        </div>
      </div>

      <!-- Interactive Coins Deal Link Generator Card -->
      <section id="coins-generator-card" class="border rounded-2xl p-4 sm:p-6 space-y-4 shadow-sm" style="background-color: var(--bg-card); border-color: var(--border-card);" aria-label="مولد روابط خصم العملات">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b pb-3" style="border-color: var(--border-card);">
          <div class="space-y-1">
            <div class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[11px] font-bold bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20">
              <i class="fa-solid fa-wand-magic-sparkles text-xs"></i>
              <span data-i18n="coin_gen_badge">أداة مجانية فورية</span>
            </div>
            <h2 class="text-base sm:text-lg font-bold flex items-center gap-2" style="color: var(--text-main);" data-i18n="coin_gen_title">
              <i class="fa-solid fa-coins text-amber-500"></i>
              <span data-i18n="coin_gen_title">مولد روابط خصم العملات (Coins Deal Generator)</span>
            </h2>
            <p class="text-xs leading-relaxed" style="color: var(--text-muted);" data-i18n="coin_gen_subtitle">
              الصق رابط أي منتج من AliExpress أو نص المشاركة لتحصل فوراً على رابط تفعيل أقصى خصم للعملات (حتى 60%) وعروض السوبر ديلز!
            </p>
          </div>
          <span class="text-[11px] text-amber-500 font-mono font-semibold flex items-center gap-1 self-start sm:self-center">
            <i class="fa-solid fa-bolt text-xs"></i>
            <span>توليد فوري 100%</span>
          </span>
        </div>

        <!-- Input & Action Bar -->
        <div class="space-y-2.5">
          <label for="coins-input-url" class="block text-xs font-semibold" style="color: var(--text-main);" data-i18n="coin_gen_input_label">
            رابط المنتج، كود المنتج (Item ID)، أو نص المشاركة من التطبيق:
          </label>
          <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-2">
            <div class="relative flex-1">
              <i class="fa-solid fa-link absolute right-3.5 top-1/2 -translate-y-1/2 text-xs opacity-40 pointer-events-none"></i>
              <input 
                type="text" 
                id="coins-input-url" 
                placeholder="https://www.aliexpress.com/item/100500... أو https://a.aliexpress.com/_m..." 
                class="w-full border rounded-xl pr-9 pl-20 py-2.5 text-xs sm:text-sm focus:outline-none focus:border-amber-500 transition min-h-[44px]"
                style="background-color: var(--input-bg); border-color: var(--border-card); color: var(--text-main);"
                onkeydown="if(event.key==='Enter') generateCoinLink()"
              />
              <button 
                type="button" 
                onclick="pasteToCoinsInput()" 
                id="coins-paste-btn"
                title="لصق من الحافظة"
                class="absolute left-2 top-1/2 -translate-y-1/2 px-2.5 py-1 rounded-lg border text-[11px] font-semibold flex items-center gap-1 transition active:scale-95 touch-manipulation cursor-pointer"
                style="background-color: var(--bg-card); border-color: var(--border-card); color: var(--text-muted);"
              >
                <i class="fa-regular fa-paste text-[10px]"></i>
                <span data-i18n="btn_paste">لصق</span>
              </button>
            </div>
            <button 
              type="button" 
              onclick="generateCoinLink()" 
              id="coins-submit-btn"
              class="min-h-[44px] px-5 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-zinc-950 font-bold text-xs sm:text-sm flex items-center justify-center gap-2 shadow-sm active:scale-95 transition cursor-pointer flex-shrink-0"
            >
              <i class="fa-solid fa-coins text-sm"></i>
              <span data-i18n="btn_generate_coin_deal">توليد رابط العملات</span>
            </button>
          </div>
          <div id="coins-gen-error" class="hidden text-xs text-rose-500 flex items-center gap-1.5 pt-1">
            <i class="fa-solid fa-circle-exclamation text-xs"></i>
            <span id="coins-gen-error-text">يرجى إدخال رابط منتج صالح من AliExpress أو رقم المنتج.</span>
          </div>
        </div>

        <!-- Generated Result Card (Reveals upon generation) -->
        <div id="coins-gen-result" class="hidden border rounded-xl p-4 sm:p-5 space-y-4 animate-slide-up" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
          <div class="flex flex-wrap items-center justify-between gap-2 border-b pb-3" style="border-color: var(--border-card);">
            <div class="flex items-center gap-2">
              <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
              <span class="font-bold text-xs sm:text-sm text-emerald-500" data-i18n="coin_gen_success">تم تجهيز روابط الخصم بنجاح!</span>
            </div>
            <span id="coins-gen-pid-badge" class="font-mono text-xs px-2.5 py-0.5 rounded-lg border" style="background-color: var(--bg-card); border-color: var(--border-card); color: var(--text-muted);">ID: 100500...</span>
          </div>

          <!-- Highlighted Coin Deal Link -->
          <div class="border rounded-xl p-3.5 space-y-2 border-amber-500/40" style="background-color: var(--bg-card);">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-amber-500 flex items-center gap-1.5">
                <i class="fa-solid fa-coins"></i>
                <span data-i18n="coin_link_primary_title">رابط العملات المخفض (Coins Deal - حتى 60% خصم)</span>
              </span>
              <span class="text-[10px] bg-amber-500/10 text-amber-500 px-2 py-0.5 rounded-md font-bold">أعلى توفير</span>
            </div>
            <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-2">
              <input 
                type="text" 
                id="coins-gen-out-coin" 
                readonly 
                class="flex-1 font-mono text-[11px] px-3 py-2 rounded-lg border focus:outline-none select-all"
                style="background-color: var(--input-bg); border-color: var(--border-card); color: var(--text-main);"
              />
              <div class="flex items-center gap-1.5">
                <button 
                  onclick="copyCoinLink('coins-gen-out-coin', this)" 
                  class="flex-1 sm:flex-none min-h-[38px] px-3 py-1.5 rounded-lg border text-xs font-bold flex items-center justify-center gap-1.5 active:scale-95 transition touch-manipulation cursor-pointer"
                  style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-main);"
                >
                  <i class="fa-regular fa-copy"></i>
                  <span data-i18n="btn_copy_link">نسخ الرابط</span>
                </button>
                <a 
                  id="coins-gen-btn-buy" 
                  href="#" 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  class="flex-1 sm:flex-none min-h-[38px] px-4 py-1.5 rounded-lg bg-amber-500 hover:bg-amber-400 text-zinc-950 text-xs font-bold flex items-center justify-center gap-1.5 active:scale-95 transition shadow-sm"
                >
                  <i class="fa-solid fa-cart-shopping"></i>
                  <span data-i18n="btn_buy_coins_deal">فتح وشراء بالعملات</span>
                </a>
              </div>
            </div>
          </div>

          <!-- Other Deal Formats (SuperDeals & Bundle Deals) -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 text-xs">
            <!-- SuperDeals -->
            <div class="border rounded-xl p-3 space-y-1.5" style="background-color: var(--bg-card); border-color: var(--border-card);">
              <div class="flex items-center justify-between text-rose-500 font-bold text-[11px]">
                <span class="flex items-center gap-1"><i class="fa-solid fa-bolt"></i> <span data-i18n="superdeal_link_title">رابط السوبر ديلز (SuperDeals)</span></span>
              </div>
              <div class="flex items-center gap-1.5">
                <button onclick="copyCoinLink('coins-gen-out-super', this)" class="px-2.5 py-1 rounded-lg border text-[11px] font-semibold active:scale-95 transition" style="border-color: var(--border-card); background-color: var(--bg-elevated); color: var(--text-main);">
                  <i class="fa-regular fa-copy text-[10px]"></i> <span data-i18n="btn_copy_link">نسخ الرابط</span>
                </button>
                <a id="coins-gen-btn-super" href="#" target="_blank" rel="noopener noreferrer" class="flex-1 text-center py-1 rounded-lg border text-[11px] font-bold text-rose-500 hover:bg-rose-500 hover:text-white transition" style="border-color: var(--border-card);">
                  <span data-i18n="btn_open_deal">فتح العرض</span> &larr;
                </a>
              </div>
              <input type="hidden" id="coins-gen-out-super" />
            </div>

            <!-- Bundle Deals -->
            <div class="border rounded-xl p-3 space-y-1.5" style="background-color: var(--bg-card); border-color: var(--border-card);">
              <div class="flex items-center justify-between text-emerald-500 font-bold text-[11px]">
                <span class="flex items-center gap-1"><i class="fa-solid fa-box-open"></i> <span data-i18n="bundle_link_title">عروض الحزم (Bundle Deals)</span></span>
              </div>
              <div class="flex items-center gap-1.5">
                <button onclick="copyCoinLink('coins-gen-out-bundle', this)" class="px-2.5 py-1 rounded-lg border text-[11px] font-semibold active:scale-95 transition" style="border-color: var(--border-card); background-color: var(--bg-elevated); color: var(--text-main);">
                  <i class="fa-regular fa-copy text-[10px]"></i> <span data-i18n="btn_copy_link">نسخ الرابط</span>
                </button>
                <a id="coins-gen-btn-bundle" href="#" target="_blank" rel="noopener noreferrer" class="flex-1 text-center py-1 rounded-lg border text-[11px] font-bold text-emerald-500 hover:bg-emerald-500 hover:text-white transition" style="border-color: var(--border-card);">
                  <span data-i18n="btn_open_deal">فتح العرض</span> &larr;
                </a>
              </div>
              <input type="hidden" id="coins-gen-out-bundle" />
            </div>
          </div>

          <!-- Pro Tip Box -->
          <div class="p-3 rounded-xl border border-dashed flex items-start gap-2.5 text-xs" style="background-color: var(--bg-card); border-color: var(--border-card); color: var(--text-muted);">
            <i class="fa-solid fa-lightbulb text-amber-500 text-sm mt-0.5 flex-shrink-0"></i>
            <p class="leading-relaxed text-[11px]" data-i18n="coin_gen_tip">
              💡 سر الخصم: افتح رابط العملات داخل تطبيق AliExpress واضغط مباشرة على زر (شراء الآن / Acheter) أو أضف المنتج إلى السلة من نفس الصفحة لتفعيل خصم العملات الكامل بدلاً من 2% فقط!
            </p>
          </div>
        </div>
      </section>

      <!-- 3 Steps Section with Semantic H2 -->
      <div class="space-y-4">
        <div class="space-y-1">
          <h2 class="text-base sm:text-lg font-bold" style="color: var(--text-main);" data-i18n="coins_steps_section_title">
            طريقة تفعيل أقصى خصم للعملات خطوة بخطوة 🪙
          </h2>
          <p class="text-xs" style="color: var(--text-muted);" data-i18n="coins_steps_section_sub">
            اتبع هذه الخطوات البسيطة لتحويل أي رابط منتج عادي إلى رابط تخفيض العملات الأقصى:
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="border rounded-xl p-4 sm:p-5 space-y-2.5" style="background-color: var(--bg-card); border-color: var(--border-card);">
            <div class="w-8 h-8 rounded-lg text-amber-500 font-bold text-sm flex items-center justify-center font-mono" style="background-color: var(--bg-elevated);">1</div>
            <h3 class="font-bold text-xs sm:text-sm" style="color: var(--text-main);" data-i18n="coins_step1_title">انسخ رابط المنتج من AliExpress</h3>
            <p class="text-xs leading-relaxed" style="color: var(--text-muted);" data-i18n="coins_step1_desc">افتح أي منتج يعجبك داخل تطبيق AliExpress، اضغط على زر المشاركة ثم اختر نسخ الرابط (Copy Link).</p>
          </div>

          <div class="border rounded-xl p-4 sm:p-5 space-y-2.5" style="background-color: var(--bg-card); border-color: var(--border-card);">
            <div class="w-8 h-8 rounded-lg text-sky-500 font-bold text-sm flex items-center justify-center font-mono" style="background-color: var(--bg-elevated);">2</div>
            <h3 class="font-bold text-xs sm:text-sm" style="color: var(--text-main);" data-i18n="coins_step2_title">أرسل الرابط لبوت التخفيض</h3>
            <p class="text-xs leading-relaxed" style="color: var(--text-muted);" data-i18n="coins_step2_desc">افتح بوت التيليجرام <b class="text-sky-500 font-mono">@Alilo07BOT</b> والصق الرابط في المحادثة. سيقوم البوت فوراً بالبحث عن أقصى نسبة خصم متاحة للعملات.</p>
          </div>

          <div class="border rounded-xl p-4 sm:p-5 space-y-2.5" style="background-color: var(--bg-card); border-color: var(--border-card);">
            <div class="w-8 h-8 rounded-lg text-emerald-500 font-bold text-sm flex items-center justify-center font-mono" style="background-color: var(--bg-elevated);">3</div>
            <h3 class="font-bold text-xs sm:text-sm" style="color: var(--text-main);" data-i18n="coins_step3_title">ادفع بالسعر المخفض</h3>
            <p class="text-xs leading-relaxed" style="color: var(--text-muted);" data-i18n="coins_step3_desc">اضغط على زر (شراء الآن) من الرابط الذي يرجعه البوت، وستلاحظ أن خانة العملات قد خصمت ما يصل إلى 10$ إلى 40$ من السعر الإجمالي!</p>
          </div>
        </div>
      </div>

      <!-- Cross-Links from Coins Page -->
      <div class="border rounded-xl p-4 flex flex-wrap items-center justify-between gap-3 text-xs" style="background-color: var(--bg-card); border-color: var(--border-card);">
        <div class="font-bold flex items-center gap-1.5" style="color: var(--text-main);">
          <i class="fa-solid fa-compass text-amber-500"></i>
          <span data-i18n="coins_crosslink_heading">تصفح أيضاً عبر DealScout DZ:</span>
        </div>
        <div class="flex items-center gap-2">
          <a href="#deals" onclick="showPage('deals')" class="px-3 py-1.5 rounded-lg border font-bold hover:bg-crimson-500/10 transition active:scale-95" style="border-color: var(--border-card); color: var(--text-main);">
            <i class="fa-solid fa-fire text-crimson-500 mr-1"></i>
            <span data-i18n="nav_deals">الصفقات المباشرة</span>
          </a>
          <a href="#cards" onclick="showPage('cards')" class="px-3 py-1.5 rounded-lg border font-bold hover:bg-emerald-500/10 transition active:scale-95" style="border-color: var(--border-card); color: var(--text-main);">
            <i class="fa-solid fa-credit-card text-emerald-500 mr-1"></i>
            <span data-i18n="nav_cards">دليل البطاقات وبريدي موب</span>
          </a>
          <a href="#faq" onclick="showPage('faq')" class="px-3 py-1.5 rounded-lg border font-bold hover:bg-sky-500/10 transition active:scale-95" style="border-color: var(--border-card); color: var(--text-main);">
            <i class="fa-solid fa-circle-question text-sky-500 mr-1"></i>
            <span data-i18n="nav_faq">الأسئلة الشائعة</span>
          </a>
        </div>
      </div>

    </div>

    <!-- ───────────────────────────────────────────────────────── -->
    <!-- PAGE 3: FAQ PAGE                                          -->
    <!-- ───────────────────────────────────────────────────────── -->
    <div id="page-faq" class="page-view hidden space-y-6">
      
      <div class="text-center max-w-2xl mx-auto space-y-2">
        <h1 class="text-xl sm:text-2xl font-bold" style="color: var(--text-main);" data-i18n="faq_title">الأسئلة الشائعة وإرشادات الشراء</h1>
        <p class="text-xs sm:text-sm" style="color: var(--text-muted);" data-i18n="faq_subtitle">كل ما يحتاجه المتسوق الجزائري لمعرفة طرق الشحن، حساب الأسعار بالدينار، والتعامل مع عروض AliExpress.</p>
      </div>

      <div class="space-y-3 max-w-3xl mx-auto">
        <!-- Q1 -->
        <details class="faq-item group border rounded-2xl p-4 transition-colors" style="background-color: var(--bg-card); border-color: var(--border-card);">
          <summary class="flex items-center justify-between cursor-pointer list-none font-bold text-xs sm:text-sm select-none" style="color: var(--text-main);">
            <h3 class="flex items-center gap-2 m-0 p-0 text-xs sm:text-sm font-bold">
              <i class="fa-solid fa-coins text-amber-500"></i>
              <span data-i18n="faq_q1">كيف يتم احتساب الأسعار بالدينار الجزائري (DZD)؟</span>
            </h3>
            <i class="fa-solid fa-chevron-down text-xs transition-transform duration-200 faq-icon opacity-50"></i>
          </summary>
          <div class="pt-3 text-xs leading-relaxed border-t mt-3" style="border-color: var(--border-card); color: var(--text-muted);" data-i18n="faq_a1">
            يتم حساب السعر بالدينار الجزائري تلقائياً وبدقة عالية اعتماداً على سعر صرف الدولار واليورو في السوق الموازي (سعر السكوار الحقيقي) المستخرج مباشرة من موقع SquareAlgerie.com، حتى تتطابق المبالغ مع ما تدفعه حقيقة عند شحن بطاقاتك (Visa / Mastercard / Bybit / RedotPay).
          </div>
        </details>

        <!-- Q2 -->
        <details class="faq-item group border rounded-2xl p-4 transition-colors" style="background-color: var(--bg-card); border-color: var(--border-card);">
          <summary class="flex items-center justify-between cursor-pointer list-none font-bold text-xs sm:text-sm select-none" style="color: var(--text-main);">
            <h3 class="flex items-center gap-2 m-0 p-0 text-xs sm:text-sm font-bold">
              <i class="fa-solid fa-truck-fast text-sky-500"></i>
              <span data-i18n="faq_q2">كيف يتم شحن الطرود واستلامها في الجزائر؟</span>
            </h3>
            <i class="fa-solid fa-chevron-down text-xs transition-transform duration-200 faq-icon opacity-50"></i>
          </summary>
          <div class="pt-3 text-xs leading-relaxed border-t mt-3" style="border-color: var(--border-card); color: var(--text-muted);" data-i18n="faq_a2">
            تشحن معظم المنتجات عبر بريد الجزائر (Algérie Poste / EMS). يصل الطرد إلى أقرب مكتب بريد لعنوان سكناك ويتم إرسال إشعار وصول إلى هاتفك أو صندوق بريدك. للشحنات العادية، تتراوح مدة الوصول بين 15 و35 يوماً عبر خيار AliExpress Standard Shipping.
          </div>
        </details>

        <!-- Q3 -->
        <details class="faq-item group border rounded-2xl p-4 transition-colors" style="background-color: var(--bg-card); border-color: var(--border-card);">
          <summary class="flex items-center justify-between cursor-pointer list-none font-bold text-xs sm:text-sm select-none" style="color: var(--text-main);">
            <h3 class="flex items-center gap-2 m-0 p-0 text-xs sm:text-sm font-bold">
              <i class="fa-solid fa-credit-card text-emerald-500"></i>
              <span data-i18n="faq_q3">ما هي أفضل طرق وبطاقات الدفع المتاحة للجزائريين؟</span>
            </h3>
            <i class="fa-solid fa-chevron-down text-xs transition-transform duration-200 faq-icon opacity-50"></i>
          </summary>
          <div class="pt-3 text-xs leading-relaxed border-t mt-3" style="border-color: var(--border-card); color: var(--text-muted);" data-i18n="faq_a3">
            يمكنك الدفع بسهولة عبر بطاقات فيزا وماستركارد الافتراضية الدولية مثل RedotPay، Bybit Card، Paysera، Pyypl، أو بطاقات العملة الصعبة الصادرة من البنوك الوطنية الجزائرية (AGB، BDL، بنك الخليج الجزائر).
          </div>
        </details>

        <!-- Q4 -->
        <details class="faq-item group border rounded-2xl p-4 transition-colors" style="background-color: var(--bg-card); border-color: var(--border-card);">
          <summary class="flex items-center justify-between cursor-pointer list-none font-bold text-xs sm:text-sm select-none" style="color: var(--text-main);">
            <h3 class="flex items-center gap-2 m-0 p-0 text-xs sm:text-sm font-bold">
              <i class="fa-solid fa-ticket text-rose-500"></i>
              <span data-i18n="faq_q4">لماذا يظهر كود الخصم غير صالح أو منتهي الصلاحية أحياناً؟</span>
            </h3>
            <i class="fa-solid fa-chevron-down text-xs transition-transform duration-200 faq-icon opacity-50"></i>
          </summary>
          <div class="pt-3 text-xs leading-relaxed border-t mt-3" style="border-color: var(--border-card); color: var(--text-muted);" data-i18n="faq_a4">
            أكواد الخصم الترويجية في AliExpress تكون محدودة بعدد استخدامات معين لكل دولة. نقوم بتحديث الأكواد لحظياً وإلغاء المنتهية فوراً، ولكن ننصح دائماً بالشراء السريع عند نشر الكود قبل نفاد حصة الجزائر.
          </div>
        </details>

        <!-- Q5 -->
        <details class="faq-item group border rounded-2xl p-4 transition-colors" style="background-color: var(--bg-card); border-color: var(--border-card);">
          <summary class="flex items-center justify-between cursor-pointer list-none font-bold text-xs sm:text-sm select-none" style="color: var(--text-main);">
            <h3 class="flex items-center gap-2 m-0 p-0 text-xs sm:text-sm font-bold">
              <i class="fa-solid fa-earth-europe text-blue-500"></i>
              <span data-i18n="faq_q5">ما هي قناة عروض فرنسا (@francedealsdz)؟</span>
            </h3>
            <i class="fa-solid fa-chevron-down text-xs transition-transform duration-200 faq-icon opacity-50"></i>
          </summary>
          <div class="pt-3 text-xs leading-relaxed border-t mt-3" style="border-color: var(--border-card); color: var(--text-muted);" data-i18n="faq_a5">
            هي قناة متخصصة وموجهة لأفراد الجالية الجزائرية المقيمين في فرنسا وأوروبا، أو للجزائريين الذين يستعينون بشركات إعادة توجيه الطرود (Forwarders). أسعارها باليورو الأوروبي وعروضها مشحونة من مستودعات أوروبية سريعة (خلال 3-7 أيام).
          </div>
        </details>

        <!-- Q6: BaridiMob & Binance P2P -->
        <details class="faq-item group border rounded-2xl p-4 transition-colors" style="background-color: var(--bg-card); border-color: var(--border-card);">
          <summary class="flex items-center justify-between cursor-pointer list-none font-bold text-xs sm:text-sm select-none" style="color: var(--text-main);">
            <h3 class="flex items-center gap-2 m-0 p-0 text-xs sm:text-sm font-bold">
              <i class="fa-solid fa-building-columns text-emerald-500"></i>
              <span data-i18n="faq_q6">كيف أشتري من AliExpress باستخدام تطبيق بريدي موب (BaridiMob)؟</span>
            </h3>
            <i class="fa-solid fa-chevron-down text-xs transition-transform duration-200 faq-icon opacity-50"></i>
          </summary>
          <div class="pt-3 text-xs leading-relaxed border-t mt-3" style="border-color: var(--border-card); color: var(--text-muted);" data-i18n="faq_a6">
            لا يقبل AliExpress الدفع المباشر بالدينار أو البطاقة الذهبية. الطريقة المعتمدة هي فتح حساب في Binance واستخدام قسم التداول P2P لشراء رصيد USDT بالدينار الجزائري عبر بريدي موب من بائع معتمد، ثم تحويل الرصيد إلى بطاقة Bybit ماستركارد المجانية أو بطاقة RedotPay واستعمالها في الدفع فوراً.
          </div>
        </details>

        <!-- Q7: Customs & Douane Regulations -->
        <details class="faq-item group border rounded-2xl p-4 transition-colors" style="background-color: var(--bg-card); border-color: var(--border-card);">
          <summary class="flex items-center justify-between cursor-pointer list-none font-bold text-xs sm:text-sm select-none" style="color: var(--text-main);">
            <h3 class="flex items-center gap-2 m-0 p-0 text-xs sm:text-sm font-bold">
              <i class="fa-solid fa-shield-halved text-amber-500"></i>
              <span data-i18n="faq_q7">ما هي قوانين الجمارك الجزائرية للطرود؟ وما هي المنتجات الممنوعة؟</span>
            </h3>
            <i class="fa-solid fa-chevron-down text-xs transition-transform duration-200 faq-icon opacity-50"></i>
          </summary>
          <div class="pt-3 text-xs leading-relaxed border-t mt-3" style="border-color: var(--border-card); color: var(--text-muted);" data-i18n="faq_a7">
            الطرود الموجهة للاستعمال الشخصي والعائلي معفاة تماماً من الرسوم الجمركية في الجزائر. لتفادي المشاكل، لا تطلب كميات تجارية متكررة من نفس السلعة في شحنة واحدة. يُمنع منعاً باتاً استيراد: طائرات الدرون بجميع أنواعها، كاميرات التجسس المخفية، أجهزة اللاسلكي غير المرخصة، ومؤشرات الليزر المحظورة.
          </div>
        </details>

        <!-- Q8: Coins Discount Trick -->
        <details class="faq-item group border rounded-2xl p-4 transition-colors" style="background-color: var(--bg-card); border-color: var(--border-card);">
          <summary class="flex items-center justify-between cursor-pointer list-none font-bold text-xs sm:text-sm select-none" style="color: var(--text-main);">
            <h3 class="flex items-center gap-2 m-0 p-0 text-xs sm:text-sm font-bold">
              <i class="fa-solid fa-wand-magic-sparkles text-rose-500"></i>
              <span data-i18n="faq_q8">كيف أحصل على أقصى تخفيض للعملات Coins (حتى 70%)؟</span>
            </h3>
            <i class="fa-solid fa-chevron-down text-xs transition-transform duration-200 faq-icon opacity-50"></i>
          </summary>
          <div class="pt-3 text-xs leading-relaxed border-t mt-3" style="border-color: var(--border-card); color: var(--text-muted);" data-i18n="faq_a8">
            عند التسوق العادي يخصم AliExpress نسبة 1% إلى 5% فقط من العملات. باستخدام أداة مولد روابط العملات على موقعنا أو بوت @Alilo07BOT، يتم توليد رابط مخصص مع وسم المصدر sourceType=620، مما يرفع نسبة قبول العملات على نفس السلعة حتى 50% أو 70% عند الشراء مباشرة من قسم العملات.
          </div>
        </details>

        <!-- Q9: Postal Address Formatting -->
        <details class="faq-item group border rounded-2xl p-4 transition-colors" style="background-color: var(--bg-card); border-color: var(--border-card);">
          <summary class="flex items-center justify-between cursor-pointer list-none font-bold text-xs sm:text-sm select-none" style="color: var(--text-main);">
            <h3 class="flex items-center gap-2 m-0 p-0 text-xs sm:text-sm font-bold">
              <i class="fa-solid fa-location-dot text-indigo-500"></i>
              <span data-i18n="faq_q9">كيف أكتب العنوان الجزائري والرمز البريدي (Code Postal) بشكل صحيح؟</span>
            </h3>
            <i class="fa-solid fa-chevron-down text-xs transition-transform duration-200 faq-icon opacity-50"></i>
          </summary>
          <div class="pt-3 text-xs leading-relaxed border-t mt-3" style="border-color: var(--border-card); color: var(--text-muted);" data-i18n="faq_a9">
            اكتب اسمك الكامل مطابقاً لبطاقة التعريف الوطنية، ورقم هاتفك المحمول الصحيح لتلقي SMS من بريد الجزائر. الرمز البريدي يتكون من 5 أرقام (أول رقمين هما رقم ولايتك، مثلاً 16 للجزائر أو 31 لوهران)، والأرقام الثلاثة المتبقية تدل على مركز التوزيع لبلديتك. احرص على وضع كود مركز البريد الأقرب إليك لضمان عدم تأخر الطرد.
          </div>
        </details>

        <!-- Cross-Links from FAQ Page -->
        <div class="border rounded-2xl p-4 mt-6 flex flex-wrap items-center justify-between gap-3 text-xs" style="background-color: var(--bg-card); border-color: var(--border-card);">
          <div class="font-bold flex items-center gap-1.5" style="color: var(--text-main);">
            <i class="fa-solid fa-link text-sky-500"></i>
            <span data-i18n="faq_crosslink_heading">مواضيع ذات صلة تهمك:</span>
          </div>
          <div class="flex items-center gap-2">
            <a href="#deals" onclick="showPage('deals')" class="px-3 py-1.5 rounded-lg border font-bold hover:bg-crimson-500/10 transition active:scale-95" style="border-color: var(--border-card); color: var(--text-main);">
              <i class="fa-solid fa-fire text-crimson-500 mr-1"></i>
              <span data-i18n="nav_deals">الصفقات</span>
            </a>
            <a href="#cards" onclick="showPage('cards')" class="px-3 py-1.5 rounded-lg border font-bold hover:bg-emerald-500/10 transition active:scale-95" style="border-color: var(--border-card); color: var(--text-main);">
              <i class="fa-solid fa-credit-card text-emerald-500 mr-1"></i>
              <span data-i18n="nav_cards">دليل البطاقات</span>
            </a>
            <a href="#coins" onclick="showPage('coins')" class="px-3 py-1.5 rounded-lg border font-bold hover:bg-amber-500/10 transition active:scale-95" style="border-color: var(--border-card); color: var(--text-main);">
              <i class="fa-solid fa-coins text-amber-500 mr-1"></i>
              <span data-i18n="nav_coins">بوت العملات</span>
            </a>
          </div>
        </div>
      </div>

    </div>

    <!-- ───────────────────────────────────────────────────────── -->
    <!-- PAGE 4: CONTACT & SUPPORT PAGE                            -->
    <!-- ───────────────────────────────────────────────────────── -->
    <div id="page-contact" class="page-view hidden space-y-6">
      
      <div class="text-center max-w-2xl mx-auto space-y-2">
        <h1 class="text-xl sm:text-2xl font-bold" style="color: var(--text-main);" data-i18n="contact_title">اتصل بنا والدعم الفني</h1>
        <p class="text-xs sm:text-sm" style="color: var(--text-muted);" data-i18n="contact_subtitle">فريق DealScout DZ يرحب باقتراحاتكم، إبلاغكم عن الروابط التالفة، واستفساراتكم حول الصفقات.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto">
        <!-- Direct Telegram Support Card -->
        <div class="border rounded-2xl p-6 space-y-4 flex flex-col justify-between" style="background-color: var(--bg-card); border-color: var(--border-card);">
          <div class="space-y-3">
            <div class="w-12 h-12 rounded-2xl bg-sky-500/15 text-sky-500 flex items-center justify-center text-xl">
              <i class="fa-brands fa-telegram"></i>
            </div>
            <h2 class="font-bold text-base" style="color: var(--text-main);" data-i18n="contact_tg_title">مجموعة المحادثة والنقاش عبر Telegram</h2>
            <p class="text-xs leading-relaxed" style="color: var(--text-muted);" data-i18n="contact_tg_desc">
              تواصل مباشرة مع فريق العمل ومجتمع المتسوقين عبر مجموعة المناقشات والاستفسارات الملحقة بقناة صفقات الجزائر. اطرح سؤالك، شارك تجارب الشراء، أو اطلب التحقق من أي صفقة.
            </p>
          </div>

          <div class="space-y-2.5 pt-2">
            <a href="https://t.me/DzAliexpress0" target="_blank" rel="noopener noreferrer" class="w-full min-h-[44px] bg-[#229ED9] hover:bg-[#1c8cc1] text-white font-bold text-xs py-2.5 px-4 rounded-xl flex items-center justify-center gap-2 active:scale-95 transition">
              <i class="fa-solid fa-comments text-xs"></i>
              <span data-i18n="contact_tg_btn_admin">مجموعة المناقشات والاستفسارات (@DzAliexpress0)</span>
            </a>
            <a href="https://t.me/Alilo07BOT" target="_blank" rel="noopener noreferrer" class="w-full min-h-[44px] border font-bold text-xs py-2.5 px-4 rounded-xl flex items-center justify-center gap-2 active:scale-95 transition text-amber-500" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
              <i class="fa-solid fa-coins text-xs"></i>
              <span data-i18n="contact_tg_btn_bot">الدخول لبوت العملات (@Alilo07BOT)</span>
            </a>
          </div>
        </div>

        <!-- Contact Form -->
        <div class="border rounded-2xl p-6 space-y-4" style="background-color: var(--bg-card); border-color: var(--border-card);">
          <h2 class="font-bold text-base" style="color: var(--text-main);" data-i18n="contact_form_title">إرسال رسالة أو اقتراح</h2>
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
          <h1 class="text-xl sm:text-2xl font-bold tracking-tight" style="color: var(--text-main);" data-i18n="about_title">حول منصة DealScout DZ</h1>
          <p class="leading-relaxed" data-i18n="about_p1">
            تأسست منصة <b>DealScout DZ</b> بهدف حل أكبر مشكلة تواجه المتسوقين في الجزائر عبر الإنترنت: صعوبة الوصول إلى التخفيضات الحقيقية، والارتباك الناتج عن حساب تكلفة المنتج بالدينار الجزائري في ظل تغير أسعار سوق السكوار.
          </p>
          <p class="leading-relaxed" data-i18n="about_p2">
            نقوم بمسح آلاف الصفقات المنشورة في مجموعات AliExpress المعتمدة، ثم نطبق خوارزميات ذكية لتصفية العروض الوهمية، وإبراز المنتجات الأكثر طلباً في السوق الجزائري (الهواتف الذكية، ملحقات الحواسيب، أجهزة القيمنق، الشواحن الأصلية، والأدوات المنزلية الذكية).
          </p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div class="border rounded-2xl p-5 space-y-2" style="background-color: var(--bg-card); border-color: var(--border-card);">
            <h2 class="font-bold text-sm flex items-center gap-2" style="color: var(--text-main);">
              <i class="fa-solid fa-chart-line text-emerald-500"></i>
              <span data-i18n="about_feat1_title">ربط مباشر مع سعر السكوار</span>
            </h2>
            <p class="text-xs leading-relaxed" style="color: var(--text-muted);" data-i18n="about_feat1_desc">نحدث أسعار USDT بالدينار الجزائري لحظة بلحظة لضمان شفافية كاملة قبل الضغط على زر الشراء.</p>
          </div>

          <div class="border rounded-2xl p-5 space-y-2" style="background-color: var(--bg-card); border-color: var(--border-card);">
            <h2 class="font-bold text-sm flex items-center gap-2" style="color: var(--text-main);">
              <i class="fa-solid fa-robot text-sky-500"></i>
              <span data-i18n="about_feat2_title">روبوتات آلية وخوارزميات أمان</span>
            </h2>
            <p class="text-xs leading-relaxed" style="color: var(--text-muted);" data-i18n="about_feat2_desc">نظام ذكي يلتقط التخفيضات في الثواني الأولى لنزولها ويختبر صلاحية أكواد الخصم والعملات.</p>
          </div>
        </div>

        <!-- Affiliate Disclosure Notice -->
        <div class="border rounded-2xl p-4 sm:p-5 space-y-2 text-xs" style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-muted);">
          <h2 class="font-bold flex items-center gap-2 text-xs" style="color: var(--text-main);">
            <i class="fa-solid fa-handshake text-blue-500"></i>
            <span data-i18n="about_disclosure_title">إفصاح الشفافية والتسويق بالعمولة (Affiliate Disclosure)</span>
          </h2>
          <p class="leading-relaxed" data-i18n="about_disclosure_desc">
            منصة DealScout DZ مشتركة في برنامج شركاء AliExpress الرسمي (AliExpress Portals Affiliate Program). عند النقر على روابط الشراء وإتمام الطلب، قد نحصل على عمولة تسويقية صغيرة من منصة AliExpress دون أي تكلفة إضافية عليك.
          </p>
        </div>

      </div>

    </div>

  </main>

  <!-- Mobile Bottom Navigation Bar -->
  <nav class="md:hidden fixed bottom-0 left-0 right-0 z-50 backdrop-blur-md border-t px-1 py-1 flex items-center justify-around text-center text-[10px] bottom-nav-safe transition-colors" style="background-color: var(--header-bg); border-color: var(--border-card);" aria-label="التنقل للجوال">
    <button onclick="showPage('deals')" id="mob-bottom-deals" class="flex-1 min-h-[48px] py-1 flex flex-col items-center justify-center gap-0.5 text-crimson-500 font-bold active:scale-90 transition-transform touch-manipulation cursor-pointer">
      <i class="fa-solid fa-fire text-base"></i>
      <span data-i18n="nav_deals">الصفقات</span>
    </button>
    <button onclick="showPage('tracking')" id="mob-bottom-tracking" class="flex-1 min-h-[48px] py-1 flex flex-col items-center justify-center gap-0.5 opacity-70 hover:opacity-100 font-medium active:scale-90 transition-transform touch-manipulation cursor-pointer text-blue-500">
      <i class="fa-solid fa-box text-base"></i>
      <span data-i18n="nav_tracking">تتبع الطرود</span>
    </button>
    <a href="https://t.me/DzAliexpress0" id="mob-bottom-tg" target="_blank" rel="noopener noreferrer" class="flex-1 min-h-[48px] py-1 flex flex-col items-center justify-center gap-0.5 text-sky-500 font-bold active:scale-90 transition-transform touch-manipulation cursor-pointer">
      <i class="fa-brands fa-telegram text-lg"></i>
      <span data-i18n="nav_telegram">تيليجرام</span>
    </a>
    <button onclick="showPage('coins')" id="mob-bottom-coins" class="flex-1 min-h-[48px] py-1 flex flex-col items-center justify-center gap-0.5 opacity-70 hover:opacity-100 font-medium active:scale-90 transition-transform touch-manipulation cursor-pointer">
      <i class="fa-solid fa-coins text-base text-amber-500"></i>
      <span data-i18n="nav_coins">العملات</span>
    </button>
    <button onclick="showPage('cards')" id="mob-bottom-cards" class="flex-1 min-h-[48px] py-1 flex flex-col items-center justify-center gap-0.5 opacity-70 hover:opacity-100 font-medium active:scale-90 transition-transform touch-manipulation cursor-pointer">
      <i class="fa-solid fa-credit-card text-base text-emerald-500"></i>
      <span data-i18n="nav_cards">البطاقات</span>
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
        <span id="modal-country" class="absolute top-2.5 right-2.5 text-xs px-2.5 py-1 rounded-lg font-black border hidden shadow-md z-20 backdrop-blur-md" style="background-color: #e11d48; border-color: rgba(255, 255, 255, 0.35); color: #ffffff;"></span>
        <span id="modal-coins" class="absolute top-2.5 left-2.5 bg-amber-500 text-zinc-950 text-xs font-bold px-2 py-0.5 rounded-lg hidden items-center gap-1 shadow-sm"><i class="fa-solid fa-coins text-[10px]"></i> Coins</span>
      </div>

      <!-- Modal Content Body -->
      <div class="space-y-3.5">
        <div class="flex items-center justify-between gap-2 text-xs" style="color: var(--text-soft);">
          <span id="modal-cat" class="px-2.5 py-1 rounded-lg border text-[11px] font-semibold" style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-main);"></span>
          <span id="modal-date" class="font-mono text-xs opacity-75"></span>
        </div>

        <!-- Prominent Country Setting Alert -->
        <div id="modal-country-alert" class="hidden rounded-xl p-3 border flex items-center justify-between gap-3 shadow-sm transition" style="background-color: var(--bg-elevated); border-color: rgba(225, 29, 72, 0.35);">
          <div class="flex items-center gap-2.5 min-w-0">
            <div class="w-8 h-8 rounded-lg flex items-center justify-center text-sm font-bold flex-shrink-0 bg-rose-500/15 text-rose-500">
              <i class="fa-solid fa-location-dot"></i>
            </div>
            <div class="min-w-0">
              <div class="text-[10px] font-bold uppercase tracking-wider opacity-70" data-i18n="modal_country_hint">شرط تطبيق سعر العرض:</div>
              <div class="text-xs sm:text-sm font-black" style="color: var(--text-main);">
                <span>خلي بلد الحساب في تطبيق AliExpress:</span>
                <span id="modal-country-target" class="text-rose-600 dark:text-rose-400 font-extrabold underline decoration-rose-500/50 decoration-2 px-1"></span>
              </div>
            </div>
          </div>
          <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-rose-500/10 text-rose-500 border border-rose-500/25 flex-shrink-0">ضروري للخصم</span>
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
          <button id="modal-coupon-btn" onclick="copyCouponFromModal(this)" class="min-h-[42px] px-3.5 py-1.5 border active:scale-95 text-xs font-bold rounded-lg transition flex items-center gap-1.5 flex-shrink-0 touch-manipulation cursor-pointer" style="background-color: var(--bg-card); border-color: var(--border-card); color: var(--text-main);">
            <i class="fa-regular fa-copy"></i>
            <span class="copy-text" data-i18n="btn_copy">نسخ الكود</span>
          </button>
        </div>

        <!-- Multi-coupon container inside modal -->
        <div id="modal-multi-coupons" class="hidden flex flex-col gap-2"></div>

        <!-- Clean Description / Specs inside modal -->
        <div id="modal-desc-wrap" class="hidden rounded-xl p-3 border text-xs sm:text-sm leading-relaxed whitespace-pre-line select-text" style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-muted);">
          <div class="text-[10px] font-bold uppercase tracking-wider mb-1.5 opacity-75 flex items-center gap-1.5" style="color: var(--text-main);">
            <i class="fa-solid fa-list-check text-rose-500 text-[11px]"></i>
            <span>المواصفات وملاحظات العرض:</span>
          </div>
          <div id="modal-desc-text" class="font-sans leading-relaxed"></div>
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

  <!-- Floating Deal Discovery Button (Desktop & Tablet only, hidden on phones) -->
  <button id="fab-roulette" onclick="openRouletteModal()" aria-label="اقتراح صفقة" class="hidden md:flex fixed z-40 bottom-6 right-6 backdrop-blur-md active:scale-95 text-xs font-semibold px-4 py-2.5 rounded-full shadow-lg items-center gap-2 cursor-pointer transition-all touch-manipulation border" style="background-color: var(--bg-card); border-color: var(--border-card); color: var(--text-main);">
    <i class="fa-solid fa-sparkles text-xs text-emerald-500"></i>
    <span data-i18n="roulette_fab">اقتراح صفقة</span>
  </button>

  <!-- Deal Discovery Modal -->
  <div id="roulette-modal" onclick="onRouletteBackdropClick(event)" style="display: none;" class="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm hidden items-end sm:items-center justify-center p-0 sm:p-4 animate-fade-in" role="dialog" aria-modal="true" aria-labelledby="roulette-modal-title">
    <div class="border-t sm:border rounded-t-3xl sm:rounded-2xl w-full max-w-md max-h-[90vh] overflow-y-auto no-scrollbar shadow-2xl p-5 sm:p-6 pb-safe space-y-4 animate-slide-up relative" style="background-color: var(--bg-card); border-color: var(--border-card);">
      
      <!-- Pull handle on mobile -->
      <div class="sm:hidden w-12 h-1.5 rounded-full mx-auto -mt-1 mb-2 opacity-40 cursor-pointer" style="background-color: var(--text-soft);" onclick="closeRouletteModal()"></div>
      
      <!-- Close button -->
      <button type="button" onclick="closeRouletteModal()" aria-label="إغلاق" class="absolute top-3.5 left-3.5 w-8 h-8 rounded-full flex items-center justify-center text-xs border active:scale-95 transition z-30 touch-manipulation cursor-pointer hover:opacity-80" style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-muted);">
        <i class="fa-solid fa-xmark"></i>
      </button>

      <div class="text-center space-y-1.5 pt-1">
        <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium border" style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-muted);">
          <i class="fa-solid fa-sliders text-[11px] text-emerald-500"></i>
          <span data-i18n="roulette_badge">اختيار تلقائي ذكي</span>
        </div>
        <h3 id="roulette-modal-title" class="text-base sm:text-lg font-bold tracking-tight" style="color: var(--text-main);" data-i18n="roulette_title">صفقة مقترحة مختارة</h3>
        <p class="text-xs max-w-xs mx-auto leading-relaxed" style="color: var(--text-muted);" data-i18n="roulette_subtitle">اضغط على الزر لاقتراح صفقة نشطة بأقوى نسبة تخفيض</p>
      </div>

      <!-- Display Card Container -->
      <div id="roulette-display-card" class="border rounded-xl p-4 space-y-3 relative overflow-hidden transition-all text-right" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
        <div id="roulette-img-wrap" class="relative w-full aspect-[16/10] sm:aspect-[4/3] rounded-lg overflow-hidden border flex items-center justify-center mx-auto" style="background-color: var(--bg-page); border-color: var(--border-card);">
          <img id="roulette-img" src="" alt="Deal" class="w-full h-full object-contain transition-transform duration-200">
          <div id="roulette-winner-tag" class="hidden absolute top-2 right-2 text-white text-[11px] font-semibold px-2.5 py-0.5 rounded shadow-sm flex items-center gap-1.5 bg-emerald-600">
            <i class="fa-solid fa-check text-[10px]"></i> <span data-i18n="roulette_winner_tag">صفقة مختارة</span>
          </div>
        </div>

        <div class="space-y-2">
          <!-- Category & Country Header Row -->
          <div class="flex items-center justify-between gap-2">
            <span id="roulette-cat" class="text-[10px] font-semibold px-2 py-0.5 rounded border" style="background-color: var(--bg-card); border-color: var(--border-card); color: var(--text-muted);"></span>
            
            <!-- COUNTRY CALLOUT BADGE -->
            <div id="roulette-country-badge" class="inline-flex items-center gap-1 text-[11px] font-bold px-2 py-0.5 rounded border" style="background-color: var(--bg-page); border-color: var(--border-card); color: var(--text-main);">
              <i class="fa-solid fa-location-dot text-emerald-500 text-[10px]"></i>
              <span id="roulette-country-text">الجزائر 🇩🇿</span>
            </div>
          </div>

          <h4 id="roulette-deal-title" class="font-bold text-xs sm:text-sm line-clamp-2 leading-snug" style="color: var(--text-main);">اضغط زر الاقتراح للبدء</h4>

          <!-- Price & Coupon Clean Row -->
          <div id="roulette-price-wrap" class="flex items-center justify-between pt-2 border-t" style="border-color: var(--border-card);">
            <div id="roulette-price" class="text-sm sm:text-base font-bold font-mono" style="color: var(--text-main);"></div>
            <div id="roulette-coupon-pill" class="text-xs font-mono font-semibold px-2 py-0.5 rounded border" style="background-color: var(--bg-page); border-color: var(--border-card); color: var(--text-main);"></div>
          </div>

          <!-- PROMINENT COUNTRY INSTRUCTION BOX -->
          <div id="roulette-country-box" class="flex items-center justify-between px-3 py-2 rounded-lg border text-xs" style="background-color: var(--bg-page); border-color: var(--border-card);">
            <span class="flex items-center gap-1.5 text-[11px]" style="color: var(--text-muted);">
              <i class="fa-solid fa-earth-americas text-emerald-500"></i>
              <span data-i18n="roulette_country_label">الدولة المطلوبة في التطبيق:</span>
            </span>
            <span id="roulette-country-val" class="font-bold text-xs text-emerald-500">الجزائر 🇩🇿</span>
          </div>
        </div>
      </div>

      <!-- Action buttons -->
      <div class="space-y-2 pt-1">
        <a id="roulette-buy-btn" href="#" target="_blank" rel="noopener noreferrer" style="display: none;" class="w-full min-h-[44px] rounded-xl text-white font-semibold text-sm flex items-center justify-center gap-2 shadow-sm transition cursor-pointer touch-manipulation bg-emerald-600 hover:bg-emerald-500 active:scale-98">
          <i class="fa-solid fa-arrow-up-right-from-square text-xs"></i>
          <span data-i18n="roulette_claim_btn">فتح رابط الشراء على AliExpress</span>
        </a>

        <button id="roulette-spin-btn" onclick="spinRoulette()" class="w-full min-h-[44px] rounded-xl font-semibold text-sm flex items-center justify-center gap-2 border transition cursor-pointer touch-manipulation active:scale-98 hover:opacity-90" style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-main);">
          <i class="fa-solid fa-arrows-rotate text-xs"></i>
          <span id="roulette-btn-text" data-i18n="roulette_spin_btn">اقتراح صفقة أخرى</span>
        </button>
      </div>

      <!-- Tip -->
      <div class="text-center text-[11px] opacity-60 flex items-center justify-center gap-1.5 pt-0.5" style="color: var(--text-muted);">
        <i class="fa-solid fa-mobile-screen text-[10px]"></i>
        <span data-i18n="roulette_shake_tip">يمكنك هز الهاتف لاقتراح صفقة أخرى تلقائياً</span>
      </div>

    </div>
  </div>

  <!-- Shopping Tools Hub & Square Dinar Calculator Modal -->
  <div id="gamification-modal" onclick="onGamificationBackdropClick(event)" style="display: none;" class="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm hidden items-end sm:items-center justify-center p-0 sm:p-4 animate-fade-in" role="dialog" aria-modal="true" aria-labelledby="tools-modal-title">
    <div class="border-t sm:border rounded-t-3xl sm:rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto no-scrollbar shadow-2xl p-5 sm:p-6 pb-safe space-y-5 animate-slide-up relative" style="background-color: var(--bg-card); border-color: var(--border-card);">
      
      <!-- Pull handle on mobile -->
      <div class="sm:hidden w-12 h-1.5 rounded-full mx-auto -mt-1 mb-2 opacity-40 cursor-pointer" style="background-color: var(--text-soft);" onclick="closeGamificationHub()"></div>
      
      <!-- Close button -->
      <button type="button" onclick="closeGamificationHub()" aria-label="إغلاق" class="absolute top-3.5 left-3.5 w-9 h-9 rounded-full flex items-center justify-center text-sm border active:scale-95 transition z-30 touch-manipulation cursor-pointer hover:bg-rose-600 hover:text-white" style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-main);">
        <i class="fa-solid fa-xmark"></i>
      </button>

      <!-- Modal Header -->
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-emerald-500/15 text-emerald-500 flex items-center justify-center text-xl">
          <i class="fa-solid fa-calculator"></i>
        </div>
        <div>
          <h3 id="tools-modal-title" class="font-bold text-base sm:text-lg" style="color: var(--text-main);" data-i18n="tools_modal_title">مركز الأدوات وحاسبة السكوار</h3>
          <p class="text-xs" style="color: var(--text-muted);" data-i18n="tools_modal_subtitle">حاسبة السكوار الفورية للدينار الجزائري وروابط الوصول السريع للقنوات</p>
        </div>
      </div>

      <!-- Live Square Dinar Calculator Card -->
      <div class="border rounded-2xl p-4 sm:p-5 space-y-4" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
        <div class="flex items-center justify-between pb-2 border-b" style="border-color: var(--border-card);">
          <div class="flex items-center gap-2">
            <i class="fa-solid fa-chart-line text-emerald-500"></i>
            <span class="font-bold text-xs sm:text-sm" style="color: var(--text-main);" data-i18n="calc_title">حاسبة التحويل بسعر السكوار</span>
          </div>
          <span class="text-[11px] font-mono font-bold text-emerald-500 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
            1 USDT ≈ <span id="calc-usdt-rate">256.9</span> دج
          </span>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <!-- Foreign Currency Input -->
          <div>
            <label class="block text-[11px] font-bold mb-1 opacity-75" style="color: var(--text-main);" data-i18n="calc_amount_foreign">المبلغ بالدولار ($) أو اليورو (€)</label>
            <div class="relative">
              <input 
                type="number" 
                id="calc-foreign-input" 
                min="0" 
                step="0.01" 
                placeholder="مثال: 25.50" 
                oninput="onCalcForeignChange(this.value)"
                class="w-full border rounded-xl px-3 py-2 text-sm font-mono font-bold focus:outline-none focus:border-rose-500 transition min-h-[42px]"
                style="background-color: var(--input-bg); border-color: var(--border-card); color: var(--text-main);"
              />
              <span class="absolute left-3 top-1/2 -translate-y-1/2 text-xs font-mono opacity-50" id="calc-curr-symbol">$</span>
            </div>
          </div>

          <!-- DZD Result Input -->
          <div>
            <label class="block text-[11px] font-bold mb-1 opacity-75" style="color: var(--text-main);" data-i18n="calc_amount_dzd">المبلغ المقابل بالدينار الجزائري (دج)</label>
            <div class="relative">
              <input 
                type="number" 
                id="calc-dzd-input" 
                min="0" 
                step="10" 
                placeholder="مثال: 6500" 
                oninput="onCalcDzdChange(this.value)"
                class="w-full border rounded-xl px-3 py-2 text-sm font-mono font-bold focus:outline-none focus:border-emerald-500 transition min-h-[42px] text-emerald-500"
                style="background-color: var(--input-bg); border-color: var(--border-card);"
              />
              <span class="absolute left-3 top-1/2 -translate-y-1/2 text-xs font-mono font-bold text-emerald-500">دج</span>
            </div>
          </div>
        </div>

        <!-- Breakdown Info -->
        <div class="p-2.5 rounded-xl text-[11px] space-y-1 border" style="background-color: var(--bg-card); border-color: var(--border-card); color: var(--text-muted);">
          <div class="flex justify-between">
            <span data-i18n="calc_bybit_fee">تكلفة الشراء عبر بطاقة Bybit (رسوم 0%):</span>
            <span id="calc-bybit-total" class="font-mono font-bold text-emerald-500">0 دج</span>
          </div>
          <div class="flex justify-between">
            <span data-i18n="calc_redot_fee">تكلفة الشراء عبر بطاقة RedotPay (رسوم ~1.2%):</span>
            <span id="calc-redot-total" class="font-mono font-bold text-rose-500">0 دج</span>
          </div>
        </div>
      </div>

      <!-- Quick Shopping Tools & Direct Channels -->
      <div class="space-y-2.5">
        <h4 class="font-bold text-xs opacity-75" style="color: var(--text-muted);" data-i18n="tools_quick_links">وصول سريع للأدوات والقنوات:</h4>
        
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
          <!-- Official Algeria Channel -->
          <a href="https://t.me/DzAliexpress0" target="_blank" rel="noopener noreferrer" class="border rounded-xl p-3 flex items-center justify-between gap-2 transition hover:border-[#229ED9] active:scale-95 touch-manipulation" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
            <div class="flex items-center gap-2.5">
              <div class="w-8 h-8 rounded-lg bg-[#229ED9]/15 text-[#229ED9] flex items-center justify-center text-base">
                <i class="fa-brands fa-telegram"></i>
              </div>
              <div>
                <div class="font-bold" style="color: var(--text-main);">صفقات الجزائر</div>
                <div class="text-[10px] opacity-60">@DzAliexpress0</div>
              </div>
            </div>
            <i class="fa-solid fa-arrow-up-right-from-square text-xs opacity-50"></i>
          </a>

          <!-- Official France Channel -->
          <a href="https://t.me/francedealsdz" target="_blank" rel="noopener noreferrer" class="border rounded-xl p-3 flex items-center justify-between gap-2 transition hover:border-[#229ED9] active:scale-95 touch-manipulation" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
            <div class="flex items-center gap-2.5">
              <div class="w-8 h-8 rounded-lg bg-[#229ED9]/15 text-[#229ED9] flex items-center justify-center text-base">
                <i class="fa-brands fa-telegram"></i>
              </div>
              <div>
                <div class="font-bold" style="color: var(--text-main);">صفقات فرنسا</div>
                <div class="text-[10px] opacity-60">@francedealsdz</div>
              </div>
            </div>
            <i class="fa-solid fa-arrow-up-right-from-square text-xs opacity-50"></i>
          </a>

          <!-- Coin Bot -->
          <a href="https://t.me/Alilo07BOT" target="_blank" rel="noopener noreferrer" class="border rounded-xl p-3 flex items-center justify-between gap-2 transition hover:border-amber-500 active:scale-95 touch-manipulation" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
            <div class="flex items-center gap-2.5">
              <div class="w-8 h-8 rounded-lg bg-amber-500/15 text-amber-500 flex items-center justify-center text-base">
                <i class="fa-solid fa-coins"></i>
              </div>
              <div>
                <div class="font-bold" style="color: var(--text-main);">بوت العملات</div>
                <div class="text-[10px] opacity-60">@Alilo07BOT</div>
              </div>
            </div>
            <i class="fa-solid fa-arrow-up-right-from-square text-xs opacity-50"></i>
          </a>

          <!-- Cards Guide -->
          <button onclick="closeGamificationHub(); showPage('cards');" class="border rounded-xl p-3 flex items-center justify-between gap-2 transition hover:border-emerald-500 active:scale-95 touch-manipulation text-right" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
            <div class="flex items-center gap-2.5">
              <div class="w-8 h-8 rounded-lg bg-emerald-500/15 text-emerald-500 flex items-center justify-center text-base">
                <i class="fa-solid fa-credit-card"></i>
              </div>
              <div>
                <div class="font-bold" style="color: var(--text-main);">بطاقات الدفع وبريدي موب</div>
                <div class="text-[10px] opacity-60">Bybit & RedotPay</div>
              </div>
            </div>
            <i class="fa-solid fa-chevron-left text-xs opacity-50 rtl:rotate-0 ltr:rotate-180"></i>
          </button>

          <!-- Coins Link Generator Shortcut -->
          <button onclick="closeGamificationHub(); showPage('coins'); setTimeout(() => document.getElementById('coins-input-url')?.focus(), 150);" class="border rounded-xl p-3 flex items-center justify-between gap-2 transition hover:border-amber-500 active:scale-95 touch-manipulation text-right" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
            <div class="flex items-center gap-2.5">
              <div class="w-8 h-8 rounded-lg bg-amber-500/15 text-amber-500 flex items-center justify-center text-base">
                <i class="fa-solid fa-wand-magic-sparkles"></i>
              </div>
              <div>
                <div class="font-bold text-amber-500" data-i18n="tools_coin_generator">مولد روابط العملات 🪙</div>
                <div class="text-[10px] opacity-60">توليد خصم فوري بالرابط</div>
              </div>
            </div>
            <i class="fa-solid fa-chevron-left text-xs opacity-50 rtl:rotate-0 ltr:rotate-180"></i>
          </button>
        </div>
      </div>

      <!-- Real Cumulative Estimated Savings Box -->
      <div class="border rounded-xl p-3.5 flex items-center justify-between" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
        <div class="flex items-center gap-2">
          <i class="fa-solid fa-piggy-bank text-emerald-500 text-base"></i>
          <div>
            <div class="text-[10px] opacity-70" data-i18n="tools_savings_title">إجمالي التوفير التقديري من الكوبونات:</div>
            <div id="tools-total-saved" class="font-black font-mono text-emerald-500 text-sm sm:text-base">0 دج</div>
          </div>
        </div>
        <button onclick="filterByFavoritesMobile(); closeGamificationHub();" class="text-xs font-bold text-rose-500 hover:underline flex items-center gap-1 active:scale-95">
          <i class="fa-solid fa-heart text-[10px]"></i>
          <span data-i18n="tools_view_favs">عرض المفضلة</span>
        </button>
      </div>

    </div>
  </div>

  <!-- ========================================== -->
  <!-- TELEGRAM CHANNEL JOIN MODAL / POPUP        -->
  <!-- ========================================== -->
  <div id="telegram-modal" onclick="onTelegramPopupBackdropClick(event)" style="display: none;" class="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm hidden items-end sm:items-center justify-center p-0 sm:p-4 animate-fade-in" role="dialog" aria-modal="true" aria-labelledby="tg-popup-title">
    <div id="telegram-popup-container" class="border-t sm:border rounded-t-3xl sm:rounded-2xl w-full max-w-md max-h-[90vh] overflow-y-auto no-scrollbar shadow-2xl p-5 sm:p-6 pb-safe space-y-4 animate-slide-up relative" style="background-color: var(--bg-card); border-color: var(--border-card);">
      
      <!-- Pull handle on mobile -->
      <div class="sm:hidden w-12 h-1.5 rounded-full mx-auto -mt-1 mb-2 opacity-40 cursor-pointer" style="background-color: var(--text-soft);" onclick="closeTelegramPopup(true)"></div>

      <!-- Top Bar: Badge & Close Button -->
      <div class="flex items-center justify-between">
        <div class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold bg-[#229ED9]/15 text-[#229ED9] border border-[#229ED9]/30">
          <i class="fa-brands fa-telegram text-sm"></i>
          <span data-i18n="tg_popup_badge">قناة تيليجرام الرسمية 🇩🇿</span>
        </div>
        <button onclick="closeTelegramPopup(true)" aria-label="إغلاق النافذة" class="w-8 h-8 rounded-full border flex items-center justify-center text-xs opacity-75 hover:opacity-100 transition active:scale-95 touch-manipulation cursor-pointer" style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-main);">
          <i class="fa-solid fa-xmark text-sm"></i>
        </button>
      </div>

      <!-- Icon & Headline -->
      <div class="text-center pt-1 pb-1 space-y-2">
        <div class="w-16 h-16 mx-auto rounded-2xl bg-gradient-to-tr from-[#229ED9] to-[#0088cc] flex items-center justify-center shadow-lg shadow-[#229ED9]/25 text-white text-3xl">
          <i class="fa-brands fa-telegram"></i>
        </div>
        <h3 id="tg-popup-title" class="text-lg sm:text-xl font-black leading-tight" style="color: var(--text-main);" data-i18n="tg_popup_title">
          لا تفوّت صفقات وتخفيضات علي اكسبراس في الجزائر!
        </h3>
        <p class="text-xs sm:text-sm leading-relaxed" style="color: var(--text-muted);" data-i18n="tg_popup_desc">
          أقوى الصفقات الخارقة وكوبونات التخفيض تنفذ في دقائق معدودة! انضم إلى قناتنا على تيليجرام لتصلك تنبيهات العروض اللحظية والعملات في الجزائر مباشرة على هاتفك مجاناً.
        </p>
      </div>

      <!-- Value Proposition Highlights -->
      <div class="space-y-2 pt-1 text-xs" style="color: var(--text-main);">
        <div class="flex items-center gap-2.5 p-2.5 rounded-xl border" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
          <div class="w-7 h-7 rounded-lg bg-crimson-500/15 text-crimson-500 flex items-center justify-center text-xs font-bold flex-shrink-0">
            <i class="fa-solid fa-bolt"></i>
          </div>
          <div class="flex-1 min-w-0">
            <span class="font-bold block text-xs" data-i18n="tg_popup_feat1_title">عروض سريعة وكوبونات فورية</span>
            <span class="text-[11px] opacity-75 block leading-tight mt-0.5" data-i18n="tg_popup_feat1_desc">نشر فوري للصفقات الخاطفة قبل نفاذ الكمية في الجزائر</span>
          </div>
        </div>

        <div class="flex items-center gap-2.5 p-2.5 rounded-xl border" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
          <div class="w-7 h-7 rounded-lg bg-amber-500/15 text-amber-500 flex items-center justify-center text-xs font-bold flex-shrink-0">
            <i class="fa-solid fa-coins"></i>
          </div>
          <div class="flex-1 min-w-0">
            <span class="font-bold block text-xs" data-i18n="tg_popup_feat2_title">روابط خصم العملات الأقصى (Coins)</span>
            <span class="text-[11px] opacity-75 block leading-tight mt-0.5" data-i18n="tg_popup_feat2_desc">تخفيضات حقيقية تصل إلى 70% عبر روابط العملات الحصرية</span>
          </div>
        </div>

        <div class="flex items-center gap-2.5 p-2.5 rounded-xl border" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
          <div class="w-7 h-7 rounded-lg bg-emerald-500/15 text-emerald-500 flex items-center justify-center text-xs font-bold flex-shrink-0">
            <i class="fa-solid fa-money-bill-wave"></i>
          </div>
          <div class="flex-1 min-w-0">
            <span class="font-bold block text-xs" data-i18n="tg_popup_feat3_title">أسعار حقيقية بالدينار الجزائري (DZD)</span>
            <span class="text-[11px] opacity-75 block leading-tight mt-0.5" data-i18n="tg_popup_feat3_desc">حساب السعر بسعر السكوار لحظياً دون رسوم مخفية</span>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="pt-2 space-y-2">
        <a id="tg-popup-join-btn" href="https://t.me/DzAliexpress0" target="_blank" rel="noopener noreferrer" onclick="onTelegramPopupJoinClick()" class="w-full min-h-[48px] bg-[#229ED9] hover:bg-[#1c8cc1] active:scale-[0.98] text-white font-extrabold text-sm py-3 px-4 rounded-xl text-center flex items-center justify-center gap-2 shadow-lg shadow-[#229ED9]/25 transition touch-manipulation cursor-pointer">
          <i class="fa-brands fa-telegram text-lg"></i>
          <span data-i18n="tg_popup_join_cta">انضم إلى قناة التيليجرام الآن مجاناً</span>
          <i class="fa-solid fa-arrow-up-right-from-square text-xs opacity-75"></i>
        </a>

        <div class="flex items-center justify-between text-xs pt-1 px-1">
          <a href="https://t.me/francedealsdz" target="_blank" rel="noopener noreferrer" onclick="onTelegramPopupJoinClick()" class="opacity-75 hover:opacity-100 hover:text-sky-500 transition flex items-center gap-1">
            <span>🇫🇷</span>
            <span data-i18n="tg_popup_france_link">قناة عروض فرنسا (@francedealsdz)</span>
          </a>
          <button onclick="closeTelegramPopup(true)" class="opacity-70 hover:opacity-100 underline transition touch-manipulation cursor-pointer" data-i18n="tg_popup_dismiss">
            لاحقاً، تصفح الموقع
          </button>
        </div>
      </div>

    </div>
  </div>

  <!-- Confetti Canvas Particle Overlay -->
  <canvas id="confetti-canvas" class="fixed inset-0 pointer-events-none z-[9999] w-full h-full" style="display: none;"></canvas>

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
            <li><a href="/blog/aliexpress-algeria-guide-dz" class="hover:underline transition text-amber-400 font-bold flex items-center gap-1"><i class="fa-solid fa-book-open text-[10px]"></i> <span>دليل الشراء من AliExpress 2026</span></a></li>
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
        meta_title: "DealScout DZ — عروض وتخفيضات علي اكسبراس في الجزائر | AliExpress Deals DZ",
        meta_desc: "منصة DealScout DZ الأولى لرصد أقوى عروض وتخفيضات علي اكسبراس في الجزائر (AliExpress Deals DZ). تتبع صفقات aliexpressdz، كود تخفيض علي اكسبراس، طرق الشراء من علي اكسبراس في الجزائر بالدينار، وروابط خصم العملات وقناة التيليجرام الرسمية.",
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
        country_filter_label: "تصفية حسب البلد:",
        country_all: "كل البلدان 🌍",
        sort_label: "ترتيب:",
        sort_newest: "الأحدث أولاً 🕒",
        sort_price_asc: "الأقل سعراً 📉",
        sort_price_desc: "الأعلى سعراً 📈",
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
        cards_redot_badge: "هدية 5$ ترحيبية",
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
        cards_faq_badge: "أسئلة شائعة حول البطاقات والشحن",
        cards_faq_title: "أهم الأسئلة الشائعة حول الدفع والشراء بالدينار الجزائري",
        cards_faq_q1: "هل بطاقة Bybit Card مجانية حقاً وبدون اشتراك شهري؟",
        cards_faq_a1: "نعم، بطاقة Bybit ماستركارد الافتراضية مجانية 100% بدون أي مصاريف فتح وبدون اقتطاع شهري أو سنوي. تدعم الدفع المباشر على AliExpress وPayPal وتحصل معها على كاش باك يصل إلى 10%.",
        cards_faq_q2: "كيف أشحن بطاقة RedotPay أو Bybit باستخدام بريدي موب (BaridiMob)؟",
        cards_faq_a2: "تتم العملية عبر منصة Binance P2P: تشتري الدولار الرقمي (USDT) بالدينار الجزائري مباشرة من بائعين جزائريين موثوقين وتدفع عبر تطبيق BaridiMob، ثم تسحب الرصيد إلى بطاقة RedotPay أو Bybit في ثوانٍ عبر شبكة BSC أو TRC20.",
        cards_faq_q3: "هل تقبل بطاقة RedotPay و Bybit التفعيل مع حساب PayPal الجزائري؟",
        cards_faq_a3: "نعم، كلاً من بطاقة RedotPay وبطاقة Bybit تقبل الربط مع PayPal الجزائري أو الأجنبي، وتصل رسالة رمز التفعيل (4 أرقام) فورياً داخل تطبيق البطاقة.",
        cards_faq_q4: "ما هو كود الحصول على هدية 5$ المجانية في RedotPay؟",
        cards_faq_a4: "عند التسجيل في RedotPay، أدخل كود الإحالة الحصري djbt3 لتحصل فوراً على بونص 5$ رصيد ترحيبي في حسابك بمجرد إكمال تأكيد الهوية ببطاقة التعريف الوطنية.",
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
        faq_q6: "كيف أشتري من AliExpress باستخدام تطبيق بريدي موب (BaridiMob)؟",
        faq_a6: "لا يقبل AliExpress الدفع المباشر بالدينار أو البطاقة الذهبية. الطريقة المعتمدة هي فتح حساب في Binance واستخدام قسم التداول P2P لشراء رصيد USDT بالدينار الجزائري عبر بريدي موب من بائع معتمد، ثم تحويل الرصيد إلى بطاقة Bybit ماستركارد المجانية أو بطاقة RedotPay واستعمالها في الدفع فوراً.",
        faq_q7: "ما هي قوانين الجمارك الجزائرية للطرود؟ وما هي المنتجات الممنوعة؟",
        faq_a7: "الطرود الموجهة للاستعمال الشخصي والعائلي معفاة تماماً من الرسوم الجمركية في الجزائر. لتفادي المشاكل، لا تطلب كميات تجارية متكررة من نفس السلعة في شحنة واحدة. يُمنع منعاً باتاً استيراد: طائرات الدرون بجميع أنواعها، كاميرات التجسس المخفية، أجهزة اللاسلكي غير المرخصة، ومؤشرات الليزر المحظورة.",
        faq_q8: "كيف أحصل على أقصى تخفيض للعملات Coins (حتى 70%)؟",
        faq_a8: "عند التسوق العادي يخصم AliExpress نسبة 1% إلى 5% فقط من العملات. باستخدام أداة مولد روابط العملات على موقعنا أو بوت @Alilo07BOT، يتم توليد رابط مخصص مع وسم المصدر sourceType=620، مما يرفع نسبة قبول العملات على نفس السلعة حتى 50% أو 70% عند الشراء مباشرة من قسم العملات.",
        faq_q9: "كيف أكتب العنوان الجزائري والرمز البريدي (Code Postal) بشكل صحيح؟",
        faq_a9: "اكتب اسمك الكامل مطابقاً لبطاقة التعريف الوطنية، ورقم هاتفك المحمول الصحيح لتلقي SMS من بريد الجزائر. الرمز البريدي يتكون من 5 أرقام (أول رقمين هما رقم ولايتك، مثلاً 16 للجزائر أو 31 لوهران)، والأرقام الثلاثة المتبقية تدل على مركز التوزيع لبلديتك. احرص على وضع كود مركز البريد الأقرب إليك لضمان عدم تأخر الطرد.",
        cards_post_badge: "إرشادات الشحن والجمارك في الجزائر 2026",
        cards_post_title: "ضبط العنوان الجزائري، قوانين الجمارك (Douane)، واستلام الطرد من البريد",
        cards_addr_h: "1. ضبط الرمز البريدي والعنوان",
        cards_addr_p: "اكتب اسمك المطابق لبطاقة الهوية ورقم هاتفك الفعال لتلقي SMS. تأكد من إدخال الرمز البريدي الدقيق المكون من 5 أرقام (أول رقمين هما رقم ولايتك، والـ 3 أرقام التالية هي مركز التوزيع البريدي لبلديتك).",
        cards_customs_h: "2. الجمارك الجزائرية والطرود",
        cards_customs_p: "الطرود الشخصية معفاة من الرسوم الجمركية. تجنب طلب كميات تجارية من نفس الصنف لتفادي الحجز. يُمنع منعاً باتاً استيراد طائرات الدرون، كاميرات المراقبة التجسسية المخفية، وأجهزة اللاسلكي غير المرخصة.",
        cards_pickup_h: "3. التتبع والاستلام من البريد",
        cards_pickup_p: "تتبع شحنتك عبر 17track وموقع بريد الجزائر بمجرد وصولها. عند وصول إشعار SMS أو Avis de passage، توجه إلى مكتب البريد مصحوباً ببطاقتك الوطنية، وادفع رسم التخليص البريدي الرمزي (~130 إلى 250 دج) واستلم طردك.",
        cards_crosslink_heading: "انتقل إلى أقسام الموقع الأخرى:",
        crosslink_cards_title: "دليل بطاقات الدفع وبريدي موب",
        crosslink_cards_sub: "Bybit مجانية وRedotPay",
        crosslink_coins_title: "بوت ومولد تخفيض العملات Coins",
        crosslink_coins_sub: "وفر حتى 70% من السعر",
        crosslink_faq_title: "الأسئلة الشائعة وقوانين الجمارك",
        crosslink_faq_sub: "الشحن واستلام الطرود بالبريد",
        coins_steps_section_title: "طريقة تفعيل أقصى خصم للعملات خطوة بخطوة 🪙",
        coins_steps_section_sub: "اتبع هذه الخطوات البسيطة لتحويل أي رابط منتج عادي إلى رابط تخفيض العملات الأقصى:",
        coins_crosslink_heading: "تصفح أيضاً عبر DealScout DZ:",
        faq_crosslink_heading: "مواضيع ذات صلة تهمك:",
        contact_title: "اتصل بنا والدعم الفني",
        contact_subtitle: "فريق DealScout DZ يرحب باقتراحاتكم، إبلاغكم عن الروابط التالفة، واستفساراتكم حول الصفقات.",
        contact_tg_title: "مجموعة المناقشات والاستفسارات عبر Telegram",
        contact_tg_desc: "تواصل معنا مباشرة عبر مجموعة النقاش والشات الملحقة بقناة صفقات الجزائر الرسمية. اطرح سؤالك، اطلب التحقق من أي صفقة أو شارك تجربتك مع مجتمع المتسوقين.",
        contact_tg_btn_admin: "مجموعة المناقشات والاستفسارات (@DzAliexpress0)",
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
        footer_back_top: "للأعلى",
        active_event_badge: "حدث ترويجي فعال حالياً",
        active_event_title: "تخفيضات عروض الشتاء Winter Offers 2026 الحصرية",
        active_event_desc: "عروض وتخفيضات رسمية نشطة حالياً مع أكواد حصرية مخصصة للجزائر وفرنسا — الأسعار بالدينار الجزائري وفق سعر السكوار الحقيقي.",
        active_deals_kw_label: "أهم صفقات الحدث الفعال:",
        roulette_fab: "اقتراح صفقة",
        roulette_badge: "اختيار تلقائي ذكي",
        roulette_title: "صفقة مقترحة مختارة",
        roulette_subtitle: "اضغط على الزر لاقتراح صفقة نشطة بأقوى نسبة تخفيض",
        roulette_winner_tag: "صفقة مختارة",
        roulette_spin_btn: "اقتراح صفقة أخرى",
        roulette_claim_btn: "فتح رابط الشراء على AliExpress",
        roulette_shake_tip: "يمكنك هز الهاتف لاقتراح صفقة أخرى تلقائياً",
        roulette_country_label: "الدولة المطلوبة في التطبيق:",
        tools_header: "حاسبة السكوار",
        tools_modal_title: "مركز الأدوات وحاسبة السكوار",
        tools_modal_subtitle: "حاسبة السكوار الفورية للدينار الجزائري وروابط الوصول السريع للقنوات",
        calc_title: "حاسبة التحويل بسعر السكوار",
        calc_amount_foreign: "المبلغ بالدولار ($) أو اليورو (€)",
        calc_amount_dzd: "المبلغ المقابل بالدينار الجزائري (دج)",
        calc_bybit_fee: "تكلفة الشراء عبر بطاقة Bybit (رسوم 0%):",
        calc_redot_fee: "تكلفة الشراء عبر بطاقة RedotPay (رسوم ~1.2%):",
        tools_quick_links: "وصول سريع للأدوات والقنوات:",
        tools_savings_title: "إجمالي التوفير التقديري من الكوبونات:",
        tools_view_favs: "عرض المفضلة",
        channel_banner_live: "تحديثات فورية",
        channel_banner_desc: "تابع الصفقات والتخفيضات وكوبونات التخفيض الحصرية لحظة بلحظة فور نزولها في القناة.",
        channel_banner_btn: "فتح القناة في تيليجرام",
        nav_telegram: "تيليجرام",
        nav_tools: "الأدوات",
        fav_empty_title: "لا توجد صفقات محفوظة بعد",
        fav_empty_desc: "اضغط على أيقونة القلب ❤️ على أي منتج لحفظه والوصول إليه بسرعة هنا.",
        tools_coin_generator: "مولد روابط العملات 🪙",
        coin_gen_badge: "أداة مجانية فورية",
        coin_gen_title: "مولد روابط خصم العملات (Coins Deal Generator)",
        coin_gen_subtitle: "الصق رابط أي منتج من AliExpress أو نص المشاركة لتحصل فوراً على رابط تفعيل أقصى خصم للعملات (حتى 60%) وعروض السوبر ديلز!",
        coin_gen_input_label: "رابط المنتج، كود المنتج (Item ID)، أو نص المشاركة من التطبيق:",
        btn_paste: "لصق",
        btn_copy_link: "نسخ الرابط",
        btn_generate_coin_deal: "توليد رابط العملات",
        coin_gen_success: "تم تجهيز روابط الخصم بنجاح!",
        coin_link_primary_title: "رابط العملات المخفض (Coins Deal - حتى 60% خصم)",
        btn_buy_coins_deal: "فتح وشراء بالعملات",
        superdeal_link_title: "رابط السوبر ديلز (SuperDeals)",
        bundle_link_title: "عروض الحزم (Bundle Deals)",
        btn_open_deal: "فتح العرض",
        coin_gen_tip: "💡 سر الخصم: افتح رابط العملات داخل تطبيق AliExpress واضغط مباشرة على زر (شراء الآن / Acheter) أو أضف المنتج إلى السلة من نفس الصفحة لتفعيل خصم العملات الكامل بدلاً من 2% فقط!",
        tg_popup_badge: "قناة تيليجرام الرسمية 🇩🇿",
        tg_popup_title: "لا تفوّت صفقات وتخفيضات علي اكسبراس في الجزائر!",
        tg_popup_desc: "أقوى الصفقات الخارقة وكوبونات التخفيض تنفذ في دقائق معدودة! انضم إلى قناتنا على تيليجرام لتصلك تنبيهات العروض اللحظية والعملات في الجزائر مباشرة على هاتفك مجاناً.",
        tg_popup_feat1_title: "عروض سريعة وكوبونات فورية",
        tg_popup_feat1_desc: "نشر فوري للصفقات الخاطفة قبل نفاذ الكمية في الجزائر",
        tg_popup_feat2_title: "روابط خصم العملات الأقصى (Coins)",
        tg_popup_feat2_desc: "تخفيضات حقيقية تصل إلى 70% عبر روابط العملات الحصرية",
        tg_popup_feat3_title: "أسعار حقيقية بالدينار الجزائري (DZD)",
        tg_popup_feat3_desc: "حساب السعر بسعر السكوار لحظياً دون رسوم مخفية",
        tg_popup_join_cta: "انضم إلى قناة التيليجرام الآن مجاناً",
        tg_popup_france_link: "قناة عروض فرنسا (@francedealsdz)",
        tg_popup_dismiss: "لاحقاً، تصفح الموقع",
        seo_badge: "دليل المتسوق الجزائري 🇩🇿",
        seo_guide_title: "عروض وتخفيضات علي اكسبراس في الجزائر — AliExpress Deals DZ",
        seo_guide_subtitle: "بوابتك الشاملة لكل ما يخص aliexpressdz، أحدث صفقات aliexpress deals dz، وطرق الشراء من علي اكسبراس في الجزائر بأقل تكلفة وبالدينار الجزائري.",
        seo_block1_h: "أقوى عروض علي اكسبراس في الجزائر (AliExpress DZ)",
        seo_block1_p: "يقوم موقع DealScout DZ بمتابعة وتحديث عروض علي اكسبراس يومياً، بما يشمل عروض السوبر ديلز (SuperDeals)، التخفيضات الموسمية، وتجميعات المنتجات الأكثر طلباً في الجزائر مع حساب التكلفة الفعلية بالدينار الجزائري (DZD) حسب سعر صرف السكوار المحدث.",
        seo_block2_h: "طريقة الشراء من علي اكسبراس في الجزائر والدفع ببريدي موب",
        seo_block2_p: "لإتمام عملية شراء من علي اكسبراس في الجزائر، يمكنك شحن بطاقتك البنكية الدولية (مثل Bybit أو RedotPay أو Paysera) بالدينار الجزائري عبر تطبيق BaridiMob من خلال منصات P2P المعتمدة (Binance P2P)، ثم طلب المنتجات مباشرة مع التوصيل إلى مكتب بريد الجزائر الأقرب إليك.",
        seo_block3_h: "تخفيض عملات وكوبونات علي اكسبراس الجزائر (Coins & Coupons)",
        seo_block3_p: "استفد من أداة توليد روابط العملات الحصرية على موقعنا لتحويل أي رابط منتج إلى رابط خصم العملات الأقصى (Coins Discount) لتوفير ما يصل إلى 70% من السعر، بالإضافة إلى نسخ أكواد الخصم والبرومو كود الترويجية الفعالة فور صدورها.",
        seo_block4_h: "قناة التيليجرام لعروض علي اكسبراس في الجزائر",
        seo_block4_p: "الهدف الرئيسي من منصتنا هو إيصال أفضل التخفيضات إليك في الثواني الأولى. نظراً لأن الصفقات القوية تنفد كمياتها بسرعة، ننصحك بالانضمام فوراً إلى قناة التيليجرام الرسمية (@DzAliexpress0) لتصلك الإشعارات اللحظية بروابط الشراء المباشرة.",
        seo_block4_btn: "انضم لقناة صفقات الجزائر (@DzAliexpress0)",
        seo_tags_title: "الكلمات الأكثر بحثاً في الجزائر:",
        geo_badge: "ملخص الذكاء الاصطناعي والإجابات المباشرة (AI Overview & GEO)",
        geo_summary_title: "حقائق سريعة لـ DealScout DZ والمحركات الذكية",
        geo_fact_currency_title: "العملة وأسعار الصرف:",
        geo_fact_currency_desc: "الدينار الجزائري (DZD) محسوب بسعر السكوار اللحظي (SquareAlgerie.com).",
        geo_fact_payment_title: "طريقة الدفع الرسمية:",
        geo_fact_payment_desc: "BaridiMob / CCP ← منصة Binance P2P ← بطاقة Bybit ماستركارد أو RedotPay.",
        geo_fact_shipping_title: "التوصيل والاستلام:",
        geo_fact_shipping_desc: "بريد الجزائر (Algérie Poste / EMS)، إعفاء تام للطرود الشخصية غير التجارية.",
        geo_fact_coins_title: "أداة العملات (Coins):",
        geo_fact_coins_desc: "مولد روابط مجاني لتفعيل خصم 50% إلى 70% بدلاً من 2% القياسية.",
        nav_tracking: "تتبع الطرود",
        tracking_badge: "خدمة تتبع الطرود المجانية 🇩🇿",
        tracking_hero_title: "تتبع طرود AliExpress وبريد الجزائر (Suivi de Colis)",
        tracking_hero_desc: "أدخل رقم تتبع طردك من AliExpress (سواء كان Cainiao أو Choice أو SunYou أو Yanwen أو بريد الجزائر) لمتابعة مسار شحنتك لحظة بلحظة حتى وصولها إلى مكتب بريد بلديتك.",
        tracking_supported_carriers: "يدعم جميع شركات الشحن:",
        tracking_input_label: "أدخل رقم التتبع (Tracking Number) أو الصق رسالة التأكيد:",
        btn_track_parcel: "تتبع الطرد الآن",
        tracking_quick_examples: "جرب أرقام تتبع شائعة:",
        tracking_label_number: "رقم الطرد:",
        tracking_est_label: "المدة التقديرية للوصول:",
        tracking_stages_title: "مراحل شحن وتوصيل الطرد في الجزائر:",
        tracking_portals_heading: "تتبع الشحنة مباشرة على المنصات الرسمية بنقرة واحدة:",
        tracking_timeline_title: "سجل المحطات ونقاط الفرز (Live Checkpoints):",
        tracking_embed_title: "التتبع التفاعلي المباشر (17TRACK Universal Embed):",
        track_card1_title: "كم يستغرق وصول الطرد؟",
        track_card1_desc: "تستغرق شحنات AliExpress Choice حوالي 14 إلى 25 يوماً للوصول إلى الجزائر، بينما الشحن الاقتصادي العادي يستغرق بين 25 و35 يوماً عبر بريد الجزائر.",
        track_card2_title: "الجمارك الجزائرية والضرائب",
        track_card2_desc: "الطرود البريدية الموجهة للاستعمال الشخصي والعائلي معفاة تماماً من الرسوم الجمركية. تجنب طلب أكثر من 3 قطع من نفس السلعة في شحنة واحدة لتفادي الصفة التجارية.",
        track_card3_title: "استلام الطرد من مكتب البريد",
        track_card3_desc: "بمجرد وصول الطرد لمكتب بريد بلديتك، ستتلقى رسالة SMS أو إشعار Avis de passage. توجه إلى المكتب مصحوباً ببطاقة التعريف الوطنية ودفع الرسم الرمزي (130-250 دج)."
      },
      fr: {
        meta_title: "DealScout DZ — Bons Plans & Promo AliExpress Algérie | AliExpress Deals DZ",
        meta_desc: "Portail n°1 des offres aliexpressdz et bons plans AliExpress en Algérie (AliExpress Deals DZ). Guide d'achat sur AliExpress en Algérie avec BaridiMob, réductions pièces (coins) et canal Telegram officiel.",
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
        country_filter_label: "Filtrer par pays :",
        country_all: "Tous les pays 🌍",
        sort_label: "Trier :",
        sort_newest: "Plus récents 🕒",
        sort_price_asc: "Prix croissant 📉",
        sort_price_desc: "Prix décroissant 📈",
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
        cards_redot_badge: "5$ de Bienvenue Offerts",
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
        cards_faq_badge: "FAQ Cartes & Recharges",
        cards_faq_title: "Questions fréquentes sur les cartes et le paiement en Algérie",
        cards_faq_q1: "La carte Bybit est-elle vraiment gratuite et sans abonnement ?",
        cards_faq_a1: "Oui, la MasterCard Bybit virtuelle est 100% gratuite : 0 frais de création, 0 abonnement mensuel ou annuel. Compatible AliExpress et PayPal avec jusqu'à 10% de cashback.",
        cards_faq_q2: "Comment recharger Bybit ou RedotPay avec BaridiMob ?",
        cards_faq_a2: "La recharge s'effectue via Binance P2P : achetez des USDT en payant par BaridiMob ou CCP auprès de vendeurs algériens vérifiés, puis transférez vos fonds vers RedotPay ou Bybit en quelques secondes via le réseau BSC/TRC20.",
        cards_faq_q3: "Les cartes RedotPay et Bybit sont-elles compatibles avec PayPal Algérie ?",
        cards_faq_a3: "Oui, les deux cartes s'associent parfaitement avec un compte PayPal algérien ou international. Le code de confirmation à 4 chiffres apparaît instantanément dans l'application de la carte.",
        cards_faq_q4: "Quel est le code promo pour recevoir 5$ offerts sur RedotPay ?",
        cards_faq_a4: "Lors de votre inscription sur RedotPay, renseignez le code de parrainage djbt3 pour recevoir immédiatement 5$ de bonus de bienvenue dès la validation de votre pièce d'identité.",
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
        faq_q6: "Comment acheter sur AliExpress avec l'application BaridiMob ?",
        faq_a6: "AliExpress n'accepte pas directement les paiements en Dinars ou via la carte Edahabia. La méthode consiste à acheter des USDT en Dinars sur Binance P2P via BaridiMob auprès d'un marchand vérifié, puis à transférer ces fonds vers une carte Bybit gratuite ou RedotPay pour régler instantanément vos commandes.",
        faq_q7: "Quelles sont les règles douanières algériennes et les articles interdits ?",
        faq_a7: "Les colis pour usage personnel sont exonérés de taxes douanières. Ne commandez pas de quantités commerciales d'un même article pour éviter le blocage en douane. Sont strictement interdits : les drones de toutes catégories, les micro-caméras d'espionnage dissimulées, les talkies-walkies non agréés et les pointeurs laser puissants.",
        faq_q8: "Comment obtenir la réduction maximale en pièces Coins (jusqu'à 70%) ?",
        faq_a8: "En navigation standard, AliExpress ne déduit que 1% à 5% en pièces. En passant par notre générateur de liens de pièces ou le bot @Alilo07BOT, un lien optimisé sourceType=620 est généré, permettant d'absorber jusqu'à 50% voire 70% du prix directement dans la section Pièces !",
        faq_q9: "Comment renseigner son adresse postale et son code postal en Algérie ?",
        faq_a9: "Indiquez votre nom exact selon votre carte d'identité et votre numéro de mobile algérien pour recevoir le SMS du facteur. Le code postal comporte 5 chiffres (les 2 premiers pour la wilaya et les 3 suivants pour le bureau distributeur de votre commune).",
        cards_post_badge: "Guide Expédition & Douane en Algérie 2026",
        cards_post_title: "Format d'adresse, réglementation douanière et retrait à Algérie Poste",
        cards_addr_h: "1. Code Postal & Coordonnées",
        cards_addr_p: "Indiquez votre nom officiel et numéro mobile. Renseignez le code postal précis à 5 chiffres de votre commune pour un acheminement direct sans erreur de tri.",
        cards_customs_h: "2. Douane & Colis Personnels",
        cards_customs_p: "Usage personnel exonéré de taxe. Évitez les lots commerciaux identiques. Drones, caméras espion et talkies-walkies sont strictement interdits d'importation.",
        cards_pickup_h: "3. Suivi & Retrait à la Poste",
        cards_pickup_p: "Suivez votre colis sur 17TRACK et Algérie Poste. Dès réception du SMS ou de l'avis de passage, retirez votre colis au guichet avec votre CNI et acquittez les droits de timbre (~130 à 250 DZD).",
        cards_crosslink_heading: "Découvrez les autres sections :",
        crosslink_cards_title: "Guide Cartes & BaridiMob",
        crosslink_cards_sub: "Bybit gratuite & RedotPay",
        crosslink_coins_title: "Générateur Réduction Coins",
        crosslink_coins_sub: "Jusqu'à 70% de remise",
        crosslink_faq_title: "FAQ & Réglementation Douane",
        crosslink_faq_sub: "Livraison & Retrait Poste",
        coins_steps_section_title: "Méthode pour activer la réduction Coins étape par étape 🪙",
        coins_steps_section_sub: "Suivez ces instructions pour convertir n'importe quel lien produit en lien méga-réduction :",
        coins_crosslink_heading: "Explorer également DealScout DZ :",
        faq_crosslink_heading: "Thématiques associées :",
        contact_title: "Contact & Assistance",
        contact_subtitle: "L'équipe DealScout DZ est à votre disposition pour vos suggestions, signalements de liens ou partenariats.",
        contact_tg_title: "Groupe d'entraide & discussions Telegram",
        contact_tg_desc: "Échangez directement avec l'équipe et les membres dans le groupe de discussion attaché au canal officiel. Posez vos questions, demandez des avis sur un produit ou suivez les alertes en direct.",
        contact_tg_btn_admin: "Groupe de discussion & entraide (@DzAliexpress0)",
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
        footer_back_top: "Haut de page",
        active_event_badge: "Événement Promo Actif",
        active_event_title: "Promotions Offres d'Hiver 2026 (Winter Offers)",
        active_event_desc: "Bons plans et réductions officielles avec codes promo exclusifs pour l'Algérie et la France — calculés en Dinar Algérien au taux Square.",
        active_deals_kw_label: "Top deals de l'événement :",
        roulette_fab: "Deal du Jour",
        roulette_badge: "Sélection Intelligente",
        roulette_title: "Offre Recommandée",
        roulette_subtitle: "Découvrez une sélection exclusive parmi les meilleures réductions du moment",
        roulette_winner_tag: "Offre Sélectionnée",
        roulette_spin_btn: "Suggérer une autre offre",
        roulette_claim_btn: "Ouvrir le deal sur AliExpress",
        roulette_shake_tip: "Secouez votre téléphone pour afficher une nouvelle offre",
        roulette_country_label: "Pays à choisir dans l'application :",
        tools_header: "Calculateur",
        tools_modal_title: "Outils & Calculateur Square",
        tools_modal_subtitle: "Calculateur instantané en Dinar et accès direct aux canaux",
        calc_title: "Calculateur Taux Square",
        calc_amount_foreign: "Montant en Dollar ($) ou Euro (€)",
        calc_amount_dzd: "Équivalent en Dinar Algérien (DZD)",
        calc_bybit_fee: "Paiement via carte Bybit (0% frais) :",
        calc_redot_fee: "Paiement via carte RedotPay (~1.2% frais) :",
        tools_quick_links: "Accès rapide aux canaux et outils :",
        tools_savings_title: "Économies totales estimées grâce aux coupons :",
        tools_view_favs: "Voir les favoris",
        channel_banner_live: "En direct",
        channel_banner_desc: "Retrouvez tous les bons plans, promotions et coupons exclusifs dès leur parution.",
        channel_banner_btn: "Ouvrir le canal Telegram",
        nav_telegram: "Telegram",
        nav_tools: "Outils",
        fav_empty_title: "Aucun favori enregistré",
        fav_empty_desc: "Cliquez sur l'icône cœur ❤️ d'un produit pour l'enregistrer ici.",
        tools_coin_generator: "Générateur Liens Pièces 🪙",
        coin_gen_badge: "Outil Gratuit & Instantané",
        coin_gen_title: "Générateur de Réduction Pièces (Coins)",
        coin_gen_subtitle: "Collez le lien d'un produit AliExpress pour obtenir instantanément votre lien maximisant la réduction Pièces (Coins jusqu'à 60%) et SuperDeals !",
        coin_gen_input_label: "Lien produit, Item ID ou texte partagé de l'application :",
        btn_paste: "Coller",
        btn_copy_link: "Copier le lien",
        btn_generate_coin_deal: "Générer le lien Pièces",
        coin_gen_success: "Liens de réduction générés avec succès !",
        coin_link_primary_title: "Lien Réduction Pièces (Coins Deal - jusqu'à 60%)",
        btn_buy_coins_deal: "Acheter avec les Pièces",
        superdeal_link_title: "Ventes Flash (SuperDeals)",
        bundle_link_title: "Offres Groupées (Bundle Deals)",
        coin_gen_tip: "💡 Astuce Réduction : Ouvrez le lien Pièces dans l'application AliExpress et cliquez directement sur (Acheter maintenant) ou ajoutez au panier depuis cette page pour débloquer la réduction maximale en pièces !",
        tg_popup_badge: "Canal Telegram Officiel 🇩🇿",
        tg_popup_title: "Ne ratez aucun bon plan AliExpress en Algérie !",
        tg_popup_desc: "Les meilleures ventes flash et codes promo expirent en quelques minutes ! Rejoignez notre canal Telegram pour recevoir les alertes des deals et pièces en Algérie directement sur votre smartphone.",
        tg_popup_feat1_title: "Bons plans flash & coupons en direct",
        tg_popup_feat1_desc: "Diffusion instantanée des offres exclusives avant rupture de stock",
        tg_popup_feat2_title: "Réduction Pièces maximale (Coins)",
        tg_popup_feat2_desc: "Jusqu'à 70% de remise réelle grâce aux liens Pièces exclusifs",
        tg_popup_feat3_title: "Prix réels en Dinars Algériens (DZD)",
        tg_popup_feat3_desc: "Calcul au taux réel du Square sans frais cachés",
        tg_popup_join_cta: "Rejoindre le canal Telegram gratuitement",
        tg_popup_france_link: "Canal Bons Plans France (@francedealsdz)",
        tg_popup_dismiss: "Plus tard, continuer la navigation",
        seo_badge: "Guide Shopping Algérie 🇩🇿",
        seo_guide_title: "Bons Plans & Promotions AliExpress en Algérie — AliExpress Deals DZ",
        seo_guide_subtitle: "Votre référence pour tout ce qui concerne aliexpressdz, les offres aliexpress deals dz, et le guide complet pour acheter sur AliExpress en Algérie au meilleur prix en Dinar.",
        seo_block1_h: "Meilleures offres AliExpress en Algérie (AliExpress DZ)",
        seo_block1_p: "DealScout DZ sélectionne et met à jour en continu les meilleures offres AliExpress : SuperDeals, ventes flash, et promotions saisonnières avec conversion automatique en Dinar Algérien (DZD) selon le taux de change réel du Square.",
        seo_block2_h: "Comment acheter sur AliExpress depuis l'Algérie avec BaridiMob",
        seo_block2_p: "Pour commander sur AliExpress depuis l'Algérie, vous pouvez recharger vos cartes bancaires internationales (Bybit, RedotPay, Paysera) en dinars via BaridiMob sur Binance P2P, puis vous faire livrer directement au bureau d'Algérie Poste le plus proche.",
        seo_block3_h: "Réductions Pièces et Coupons Promo AliExpress Algérie",
        seo_block3_p: "Utilisez notre générateur de liens Pièces gratuit pour débloquer jusqu'à 70% de remise sur vos articles favoris et copiez les codes promo actifs pour réduire le montant de votre panier.",
        seo_block4_h: "Rejoignez le canal Telegram des bons plans en Algérie",
        seo_block4_p: "Le but principal de notre plateforme est de vous transmettre les meilleures offres en quelques secondes. Les stocks étant limités, rejoignez le canal Telegram officiel (@DzAliexpress0) pour être alerté immédiatement.",
        seo_block4_btn: "Rejoindre le canal Telegram (@DzAliexpress0)",
        seo_tags_title: "Recherches populaires en Algérie :",
        geo_badge: "Fiche Synthèse IA & Moteurs Génératifs (GEO)",
        geo_summary_title: "Faits Rapides & Données Clés DealScout DZ",
        geo_fact_currency_title: "Devise & Taux Réel :",
        geo_fact_currency_desc: "Dinar Algérien (DZD) indexé au taux parallèle réel du Square (SquareAlgerie.com).",
        geo_fact_payment_title: "Moyen de Paiement :",
        geo_fact_payment_desc: "BaridiMob / CCP → Binance P2P → Carte Bybit Mastercard ou RedotPay Visa.",
        geo_fact_shipping_title: "Livraison & Douanes :",
        geo_fact_shipping_desc: "Algérie Poste (15-28 jours), exonération totale pour colis personnels non commerciaux.",
        geo_fact_coins_title: "Outil Pièces (Coins) :",
        geo_fact_coins_desc: "Générateur gratuit activant 50% à 70% de réduction au lieu de 2% standard.",
        nav_tracking: "Suivi Colis",
        tracking_badge: "Outil Gratuit de Suivi 🇩🇿",
        tracking_hero_title: "Suivi de Colis AliExpress & Algérie Poste (Suivi DZ)",
        tracking_hero_desc: "Entrez le numéro de suivi de votre commande AliExpress (Cainiao, Choice, SunYou, Yanwen ou Algérie Poste) pour suivre l'acheminement en temps réel jusqu'à votre bureau de poste.",
        tracking_supported_carriers: "Transporteurs pris en charge :",
        tracking_input_label: "Entrez le numéro de suivi ou collez la référence :",
        btn_track_parcel: "Suivre le colis maintenant",
        tracking_quick_examples: "Exemples de numéros :",
        tracking_label_number: "Numéro de colis :",
        tracking_est_label: "Délai estimé d'arrivée :",
        tracking_stages_title: "Étapes de livraison du colis en Algérie :",
        tracking_portals_heading: "Suivi direct sur les plateformes officielles :",
        tracking_timeline_title: "Historique des points de tri (Live Checkpoints) :",
        tracking_embed_title: "Widget interactif universel (17TRACK Embed) :",
        track_card1_title: "Combien de temps prend la livraison ?",
        track_card1_desc: "Les colis AliExpress Choice mettent entre 14 et 25 jours pour arriver en Algérie, tandis que les envois économiques prennent 25 à 35 jours.",
        track_card2_title: "Douanes algériennes et taxes",
        track_card2_desc: "Les colis à usage personnel ou familial sont totalement exonérés de droits de douane. Évitez de commander plus de 3 pièces identiques par envoi.",
        track_card3_title: "Retrait au bureau de poste",
        track_card3_desc: "Dès l'arrivée au bureau de poste local, vous recevrez un SMS ou avis de passage. Présentez votre carte nationale d'identité et réglez la taxe postale symbolique (130-250 DZD)."
      }
    };

    // ── Safe LocalStorage Wrappers (Protects Private/Safari/WebView Browsers)
    function getStoredItem(key, fallback = null) {
      try {
        const val = localStorage.getItem(key);
        return val !== null ? val : fallback;
      } catch (e) {
        return fallback;
      }
    }

    function setStoredItem(key, val) {
      try {
        localStorage.setItem(key, val);
      } catch (e) {}
    }

    // ── Global State ────────────────────────────────────────────────
    var currentTheme = (getStoredItem('dealscout_theme') === 'light') ? 'light' : 'dark';
    var currentLang = (getStoredItem('dealscout_lang') === 'fr') ? 'fr' : 'ar';
    var currentPageId = 'deals';
    var allDeals = [];
    var currentChannel = '@DzAliexpress0';
    var currentCategory = 'all';
    var currentCountryFilter = 'all';
    var currentDealSort = 'newest';
    var currentCurrency = currentLang === 'fr' ? 'EUR' : 'DZD';
    var currentViewMode = 'grid';
    var usdtRate = 256.9;
    var currentSearchTerm = '';
    var currentActiveDeal = null;
    var currentActiveEvent = null;

    function fallbackCopyText(text) {
      return new Promise((resolve, reject) => {
        try {
          const textArea = document.createElement("textarea");
          textArea.value = text;
          textArea.style.position = "fixed";
          textArea.style.top = "-9999px";
          textArea.style.left = "-9999px";
          textArea.style.opacity = "0";
          document.body.appendChild(textArea);
          textArea.focus();
          textArea.select();
          const successful = document.execCommand('copy');
          document.body.removeChild(textArea);
          if (successful) resolve();
          else reject(new Error('execCommand failed'));
        } catch (err) {
          reject(err);
        }
      });
    }

    function copyTextToClipboard(text) {
      if (navigator.clipboard && window.isSecureContext) {
        return navigator.clipboard.writeText(text).catch(() => {
          return fallbackCopyText(text);
        });
      } else {
        return fallbackCopyText(text);
      }
    }

    function t(key, fallback = '') {
      const dict = (typeof I18N !== 'undefined' && I18N[currentLang]) ? I18N[currentLang] : (typeof I18N !== 'undefined' ? I18N.ar : {});
      return (dict && dict[key]) || fallback || '';
    }

    // ── Theme Engine (Light / Dark) ─────────────────────────────────
    function applyTheme(theme) {
      currentTheme = theme;
      setStoredItem('dealscout_theme', theme);
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
      const toggleBtn = document.getElementById('theme-toggle-btn');
      
      if (icon) {
        icon.className = isDark ? 'fa-solid fa-sun text-[11px] text-amber-500' : 'fa-solid fa-moon text-[11px] text-indigo-400';
      }
      if (text) {
        text.textContent = isDark 
          ? (I18N[currentLang] ? I18N[currentLang].theme_light : 'فاتح')
          : (I18N[currentLang] ? I18N[currentLang].theme_dark : 'داكن');
      }
      if (toggleBtn) {
        toggleBtn.setAttribute('title', isDark ? (currentLang === 'fr' ? 'Passer au mode clair' : 'تفعيل الوضع الفاتح') : (currentLang === 'fr' ? 'Passer au mode sombre' : 'تفعيل الوضع الداكن'));
        toggleBtn.setAttribute('aria-label', isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode');
      }
    }

    function toggleTheme() {
      const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
      applyTheme(nextTheme);
    }

    // ── Internationalization Engine ─────────────────────────────────
    function setLanguage(lang) {
      if (!I18N[lang]) lang = 'ar';
      currentLang = lang;
      setStoredItem('dealscout_lang', lang);

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

      applyTheme(currentTheme);
      showPage(currentPageId, false);

      if (currentActiveEvent) {
        updateActiveEventBanner(currentActiveEvent);
      }

      if (allDeals && allDeals.length > 0) {
        filterDeals();
      }
    }

    // ── Multi-Page Navigation Router & Dynamic SEO ──────────────────
    function showPage(pageId, updateHistory = true) {
      const pages = ['deals', 'tracking', 'cards', 'coins', 'faq', 'contact', 'about'];
      if (!pages.includes(pageId)) pageId = 'deals';
      currentPageId = pageId;

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

      // Update Dynamic SEO Metadata for Search Engines and Social Cards
      const isFr = currentLang === 'fr';
      let pageTitle = (I18N[currentLang] && I18N[currentLang].meta_title) || document.title;
      let pageDesc = (I18N[currentLang] && I18N[currentLang].meta_desc) || '';

      if (pageId === 'tracking') {
        renderRecentTrackingList();
        pageTitle = isFr
          ? "Suivi de Colis AliExpress Algérie & Algérie Poste | DealScout DZ"
          : "تتبع طرود AliExpress وبريد الجزائر (Suivi de Colis DZ) | DealScout DZ";
        pageDesc = isFr
          ? "Suivi gratuit en direct de vos colis AliExpress Choice, Cainiao, et Algérie Poste avec étapes de livraison et dédouanement."
          : "أداة مجانية لتتبع طرود علي إكسبرس (Cainiao, Algérie Poste, SunYou) لحظة بلحظة حتى الاستلام في مكتب البريد الجزائري.";
      } else if (pageId === 'cards') {
        pageTitle = isFr
          ? "Cartes Bancaires & BaridiMob pour AliExpress en Algérie — Bybit, RedotPay, Binance P2P | DealScout DZ"
          : "بطاقات الشراء من AliExpress بالدينار الجزائري — Bybit, RedotPay, بريدي موب Binance P2P | DealScout DZ";
        pageDesc = isFr
          ? "Guide complet pour acheter sur AliExpress depuis l'Algérie avec BaridiMob via Binance P2P. Cartes virtuelles Bybit MasterCard gratuite et RedotPay Visa avec 5$ offerts."
          : "دليل شامل لشراء وشحن بطاقات فيزا وماستركارد الدولية الافتراضية (Bybit, RedotPay) بالدينار الجزائري عبر بريدي موب ومنصة بينانس للتسوق من AliExpress.";
      } else if (pageId === 'coins') {
        pageTitle = isFr
          ? "Bot Pièces AliExpress @Alilo07BOT — Réduction Maximale Coins | DealScout DZ"
          : "بوت عملات علي اكسبرس @Alilo07BOT — أقصى خصم Coins | DealScout DZ";
      } else if (pageId === 'faq') {
        pageTitle = isFr
          ? "FAQ & Guide d'Achat AliExpress en Algérie | DealScout DZ"
          : "الأسئلة الشائعة ودليل الشراء من علي اكسبرس في الجزائر | DealScout DZ";
      } else if (pageId === 'contact') {
        pageTitle = isFr
          ? "Contact & Assistance | DealScout DZ"
          : "اتصل بنا والدعم الفني | DealScout DZ";
      } else if (pageId === 'about') {
        pageTitle = isFr
          ? "À Propos de DealScout DZ — Cours Square & Bons Plans"
          : "من نحن — DealScout DZ ومنصة صفقات الجزائر";
      }

      document.title = pageTitle;
      const metaDescEl = document.querySelector('meta[name="description"]');
      if (metaDescEl) metaDescEl.content = pageDesc;
      const ogTitleEl = document.querySelector('meta[property="og:title"]');
      if (ogTitleEl) ogTitleEl.content = pageTitle;
      const ogDescEl = document.querySelector('meta[property="og:description"]');
      if (ogDescEl) ogDescEl.content = pageDesc;

      // Sync URL routing without page refresh
      if (updateHistory && window.history && window.history.pushState) {
        const newPath = pageId === 'deals' ? '/' : '/' + pageId;
        if (window.location.pathname !== newPath && window.location.hash !== ('#' + pageId)) {
          try {
            history.pushState({ page: pageId }, '', newPath);
          } catch(e) {}
        }
      }

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

    let toastTimer = null;
    function showToast(message) {
      const toast = document.getElementById('toast');
      const msg = document.getElementById('toast-msg');
      if (!toast || !msg) return;
      msg.textContent = message;
      if (toastTimer) clearTimeout(toastTimer);
      toast.classList.remove('translate-y-16', 'opacity-0');
      toastTimer = setTimeout(() => {
        toast.classList.add('translate-y-16', 'opacity-0');
      }, 2000);
    }

    // ── Confetti & Haptic Feedback Engine ───────────────────────────
    function triggerHaptic(pattern = [15, 30, 15]) {
      try {
        if (window.navigator && typeof window.navigator.vibrate === 'function') {
          window.navigator.vibrate(pattern);
        }
      } catch (e) {}
    }

    let confettiParticles = [];
    let confettiAnimId = null;

    function fireConfetti(sourceEl = null) {
      const canvas = document.getElementById('confetti-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      if (!ctx) return;

      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      canvas.style.display = 'block';

      let originX = canvas.width / 2;
      let originY = canvas.height * 0.45;

      if (sourceEl && typeof sourceEl.getBoundingClientRect === 'function') {
        const rect = sourceEl.getBoundingClientRect();
        originX = rect.left + rect.width / 2;
        originY = rect.top + rect.height / 2;
      }

      const colors = ['#e11d48', '#f59e0b', '#10b981', '#38bdf8', '#a855f7', '#fbbf24', '#ffffff'];
      confettiParticles = [];
      const particleCount = 42;

      for (let i = 0; i < particleCount; i++) {
        const angle = Math.random() * Math.PI * 2;
        const velocity = 4 + Math.random() * 8;
        confettiParticles.push({
          x: originX,
          y: originY,
          vx: Math.cos(angle) * velocity,
          vy: Math.sin(angle) * velocity - 3,
          size: 4 + Math.random() * 5,
          color: colors[Math.floor(Math.random() * colors.length)],
          rotation: Math.random() * 360,
          rotSpeed: (Math.random() - 0.5) * 12,
          opacity: 1,
          decay: 0.015 + Math.random() * 0.02
        });
      }

      if (confettiAnimId) cancelAnimationFrame(confettiAnimId);

      function render() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        let alive = 0;

        for (let i = 0; i < confettiParticles.length; i++) {
          const p = confettiParticles[i];
          if (p.opacity <= 0) continue;
          alive++;
          p.x += p.vx;
          p.y += p.vy;
          p.vy += 0.28;
          p.vx *= 0.98;
          p.rotation += p.rotSpeed;
          p.opacity -= p.decay;

          ctx.save();
          ctx.translate(p.x, p.y);
          ctx.rotate((p.rotation * Math.PI) / 180);
          ctx.globalAlpha = Math.max(0, p.opacity);
          ctx.fillStyle = p.color;
          ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 0.7);
          ctx.restore();
        }

        if (alive > 0) {
          confettiAnimId = requestAnimationFrame(render);
        } else {
          canvas.style.display = 'none';
          confettiAnimId = null;
        }
      }

      confettiAnimId = requestAnimationFrame(render);
    }

    // ── Shopping Tools Hub & Favorites Store ────────────────────────
    function getGameState() {
      const raw = getStoredItem('dealscout_user_state', null) || getStoredItem('dealscout_game_state', null);
      if (raw) {
        try {
          const parsed = JSON.parse(raw);
          if (parsed && typeof parsed.saved_dzd === 'number') {
            if (!Array.isArray(parsed.favs)) parsed.favs = [];
            return parsed;
          }
        } catch (e) {}
      }
      return {
        saved_dzd: 4800,
        favs: []
      };
    }

    function saveGameState(state) {
      setStoredItem('dealscout_user_state', JSON.stringify(state));
      updateGamificationBadges(state);
    }

    function addSavedDZD(amount) {
      const state = getGameState();
      state.saved_dzd = (state.saved_dzd || 0) + amount;
      saveGameState(state);
    }

    function updateGamificationBadges(state = null) {
      if (!state) state = getGameState();
      const favBadge = document.getElementById('mob-fav-badge');
      const countFavs = document.getElementById('count-favs');
      const favCount = (state.favs || []).length;
      if (favBadge) {
        favBadge.textContent = favCount;
        if (favCount > 0) {
          favBadge.classList.remove('hidden');
          favBadge.classList.add('flex');
        } else {
          favBadge.classList.add('hidden');
          favBadge.classList.remove('flex');
        }
      }
      if (countFavs) {
        countFavs.textContent = favCount;
      }
    }

    // ── Live Square Dinar Converter Handlers ────────────────────────
    function onCalcForeignChange(val) {
      const amount = parseFloat(val);
      const dzdInput = document.getElementById('calc-dzd-input');
      const bybitEl = document.getElementById('calc-bybit-total');
      const redotEl = document.getElementById('calc-redot-total');
      const curSym = (currentCurrency === 'EUR') ? '€' : '$';
      const symEl = document.getElementById('calc-curr-symbol');
      if (symEl) symEl.textContent = curSym;

      if (isNaN(amount) || amount <= 0) {
        if (dzdInput) dzdInput.value = '';
        if (bybitEl) bybitEl.textContent = '0 ' + I18N[currentLang].currency_dzd;
        if (redotEl) redotEl.textContent = '0 ' + I18N[currentLang].currency_dzd;
        return;
      }
      const rate = usdtRate || 256.9;
      const dzd = Math.round(amount * rate);
      if (dzdInput) dzdInput.value = dzd;
      if (bybitEl) bybitEl.textContent = dzd.toLocaleString() + ' ' + I18N[currentLang].currency_dzd;
      if (redotEl) redotEl.textContent = Math.round(dzd * 1.012).toLocaleString() + ' ' + I18N[currentLang].currency_dzd;
    }

    function onCalcDzdChange(val) {
      const dzd = parseFloat(val);
      const foreignInput = document.getElementById('calc-foreign-input');
      const bybitEl = document.getElementById('calc-bybit-total');
      const redotEl = document.getElementById('calc-redot-total');
      if (isNaN(dzd) || dzd <= 0) {
        if (foreignInput) foreignInput.value = '';
        if (bybitEl) bybitEl.textContent = '0 ' + I18N[currentLang].currency_dzd;
        if (redotEl) redotEl.textContent = '0 ' + I18N[currentLang].currency_dzd;
        return;
      }
      const rate = usdtRate || 256.9;
      const foreign = (dzd / rate).toFixed(2);
      if (foreignInput) foreignInput.value = foreign;
      if (bybitEl) bybitEl.textContent = Math.round(dzd).toLocaleString() + ' ' + I18N[currentLang].currency_dzd;
      if (redotEl) redotEl.textContent = Math.round(dzd * 1.012).toLocaleString() + ' ' + I18N[currentLang].currency_dzd;
    }

    function renderGamificationHub() {
      const state = getGameState();
      const savedEl = document.getElementById('tools-total-saved');
      const rateEl = document.getElementById('calc-usdt-rate');
      const symEl = document.getElementById('calc-curr-symbol');

      if (savedEl) savedEl.textContent = `${(state.saved_dzd || 0).toLocaleString()} ${I18N[currentLang].currency_dzd}`;
      if (rateEl) rateEl.textContent = usdtRate || '256.9';
      if (symEl) symEl.textContent = (currentCurrency === 'EUR') ? '€' : '$';

      const foreignInput = document.getElementById('calc-foreign-input');
      if (foreignInput && foreignInput.value) {
        onCalcForeignChange(foreignInput.value);
      } else if (foreignInput) {
        foreignInput.value = '20';
        onCalcForeignChange('20');
      }
    }

    function openGamificationHub() {
      renderGamificationHub();
      const modal = document.getElementById('gamification-modal');
      if (modal) {
        modal.classList.remove('hidden');
        modal.style.display = 'flex';
      }
      document.body.style.overflow = 'hidden';
    }

    function closeGamificationHub() {
      const modal = document.getElementById('gamification-modal');
      if (modal) {
        modal.classList.add('hidden');
        modal.style.display = 'none';
      }
      document.body.style.overflow = '';
    }

    function onGamificationBackdropClick(e) {
      if (e.target && e.target.id === 'gamification-modal') {
        closeGamificationHub();
      }
    }

    // ── Favorites / Bookmarks Engine ────────────────────────────────
    function isFavorite(dealId) {
      const state = getGameState();
      return Array.isArray(state.favs) && state.favs.includes(dealId);
    }

    function toggleFavorite(dealId, event) {
      if (event) {
        try { event.stopPropagation(); } catch (e) {}
      }
      const state = getGameState();
      if (!Array.isArray(state.favs)) state.favs = [];
      const idx = state.favs.indexOf(dealId);
      const isAdding = (idx === -1);

      if (isAdding) {
        state.favs.push(dealId);
        triggerHaptic([20]);
        showToast(currentLang === 'fr' ? 'Ajouté aux favoris ❤️' : 'تم الحفظ في المفضلة ❤️');
      } else {
        state.favs.splice(idx, 1);
        triggerHaptic([10]);
        showToast(currentLang === 'fr' ? 'Retiré des favoris' : 'تمت الإزالة من المفضلة');
      }
      saveGameState(state);

      // Animate heart icon on the card
      const icon = document.getElementById('fav-icon-' + dealId);
      if (icon) {
        if (isAdding) {
          icon.className = 'fa-solid fa-heart text-rose-500 text-xs animate-heart-pop';
        } else {
          icon.className = 'fa-regular fa-heart text-white/90 text-xs animate-heart-pop';
        }
      }

      if (currentCategory === 'favs') {
        filterDeals();
      }
    }

    function filterByFavoritesMobile() {
      showPage('deals');
      setCategory('favs');
    }

    // ── Deal Roulette Engine ("صفقة الحظ 🎲") ──────────────────────
    let isSpinningRoulette = false;

    function openRouletteModal() {
      const modal = document.getElementById('roulette-modal');
      if (modal) {
        modal.classList.remove('hidden');
        modal.style.display = 'flex';
      }
      document.body.style.overflow = 'hidden';

      // Set initial preview if available
      if (allDeals && allDeals.length > 0) {
        const randomInitial = allDeals[Math.floor(Math.random() * allDeals.length)];
        displayRouletteDeal(randomInitial, false);
      }
    }

    function closeRouletteModal() {
      if (isSpinningRoulette) return;
      const modal = document.getElementById('roulette-modal');
      if (modal) {
        modal.classList.add('hidden');
        modal.style.display = 'none';
      }
      document.body.style.overflow = '';
    }

    function onRouletteBackdropClick(e) {
      if (e.target && e.target.id === 'roulette-modal') {
        closeRouletteModal();
      }
    }

    function displayRouletteDeal(deal, isWinner = false) {
      if (!deal) return;
      const img = document.getElementById('roulette-img');
      const title = document.getElementById('roulette-deal-title');
      const cat = document.getElementById('roulette-cat');
      const price = document.getElementById('roulette-price');
      const coupon = document.getElementById('roulette-coupon-pill');
      const winnerTag = document.getElementById('roulette-winner-tag');
      const buyBtn = document.getElementById('roulette-buy-btn');
      const countryText = document.getElementById('roulette-country-text');
      const countryVal = document.getElementById('roulette-country-val');

      if (img && deal.photo_url) img.src = deal.photo_url;
      if (title) title.textContent = deal.title || 'Deal AliExpress';
      if (cat) cat.textContent = deal.category_label || (I18N[currentLang].cat_all || 'صفقة');
      if (price) price.innerHTML = formatPrice(deal);
      if (coupon) {
        if (deal.coupon) {
          coupon.textContent = currentLang === 'fr' ? `Code : ${deal.coupon}` : `كود: ${deal.coupon}`;
          coupon.style.display = 'inline-block';
        } else {
          coupon.textContent = '';
          coupon.style.display = 'none';
        }
      }

      // Populate Country Indicator
      const defaultCountry = currentLang === 'fr' ? 'Algérie 🇩🇿' : 'الجزائر 🇩🇿';
      const cStr = deal.country || defaultCountry;
      if (countryText) countryText.textContent = cStr;
      if (countryVal) countryVal.textContent = cStr;

      if (winnerTag) {
        if (isWinner) winnerTag.classList.remove('hidden');
        else winnerTag.classList.add('hidden');
      }

      if (buyBtn) {
        if (isWinner && deal.affiliate_url) {
          buyBtn.href = deal.affiliate_url;
          buyBtn.style.display = 'flex';
          buyBtn.onclick = () => handleBuyClick(deal.coupon || '');
        } else {
          buyBtn.style.display = 'none';
        }
      }
    }

    function spinRoulette() {
      if (isSpinningRoulette) return;
      if (!allDeals || allDeals.length === 0) {
        showToast(currentLang === 'fr' ? 'Chargement des offres...' : 'جاري تحميل الصفقات...');
        return;
      }

      isSpinningRoulette = true;
      const spinBtn = document.getElementById('roulette-spin-btn');
      const btnText = document.getElementById('roulette-btn-text');
      const displayCard = document.getElementById('roulette-display-card');
      const winnerTag = document.getElementById('roulette-winner-tag');
      const buyBtn = document.getElementById('roulette-buy-btn');

      if (winnerTag) winnerTag.classList.add('hidden');
      if (buyBtn) buyBtn.style.display = 'none';
      if (spinBtn) spinBtn.disabled = true;
      if (btnText) btnText.textContent = currentLang === 'fr' ? 'Sélection en cours...' : 'جاري الاختيار...';
      if (displayCard) displayCard.classList.add('animate-slot-roll');

      let cycles = 0;
      const maxCycles = 16;
      let winningDeal = null;

      const interval = setInterval(() => {
        cycles++;
        const randomIndex = Math.floor(Math.random() * allDeals.length);
        const candidate = allDeals[randomIndex];
        displayRouletteDeal(candidate, false);
        triggerHaptic([10]);

        if (cycles >= maxCycles) {
          clearInterval(interval);
          isSpinningRoulette = false;
          if (displayCard) displayCard.classList.remove('animate-slot-roll');
          if (spinBtn) spinBtn.disabled = false;
          if (btnText) btnText.textContent = currentLang === 'fr' ? 'Suggérer une autre offre' : 'اقتراح صفقة أخرى';

          winningDeal = candidate;
          displayRouletteDeal(winningDeal, true);
          fireConfetti(spinBtn);
          triggerHaptic([30, 60, 30]);
        }
      }, 75);
    }

    // Mobile Shake Detection for Instant Roulette Roll
    let lastShakeTime = 0;
    let lastX = 0, lastY = 0, lastZ = 0;
    if (window.DeviceMotionEvent) {
      window.addEventListener('devicemotion', (e) => {
        const acc = e.accelerationIncludingGravity;
        if (!acc) return;
        const curTime = Date.now();
        if ((curTime - lastShakeTime) > 1200) {
          const diffTime = curTime - lastShakeTime;
          const speed = Math.abs(acc.x + acc.y + acc.z - lastX - lastY - lastZ) / diffTime * 10000;
          if (speed > 28) {
            lastShakeTime = curTime;
            triggerHaptic([25, 40]);
            openRouletteModal();
            spinRoulette();
          }
          lastX = acc.x; lastY = acc.y; lastZ = acc.z;
        }
      });
    }

    function handleBuyClick(couponCode) {
      triggerHaptic([20, 40, 20]);
      addSavedDZD(1500);
      fireConfetti();
      if (couponCode && couponCode.length >= 3) {
        copyTextToClipboard(couponCode).then(() => {
          showToast(currentLang === 'fr' ? `Code promo ${couponCode} copié !` : `تم نسخ كود الخصم ${couponCode} تلقائياً! 🚀`);
        }).catch(() => {});
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

    // ── Telegram Channel Engagement Popup (Non-Annoying & Closable) ───
    var tgPopupTimer = null;
    var tgPopupScrollHandler = null;

    function openTelegramPopup() {
      const modal = document.getElementById('telegram-modal');
      if (modal) {
        modal.classList.remove('hidden');
        modal.style.display = 'flex';
      }
      document.body.style.overflow = 'hidden';
    }

    function closeTelegramPopup(userInitiated = false) {
      if (tgPopupTimer) {
        clearTimeout(tgPopupTimer);
        tgPopupTimer = null;
      }
      if (tgPopupScrollHandler) {
        window.removeEventListener('scroll', tgPopupScrollHandler);
        tgPopupScrollHandler = null;
      }
      const modal = document.getElementById('telegram-modal');
      if (modal) {
        modal.classList.add('hidden');
        modal.style.display = 'none';
      }
      document.body.style.overflow = '';
      if (userInitiated) {
        // User explicitly closed/dismissed: respect choice for 24 hours
        setStoredItem('dealscout_tg_popup_dismissed_until', Date.now() + (24 * 60 * 60 * 1000));
      }
    }

    function onTelegramPopupBackdropClick(event) {
      if (event && event.target && event.target.id === 'telegram-modal') {
        closeTelegramPopup(true);
      }
    }

    function onTelegramPopupJoinClick() {
      // User clicked to join! Don't prompt again for 30 days
      setStoredItem('dealscout_tg_popup_dismissed_until', Date.now() + (30 * 24 * 60 * 60 * 1000));
      setTimeout(() => closeTelegramPopup(false), 300);
    }

    function initTelegramPopupTrigger() {
      const dismissedUntil = getStoredItem('dealscout_tg_popup_dismissed_until');
      if (dismissedUntil && Date.now() < parseInt(dismissedUntil, 10)) {
        return; // Respect user choice, never annoy!
      }

      let popupTriggered = false;
      function triggerPopup() {
        if (popupTriggered) return;
        popupTriggered = true;
        if (tgPopupScrollHandler) {
          window.removeEventListener('scroll', tgPopupScrollHandler);
          tgPopupScrollHandler = null;
        }

        // Avoid interrupting when a modal or lightbox is already active
        const dealModal = document.getElementById('deal-modal');
        const rouletteModal = document.getElementById('roulette-modal');
        const toolsModal = document.getElementById('gamification-modal');
        const isDealOpen = dealModal && !dealModal.classList.contains('hidden') && dealModal.style.display !== 'none';
        const isRouletteOpen = rouletteModal && !rouletteModal.classList.contains('hidden') && rouletteModal.style.display !== 'none';
        const isToolsOpen = toolsModal && !toolsModal.classList.contains('hidden') && toolsModal.style.display !== 'none';

        if (isDealOpen || isRouletteOpen || isToolsOpen) {
          // Retry later after 8 seconds
          tgPopupTimer = setTimeout(() => {
            popupTriggered = false;
            triggerPopup();
          }, 8000);
          return;
        }

        openTelegramPopup();
      }

      // Dwell trigger: after 7 seconds of browsing
      tgPopupTimer = setTimeout(triggerPopup, 7000);

      // Scroll trigger: when scrolling past 35% of page content
      tgPopupScrollHandler = function() {
        const scrollable = document.documentElement.scrollHeight - window.innerHeight;
        if (scrollable > 300 && (window.scrollY / scrollable) >= 0.35) {
          if (tgPopupTimer) clearTimeout(tgPopupTimer);
          triggerPopup();
        }
      };
      window.addEventListener('scroll', tgPopupScrollHandler, { passive: true });
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
      const bannerName = document.getElementById('channel-banner-name');
      const bannerBtn = document.getElementById('channel-banner-btn');
      const mobTg = document.getElementById('mob-bottom-tg');
      const topTg = document.getElementById('top-telegram-link');
      const tgPopupBtn = document.getElementById('tg-popup-join-btn');
      const targetUrl = isDz ? 'https://t.me/DzAliexpress0' : 'https://t.me/francedealsdz';

      if (btnJoin) btnJoin.href = targetUrl;
      if (bannerBtn) bannerBtn.href = targetUrl;
      if (mobTg) mobTg.href = targetUrl;
      if (topTg) topTg.href = targetUrl;
      if (tgPopupBtn) tgPopupBtn.href = targetUrl;

      if (isDz) {
        if (tabDz) tabDz.className = 'flex-1 sm:flex-none min-h-[40px] px-4 py-2 rounded-lg bg-crimson-600 text-white transition flex items-center justify-center gap-2 active:scale-95 shadow-sm';
        if (tabFr) tabFr.className = 'flex-1 sm:flex-none min-h-[40px] px-4 py-2 rounded-lg opacity-70 hover:opacity-100 transition flex items-center justify-center gap-2 active:scale-95';
        if (bannerName) bannerName.textContent = currentLang === 'fr' ? 'Canal Telegram Algérie (@DzAliexpress0)' : 'قناة التيليجرام الرسمية (@DzAliexpress0)';
        setCurrency('DZD');
      } else {
        if (tabFr) tabFr.className = 'flex-1 sm:flex-none min-h-[40px] px-4 py-2 rounded-lg bg-crimson-600 text-white transition flex items-center justify-center gap-2 active:scale-95 shadow-sm';
        if (tabDz) tabDz.className = 'flex-1 sm:flex-none min-h-[40px] px-4 py-2 rounded-lg opacity-70 hover:opacity-100 transition flex items-center justify-center gap-2 active:scale-95';
        if (bannerName) bannerName.textContent = currentLang === 'fr' ? 'Canal Telegram France (@francedealsdz)' : 'قناة التيليجرام — عروض فرنسا (@francedealsdz)';
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

    function setCountryFilter(country) {
      currentCountryFilter = country;
      document.querySelectorAll('.country-pill').forEach(btn => {
        btn.style.backgroundColor = 'var(--bg-card)';
        btn.style.borderColor = 'var(--border-card)';
        btn.style.color = 'var(--text-muted)';
        btn.classList.remove('font-bold');
        btn.classList.add('font-semibold');
      });
      const active = document.getElementById('country-' + country);
      if (active) {
        active.style.backgroundColor = 'var(--text-main)';
        active.style.borderColor = 'var(--text-main)';
        active.style.color = 'var(--bg-page)';
        active.classList.remove('font-semibold');
        active.classList.add('font-bold');
      }
      filterDeals();
    }

    function setDealSort(sortVal) {
      currentDealSort = sortVal;
      const select = document.getElementById('deal-sort-select');
      if (select && select.value !== sortVal) select.value = sortVal;
      filterDeals();
    }

    function handleSearchInput(term) {
      currentSearchTerm = term.trim().toLowerCase();
      const desk = document.getElementById('desktop-search');
      const mob = document.getElementById('mobile-search');
      const deskClear = document.getElementById('desktop-search-clear');
      const mobClear = document.getElementById('mobile-search-clear');
      if (desk && desk.value !== term) desk.value = term;
      if (mob && mob.value !== term) mob.value = term;
      if (deskClear) deskClear.classList.toggle('hidden', !currentSearchTerm);
      if (mobClear) mobClear.classList.toggle('hidden', !currentSearchTerm);
      filterDeals();
    }

    function resetFilters() {
      currentSearchTerm = '';
      currentCategory = 'all';
      currentCountryFilter = 'all';
      currentDealSort = 'newest';
      const desk = document.getElementById('desktop-search');
      const mob = document.getElementById('mobile-search');
      const deskClear = document.getElementById('desktop-search-clear');
      const mobClear = document.getElementById('mobile-search-clear');
      if (desk) desk.value = '';
      if (mob) mob.value = '';
      if (deskClear) deskClear.classList.add('hidden');
      if (mobClear) mobClear.classList.add('hidden');
      const sortSelect = document.getElementById('deal-sort-select');
      if (sortSelect) sortSelect.value = 'newest';
      setCountryFilter('all');
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

        if (data.active_event) {
          currentActiveEvent = data.active_event;
          updateActiveEventBanner(currentActiveEvent);
        }

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
      const urlMatch = text.match(new RegExp('https?:\\/\\/(?:s\\.click\\.aliexpress\\.com\\/e\\/[A-Za-z0-9_-]+|(?:[a-z0-9-]+\\.)?aliexpress\\.com\\/(?:item|p)\\/[A-Za-z0-9_.-]+)', 'i'));
      if (!urlMatch) {
        return null;
      }

      // 2. Strict Filter: Reject religious verses, prayers, adhkars, and spiritual reminders
      const isReligious = /(?:وَتَوَكَّلْ|وتوكل|سبحان الله|الحمد لله|الله أكبر|صلى الله|عليه وسلم|سورة|القرآن|أذكار|دعاء|تذكير ديني|استغفر الله|لا إله إلا الله|حسبي الله|اذكار)/i.test(text);
      if (isReligious) {
        return null;
      }

      // 3. Strict Filter: Reject general non-product announcements, referral posts, and payment guides
      const isAnnouncement = /(?:إعلان هام|تنبيه هام|دليل الشراء بالدينار|شحن بطاقتك|قناة الصفقات|قناة العروض|كيفاش تشري من AliExpress|كيف تشحن بطاقاتك)/i.test(text) && !text.includes('/item/');
      if (isAnnouncement) {
        return null;
      }

      // 4. Reject emoji-only or too-short posts
      const alphanumeric = text.replace(/[\\s\\p{Emoji_Presentation}\\p{Extended_Pictographic}\\p{Punctuation}]/gu, '');
      if (alphanumeric.length < 5) {
        return null;
      }

      // 5. Strict Active Promo Event Filter: Reject posts from expired campaigns
      const isExpiredEvent = /(?:OTPRD|BDQT|FRPRD|FRBD|Party Ready|Brand Day|عروض الحفلة)/i.test(text);
      const hasActiveEventCode = /(?:WOAE|FRWO|Winter Offers|عروض الشتاء)/i.test(text);
      if (isExpiredEvent && !hasActiveEventCode) {
        return null;
      }
      if (post.date && post.date < '2026-10-14' && !hasActiveEventCode) {
        return null;
      }

      let coupon = null;
      let priceUsd = null;
      let priceEur = null;
      let country = null;
      let hasCoins = false;
      let category = 'other';
      let categoryLabel = I18N[currentLang].deal_category_fallback;

      const lines = text.split(/\\r?\\n/).map(l => l.trim()).filter(Boolean);

      const countryNames = [
        'السعودية', 'سعودية', 'saudi', 'ksa', 'أستراليا', 'استراليا', 'australia',
        'كندا', 'canada', 'فرنسا', 'france', 'أوكرانيا', 'اوكرانيا', 'ukraine',
        'إسبانيا', 'اسبانيا', 'spain', 'الإمارات', 'امارات', 'uae', 'قطر', 'qatar',
        'الكويت', 'kuwait', 'البحرين', 'bahrain', 'عمان', 'oman', 'كوريا', 'korea',
        'الجزائر', 'algeria'
      ];

      const isBoilerplate = (l) => {
        if (!l) return true;
        const s = l.toLowerCase().replace(/[\u0640]/g, '').trim();
        if (countryNames.includes(s)) return true;
        if (countryNames.some(c => s === 'خلي البلد ' + c || s === 'ضع البلد ' + c || s === 'بلد الحساب ' + c)) return true;
        return (
          s.includes('http') || s.includes('@') || s.includes('t.me') ||
          s.includes('خلي البلد') || s.includes('بلد الحساب') || s.includes('ضع البلد') ||
          s.includes('livraison') || s.includes('pays') || s.includes('السعر') || s.includes('prix') ||
          s.includes('price') || s.includes('كوبون') || s.includes('قسيمة') || s.includes('code') ||
          s.includes('coupon') || s.includes('عملات') || s.includes('coins') || s.includes('pièces') ||
          s.includes('pièce') || s.includes('لافار') || s.includes('عرض اليوم') || s.includes('صفقة') ||
          s.includes('صيدة') || s.includes('باطل') || s.includes('تخفيض قوي') || s.includes('رابط الشراء') ||
          s.includes('بوت') || s.includes('قناة') || s.includes('bonne affaire') ||
          s.includes('meilleur bon plan') || s.includes('guide') || s.includes('تنبيه') ||
          s.includes('طريقة') || s.includes('احجز') || s.includes('طبقوا') || s.includes('حبات قلال') ||
          s.includes('سارعوا') || s.includes('سعر ممتاز') || s.includes('هبوط قوي') || s.includes('بخاصية') ||
          s.includes('متوسط') || s.includes('سعره') || s.includes('دج') || s.includes('صفقة اليوم') || s.includes('صيدة اليوم') ||
          countryNames.some(c => s.includes('خلي البلد ' + c) || s.includes('ضع البلد ' + c))
        );
      };

      let title = '';
      if (post.title && !isBoilerplate(post.title)) {
        title = post.title.trim();
      }

      // Priority 1: Checkmark bullet (DealScout DZ & top channels standard: ✅ [Title] or ✔️ [Title])
      if (!title) {
        for (let i = 0; i < lines.length; i++) {
          const line = lines[i];
          if (line === '✅' || line === '✔️' || line === '☑️') {
            if (i + 1 < lines.length) {
              const next = lines[i + 1].replace(/<[^>]*>/g, '').trim();
              if (next.length >= 3 && !isBoilerplate(next)) {
                title = next;
                break;
              }
            }
          }
          const m = line.match(/^[✅✔️☑️]\\s*(.+)$/) || line.match(/✅\\s*([^\\n]+)/);
          if (m) {
            const cand = m[1].replace(/<[^>]*>/g, '').replace(/^[✅✔️☑️\\s*#]+/, '').trim();
            if (cand.length >= 3 && !isBoilerplate(cand)) {
              title = cand;
              break;
            }
          }
        }
      }

      // Priority 2: Star, device, or category prefixes (⭐️, 📱, 🎮, 🎧, ⚡, 📦, تخفيض لـ, Produit)
      if (!title) {
        for (let i = 0; i < lines.length; i++) {
          const line = lines[i];
          const m = line.match(/^(?:⭐️|⭐|🌟|📱|🎮|🎧|⚡|📦|تخفيض\\s*(?:لـ|ل)?|عرض\\s*خاص\\s*(?:لـ|ل)?|تخفيض\\s*على|produit\\s*:?|offre\\s*:?)\\s*(.+)$/i);
          if (m) {
            const cand = m[1].replace(/<[^>]*>/g, '').trim();
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
          const clean = line.replace(/^[-🛍️🔥⚡⭐💥📦📍🏷️✅✔️•*\\s]+/, '').replace(/<[^>]*>/g, '').trim();
          if (clean.length >= 4 && !isBoilerplate(clean) && !clean.match(/^[A-Z0-9_-]{4,20}$/)) {
            title = clean;
            break;
          }
        }
      }

      // Priority 4: Non-link fallback line
      if (!title) {
        for (const line of lines) {
          if (!line.includes('http') && !line.includes('@') && !line.includes('t.me') && line.length >= 4 && !isBoilerplate(line)) {
            const clean = line.replace(/^[-🛍️🔥⚡⭐💥📦📍🏷️✅✔️•*\\s]+/, '').trim();
            if (clean.length >= 4 && !isBoilerplate(clean)) {
              title = clean;
              break;
            }
          }
        }
      }

      if (title && isBoilerplate(title)) {
        title = '';
      }

      if (title) {
        title = title.replace(/<[^>]*>/g, '').trim();
        if (title.length > 95) title = title.slice(0, 92) + '...';
      } else {
        title = (currentLang === 'fr' ? "Offre Spéciale Winter Offers" : "عرض مميز تخفيضات الشتاء (Winter Offers)");
      }

      const usdMatch = text.match(/(?:\\$|US\\s*\\$|USD\\s*)\\s*([0-9]+[.,][0-9]{1,2})/i) || text.match(/([0-9]+[.,][0-9]{1,2})\\s*(?:\\bUSD\\b|\\$)/i);
      if (usdMatch) {
        priceUsd = parseFloat(usdMatch[1].replace(',', '.'));
      }
      const eurMatch = text.match(/(?:€|EUR\\s*)\\s*([0-9]+[.,][0-9]{1,2})/i) || text.match(/([0-9]+[.,][0-9]{1,2})\\s*(?:€|\\bEUR\\b)/i);
      if (eurMatch) {
        priceEur = parseFloat(eurMatch[1].replace(',', '.'));
      }

      // Enhanced Multi-Coupon Extraction across all Arabic, French, and Telegram formats
      const cleanNorm = text.replace(/[\u0640]/g, '');
      const extractedCoupons = [];
      const extractedDetails = [];
      const seenCodes = new Set();
      const blCodes = ['http', 'https', 'aliexpress', 'tme', 'link', 'item', 'click', 'coins', 'bot', 'france', 'canada', 'algerie', 'promo', 'reduction', 'code', 'camera', 'battery'];
      const compBrands = ['anis', 'bnd', 'zed', 'lody', 'ecks', 'megaprix', 'megaphonna', 'cp4dz', 'francecp'];

      function addParsedCode(codeStr, label, tier) {
        if (!codeStr) return;
        const cleaned = codeStr.trim().replace(/^[<>/`*#()[\\]{}:;,+=ـ-]+|[<>/`*#()[\\]{}:;,+=ـ-]+$/g, '').replace(/<[^>]+>/g, '').toUpperCase();
        if (cleaned.length < 3 || cleaned.length > 25 || !/[A-Za-z]/.test(cleaned)) return;
        const cl = cleaned.toLowerCase();
        if (blCodes.includes(cl) || blCodes.some(b => cl.includes(b))) return;
        if (compBrands.some(brand => cl.startsWith(brand) || cl.includes('_' + brand) || cl.includes('-' + brand))) return;
        if (['anis', 'megaprix', 'megaphonna', 'ecks'].some(brand => cl.includes(brand))) return;

        let cleanTier = (tier || '').trim().replace(/\\s+/g, '');
        if (cleanTier && !cleanTier.startsWith('$') && !cleanTier.endsWith('$') && !cleanTier.startsWith('€') && !cleanTier.endsWith('€')) {
          cleanTier += '$';
        }
        let cleanLabel = (label || 'كوبون').trim().replace(/^[🏷️🎟️🎫•\\-\\*:\\s]+|[🏷️🎟️🎫•\\-\\*:\\s]+$/g, '');
        if (!cleanLabel) cleanLabel = 'كوبون';

        if (!seenCodes.has(cleaned)) {
          seenCodes.add(cleaned);
          extractedCoupons.push(cleaned);
          extractedDetails.push({ code: cleaned, tier: cleanTier, label: cleanLabel });
        }
      }

      // Tier first: '🎟️ 6/49$ : WOAE06' or 'كوبون $2/15$: WOAE02'
      const p1Regex = /(?:🎟️?|🎫|•|\\-|\\*)?\\s*(?:(?:ال)?كوبون(?:\\s*آخر|\\s*إضافي)?|(?:ال)?كود(?:\\s*آخر|\\s*إضافي)?|code\\s*promo|(?:ال)?قسيمة|خصم|تخفيض)?\\s*([$€]?[0-9]+(?:\\.[0-9]+)?\\s*\\/\\s*[$€]?[0-9]+(?:\\.[0-9]+)?[$€]?)\\s*(?:بكود|code|:|=|：|\\-)?\\s*([A-Za-z0-9_-]{3,25})/gi;
      let mMatch;
      while ((mMatch = p1Regex.exec(cleanNorm)) !== null) {
        addParsedCode(mMatch[2], 'كوبون', mMatch[1]);
      }

      // Code then tier: 'OTPRD02 : 2/15$'
      const p2Regex = /(?:🎟️?|🎫|•|\\-|\\*)?\\s*(?:(?:ال)?كوبون|(?:ال)?كود|code\\s*promo|(?:ال)?قسيمة)?\\s*([A-Za-z][A-Za-z0-9_-]{2,24})\\s*(?:[:=：\\-]|خصم|بخصم|\\()?([$€]?[0-9]+(?:\\.[0-9]+)?\\s*\\/\\s*[$€]?[0-9]+(?:\\.[0-9]+)?[$€]?)\\)?/gi;
      while ((mMatch = p2Regex.exec(cleanNorm)) !== null) {
        addParsedCode(mMatch[1], 'كوبون', mMatch[2]);
      }

      // Labeled lines & Slashed codes: 'كوبون: CODE1', 'كود: CODE1 / CODE2'
      const pLineRegex = /(?:(?:استخدم\\s+|استعمل\\s+|انسخ\\s+|بكود\\s+)?(?:(?:ال)?كـ?وبون|(?:ال)?كـ?ود|(?:ال)?قسيمـ?ة|code\\s*promo|code\\s*de\\s*r[ée]duction|code\\s*r[ée]duction|coupon|promo|utilisez\\s*le\\s*code|avec\\s*le\\s*code)[^\\n:]*|[🏷️🎟️🎫👊])\\s*[:：\\-]\\s*([^\\r\\n]+)/gi;
      while ((mMatch = pLineRegex.exec(cleanNorm)) !== null) {
        let content = mMatch[1].trim();
        const tierMatch = content.match(/\\(?([$€]?[0-9]+(?:\\.[0-9]+)?\\/[0-9]+(?:\\.[0-9]+)?[$€]?)\\)?/);
        const lineTier = tierMatch ? tierMatch[1] : '';
        if (lineTier) content = content.replace(tierMatch[0], '');
        const parts = content.split(/[\\/\\|,،]|\\s+(?:أو|or|ou)\\s+/);
        for (const p of parts) {
          const toks = p.match(/[A-Za-z0-9_-]{3,25}/g) || [];
          for (const tok of toks) {
            addParsedCode(tok, 'كوبون', lineTier);
          }
        }
      }

      // Code tags: <code>CODE</code>
      const pTagsRegex = /(?:(?:ال)?كود|(?:ال)?كوبون|(?:ال)?قسيمة|code|coupon|promo)[^\\r\\n]{0,60}?(?:<code>|`|\\*\\*)([A-Za-z0-9_-]{3,25})(?:<\\/code>|`|\\*\\*)/gi;
      while ((mMatch = pTagsRegex.exec(cleanNorm)) !== null) {
        addParsedCode(mMatch[1], 'كود الخصم', '');
      }

      const finalCoupons = (post.coupons && post.coupons.length > 0) ? post.coupons : extractedCoupons;
      const finalDetails = (post.coupon_details && post.coupon_details.length > 0) ? post.coupon_details : extractedDetails;
      coupon = finalCoupons.length > 0 ? finalCoupons[0] : null;

      // Robust Country Extraction with Tatweel Normalization
      if (/سعودية|السعودية|🇸🇦|saudi|ksa/i.test(cleanNorm)) {
        country = "السعودية 🇸🇦";
      } else if (/إمارات|الامارات|الإمارات|🇦🇪|uae|emirates/i.test(cleanNorm)) {
        country = "الإمارات 🇦🇪";
      } else if (/قطر|🇶🇦|qatar/i.test(cleanNorm)) {
        country = "قطر 🇶🇦";
      } else if (/كويت|الكويت|🇰🇼|kuwait/i.test(cleanNorm)) {
        country = "الكويت 🇰🇼";
      } else if (/بحرين|البحرين|🇧🇭|bahrain/i.test(cleanNorm)) {
        country = "البحرين 🇧🇭";
      } else if (/عمان|عُمان|🇴🇲|oman/i.test(cleanNorm)) {
        country = "عمان 🇴🇲";
      } else if (/كندا|🇨🇦|canada/i.test(cleanNorm)) {
        country = "كندا 🇨🇦";
      } else if (/كوريا|🇰🇷|korea/i.test(cleanNorm)) {
        country = "كوريا 🇰🇷";
      } else if (/الجزائر|🇩🇿|algeria/i.test(cleanNorm)) {
        country = "الجزائر 🇩🇿";
      } else if (/فرنسا|🇫🇷|france/i.test(cleanNorm)) {
        country = "فرنسا 🇫🇷";
      } else if (/أوكرانيا|اوكرانيا|🇺🇦|ukraine/i.test(cleanNorm)) {
        country = "أوكرانيا 🇺🇦";
      } else if (/استراليا|أستراليا|🇦🇺|australia/i.test(cleanNorm)) {
        country = "أستراليا 🇦🇺";
      } else if (/إسبانيا|اسبانيا|🇪🇸|spain/i.test(cleanNorm)) {
        country = "إسبانيا 🇪🇸";
      } else if (/(?:خلي\\s*البلد\\s*كندا|بلد\\s*الحساب\\s*كندا|ضع\\s*البلد\\s*كندا)/i.test(cleanNorm)) {
        country = "كندا 🇨🇦";
      }

      // Clean description extraction (spec lines without telegram handles or affiliate links)
      let cleanDesc = post.description || '';
      if (!cleanDesc) {
        const stripKeywords = ['http://', 'https://', 't.me/', 's.click', 'aliexpress.com', 'رابط الشراء', 'بوت', 'قناتنا', 'تابعونا', 'خلي البلد', 'بلد الحساب', 'ضع البلد', 'السعر', 'prix', 'price'];
        const descLines = [];
        for (const l of lines) {
          const ll = l.toLowerCase();
          if (stripKeywords.some(kw => ll.includes(kw))) continue;
          if (/https?:\\/\\/|t\\.me\\/|@[a-zA-Z0-9_]+/i.test(l)) continue;
          if (/^(?:🎟️|🎫|•|\\-|\\*)?\\s*(?:(?:ال)?كوبون|(?:ال)?كود|code\\s*promo|(?:ال)?قسيمة|code|coupon)\\b/i.test(l)) continue;
          if (/^(?:🎟️|🎫)\\s*[$€]?[0-9]+/i.test(l)) continue;
          const cl = l.replace(/https?:\\/\\/\\S+/g, '').replace(/@[a-zA-Z0-9_]+/g, '').replace(/<\\/?[a-zA-Z0-9_-]+>/g, '').trim();
          if (cl.length > 1) descLines.push(cl);
        }
        cleanDesc = descLines.join('\\n').trim();
      }

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

      const coupons = post.coupons || (coupon ? [coupon] : []);
      const couponDetails = post.coupon_details || (coupon ? [{ code: coupon, tier: '', label: 'كوبون' }] : []);
      const description = post.description || '';

      return {
        id: 'deal-' + index,
        title,
        price_usd: priceUsd,
        price_eur: priceEur,
        price_dzd: priceDzd,
        coupon,
        coupon_code: coupon,
        coupons,
        coupon_details: couponDetails,
        description,
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
      updateGamificationBadges();
    }

    function filterDeals() {
      let filtered = allDeals;
      if (currentCategory === 'favs') {
        const favIds = new Set(getGameState().favs || []);
        filtered = filtered.filter(d => favIds.has(d.id));
      } else if (currentCategory !== 'all') {
        filtered = filtered.filter(d => d.category === currentCategory);
      }

      // Country filtering
      if (currentCountryFilter !== 'all') {
        if (currentCountryFilter === 'canada') {
          filtered = filtered.filter(d => (d.country && d.country.includes('كندا')) || (d.raw_text && /كندا|🇨🇦|canada/i.test(d.raw_text)));
        } else if (currentCountryFilter === 'korea') {
          filtered = filtered.filter(d => (d.country && d.country.includes('كوريا')) || (d.raw_text && /كوريا|🇰🇷|korea/i.test(d.raw_text)));
        } else if (currentCountryFilter === 'algeria') {
          filtered = filtered.filter(d => (d.country && d.country.includes('الجزائر')) || (d.raw_text && /الجزائر|🇩🇿|algeria/i.test(d.raw_text)));
        } else if (currentCountryFilter === 'france') {
          filtered = filtered.filter(d => (d.country && d.country.includes('فرنسا')) || (d.raw_text && /فرنسا|🇫🇷|france/i.test(d.raw_text)));
        }
      }

      if (currentSearchTerm) {
        filtered = filtered.filter(d => 
          (d.title && d.title.toLowerCase().includes(currentSearchTerm)) ||
          (d.raw_text && d.raw_text.toLowerCase().includes(currentSearchTerm)) ||
          (d.coupon && d.coupon.toLowerCase().includes(currentSearchTerm))
        );
      }

      // Sort Deals
      if (currentDealSort === 'price_asc') {
        filtered = [...filtered].sort((a, b) => {
          const pa = a.price_dzd || (a.price_usd ? a.price_usd * usdtRate : 9999999);
          const pb = b.price_dzd || (b.price_usd ? b.price_usd * usdtRate : 9999999);
          return pa - pb;
        });
      } else if (currentDealSort === 'price_desc') {
        filtered = [...filtered].sort((a, b) => {
          const pa = a.price_dzd || (a.price_usd ? a.price_usd * usdtRate : 0);
          const pb = b.price_dzd || (b.price_usd ? b.price_usd * usdtRate : 0);
          return pb - pa;
        });
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
        if (emptyEl) {
          emptyEl.classList.remove('hidden');
          const emptyTitle = emptyEl.querySelector('h3');
          const emptyDesc = emptyEl.querySelector('p');
          if (currentCategory === 'favs') {
            if (emptyTitle) emptyTitle.textContent = I18N[currentLang].fav_empty_title || 'لا توجد صفقات محفوظة بعد';
            if (emptyDesc) emptyDesc.textContent = I18N[currentLang].fav_empty_desc || 'اضغط على أيقونة القلب ❤️ على أي منتج لحفظه والوصول إليه بسرعة هنا.';
          } else {
            if (emptyTitle) emptyTitle.textContent = I18N[currentLang].empty_title || 'لم نعثر على أي صفقات تطابق بحثك';
            if (emptyDesc) emptyDesc.textContent = I18N[currentLang].empty_desc || 'جرّب البحث باسم منتج آخر أو اختيار تصنيف مختلف.';
          }
        }
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

    function updateActiveEventBanner(event) {
      if (!event) return;
      const isFr = currentLang === 'fr';
      const titleEl = document.getElementById('active-event-title');
      const couponsEl = document.getElementById('active-event-coupons');

      if (titleEl) {
        titleEl.textContent = isFr ? (event.name_fr || event.name) : (event.name_ar || event.name);
      }
      if (couponsEl && event.coupon_tiers) {
        const isFranceCh = currentChannel === '@francedealsdz';
        const tiers = (isFranceCh && event.coupon_tiers_fr && event.coupon_tiers_fr.length > 0)
          ? event.coupon_tiers_fr
          : event.coupon_tiers;
        if (tiers && tiers.length > 0) {
          couponsEl.innerHTML = tiers.map(t => `
            <button onclick="copyReferralCode('${t.code}', this)" class="border border-dashed rounded-lg px-2.5 py-1.5 text-xs font-mono font-bold flex items-center gap-1.5 active:scale-95 transition touch-manipulation cursor-pointer hover:border-rose-500" style="background-color: var(--bg-card); border-color: var(--border-subtle); color: var(--text-main);" title="${isFr ? 'Copier le code ' + t.code : 'نسخ الكود ' + t.code}">
              <i class="fa-solid fa-ticket text-rose-500 text-[10px]"></i>
              <span>${t.code}</span>
              <span class="text-[10px] font-sans font-medium text-rose-500">(${t.tier || (t.discount ? '-' + t.discount + '$' : '')})</span>
            </button>
          `).join('');
        }
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
          "image": deal.photo_url || "https://dealscoutgreen.vercel.app/icon.svg",
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

      // Populate Active Deals Trending Keywords Tag Bar
      const kwContainer = document.getElementById('active-deals-keywords');
      if (kwContainer && deals && deals.length > 0) {
        const uniqueTitles = [];
        const seenWords = new Set();
        for (const deal of deals) {
          if (!deal.title) continue;
          let kw = deal.title
            .replace(/[()\\[\\]{}|#*]/g, ' ')
            .replace(/\\s+/g, ' ')
            .trim();
          const parts = kw.split(' ');
          kw = parts.slice(0, 3).join(' ');
          if (kw.length > 25) kw = kw.slice(0, 25).trim();
          const lowerKw = kw.toLowerCase();
          if (kw.length >= 3 && !seenWords.has(lowerKw)) {
            seenWords.add(lowerKw);
            uniqueTitles.push(kw);
          }
          if (uniqueTitles.length >= 8) break;
        }

        if (uniqueTitles.length > 0) {
          kwContainer.innerHTML = uniqueTitles.map(kw => `
            <button onclick="handleSearchInput('${escapeHtml(kw)}')" class="border px-2 py-0.5 rounded-lg text-[10px] font-semibold transition active:scale-95 touch-manipulation hover:border-rose-500 flex items-center gap-1 cursor-pointer" style="background-color: var(--bg-card); border-color: var(--border-card); color: var(--text-main);" title="تصفية حسب ${escapeHtml(kw)}">
              <span class="text-rose-500 font-bold">#</span>
              <span>${escapeHtml(kw)}</span>
            </button>
          `).join('');
        }
      }

      // Update dynamic SEO Meta Keywords & Description with Active Deals
      try {
        const metaKw = document.querySelector('meta[name="keywords"]');
        if (metaKw && deals && deals.length > 0) {
          const dealKws = deals.slice(0, 12).map(d => d.title.replace(/[,;]/g, '').slice(0, 30).trim()).filter(Boolean);
          const baseKws = currentLang === 'fr'
            ? ['Winter Offers AliExpress', 'Codes Promo AliExpress 2026', 'WOAE06', 'WOAE12', 'WOAE23', 'WOAE35', 'AliExpress Algérie', 'Bons Plans Dinar']
            : ['عروض الشتاء AliExpress', 'كوبونات تخفيضات الشتاء 2026', 'WOAE06', 'WOAE12', 'WOAE23', 'WOAE35', 'علي إكسبرس الجزائر', 'أسعار السكوار بالدينار'];
          metaKw.setAttribute('content', [...baseKws, ...dealKws].join(', '));
        }

        const metaDesc = document.querySelector('meta[name="description"]');
        if (metaDesc && deals && deals.length > 0) {
          const topNames = deals.slice(0, 4).map(d => d.title).join(currentLang === 'fr' ? ', ' : '، ');
          metaDesc.setAttribute('content', currentLang === 'fr'
            ? `Bons plans actifs Winter Offers 2026 AliExpress : ${topNames} au meilleur prix converti en Dinar Algérien (DZD) avec codes promo actifs.`
            : `أقوى صفقات عروض الشتاء Winter Offers 2026 الفعالة حالياً على AliExpress: ${topNames} بأفضل سعر بالدينار الجزائري مع كوبونات الخصم.`);
        }
      } catch (e) {}
    }

    function formatPrice(deal) {
      const isAr = currentLang === 'ar';
      if (currentCurrency === 'DZD') {
        if (deal.price_dzd) {
          return `<span class="text-base sm:text-lg font-black font-mono tracking-tight whitespace-nowrap inline-flex items-baseline gap-1 price-num" style="color: var(--text-main);">${deal.price_dzd.toLocaleString()} <span class="text-xs text-rose-500 font-bold font-heading px-1 py-0.5 rounded bg-rose-500/10">${isAr ? 'دج' : 'DZD'}</span></span>`;
        }
      } else if (currentCurrency === 'EUR') {
        if (deal.price_eur) {
          return `<span class="text-base sm:text-lg font-black font-mono tracking-tight whitespace-nowrap inline-flex items-baseline gap-1 price-num" style="color: var(--text-main);">${deal.price_eur.toFixed(2)} <span class="text-xs text-rose-500 font-bold font-heading px-1 py-0.5 rounded bg-rose-500/10">€</span></span>`;
        }
      } else if (currentCurrency === 'USD') {
        if (deal.price_usd) {
          return `<span class="text-base sm:text-lg font-black font-mono tracking-tight whitespace-nowrap inline-flex items-baseline gap-1 price-num" style="color: var(--text-main);">${deal.price_usd.toFixed(2)} <span class="text-xs text-rose-500 font-bold font-heading px-1 py-0.5 rounded bg-rose-500/10">$</span></span>`;
        }
      }
      return `<span class="text-sm font-bold text-rose-500 font-heading">${isAr ? 'تخفيض خاص' : 'Prix Promo'}</span>`;
    }

    function renderGrid(dealsToRender = null) {
      const deals = dealsToRender !== null ? dealsToRender : allDeals;
      const grid = document.getElementById('deals-grid');
      if (!grid) return;
      grid.innerHTML = '';

      deals.forEach(deal => {
        const card = document.createElement('article');
        card.className = 'deal-card p-3 sm:p-3.5 flex flex-col justify-between';

        const safeTitle = escapeHtml(deal.title);

        const isFav = isFavorite(deal.id);
        const favBtnHtml = `
          <button type="button" onclick="toggleFavorite('${deal.id}', event)" aria-label="${isFav ? 'إزالة من المفضلة' : 'حفظ في المفضلة'}" class="absolute top-2 right-2 w-7 h-7 rounded border flex items-center justify-center transition active:scale-125 touch-manipulation z-20 cursor-pointer shadow-sm hover:border-rose-500" style="background-color: rgba(18, 18, 21, 0.85); border-color: rgba(255, 255, 255, 0.2);">
            <i class="${isFav ? 'fa-solid text-rose-500' : 'fa-regular text-white/90'} fa-heart text-xs" id="fav-icon-${deal.id}"></i>
          </button>
        `;

        const photoHtml = deal.photo_url ? `
          <div class="relative w-full aspect-[4/3] rounded-lg overflow-hidden mb-2.5 cursor-pointer group flex items-center justify-center border" style="background-color: var(--bg-page); border-color: var(--border-card);" onclick="openDealModal('${deal.id}')">
            <img src="${deal.photo_url}" alt="${safeTitle}" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="handleImgError(this, '${escapeHtml(deal.photo_url)}')" class="w-full h-full object-contain group-hover:scale-102 transition-transform duration-200">
            ${favBtnHtml}
            <div class="absolute top-2 left-2 flex flex-col items-start gap-1 z-10 pointer-events-none">
              ${deal.country ? `<span class="text-[10px] sm:text-[11px] font-black px-2 py-0.5 rounded shadow border flex items-center gap-1 backdrop-blur-md" style="background-color: #e11d48; border-color: rgba(255, 255, 255, 0.35); color: #ffffff;"><i class="fa-solid fa-location-dot text-[9px]"></i> <span>خلي البلد: ${escapeHtml(deal.country)}</span></span>` : ''}
              ${deal.has_coins ? `<span class="bg-amber-500 text-zinc-950 text-[10px] font-bold px-1.5 py-0.5 rounded shadow-sm flex items-center gap-1 tracking-tight"><i class="fa-solid fa-coins text-[9px]"></i> Coins</span>` : ''}
            </div>
          </div>
        ` : `
          <div class="relative w-full aspect-[4/3] rounded-lg overflow-hidden mb-2.5 cursor-pointer group flex items-center justify-center border" style="background-color: var(--bg-page); border-color: var(--border-card);" onclick="openDealModal('${deal.id}')">
            <div class="flex flex-col items-center justify-center gap-1.5 opacity-50 p-4 text-center">
              <i class="fa-solid fa-bag-shopping text-xl text-rose-500"></i>
              <span class="text-[11px] font-semibold" style="color: var(--text-muted);">${safeTitle.slice(0, 30)}...</span>
            </div>
            ${favBtnHtml}
            <div class="absolute top-2 left-2 flex flex-col items-start gap-1 z-10 pointer-events-none">
              ${deal.country ? `<span class="text-[10px] sm:text-[11px] font-black px-2 py-0.5 rounded shadow border flex items-center gap-1 backdrop-blur-md" style="background-color: #e11d48; border-color: rgba(255, 255, 255, 0.35); color: #ffffff;"><i class="fa-solid fa-location-dot text-[9px]"></i> <span>خلي البلد: ${escapeHtml(deal.country)}</span></span>` : ''}
              ${deal.has_coins ? `<span class="bg-amber-500 text-zinc-950 text-[10px] font-bold px-1.5 py-0.5 rounded shadow-sm flex items-center gap-1 tracking-tight"><i class="fa-solid fa-coins text-[9px]"></i> Coins</span>` : ''}
            </div>
          </div>
        `;

        const couponHtml = deal.coupon ? `
          <div class="border border-dashed rounded-lg px-2.5 py-1.5 flex items-center justify-between gap-1.5 mb-2.5 transition coupon-chip">
            <div class="flex items-center gap-1.5 min-w-0">
              <i class="fa-solid fa-ticket text-xs flex-shrink-0 text-amber-500"></i>
              <div class="min-w-0">
                <span class="text-[9px] uppercase tracking-wider block font-bold opacity-60 font-heading">${currentLang === 'fr' ? 'Code Promo' : 'كود الخصم'}</span>
                <span class="font-mono text-xs font-bold truncate select-all block text-rose-600 dark:text-rose-400 tracking-wide">${escapeHtml(deal.coupon)}</span>
              </div>
            </div>
            <button onclick="copyCoupon('${deal.coupon}', this)" aria-label="Copy coupon" class="min-h-[32px] min-w-[62px] border text-[11px] font-bold px-2 py-0.5 rounded transition flex items-center justify-center gap-1 flex-shrink-0 touch-manipulation active:scale-95 shadow-sm hover:border-zinc-400 dark:hover:border-zinc-500 cursor-pointer" style="background-color: var(--bg-card); border-color: var(--border-card); color: var(--text-main);">
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
            <div class="flex items-center justify-between gap-2 mb-1">
              <span class="text-[10px] font-bold px-2 py-0.5 rounded border font-heading" style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-muted);">
                ${deal.category_label || I18N[currentLang].deal_category_fallback}
              </span>
              <span class="text-[10px] font-mono opacity-60 flex items-center gap-1">
                <i class="fa-regular fa-clock text-[9px]"></i>
                ${deal.date ? deal.date.split(' ')[0] : ''}
              </span>
            </div>
            ${deal.country ? `
              <div class="mb-2 px-2 py-0.5 rounded text-[11px] font-bold flex items-center gap-1.5 border border-rose-500/25 bg-rose-500/10 text-rose-600 dark:text-rose-400">
                <i class="fa-solid fa-location-dot text-[10px] flex-shrink-0"></i>
                <span class="truncate">${currentLang === 'fr' ? 'Régler pays:' : 'شرط السعر: خلي البلد'} <strong>${escapeHtml(deal.country)}</strong></span>
              </div>
            ` : ''}
            <h3 class="font-bold text-xs sm:text-sm line-clamp-2 mb-2 hover:text-rose-500 transition cursor-pointer leading-snug break-words font-heading" style="color: var(--text-main);" onclick="openDealModal('${deal.id}')">
              ${safeTitle}
            </h3>
            ${couponHtml}
          </div>

          <div class="pt-2 border-t space-y-2" style="border-color: var(--border-card);">
            <div class="flex items-baseline justify-between gap-2">
              <div class="flex items-baseline flex-wrap gap-1.5 min-w-0">
                ${formatPrice(deal)}
                ${secondaryPrice}
              </div>
              ${deal.telegram_url ? `
                <a href="${deal.telegram_url}" target="_blank" rel="noopener noreferrer" title="Telegram" class="w-7 h-7 rounded border flex items-center justify-center active:scale-95 transition touch-manipulation flex-shrink-0 text-sky-500 hover:border-sky-500" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
                  <i class="fa-brands fa-telegram text-xs"></i>
                </a>
              ` : ''}
            </div>

            <!-- Primary Buy Button with Coupon Auto-Copy -->
            <a href="${deal.affiliate_url}" target="_blank" rel="noopener noreferrer" onclick="handleBuyClick('${deal.coupon || ''}')" class="w-full btn-ali-primary active:scale-[0.98] text-white font-bold text-xs sm:text-sm py-2 px-3 rounded-lg text-center flex items-center justify-center gap-1.5 transition shadow-sm touch-manipulation min-h-[40px] font-heading cursor-pointer">
              <i class="fa-solid fa-cart-shopping text-xs"></i>
              <span>${I18N[currentLang].btn_buy}</span>
              ${deal.coupon ? `<span class="bg-black/25 text-[10px] font-mono px-1.5 py-0.5 rounded text-white mr-1 inline-flex items-center gap-1 font-bold"><i class="fa-solid fa-ticket text-[9px]"></i> ${escapeHtml(deal.coupon)}</span>` : ''}
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
          .replace(new RegExp('\\n', 'g'), '<br>')
          .replace(new RegExp('(https?:\\/\\/s\\.click\\.aliexpress\\.com\\/e\\/[A-Za-z0-9_-]+)', 'g'), '<a href="$1" target="_blank" rel="noopener noreferrer" class="text-rose-500 font-bold underline break-all">$1</a>')
          .replace(new RegExp('(@[A-Za-z0-9_]+)', 'g'), '<span class="text-sky-500 font-semibold">$1</span>');

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

      const countryAlert = document.getElementById('modal-country-alert');
      const countryTarget = document.getElementById('modal-country-target');
      if (deal.country) {
        country.innerHTML = `<i class="fa-solid fa-location-dot text-[10px]"></i> <span>خلي البلد: ${escapeHtml(deal.country)}</span>`;
        country.classList.remove('hidden');
        if (countryAlert && countryTarget) {
          countryTarget.textContent = deal.country;
          countryAlert.classList.remove('hidden');
          countryAlert.style.display = 'flex';
        }
      } else {
        country.classList.add('hidden');
        if (countryAlert) {
          countryAlert.classList.add('hidden');
          countryAlert.style.display = 'none';
        }
      }

      if (deal.has_coins) coins.classList.remove('hidden');
      else coins.classList.add('hidden');

      // Multi-coupon & single coupon handling
      const multiWrap = document.getElementById('modal-multi-coupons');
      const coupons = deal.coupons || (deal.coupon ? [deal.coupon] : []);
      const details = deal.coupon_details || [];

      if (coupons.length > 1) {
        if (couponWrap) { couponWrap.classList.add('hidden'); couponWrap.style.display = 'none'; }
        if (multiWrap) {
          multiWrap.classList.remove('hidden');
          multiWrap.style.display = 'flex';
          multiWrap.innerHTML = coupons.map((c, i) => {
            const det = details.find(d => d.code === c) || {};
            const lbl = det.label || (i === 0 ? 'كوبون' : 'كوبون إضافي');
            const tierBadge = det.tier ? `<span class="bg-rose-500/10 text-rose-500 text-[10px] font-bold px-1.5 py-0.5 rounded border border-rose-500/20">${escapeHtml(det.tier)}</span>` : '';
            return `
              <div class="border border-dashed rounded-xl p-2.5 flex items-center justify-between gap-2" style="background-color: var(--bg-elevated); border-color: var(--border-card);">
                <div class="flex items-center gap-2 min-w-0">
                  <i class="fa-solid fa-ticket text-sm flex-shrink-0 text-amber-500"></i>
                  <div class="min-w-0">
                    <div class="text-[10px] opacity-75 flex items-center gap-1">${escapeHtml(lbl)} ${tierBadge}</div>
                    <span class="font-mono font-bold text-sm tracking-wider truncate block" style="color: var(--text-main);">${escapeHtml(c)}</span>
                  </div>
                </div>
                <button onclick="copyCoupon('${escapeHtml(c)}', this)" class="min-h-[36px] px-3 py-1 border active:scale-95 text-xs font-bold rounded-lg transition flex items-center gap-1 flex-shrink-0 touch-manipulation cursor-pointer" style="background-color: var(--bg-card); border-color: var(--border-card); color: var(--text-main);">
                  <i class="fa-regular fa-copy text-[11px]"></i>
                  <span class="copy-text">${I18N[currentLang].btn_copy}</span>
                </button>
              </div>
            `;
          }).join('');
        }
      } else if (coupons.length === 1) {
        if (multiWrap) { multiWrap.classList.add('hidden'); multiWrap.style.display = 'none'; }
        if (couponWrap) {
          couponWrap.classList.remove('hidden');
          couponWrap.style.display = 'flex';
          couponCode.textContent = coupons[0];
        }
      } else {
        if (multiWrap) { multiWrap.classList.add('hidden'); multiWrap.style.display = 'none'; }
        if (couponWrap) {
          couponWrap.classList.add('hidden');
          couponWrap.style.display = 'none';
        }
      }

      // Clean Description / Specs in modal
      const descWrap = document.getElementById('modal-desc-wrap');
      const descText = document.getElementById('modal-desc-text');
      if (descWrap && descText) {
        if (deal.description && deal.description.trim().length > 3) {
          descText.textContent = deal.description.trim();
          descWrap.classList.remove('hidden');
          descWrap.style.display = 'block';
        } else {
          descWrap.classList.add('hidden');
          descWrap.style.display = 'none';
        }
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
      copyTextToClipboard(code).then(() => {
        triggerHaptic([15, 30, 15]);
        addSavedDZD(1000);
        fireConfetti(btn);
        showToast((I18N[currentLang].btn_copied || 'تم النسخ!') + ' ' + code);
        if (btn) {
          const span = btn.querySelector('.copy-text') || btn.querySelector('span');
          const icon = btn.querySelector('i');
          const origIcon = icon ? icon.className : '';
          const origText = span ? span.textContent : '';
          
          if (span) span.textContent = I18N[currentLang].btn_copied || 'تم النسخ!';
          if (icon) icon.className = 'fa-solid fa-check text-[11px] text-emerald-500';
          btn.classList.add('border-emerald-500', 'text-emerald-500');
          
          setTimeout(() => {
            if (span) span.textContent = origText;
            if (icon) icon.className = origIcon;
            btn.classList.remove('border-emerald-500', 'text-emerald-500');
          }, 1800);
        }
      }).catch(() => {
        showToast(code);
      });
    }

    function copyCouponFromModal(btn) {
      if (currentActiveDeal && currentActiveDeal.coupon) {
        copyCoupon(currentActiveDeal.coupon, btn);
      }
    }

    function copyReferralCode(code, btn) {
      if (!code) return;
      copyTextToClipboard(code).then(() => {
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

    // ── AliExpress Coins Deal Link Generator ────────────────────────
    const AFF_TRACKING_TAG = 'dzkhvled16';

    function extractAliExpressPid(input) {
      if (!input) return null;
      const str = String(input).trim();
      // 1. Direct digits (10 to 20 digits)
      if (/^[0-9]{10,20}$/.test(str)) return str;
      // 2. /item/123456789.html
      const mItem = str.match(new RegExp('/item/(\\d{10,20})', 'i'));
      if (mItem) return mItem[1];
      // 3. /p/trade/123456789 or /p/anything/123456789
      const mP = str.match(new RegExp('/p/[a-z0-9_-]+/(\\d{10,20})', 'i'));
      if (mP) return mP[1];
      // 4. productIds=123456789 or productId=123456789
      const mProd = str.match(/productIds?=([0-9]{10,20})/i);
      if (mProd) return mProd[1];
      // 5. itemId=123456789 or item_id=123456789
      const mItemParam = str.match(/(?:itemId|item_id)[=:]([0-9]{10,20})/i);
      if (mItemParam) return mItemParam[1];
      // 6. Generic id=123456789
      const mGenericId = str.match(/[?&#]id=([0-9]{10,20})/i);
      if (mGenericId) return mGenericId[1];
      // 7. Any 11-18 continuous digits in an aliexpress context
      if (str.includes('aliexpress') || str.includes('alibab')) {
        const mDigits = str.match(/([0-9]{11,18})/);
        if (mDigits) return mDigits[1];
      }
      return null;
    }

    async function pasteToCoinsInput() {
      try {
        if (navigator.clipboard && navigator.clipboard.readText) {
          const text = await navigator.clipboard.readText();
          const input = document.getElementById('coins-input-url');
          if (input && text) {
            input.value = text.trim();
            generateCoinLink();
          }
        }
      } catch (e) {
        showToast(currentLang === 'fr' ? 'Collez manuellement le lien' : 'الصق الرابط يدوياً في الخانة');
      }
    }

    async function generateCoinLink() {
      const input = document.getElementById('coins-input-url');
      const errBox = document.getElementById('coins-gen-error');
      const errText = document.getElementById('coins-gen-error-text');
      const resultBox = document.getElementById('coins-gen-result');
      const submitBtn = document.getElementById('coins-submit-btn');

      if (!input) return;
      const raw = input.value.trim();
      if (!raw) {
        if (errBox) {
          errBox.classList.remove('hidden');
          if (errText) errText.textContent = (currentLang === 'fr') ? 'Veuillez coller un lien AliExpress ou un ID valide.' : 'يرجى إدخال رابط منتج صالح من AliExpress أو رقم المنتج.';
        }
        return;
      }

      if (errBox) errBox.classList.add('hidden');

      // 1. Try instant client-side regex extraction
      let pid = extractAliExpressPid(raw);

      // 2. If shortlink (e.g. a.aliexpress.com or s.click.aliexpress.com), resolve via backend
      if (!pid && (raw.includes('a.aliexpress.com') || raw.includes('s.click.aliexpress.com') || raw.includes('/e/'))) {
        if (submitBtn) {
          submitBtn.disabled = true;
          submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> ' + (currentLang === 'fr' ? 'Résolution...' : 'جاري الفحص...');
        }
        try {
          const resp = await fetch(`/api/resolve-coin-link?url=${encodeURIComponent(raw)}`);
          if (resp.ok) {
            const data = await resp.json();
            if (data && data.product_id) {
              pid = data.product_id;
            }
          }
        } catch (e) {
          console.warn('Backend resolution fallback:', e);
        } finally {
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="fa-solid fa-coins text-sm"></i> ' + (currentLang === 'fr' ? 'Générer le lien Pièces' : 'توليد رابط العملات');
          }
        }
      }

      if (!pid) {
        if (errBox) {
          errBox.classList.remove('hidden');
          if (errText) errText.textContent = (currentLang === 'fr') ? "Lien non reconnu. Assurez-vous qu'il s'agit d'un produit AliExpress valide." : 'لم يتم التعرف على كود المنتج. يرجى التأكد من نسخ رابط منتج صحيح من AliExpress.';
        }
        return;
      }

      // Build monentized links with affiliate tracking ID
      const coinUrl = `https://www.aliexpress.com/item/${pid}.html?sourceType=620&channel=coin&aff_fcid=${AFF_TRACKING_TAG}`;
      const superUrl = `https://www.aliexpress.com/item/${pid}.html?sourceType=561&channel=superdeal&aff_fcid=${AFF_TRACKING_TAG}`;
      const bundleUrl = `https://www.aliexpress.com/ssr/300000512/BundleDeals2?disableNav=YES&pha_manifest=ssr&_immersiveMode=true&productIds=${pid}&aff_fcid=${AFF_TRACKING_TAG}`;
      const directUrl = `https://www.aliexpress.com/item/${pid}.html?aff_fcid=${AFF_TRACKING_TAG}`;

      // Populate UI
      const pidBadge = document.getElementById('coins-gen-pid-badge');
      if (pidBadge) pidBadge.textContent = 'ID: ' + pid;

      const outCoin = document.getElementById('coins-gen-out-coin');
      if (outCoin) outCoin.value = coinUrl;

      const btnBuy = document.getElementById('coins-gen-btn-buy');
      if (btnBuy) btnBuy.href = coinUrl;

      const outSuper = document.getElementById('coins-gen-out-super');
      if (outSuper) outSuper.value = superUrl;
      const btnSuper = document.getElementById('coins-gen-btn-super');
      if (btnSuper) btnSuper.href = superUrl;

      const outBundle = document.getElementById('coins-gen-out-bundle');
      if (outBundle) outBundle.value = bundleUrl;
      const btnBundle = document.getElementById('coins-gen-btn-bundle');
      if (btnBundle) btnBundle.href = bundleUrl;

      if (resultBox) {
        resultBox.classList.remove('hidden');
        resultBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }

      showToast(currentLang === 'fr' ? 'Lien de réduction Pièces généré avec succès !' : 'تم توليد رابط خصم العملات بنجاح!');
    }

    function copyCoinLink(inputId, btn) {
      const input = document.getElementById(inputId);
      if (!input || !input.value) return;
      const textToCopy = input.value;
      copyTextToClipboard(textToCopy).then(() => {
        if (btn) {
          const original = btn.innerHTML;
          btn.innerHTML = '<i class="fa-solid fa-check text-emerald-500"></i> ' + (currentLang === 'fr' ? 'Copié !' : 'تم النسخ!');
          btn.classList.add('border-emerald-500');
          setTimeout(() => {
            btn.innerHTML = original;
            btn.classList.remove('border-emerald-500');
          }, 2000);
        }
        showToast(currentLang === 'fr' ? 'Lien copié dans le presse-papier !' : 'تم نسخ رابط الخصم بنجاح!');
      }).catch(() => {
        showToast(textToCopy);
      });
    }

    // ── Algerian & Universal Parcel Tracking Engine ───────────────────
    async function pasteToTrackingInput() {
      try {
        const text = await navigator.clipboard.readText();
        if (text) {
          const input = document.getElementById('tracking-input-num');
          if (input) {
            input.value = text.trim();
            submitTracking();
          }
        }
      } catch (e) {
        showToast(currentLang === 'fr' ? 'Collez le numéro de suivi' : 'الصق رقم التتبع في الخانة');
      }
    }

    function setTrackingSample(code) {
      const input = document.getElementById('tracking-input-num');
      if (input) {
        input.value = code;
        submitTracking();
      }
    }

    function saveRecentTrackingNum(num) {
      if (!num) return;
      try {
        let recents = JSON.parse(localStorage.getItem('dealscout_recent_tracks') || '[]');
        recents = [num, ...recents.filter(n => n !== num)].slice(0, 4);
        localStorage.setItem('dealscout_recent_tracks', JSON.stringify(recents));
      } catch (e) {}
    }

    function renderRecentTrackingList() {
      const wrap = document.getElementById('tracking-recent-wrap');
      const list = document.getElementById('tracking-recent-list');
      if (!wrap || !list) return;
      try {
        const recents = JSON.parse(localStorage.getItem('dealscout_recent_tracks') || '[]');
        if (recents.length > 0) {
          list.innerHTML = recents.map(n => `
            <button type="button" onclick="setTrackingSample('${n}')" class="font-mono text-[10px] px-2 py-0.5 rounded border flex items-center gap-1 hover:border-blue-500 transition active:scale-95" style="background-color: var(--bg-elevated); border-color: var(--border-card); color: var(--text-main);">
              <span>${n}</span>
            </button>
          `).join('');
          wrap.classList.remove('hidden');
        } else {
          wrap.classList.add('hidden');
        }
      } catch (e) {
        wrap.classList.add('hidden');
      }
    }

    function copyTrackingNum() {
      const numEl = document.getElementById('tracking-result-num');
      const icon = document.getElementById('tracking-copy-icon');
      const text = document.getElementById('tracking-copy-text');
      if (numEl && numEl.textContent) {
        copyTextToClipboard(numEl.textContent.trim()).then(() => {
          if (icon) icon.className = 'fa-solid fa-check text-emerald-400';
          if (text) text.textContent = (currentLang === 'fr') ? 'Copié !' : 'تم النسخ!';
          showToast(currentLang === 'fr' ? 'Numéro de suivi copié !' : 'تم نسخ رقم التتبع!');
          setTimeout(() => {
            if (icon) icon.className = 'fa-regular fa-copy';
            if (text) text.textContent = (currentLang === 'fr') ? 'Copier' : 'نسخ';
          }, 2000);
        }).catch(() => {
          showToast(numEl.textContent.trim());
        });
      }
    }

    async function submitTracking() {
      const input = document.getElementById('tracking-input-num');
      const errBox = document.getElementById('tracking-error');
      const errText = document.getElementById('tracking-error-text');
      const resultCard = document.getElementById('tracking-result-card');
      const submitBtn = document.getElementById('tracking-submit-btn');

      if (!input) return;
      const rawNum = input.value.trim().replace(/\\s+/g, '');
      if (!rawNum || rawNum.length < 5) {
        if (errBox) {
          errBox.classList.remove('hidden');
          if (errText) errText.textContent = (currentLang === 'fr') 
            ? 'Veuillez saisir un numéro de suivi valide.' 
            : 'يرجى إدخال رقم تتبع صالح.';
        }
        return;
      }
      if (errBox) errBox.classList.add('hidden');

      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> ' + (currentLang === 'fr' ? 'Recherche...' : 'جاري التتبع...');
      }

      try {
        const resp = await fetch(`/api/track-parcel?num=${encodeURIComponent(rawNum)}`);
        const data = await resp.json();

        if (data && data.ok) {
          if (resultCard) resultCard.classList.remove('hidden');

          // Save to recent tracking numbers history
          saveRecentTrackingNum(data.tracking_number);
          renderRecentTrackingList();

          const carrier = data.carrier || {};
          const isFr = currentLang === 'fr';

          // Carrier details & Flag
          const flagEl = document.getElementById('tracking-carrier-flag');
          if (flagEl) flagEl.textContent = carrier.origin_flag || '🌐';

          const carrierName = document.getElementById('tracking-carrier-name');
          if (carrierName) carrierName.textContent = isFr ? (carrier.name_fr || carrier.name_ar) : carrier.name_ar;

          const serviceBadge = document.getElementById('tracking-service-badge');
          if (serviceBadge) serviceBadge.textContent = isFr ? (carrier.service_type_fr || carrier.service_type_ar) : carrier.service_type_ar;

          const routeOrigin = document.getElementById('tracking-route-origin');
          if (routeOrigin) routeOrigin.textContent = isFr ? (carrier.origin_country_fr || carrier.origin_country_ar) : carrier.origin_country_ar;
          const routeOriginFlag = document.getElementById('tracking-route-origin-flag');
          if (routeOriginFlag) routeOriginFlag.textContent = carrier.origin_flag || '🇨🇳';

          const resultNum = document.getElementById('tracking-result-num');
          if (resultNum) resultNum.textContent = data.tracking_number;

          const estTime = document.getElementById('tracking-est-time');
          if (estTime) estTime.textContent = carrier.typical_days || '14 - 25 يوم';

          // Status Badge with Color & Text
          const statusText = document.getElementById('tracking-status-text');
          const statusBadge = document.getElementById('tracking-status-badge');
          if (statusBadge && statusText) {
            const stageTexts = {
              'delivered': isFr ? 'Prêt au bureau de poste / Livré 🎉' : 'جاهز للاستلام ببريد بلديتك 🎉',
              'customs': isFr ? 'En cours de dédouanement' : 'في المعالجة والرقابة الجمركية',
              'in_destination_country': isFr ? 'Arrivé en Algérie (CTN Alger) 🇩🇿' : 'وصل للجزائر (مركز الفرز CTN) 🇩🇿',
              'in_flight': isFr ? 'En transit aérien international ✈️' : 'في رحلة الشحن الجوي الدولي ✈️',
              'in_transit': isFr ? "En cours d'acheminement" : 'في مسار الشحن الدولي',
              'registered_awaiting_scan': isFr ? 'Numéro généré — En attente du premier scan' : 'مسجل حديثاً — بانتظار أول فحص فيزيائي ⏳'
            };
            statusText.textContent = stageTexts[data.status_stage] || (isFr ? 'En transit' : 'في مسار الشحن');
            if (data.status_stage === 'delivered') {
              statusBadge.className = 'px-3 py-1 rounded-xl text-xs font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/25 flex items-center gap-1.5';
            } else if (data.status_stage === 'registered_awaiting_scan') {
              statusBadge.className = 'px-3 py-1 rounded-xl text-xs font-bold bg-amber-500/10 text-amber-400 border border-amber-500/25 flex items-center gap-1.5';
            } else {
              statusBadge.className = 'px-3 py-1 rounded-xl text-xs font-bold bg-blue-500/10 text-blue-400 border border-blue-500/25 flex items-center gap-1.5';
            }
          }

          // Smart Advisory Card
          const advisoryCard = document.getElementById('tracking-advisory-card');
          const advisoryTitle = document.getElementById('tracking-advisory-title');
          const advisoryBody = document.getElementById('tracking-advisory-body');
          if (advisoryCard && advisoryTitle && advisoryBody && data.advice) {
            advisoryTitle.textContent = isFr ? (data.advice.title_fr || data.advice.title_ar) : data.advice.title_ar;
            advisoryBody.textContent = isFr ? (data.advice.body_fr || data.advice.body_ar) : data.advice.body_ar;
            advisoryCard.classList.remove('hidden');
          }

          // 5-Step Algerian Delivery Journey Stages
          let activeStepNum = 1;
          if (data.delivery_stages && data.delivery_stages.length > 0) {
            data.delivery_stages.forEach(st => {
              const stepEl = document.getElementById('track-step-' + st.step);
              if (stepEl) {
                const badge = stepEl.querySelector('span');
                if (st.completed) {
                  stepEl.classList.remove('opacity-40');
                  stepEl.style.borderColor = 'rgba(16, 185, 129, 0.4)';
                  if (badge) {
                    badge.className = 'w-5 h-5 rounded-full bg-emerald-500 text-white font-bold text-[10px] flex items-center justify-center';
                  }
                } else {
                  stepEl.classList.add('opacity-40');
                  stepEl.style.borderColor = 'var(--border-card)';
                  if (badge) {
                    badge.className = 'w-5 h-5 rounded-full bg-zinc-600 text-white font-bold text-[10px] flex items-center justify-center';
                  }
                }
                if (st.active) {
                  activeStepNum = st.step;
                  stepEl.classList.remove('opacity-40');
                  stepEl.style.borderColor = 'var(--border-subtle)';
                  if (badge) {
                    badge.className = 'w-5 h-5 rounded-full bg-emerald-500 text-white font-bold text-[10px] flex items-center justify-center ring-2 ring-emerald-500/40 animate-pulse';
                  }
                }
              }
            });
            const progressEl = document.getElementById('tracking-journey-progress');
            if (progressEl) {
              progressEl.textContent = isFr ? `Étape ${activeStepNum} sur 5` : `المرحلة ${activeStepNum} من 5`;
            }
          }

          // Checkpoints list feed
          const checkWrap = document.getElementById('tracking-checkpoints-wrap');
          const checkList = document.getElementById('tracking-checkpoints-list');
          if (checkWrap && checkList) {
            if (data.has_live_checkpoints && data.live_checkpoints && data.live_checkpoints.length > 0) {
              checkList.innerHTML = data.live_checkpoints.map(cp => `
                <div class="relative pb-3">
                  <span class="w-2.5 h-2.5 rounded-full bg-blue-500 absolute -right-[18px] top-1 ring-4 ring-blue-500/20"></span>
                  <div class="font-bold text-xs" style="color: var(--text-main);">${cp.description}</div>
                  <div class="text-[11px] font-mono opacity-70 mt-0.5" style="color: var(--text-muted);">${cp.time || ''} ${cp.location ? '• ' + cp.location : ''}</div>
                </div>
              `).join('');
              checkWrap.classList.remove('hidden');
            } else {
              checkWrap.classList.add('hidden');
            }
          }

          // Direct Portal Deep-Link Verification Buttons
          const links = data.portal_links || data.direct_links || {};
          const p17 = document.getElementById('btn-portal-17track');
          if (p17 && links.track17) p17.href = isFr ? (links.track17_en || links.track17) : links.track17;
          const pNinja = document.getElementById('btn-portal-ninja');
          if (pNinja && links.postal_ninja) pNinja.href = isFr ? (links.postal_ninja_en || links.postal_ninja) : links.postal_ninja;
          const pCainiao = document.getElementById('btn-portal-cainiao');
          if (pCainiao && links.cainiao) pCainiao.href = links.cainiao;
          const pPoste = document.getElementById('btn-portal-poste');
          if (pPoste && links.algerie_poste) pPoste.href = links.algerie_poste;
          const pParcels = document.getElementById('btn-portal-parcels');
          if (pParcels && links.parcels_app) pParcels.href = links.parcels_app;

          if (resultCard) {
            resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
          }
          showToast(isFr ? 'Détails de livraison chargés avec succès !' : 'تم استرجاع مسار الشحنة بنجاح!');
        } else {
          if (errBox) {
            errBox.classList.remove('hidden');
            if (errText) errText.textContent = (currentLang === 'fr') 
              ? (data.error_fr || 'Numéro de suivi introuvable.') 
              : (data.error_ar || 'تعذر العثور على شحنة بهذا الرقم.');
          }
        }
      } catch (err) {
        console.warn('Tracking query error:', err);
        showToast(currentLang === 'fr' ? 'Erreur de connexion au service de suivi' : 'حدث خطأ في الاتصال بخدمة التتبع');
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = '<i class="fa-solid fa-magnifying-glass text-xs"></i> ' + (currentLang === 'fr' ? 'Suivre le colis' : 'تتبع الشحنة');
        }
      }
    }

    // ── Keyboard & Lifecycle Handlers ───────────────────────────────
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        closeDealModal();
        closeTelegramPopup(true);
        closeRouletteModal();
        closeGamificationHub();
        if (currentSearchTerm) resetFilters();
      }
      // Ctrl+K or / keyboard shortcut to focus search
      if ((e.ctrlKey || e.metaKey) && (e.key === 'k' || e.key === 'K')) {
        e.preventDefault();
        const searchInput = (window.innerWidth >= 768) ? document.getElementById('desktop-search') : document.getElementById('mobile-search');
        if (searchInput) searchInput.focus();
      } else if (e.key === '/' && !['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) {
        e.preventDefault();
        const searchInput = (window.innerWidth >= 768) ? document.getElementById('desktop-search') : document.getElementById('mobile-search');
        if (searchInput) searchInput.focus();
      }
    });

    window.addEventListener('popstate', (e) => {
      const page = (e.state && e.state.page) || window.location.pathname.replace(new RegExp('^/'), '').split('/')[0] || window.location.hash.replace(/^#/, '') || 'deals';
      showPage(page, false);
    });

    document.addEventListener('DOMContentLoaded', () => {
      // Determine initial page from URL pathname or hash (e.g. /cards or /#cards)
      const pathRoute = window.location.pathname.replace(new RegExp('^/'), '').split('/')[0].toLowerCase();
      const hashRoute = window.location.hash.replace(/^#/, '').toLowerCase();
      const validPages = ['deals', 'cards', 'coins', 'faq', 'contact', 'about'];
      if (!validPages.includes('tracking')) validPages.push('tracking');
      const initialRoute = validPages.includes(pathRoute) ? pathRoute : (validPages.includes(hashRoute) ? hashRoute : 'deals');

      // Initialize theme & language
      applyTheme(currentTheme);
      setLanguage(currentLang);
      updateGamificationBadges();
      renderRecentTrackingList();
      if (initialRoute !== 'deals') {
        showPage(initialRoute, false);
      }
      fetchDeals();
      setInterval(() => fetchDeals(false), 180000);
      initTelegramPopupTrigger();
    });
  </script>

</body>
</html>"""

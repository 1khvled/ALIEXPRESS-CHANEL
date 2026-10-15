"""
User-Facing Public Website for DealScout DZ.
Features:
- Real-time Telegram content feed from @DzAliexpress0 & @francedealsdz
- Interactive Deals Grid & Telegram Message Stream view
- Live SquareAlgerie.com USDT/Dinar exchange rate integration
- Instant price conversion to Algerian Dinar (DZD)
- 1-click coupon code copying with visual feedback
- Category filtering (Smartphones, Gaming, Audio, Tech, Roundups)
- Live search by product name & brand
- Shopping guide for Algerian buyers (Coin discounts, country switches, payment cards)
- Mobile-first responsive PWA design
"""

USER_WEBSITE_HTML = """<!DOCTYPE html>
<html lang="ar" dir="rtl" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>عروض علي اكسبرس الجزائر 🇩🇿 | صفقات وتخفيضات AliExpress المباشرة</title>
  <meta name="description" content="أفضل صفقات وتخفيضات AliExpress في الجزائر مع كوبونات الخصم وتخفيض العملات المحدثة لحظياً من قنوات التيليجرام بالدينار الجزائري.">

  <!-- PWA & Mobile Meta -->
  <link rel="manifest" href="/manifest.json">
  <link rel="icon" type="image/svg+xml" href="/icon.svg">
  <meta name="theme-color" content="#e11d48">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="DealScout DZ">

  <!-- Tailwind CSS & Icons -->
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
          },
          colors: {
            brand: {
              50: '#fff1f2',
              100: '#ffe4e6',
              500: '#f43f5e',
              600: '#e11d48',
              700: '#be123c',
              800: '#9f1239',
              900: '#881337',
            }
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
    .glass-card {
      background: rgba(15, 23, 42, 0.75);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .glass-card:hover {
      border-color: rgba(244, 63, 94, 0.4);
      box-shadow: 0 10px 30px -10px rgba(225, 29, 72, 0.25);
    }
    .deal-card-transition {
      transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .deal-card-transition:hover {
      transform: translateY(-3px);
    }
    .text-glow {
      text-shadow: 0 0 16px rgba(225, 29, 72, 0.45);
    }
    .text-glow-emerald {
      text-shadow: 0 0 16px rgba(16, 185, 129, 0.45);
    }
    .pb-safe {
      padding-bottom: calc(5.5rem + env(safe-area-inset-bottom, 0px));
    }
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #030712; }
    ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #e11d48; }
    @keyframes pulseGlow {
      0%, 100% { opacity: 0.6; transform: scale(1); }
      50% { opacity: 1; transform: scale(1.05); }
    }
    .pulse-glow {
      animation: pulseGlow 2.5s infinite ease-in-out;
    }
  </style>
</head>
<body class="min-h-screen bg-slate-950 text-slate-100 flex flex-col justify-between selection:bg-rose-500 selection:text-white">

  <!-- Ambient Background Glows -->
  <div class="fixed top-0 left-1/2 -translate-x-1/2 w-full max-w-7xl h-96 bg-gradient-to-b from-rose-600/15 via-amber-500/10 to-transparent blur-3xl pointer-events-none -z-10"></div>
  <div class="fixed bottom-0 left-1/4 w-96 h-96 bg-emerald-500/5 blur-3xl pointer-events-none -z-10"></div>

  <!-- Header / Navigation -->
  <header class="glass-card sticky top-0 z-40 border-b border-slate-800/80 px-4 py-3">
    <div class="max-w-7xl mx-auto flex items-center justify-between gap-3">
      
      <!-- Brand & Channel Badge -->
      <div class="flex items-center space-x-3 space-x-reverse">
        <a href="/" class="flex items-center gap-2.5 group">
          <div class="w-10 h-10 rounded-2xl bg-gradient-to-tr from-rose-600 via-rose-500 to-amber-500 flex items-center justify-center font-black text-white shadow-lg shadow-rose-600/30 group-hover:scale-105 transition">
            <i class="fa-solid fa-bolt text-lg"></i>
          </div>
          <div>
            <div class="flex items-center gap-2">
              <h1 class="font-black text-lg text-white font-inter tracking-tight">DealScout<span class="text-rose-500">DZ</span></h1>
              <span class="bg-emerald-500/15 text-emerald-400 text-[10px] font-bold px-2 py-0.5 rounded-full border border-emerald-500/30 flex items-center gap-1">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping"></span>
                <span>مباشر</span>
              </span>
            </div>
            <p class="text-[11px] text-slate-400 font-medium">عروض وتخفيضات AliExpress الجزائر 🇩🇿</p>
          </div>
        </a>
      </div>

      <!-- Live Exchange Rate & Actions -->
      <div class="flex items-center space-x-2 space-x-reverse">
        
        <!-- Live USDT Exchange Rate Pill -->
        <a href="https://squarealgerie.com" target="_blank" title="سعر صرف USDT في السوق الموازية (Square Algerie)" class="hidden sm:flex items-center gap-1.5 bg-slate-900 hover:bg-slate-800 border border-slate-800 text-xs px-3 py-1.5 rounded-xl transition text-slate-200">
          <i class="fa-solid fa-coins text-amber-400"></i>
          <span>1 USDT ≈ <b id="usdt-rate-badge" class="text-emerald-400 font-mono">249.0</b> دج</span>
        </a>

        <!-- Coin Bot Link -->
        <a href="https://t.me/Alilo07BOT" target="_blank" class="hidden md:flex items-center gap-1.5 bg-amber-500/10 hover:bg-amber-500/20 border border-amber-500/30 text-amber-300 text-xs px-3 py-1.5 rounded-xl font-bold transition">
          <i class="fa-solid fa-robot"></i>
          <span>بوت العملات @Alilo07BOT</span>
        </a>

        <!-- Telegram Channel Direct CTA -->
        <a id="header-telegram-join" href="https://t.me/DzAliexpress0" target="_blank" class="bg-gradient-to-r from-sky-500 to-blue-600 hover:from-sky-400 hover:to-blue-500 text-white text-xs px-3.5 py-1.5 rounded-xl font-bold shadow-lg shadow-sky-500/25 flex items-center gap-1.5 transition active:scale-95">
          <i class="fa-brands fa-telegram text-sm"></i>
          <span class="hidden sm:inline">انضم للقناة</span>
          <span id="channel-name-badge" class="text-[10px] bg-white/20 px-1.5 py-0.5 rounded">@DzAliexpress0</span>
        </a>

        <!-- Refresh Button -->
        <button onclick="fetchDeals(true)" id="refresh-deals-btn" title="تحديث الصفقات" class="bg-slate-900 hover:bg-slate-800 text-slate-300 text-xs p-2 rounded-xl border border-slate-800 flex items-center justify-center transition active:scale-95">
          <i class="fa-solid fa-rotate-right" id="refresh-icon"></i>
        </button>
      </div>

    </div>
  </header>

  <!-- Main Container -->
  <main class="max-w-7xl mx-auto px-4 py-5 space-y-6 pb-safe w-full">

    <!-- Hero Banner with Live Search & Channel Switcher -->
    <div class="relative overflow-hidden rounded-3xl p-6 sm:p-8 bg-gradient-to-br from-slate-900 via-slate-900/90 to-slate-950 border border-slate-800 shadow-2xl">
      <div class="relative z-10 max-w-3xl space-y-4">
        
        <!-- Live Ticker Tag -->
        <div class="inline-flex items-center gap-2 bg-rose-500/10 border border-rose-500/25 text-rose-300 text-xs font-bold px-3 py-1 rounded-full">
          <i class="fa-solid fa-fire text-amber-400 animate-bounce"></i>
          <span>صفقات حصرية ومحدثة لحظة بلحظة مع أكواد الخصم والعملات</span>
        </div>

        <h2 class="text-2xl sm:text-4xl font-extrabold text-white leading-tight">
          كل عروض <span class="bg-gradient-to-r from-rose-500 via-amber-400 to-rose-400 bg-clip-text text-transparent">AliExpress</span> المنشورة في القناة، بين يديك!
        </h2>
        <p class="text-xs sm:text-sm text-slate-400 leading-relaxed max-w-2xl">
          تصفح الصفقات اليومية، احصل على روابط الشراء المباشرة التابعة، انسخ أكواد الخصم بضغطة زر، وتعرف على السعر الحقيقي بالدينار الجزائري حسب سعر الصرف في السكوار.
        </p>

        <!-- Channel Switcher Buttons -->
        <div class="flex flex-wrap items-center gap-2 pt-2">
          <button onclick="switchChannel('@DzAliexpress0')" id="tab-dz" class="channel-tab-btn bg-gradient-to-r from-rose-600 to-amber-600 text-white font-bold text-xs sm:text-sm px-4 py-2 rounded-xl shadow-lg shadow-rose-600/20 flex items-center gap-2 transition active:scale-95">
            <span>🇩🇿 عروض الجزائر (@DzAliexpress0)</span>
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
          </button>
          <button onclick="switchChannel('@francedealsdz')" id="tab-fr" class="channel-tab-btn bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold text-xs sm:text-sm px-4 py-2 rounded-xl border border-slate-700 flex items-center gap-2 transition active:scale-95">
            <span>🇫🇷 عروض فرنسا (@francedealsdz)</span>
          </button>
        </div>

        <!-- Search Bar & Currency Selector -->
        <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-2 pt-2">
          <div class="relative flex-1">
            <i class="fa-solid fa-magnifying-glass absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 text-sm"></i>
            <input 
              type="text" 
              id="deal-search-input" 
              oninput="filterDeals()" 
              placeholder="ابحث عن هاتف، ماوس، سماعات، شاحن، كود خصم، علامة تجارية..." 
              class="w-full bg-slate-950/90 border border-slate-700/80 rounded-2xl pr-11 pl-4 py-3 text-xs sm:text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500 transition shadow-inner"
            />
          </div>

          <!-- Currency Selector Toggle -->
          <div class="flex items-center bg-slate-950/90 border border-slate-800 rounded-2xl p-1 gap-1 flex-shrink-0 self-end sm:self-auto">
            <button onclick="setCurrency('DZD')" id="curr-dzd" class="curr-btn bg-rose-600 text-white text-xs px-3 py-2 rounded-xl font-bold transition">
              🇩🇿 دج (DZD)
            </button>
            <button onclick="setCurrency('USD')" id="curr-usd" class="curr-btn text-slate-400 hover:text-slate-200 text-xs px-3 py-2 rounded-xl font-bold transition">
              💵 $ (USD)
            </button>
            <button onclick="setCurrency('EUR')" id="curr-eur" class="curr-btn text-slate-400 hover:text-slate-200 text-xs px-3 py-2 rounded-xl font-bold transition">
              💶 € (EUR)
            </button>
          </div>
        </div>

      </div>
    </div>

    <!-- Category Pills & View Mode Bar -->
    <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-3">
      
      <!-- Category Chips -->
      <div class="flex items-center gap-1.5 overflow-x-auto w-full md:w-auto pb-1 no-scrollbar">
        <button onclick="setCategory('all')" id="cat-all" class="cat-chip bg-rose-600 text-white text-xs px-3.5 py-1.5 rounded-xl font-bold flex items-center gap-1.5 whitespace-nowrap transition active:scale-95 shadow">
          <span>🌟 الكل</span>
          <span id="count-all" class="text-[10px] bg-white/20 px-1.5 py-0.2 rounded-full">0</span>
        </button>
        <button onclick="setCategory('smartphones')" id="cat-smartphones" class="cat-chip bg-slate-900 hover:bg-slate-800 text-slate-300 text-xs px-3.5 py-1.5 rounded-xl font-bold flex items-center gap-1.5 whitespace-nowrap border border-slate-800 transition active:scale-95">
          <span>📱 هواتف ذكية</span>
          <span id="count-smartphones" class="text-[10px] bg-slate-800 px-1.5 py-0.2 rounded-full text-slate-400">0</span>
        </button>
        <button onclick="setCategory('gaming')" id="cat-gaming" class="cat-chip bg-slate-900 hover:bg-slate-800 text-slate-300 text-xs px-3.5 py-1.5 rounded-xl font-bold flex items-center gap-1.5 whitespace-nowrap border border-slate-800 transition active:scale-95">
          <span>🎮 قيمنق وعَتاد</span>
          <span id="count-gaming" class="text-[10px] bg-slate-800 px-1.5 py-0.2 rounded-full text-slate-400">0</span>
        </button>
        <button onclick="setCategory('audio')" id="cat-audio" class="cat-chip bg-slate-900 hover:bg-slate-800 text-slate-300 text-xs px-3.5 py-1.5 rounded-xl font-bold flex items-center gap-1.5 whitespace-nowrap border border-slate-800 transition active:scale-95">
          <span>🎧 سماعات وصوتيات</span>
          <span id="count-audio" class="text-[10px] bg-slate-800 px-1.5 py-0.2 rounded-full text-slate-400">0</span>
        </button>
        <button onclick="setCategory('tech')" id="cat-tech" class="cat-chip bg-slate-900 hover:bg-slate-800 text-slate-300 text-xs px-3.5 py-1.5 rounded-xl font-bold flex items-center gap-1.5 whitespace-nowrap border border-slate-800 transition active:scale-95">
          <span>⚡ شواحن وملحقات</span>
          <span id="count-tech" class="text-[10px] bg-slate-800 px-1.5 py-0.2 rounded-full text-slate-400">0</span>
        </button>
        <button onclick="setCategory('tajmi3at')" id="cat-tajmi3at" class="cat-chip bg-slate-900 hover:bg-slate-800 text-slate-300 text-xs px-3.5 py-1.5 rounded-xl font-bold flex items-center gap-1.5 whitespace-nowrap border border-slate-800 transition active:scale-95">
          <span>📦 تجميعات العروض</span>
          <span id="count-tajmi3at" class="text-[10px] bg-slate-800 px-1.5 py-0.2 rounded-full text-slate-400">0</span>
        </button>
      </div>

      <!-- View Switcher (Cards Grid vs Telegram Stream) -->
      <div class="flex items-center gap-1 bg-slate-900 border border-slate-800 rounded-xl p-1 self-end md:self-auto flex-shrink-0">
        <button onclick="setViewMode('grid')" id="view-mode-grid" class="view-btn bg-slate-800 text-rose-400 text-xs px-2.5 py-1 rounded-lg font-bold flex items-center gap-1 transition">
          <i class="fa-solid fa-table-cells"></i>
          <span class="hidden sm:inline">شبكة البطاقات</span>
        </button>
        <button onclick="setViewMode('feed')" id="view-mode-feed" class="view-btn text-slate-400 hover:text-slate-200 text-xs px-2.5 py-1 rounded-lg font-bold flex items-center gap-1 transition">
          <i class="fa-brands fa-telegram"></i>
          <span class="hidden sm:inline">منشورات القناة</span>
        </button>
      </div>

    </div>

    <!-- Deals Grid Container -->
    <div id="deals-grid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
      <!-- Loading Skeleton Cards -->
      <div class="glass-card rounded-2xl p-4 animate-pulse space-y-3">
        <div class="w-full h-48 bg-slate-800 rounded-xl"></div>
        <div class="h-4 bg-slate-800 rounded w-3/4"></div>
        <div class="h-6 bg-slate-800 rounded w-1/2"></div>
        <div class="h-10 bg-slate-800 rounded-xl"></div>
      </div>
      <div class="glass-card rounded-2xl p-4 animate-pulse space-y-3">
        <div class="w-full h-48 bg-slate-800 rounded-xl"></div>
        <div class="h-4 bg-slate-800 rounded w-3/4"></div>
        <div class="h-6 bg-slate-800 rounded w-1/2"></div>
        <div class="h-10 bg-slate-800 rounded-xl"></div>
      </div>
      <div class="glass-card rounded-2xl p-4 animate-pulse space-y-3">
        <div class="w-full h-48 bg-slate-800 rounded-xl"></div>
        <div class="h-4 bg-slate-800 rounded w-3/4"></div>
        <div class="h-6 bg-slate-800 rounded w-1/2"></div>
        <div class="h-10 bg-slate-800 rounded-xl"></div>
      </div>
    </div>

    <!-- Telegram Feed Stream Container (Hidden by default) -->
    <div id="deals-feed" class="hidden max-w-2xl mx-auto space-y-4"></div>

    <!-- Empty State / No Deals Found -->
    <div id="empty-state" class="hidden glass-card rounded-3xl p-10 text-center space-y-3">
      <div class="w-16 h-16 rounded-2xl bg-rose-500/10 text-rose-400 mx-auto flex items-center justify-center text-3xl">
        <i class="fa-solid fa-magnifying-glass"></i>
      </div>
      <h3 class="font-bold text-lg text-white">لم يتم العثور على صفقات مطابقة</h3>
      <p class="text-xs text-slate-400">جرب البحث بكلمة أخرى أو تصفح باقي الأقسام.</p>
      <button onclick="resetFilters()" class="bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs px-4 py-2 rounded-xl transition">
        إعادة تعيين الفلاتر
      </button>
    </div>

    <!-- How It Works / Smart Shopping Guide for Algerians -->
    <section class="glass-card rounded-3xl p-6 sm:p-8 border border-slate-800 space-y-6">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-2xl bg-gradient-to-tr from-amber-500 to-rose-600 flex items-center justify-center text-white shadow-lg shadow-rose-600/30">
          <i class="fa-solid fa-lightbulb text-lg"></i>
        </div>
        <div>
          <h3 class="font-extrabold text-base sm:text-lg text-white">دليل الشراء والتوفير الأقصى في الجزائر 💡🇩🇿</h3>
          <p class="text-xs text-slate-400">كيفاش تشري بأقل سعر ممكن وتستفيد من الخصومات الإضافية؟</p>
        </div>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        
        <!-- Tip 1: Country Switch -->
        <div class="bg-slate-900/90 rounded-2xl p-4 border border-slate-800/80 space-y-2">
          <div class="w-8 h-8 rounded-xl bg-rose-500/10 text-rose-400 flex items-center justify-center font-bold text-sm">
            <i class="fa-solid fa-earth-americas"></i>
          </div>
          <h4 class="font-bold text-sm text-white">1. تحويل بلد الحساب</h4>
          <p class="text-xs text-slate-400 leading-relaxed">
            العديد من العروض تتطلب تحويل بلد الحساب في إعدادات التطبيق إلى (كندا 🇨🇦، كوريا 🇰🇷، أوكرانيا 🇺🇦) مع إبقاء عنوان الشحن نحو الجزائر 🇩🇿. هذا يفتح أسعار التصفية الحصرية!
          </p>
        </div>

        <!-- Tip 2: Coin Bot -->
        <div class="bg-slate-900/90 rounded-2xl p-4 border border-slate-800/80 space-y-2">
          <div class="w-8 h-8 rounded-xl bg-amber-500/10 text-amber-400 flex items-center justify-center font-bold text-sm">
            <i class="fa-solid fa-robot"></i>
          </div>
          <h4 class="font-bold text-sm text-white">2. تفعيل خصم العملات</h4>
          <p class="text-xs text-slate-400 leading-relaxed">
            استخدم بوتنا المجاني <a href="https://t.me/Alilo07BOT" target="_blank" class="text-amber-400 font-bold underline">@Alilo07BOT</a> لتحويل أي رابط للمنتج إلى صفحة الخصم الأقصى للعملات (تخفيض يصل حتى 70%).
          </p>
        </div>

        <!-- Tip 3: Payment Cards -->
        <div class="bg-slate-900/90 rounded-2xl p-4 border border-slate-800/80 space-y-2">
          <div class="w-8 h-8 rounded-xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center font-bold text-sm">
            <i class="fa-solid fa-credit-card"></i>
          </div>
          <h4 class="font-bold text-sm text-white">3. البطاقات البنكية المقبولة</h4>
          <p class="text-xs text-slate-400 leading-relaxed">
            يمكنك الدفع بسهولة من الجزائر باستعمال بطاقات فيزا وماستركارد الافتراضية مثل Bybit Card، RedotPay، Wise، أو بطاقات البنوك الجزائرية (بدر، القرض الشعبي).
          </p>
        </div>

      </div>
    </section>

  </main>

  <!-- Mobile Bottom Floating Navigation Bar -->
  <nav class="md:hidden glass-card fixed bottom-0 left-0 right-0 z-50 border-t border-slate-800/90 px-3 py-2 flex items-center justify-around">
    <button onclick="setCategory('all'); window.scrollTo({top: 0, behavior: 'smooth'});" class="flex flex-col items-center gap-1 text-rose-500 font-bold text-[11px]">
      <i class="fa-solid fa-bolt text-base"></i>
      <span>العروض</span>
    </button>
    <button onclick="setCategory('smartphones')" class="flex flex-col items-center gap-1 text-slate-400 hover:text-slate-200 text-[11px]">
      <i class="fa-solid fa-mobile-screen-button text-base"></i>
      <span>هواتف</span>
    </button>
    <button onclick="setCategory('gaming')" class="flex flex-col items-center gap-1 text-slate-400 hover:text-slate-200 text-[11px]">
      <i class="fa-solid fa-gamepad text-base"></i>
      <span>قيمنق</span>
    </button>
    <a href="https://t.me/Alilo07BOT" target="_blank" class="flex flex-col items-center gap-1 text-amber-400 text-[11px] font-bold">
      <i class="fa-solid fa-robot text-base"></i>
      <span>بوت العملات</span>
    </a>
    <a href="https://t.me/DzAliexpress0" target="_blank" class="flex flex-col items-center gap-1 text-sky-400 text-[11px] font-bold">
      <i class="fa-brands fa-telegram text-base"></i>
      <span>القناة</span>
    </a>
  </nav>

  <!-- Image Lightbox Modal -->
  <div id="image-modal" onclick="closeImageModal()" class="fixed inset-0 z-50 bg-black/90 backdrop-blur-md hidden flex items-center justify-center p-4">
    <div class="relative max-w-xl max-h-[90vh]">
      <img id="modal-img" src="" alt="Deal preview" class="w-full h-auto max-h-[85vh] object-contain rounded-2xl shadow-2xl">
      <button onclick="closeImageModal()" class="absolute top-3 left-3 bg-slate-900/80 hover:bg-slate-900 text-white w-9 h-9 rounded-full flex items-center justify-center text-sm border border-slate-700">
        <i class="fa-solid fa-xmark"></i>
      </button>
    </div>
  </div>

  <!-- Toast Notification -->
  <div id="toast" class="fixed bottom-20 md:bottom-6 left-1/2 -translate-x-1/2 z-50 bg-emerald-600 text-white font-bold text-xs sm:text-sm px-5 py-2.5 rounded-2xl shadow-2xl flex items-center gap-2 transform translate-y-20 opacity-0 pointer-events-none transition-all duration-300">
    <i class="fa-solid fa-circle-check"></i>
    <span id="toast-msg">تم نسخ الكود بنجاح!</span>
  </div>

  <!-- Footer -->
  <footer class="border-t border-slate-800/80 bg-slate-950 py-8 px-4 text-center text-xs text-slate-500 space-y-3">
    <div class="flex flex-wrap items-center justify-center gap-4 text-slate-400">
      <a href="https://t.me/DzAliexpress0" target="_blank" class="hover:text-rose-400 transition flex items-center gap-1.5">
        <i class="fa-brands fa-telegram text-sky-400"></i>
        <span>قناة الجزائر (@DzAliexpress0)</span>
      </a>
      <span>•</span>
      <a href="https://t.me/francedealsdz" target="_blank" class="hover:text-rose-400 transition flex items-center gap-1.5">
        <i class="fa-brands fa-telegram text-sky-400"></i>
        <span>قناة فرنسا (@francedealsdz)</span>
      </a>
      <span>•</span>
      <a href="https://t.me/Alilo07BOT" target="_blank" class="hover:text-rose-400 transition flex items-center gap-1.5">
        <i class="fa-solid fa-robot text-amber-400"></i>
        <span>بوت العملات (@Alilo07BOT)</span>
      </a>
      <span>•</span>
      <a href="https://squarealgerie.com" target="_blank" class="hover:text-rose-400 transition flex items-center gap-1.5">
        <i class="fa-solid fa-chart-line text-emerald-400"></i>
        <span>أسعار الصرف (Square Algerie)</span>
      </a>
    </div>
    <p>DealScout DZ — موقع عروض وتخفيضات AliExpress المباشرة من قنوات التيليجرام بالدينار الجزائري 🇩🇿</p>
    <p class="text-[11px] text-slate-600">جميع الروابط مؤمنة وتفتح موقع وتطبيق AliExpress الرسمي عبر برنامج الشراكة الرسمي AliExpress Portals Affiliate.</p>
  </footer>

  <!-- JavaScript Application Logic -->
  <script>
    let allDeals = [];
    let currentChannel = '@DzAliexpress0';
    let currentCategory = 'all';
    let currentCurrency = 'DZD';
    let currentViewMode = 'grid';
    let usdtRate = 249.0;

    // Toast helper
    function showToast(message) {
      const toast = document.getElementById('toast');
      const msg = document.getElementById('toast-msg');
      msg.textContent = message;
      toast.classList.remove('translate-y-20', 'opacity-0', 'pointer-events-none');
      setTimeout(() => {
        toast.classList.add('translate-y-20', 'opacity-0', 'pointer-events-none');
      }, 2500);
    }

    // Copy coupon code
    function copyCoupon(code, btn) {
      navigator.clipboard.writeText(code).then(() => {
        showToast('تم نسخ الكود: ' + code);
        const originalHtml = btn.innerHTML;
        btn.innerHTML = '<i class="fa-solid fa-check"></i> <span>تم النسخ!</span>';
        btn.classList.add('bg-emerald-600', 'text-white');
        setTimeout(() => {
          btn.innerHTML = originalHtml;
          btn.classList.remove('bg-emerald-600', 'text-white');
        }, 2000);
      }).catch(() => {
        showToast('كود الخصم: ' + code);
      });
    }

    // Image Modal
    function openImageModal(src) {
      document.getElementById('modal-img').src = src;
      document.getElementById('image-modal').classList.remove('hidden');
    }
    function closeImageModal() {
      document.getElementById('image-modal').classList.add('hidden');
    }

    // Currency Switcher
    function setCurrency(curr) {
      currentCurrency = curr;
      document.querySelectorAll('.curr-btn').forEach(btn => {
        btn.classList.remove('bg-rose-600', 'text-white');
        btn.classList.add('text-slate-400');
      });
      const activeBtn = document.getElementById('curr-' + curr.toLowerCase());
      if (activeBtn) {
        activeBtn.classList.add('bg-rose-600', 'text-white');
        activeBtn.classList.remove('text-slate-400');
      }
      renderDeals();
    }

    // Category Filter
    function setCategory(cat) {
      currentCategory = cat;
      document.querySelectorAll('.cat-chip').forEach(btn => {
        btn.classList.remove('bg-rose-600', 'text-white');
        btn.classList.add('bg-slate-900', 'text-slate-300');
      });
      const active = document.getElementById('cat-' + cat);
      if (active) {
        active.classList.add('bg-rose-600', 'text-white');
        active.classList.remove('bg-slate-900', 'text-slate-300');
      }
      filterDeals();
    }

    // View Mode Switcher (Grid vs Feed)
    function setViewMode(mode) {
      currentViewMode = mode;
      const gridBtn = document.getElementById('view-mode-grid');
      const feedBtn = document.getElementById('view-mode-feed');
      const gridEl = document.getElementById('deals-grid');
      const feedEl = document.getElementById('deals-feed');

      if (mode === 'grid') {
        gridBtn.classList.add('bg-slate-800', 'text-rose-400');
        gridBtn.classList.remove('text-slate-400');
        feedBtn.classList.remove('bg-slate-800', 'text-rose-400');
        feedBtn.classList.add('text-slate-400');
        gridEl.classList.remove('hidden');
        feedEl.classList.add('hidden');
      } else {
        feedBtn.classList.add('bg-slate-800', 'text-rose-400');
        feedBtn.classList.remove('text-slate-400');
        gridBtn.classList.remove('bg-slate-800', 'text-rose-400');
        gridBtn.classList.add('text-slate-400');
        feedEl.classList.remove('hidden');
        gridEl.classList.add('hidden');
      }
    }

    // Switch Channel
    function switchChannel(channel) {
      currentChannel = channel;
      const tabDz = document.getElementById('tab-dz');
      const tabFr = document.getElementById('tab-fr');
      const badge = document.getElementById('channel-name-badge');
      const joinBtn = document.getElementById('header-telegram-join');

      if (channel === '@DzAliexpress0') {
        tabDz.className = 'channel-tab-btn bg-gradient-to-r from-rose-600 to-amber-600 text-white font-bold text-xs sm:text-sm px-4 py-2 rounded-xl shadow-lg shadow-rose-600/20 flex items-center gap-2 transition active:scale-95';
        tabFr.className = 'channel-tab-btn bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold text-xs sm:text-sm px-4 py-2 rounded-xl border border-slate-700 flex items-center gap-2 transition active:scale-95';
        badge.textContent = '@DzAliexpress0';
        joinBtn.href = 'https://t.me/DzAliexpress0';
        currentCurrency = 'DZD';
      } else {
        tabFr.className = 'channel-tab-btn bg-gradient-to-r from-blue-600 to-sky-600 text-white font-bold text-xs sm:text-sm px-4 py-2 rounded-xl shadow-lg shadow-blue-600/20 flex items-center gap-2 transition active:scale-95';
        tabDz.className = 'channel-tab-btn bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold text-xs sm:text-sm px-4 py-2 rounded-xl border border-slate-700 flex items-center gap-2 transition active:scale-95';
        badge.textContent = '@francedealsdz';
        joinBtn.href = 'https://t.me/francedealsdz';
        currentCurrency = 'EUR';
      }
      setCurrency(currentCurrency);
      fetchDeals(false);
    }

    // Fetch Deals from Backend API
    async function fetchDeals(force = false) {
      const icon = document.getElementById('refresh-icon');
      if (icon) icon.classList.add('fa-spin');

      try {
        const resp = await fetch(`/api/deals?channel=${encodeURIComponent(currentChannel)}${force ? '&force=true' : ''}`);
        const data = await resp.json();
        
        if (data.usdt_rate) {
          usdtRate = data.usdt_rate;
          const badge = document.getElementById('usdt-rate-badge');
          if (badge) badge.textContent = usdtRate.toFixed(1);
        }

        allDeals = data.deals || [];
        updateCategoryCounts();
        filterDeals();

      } catch (err) {
        console.error('Error fetching deals:', err);
      } finally {
        if (icon) icon.classList.remove('fa-spin');
      }
    }

    // Update Category Badges Counts
    function updateCategoryCounts() {
      const counts = { all: allDeals.length, smartphones: 0, gaming: 0, audio: 0, tech: 0, tajmi3at: 0 };
      allDeals.forEach(d => {
        if (counts[d.category] !== undefined) {
          counts[d.category]++;
        }
      });
      for (const [cat, cnt] of Object.entries(counts)) {
        const el = document.getElementById('count-' + cat);
        if (el) el.textContent = cnt;
      }
    }

    // Filter Deals by Category & Search
    function filterDeals() {
      const q = (document.getElementById('deal-search-input').value || '').toLowerCase().trim();
      
      const filtered = allDeals.filter(d => {
        // Category filter
        if (currentCategory !== 'all' && d.category !== currentCategory) {
          return false;
        }
        // Search filter
        if (q) {
          const matchTitle = (d.title || '').toLowerCase().includes(q);
          const matchRaw = (d.raw_text || '').toLowerCase().includes(q);
          const matchCoupon = (d.coupon_code || '').toLowerCase().includes(q);
          const matchCountry = (d.country || '').toLowerCase().includes(q);
          if (!matchTitle && !matchRaw && !matchCoupon && !matchCountry) {
            return false;
          }
        }
        return true;
      });

      renderDeals(filtered);
      renderFeed(filtered);

      const empty = document.getElementById('empty-state');
      if (filtered.length === 0) {
        empty.classList.remove('hidden');
      } else {
        empty.classList.add('hidden');
      }
    }

    function resetFilters() {
      document.getElementById('deal-search-input').value = '';
      setCategory('all');
    }

    // Render Formatted Deal Price
    function formatPrice(deal) {
      if (currentCurrency === 'DZD') {
        if (deal.price_dzd) {
          return `<div class="flex items-baseline gap-1.5"><span class="text-xl sm:text-2xl font-black text-emerald-400 font-inter">${deal.price_dzd.toLocaleString()}</span><span class="text-xs text-slate-300 font-bold">دج</span></div>`;
        }
      } else if (currentCurrency === 'EUR') {
        if (deal.price_eur) {
          return `<div class="flex items-baseline gap-1"><span class="text-xl sm:text-2xl font-black text-sky-400 font-inter">${deal.price_eur.toFixed(2)}</span><span class="text-xs text-slate-300 font-bold">€</span></div>`;
        }
      } else {
        if (deal.price_usd) {
          return `<div class="flex items-baseline gap-1"><span class="text-xl sm:text-2xl font-black text-amber-400 font-inter">$${deal.price_usd.toFixed(2)}</span></div>`;
        }
      }

      // Fallback
      if (deal.price_dzd) return `<div class="flex items-baseline gap-1.5"><span class="text-xl sm:text-2xl font-black text-emerald-400 font-inter">${deal.price_dzd.toLocaleString()}</span><span class="text-xs text-slate-300 font-bold">دج</span></div>`;
      if (deal.price_usd) return `<div class="flex items-baseline gap-1"><span class="text-xl sm:text-2xl font-black text-amber-400 font-inter">$${deal.price_usd}</span></div>`;
      if (deal.price_eur) return `<div class="flex items-baseline gap-1"><span class="text-xl sm:text-2xl font-black text-sky-400 font-inter">${deal.price_eur}€</span></div>`;
      return `<span class="text-sm font-bold text-slate-400">سعر خاص</span>`;
    }

    // Render Deals in Grid View
    function renderDeals(dealsToRender = null) {
      const deals = dealsToRender !== null ? dealsToRender : allDeals;
      const grid = document.getElementById('deals-grid');
      grid.innerHTML = '';

      deals.forEach(deal => {
        const card = document.createElement('div');
        card.className = 'glass-card deal-card-transition rounded-3xl p-4 sm:p-5 flex flex-col justify-between border border-slate-800 shadow-xl relative overflow-hidden group';

        const photoHtml = deal.photo_url 
          ? `<div class="relative w-full h-52 sm:h-56 rounded-2xl overflow-hidden bg-slate-900 border border-slate-800 cursor-pointer flex items-center justify-center mb-3.5 group-hover:border-rose-500/30 transition" onclick="openImageModal('${deal.photo_url}')">
               <img src="${deal.photo_url}" alt="${deal.title}" loading="lazy" class="w-full h-full object-cover group-hover:scale-105 transition duration-300" />
               <div class="absolute inset-0 bg-gradient-to-t from-slate-950/80 via-transparent to-transparent"></div>
               <span class="absolute bottom-2 left-2 bg-black/60 backdrop-blur-md text-white text-[10px] px-2 py-0.5 rounded-lg flex items-center gap-1 border border-white/10">
                 <i class="fa-solid fa-expand text-[9px]"></i> تكبير
               </span>
               ${deal.country ? `<span class="absolute top-2.5 right-2.5 bg-slate-900/90 backdrop-blur-md text-slate-200 text-xs px-2.5 py-1 rounded-xl font-bold border border-slate-700/80 shadow-lg flex items-center gap-1.5"><i class="fa-solid fa-location-dot text-rose-500 text-[11px]"></i> ${deal.country}</span>` : ''}
               ${deal.has_coins ? `<span class="absolute top-2.5 left-2.5 bg-amber-500/90 text-slate-950 text-[10px] font-black px-2 py-0.5 rounded-lg shadow flex items-center gap-1"><i class="fa-solid fa-coins"></i> عملات</span>` : ''}
             </div>`
          : `<div class="w-full h-24 rounded-2xl bg-gradient-to-tr from-rose-950/30 to-amber-950/30 border border-slate-800 flex items-center justify-center mb-3.5">
               <i class="fa-solid fa-tags text-rose-500/40 text-3xl"></i>
             </div>`;

        const couponHtml = deal.coupon_code 
          ? `<div class="bg-rose-500/10 border border-rose-500/25 rounded-2xl p-2.5 flex items-center justify-between gap-2 mb-3.5">
               <div class="flex items-center gap-2">
                 <i class="fa-solid fa-ticket text-rose-400 text-sm"></i>
                 <div>
                   <div class="text-[10px] text-rose-300 font-bold">كود الخصم الفعّال</div>
                   <div class="font-mono font-bold text-xs sm:text-sm text-white tracking-wider">${deal.coupon_code}</div>
                 </div>
               </div>
               <button onclick="copyCoupon('${deal.coupon_code}', this)" class="bg-rose-600 hover:bg-rose-500 text-white text-xs px-3 py-1.5 rounded-xl font-bold flex items-center gap-1 transition active:scale-95 shadow">
                 <i class="fa-regular fa-copy"></i>
                 <span>نسخ</span>
               </button>
             </div>`
          : '';

        const secondaryPrice = deal.price_usd && currentCurrency === 'DZD' 
          ? `<span class="text-xs text-slate-400 font-mono">($${deal.price_usd.toFixed(2)})</span>`
          : (deal.price_dzd && currentCurrency !== 'DZD' ? `<span class="text-xs text-slate-400 font-mono">(${deal.price_dzd.toLocaleString()} دج)</span>` : '');

        card.innerHTML = `
          <div>
            ${photoHtml}
            <div class="flex items-center justify-between gap-2 mb-2">
              <span class="text-[11px] font-bold text-rose-400 bg-rose-500/10 border border-rose-500/20 px-2 py-0.5 rounded-lg">
                ${deal.category_label || 'عرض ترويجي'}
              </span>
              <span class="text-[10px] text-slate-500 font-mono flex items-center gap-1">
                <i class="fa-regular fa-clock"></i> ${deal.date || 'اليوم'}
              </span>
            </div>
            <h3 class="font-bold text-sm sm:text-base text-white leading-snug line-clamp-2 mb-3 hover:text-rose-400 transition cursor-pointer" onclick="window.open('${deal.affiliate_url}', '_blank')">
              ${deal.title}
            </h3>
            ${couponHtml}
          </div>

          <div class="pt-3 border-t border-slate-800/80 space-y-3">
            <div class="flex items-center justify-between gap-2">
              <div>
                <span class="text-[10px] text-slate-400 block font-bold">السعر النهائي:</span>
                <div class="flex items-center gap-2">
                  ${formatPrice(deal)}
                  ${secondaryPrice}
                </div>
              </div>
              ${deal.telegram_url ? `
                <a href="${deal.telegram_url}" target="_blank" title="عرض في تيليجرام" class="text-slate-400 hover:text-sky-400 p-2 rounded-xl border border-slate-800 hover:bg-slate-800 transition">
                  <i class="fa-brands fa-telegram text-base"></i>
                </a>
              ` : ''}
            </div>

            <!-- Primary Buy Button -->
            <a href="${deal.affiliate_url}" target="_blank" rel="noopener noreferrer" class="w-full bg-gradient-to-r from-rose-600 to-amber-600 hover:from-rose-500 hover:to-amber-500 text-white font-extrabold text-xs sm:text-sm py-2.5 px-4 rounded-xl shadow-lg shadow-rose-600/25 flex items-center justify-center gap-2 transition active:scale-98">
              <i class="fa-solid fa-cart-shopping"></i>
              <span>اشتري الآن من AliExpress</span>
              <i class="fa-solid fa-arrow-left text-xs"></i>
            </a>
          </div>
        `;

        grid.appendChild(card);
      });
    }

    // Render Authentic Telegram Feed Stream View
    function renderFeed(dealsToRender = null) {
      const deals = dealsToRender !== null ? dealsToRender : allDeals;
      const feed = document.getElementById('deals-feed');
      feed.innerHTML = '';

      deals.forEach(deal => {
        const bubble = document.createElement('div');
        bubble.className = 'glass-card rounded-3xl p-5 border border-slate-800 space-y-3 relative overflow-hidden';

        const formattedText = (deal.raw_text || '')
          .replace(/\\n/g, '<br>')
          .replace(/(https?:\\/\\/s\\.click\\.aliexpress\\.com\\/e\\/[A-Za-z0-9_-]+)/g, '<a href="$1" target="_blank" class="text-rose-400 underline font-bold break-all">$1</a>')
          .replace(/(@[A-Za-z0-9_]+)/g, '<span class="text-sky-400 font-bold">$1</span>');

        bubble.innerHTML = `
          <!-- Telegram Post Header -->
          <div class="flex items-center justify-between pb-3 border-b border-slate-800">
            <div class="flex items-center gap-2.5">
              <div class="w-9 h-9 rounded-full bg-gradient-to-tr from-rose-600 to-amber-500 flex items-center justify-center text-white font-bold text-sm">
                <i class="fa-brands fa-telegram"></i>
              </div>
              <div>
                <div class="flex items-center gap-1.5">
                  <h4 class="font-bold text-sm text-white">${currentChannel.replace('@', '')}</h4>
                  <i class="fa-solid fa-circle-check text-sky-400 text-xs"></i>
                </div>
                <span class="text-[11px] text-slate-500">${deal.date || 'اليوم'}</span>
              </div>
            </div>
            ${deal.telegram_url ? `<a href="${deal.telegram_url}" target="_blank" class="text-xs text-sky-400 hover:underline flex items-center gap-1 font-bold"><i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i> فتح بالتيليجرام</a>` : ''}
          </div>

          <!-- Telegram Photo -->
          ${deal.photo_url ? `
            <div class="rounded-2xl overflow-hidden border border-slate-800 max-h-96 cursor-pointer" onclick="openImageModal('${deal.photo_url}')">
              <img src="${deal.photo_url}" alt="Post image" loading="lazy" class="w-full h-auto object-cover hover:scale-102 transition duration-200">
            </div>
          ` : ''}

          <!-- Telegram Post Body -->
          <div class="text-xs sm:text-sm text-slate-200 leading-relaxed font-sans select-text">
            ${formattedText}
          </div>

          <!-- Direct Buy Action Bar -->
          <div class="pt-2 flex flex-wrap gap-2">
            <a href="${deal.affiliate_url}" target="_blank" class="flex-1 bg-gradient-to-r from-rose-600 to-amber-600 hover:from-rose-500 hover:to-amber-500 text-white font-bold text-xs py-2.5 px-4 rounded-xl text-center flex items-center justify-center gap-2 shadow-lg shadow-rose-600/25">
              <i class="fa-solid fa-cart-shopping"></i>
              <span>رابط الشراء على AliExpress</span>
            </a>
            <a href="https://t.me/Alilo07BOT" target="_blank" class="bg-slate-800 hover:bg-slate-700 text-amber-300 font-bold text-xs py-2.5 px-4 rounded-xl flex items-center gap-1.5 border border-slate-700">
              <i class="fa-solid fa-coins"></i>
              <span>بوت العملات</span>
            </a>
          </div>
        `;

        feed.appendChild(bubble);
      });
    }

    // Auto load on start
    document.addEventListener('DOMContentLoaded', () => {
      fetchDeals();
      // Auto refresh deals every 3 minutes
      setInterval(() => fetchDeals(false), 180000);
    });
  </script>

</body>
</html>"""

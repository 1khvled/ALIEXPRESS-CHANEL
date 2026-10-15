"""
DealScout DZ — Admin Dashboard Interface
Professional administration suite for managing Telegram deal publishing, link inspection,
live channel feed monitoring, and auto-publishing schedule controls.
Styled with the platform's obsidian dark theme tokens, dot-matrix architectural textures,
and crisp typography (Cairo, Readex Pro, Plus Jakarta Sans, JetBrains Mono).
"""

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="ar" dir="rtl" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, viewport-fit=cover">
  <meta name="referrer" content="no-referrer">
  <title>لوحة تحكم الأدمن | DealScout DZ Admin</title>
  
  <!-- PWA & Mobile Metadata -->
  <link rel="manifest" href="/manifest.json">
  <link rel="icon" type="image/png" href="/logo_circular.png">
  <link rel="shortcut icon" href="/logo_circular.png">
  <link rel="apple-touch-icon" href="/logo_circular.png">
  <meta name="theme-color" content="#06080d">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="DealScout Admin">
  <meta name="mobile-web-app-capable" content="yes">

  <!-- Production Stylesheets & Fonts -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Readex+Pro:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    if (typeof tailwind !== 'undefined') {
      tailwind.config = {
        darkMode: 'class',
        theme: {
          extend: {
            fontFamily: {
              sans: ['"Readex Pro"', '"Plus Jakarta Sans"', 'Cairo', 'sans-serif'],
              heading: ['Cairo', '"Readex Pro"', '"Plus Jakarta Sans"', 'sans-serif'],
              mono: ['"JetBrains Mono"', 'ui-monospace', 'monospace'],
              inter: ['"Plus Jakarta Sans"', 'sans-serif']
            },
            colors: {
              obsidian: {
                950: '#06080d',
                900: '#0c1018',
                800: '#141a27',
                700: '#1e2638'
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
      --header-bg: rgba(9, 12, 19, 0.92);
      --input-bg: rgba(13, 17, 26, 0.95);
      --shadow-card: 0 4px 12px -2px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.06);
    }

    body {
      background-color: var(--bg-page);
      background-image: radial-gradient(rgba(255, 255, 255, 0.08) 1px, transparent 1px);
      background-size: 24px 24px;
      color: var(--text-main);
      font-family: 'Readex Pro', 'Cairo', 'Plus Jakarta Sans', sans-serif;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      -webkit-tap-highlight-color: transparent;
      overflow-x: hidden !important;
    }

    .glass-panel {
      background: var(--bg-card);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid var(--border-card);
      box-shadow: var(--shadow-card);
    }

    .glass-glow {
      box-shadow: 0 0 25px -5px rgba(225, 29, 72, 0.18), inset 0 1px 0 rgba(255, 255, 255, 0.08);
    }

    .card-hover {
      transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .card-hover:hover {
      background: var(--bg-card-hover);
      border-color: rgba(244, 63, 94, 0.35);
      transform: translateY(-2px);
      box-shadow: 0 12px 32px -8px rgba(0, 0, 0, 0.65);
    }

    .pb-safe {
      padding-bottom: calc(5rem + var(--sab));
    }

    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: #06080d; }
    ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #334155; }
  </style>
</head>
<body class="min-h-screen text-slate-100 flex flex-col justify-between selection:bg-rose-500 selection:text-white">

  <!-- Ambient Glow Background -->
  <div class="fixed top-0 left-1/2 -translate-x-1/2 w-full max-w-7xl h-96 bg-gradient-to-b from-rose-600/10 via-amber-500/5 to-transparent blur-3xl pointer-events-none -z-10"></div>

  <!-- Header -->
  <header class="glass-panel sticky top-0 z-40 border-b border-white/10 px-4 py-3">
    <div class="max-w-7xl mx-auto flex items-center justify-between gap-3">
      
      <!-- Brand & Info -->
      <div class="flex items-center space-x-3 space-x-reverse">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-rose-600 via-rose-500 to-amber-500 flex items-center justify-center font-bold text-white shadow-lg shadow-rose-600/25 border border-white/10">
          <i class="fa-solid fa-bolt text-lg"></i>
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="font-extrabold text-lg text-white font-heading tracking-tight">DealScout<span class="text-rose-500">DZ</span></h1>
            <span class="bg-rose-500/10 text-rose-400 text-[10px] font-bold px-2 py-0.5 rounded-full border border-rose-500/20">ADMIN LIVE</span>
          </div>
          <p class="text-[11px] text-slate-400">@DzAliexpress0 • تتبع وإدارة صفقات الجزائر وفرنسا</p>
        </div>
      </div>

      <!-- Action buttons -->
      <div class="flex items-center space-x-2 space-x-reverse">
        
        <!-- Instant Trigger Button (Solves missed deals queue delay) -->
        <button 
          onclick="triggerCollector()" 
          id="trigger-btn" 
          title="تشغيل فحص ونشر العروض فوراً دون انتظار المؤقت التلقائي"
          class="bg-gradient-to-r from-rose-600 to-amber-600 hover:from-rose-500 hover:to-amber-500 text-white text-xs px-3.5 py-2 rounded-xl font-bold shadow-lg shadow-rose-600/25 flex items-center gap-1.5 transition active:scale-95 border border-rose-400/20"
        >
          <i class="fa-solid fa-rocket" id="trigger-btn-icon"></i>
          <span class="hidden sm:inline" id="trigger-btn-text">تشغيل الفحص الآن ⚡</span>
        </button>

        <!-- Live USDT Badge -->
        <a href="https://squarealgerie.com" target="_blank" class="hidden md:flex items-center gap-1.5 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs px-3 py-1.5 rounded-xl hover:bg-emerald-500/20 transition">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>1 USDT ≈ <b id="header-usdt-rate">249.0</b> دج</span>
        </a>

        <!-- Install PWA Button (Hidden until prompt available) -->
        <button id="pwa-install-btn" class="hidden bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs px-3 py-1.5 rounded-xl font-bold border border-white/10 flex items-center gap-1.5 transition active:scale-95">
          <i class="fa-solid fa-download"></i>
          <span>تثبيت</span>
        </button>

        <!-- Return to User Site -->
        <a href="/" target="_blank" title="عرض موقع العروض العام" class="bg-slate-800/80 hover:bg-slate-700 text-slate-300 text-xs px-3 py-2 rounded-xl border border-white/10 flex items-center gap-1.5 transition">
          <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
          <span class="hidden sm:inline">موقع العروض</span>
        </a>

        <!-- Refresh Button -->
        <button onclick="refreshDashboard()" id="refresh-btn" class="bg-slate-800/80 hover:bg-slate-700 text-slate-200 text-xs px-3 py-2 rounded-xl border border-white/10 flex items-center gap-1.5 transition active:scale-95">
          <i class="fa-solid fa-arrows-rotate" id="refresh-icon"></i>
          <span class="hidden sm:inline">تحديث</span>
        </button>

        <!-- Logout Button -->
        <a href="/api/admin/logout" title="تسجيل الخروج" class="bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 text-xs px-3 py-2 rounded-xl border border-rose-500/20 flex items-center gap-1.5 transition active:scale-95">
          <i class="fa-solid fa-right-from-bracket"></i>
          <span class="hidden sm:inline">خروج</span>
        </a>
      </div>
    </div>
  </header>

  <!-- Global Action Notification Toast -->
  <div id="action-toast" class="fixed top-16 left-1/2 -translate-x-1/2 z-50 hidden transition-all duration-300 max-w-md w-full px-4">
    <div id="action-toast-body" class="p-3.5 rounded-2xl text-xs font-bold shadow-2xl flex items-center justify-between gap-3 border">
      <div class="flex items-center gap-2">
        <i id="action-toast-icon" class="fa-solid fa-circle-check text-sm"></i>
        <span id="action-toast-text">تم تنفيذ الإجراء بنجاح</span>
      </div>
      <button onclick="document.getElementById('action-toast').classList.add('hidden')" class="opacity-70 hover:opacity-100 p-1">
        <i class="fa-solid fa-xmark"></i>
      </button>
    </div>
  </div>

  <!-- Main Container -->
  <main class="max-w-7xl mx-auto px-4 py-5 space-y-6 pb-safe w-full">

    <!-- Interactive Deal Scout Tool (Instant Link Inspector) -->
    <div class="glass-panel glass-glow rounded-3xl p-4 sm:p-6 border border-rose-500/20">
      <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 mb-3">
        <div class="flex items-center gap-2.5">
          <div class="w-9 h-9 rounded-xl bg-rose-500/10 border border-rose-500/20 flex items-center justify-center text-rose-400">
            <i class="fa-solid fa-magnifying-glass-dollar text-base"></i>
          </div>
          <div>
            <h2 class="text-sm sm:text-base font-bold text-white font-heading">فاحص ومحول روابط AliExpress الفوري 🔍</h2>
            <p class="text-[11px] text-slate-400">تحويل أي رابط عادي لرابط تابع مخصص وكشف نسبة خصم العملات</p>
          </div>
        </div>
        <span class="text-[11px] text-slate-400 bg-white/5 border border-white/5 px-2.5 py-1 rounded-lg">يدعم روابط التطبيق، المتصفح، أو رقم المنتج</span>
      </div>

      <div class="flex flex-col sm:flex-row gap-2">
        <input 
          type="text" 
          id="scout-url-input" 
          placeholder="ألصق أي رابط أو كود منتج من AliExpress هنا..." 
          dir="ltr"
          class="flex-1 bg-black/40 border border-white/10 rounded-xl px-4 py-2.5 text-xs sm:text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500 font-mono transition"
        />
        <button 
          onclick="scoutDeal()" 
          id="scout-submit-btn" 
          class="bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs sm:text-sm px-5 py-2.5 rounded-xl shadow-lg shadow-rose-600/30 flex items-center justify-center gap-2 transition active:scale-95 border border-rose-400/20"
        >
          <i class="fa-solid fa-wand-magic-sparkles"></i>
          <span>فحص العرض</span>
        </button>
      </div>

      <!-- Scout Result Card -->
      <div id="scout-result" class="hidden mt-4 pt-4 border-t border-white/10">
        <div class="bg-black/30 rounded-2xl p-4 border border-white/10 flex flex-col md:flex-row items-start gap-4">
          <div id="scout-img-box" class="w-24 h-24 rounded-xl bg-slate-900 border border-white/10 flex-shrink-0 overflow-hidden flex items-center justify-center">
            <i class="fa-solid fa-image text-slate-600 text-2xl"></i>
          </div>
          <div class="flex-1 min-w-0 space-y-2">
            <h4 id="scout-title" class="font-bold text-sm text-white line-clamp-2"></h4>
            <div class="flex flex-wrap items-center gap-2 text-xs">
              <span id="scout-price-usd" class="text-emerald-400 font-bold bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 rounded-md font-mono"></span>
              <span id="scout-price-eur" class="text-sky-400 font-bold bg-sky-500/10 border border-sky-500/20 px-2 py-0.5 rounded-md font-mono hidden"></span>
              <span id="scout-price-dzd" class="text-amber-400 font-bold bg-amber-500/10 border border-amber-500/20 px-2 py-0.5 rounded-md font-mono"></span>
              <span id="scout-pid" class="text-slate-400 text-[11px] font-mono"></span>
            </div>
            <div class="flex flex-wrap gap-2 pt-1">
              <a id="scout-direct-link" href="#" target="_blank" class="bg-white/5 hover:bg-white/10 border border-white/10 text-white text-xs px-3 py-1.5 rounded-lg flex items-center gap-1.5 transition">
                <i class="fa-solid fa-cart-shopping text-rose-400"></i>
                <span>رابط الشراء المباشر</span>
              </a>
              <a id="scout-coin-link" href="#" target="_blank" class="bg-rose-600 hover:bg-rose-500 text-white text-xs px-3 py-1.5 rounded-lg flex items-center gap-1.5 transition shadow">
                <i class="fa-solid fa-coins text-amber-300"></i>
                <span>رابط تخفيض العملات</span>
              </a>
              <button onclick="copyScoutToReformatter()" class="bg-gradient-to-r from-amber-600 to-rose-600 hover:from-amber-500 hover:to-rose-500 text-white text-xs px-3 py-1.5 rounded-lg flex items-center gap-1.5 font-bold transition active:scale-95 shadow">
                <i class="fa-solid fa-wand-magic-sparkles"></i>
                <span>توليد ونشر المنشور ⚡</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Telegram Post Reformatter & 1-Tap Publisher Tool -->
    <div class="glass-panel rounded-3xl p-5 sm:p-6 card-hover border border-rose-500/30">
      <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-4 pb-3 border-b border-white/10">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-2xl bg-gradient-to-tr from-amber-500 to-rose-600 flex items-center justify-center text-white shadow-lg shadow-rose-600/30">
            <i class="fa-solid fa-wand-magic-sparkles text-lg"></i>
          </div>
          <div>
            <h3 class="font-bold text-base sm:text-lg text-white font-heading flex items-center gap-2">
              <span>إعادة تنسيق ونشر عروض التيليجرام ⚡</span>
              <span class="text-[10px] px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-300 border border-rose-500/30 font-bold">VIP للأدمن</span>
            </h3>
            <p class="text-xs text-slate-400">ألصق منشور أي قناة منافسة وسيقوم النظام فوراً باستخراج المنتج وتوليد الروابط التابعة وإعادة الصياغة باللهجة الجزائرية ثم النشر بضغطة زر!</p>
          </div>
        </div>
      </div>

      <div class="space-y-3">
        <textarea 
          id="reformat-input" 
          rows="4" 
          placeholder="ألصق هنا المنشور كما هو من قناة التيليجرام (يحتوي على رابط AliExpress، السعر، الكوبون...)" 
          dir="auto"
          class="w-full bg-black/40 border border-white/10 rounded-2xl p-3.5 text-xs sm:text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500 font-sans leading-relaxed transition"
        ></textarea>

        <div class="flex flex-wrap items-center justify-between gap-2">
          <button 
            onclick="reformatTelegramPost()" 
            id="reformat-submit-btn" 
            class="bg-gradient-to-r from-rose-600 to-amber-600 hover:from-rose-500 hover:to-amber-500 text-white font-bold text-xs sm:text-sm px-6 py-2.5 rounded-xl shadow-lg shadow-rose-600/30 flex items-center justify-center gap-2 transition active:scale-95 border border-rose-400/20"
          >
            <i class="fa-solid fa-arrows-rotate"></i>
            <span>إعادة التنسيق والمعاينة</span>
          </button>
          <button 
            onclick="document.getElementById('reformat-input').value=''; document.getElementById('reformat-result').classList.add('hidden');" 
            class="text-xs text-slate-400 hover:text-slate-200 px-3 py-1.5 rounded-lg border border-white/10 hover:bg-white/5 transition"
          >
            مسح الحقل
          </button>
        </div>
      </div>

      <!-- Reformatted Result Card -->
      <div id="reformat-result" class="hidden mt-5 pt-5 border-t border-white/10 space-y-4">
        <div class="bg-black/30 rounded-2xl p-4 border border-white/10 flex flex-col md:flex-row items-start gap-4">
          <!-- Image Box & Selectors -->
          <div class="flex flex-col items-center gap-2 w-full md:w-auto">
            <div id="reformat-img-box" class="w-32 h-32 rounded-xl bg-slate-900 border border-white/10 overflow-hidden flex items-center justify-center flex-shrink-0">
              <i class="fa-solid fa-image text-slate-600 text-3xl"></i>
            </div>
            <div id="reformat-gallery" class="flex flex-wrap gap-1 max-w-[140px] justify-center"></div>
          </div>

          <!-- Content Details & Editable Caption -->
          <div class="flex-1 min-w-0 w-full space-y-3">
            <div class="flex flex-wrap items-center justify-between gap-2">
              <div class="flex items-center gap-2">
                <span id="reformat-pid" class="text-xs font-mono bg-white/5 text-slate-300 px-2.5 py-0.5 rounded-md border border-white/10"></span>
                <span id="reformat-target-channel-badge" class="text-xs font-bold px-2.5 py-0.5 rounded-md border border-emerald-500/20 bg-emerald-500/10 text-emerald-300">@DzAliexpress0</span>
              </div>
              <div class="flex items-center gap-2 font-mono">
                <span id="reformat-price-usd" class="text-emerald-400 font-bold bg-emerald-500/10 border border-emerald-500/20 px-2.5 py-0.5 rounded-md text-xs"></span>
                <span id="reformat-price-eur" class="text-sky-400 font-bold bg-sky-500/10 border border-sky-500/20 px-2.5 py-0.5 rounded-md text-xs hidden"></span>
                <span id="reformat-price-dzd" class="text-amber-400 font-bold bg-amber-500/10 border border-amber-500/20 px-2.5 py-0.5 rounded-md text-xs"></span>
              </div>
            </div>

            <!-- Editable Caption Box -->
            <div>
              <div class="flex items-center justify-between mb-1">
                <label id="reformat-caption-label" class="text-[11px] font-bold text-slate-300">نص المنشور المنسق (يمكنك التعديل عليه قبل النشر):</label>
                <span class="text-[10px] text-slate-500 font-mono" id="reformat-char-count"></span>
              </div>
              <textarea 
                id="reformat-caption" 
                rows="8" 
                dir="rtl"
                class="w-full bg-black/40 border border-white/10 rounded-xl p-3 text-xs sm:text-sm text-slate-100 focus:outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500 font-sans leading-relaxed"
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
                class="bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs sm:text-sm px-6 py-2.5 rounded-xl shadow-lg shadow-emerald-600/30 flex items-center justify-center gap-2 transition active:scale-95 border border-emerald-400/20"
              >
                <i class="fa-solid fa-paper-plane"></i>
                <span id="reformat-publish-btn-text">نشر في القناة الآن (@DzAliexpress0)</span>
              </button>
            </div>

            <!-- Feedback Notification Box -->
            <div id="reformat-feedback" class="hidden p-3 rounded-xl text-xs font-medium"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Auto-Publishing Speed & Schedule Control Panel -->
    <div class="glass-panel rounded-3xl p-5 sm:p-6 card-hover border border-rose-500/20">
      <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-4 pb-3 border-b border-white/10">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-rose-600 to-amber-500 flex items-center justify-center text-white shadow-lg shadow-rose-600/30">
            <i class="fa-solid fa-gauge-high"></i>
          </div>
          <div>
            <h3 class="font-bold text-sm sm:text-base text-white font-heading flex items-center gap-2">
              <span>سرعة وتوقيت النشر التلقائي</span>
              <span id="sched-badge-status" class="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-bold">نشط</span>
            </h3>
            <p class="text-[11px] text-slate-400">تحكم فوري في الفاصل الزمني بين كل دورة فحص للمنافسين (نهاراً وليلاً)</p>
          </div>
        </div>
        <div id="sched-current-summary" class="text-xs text-rose-300 font-bold bg-black/40 border border-white/10 px-3 py-1.5 rounded-xl font-mono">
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
          <button onclick="setSpeed(10)" id="btn-speed-10" class="speed-btn bg-white/5 hover:bg-white/10 text-slate-300 font-bold text-xs py-2 px-3 rounded-xl border border-white/10 transition flex items-center justify-center gap-1.5 active:scale-95">
            <i class="fa-solid fa-rocket"></i>
            <span>كل 10 دقائق</span>
          </button>
          <button onclick="setSpeed(15)" id="btn-speed-15" class="speed-btn bg-white/5 hover:bg-white/10 text-slate-300 font-bold text-xs py-2 px-3 rounded-xl border border-white/10 transition flex items-center justify-center gap-1.5 active:scale-95">
            <i class="fa-solid fa-scale-balanced"></i>
            <span>كل 15 دقيقة</span>
          </button>
          <button onclick="setSpeed(30)" id="btn-speed-30" class="speed-btn bg-white/5 hover:bg-white/10 text-slate-300 font-bold text-xs py-2 px-3 rounded-xl border border-white/10 transition flex items-center justify-center gap-1.5 active:scale-95">
            <i class="fa-solid fa-clock"></i>
            <span>كل 30 دقيقة</span>
          </button>
        </div>

        <!-- Mode Switches -->
        <div class="flex flex-wrap items-center justify-between gap-3 pt-3 border-t border-white/10 text-xs">
          <button onclick="toggleNightMode()" id="btn-night-mode" class="bg-black/30 hover:bg-white/5 border border-white/10 text-slate-300 px-3 py-1.5 rounded-xl flex items-center gap-2 transition active:scale-95">
            <i class="fa-solid fa-moon text-indigo-400"></i>
            <span id="text-night-mode">الوضع الليلي: مفعّل (30د بعد منتصف الليل)</span>
          </button>
          <button onclick="togglePauseAuto()" id="btn-pause-auto" class="bg-black/30 hover:bg-white/5 border border-white/10 text-slate-300 px-3 py-1.5 rounded-xl flex items-center gap-2 transition active:scale-95">
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
        <div id="stat-total" class="text-xl sm:text-2xl font-black text-rose-400 font-mono">--</div>
        <span class="text-[10px] text-slate-500 mt-1 block">تحديث دوري من القناة</span>
      </div>

      <div class="glass-panel rounded-2xl p-4 card-hover">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span>عروض بالصور HD</span>
          <i class="fa-solid fa-image text-emerald-400"></i>
        </div>
        <div id="stat-photos" class="text-xl sm:text-2xl font-black text-emerald-400 font-mono">--</div>
        <span class="text-[10px] text-slate-500 mt-1 block">صور المنتجات الأصلية</span>
      </div>

      <div class="glass-panel rounded-2xl p-4 card-hover">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span>سعر صرف الـ USDT 🇩🇿</span>
          <i class="fa-solid fa-arrow-trend-up text-amber-400"></i>
        </div>
        <div id="stat-usdt" class="text-xl sm:text-2xl font-black text-amber-400 font-mono">249.0 دج</div>
        <a href="https://squarealgerie.com" target="_blank" class="text-[10px] text-slate-400 hover:text-amber-400 mt-1 block">SquareAlgerie.com</a>
      </div>

      <div class="glass-panel rounded-2xl p-4 card-hover">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span>حالة البوتات والمنظومة</span>
          <i class="fa-solid fa-robot text-sky-400"></i>
        </div>
        <div class="text-sm sm:text-base font-bold text-emerald-400 flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>تعمل بكفاءة 100%</span>
        </div>
        <span class="text-[10px] text-slate-500 mt-1 block font-mono">@Alilo07BOT • @DzAliexpress0</span>
      </div>
    </div>

    <!-- Main Content Layout -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

      <!-- Left 2 Cols: Posts Feed -->
      <div class="lg:col-span-2 space-y-4">
        <div class="flex items-center justify-between flex-wrap gap-2">
          <div class="flex items-center gap-2">
            <h3 class="font-bold text-base text-white font-heading">آخر العروض المنشورة</h3>
            <span id="posts-badge" class="bg-white/5 text-slate-300 text-xs px-2.5 py-0.5 rounded-full border border-white/10 font-mono">0</span>
          </div>
          <div class="flex items-center bg-black/40 border border-white/10 rounded-xl p-1 text-xs">
            <button onclick="switchFeedChannel('@DzAliexpress0')" id="feed-btn-dz" class="px-3 py-1 rounded-lg font-bold bg-rose-600 text-white transition">🇩🇿 الجزائر</button>
            <button onclick="switchFeedChannel('@francedealsdz')" id="feed-btn-fr" class="px-3 py-1 rounded-lg font-bold text-slate-400 hover:text-white transition">🇫🇷 فرنسا</button>
          </div>
          <span id="last-update" class="text-xs text-slate-500"></span>
        </div>

        <!-- Skeleton Loading -->
        <div id="skeleton-container" class="space-y-3">
          <div class="glass-panel rounded-2xl p-4 space-y-3 animate-pulse">
            <div class="flex gap-3"><div class="w-20 h-20 bg-slate-900 rounded-xl"></div><div class="flex-1 space-y-2"><div class="h-4 bg-slate-900 rounded w-3/4"></div><div class="h-3 bg-slate-900 rounded w-1/2"></div></div></div>
          </div>
          <div class="glass-panel rounded-2xl p-4 space-y-3 animate-pulse">
            <div class="flex gap-3"><div class="w-20 h-20 bg-slate-900 rounded-xl"></div><div class="flex-1 space-y-2"><div class="h-4 bg-slate-900 rounded w-2/3"></div><div class="h-3 bg-slate-900 rounded w-1/3"></div></div></div>
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
          <h4 class="font-bold text-sm text-white font-heading flex items-center gap-2">
            <i class="fa-solid fa-paper-plane text-rose-400"></i>
            <span>بوتات وقنوات المنظومة الرسمية</span>
          </h4>
          
          <div class="space-y-2 text-xs">
            <a href="https://t.me/Alilo07BOT" target="_blank" class="block p-3 rounded-xl bg-black/30 hover:bg-white/5 border border-white/10 transition">
              <div class="flex items-center justify-between mb-1">
                <span class="font-bold text-rose-400">🪙 بوت العملات للجميع</span>
                <span class="text-[10px] text-slate-500 font-mono">@Alilo07BOT</span>
              </div>
              <p class="text-[11px] text-slate-400">مخصص لجميع المشتركين لزيادة تخفيض العملات حتى 70% وتوليد الروابط المباشرة.</p>
            </a>

            <a href="https://t.me/DealscoutadminBOT" target="_blank" class="block p-3 rounded-xl bg-black/30 hover:bg-white/5 border border-white/10 transition">
              <div class="flex items-center justify-between mb-1">
                <span class="font-bold text-amber-400">👑 بوت الإدارة الداخلي</span>
                <span class="text-[10px] text-slate-500 font-mono">@DealscoutadminBOT</span>
              </div>
              <p class="text-[11px] text-slate-400">مخصص للأدمن فقط لتلقي تنبيهات الأعطال والتحكم الداخلي السريع.</p>
            </a>

            <a href="https://t.me/francedealsdz" target="_blank" class="block p-3 rounded-xl bg-black/30 hover:bg-white/5 border border-white/10 transition">
              <div class="flex items-center justify-between mb-1">
                <span class="font-bold text-sky-400">🇫🇷 قناة الصفقات لفرنسا</span>
                <span class="text-[10px] text-slate-500 font-mono">@francedealsdz</span>
              </div>
              <p class="text-[11px] text-slate-400">قناة الصفقات والكوبونات الحصرية للجالية بفرنسا وأوروبا مع روابط مباشرة /e/.</p>
            </a>
          </div>
        </div>

        <!-- SquareAlgerie Rate Card -->
        <div class="glass-panel rounded-2xl p-4 space-y-2.5">
          <div class="flex items-center justify-between">
            <h4 class="font-bold text-sm text-white font-heading flex items-center gap-2">
              <i class="fa-solid fa-chart-line text-emerald-400"></i>
              <span>سعر الصرف الموازي (السكوار)</span>
            </h4>
            <span class="text-[10px] text-slate-400 font-mono">مباشر</span>
          </div>
          <div class="p-3 rounded-xl bg-black/30 border border-white/10 flex items-center justify-between">
            <div>
              <span class="text-xs text-slate-400 block">سعر 1 USDT (الدولار الرقمي)</span>
              <span id="card-usdt-rate" class="text-lg font-black text-emerald-400 font-mono">249.0 دج</span>
            </div>
            <a href="https://squarealgerie.com" target="_blank" class="text-xs bg-white/5 hover:bg-white/10 text-slate-200 px-3 py-1.5 rounded-lg border border-white/10 transition">
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
  <nav class="lg:hidden fixed bottom-0 left-0 right-0 glass-panel border-t border-white/10 z-50 px-6 py-2.5 flex items-center justify-around text-xs">
    <button onclick="scrollToFeed()" class="flex flex-col items-center gap-1 text-rose-400 focus:outline-none">
      <i class="fa-solid fa-bolt text-base"></i>
      <span class="text-[10px] font-bold">العروض</span>
    </button>
    <button onclick="focusScout()" class="flex flex-col items-center gap-1 text-slate-400 hover:text-white focus:outline-none">
      <i class="fa-solid fa-magnifying-glass text-base"></i>
      <span class="text-[10px]">فاحص الرابط</span>
    </button>
    <button onclick="triggerCollector()" class="flex flex-col items-center gap-1 text-amber-400 hover:text-amber-300 focus:outline-none">
      <i class="fa-solid fa-rocket text-base"></i>
      <span class="text-[10px] font-bold">تشغيل فوري</span>
    </button>
    <a href="https://t.me/DzAliexpress0" target="_blank" class="flex flex-col items-center gap-1 text-slate-400 hover:text-white">
      <i class="fa-solid fa-paper-plane text-base"></i>
      <span class="text-[10px]">القناة</span>
    </a>
  </nav>

  <script>
    // Toast Notification Utility
    function showToast(message, type = 'success') {
      const toast = document.getElementById('action-toast');
      const body = document.getElementById('action-toast-body');
      const icon = document.getElementById('action-toast-icon');
      const text = document.getElementById('action-toast-text');

      text.innerText = message;
      if (type === 'success') {
        body.className = 'p-3.5 rounded-2xl text-xs font-bold shadow-2xl flex items-center justify-between gap-3 border bg-emerald-500/15 border-emerald-500/30 text-emerald-300 backdrop-blur-xl';
        icon.className = 'fa-solid fa-circle-check text-emerald-400 text-sm';
      } else {
        body.className = 'p-3.5 rounded-2xl text-xs font-bold shadow-2xl flex items-center justify-between gap-3 border bg-rose-500/15 border-rose-500/30 text-rose-300 backdrop-blur-xl';
        icon.className = 'fa-solid fa-triangle-exclamation text-rose-400 text-sm';
      }

      toast.classList.remove('hidden');
      setTimeout(() => {
        toast.classList.add('hidden');
      }, 5000);
    }

    // Trigger Collector on Demand (Bypasses GitHub Actions 15-30m Cron Delay)
    async function triggerCollector() {
      const btn = document.getElementById('trigger-btn');
      const icon = document.getElementById('trigger-btn-icon');
      const text = document.getElementById('trigger-btn-text');

      if (btn) btn.disabled = true;
      if (icon) icon.className = 'fa-solid fa-spinner fa-spin';
      if (text) text.innerText = 'جاري التشغيل...';

      try {
        const resp = await fetch('/api/trigger-deals?force=true', { method: 'POST' });
        const data = await resp.json();

        if (resp.ok && data.ok) {
          showToast('🚀 تم إرسال أمر فحص ونشر العروض فوراً إلى GitHub Actions بنجاح!', 'success');
          setTimeout(refreshDashboard, 5000);
        } else {
          showToast('تنبيه: ' + (data.error || data.message || 'تعذر تشغيل الفحص التلقائي'), 'error');
        }
      } catch (err) {
        showToast('تعذر الاتصال بخادم التشغيل، يرجى المحاولة ثانية', 'error');
      } finally {
        if (btn) btn.disabled = false;
        if (icon) icon.className = 'fa-solid fa-rocket';
        if (text) text.innerText = 'تشغيل الفحص الآن ⚡';
      }
    }

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
    let currentFeedChannel = '@DzAliexpress0';

    function switchFeedChannel(channel) {
      currentFeedChannel = channel;
      const btnDz = document.getElementById('feed-btn-dz');
      const btnFr = document.getElementById('feed-btn-fr');
      if (btnDz && btnFr) {
        if (channel === '@DzAliexpress0') {
          btnDz.className = 'px-3 py-1 rounded-lg font-bold bg-rose-600 text-white transition';
          btnFr.className = 'px-3 py-1 rounded-lg font-bold text-slate-400 hover:text-white transition';
        } else {
          btnFr.className = 'px-3 py-1 rounded-lg font-bold bg-sky-600 text-white transition';
          btnDz.className = 'px-3 py-1 rounded-lg font-bold text-slate-400 hover:text-white transition';
        }
      }
      refreshDashboard();
    }

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
        const res = await fetch('/api/channel-posts?channel=' + encodeURIComponent(currentFeedChannel));
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
                <div class="w-20 h-20 sm:w-24 sm:h-24 rounded-xl bg-slate-900 border border-white/10 flex-shrink-0 overflow-hidden">
                  <img src="${p.photo_url}" class="w-full h-full object-cover" loading="lazy">
                </div>
              ` : `
                <div class="w-20 h-20 rounded-xl bg-slate-900 border border-white/10 flex-shrink-0 flex items-center justify-center">
                  <i class="fa-solid fa-tag text-slate-700 text-xl"></i>
                </div>
              `}
              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between text-[11px] text-slate-500 mb-1">
                  <span class="font-mono">${p.date || ''}</span>
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
    let lastScoutedDeal = null;

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
          lastScoutedDeal = d;
          document.getElementById('scout-title').innerText = d.title || 'منتج مميز من AliExpress';
          document.getElementById('scout-price-usd').innerText = d.price ? '$' + d.price.toFixed(2) : 'سعر مميز';
          
          const scoutEurEl = document.getElementById('scout-price-eur');
          if (scoutEurEl) {
            if (d.price_eur) {
              scoutEurEl.innerText = d.price_eur.toFixed(2) + '€';
              scoutEurEl.classList.remove('hidden');
            } else {
              scoutEurEl.classList.add('hidden');
            }
          }

          document.getElementById('scout-price-dzd').innerText = d.price_dzd ? '~ ' + d.price_dzd.toLocaleString() + ' دج' : '';
          document.getElementById('scout-pid').innerText = 'ID: ' + d.product_id;
          
          if (d.image_url) {
            document.getElementById('scout-img-box').innerHTML = `<img src="${d.image_url}" class="w-full h-full object-cover">`;
          }

          document.getElementById('scout-direct-link').href = d.product_link;
          document.getElementById('scout-coin-link').href = d.coin_link;

          resBox.classList.remove('hidden');
        } else {
          showToast('تعذر استخراج بيانات المنتج من الرابط: ' + (data.error || 'تأكد من الرابط'), 'error');
        }
      } catch (e) {
        showToast('حدث خطأ أثناء فحص الرابط: ' + e.message, 'error');
      } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles"></i><span>فحص العرض</span>';
      }
    }

    function copyScoutToReformatter() {
      if (!lastScoutedDeal) return;
      const refInput = document.getElementById('reformat-input');
      if (refInput) {
        let textToFill = lastScoutedDeal.product_link || lastScoutedDeal.coin_link || '';
        if (lastScoutedDeal.price) {
          textToFill += `\nالسعر: $${lastScoutedDeal.price}`;
        }
        refInput.value = textToFill;
        refInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
        reformatTelegramPost();
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
          const isFrance = data.is_france || (data.target_channel === '@francedealsdz');
          const badgeEl = document.getElementById('reformat-target-channel-badge');
          const labelEl = document.getElementById('reformat-caption-label');
          const btnTextEl = document.getElementById('reformat-publish-btn-text');

          if (badgeEl) {
            badgeEl.innerText = isFrance ? '🇫🇷 @francedealsdz (فرنسا)' : '🇩🇿 @DzAliexpress0 (الجزائر)';
            badgeEl.className = isFrance 
              ? 'text-xs font-bold px-2.5 py-0.5 rounded-md border border-sky-500/30 bg-sky-500/10 text-sky-300'
              : 'text-xs font-bold px-2.5 py-0.5 rounded-md border border-emerald-500/30 bg-emerald-500/10 text-emerald-300';
          }
          if (labelEl) {
            labelEl.innerText = isFrance ? 'نص المنشور المنسق لفرنسا (يمكنك التعديل عليه قبل النشر):' : 'نص المنشور الجزائري المنسق (يمكنك التعديل عليه قبل النشر):';
          }
          if (btnTextEl) {
            btnTextEl.innerText = isFrance ? 'نشر في القناة الفرنسية (@francedealsdz)' : 'نشر في القناة الآن (@DzAliexpress0)';
          }

          document.getElementById('reformat-pid').innerText = 'ID: ' + data.product_id;
          document.getElementById('reformat-price-usd').innerText = data.price ? '$' + data.price.toFixed(2) : 'سعر خاص';
          
          const refEurEl = document.getElementById('reformat-price-eur');
          if (refEurEl) {
            if (data.price_eur) {
              refEurEl.innerText = data.price_eur.toFixed(2) + '€';
              refEurEl.classList.remove('hidden');
            } else {
              refEurEl.classList.add('hidden');
            }
          }

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
              <div onclick="selectReformatImage('${img}')" class="w-8 h-8 rounded-md bg-slate-800 border border-white/10 overflow-hidden cursor-pointer hover:border-rose-500 transition">
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
          showToast('تعذر استخراج بيانات العرض: ' + (data.error || 'تأكد من وجود رابط AliExpress في المنشور'), 'error');
        }
      } catch (e) {
        showToast('حدث خطأ أثناء معالجة المنشور: ' + e.message, 'error');
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
        countEl.className = len > 1024 ? 'text-[10px] text-rose-400 font-bold font-mono' : 'text-[10px] text-slate-500 font-mono';
      }
    }

    async function publishReformattedDeal() {
      if (!currentReformattedDeal) return;

      const btn = document.getElementById('reformat-publish-btn');
      const feedback = document.getElementById('reformat-feedback');
      const caption = document.getElementById('reformat-caption').value.trim();

      if (!caption) {
        showToast('نص المنشور فارغ!', 'error');
        return;
      }

      const isFrance = currentReformattedDeal.is_france || (currentReformattedDeal.target_channel === '@francedealsdz');
      const targetName = isFrance ? 'الفرنسية @francedealsdz' : '@DzAliexpress0';
      if (!confirm(`هل أنت متأكد من نشر هذا المنشور في القناة ${targetName} الآن؟`)) {
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
            deal_link: currentReformattedDeal.deal_link,
            price: currentReformattedDeal.price,
            target_channel: currentReformattedDeal.target_channel || (isFrance ? '@francedealsdz' : '@DzAliexpress0')
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
          showToast('تم نشر المنشور في القناة بنجاح! #' + data.message_id, 'success');
          setTimeout(refreshDashboard, 2000);
        } else {
          feedback.className = 'p-3 rounded-xl text-xs font-medium bg-rose-500/10 border border-rose-500/20 text-rose-300';
          feedback.innerText = 'فشل النشر: ' + (data.error || 'خطأ غير معروف');
          feedback.classList.remove('hidden');
          showToast('فشل النشر: ' + (data.error || 'خطأ غير معروف'), 'error');
        }
      } catch (e) {
        showToast('حدث خطأ أثناء النشر: ' + e.message, 'error');
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
            btn.className = 'speed-btn bg-white/5 hover:bg-white/10 text-slate-300 font-bold text-xs py-2 px-3 rounded-xl border border-white/10 transition flex items-center justify-center gap-1.5 active:scale-95';
          }
        }
      });

      const summary = document.getElementById('sched-current-summary');
      if (summary) {
        if (paused) {
          summary.innerText = '⏸️ النشر متوقف مؤقتاً';
          summary.className = 'text-xs text-amber-300 font-bold bg-amber-500/10 border border-amber-500/20 px-3 py-1.5 rounded-xl font-mono';
        } else if (isNight && nightOn) {
          summary.innerText = 'كل ' + (currentSchedule.night_interval_minutes || 30) + ' دقيقة (ليلي 🌙)';
          summary.className = 'text-xs text-indigo-300 font-bold bg-indigo-500/10 border border-indigo-500/20 px-3 py-1.5 rounded-xl font-mono';
        } else {
          summary.innerText = 'كل ' + cur + ' دقائق (نهاري ☀️)';
          summary.className = 'text-xs text-rose-300 font-bold bg-black/40 border border-white/10 px-3 py-1.5 rounded-xl font-mono';
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
        showToast('تم تحديث الفاصل الزمني إلى ' + mins + ' دقائق بنجاح', 'success');
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
        showToast(currentSchedule.is_paused ? 'تم إيقاف النشر مؤقتاً' : 'تم استئناف النشر التلقائي', 'success');
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

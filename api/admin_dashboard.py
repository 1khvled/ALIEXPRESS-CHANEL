"""
DealScout DZ — Admin Dashboard Interface
Professional administration suite for managing Telegram deal publishing, link inspection,
live channel feed monitoring, and auto-publishing schedule controls.
Styled with the platform's obsidian dark theme tokens, dot-matrix architectural textures,
and crisp typography (Cairo, Readex Pro, Plus Jakarta Sans, JetBrains Mono).
"""

DASHBOARD_HTML = r"""<!DOCTYPE html>
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

      /* Deep Obsidian Slate Dark Tokens (Matching Main Site UI) */
      --bg-page: #06080d;
      --bg-card: #0e121b;
      --bg-card-hover: #141a28;
      --bg-elevated: #141a28;
      --bg-subtle: #1e2638;
      --border-card: #1f293d;
      --border-subtle: #2d3b55;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-soft: #64748b;
      --header-bg: #090c13;
      --input-bg: #141a28;
      --shadow-card: 0 4px 12px -2px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }

    body {
      background-color: var(--bg-page);
      background-image: radial-gradient(rgba(255, 255, 255, 0.07) 1px, transparent 1px);
      background-size: 24px 24px;
      color: var(--text-main);
      font-family: 'Readex Pro', 'Cairo', 'Plus Jakarta Sans', sans-serif;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      -webkit-tap-highlight-color: transparent;
      overflow-x: hidden !important;
    }

    .solid-panel {
      background-color: var(--bg-card);
      border: 1px solid var(--border-card);
      box-shadow: var(--shadow-card);
      border-radius: 16px;
    }

    .card-hover {
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .card-hover:hover {
      background-color: var(--bg-card-hover);
      border-color: #e11d48;
      transform: translateY(-2px);
      box-shadow: 0 10px 24px -4px rgba(0, 0, 0, 0.55);
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

  <!-- Header (Solid Obsidian Matching Main Site) -->
  <header class="sticky top-0 z-40 border-b px-4 py-3" style="background-color: var(--header-bg); border-color: var(--border-card);">
    <div class="max-w-7xl mx-auto flex items-center justify-between gap-3">
      
      <!-- Brand & Info -->
      <div class="flex items-center space-x-3 space-x-reverse">
        <a href="/" target="_blank" class="w-10 h-10 rounded-xl bg-gradient-to-tr from-rose-600 via-rose-500 to-amber-500 flex items-center justify-center font-bold text-white shadow-md border border-white/10 active:scale-95 transition">
          <i class="fa-solid fa-bolt text-lg"></i>
        </a>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="font-black text-lg text-white font-heading tracking-tight">DealScout<span class="text-rose-500">DZ</span></h1>
            <span class="bg-rose-500/10 text-rose-400 text-[10px] font-bold px-2 py-0.5 rounded-full border border-rose-500/20">ADMIN PANEL</span>
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
          class="bg-gradient-to-r from-rose-600 to-amber-600 hover:from-rose-500 hover:to-amber-500 text-white text-xs px-3.5 py-2 rounded-xl font-bold shadow-md flex items-center gap-1.5 transition active:scale-95 border border-rose-400/20"
        >
          <i class="fa-solid fa-rocket" id="trigger-btn-icon"></i>
          <span class="hidden sm:inline" id="trigger-btn-text">تشغيل الفحص الآن ⚡</span>
        </button>

        <!-- Live USDT Badge -->
        <a href="https://squarealgerie.com" target="_blank" class="hidden md:flex items-center gap-1.5 bg-[#141a28] border border-[#1f293d] text-emerald-400 text-xs px-3 py-1.5 rounded-xl hover:border-emerald-500/40 transition">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>1 USDT ≈ <b id="header-usdt-rate" class="font-mono">249.0</b> دج</span>
        </a>

        <!-- Return to User Site -->
        <a href="/" target="_blank" title="عرض موقع العروض العام" class="bg-[#141a28] hover:bg-[#1e2638] text-slate-300 hover:text-white text-xs px-3 py-2 rounded-xl border border-[#1f293d] flex items-center gap-1.5 transition">
          <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
          <span class="hidden sm:inline">موقع العروض</span>
        </a>

        <!-- Refresh Button -->
        <button onclick="refreshDashboard()" id="refresh-btn" class="bg-[#141a28] hover:bg-[#1e2638] text-slate-200 text-xs px-3 py-2 rounded-xl border border-[#1f293d] flex items-center gap-1.5 transition active:scale-95">
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
    <div class="solid-panel rounded-2xl p-5 sm:p-6 space-y-4">
      <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2">
        <div class="flex items-center gap-2.5">
          <div class="w-9 h-9 rounded-xl bg-rose-500/10 border border-rose-500/20 flex items-center justify-center text-rose-400">
            <i class="fa-solid fa-magnifying-glass-dollar text-base"></i>
          </div>
          <div>
            <h2 class="text-sm sm:text-base font-bold text-white font-heading">فاحص ومحول روابط AliExpress الفوري 🔍</h2>
            <p class="text-[11px] text-slate-400">تحويل أي رابط عادي لرابط تابع مخصص وكشف نسبة خصم العملات</p>
          </div>
        </div>
        <span class="text-[11px] text-slate-400 bg-[#141a28] border border-[#1f293d] px-2.5 py-1 rounded-lg">يدعم روابط التطبيق، المتصفح، أو رقم المنتج</span>
      </div>

      <div class="flex flex-col sm:flex-row gap-2">
        <input 
          type="text" 
          id="scout-url-input" 
          placeholder="ألصق أي رابط أو كود منتج من AliExpress هنا..." 
          dir="ltr"
          class="flex-1 bg-[#141a28] border border-[#1f293d] rounded-xl px-4 py-2.5 text-xs sm:text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500 font-mono transition"
        />
        <button 
          onclick="scoutDeal()" 
          id="scout-submit-btn" 
          class="bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs sm:text-sm px-5 py-2.5 rounded-xl shadow-md flex items-center justify-center gap-2 transition active:scale-95 border border-rose-400/20"
        >
          <i class="fa-solid fa-wand-magic-sparkles"></i>
          <span>فحص العرض</span>
        </button>
      </div>

      <!-- Scout Result Card -->
      <div id="scout-result" class="hidden pt-4 border-t border-[#1f293d]">
        <div class="bg-[#141a28] rounded-xl p-4 border border-[#1f293d] flex flex-col md:flex-row items-start gap-4">
          <div id="scout-img-box" class="w-24 h-24 rounded-xl bg-[#06080d] border border-[#1f293d] flex-shrink-0 overflow-hidden flex items-center justify-center">
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
              <a id="scout-direct-link" href="#" target="_blank" class="bg-[#0e121b] hover:bg-[#1e2638] border border-[#1f293d] text-white text-xs px-3 py-1.5 rounded-lg flex items-center gap-1.5 transition">
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
    <div class="solid-panel rounded-2xl p-5 sm:p-6 space-y-4">
      <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 pb-3 border-b border-[#1f293d]">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-amber-500 to-rose-600 flex items-center justify-center text-white shadow-md">
            <i class="fa-solid fa-wand-magic-sparkles text-lg"></i>
          </div>
          <div>
            <h3 class="font-bold text-base sm:text-lg text-white font-heading flex items-center gap-2">
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
          class="w-full bg-[#141a28] border border-[#1f293d] rounded-xl p-3.5 text-xs sm:text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500 font-sans leading-relaxed transition"
        ></textarea>

        <div class="flex flex-wrap items-center justify-between gap-2">
          <div class="flex flex-wrap items-center gap-2">
            <button 
              onclick="reformatTelegramPost()" 
              id="reformat-submit-btn" 
              class="bg-gradient-to-r from-rose-600 to-amber-600 hover:from-rose-500 hover:to-amber-500 text-white font-bold text-xs sm:text-sm px-6 py-2.5 rounded-xl shadow-md flex items-center justify-center gap-2 transition active:scale-95 border border-rose-400/20"
            >
              <i class="fa-solid fa-arrows-rotate"></i>
              <span>إعادة التنسيق والمعاينة</span>
            </button>
            <div class="flex items-center gap-1.5 bg-[#141a28] border border-[#1f293d] rounded-xl px-3 py-1.5">
              <span class="text-xs text-slate-300 font-bold">💰 السعر ($):</span>
              <input 
                type="number" 
                step="0.01" 
                id="reformat-manual-price" 
                placeholder="مثال: 0.60" 
                class="w-24 bg-[#0e121b] border border-[#1f293d] rounded-lg px-2 py-1 text-xs text-emerald-400 font-bold font-mono focus:outline-none focus:border-rose-500"
              />
            </div>
          </div>
          <button 
            onclick="document.getElementById('reformat-input').value=''; if(document.getElementById('reformat-manual-price')) document.getElementById('reformat-manual-price').value=''; document.getElementById('reformat-result').classList.add('hidden');" 
            class="text-xs text-slate-400 hover:text-slate-200 px-3 py-1.5 rounded-lg border border-[#1f293d] hover:bg-[#141a28] transition"
          >
            مسح الحقل
          </button>
        </div>
      </div>

      <!-- Reformatted Result Card -->
      <div id="reformat-result" class="hidden pt-4 border-t border-[#1f293d] space-y-4">
        <div class="bg-[#141a28] rounded-xl p-4 border border-[#1f293d] flex flex-col md:flex-row items-start gap-4">
          <!-- Image Box & Selectors -->
          <div class="flex flex-col items-center gap-2 w-full md:w-auto">
            <div id="reformat-img-box" class="w-32 h-32 rounded-xl bg-[#06080d] border border-[#1f293d] overflow-hidden flex items-center justify-center flex-shrink-0">
              <i class="fa-solid fa-image text-slate-600 text-3xl"></i>
            </div>
            <div id="reformat-gallery" class="flex flex-wrap gap-1 max-w-[140px] justify-center"></div>
          </div>

          <!-- Content Details & Editable Caption -->
          <div class="flex-1 min-w-0 w-full space-y-3">
            <div class="flex flex-wrap items-center justify-between gap-2">
              <div class="flex items-center gap-2">
                <span id="reformat-pid" class="text-xs font-mono bg-[#0e121b] text-slate-300 px-2.5 py-0.5 rounded-md border border-[#1f293d]"></span>
                <span id="reformat-target-channel-badge" class="text-xs font-bold px-2.5 py-0.5 rounded-md border border-emerald-500/20 bg-emerald-500/10 text-emerald-300">@DzAliexpress0</span>
              </div>
              <div class="flex items-center gap-2 font-mono">
                <div class="flex items-center gap-1.5 bg-[#0e121b] border border-emerald-500/30 rounded-lg px-2.5 py-1">
                  <span class="text-emerald-400 font-bold text-xs">$</span>
                  <input 
                    type="number" 
                    step="0.01" 
                    id="reformat-card-price-input" 
                    oninput="onAdminPriceEdit(this.value)" 
                    class="w-20 bg-transparent text-emerald-400 font-bold text-xs font-mono focus:outline-none"
                    placeholder="0.00"
                  />
                </div>
                <span id="reformat-price-eur" class="text-sky-400 font-bold bg-sky-500/10 border border-sky-500/20 px-2.5 py-1 rounded-md text-xs hidden"></span>
                <span id="reformat-price-dzd" class="text-amber-400 font-bold bg-amber-500/10 border border-amber-500/20 px-2.5 py-1 rounded-md text-xs"></span>
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
                class="w-full bg-[#0e121b] border border-[#1f293d] rounded-xl p-3 text-xs sm:text-sm text-slate-100 focus:outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500 font-sans leading-relaxed"
              ></textarea>
            </div>

            <!-- Link Type Selector Options -->
            <div class="p-2.5 bg-[#0e121b] border border-[#1f293d] rounded-xl flex flex-wrap items-center justify-between gap-2">
              <div class="flex items-center gap-2">
                <span class="text-[11px] font-bold text-slate-300">نوع الرابط التابع المعتمد:</span>
                <span id="reformat-active-link-badge" class="text-[10px] font-bold px-2 py-0.5 rounded bg-amber-500/10 text-amber-300 border border-amber-500/20">🪙 صفحة تخفيض العملات (Coins)</span>
              </div>
              <div class="flex items-center gap-1.5" id="reformat-link-options">
                <button type="button" onclick="setReformatLinkType('coin')" id="opt-link-coin" class="px-2.5 py-1 rounded-lg text-xs font-bold transition bg-amber-500 text-slate-950 shadow">🪙 عملات (Coins)</button>
                <button type="button" onclick="setReformatLinkType('direct')" id="opt-link-direct" class="px-2.5 py-1 rounded-lg text-xs font-medium transition text-slate-400 hover:text-white bg-slate-800">🛒 مباشر</button>
                <button type="button" onclick="setReformatLinkType('bundle')" id="opt-link-bundle" class="px-2.5 py-1 rounded-lg text-xs font-medium transition text-slate-400 hover:text-white bg-slate-800">📦 حزم</button>
                <button type="button" onclick="setReformatLinkType('super')" id="opt-link-super" class="px-2.5 py-1 rounded-lg text-xs font-medium transition text-slate-400 hover:text-white bg-slate-800">⚡ Super</button>
              </div>
            </div>

            <!-- Actions Row -->
            <div class="flex flex-wrap items-center justify-between gap-3 pt-1">
              <div class="flex items-center gap-3">
                <a id="reformat-deal-link" href="#" target="_blank" class="text-xs text-rose-400 hover:text-rose-300 flex items-center gap-1.5 font-bold">
                  <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                  <span>فحص الرابط التابع</span>
                </a>
                <label class="inline-flex items-center gap-1.5 cursor-pointer text-xs font-semibold text-zinc-300 hover:text-white transition select-none bg-blue-950/40 border border-blue-600/30 px-2.5 py-1 rounded-lg" title="نشر هذا المنشور أيضاً على صفحة الفيسبوك">
                  <input type="checkbox" id="reformat-fb-toggle" class="rounded accent-blue-500 w-3.5 h-3.5 cursor-pointer" checked>
                  <i class="fa-brands fa-facebook text-blue-400 text-xs"></i>
                  <span>نشر على فيسبوك</span>
                </label>
              </div>

              <button 
                onclick="publishReformattedDeal()" 
                id="reformat-publish-btn" 
                class="bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs sm:text-sm px-6 py-2.5 rounded-xl shadow-md flex items-center justify-center gap-2 transition active:scale-95 border border-emerald-400/20"
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
    <div class="solid-panel rounded-2xl p-5 sm:p-6 space-y-4">
      <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 pb-3 border-b border-[#1f293d]">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-rose-600 to-amber-500 flex items-center justify-center text-white shadow-md">
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
        <div id="sched-current-summary" class="text-xs text-rose-300 font-bold bg-[#141a28] border border-[#1f293d] px-3 py-1.5 rounded-xl font-mono">
          كل 5 دقائق ☀️
        </div>
      </div>

      <!-- Quick Speed Buttons -->
      <div class="space-y-3">
        <div class="text-xs font-semibold text-slate-300">الفاصل الزمني النهاري:</div>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
          <button onclick="setSpeed(5)" id="btn-speed-5" class="speed-btn bg-rose-600 text-white font-bold text-xs py-2 px-3 rounded-xl border border-rose-500 transition flex items-center justify-center gap-1.5 active:scale-95 shadow">
            <i class="fa-solid fa-bolt"></i>
            <span>كل 5 دقائق</span>
          </button>
          <button onclick="setSpeed(10)" id="btn-speed-10" class="speed-btn bg-[#141a28] hover:bg-[#1e2638] text-slate-300 font-bold text-xs py-2 px-3 rounded-xl border border-[#1f293d] transition flex items-center justify-center gap-1.5 active:scale-95">
            <i class="fa-solid fa-rocket"></i>
            <span>كل 10 دقائق</span>
          </button>
          <button onclick="setSpeed(15)" id="btn-speed-15" class="speed-btn bg-[#141a28] hover:bg-[#1e2638] text-slate-300 font-bold text-xs py-2 px-3 rounded-xl border border-[#1f293d] transition flex items-center justify-center gap-1.5 active:scale-95">
            <i class="fa-solid fa-scale-balanced"></i>
            <span>كل 15 دقيقة</span>
          </button>
          <button onclick="setSpeed(30)" id="btn-speed-30" class="speed-btn bg-[#141a28] hover:bg-[#1e2638] text-slate-300 font-bold text-xs py-2 px-3 rounded-xl border border-[#1f293d] transition flex items-center justify-center gap-1.5 active:scale-95">
            <i class="fa-solid fa-clock"></i>
            <span>كل 30 دقيقة</span>
          </button>
        </div>

        <!-- Mode Switches -->
        <div class="flex flex-wrap items-center justify-between gap-3 pt-3 border-t border-[#1f293d] text-xs">
          <button onclick="toggleNightMode()" id="btn-night-mode" class="bg-[#141a28] hover:bg-[#1e2638] border border-[#1f293d] text-slate-300 px-3 py-1.5 rounded-xl flex items-center gap-2 transition active:scale-95">
            <i class="fa-solid fa-moon text-indigo-400"></i>
            <span id="text-night-mode">الوضع الليلي: مفعّل (30د بعد منتصف الليل)</span>
          </button>
          <button onclick="togglePauseAuto()" id="btn-pause-auto" class="bg-[#141a28] hover:bg-[#1e2638] border border-[#1f293d] text-slate-300 px-3 py-1.5 rounded-xl flex items-center gap-2 transition active:scale-95">
            <i id="icon-pause-auto" class="fa-solid fa-pause text-amber-400"></i>
            <span id="text-pause-auto">إيقاف النشر مؤقتاً</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Quick Stats Cards (Solid Obsidian) -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
      <div class="solid-panel rounded-2xl p-4 card-hover">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span>عروض القناة الحية</span>
          <i class="fa-solid fa-bullhorn text-rose-400"></i>
        </div>
        <div id="stat-total" class="text-xl sm:text-2xl font-black text-rose-400 font-mono">--</div>
        <span class="text-[10px] text-slate-500 mt-1 block">تحديث دوري من القناة</span>
      </div>

      <div class="solid-panel rounded-2xl p-4 card-hover">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span>عروض بالصور HD</span>
          <i class="fa-solid fa-image text-emerald-400"></i>
        </div>
        <div id="stat-photos" class="text-xl sm:text-2xl font-black text-emerald-400 font-mono">--</div>
        <span class="text-[10px] text-slate-500 mt-1 block">صور المنتجات الأصلية</span>
      </div>

      <div class="solid-panel rounded-2xl p-4 card-hover">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span>سعر صرف الـ USDT 🇩🇿</span>
          <i class="fa-solid fa-arrow-trend-up text-amber-400"></i>
        </div>
        <div id="stat-usdt" class="text-xl sm:text-2xl font-black text-amber-400 font-mono">249.0 دج</div>
        <a href="https://squarealgerie.com" target="_blank" class="text-[10px] text-slate-400 hover:text-amber-400 mt-1 block">SquareAlgerie.com</a>
      </div>

      <div class="solid-panel rounded-2xl p-4 card-hover">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span>حالة المنظومة التلقائية</span>
          <i class="fa-solid fa-robot text-sky-400"></i>
        </div>
        <div class="text-sm sm:text-base font-bold text-emerald-400 flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>تعمل بكفاءة 100%</span>
        </div>
        <span class="text-[10px] text-slate-500 mt-1 block font-mono">@DzAliexpress0 • Collector</span>
      </div>
    </div>

    <!-- Main Content Layout -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

      <!-- Left 2 Cols: Posts Feed -->
      <div class="lg:col-span-2 space-y-4">
        <div class="flex items-center justify-between flex-wrap gap-2">
          <div class="flex items-center gap-2">
            <h3 class="font-bold text-base text-white font-heading">آخر العروض المنشورة</h3>
            <span id="posts-badge" class="bg-[#141a28] text-slate-300 text-xs px-2.5 py-0.5 rounded-full border border-[#1f293d] font-mono">0</span>
          </div>

          <!-- Channel switcher & Search -->
          <div class="flex items-center gap-2 flex-wrap">
            <div class="flex items-center bg-[#141a28] border border-[#1f293d] rounded-xl p-1 text-xs">
              <button onclick="switchFeedChannel('@DzAliexpress0')" id="feed-btn-dz" class="px-3 py-1 rounded-lg font-bold bg-rose-600 text-white transition">🇩🇿 الجزائر</button>
              <button onclick="switchFeedChannel('@francedealsdz')" id="feed-btn-fr" class="px-3 py-1 rounded-lg font-bold text-slate-400 hover:text-white transition">🇫🇷 فرنسا</button>
            </div>
            <span id="last-update" class="text-xs text-slate-500"></span>
          </div>
        </div>

        <!-- Realtime Search filter for posts -->
        <div class="relative">
          <i class="fa-solid fa-magnifying-glass absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-500 text-xs"></i>
          <input 
            type="text" 
            id="feed-search-input" 
            oninput="filterFeedPosts()" 
            placeholder="بحث فوري في العروض المنشورة (بالعنوان، الكوبون، السعر، الهاتف...)" 
            class="w-full bg-[#0e121b] border border-[#1f293d] rounded-xl pr-9 pl-4 py-2 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-rose-500 font-sans transition"
          >
        </div>

        <!-- Skeleton Loading -->
        <div id="skeleton-container" class="space-y-3">
          <div class="solid-panel rounded-2xl p-4 space-y-3 animate-pulse">
            <div class="flex gap-3"><div class="w-24 h-24 bg-[#141a28] rounded-xl"></div><div class="flex-1 space-y-2"><div class="h-4 bg-[#141a28] rounded w-3/4"></div><div class="h-3 bg-[#141a28] rounded w-1/2"></div></div></div>
          </div>
          <div class="solid-panel rounded-2xl p-4 space-y-3 animate-pulse">
            <div class="flex gap-3"><div class="w-24 h-24 bg-[#141a28] rounded-xl"></div><div class="flex-1 space-y-2"><div class="h-4 bg-[#141a28] rounded w-2/3"></div><div class="h-3 bg-[#141a28] rounded w-1/3"></div></div></div>
          </div>
        </div>

        <!-- Posts Feed Container -->
        <div id="posts-container" class="space-y-4 hidden"></div>

        <!-- Error State -->
        <div id="error-state" class="hidden solid-panel rounded-2xl p-6 text-center text-rose-400">
          <i class="fa-solid fa-triangle-exclamation text-2xl mb-2"></i>
          <p id="error-message" class="text-xs"></p>
        </div>
      </div>

      <!-- Right 1 Col: Quick Links & Bots Guide -->
      <div class="space-y-4">

        <!-- Bots Card -->
        <div class="solid-panel rounded-2xl p-4 space-y-3">
          <h4 class="font-bold text-sm text-white font-heading flex items-center gap-2">
            <i class="fa-solid fa-paper-plane text-rose-400"></i>
            <span>بوتات وقنوات المنظومة الرسمية</span>
          </h4>
          
          <div class="space-y-2 text-xs">
            <a href="https://t.me/Alilo07BOT" target="_blank" class="block p-3 rounded-xl bg-[#141a28] hover:border-slate-500 border border-[#1f293d] transition">
              <div class="flex items-center justify-between mb-1">
                <span class="font-bold text-rose-400">🪙 بوت العملات للجميع</span>
                <span class="text-[10px] text-slate-500 font-mono">@Alilo07BOT</span>
              </div>
              <p class="text-[11px] text-slate-400">مخصص لجميع المشتركين لزيادة تخفيض العملات حتى 70% وتوليد الروابط المباشرة.</p>
            </a>

            <a href="https://t.me/francedealsdz" target="_blank" class="block p-3 rounded-xl bg-[#141a28] hover:border-slate-500 border border-[#1f293d] transition">
              <div class="flex items-center justify-between mb-1">
                <span class="font-bold text-sky-400">🇫🇷 قناة الصفقات لفرنسا</span>
                <span class="text-[10px] text-slate-500 font-mono">@francedealsdz</span>
              </div>
              <p class="text-[11px] text-slate-400">قناة الصفقات والكوبونات الحصرية للجالية بفرنسا وأوروبا مع روابط مباشرة /e/.</p>
            </a>

            <a href="https://t.me/DzAliexpress0" target="_blank" class="block p-3 rounded-xl bg-[#141a28] hover:border-slate-500 border border-[#1f293d] transition">
              <div class="flex items-center justify-between mb-1">
                <span class="font-bold text-emerald-400">🇩🇿 القناة الرسمية للجزائر</span>
                <span class="text-[10px] text-slate-500 font-mono">@DzAliexpress0</span>
              </div>
              <p class="text-[11px] text-slate-400">القناة الرئيسية لأقوى صفقات وعروض الجزائر اليومية مع شحن مباشر وبأسعار قياسية.</p>
            </a>
          </div>
        </div>

        <!-- SquareAlgerie Rate Card -->
        <div class="solid-panel rounded-2xl p-4 space-y-2.5">
          <div class="flex items-center justify-between">
            <h4 class="font-bold text-sm text-white font-heading flex items-center gap-2">
              <i class="fa-solid fa-chart-line text-emerald-400"></i>
              <span>سعر الصرف الموازي (السكوار)</span>
            </h4>
            <span class="text-[10px] text-slate-400 font-mono">مباشر</span>
          </div>
          <div class="p-3 rounded-xl bg-[#141a28] border border-[#1f293d] flex items-center justify-between">
            <div>
              <span class="text-xs text-slate-400 block">سعر 1 USDT (الدولار الرقمي)</span>
              <span id="card-usdt-rate" class="text-lg font-black text-emerald-400 font-mono">249.0 دج</span>
            </div>
            <a href="https://squarealgerie.com" target="_blank" class="text-xs bg-[#0e121b] hover:bg-[#1e2638] text-slate-200 px-3 py-1.5 rounded-lg border border-[#1f293d] transition">
              SquareAlgerie 🇩🇿
            </a>
          </div>
        </div>

        <!-- Country Hint Notice -->
        <div class="solid-panel rounded-2xl p-4 space-y-2">
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
  <nav class="lg:hidden fixed bottom-0 left-0 right-0 border-t z-50 px-6 py-2.5 flex items-center justify-around text-xs" style="background-color: var(--header-bg); border-color: var(--border-card);">
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

    let currentLiveRate = 249.0;
    let currentRawPosts = [];
    let currentParsedPosts = [];

    // Helper: Escape HTML to prevent injection
    function escapeHtml(str) {
      if (!str) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }

    // Helper: Turn raw links inside text into clickable links
    function formatPostTextWithLinks(raw) {
      if (!raw) return '';
      const safe = escapeHtml(raw);
      return safe.replace(/(https?:\/\/[^\s<]+)/g, '<a href="$1" target="_blank" rel="noopener noreferrer" class="text-rose-400 hover:text-rose-300 underline font-mono text-[11px]">$1</a>');
    }

    // Helper: 1-Click Clipboard Copy with Feedback
    async function copyToClipboard(text, btnEl, label) {
      if (!text) return;
      try {
        await navigator.clipboard.writeText(text);
        showToast(`تم نسخ ${label || 'النص'} بنجاح!`, 'success');
        if (btnEl) {
          const original = btnEl.innerHTML;
          btnEl.innerHTML = '<i class="fa-solid fa-check text-emerald-400"></i><span class="text-emerald-400 font-bold">تم النسخ</span>';
          btnEl.classList.add('border-emerald-500/50');
          setTimeout(() => {
            btnEl.innerHTML = original;
            btnEl.classList.remove('border-emerald-500/50');
          }, 2000);
        }
      } catch (err) {
        showToast('تعذر النسخ: ' + err.message, 'error');
      }
    }

    // Deal Parser: Extracts Title, Prices, Coupons, Coins, and Links
    function parseAdminDeal(post, rate) {
      const text = (post.text || '').trim();
      const usdt = rate || 249.0;
      const lines = text.split(/\r?\n/).map(l => l.trim()).filter(Boolean);

      const isBoilerplate = (l) => {
        const s = l.toLowerCase().replace(/[\u0640]/g, '');
        return (
          s.includes('http') || s.includes('@') || s.includes('t.me') ||
          s.includes('خلي البلد') || s.includes('بلد الحساب') || s.includes('livraison') ||
          s.includes('pays') || s.includes('السعر') || s.includes('prix') || s.includes('price') ||
          s.includes('كوبون') || s.includes('قسيمة') || s.includes('code') || s.includes('coupon') ||
          s.includes('عملات') || s.includes('coins') || s.includes('pièces') ||
          s.includes('لافار') || s.includes('عرض اليوم') || s.includes('صفقة') || s.includes('صيدة') ||
          s.includes('تخفيض قوي') || s.includes('رابط الشراء') || s.includes('بوت') || s.includes('قناة') ||
          s.includes('تنبيه') || s.includes('طريقة') || s.includes('احجز') || s.includes('طبقوا') ||
          s.includes('سارعوا') || s.includes('متوسط') || s.includes('سعره') || s.includes('دج') ||
          s.includes('رزنامة') || s.includes('التخفيضات الكبرى') || s.includes('black friday') ||
          s.includes('cyber monday') || s.includes('11.11') || s.includes('شهر كامل') ||
          s.includes('promotion calendar')
        );
      };

      // 1. Title Extraction
      let title = '';
      for (const line of lines) {
        const m = line.match(/^[✅✔️☑️]\s*(.+)$/) || line.match(/✅\s*([^\n]+)/);
        if (m) {
          const cand = m[1].replace(/<[^>]*>/g, '').replace(/^[✅✔️☑️\s*#]+/, '').trim();
          if (cand.length >= 3 && !isBoilerplate(cand)) {
            title = cand;
            break;
          }
        }
      }

      if (!title) {
        for (const line of lines) {
          const m = line.match(/^(?:⭐️|⭐|🌟|📱|🎮|🎧|⚡|📦|تخفيض\s*(?:لـ|ل)?|عرض\s*خاص\s*(?:لـ|ل)?|تخفيض\s*على|produit\s*:?|offre\s*:?)\s*(.+)$/i);
          if (m) {
            const cand = m[1].replace(/<[^>]*>/g, '').trim();
            if (cand.length >= 3 && !isBoilerplate(cand)) {
              title = cand;
              break;
            }
          }
        }
      }

      if (!title) {
        for (const line of lines) {
          if (isBoilerplate(line)) continue;
          const clean = line.replace(/^[-🛍️🔥⚡⭐💥📦📍🏷️✅✔️•*\s]+/, '').replace(/<[^>]*>/g, '').trim();
          if (clean.length >= 4 && !isBoilerplate(clean) && !clean.match(/^[A-Z0-9_-]{4,20}$/)) {
            title = clean;
            break;
          }
        }
      }

      if (!title) {
        for (const line of lines) {
          if (!line.includes('http') && !line.includes('@') && !line.includes('t.me') && line.length >= 4) {
            const clean = line.replace(/^[-🛍️🔥⚡⭐💥📦📍🏷️✅✔️•*\s]+/, '').trim();
            if (clean.length >= 4) {
              title = clean;
              break;
            }
          }
        }
      }

      if (!title) title = 'صفقة AliExpress مميزة';

      // 2. Pricing Extraction
      let priceUsd = null;
      let priceEur = null;
      const usdMatch = text.match(/(?:\$|US\s*\$|USD\s*)\s*([0-9]+[.,][0-9]{1,2})/i) || text.match(/([0-9]+[.,][0-9]{1,2})\s*(?:\bUSD\b|\$)/i);
      if (usdMatch) priceUsd = parseFloat(usdMatch[1].replace(',', '.'));

      const eurMatch = text.match(/(?:€|EUR\s*)\s*([0-9]+[.,][0-9]{1,2})/i) || text.match(/([0-9]+[.,][0-9]{1,2})\s*(?:€|\bEUR\b)/i);
      if (eurMatch) priceEur = parseFloat(eurMatch[1].replace(',', '.'));

      let priceDzd = null;
      if (priceUsd) priceDzd = Math.round(priceUsd * usdt);
      else if (priceEur) priceDzd = Math.round(priceEur * (usdt * 1.08));

      // 3. Coupon Extraction
      let coupon = null;
      const cleanNorm = text.replace(/[\u0640]/g, '');
      const couponMatch = 
        cleanNorm.match(/(?:(?:ال)?كـ?وبون(?:\s*الخصم|\s*خاص)?|(?:ال)?كـ?ود(?:\s*الخصم|\s*التخفيض)?|code\s*promo|code\s*de\s*r[ée]duction|code\s*r[ée]duction|coupon|promo|code|avec\s*le\s*code|utilisez\s*le\s*code)\s*[-:：]?\s*(?:<code>|\*\*|`)*([A-Za-z0-9_-]{3,20})/i)
        || cleanNorm.match(/(?:(?:ال)?قسيمـ?ة(?:\s*البائع|\s*المتجر)?|coupon\s*vendeur|store\s*coupon)\s*[-:：]?\s*(?:<code>|\*\*|`)*([0-9]+(?:\.[0-9]+)?\$?|[A-Za-z0-9_-]{3,20})/i)
        || cleanNorm.match(/[🏷️🎟️🎫]\s*(?:code\s*[:：]?)?\s*(?:<code>|\*\*|`)*([A-Za-z0-9_-]{3,20})/i)
        || cleanNorm.match(new RegExp('(?:كود|كوبون|code|promo)[^\\r\\n]{0,60}?(?:<code>|`)([A-Za-z0-9_-]{3,20})(?:<\\/code>|`)', 'i'));

      if (couponMatch) {
        let rawCode = (couponMatch[1] || '').trim().replace(/[<>/`*#]/g, '');
        const bl = ['http', 'https', 'aliexpress', 'tme', 'link', 'item', 'click', 'coins', 'bot', 'france', 'canada', 'algerie', 'promo', 'reduction', 'code'];
        if (rawCode.length >= 3 && !bl.some(b => rawCode.toLowerCase().includes(b))) {
          coupon = rawCode.toUpperCase();
        }
      }

      // 4. Coins Detection
      const hasCoins = text.includes('عملات') || text.includes('Coins') || text.includes('coins') || text.includes('🪙');

      // 5. Country Recommendation
      let country = null;
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
      } else if (/(?:خلي\s*البلد\s*كندا|بلد\s*الحساب\s*كندا|ضع\s*البلد\s*كندا)/i.test(cleanNorm)) {
        country = "كندا 🇨🇦";
      }

      // 6. Extracted AliExpress Link
      const urlMatches = text.match(/https?:\/\/(?:[a-zA-Z0-9_\-\.]+\.)?(?:aliexpress\.com|s\.click\.aliexpress\.com)[^\s"'>)]+/gi) || [];
      const affiliateUrl = urlMatches.length > 0 ? urlMatches[0] : null;

      // 7. Category
      let category = 'عام';
      let categoryIcon = 'fa-tag';
      const lower = text.toLowerCase();
      if (/phone|هاتف|téléphone|xiaomi|redmi|poco|realme|infinix|samsung|iphone|tablet|تابلت/.test(lower)) {
        category = 'هواتف وأجهزة لوحية';
        categoryIcon = 'fa-mobile-screen-button';
      } else if (/gaming|قيمنق|gamepad|gamesir|controller|rgb|pc gamer|playstation|xbox/.test(lower)) {
        category = 'ألعاب وقيمنق';
        categoryIcon = 'fa-gamepad';
      } else if (/headphone|earphone|earbuds|سماعة|سماعات|anker|soundcore|audio|tws|bluetooth/.test(lower)) {
        category = 'صوتيات وسماعات';
        categoryIcon = 'fa-headphones';
      } else if (/charger|شاحن|ugreen|baseus|powerbank|cable|usb|adapter|محول|فلاش/.test(lower)) {
        category = 'ملحقات وشواحن';
        categoryIcon = 'fa-bolt';
      } else if (/تجميع|تجميعة|packs|bundle|عدة منتجات/.test(lower)) {
        category = 'تجميعات اقتصادية';
        categoryIcon = 'fa-boxes-packing';
      }

      return {
        id: post.id || '',
        raw: post,
        title,
        priceUsd,
        priceEur,
        priceDzd,
        coupon,
        hasCoins,
        country,
        category,
        categoryIcon,
        affiliateUrl,
        telegramUrl: post.link || null,
        date: post.date || '',
        text: text
      };
    }

    // Render Full Deal Card
    function renderAdminDealCard(deal, index) {
      const isFrance = currentFeedChannel === '@francedealsdz';
      const safeTitle = escapeHtml(deal.title);

      return `
        <article class="solid-panel rounded-2xl p-4 sm:p-5 card-hover space-y-4">
          
          <!-- Top Header: Channel Tag, Date & Time, Telegram Link -->
          <div class="flex items-center justify-between flex-wrap gap-2 pb-3 border-b border-[#1f293d]">
            <div class="flex items-center gap-2">
              <span class="px-2.5 py-0.5 rounded-lg text-xs font-bold ${isFrance ? 'bg-sky-500/10 text-sky-400 border border-sky-500/20' : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'}">
                ${isFrance ? '🇫🇷 @francedealsdz' : '🇩🇿 @DzAliexpress0'}
              </span>
              <span class="text-xs font-mono text-slate-400 flex items-center gap-1.5">
                <i class="fa-regular fa-clock text-[10px] text-slate-500"></i>
                <span>${escapeHtml(deal.date)}</span>
              </span>
            </div>

            <div class="flex items-center gap-2">
              ${deal.telegramUrl ? `
                <a href="${deal.telegramUrl}" target="_blank" rel="noopener noreferrer" class="text-xs text-rose-400 hover:text-rose-300 font-bold flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-[#141a28] border border-[#1f293d] hover:border-rose-500/40 transition active:scale-95">
                  <i class="fa-brands fa-telegram text-rose-500"></i>
                  <span>فتح بالتيليجرام ↗</span>
                </a>
              ` : ''}
            </div>
          </div>

          <!-- Main Info: Image + Details + Badges -->
          <div class="flex flex-col sm:flex-row items-start gap-4">
            
            <!-- Product Photo -->
            ${deal.raw.photo_url ? `
              <div class="relative w-full sm:w-36 h-36 rounded-xl bg-[#06080d] border border-[#1f293d] overflow-hidden flex-shrink-0 group flex items-center justify-center">
                <img src="${deal.raw.photo_url}" class="w-full h-full object-contain p-1 group-hover:scale-105 transition-transform duration-200" loading="lazy">
                <a href="${deal.raw.photo_url}" target="_blank" class="absolute bottom-1.5 left-1.5 bg-black/80 hover:bg-black text-white text-[10px] px-2 py-0.5 rounded border border-white/20 transition flex items-center gap-1">
                  <i class="fa-solid fa-up-right-and-down-left-from-center text-[9px]"></i>
                  <span>تكبير</span>
                </a>
              </div>
            ` : `
              <div class="w-full sm:w-36 h-36 rounded-xl bg-[#141a28] border border-[#1f293d] flex flex-col items-center justify-center text-slate-600 flex-shrink-0">
                <i class="fa-solid fa-bag-shopping text-3xl mb-1 text-slate-500"></i>
                <span class="text-[10px] text-slate-400">بدون صورة</span>
              </div>
            `}

            <!-- Content Details -->
            <div class="flex-1 min-w-0 space-y-2.5 w-full">
              
              <!-- Clean Extracted Title -->
              <h4 class="font-bold text-base sm:text-lg text-white font-heading leading-snug">
                ${safeTitle}
              </h4>

              <!-- Prices Breakdown -->
              <div class="flex items-center flex-wrap gap-2 pt-0.5">
                ${deal.priceUsd ? `
                  <div class="flex items-center gap-1.5 px-3 py-1 rounded-xl bg-emerald-500/10 border border-emerald-500/25 text-emerald-400 font-mono font-bold text-sm sm:text-base">
                    <span class="text-xs opacity-75">$</span>
                    <span>${deal.priceUsd.toFixed(2)}</span>
                  </div>
                ` : ''}

                ${deal.priceEur ? `
                  <div class="flex items-center gap-1.5 px-3 py-1 rounded-xl bg-sky-500/10 border border-sky-500/25 text-sky-400 font-mono font-bold text-sm sm:text-base">
                    <span>${deal.priceEur.toFixed(2)}</span>
                    <span class="text-xs opacity-75">€</span>
                  </div>
                ` : ''}

                ${deal.priceDzd ? `
                  <div class="flex items-center gap-1.5 px-3 py-1 rounded-xl bg-amber-500/10 border border-amber-500/25 text-amber-300 font-mono font-bold text-sm sm:text-base">
                    <span>≈ ${deal.priceDzd.toLocaleString()} دج</span>
                  </div>
                ` : ''}
              </div>

              <!-- Feature Badges: Category, Coupon, Coins, Country -->
              <div class="flex items-center flex-wrap gap-2 text-xs">
                <span class="px-2.5 py-1 rounded-lg bg-[#141a28] border border-[#1f293d] text-slate-300 flex items-center gap-1.5 font-medium">
                  <i class="fa-solid ${deal.categoryIcon} text-rose-400 text-[11px]"></i>
                  <span>${escapeHtml(deal.category)}</span>
                </span>

                ${deal.coupon ? `
                  <div class="flex items-center rounded-lg bg-[#141a28] border border-rose-500/30 overflow-hidden text-rose-300">
                    <span class="px-2.5 py-1 font-mono font-bold tracking-wider flex items-center gap-1">
                      <i class="fa-solid fa-ticket text-rose-400 text-[10px]"></i>
                      <span>${escapeHtml(deal.coupon)}</span>
                    </span>
                    <button onclick="copyToClipboard('${escapeHtml(deal.coupon)}', this, 'كود الكوبون')" class="px-2.5 py-1 bg-rose-500/20 hover:bg-rose-500/30 text-rose-300 border-r border-rose-500/30 transition text-[11px] font-bold">
                      نسخ
                    </button>
                  </div>
                ` : ''}

                ${deal.hasCoins ? `
                  <span class="px-2.5 py-1 rounded-lg bg-amber-500/10 border border-amber-500/25 text-amber-300 flex items-center gap-1.5 font-bold">
                    <i class="fa-solid fa-coins text-amber-400 text-[11px]"></i>
                    <span>خصم العملات Coins</span>
                  </span>
                ` : ''}

                ${deal.country ? `
                  <span class="px-2.5 py-1 rounded-lg bg-[#141a28] border border-[#1f293d] text-slate-300 flex items-center gap-1">
                    <i class="fa-solid fa-location-dot text-blue-400 text-[10px]"></i>
                    <span>${escapeHtml(deal.country)}</span>
                  </span>
                ` : ''}
              </div>

              <!-- Direct Action Buttons -->
              <div class="flex items-center flex-wrap gap-2 pt-1.5">
                ${deal.affiliateUrl ? `
                  <a href="${deal.affiliateUrl}" target="_blank" rel="noopener noreferrer" class="px-3.5 py-2 rounded-xl bg-gradient-to-r from-rose-600 to-amber-600 hover:from-rose-500 hover:to-amber-500 text-white font-bold text-xs flex items-center gap-1.5 shadow transition active:scale-95 border border-rose-400/20">
                    <i class="fa-solid fa-cart-shopping"></i>
                    <span>رابط الشراء على AliExpress ↗</span>
                  </a>
                  <button onclick="copyToClipboard('${deal.affiliateUrl}', this, 'رابط المنتج')" class="px-3 py-2 rounded-xl bg-[#141a28] hover:bg-[#1e2638] border border-[#1f293d] text-slate-300 hover:text-white text-xs font-bold flex items-center gap-1.5 transition active:scale-95">
                    <i class="fa-regular fa-copy"></i>
                    <span>نسخ الرابط</span>
                  </button>
                ` : ''}
                <button onclick="sendDealToReformatter(${index})" class="px-3 py-2 rounded-xl bg-[#141a28] hover:bg-[#1e2638] border border-[#1f293d] text-amber-400 hover:text-amber-300 text-xs font-bold flex items-center gap-1.5 transition active:scale-95">
                  <i class="fa-solid fa-wand-magic-sparkles"></i>
                  <span>تعديل وإعادة النشر ⚡</span>
                </button>
              </div>

            </div>
          </div>

          <!-- FULL DETAILS: Complete, Uncut Deal Text -->
          <div class="pt-3 border-t border-[#1f293d] space-y-2">
            <div class="flex items-center justify-between text-xs">
              <span class="font-bold text-slate-400 flex items-center gap-1.5">
                <i class="fa-solid fa-align-right text-rose-500"></i>
                <span>تفاصيل المنشور الكاملة (Full Uncut Text):</span>
              </span>
              <button onclick="copyToClipboard(currentParsedPosts[${index}].text, this, 'نص المنشور الكامل')" class="text-[11px] text-slate-400 hover:text-white flex items-center gap-1.5 transition px-2.5 py-1 rounded-lg bg-[#141a28] border border-[#1f293d] hover:border-slate-500">
                <i class="fa-regular fa-copy"></i>
                <span>نسخ النص كاملاً</span>
              </button>
            </div>
            
            <div class="rounded-xl p-3.5 border border-[#1f293d] bg-[#070a10] text-slate-200 text-xs leading-relaxed font-sans whitespace-pre-wrap select-text">
${formatPostTextWithLinks(deal.text)}
            </div>
          </div>

        </article>
      `;
    }

    // Real-Time Search Filter
    function filterFeedPosts() {
      const input = document.getElementById('feed-search-input');
      const query = (input ? input.value : '').trim().toLowerCase();
      const container = document.getElementById('posts-container');
      if (!container) return;

      const filtered = currentParsedPosts.filter(d => {
        if (!query) return true;
        return (
          d.title.toLowerCase().includes(query) ||
          d.text.toLowerCase().includes(query) ||
          (d.coupon && d.coupon.toLowerCase().includes(query)) ||
          d.category.toLowerCase().includes(query)
        );
      });

      if (filtered.length === 0) {
        container.innerHTML = `<div class="solid-panel rounded-2xl p-8 text-center text-slate-400 space-y-2">
          <i class="fa-solid fa-magnifying-glass text-slate-600 text-2xl"></i>
          <div>لا توجد نتائج تطابق بحثك: <span class="text-rose-400 font-bold">${escapeHtml(query)}</span></div>
        </div>`;
      } else {
        container.innerHTML = filtered.map((d, idx) => renderAdminDealCard(d, idx)).join('');
      }
    }

    // Send Deal to Reformatting Tool
    function sendDealToReformatter(idx) {
      const deal = currentParsedPosts[idx];
      if (!deal) return;
      const refInput = document.getElementById('reformat-input');
      if (refInput) {
        refInput.value = deal.text;
        refInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
        reformatTelegramPost();
      }
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
            currentLiveRate = rData.rate;
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
            container.innerHTML = '<div class="solid-panel rounded-2xl p-8 text-center text-slate-400">لا توجد منشورات حالياً في القناة.</div>';
            container.classList.remove('hidden');
          }
          return;
        }

        currentRawPosts = data.posts;
        currentParsedPosts = currentRawPosts.map(p => parseAdminDeal(p, currentLiveRate));

        document.getElementById('stat-total').innerText = currentRawPosts.length;
        document.getElementById('stat-photos').innerText = currentRawPosts.filter(p => p.photo_url).length;
        document.getElementById('posts-badge').innerText = currentRawPosts.length;
        document.getElementById('last-update').innerText = 'تم التحديث ' + new Date().toLocaleTimeString('ar-DZ');

        container.innerHTML = currentParsedPosts.map((d, idx) => renderAdminDealCard(d, idx)).join('');
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
        let textToFill = lastScoutedDeal.coin_link || lastScoutedDeal.deal_link || lastScoutedDeal.product_link || '';
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
        const manualP = (document.getElementById('reformat-manual-price') ? document.getElementById('reformat-manual-price').value.trim() : '');
        const activeLinkType = (currentReformattedDeal && currentReformattedDeal.link_type) || 'coin';
        const resp = await fetch('/api/reformat-deal', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ 
            text: val, 
            price: manualP || null,
            link_type: activeLinkType 
          })
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
          const cardPriceInp = document.getElementById('reformat-card-price-input');
          if (cardPriceInp) {
            cardPriceInp.value = data.price ? data.price.toFixed(2) : '';
          }
          const manualPriceInp = document.getElementById('reformat-manual-price');
          if (manualPriceInp && data.price && !manualPriceInp.value) {
            manualPriceInp.value = data.price.toFixed(2);
          }
          
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
          if (typeof setReformatLinkType === 'function') {
            setReformatLinkType(data.link_type || 'coin', false);
          }
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

    function setReformatLinkType(type, notify = true) {
      if (!currentReformattedDeal) return;
      
      let targetUrl = currentReformattedDeal.deal_link;
      let badgeText = 'رابط مخصص';
      let badgeClass = 'bg-slate-700/50 text-slate-300 border-slate-600/30';
      
      if (type === 'coin') {
        targetUrl = currentReformattedDeal.coin_link || currentReformattedDeal.deal_link;
        badgeText = '🪙 صفحة تخفيض العملات (Coins)';
        badgeClass = 'bg-amber-500/10 text-amber-300 border-amber-500/20';
      } else if (type === 'direct') {
        targetUrl = currentReformattedDeal.direct_link || currentReformattedDeal.deal_link;
        badgeText = '🛒 رابط المنتج المباشر (Direct)';
        badgeClass = 'bg-blue-500/10 text-blue-300 border-blue-500/20';
      } else if (type === 'bundle') {
        targetUrl = currentReformattedDeal.bundle_link || currentReformattedDeal.deal_link;
        badgeText = '📦 عروض الحزم (Bundle Deals)';
        badgeClass = 'bg-purple-500/10 text-purple-300 border-purple-500/20';
      } else if (type === 'super') {
        targetUrl = currentReformattedDeal.super_link || currentReformattedDeal.deal_link;
        badgeText = '⚡ عروض Super Deals';
        badgeClass = 'bg-rose-500/10 text-rose-300 border-rose-500/20';
      }
      
      if (!targetUrl) return;

      const oldUrl = currentReformattedDeal.deal_link;
      currentReformattedDeal.deal_link = targetUrl;
      currentReformattedDeal.link_type = type;

      // Update caption textarea
      const captionArea = document.getElementById('reformat-caption');
      if (captionArea && targetUrl) {
        if (oldUrl && captionArea.value.includes(oldUrl)) {
          captionArea.value = captionArea.value.replace(oldUrl, targetUrl);
        } else {
          captionArea.value = captionArea.value.replace(/https?:\/\/(?:s\.click\.aliexpress\.com\/e\/[A-Za-z0-9_-]+|(?:[a-z0-9-]+\.)?aliexpress\.com\/[^\s\n<]+)/i, targetUrl);
        }
        updateCaptionCharCount();
      }

      // Update check link href
      const linkCheck = document.getElementById('reformat-deal-link');
      if (linkCheck) linkCheck.href = targetUrl;

      // Update badge
      const badge = document.getElementById('reformat-active-link-badge');
      if (badge) {
        badge.innerText = badgeText;
        badge.className = `text-[10px] font-bold px-2 py-0.5 rounded border ${badgeClass}`;
      }

      // Update button styles
      ['coin', 'direct', 'bundle', 'super'].forEach(t => {
        const btn = document.getElementById('opt-link-' + t);
        if (btn) {
          if (t === type) {
            btn.className = 'px-2.5 py-1 rounded-lg text-xs font-bold transition bg-amber-500 text-slate-950 shadow';
          } else {
            btn.className = 'px-2.5 py-1 rounded-lg text-xs font-medium transition text-slate-400 hover:text-white bg-slate-800';
          }
        }
      });
      if (notify) {
        showToast('تم ضبط نوع الرابط إلى: ' + badgeText, 'info');
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

    function onAdminPriceEdit(newVal) {
      if (!currentReformattedDeal) return;
      const p = parseFloat(newVal);
      if (isNaN(p) || p <= 0) return;

      currentReformattedDeal.price = p;
      const eurRate = 0.92;
      const eurPrice = Math.round(p * eurRate * 100) / 100;
      currentReformattedDeal.price_eur = eurPrice;

      const rate = currentLiveRate || 249.0;
      const dzd = Math.round(p * rate);
      currentReformattedDeal.price_dzd = dzd;

      const dzdEl = document.getElementById('reformat-price-dzd');
      if (dzdEl) dzdEl.innerText = '~ ' + dzd.toLocaleString() + ' دج';

      const eurEl = document.getElementById('reformat-price-eur');
      if (eurEl) {
        eurEl.innerText = eurPrice.toFixed(2) + '€';
        eurEl.classList.remove('hidden');
      }

      const captionArea = document.getElementById('reformat-caption');
      if (captionArea) {
        const pRegex = /(💰\s*<b>\s*السعر\s*[:：]\s*<\/b>\s*<b>\s*\$)[0-9]+(?:\.[0-9]+)?(\s*<\/b>)/i;
        if (pRegex.test(captionArea.value)) {
          captionArea.value = captionArea.value.replace(pRegex, `$1${p.toFixed(2)}$2`);
        } else {
          const fallbackRegex = /(💰\s*السعر\s*[:：]?\s*\$)[0-9]+(?:\.[0-9]+)?/i;
          if (fallbackRegex.test(captionArea.value)) {
            captionArea.value = captionArea.value.replace(fallbackRegex, `$1${p.toFixed(2)}`);
          }
        }
        updateCaptionCharCount();
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
            target_channel: currentReformattedDeal.target_channel || (isFrance ? '@francedealsdz' : '@DzAliexpress0'),
            post_to_facebook: document.getElementById('reformat-fb-toggle')?.checked ?? false
          })
        });
        const data = await resp.json();

        if (data.ok) {
          const fbOk = data.facebook && data.facebook.published;
          const fbErr = data.facebook && data.facebook.error;
          feedback.className = 'p-3 rounded-xl text-xs font-medium bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2';
          feedback.innerHTML = `
            <div class="flex items-center gap-2 flex-wrap">
              <i class="fa-solid fa-circle-check text-emerald-400 text-sm"></i>
              <span>تم نشر المنشور في القناة بنجاح! (#${data.message_id})</span>
              ${fbOk ? `<span class="bg-blue-600/30 text-blue-300 border border-blue-500/40 px-2 py-0.5 rounded text-[10px] font-bold flex items-center gap-1"><i class="fa-brands fa-facebook"></i> نُشر على فيسبوك</span>` : ''}
              ${fbErr && !fbOk && document.getElementById('reformat-fb-toggle')?.checked ? `<span class="bg-amber-500/20 text-amber-300 border border-amber-500/30 px-2 py-0.5 rounded text-[10px]" title="${escapeHtml(fbErr)}">⚠️ فيسبوك: غير مهيأ أو حدث خطأ</span>` : ''}
            </div>
            ${data.post_url ? `<a href="${data.post_url}" target="_blank" class="bg-emerald-600 hover:bg-emerald-500 text-white px-2.5 py-1 rounded-lg text-[11px] font-bold">عرض بالتيليجرام</a>` : ''}
          `;
          feedback.classList.remove('hidden');
          showToast('تم نشر المنشور بنجاح! #' + data.message_id + (fbOk ? ' (وفيسبوك ✅)' : ''), 'success');
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

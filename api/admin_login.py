"""
DealScout DZ — Admin Login Interface
Secures /admin and /dashboard behind a password-protected authentication screen.
Redesigned to perfectly match the main platform's modern obsidian dark theme, dot-matrix textures,
and crisp typography (Cairo, Readex Pro, Plus Jakarta Sans).
"""

ADMIN_LOGIN_HTML = """<!DOCTYPE html>
<html lang="ar" dir="rtl" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, viewport-fit=cover">
  <meta name="referrer" content="no-referrer">
  <title>تسجيل دخول الأدمن | DealScout DZ Admin</title>
  <link rel="icon" type="image/png" href="/logo_circular.png">
  <link rel="apple-touch-icon" href="/logo_circular.png">
  <meta name="theme-color" content="#06080d">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">

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
              mono: ['"JetBrains Mono"', 'ui-monospace', 'monospace']
            }
          }
        }
      };
    }
  </script>

  <style>
    :root {
      --bg-page: #06080d;
      --bg-card: rgba(14, 18, 27, 0.94);
      --bg-card-hover: rgba(20, 26, 40, 0.98);
      --border-card: rgba(255, 255, 255, 0.09);
      --border-subtle: rgba(255, 255, 255, 0.16);
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-soft: #64748b;
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
    }
    .glass-card {
      background: var(--bg-card);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid var(--border-card);
      box-shadow: var(--shadow-card);
    }
  </style>
</head>
<body class="min-h-screen flex flex-col justify-between selection:bg-rose-500 selection:text-white p-4">

  <!-- Ambient Obsidian Glow -->
  <div class="fixed top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-rose-600/10 blur-3xl rounded-full pointer-events-none -z-10"></div>
  <div class="fixed bottom-1/4 left-1/3 w-80 h-80 bg-amber-500/5 blur-3xl rounded-full pointer-events-none -z-10"></div>

  <!-- Header minimal -->
  <header class="max-w-md mx-auto w-full flex items-center justify-between py-4">
    <a href="/" class="inline-flex items-center gap-2 text-xs text-slate-400 hover:text-slate-100 transition py-1 px-2.5 rounded-lg hover:bg-white/5 border border-transparent hover:border-white/10">
      <i class="fa-solid fa-arrow-right text-[11px]"></i>
      <span class="font-medium">العودة لموقع العروض</span>
    </a>
    <div class="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-rose-500/10 border border-rose-500/20 text-[11px] font-mono text-rose-400">
      <span class="w-1.5 h-1.5 rounded-full bg-rose-500 animate-pulse"></span>
      <span>Admin Gateway v2.8</span>
    </div>
  </header>

  <!-- Login Card -->
  <main class="max-w-md mx-auto w-full my-auto py-6">
    <div class="glass-card rounded-3xl p-6 sm:p-8 space-y-6">
      
      <!-- Brand & Icon -->
      <div class="text-center space-y-3">
        <div class="w-16 h-16 rounded-2xl bg-gradient-to-tr from-rose-600 via-rose-500 to-amber-500 mx-auto flex items-center justify-center text-white shadow-xl shadow-rose-600/25 border border-white/20">
          <i class="fa-solid fa-shield-halved text-2xl"></i>
        </div>
        <div>
          <h1 class="text-xl sm:text-2xl font-black text-white font-heading">لوحة تحكم الأدمن 🔐</h1>
          <p class="text-xs text-slate-400 mt-1">منطقة محمية ومخصصة لإدارة ونشر صفقات DealScout DZ</p>
        </div>
      </div>

      <!-- Error Alert Box -->
      <div id="login-error" class="hidden p-3.5 rounded-2xl bg-rose-500/10 border border-rose-500/25 text-rose-300 text-xs flex items-center gap-2.5 animate-pulse">
        <i class="fa-solid fa-triangle-exclamation text-rose-400 text-sm flex-shrink-0"></i>
        <span id="login-error-text" class="flex-1 font-medium leading-relaxed">كلمة المرور غير صحيحة!</span>
      </div>

      <!-- Password Form -->
      <form id="admin-login-form" onsubmit="handleLogin(event)" class="space-y-4">
        <div>
          <label for="admin-pass" class="block text-xs font-bold text-slate-300 mb-2">كلمة مرور الأدمن (ADMIN_PASSWORD):</label>
          <div class="relative">
            <i class="fa-solid fa-key absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 text-sm"></i>
            <input 
              type="password" 
              id="admin-pass" 
              required
              autofocus
              placeholder="أدخل كلمة المرور..." 
              class="w-full bg-black/40 border border-white/10 rounded-2xl pr-10 pl-11 py-3 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500 font-mono transition"
            />
            <button 
              type="button" 
              onclick="togglePassVisibility()" 
              aria-label="إظهار / إخفاء كلمة المرور"
              class="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-200 transition text-sm p-1"
            >
              <i class="fa-solid fa-eye" id="pass-eye"></i>
            </button>
          </div>
        </div>

        <button 
          type="submit" 
          id="login-btn" 
          class="w-full bg-gradient-to-r from-rose-600 to-rose-500 hover:from-rose-500 hover:to-rose-600 text-white font-bold text-sm py-3 px-4 rounded-2xl shadow-lg shadow-rose-600/30 flex items-center justify-center gap-2 transition active:scale-95 border border-rose-400/30"
        >
          <i class="fa-solid fa-lock-open" id="login-btn-icon"></i>
          <span id="login-btn-text">تسجيل الدخول</span>
        </button>
      </form>

      <!-- Security Notice -->
      <div class="pt-2 text-center text-[11px] text-slate-500 flex items-center justify-center gap-1.5 border-t border-white/5">
        <i class="fa-solid fa-lock text-[10px]"></i>
        <span>جلسة مشفرة ومؤمنة بـ HTTPS و HttpOnly Cookie</span>
      </div>

    </div>
  </main>

  <!-- Footer minimal -->
  <footer class="max-w-md mx-auto w-full text-center py-4 text-xs text-slate-500 font-mono">
    DealScout DZ Admin Gateway • @DzAliexpress0
  </footer>

  <script>
    function togglePassVisibility() {
      const input = document.getElementById('admin-pass');
      const eye = document.getElementById('pass-eye');
      if (input.type === 'password') {
        input.type = 'text';
        eye.className = 'fa-solid fa-eye-slash';
      } else {
        input.type = 'password';
        eye.className = 'fa-solid fa-eye';
      }
    }

    async function handleLogin(e) {
      e.preventDefault();
      const pass = document.getElementById('admin-pass').value;
      const btn = document.getElementById('login-btn');
      const btnText = document.getElementById('login-btn-text');
      const btnIcon = document.getElementById('login-btn-icon');
      const errBox = document.getElementById('login-error');
      const errText = document.getElementById('login-error-text');

      errBox.classList.add('hidden');
      btn.disabled = true;
      btnIcon.className = 'fa-solid fa-spinner fa-spin';
      btnText.textContent = 'جاري التحقق...';

      try {
        const resp = await fetch('/api/admin/login', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({password: pass})
        });

        const data = await resp.json();
        if (resp.ok && data.success) {
          btnIcon.className = 'fa-solid fa-circle-check';
          btnText.textContent = 'تم تسجيل الدخول!';
          btn.classList.remove('from-rose-600', 'to-rose-500');
          btn.classList.add('bg-emerald-600');
          setTimeout(() => {
            window.location.reload();
          }, 350);
        } else {
          errText.textContent = data.error || 'كلمة المرور غير صحيحة!';
          errBox.classList.remove('hidden');
          btn.disabled = false;
          btnIcon.className = 'fa-solid fa-lock-open';
          btnText.textContent = 'تسجيل الدخول';
        }
      } catch (err) {
        errText.textContent = 'تعذر الاتصال بالخادم، يرجى المحاولة ثانية.';
        errBox.classList.remove('hidden');
        btn.disabled = false;
        btnIcon.className = 'fa-solid fa-lock-open';
        btnText.textContent = 'تسجيل الدخول';
      }
    }
  </script>

</body>
</html>"""

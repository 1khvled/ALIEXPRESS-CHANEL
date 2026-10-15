"""
DealScout DZ — Admin Login Interface
Secures /admin and /dashboard behind a password-protected authentication screen.
"""

ADMIN_LOGIN_HTML = """<!DOCTYPE html>
<html lang="ar" dir="rtl" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>تسجيل دخول الأدمن | DealScout DZ</title>
  <link rel="icon" type="image/svg+xml" href="/icon.svg">
  <meta name="theme-color" content="#e11d48">
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">

  <style>
    body {
      font-family: 'Tajawal', sans-serif;
      background-color: #030712;
      color: #f1f5f9;
      -webkit-tap-highlight-color: transparent;
    }
    .glass-panel {
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .glow-box {
      box-shadow: 0 0 35px -5px rgba(225, 29, 72, 0.25);
    }
  </style>
</head>
<body class="min-h-screen bg-slate-950 flex flex-col justify-between selection:bg-rose-500 selection:text-white p-4">

  <!-- Ambient Glow -->
  <div class="fixed top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-rose-600/15 blur-3xl rounded-full pointer-events-none -z-10"></div>
  <div class="fixed top-2/3 left-1/3 w-80 h-80 bg-amber-500/10 blur-3xl rounded-full pointer-events-none -z-10"></div>

  <!-- Header minimal -->
  <header class="max-w-md mx-auto w-full flex items-center justify-between py-4">
    <a href="/" class="flex items-center gap-2 text-xs text-slate-400 hover:text-slate-200 transition">
      <i class="fa-solid fa-arrow-right"></i>
      <span>العودة لموقع العروض</span>
    </a>
    <span class="text-[11px] font-mono text-slate-500">DealScout Security v2.5</span>
  </header>

  <!-- Login Card -->
  <main class="max-w-md mx-auto w-full my-auto">
    <div class="glass-panel glow-box rounded-3xl p-6 sm:p-8 border border-slate-800 space-y-6">
      
      <!-- Brand & Icon -->
      <div class="text-center space-y-3">
        <div class="w-16 h-16 rounded-3xl bg-gradient-to-tr from-rose-600 via-rose-500 to-amber-500 mx-auto flex items-center justify-center text-white shadow-xl shadow-rose-600/30">
          <i class="fa-solid fa-shield-halved text-2xl"></i>
        </div>
        <div>
          <h1 class="text-xl sm:text-2xl font-black text-white">لوحة تحكم الأدمن 🔐</h1>
          <p class="text-xs text-slate-400 mt-1">منطقة محمية مخصصة لإدارة ونشر الصفقات</p>
        </div>
      </div>

      <!-- Error Alert Box -->
      <div id="login-error" class="hidden p-3 rounded-2xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs flex items-center gap-2">
        <i class="fa-solid fa-triangle-exclamation"></i>
        <span id="login-error-text">كلمة المرور غير صحيحة!</span>
      </div>

      <!-- Password Form -->
      <form id="admin-login-form" onsubmit="handleLogin(event)" class="space-y-4">
        <div>
          <label for="admin-pass" class="block text-xs font-bold text-slate-300 mb-1.5">كلمة مرور الأدمن:</label>
          <div class="relative">
            <i class="fa-solid fa-key absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 text-sm"></i>
            <input 
              type="password" 
              id="admin-pass" 
              required
              placeholder="أدخل كلمة المرور..." 
              class="w-full bg-slate-900 border border-slate-700/80 rounded-2xl pr-10 pl-11 py-3 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500 transition"
            />
            <button 
              type="button" 
              onclick="togglePassVisibility()" 
              class="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-200 transition text-sm"
            >
              <i class="fa-solid fa-eye" id="pass-eye"></i>
            </button>
          </div>
        </div>

        <button 
          type="submit" 
          id="login-btn" 
          class="w-full bg-gradient-to-r from-rose-600 to-amber-600 hover:from-rose-500 hover:to-amber-500 text-white font-black text-sm py-3 px-4 rounded-2xl shadow-lg shadow-rose-600/30 flex items-center justify-center gap-2 transition active:scale-95"
        >
          <i class="fa-solid fa-lock-open" id="login-btn-icon"></i>
          <span id="login-btn-text">تسجيل الدخول</span>
        </button>
      </form>

      <!-- Security Notice -->
      <div class="pt-2 text-center text-[11px] text-slate-500 flex items-center justify-center gap-1.5">
        <i class="fa-solid fa-lock text-[10px]"></i>
        <span>جلسة مشفرة ومؤمنة بـ HTTPS و HttpOnly Cookies</span>
      </div>

    </div>
  </main>

  <!-- Footer minimal -->
  <footer class="max-w-md mx-auto w-full text-center py-4 text-xs text-slate-600">
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
          btn.classList.add('bg-emerald-600');
          setTimeout(() => {
            window.location.reload();
          }, 400);
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

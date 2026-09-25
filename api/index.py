"""
Vercel Serverless Entry Point — Lightweight Dashboard
Reads posts directly from @DzAliexpress0 Telegram channel web preview.
No database required.
"""
import re
from datetime import datetime, timezone
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import httpx
from bs4 import BeautifulSoup

app = FastAPI(title="DealScout Dashboard", version="1.0.0")

# ── Dashboard HTML ──────────────────────────────────────────────
DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DealScout — @DzAliexpress0 Dashboard</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <style>
    .arabic-text { direction: rtl; text-align: right; font-family: 'Segoe UI', Tahoma, sans-serif; }
    .skeleton { background: linear-gradient(90deg, #1e293b 25%, #334155 50%, #1e293b 75%); background-size: 200% 100%; animation: shimmer 1.5s infinite; }
    @keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }
    .card-hover { transition: all 0.2s; }
    .card-hover:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(0,0,0,0.3); border-color: #475569; }
    .fade-in { animation: fadeIn 0.4s ease-out; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0f172a; }
    ::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen">

  <!-- Header -->
  <header class="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 border-b border-slate-700/50 sticky top-0 z-50 backdrop-blur-sm">
    <div class="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="w-11 h-11 rounded-xl bg-gradient-to-tr from-rose-600 to-amber-500 flex items-center justify-center font-bold text-white shadow-lg shadow-rose-500/30">
          <i class="fa-solid fa-bolt text-lg"></i>
        </div>
        <div>
          <h1 class="font-bold text-lg leading-tight tracking-tight">DealScout</h1>
          <p class="text-xs text-slate-400">@DzAliexpress0 Live Dashboard</p>
        </div>
      </div>

      <div class="flex items-center space-x-3">
        <div class="hidden sm:flex items-center space-x-2 bg-emerald-500/10 border border-emerald-500/20 rounded-lg px-3 py-1.5">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span class="text-xs text-emerald-400 font-medium">Bot Active</span>
        </div>
        <button onclick="refreshPosts()" id="refresh-btn" class="bg-rose-600 hover:bg-rose-500 text-white text-xs px-4 py-2 rounded-lg font-medium shadow-lg shadow-rose-600/20 flex items-center space-x-2 transition active:scale-95">
          <i class="fa-solid fa-arrows-rotate" id="refresh-icon"></i>
          <span>Refresh</span>
        </button>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 py-6 space-y-6">

    <!-- Stats Cards -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 card-hover">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span>Total Posts</span>
          <i class="fa-solid fa-newspaper text-blue-400"></i>
        </div>
        <div id="stat-total" class="text-2xl font-bold text-blue-400">--</div>
      </div>
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 card-hover">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span>With Photos</span>
          <i class="fa-solid fa-image text-emerald-400"></i>
        </div>
        <div id="stat-photos" class="text-2xl font-bold text-emerald-400">--</div>
      </div>
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 card-hover">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span>With Links</span>
          <i class="fa-solid fa-link text-amber-400"></i>
        </div>
        <div id="stat-links" class="text-2xl font-bold text-amber-400">--</div>
      </div>
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 card-hover">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-2">
          <span>Bot Schedule</span>
          <i class="fa-solid fa-clock text-indigo-400"></i>
        </div>
        <div class="text-lg font-bold text-indigo-400">Every 5m</div>
        <p class="text-[10px] text-slate-500 mt-0.5">GitHub Actions</p>
      </div>
    </div>

    <!-- Main Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

      <!-- Posts Feed (2 cols) -->
      <div class="lg:col-span-2 space-y-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <h2 class="text-base font-bold">Channel Posts</h2>
            <span id="posts-badge" class="bg-slate-800 text-slate-400 text-xs px-2 py-0.5 rounded-full border border-slate-700">0</span>
          </div>
          <span id="last-update" class="text-xs text-slate-500"></span>
        </div>

        <!-- Loading Skeleton -->
        <div id="skeleton-container" class="space-y-3">
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-3">
            <div class="flex space-x-3"><div class="skeleton w-16 h-16 rounded-lg"></div><div class="flex-1 space-y-2"><div class="skeleton h-4 w-3/4 rounded"></div><div class="skeleton h-3 w-1/2 rounded"></div></div></div>
            <div class="skeleton h-20 rounded-lg"></div>
          </div>
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-3">
            <div class="flex space-x-3"><div class="skeleton w-16 h-16 rounded-lg"></div><div class="flex-1 space-y-2"><div class="skeleton h-4 w-2/3 rounded"></div><div class="skeleton h-3 w-1/3 rounded"></div></div></div>
            <div class="skeleton h-16 rounded-lg"></div>
          </div>
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-3">
            <div class="flex space-x-3"><div class="skeleton w-16 h-16 rounded-lg"></div><div class="flex-1 space-y-2"><div class="skeleton h-4 w-1/2 rounded"></div><div class="skeleton h-3 w-2/5 rounded"></div></div></div>
            <div class="skeleton h-24 rounded-lg"></div>
          </div>
        </div>

        <!-- Posts Container -->
        <div id="posts-container" class="space-y-3 hidden"></div>

        <!-- Empty State -->
        <div id="empty-state" class="hidden bg-slate-900 border border-slate-800 rounded-xl p-12 text-center">
          <i class="fa-solid fa-inbox text-4xl text-slate-700 mb-3"></i>
          <p class="text-slate-400">No posts found in the channel yet.</p>
          <p class="text-xs text-slate-500 mt-1">The bot posts deals every 5 minutes via GitHub Actions.</p>
        </div>

        <!-- Error State -->
        <div id="error-state" class="hidden bg-rose-950/30 border border-rose-800/40 rounded-xl p-8 text-center">
          <i class="fa-solid fa-triangle-exclamation text-3xl text-rose-400 mb-3"></i>
          <p class="text-rose-300 font-medium" id="error-message">Failed to load posts</p>
          <button onclick="refreshPosts()" class="mt-3 bg-rose-600 hover:bg-rose-500 text-white text-xs px-4 py-2 rounded-lg">Try Again</button>
        </div>
      </div>

      <!-- Right Column -->
      <div class="space-y-6">

        <!-- Promo Calendar Card -->
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-3">
          <h3 class="font-bold text-sm flex items-center justify-between">
            <span class="flex items-center space-x-2">
              <i class="fa-solid fa-calendar-days text-amber-400"></i>
              <span>AliExpress Promo Calendar</span>
            </span>
            <span class="text-[10px] bg-amber-500/10 text-amber-400 px-2 py-0.5 rounded-full border border-amber-500/20">Upcoming</span>
          </h3>
          <div class="bg-slate-950 p-3 rounded-lg border border-slate-800 space-y-1 text-xs">
            <div class="font-semibold text-rose-400">🎯 Choice Day (1 - 7 أكتوبر)</div>
            <div class="text-slate-400 text-[11px]">Starts October 1st • 7 days of mega sales & coupon tiers</div>
          </div>
          <div class="space-y-1.5 text-xs text-slate-400">
            <div class="flex items-center justify-between py-1 border-b border-slate-800/80">
              <span>Sept 20 Promos</span>
              <span class="text-rose-400 font-medium">Expired & Filtered</span>
            </div>
            <div class="flex items-center justify-between py-1">
              <span>Photo Source</span>
              <span class="text-emerald-400 font-medium">100% AliExpress CDN</span>
            </div>
          </div>
        </div>

        <!-- Bot Status Card -->
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-3">
          <h3 class="font-bold text-sm flex items-center space-x-2">
            <i class="fa-solid fa-robot text-rose-400"></i>
            <span>Bot Status</span>
          </h3>
          <div class="space-y-2 text-xs">
            <div class="flex items-center justify-between py-1.5 border-b border-slate-800">
              <span class="text-slate-400">Platform</span>
              <span class="text-slate-200 font-medium">GitHub Actions</span>
            </div>
            <div class="flex items-center justify-between py-1.5 border-b border-slate-800">
              <span class="text-slate-400">Frequency</span>
              <span class="text-emerald-400 font-medium">Every 5 minutes</span>
            </div>
            <div class="flex items-center justify-between py-1.5 border-b border-slate-800">
              <span class="text-slate-400">Target Channel</span>
              <a href="https://t.me/DzAliexpress0" target="_blank" class="text-blue-400 hover:text-blue-300">@DzAliexpress0</a>
            </div>
            <div class="flex items-center justify-between py-1.5 border-b border-slate-800">
              <span class="text-slate-400">Affiliate</span>
              <span class="text-amber-400 font-medium">s.click.aliexpress.com</span>
            </div>
            <div class="flex items-center justify-between py-1.5">
              <span class="text-slate-400">Categories</span>
              <span class="text-slate-200">Gaming, Phones, Watches, Tablets</span>
            </div>
          </div>
        </div>

        <!-- Source Channels -->
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-3">
          <h3 class="font-bold text-sm flex items-center space-x-2">
            <i class="fa-solid fa-satellite-dish text-blue-400"></i>
            <span>Source Channels</span>
          </h3>
          <div class="space-y-2">
            <div class="flex items-center justify-between py-1.5 border-b border-slate-800">
              <div class="flex items-center space-x-2">
                <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                <a href="https://t.me/lodydeals" target="_blank" class="text-xs text-slate-200 hover:text-blue-400">@lodydeals</a>
              </div>
              <span class="text-[10px] text-slate-500">Active</span>
            </div>
            <div class="flex items-center justify-between py-1.5 border-b border-slate-800">
              <div class="flex items-center space-x-2">
                <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                <a href="https://t.me/BNDDEALS" target="_blank" class="text-xs text-slate-200 hover:text-blue-400">@BNDDEALS</a>
              </div>
              <span class="text-[10px] text-slate-500">Active</span>
            </div>
            <div class="flex items-center justify-between py-1.5 border-b border-slate-800">
              <div class="flex items-center space-x-2">
                <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                <a href="https://t.me/Pcgamingpart" target="_blank" class="text-xs text-slate-200 hover:text-blue-400">@Pcgamingpart</a>
              </div>
              <span class="text-[10px] text-slate-500">Active</span>
            </div>
            <div class="flex items-center justify-between py-1.5">
              <div class="flex items-center space-x-2">
                <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                <a href="https://t.me/zedstoreonline" target="_blank" class="text-xs text-slate-200 hover:text-blue-400">@zedstoreonline</a>
              </div>
              <span class="text-[10px] text-slate-500">Active</span>
            </div>
          </div>
        </div>

        <!-- How it Works -->
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-3">
          <h3 class="font-bold text-sm flex items-center space-x-2">
            <i class="fa-solid fa-circle-info text-slate-400"></i>
            <span>How It Works</span>
          </h3>
          <div class="space-y-2 text-xs text-slate-400">
            <div class="flex items-start space-x-2">
              <span class="text-rose-400 font-bold mt-0.5">1.</span>
              <span>Bot scrapes 4 source channels every 5 min</span>
            </div>
            <div class="flex items-start space-x-2">
              <span class="text-amber-400 font-bold mt-0.5">2.</span>
              <span>Filters for gaming, phones, watches, tablets only</span>
            </div>
            <div class="flex items-start space-x-2">
              <span class="text-emerald-400 font-bold mt-0.5">3.</span>
              <span>Generates real s.click affiliate links</span>
            </div>
            <div class="flex items-start space-x-2">
              <span class="text-blue-400 font-bold mt-0.5">4.</span>
              <span>Creates branded HD product cards & publishes</span>
            </div>
          </div>
        </div>

      </div>
    </div>
  </main>

  <!-- Footer -->
  <footer class="border-t border-slate-800 mt-12 py-4 text-center text-xs text-slate-600">
    DealScout &copy; 2026 — Powered by AliExpress Open Platform API
  </footer>

  <script>
    let isLoading = false;

    async function refreshPosts() {
      if (isLoading) return;
      isLoading = true;

      const btn = document.getElementById('refresh-icon');
      btn.classList.add('animate-spin');

      const skeleton = document.getElementById('skeleton-container');
      const container = document.getElementById('posts-container');
      const empty = document.getElementById('empty-state');
      const error = document.getElementById('error-state');

      container.classList.add('hidden');
      empty.classList.add('hidden');
      error.classList.add('hidden');
      skeleton.classList.remove('hidden');

      try {
        const res = await fetch('/api/channel-posts');
        const data = await res.json();

        skeleton.classList.add('hidden');

        if (!data.posts || data.posts.length === 0) {
          empty.classList.remove('hidden');
          updateStats(0, 0, 0);
          return;
        }

        const posts = data.posts;
        updateStats(posts.length,
          posts.filter(p => p.photo_url).length,
          posts.filter(p => p.text && p.text.includes('s.click.aliexpress.com')).length
        );

        document.getElementById('posts-badge').innerText = posts.length;
        document.getElementById('last-update').innerText = 'Updated ' + new Date().toLocaleTimeString();

        container.innerHTML = posts.map((p, i) => `
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 card-hover fade-in" style="animation-delay: ${i * 50}ms">
            <div class="flex items-start gap-3">
              ${p.photo_url ? `
                <div class="w-20 h-20 rounded-lg bg-slate-800 border border-slate-700 flex-shrink-0 overflow-hidden">
                  <img src="${p.photo_url}" class="w-full h-full object-cover" loading="lazy" onerror="this.parentElement.innerHTML='<div class=\\'flex items-center justify-center w-full h-full\\'><i class=\\'fa-solid fa-image text-slate-700\\'></i></div>'">
                </div>
              ` : `
                <div class="w-20 h-20 rounded-lg bg-slate-800 border border-slate-700 flex-shrink-0 flex items-center justify-center">
                  <i class="fa-solid fa-tag text-slate-700 text-xl"></i>
                </div>
              `}
              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between mb-1">
                  <span class="text-[10px] text-slate-500">${p.date || ''}</span>
                  ${p.link ? `<a href="${p.link}" target="_blank" class="text-[10px] text-blue-400 hover:text-blue-300 flex items-center space-x-1"><i class="fa-solid fa-arrow-up-right-from-square"></i><span>Open</span></a>` : ''}
                </div>
                ${p.text ? `<pre class="arabic-text text-xs text-slate-200 whitespace-pre-wrap leading-relaxed line-clamp-6 font-sans">${escapeHtml(p.text)}</pre>` : '<span class="text-xs text-slate-500 italic">Photo only</span>'}
              </div>
            </div>
          </div>
        `).join('');

        container.classList.remove('hidden');
      } catch (e) {
        skeleton.classList.add('hidden');
        error.classList.remove('hidden');
        document.getElementById('error-message').innerText = 'Failed to load: ' + e.message;
        console.error('Fetch error:', e);
      } finally {
        isLoading = false;
        btn.classList.remove('animate-spin');
      }
    }

    function updateStats(total, photos, links) {
      document.getElementById('stat-total').innerText = total;
      document.getElementById('stat-photos').innerText = photos;
      document.getElementById('stat-links').innerText = links;
    }

    function escapeHtml(str) {
      const div = document.createElement('div');
      div.textContent = str;
      return div.innerHTML;
    }

    // Initial load + auto-refresh every 60s
    refreshPosts();
    setInterval(refreshPosts, 60000);
  </script>
</body>
</html>"""


# ── API Routes ──────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def dashboard():
    return HTMLResponse(content=DASHBOARD_HTML)


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "service": "DealScout Dashboard",
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
                headers={"User-Agent": "Mozilla/5.0 (compatible; DealScoutBot/1.0)"}
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
            # Extract text
            text_div = block.find("div", class_="tgme_widget_message_text")
            text = text_div.get_text(separator="\n").strip() if text_div else ""

            # Extract photo URL
            photo_url = None
            photo_wrap = block.find("a", class_="tgme_widget_message_photo_wrap")
            if photo_wrap and photo_wrap.get("style"):
                m = re.search(r"url\('([^']+)'\)", photo_wrap["style"])
                if m:
                    photo_url = m.group(1)

            # Extract date
            date_str = ""
            date_el = block.find("time")
            if date_el and date_el.get("datetime"):
                try:
                    dt = datetime.fromisoformat(date_el["datetime"].replace("Z", "+00:00"))
                    date_str = dt.strftime("%Y-%m-%d %H:%M")
                except Exception:
                    date_str = date_el.get("datetime", "")

            # Extract message link
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


@app.post("/api/webhook")
async def telegram_webhook(request: Request):
    """Serverless Telegram Coin & Discount Bot webhook."""
    try:
        update = await request.json()
        from api.coin_bot import handle_update
        await handle_update(update)
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@app.post("/api/admin-webhook")
async def telegram_admin_webhook(request: Request):
    """Serverless Telegram Admin Scout & Publisher Bot webhook."""
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


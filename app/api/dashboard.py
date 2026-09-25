from fastapi import APIRouter
from fastapi.responses import HTMLResponse

dashboard_router = APIRouter()

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AliExpress Telegram Deals Automation</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    [x-cloak] { display: none !important; }
    .arabic-text { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; direction: rtl; text-align: right; }
  </style>
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen">
  <!-- Top Navigation -->
  <header class="bg-slate-800 border-b border-slate-700 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-rose-600 to-amber-500 flex items-center justify-center font-bold text-white shadow-lg shadow-rose-500/20">
          <i class="fa-solid fa-bolt"></i>
        </div>
        <div>
          <h1 class="font-bold text-lg leading-tight">AliExpress Deal Bot</h1>
          <p class="text-xs text-slate-400">Telegram Deals Channel Automation</p>
        </div>
      </div>

      <div class="flex items-center space-x-4">
        <!-- Mode Selector -->
        <div class="flex items-center bg-slate-900/80 rounded-lg p-1 border border-slate-700 text-xs">
          <button onclick="setPublishMode('auto')" id="mode-auto" class="px-3 py-1 rounded font-medium transition">AUTO</button>
          <button onclick="setPublishMode('approval')" id="mode-approval" class="px-3 py-1 rounded font-medium transition">APPROVAL</button>
          <button onclick="setPublishMode('dry_run')" id="mode-dry_run" class="px-3 py-1 rounded font-medium transition">DRY RUN</button>
        </div>

        <button onclick="triggerScan()" class="bg-rose-600 hover:bg-rose-500 text-white text-xs px-3.5 py-2 rounded-lg font-medium shadow flex items-center space-x-2 transition">
          <i class="fa-solid fa-arrows-rotate"></i>
          <span>Scan 10 Channels</span>
        </button>
      </div>
    </div>
  </header>

  <!-- Main Content Container -->
  <main class="max-w-7xl mx-auto px-4 py-6 space-y-6">

    <!-- Metrics Cards -->
    <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
      <div class="bg-slate-800 border border-slate-700/80 rounded-xl p-4">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-1">
          <span>Detected Today</span>
          <i class="fa-solid fa-radar text-blue-400"></i>
        </div>
        <div id="stat-detected" class="text-2xl font-bold">--</div>
      </div>

      <div class="bg-slate-800 border border-slate-700/80 rounded-xl p-4">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-1">
          <span>Published to TG</span>
          <i class="fa-solid fa-paper-plane text-emerald-400"></i>
        </div>
        <div id="stat-published" class="text-2xl font-bold text-emerald-400">--</div>
      </div>

      <div class="bg-slate-800 border border-slate-700/80 rounded-xl p-4">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-1">
          <span>Pending Review</span>
          <i class="fa-solid fa-clock-rotate-left text-amber-400"></i>
        </div>
        <div id="stat-review" class="text-2xl font-bold text-amber-400">--</div>
      </div>

      <div class="bg-slate-800 border border-slate-700/80 rounded-xl p-4">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-1">
          <span>Skipped / Filtered</span>
          <i class="fa-solid fa-filter text-slate-400"></i>
        </div>
        <div id="stat-skipped" class="text-2xl font-bold text-slate-400">--</div>
      </div>

      <div class="bg-slate-800 border border-slate-700/80 rounded-xl p-4">
        <div class="flex items-center justify-between text-slate-400 text-xs mb-1">
          <span>Tracking Clicks</span>
          <i class="fa-solid fa-arrow-pointer text-indigo-400"></i>
        </div>
        <div id="stat-clicks" class="text-2xl font-bold text-indigo-400">--</div>
      </div>
    </div>

    <!-- Live Parser Tester & Deal Feeds Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

      <!-- Left Column: Deals Feed (2 Cols) -->
      <div class="lg:col-span-2 space-y-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <h2 class="text-base font-bold">Deals Feed</h2>
            <span id="deals-count-badge" class="bg-slate-800 text-slate-400 text-xs px-2 py-0.5 rounded-full border border-slate-700">0</span>
          </div>

          <!-- Status Filter -->
          <div class="flex items-center space-x-1 text-xs">
            <button onclick="setFilter('ALL')" class="filter-btn px-2.5 py-1 rounded bg-slate-800 border border-slate-700 text-white" data-status="ALL">All</button>
            <button onclick="setFilter('PENDING_REVIEW')" class="filter-btn px-2.5 py-1 rounded bg-slate-900 text-slate-400 hover:text-white" data-status="PENDING_REVIEW">Review</button>
            <button onclick="setFilter('PUBLISHED')" class="filter-btn px-2.5 py-1 rounded bg-slate-900 text-slate-400 hover:text-white" data-status="PUBLISHED">Published</button>
            <button onclick="setFilter('SKIPPED')" class="filter-btn px-2.5 py-1 rounded bg-slate-900 text-slate-400 hover:text-white" data-status="SKIPPED">Skipped</button>
          </div>
        </div>

        <!-- Deals Container -->
        <div id="deals-container" class="space-y-3">
          <div class="text-center py-12 text-slate-500">Loading deals...</div>
        </div>
      </div>

      <!-- Right Column: Live Testing & Channel Status (1 Col) -->
      <div class="space-y-6">

        <!-- Live Parser Box -->
        <div class="bg-slate-800 border border-slate-700 rounded-xl p-4 space-y-3">
          <div class="flex items-center justify-between">
            <h3 class="font-bold text-sm flex items-center space-x-2">
              <i class="fa-solid fa-flask-vial text-rose-400"></i>
              <span>Live Post & Link Tester</span>
            </h3>
            <span class="text-[10px] text-slate-400">Instant Preview</span>
          </div>
          <p class="text-xs text-slate-400">Paste any Telegram post text or AliExpress URL to test real-time extraction & Arabic caption preview:</p>

          <textarea id="test-input" rows="4" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-xs text-slate-200 focus:outline-none focus:border-rose-500" placeholder="🔥 Wireless Mouse PAW3395\nPrice: $29.99\nCoupon: GAMER5\nhttps://a.aliexpress.com/xxxxx"></textarea>

          <button onclick="testParser()" class="w-full bg-slate-700 hover:bg-slate-600 text-xs py-2 rounded-lg font-medium transition flex items-center justify-center space-x-2">
            <i class="fa-solid fa-magnifying-glass"></i>
            <span>Test Extraction & Generate Caption</span>
          </button>

          <!-- Result Preview Box -->
          <div id="test-result-box" class="hidden mt-3 p-3 bg-slate-900 rounded-lg border border-slate-700/80 text-xs space-y-2">
            <div class="flex items-center justify-between text-[11px] text-slate-400 border-b border-slate-800 pb-1">
              <span>Extracted Fields:</span>
              <span id="test-res-score" class="text-rose-400 font-bold"></span>
            </div>
            <div id="test-fields" class="grid grid-cols-2 gap-1 text-[11px] text-slate-300"></div>

            <div class="pt-2 border-t border-slate-800">
              <span class="text-[11px] text-slate-400 block mb-1">Generated Arabic Caption:</span>
              <pre id="test-preview-caption" class="arabic-text bg-slate-950 p-2.5 rounded text-emerald-400 whitespace-pre-wrap text-xs leading-relaxed"></pre>
            </div>
          </div>
        </div>

        <!-- 10 Monitored Channels Card -->
        <div class="bg-slate-800 border border-slate-700 rounded-xl p-4 space-y-3">
          <div class="flex items-center justify-between">
            <h3 class="font-bold text-sm flex items-center space-x-2">
              <i class="fa-solid fa-satellite-dish text-blue-400"></i>
              <span>10 Source Channels</span>
            </h3>
            <span class="text-xs text-slate-400">180s cycle</span>
          </div>

          <div id="channels-list" class="divide-y divide-slate-700/60 max-h-72 overflow-y-auto pr-1 text-xs">
            <div class="text-slate-500 py-2 text-center">Loading channels...</div>
          </div>
        </div>

        <!-- System Logs Box -->
        <div class="bg-slate-800 border border-slate-700 rounded-xl p-4 space-y-3">
          <h3 class="font-bold text-sm flex items-center space-x-2">
            <i class="fa-solid fa-terminal text-slate-400"></i>
            <span>System Activity</span>
          </h3>
          <div id="logs-container" class="bg-slate-950 p-2.5 rounded-lg border border-slate-800 text-[11px] font-mono text-slate-400 space-y-1.5 max-h-48 overflow-y-auto">
            <div>Connecting...</div>
          </div>
        </div>

      </div>

    </div>
  </main>

  <script>
    let currentFilter = 'ALL';
    let currentMode = 'approval';

    async function fetchStats() {
      try {
        const res = await fetch('/api/stats');
        const data = await res.json();
        document.getElementById('stat-detected').innerText = data.today.detected;
        document.getElementById('stat-published').innerText = data.today.published;
        document.getElementById('stat-review').innerText = data.today.pending_review;
        document.getElementById('stat-skipped').innerText = data.today.skipped_or_rejected;
        document.getElementById('stat-clicks').innerText = data.today.clicks;
        updateModeUI(data.system.publish_mode);
      } catch (e) {
        console.error('Stats error:', e);
      }
    }

    function updateModeUI(mode) {
      currentMode = mode.toLowerCase();
      ['auto', 'approval', 'dry_run'].forEach(m => {
        const btn = document.getElementById('mode-' + m);
        if (btn) {
          if (m === currentMode) {
            btn.className = 'px-3 py-1 rounded font-medium bg-rose-600 text-white shadow';
          } else {
            btn.className = 'px-3 py-1 rounded font-medium text-slate-400 hover:text-white';
          }
        }
      });
    }

    async function setPublishMode(mode) {
      try {
        const res = await fetch('/api/settings/mode', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ mode })
        });
        const data = await res.json();
        updateModeUI(data.publish_mode);
      } catch (e) {
        alert('Failed to update mode: ' + e);
      }
    }

    async function triggerScan() {
      try {
        const res = await fetch('/api/channels/scan-now', { method: 'POST' });
        const data = await res.json();
        alert(data.message);
        setTimeout(fetchDeals, 2000);
      } catch (e) {
        alert('Error triggering scan: ' + e);
      }
    }

    async function fetchDeals() {
      try {
        const url = currentFilter === 'ALL' ? '/api/deals' : `/api/deals?status=${currentFilter}`;
        const res = await fetch(url);
        const deals = await res.json();

        document.getElementById('deals-count-badge').innerText = deals.length;
        const container = document.getElementById('deals-container');

        if (deals.length === 0) {
          container.innerHTML = `<div class="bg-slate-800 border border-slate-700 rounded-xl p-8 text-center text-slate-400 text-sm">
            No deals found under filter <span class="text-rose-400 font-semibold">${currentFilter}</span>.
          </div>`;
          return;
        }

        container.innerHTML = deals.map(d => {
          let badgeColor = 'bg-slate-700 text-slate-300';
          if (d.status === 'PUBLISHED') badgeColor = 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30';
          else if (d.status === 'PENDING_REVIEW') badgeColor = 'bg-amber-500/20 text-amber-400 border border-amber-500/30';
          else if (d.status === 'SKIPPED') badgeColor = 'bg-slate-800 text-slate-400 border border-slate-700';
          else if (d.status === 'REJECTED' || d.status === 'FAILED') badgeColor = 'bg-rose-500/20 text-rose-400 border border-rose-500/30';

          const priceStr = d.current_price ? `$${d.current_price.toFixed(2)} (${(d.current_price_eur || (d.current_price * 0.92)).toFixed(2)}€)` : 'Price N/A';

          return `
            <div class="bg-slate-800 border border-slate-700/80 rounded-xl p-4 hover:border-slate-600 transition space-y-3">
              <div class="flex items-start justify-between gap-3">
                <div class="flex items-start space-x-3">
                  <div class="w-12 h-12 rounded-lg bg-slate-900 border border-slate-700 flex-shrink-0 overflow-hidden flex items-center justify-center">
                    ${d.image_url ? `<img src="${d.image_url}" class="w-full h-full object-cover">` : '<i class="fa-solid fa-tag text-slate-600"></i>'}
                  </div>
                  <div>
                    <h4 class="font-bold text-sm text-slate-100 line-clamp-1">${d.title || 'AliExpress Deal'}</h4>
                    <div class="flex items-center space-x-3 text-xs mt-1">
                      <span class="text-amber-400 font-semibold">${priceStr}</span>
                      ${d.coupon_code ? `<span class="bg-rose-950/80 text-rose-300 px-1.5 py-0.5 rounded border border-rose-800 text-[10px]">Coupon: ${d.coupon_code}</span>` : ''}
                      ${d.has_points_discount ? `<span class="bg-amber-950/80 text-amber-300 px-1.5 py-0.5 rounded border border-amber-800 text-[10px]">Points Discount</span>` : ''}
                      <span class="text-slate-400 text-[10px]">Score: <b class="text-slate-200">${d.quality_score}</b>/100</span>
                    </div>
                  </div>
                </div>

                <div class="flex flex-col items-end space-y-1">
                  <span class="text-[11px] px-2 py-0.5 rounded-full font-medium ${badgeColor}">${d.status}</span>
                  <span class="text-[10px] text-slate-500">#${d.id}</span>
                </div>
              </div>

              ${d.rejection_reason ? `<div class="text-[11px] text-rose-400 bg-rose-950/30 p-2 rounded border border-rose-900/40">Reason: ${d.rejection_reason}</div>` : ''}

              ${d.caption ? `
                <div class="bg-slate-900/90 rounded-lg p-2.5 border border-slate-800">
                  <pre class="arabic-text text-slate-200 text-xs whitespace-pre-wrap leading-relaxed">${d.caption}</pre>
                </div>
              ` : ''}

              <div class="flex items-center justify-between pt-2 border-t border-slate-700/60 text-xs">
                <div class="flex items-center space-x-2">
                  ${d.original_url ? `<a href="${d.original_url}" target="_blank" class="text-slate-400 hover:text-slate-200 text-[11px] flex items-center space-x-1"><i class="fa-solid fa-arrow-up-right-from-square"></i><span>Original</span></a>` : ''}
                  ${d.affiliate_url ? `<a href="${d.affiliate_url}" target="_blank" class="text-amber-400 hover:text-amber-300 text-[11px] flex items-center space-x-1"><i class="fa-solid fa-link"></i><span>Affiliate Link</span></a>` : ''}
                </div>

                <div class="flex items-center space-x-2">
                  ${d.status === 'PENDING_REVIEW' || d.status === 'REJECTED' || d.status === 'FAILED' ? `
                    <button onclick="approveDeal(${d.id})" class="bg-emerald-600 hover:bg-emerald-500 text-white px-3 py-1 rounded text-xs font-medium transition flex items-center space-x-1">
                      <i class="fa-solid fa-check"></i>
                      <span>Approve & Publish</span>
                    </button>
                  ` : ''}

                  ${d.status === 'PENDING_REVIEW' ? `
                    <button onclick="rejectDeal(${d.id})" class="bg-slate-700 hover:bg-rose-900 text-slate-300 hover:text-rose-200 px-2.5 py-1 rounded text-xs transition">
                      <i class="fa-solid fa-xmark"></i>
                    </button>
                  ` : ''}

                  ${d.status === 'FAILED' ? `
                    <button onclick="retryDeal(${d.id})" class="bg-slate-700 hover:bg-slate-600 text-slate-200 px-2.5 py-1 rounded text-xs transition">
                      <i class="fa-solid fa-rotate-right"></i> Retry
                    </button>
                  ` : ''}
                </div>
              </div>
            </div>
          `;
        }).join('');
      } catch (e) {
        console.error('Error fetching deals:', e);
      }
    }

    async function setFilter(status) {
      currentFilter = status;
      document.querySelectorAll('.filter-btn').forEach(btn => {
        if (btn.dataset.status === status) {
          btn.className = 'filter-btn px-2.5 py-1 rounded bg-slate-800 border border-slate-700 text-white';
        } else {
          btn.className = 'filter-btn px-2.5 py-1 rounded bg-slate-900 text-slate-400 hover:text-white';
        }
      });
      fetchDeals();
    }

    async function approveDeal(id) {
      if (!confirm(`Approve and publish Deal #${id} to your Telegram channel now?`)) return;
      try {
        const res = await fetch(`/api/deals/${id}/approve`, { method: 'POST' });
        const data = await res.json();
        if (res.ok) {
          fetchDeals();
          fetchStats();
        } else {
          alert('Error: ' + data.detail);
        }
      } catch (e) {
        alert('Request failed: ' + e);
      }
    }

    async function rejectDeal(id) {
      try {
        await fetch(`/api/deals/${id}/reject`, { method: 'POST' });
        fetchDeals();
        fetchStats();
      } catch (e) {
        alert('Error: ' + e);
      }
    }

    async function retryDeal(id) {
      try {
        await fetch(`/api/deals/${id}/retry`, { method: 'POST' });
        fetchDeals();
        fetchStats();
      } catch (e) {
        alert('Error: ' + e);
      }
    }

    async function testParser() {
      const text = document.getElementById('test-input').value.trim();
      if (!text) {
        alert('Please enter or paste a Telegram message or AliExpress URL to test.');
        return;
      }
      try {
        const res = await fetch('/api/test-parse', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text })
        });
        const data = await res.json();
        const box = document.getElementById('test-result-box');
        if (!data.success) {
          alert('Extractor: ' + data.error);
          return;
        }

        box.classList.remove('hidden');
        document.getElementById('test-fields').innerHTML = `
          <div>Product ID: <b class="text-white">${data.product_id || 'N/A'}</b></div>
          <div>Price USD: <b class="text-white">${data.current_price ? '$' + data.current_price : 'N/A'}</b></div>
          <div>Price EUR: <b class="text-white">${data.current_price_eur ? data.current_price_eur + '€' : 'N/A'}</b></div>
          <div>Coupon: <b class="text-white">${data.coupon_code || 'None'}</b></div>
          <div>Points Discount: <b class="text-white">${data.has_points_discount ? 'Yes' : 'No'}</b></div>
        `;
        document.getElementById('test-preview-caption').innerText = data.preview_caption;
      } catch (e) {
        alert('Test failed: ' + e);
      }
    }

    async function fetchChannels() {
      try {
        const res = await fetch('/api/channels');
        const channels = await res.json();
        const list = document.getElementById('channels-list');
        list.innerHTML = channels.map(c => `
          <div class="py-2 flex items-center justify-between">
            <div class="flex items-center space-x-2">
              <span class="w-2 h-2 rounded-full ${c.enabled ? 'bg-emerald-500' : 'bg-slate-600'}"></span>
              <div>
                <div class="font-medium text-slate-200">@${c.username}</div>
                <div class="text-[10px] text-slate-500">${c.display_name || 'Channel'} • Cursor ID: ${c.last_message_id || 0}</div>
              </div>
            </div>
            <span class="text-[10px] text-slate-400">${c.last_checked_at ? new Date(c.last_checked_at).toLocaleTimeString() : 'Pending'}</span>
          </div>
        `).join('');
      } catch (e) {
        console.error('Channels fetch error:', e);
      }
    }

    async function fetchLogs() {
      try {
        const res = await fetch('/api/logs?limit=15');
        const logs = await res.json();
        const container = document.getElementById('logs-container');
        container.innerHTML = logs.map(l => {
          let col = 'text-slate-400';
          if (l.level === 'ERROR') col = 'text-rose-400';
          else if (l.level === 'WARNING') col = 'text-amber-400';
          return `<div><span class="text-slate-600">${l.created_at ? l.created_at.slice(11, 19) : ''}</span> [${l.component}] <span class="${col}">${l.message}</span></div>`;
        }).join('');
      } catch (e) {
        console.error('Logs fetch error:', e);
      }
    }

    // Polling intervals
    fetchStats();
    fetchDeals();
    fetchChannels();
    fetchLogs();
    setInterval(fetchStats, 10000);
    setInterval(fetchDeals, 15000);
    setInterval(fetchLogs, 10000);
  </script>
</body>
</html>
"""

@dashboard_router.get("/", response_class=HTMLResponse)
@dashboard_router.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard():
    return HTMLResponse(content=DASHBOARD_HTML)

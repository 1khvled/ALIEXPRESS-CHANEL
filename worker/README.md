# @Alilo07BOT — Cloudflare Worker

The Vercel FastAPI deployment that used to host the bot webhook now answers
`402 Payment Required`, so the bot stopped replying. This Worker is a
dependency-free port of the link flow in `api/coin_bot.py`.

## What it does

Send it any AliExpress link (browser URL, `a.aliexpress.com` short link,
`s.click` affiliate link, or a raw 10–18 digit product id) and it answers with
five affiliate-tagged links:

| Link | Purpose |
| --- | --- |
| Direct | plain product page |
| Coins | `coin-index` page — the big discount |
| Bundle | `BundleDeals2` page |
| SuperDeals | `?sourceType=561&channel=superdeal` |
| Limited | `?sourceType=562&channel=limited` |

Plus `/start`, `/help`, `/calc`, `/rate`, `/coupons`, `/myid`, `/fr`, `/ar`,
inline callbacks, 20 links/hour per user, and an admin-only `/post` that
publishes to `@DzAliexpress0`.

Title and image come from the product page's Open Graph tags (best effort);
price comes from the AliExpress app share text, exactly like the old fallback.

## Deploy

```powershell
cd worker
npx wrangler deploy
```

Then set the secrets and point Telegram at the Worker:

```powershell
"<token>"    | npx wrangler secret put TELEGRAM_BOT_TOKEN
"<secret>"   | npx wrangler secret put TELEGRAM_WEBHOOK_SECRET
"<admin_id>" | npx wrangler secret put ADMIN_USER_ID
```

```
https://api.telegram.org/bot<token>/setWebhook?url=https://alilo07bot.<subdomain>.workers.dev/telegram&secret_token=<secret>&drop_pending_updates=false
```

Check it with `getWebhookInfo` and `GET /health`.

## Free-tier budget

Built to sit far below the Workers free plan (100k requests/day, 10 ms CPU
per invocation):

| Cost | When | Mitigation |
| --- | --- | --- |
| Worker request | every message | one webhook call per Telegram update |
| CPU | every message | warm path is regex only (~0.5 ms) |
| AliExpress fetch | cache miss only | L1 isolate map → L2 edge cache, 7 days |
| USDT fetch | only when a USD price needs DZD | 30 min cache, skipped for French replies |
| Short-link hops | cache miss only | `s.click`/`a.aliexpress` code → product id, 7 days |
| Telegram calls | every reply | typing + message fired in parallel |

Only the first 80KB of a product page is read and only its `<head>` is
scanned. A captcha/blocked page is remembered as "empty" for 30 minutes, not
a week, so a block cannot poison the cache.

## Routes

- `POST /telegram` — Telegram webhook (also accepts `POST /`)
- `GET /health` — JSON status

No cron, no polling, no KV, no D1: one request per Telegram update.

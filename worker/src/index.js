/**
 * @Alilo07BOT — Cloudflare Worker webhook
 * ------------------------------------------------------------------
 * Drop-in replacement for the Vercel FastAPI webhook that died with
 * HTTP 402. Ports the link flow from api/coin_bot.py:
 *
 *   AliExpress link / short link / raw product id
 *     -> product id
 *     -> direct + coin + bundle + superdeals + limited links
 *     -> affiliate tagged (aff_fcid) and replied with inline buttons
 *
 * Zero npm dependencies, zero cron, zero polling: one webhook route.
 * Free tier: 100k requests/day, and a webhook bot uses a few hundred.
 */

const CH_DZ = "https://t.me/DzAliexpress0";
const CH_FR = "https://t.me/francedealsdz";
const BOT_URL = "https://t.me/Alilo07BOT";
const SITE_URL = "https://t.me/DzAliexpress0";

const UA =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " +
  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36";

const MAX_LINKS_PER_HOUR = 20;
const HOUR_MS = 3600 * 1000;
const WORK_BUDGET_MS = 25000;

/* ------------------------------------------------------------------ */
/* In-memory state (per isolate — best effort, same as the old server) */
/* ------------------------------------------------------------------ */

const userLang = new Map(); // userId -> "ar" | "fr"
const linkHits = new Map(); // userId -> [timestamps]
const usdtCache = { rate: 249.0, at: 0 };

const nf = new Intl.NumberFormat("en-US");

/* ------------------------------------------------------------------ */
/* Copy                                                                */
/* ------------------------------------------------------------------ */

const WELCOME_AR = `👋 <b>مرحباً بك في بوت DealScoutDz لزيادة تخفيض العملات!</b> 🪙

هذا البوت يعمل على <b>زيادة نسبة التخفيض بالعملات (النقاط)</b> من 1%~5% إلى نسبة عالية تصل حتى <b>70%</b> في معظم منتجات AliExpress 🤑

📌 <b>طريقة الاستخدام بكل بساطة:</b>
1️⃣ انسخ رابط أي منتج تريده من تطبيق أو موقع AliExpress.
2️⃣ أرسل الرابط هنا في المحادثة.
3️⃣ سيرسل لك البوت فوراً روابط التخفيض الأكبر (تخفيض العملات، Bundle Deals، السوبر ديلز، والرابط المباشر) مع السعر المباشر بالدينار الجزائري! 🚀

💡 <i>أرسل أي رابط منتج من AliExpress الآن لتجربة التخفيض!</i>`;

const WELCOME_FR = `👋 <b>Bienvenue sur DealScout Bot - Maximiseur de Réduction Pièces (Coins) AliExpress !</b> 🪙

Ce bot vous permet d'<b>augmenter la réduction par pièces (Coins)</b> de 1%~5% jusqu'à <b>70%</b> sur la plupart des produits AliExpress 🤑

📌 <b>Comment l'utiliser facilement :</b>
1️⃣ Copiez le lien de n'importe quel produit depuis l'application ou le site AliExpress.
2️⃣ Envoyez le lien ici dans cette conversation.
3️⃣ Le bot génère instantanément vos liens de réduction maximale (Pièces Coins, Bundle Deals, SuperDeals, et Lien Direct) avec le prix estimé en Euros ! 🚀

💡 <i>Envoyez un lien AliExpress dès maintenant pour tester la réduction !</i>`;

const HELP_AR = `💡 <b>دليل استخدام تخفيض العملات بأقصى نسبة:</b>

1️⃣ <b>كيف تفعل الخصم الأكبر؟</b>
عند فتح رابط العملات، لا تشترِ من الصفحة العادية! اضغط على زر <b>"شراء الآن"</b> مباشرة من صفحة العملات، أو أضف المنتج إلى السلة من داخل صفحة العملات لتخصم لك كل النقاط المتاحة.

2️⃣ <b>تحويل الدولة إلى كوريا 🇰🇷:</b>
لا تنسى تحويل دولة التطبيق إلى كوريا 🇰🇷 📍 من إعدادات AliExpress للحصول على أسعار أقل وتخفيض عملات إضافي على الكثير من الأجهزة والعتاد!

3️⃣ <b>كيف تجمع العملات يومياً؟</b>
ادخل يومياً لتطبيق AliExpress واضغط على أيقونة <b>Coins / العملات</b> واجمع العملات المجانية اليومية (يمكنك جمع 70 إلى 150 عملة يومياً مجاناً).

4️⃣ <b>أسعار الصرف في الجزائر:</b>
تابع أسعار صرف السكوار والـ USDT لحظة بلحظة عبر: <a href="https://squarealgerie.com">SquareAlgerie.com</a> 🇩🇿

📢 للمزيد من العروض اليومية، انضم لقنواتنا:
🇩🇿 صفقات الجزائر: @DzAliexpress0
🇫🇷 صفقات فرنسا وأوروبا: @francedealsdz`;

const HELP_FR = `💡 <b>Guide pour maximiser votre réduction par pièces (Coins) :</b>

1️⃣ <b>Comment activer la réduction maximale ?</b>
En ouvrant le lien Coins, n'achetez pas depuis la page classique ! Cliquez directement sur le bouton <b>"Acheter maintenant"</b> depuis la page des pièces, ou ajoutez le produit au panier depuis cette page pour déduire tous vos points disponibles.

2️⃣ <b>Changer le pays vers la Corée 🇰🇷 (Astuce Tech) :</b>
Changer le pays de livraison vers la Corée 🇰🇷 📍 dans les paramètres AliExpress permet souvent d'obtenir des prix de base plus bas et un pourcentage de pièces supérieur sur le matériel tech et gaming !

3️⃣ <b>Comment collecter des pièces chaque jour ?</b>
Ouvrez chaque jour l'application AliExpress, accédez à la section <b>Coins / Pièces</b> et récupérez vos pièces quotidiennes gratuites (70 à 150 pièces par jour).

📢 Pour ne rater aucun bon plan au quotidien, rejoignez nos canaux :
🇩🇿 Bons plans Algérie : @DzAliexpress0
🇫🇷 Bons plans France : @francedealsdz`;

const COUPONS_AR = `🎟️ <b>كودات وكوبونات AliExpress</b>
━━━━━━━━━━━━━━━━━
💡 تابع قنواتنا الرسمية لمعرفة أحدث الكودات اليومية فور توفرها:
🇩🇿 صفقات الجزائر: @DzAliexpress0
🇫🇷 صفقات فرنسا وأوروبا: @francedealsdz

🪙 <i>تذكير: تخفيض العملات (Coins) يعمل دائماً ويوفر حتى 70% بدون أي كود — فقط أرسل رابط المنتج هنا.</i>`;

/* ------------------------------------------------------------------ */
/* Small helpers                                                       */
/* ------------------------------------------------------------------ */

const esc = (s) =>
  String(s == null ? "" : s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

const json = (obj, status = 200) =>
  new Response(JSON.stringify(obj), {
    status,
    headers: { "content-type": "application/json; charset=utf-8" },
  });

const remaining = (deadline) => Math.max(800, deadline - Date.now());

function isAdmin(userId, env) {
  if (!userId) return false;
  const id = String(userId);
  if (env.ADMIN_USER_ID && String(env.ADMIN_USER_ID) === id) return true;
  if (env.ADMIN_USER_IDS) {
    return String(env.ADMIN_USER_IDS)
      .split(",")
      .map((x) => x.trim())
      .filter(Boolean)
      .includes(id);
  }
  return false;
}

function getLang(userId) {
  return userLang.get(userId) || "ar";
}

function checkRateLimit(userId, env) {
  if (isAdmin(userId, env)) return { limited: false, waitMs: 0 };
  const now = Date.now();
  const cutoff = now - HOUR_MS;
  const hits = (linkHits.get(userId) || []).filter((t) => t > cutoff);
  if (hits.length >= MAX_LINKS_PER_HOUR) {
    linkHits.set(userId, hits);
    return { limited: true, waitMs: Math.max(1000, HOUR_MS - (now - hits[0])) };
  }
  hits.push(now);
  linkHits.set(userId, hits);
  return { limited: false, waitMs: 0 };
}

/* ------------------------------------------------------------------ */
/* Telegram API                                                        */
/* ------------------------------------------------------------------ */

async function tg(env, method, payload, deadline) {
  if (!env.TELEGRAM_BOT_TOKEN) {
    return { ok: false, error: "TELEGRAM_BOT_TOKEN missing" };
  }
  try {
    const res = await fetch(`https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/${method}`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(Math.max(1500, Math.min(8000, remaining(deadline)))),
    });
    let data = null;
    try {
      data = await res.json();
    } catch (_) {}
    return {
      ok: res.ok && data && data.ok === true,
      status: res.status,
      error: data && data.description ? data.description : res.ok ? null : `HTTP ${res.status}`,
      result: data && data.result,
    };
  } catch (e) {
    return { ok: false, error: String(e && e.message ? e.message : e) };
  }
}

const sendMsg = (env, chatId, text, markup, deadline, replyTo) =>
  tg(
    env,
    "sendMessage",
    {
      chat_id: chatId,
      text,
      parse_mode: "HTML",
      ...(markup ? { reply_markup: markup } : {}),
      ...(replyTo ? { reply_to_message_id: replyTo } : {}),
    },
    deadline
  );

const sendPhoto = (env, chatId, photo, caption, markup, deadline, replyTo) =>
  tg(
    env,
    "sendPhoto",
    {
      chat_id: chatId,
      photo,
      caption: String(caption).slice(0, 1024),
      parse_mode: "HTML",
      ...(markup ? { reply_markup: markup } : {}),
      ...(replyTo ? { reply_to_message_id: replyTo } : {}),
    },
    deadline
  );

/* ------------------------------------------------------------------ */
/* Link parsing                                                        */
/* ------------------------------------------------------------------ */

const URL_RE = /(https?:\/\/[^\s<>"',;]+)/gi;

function extractUrls(text) {
  if (!text) return [];
  const out = [];
  for (const m of String(text).matchAll(URL_RE)) {
    out.push(m[1].replace(/[.,;!?:)\]}"'>]+$/, ""));
  }
  return out;
}

function extractPid(text) {
  if (!text) return null;
  const clean = String(text).trim();
  if (/^\d{10,18}$/.test(clean)) return clean;

  let m = clean.match(/\/item\/(\d{10,18})/i);
  if (m) return m[1];
  m = clean.match(/productIds?=(\d{10,18})/i);
  if (m) return m[1];
  m = clean.match(/(?:itemId|item_id|productId|product_id)[=:](\d{10,18})/i);
  if (m) return m[1];
  m = clean.match(/(?:^|[?&#;])id=(\d{10,18})(?:$|[&#;])/i);
  if (m) return m[1];
  return null;
}

/** Pull a title + price out of an AliExpress app share message. */
function extractTitleAndPrice(text) {
  if (!text) return { title: null, price: null };
  let cleaned = String(text).replace(/https?:\/\/\S+/gi, " ");
  let price = null;

  const mp = cleaned.match(/(?:US\s*)?\$?\s*([0-9]+[.,][0-9]{1,2})\s*\$?/i);
  if (mp) {
    const v = parseFloat(mp[1].replace(",", "."));
    if (Number.isFinite(v) && v > 0) price = v;
  }

  cleaned = cleaned
    .replace(/(?:US\s*)?\$?\s*[0-9]+[.,][0-9]{1,2}\s*\$?/gi, " ")
    .replace(
      /Just found this amazing item on AliExpress\.?|Check it out!?|لقيت هذا المنتج|شوف هذا العرض|علي اكسبرس|AliExpress/gi,
      " "
    )
    .replace(/[|؛:,\-_~]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();

  return { title: cleaned.length >= 8 ? cleaned.slice(0, 90) : null, price };
}

/**
 * Resolve any AliExpress input to a product id.
 * Follows s.click / a.aliexpress / star short links by hand so the
 * final landing page never has to be rendered.
 */
async function resolveProductId(text, deadline) {
  const direct = extractPid(text);
  if (direct) return direct;

  const candidates = [];
  const sc = String(text).match(/s\.click\.aliexpress\.com\/e\/(_[A-Za-z0-9]+)/);
  if (sc) candidates.push(`https://s.click.aliexpress.com/e/${sc[1]}`);
  const a = String(text).match(/a\.aliexpress\.com\/(_[A-Za-z0-9]+)/);
  if (a) candidates.push(`https://a.aliexpress.com/${a[1]}`);
  for (const u of extractUrls(text)) {
    if (!candidates.includes(u)) candidates.push(u);
  }

  for (const start of candidates.slice(0, 3)) {
    let current = start;
    for (let hop = 0; hop < 6; hop++) {
      if (Date.now() > deadline) return null;
      const pid = extractPid(current);
      if (pid) return pid;

      let res;
      try {
        res = await fetch(current, {
          redirect: "manual",
          headers: {
            "user-agent": UA,
            accept: "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9,ar;q=0.8",
          },
          signal: AbortSignal.timeout(Math.min(6000, remaining(deadline))),
        });
      } catch (_) {
        break;
      }

      const loc = res.headers.get("location");
      if (loc) {
        try {
          current = new URL(loc, current).toString();
        } catch (_) {
          break;
        }
        continue;
      }

      // Landing page: scan the body for a product id / item URL.
      try {
        const body = (await res.text()).slice(0, 80000);
        const found = extractPid(body);
        if (found) return found;
        const m = body.match(/\/item\/(\d{10,18})/);
        if (m) return m[1];
      } catch (_) {}
      break;
    }
  }

  return null;
}

/* ------------------------------------------------------------------ */
/* Product metadata (best effort)                                      */
/* ------------------------------------------------------------------ */

function decodeEntities(s) {
  return String(s)
    .replace(/&amp;/g, "&")
    .replace(/&quot;/g, '"')
    .replace(/&#0?39;/g, "'")
    .replace(/&apos;/g, "'")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&#x([0-9a-f]+);/gi, (_, h) => String.fromCodePoint(parseInt(h, 16)))
    .replace(/&#(\d+);/g, (_, d) => String.fromCodePoint(parseInt(d, 10)));
}

function metaContent(html, prop) {
  const p = prop.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  let m = html.match(new RegExp(`<meta[^>]+(?:property|name)=["']${p}["'][^>]*>`, "i"));
  let tag = m && m[0];
  if (!tag) {
    m = html.match(new RegExp(`<meta[^>]+content=["'][^"']*["'][^>]*(?:property|name)=["']${p}["'][^>]*>`, "i"));
    tag = m && m[0];
  }
  if (!tag) return null;
  const c = tag.match(/content=["']([^"']*)["']/i);
  return c ? decodeEntities(c[1]) : null;
}

async function fetchProductMeta(pid, deadline) {
  const out = {};
  try {
    const res = await fetch(`https://www.aliexpress.com/item/${pid}.html`, {
      redirect: "follow",
      headers: { "user-agent": UA, "accept-language": "en-US,en;q=0.9" },
      signal: AbortSignal.timeout(Math.min(6000, remaining(deadline))),
    });
    if (!res.ok) return out;
    const html = await res.text();
    const title = metaContent(html, "og:title") || metaContent(html, "twitter:title");
    if (title) {
      const clean = title.replace(/\s*[-|]\s*AliExpress\s*\d*\s*$/i, "").trim();
      if (clean.length >= 5) out.title = clean.slice(0, 120);
    }
    const image = metaContent(html, "og:image") || metaContent(html, "twitter:image");
    if (image && /alicdn\.com|aliexpress-media\.com/.test(image)) out.image = image;
  } catch (_) {}
  return out;
}

/* ------------------------------------------------------------------ */
/* USDT rate                                                           */
/* ------------------------------------------------------------------ */

async function getUsdtRate() {
  const now = Date.now();
  if (usdtCache.at && now - usdtCache.at < 30 * 60 * 1000) return usdtCache.rate;
  try {
    const res = await fetch("https://squarealgerie.com/api/rates", {
      signal: AbortSignal.timeout(3000),
    });
    if (res.ok) {
      const data = await res.json();
      const usdt = (data && data.currencies ? data.currencies : []).find((c) => c && c.code === "USDT");
      const rate = Number(usdt && usdt.buy);
      if (Number.isFinite(rate) && rate >= 220 && rate <= 280) {
        usdtCache.rate = rate;
        usdtCache.at = now;
        return rate;
      }
    }
  } catch (_) {}
  usdtCache.at = now;
  return usdtCache.rate;
}

/* ------------------------------------------------------------------ */
/* Deal generation                                                     */
/* ------------------------------------------------------------------ */

function withAff(url, trackingId) {
  if (!url) return url;
  if (!trackingId || url.includes("aff_fcid=")) return url;
  return url + (url.includes("?") ? "&" : "?") + "aff_fcid=" + encodeURIComponent(trackingId);
}

function buildLinks(pid, trackingId) {
  const direct = `https://www.aliexpress.com/item/${pid}.html`;
  const coin = `https://m.aliexpress.com/p/coin-index/index.html?_immersiveMode=true&tabname=configTab_1926001&productIds=${pid}`;
  const bundle = `https://www.aliexpress.com/ssr/300000512/BundleDeals2?disableNav=YES&pha_manifest=ssr&_immersiveMode=true&productIds=${pid}`;
  const superdeal = `https://www.aliexpress.com/item/${pid}.html?sourceType=561&channel=superdeal`;
  const limited = `https://www.aliexpress.com/item/${pid}.html?sourceType=562&channel=limited`;
  return {
    direct: withAff(direct, trackingId),
    coin: withAff(coin, trackingId),
    bundle: withAff(bundle, trackingId),
    super: withAff(superdeal, trackingId),
    limited: withAff(limited, trackingId),
  };
}

async function generateDeal(pid, rawText, lang, env, deadline) {
  const trackingId = env.AFF_TRACKING_ID || "";
  const links = buildLinks(pid, trackingId);
  const fromText = extractTitleAndPrice(rawText);

  const [meta, rate] = await Promise.all([fetchProductMeta(pid, deadline), getUsdtRate()]);

  const title =
    meta.title ||
    fromText.title ||
    (lang === "fr" ? "Produit AliExpress" : "منتج مميز من AliExpress");

  const price = fromText.price;
  const safeTitle = esc(title);

  let text;
  let markup;

  if (lang === "fr") {
    const eur = price ? Math.round(price * 0.92 * 100) / 100 : null;
    const priceLine = eur
      ? `💶 Prix estimé : <b>${eur.toFixed(2)}€</b> (~<b>${price.toFixed(2)}$</b>)\n`
      : "";

    text = `🛍️ <b>${safeTitle}</b>
${priceLine}
🛒 <b>Lien direct du produit :</b>
🔗 ${links.direct}

🪙 <b>Prix avec réduction Pièces (Coins) :</b>
🔗 ${links.coin}

📦 <b>Offres groupées (Bundle Deals) :</b>
🔗 ${links.bundle}

⚡ <b>Ventes Flash (SuperDeals) :</b>
🔗 ${links.super}

⏳ <b>Offre limitée (Limited Offer) :</b>
🔗 ${links.limited}

💡 <i>Conseil : Ouvrez le lien Pièces et achetez directement pour déduire le maximum de pièces !</i>`;

    markup = {
      inline_keyboard: [
        [
          { text: "🛒 Lien Direct", url: links.direct },
          { text: "🪙 Réduction Pièces (Coins)", url: links.coin },
        ],
        [
          { text: "📦 Offres Bundle Deals", url: links.bundle },
          { text: "⚡ Ventes SuperDeals", url: links.super },
        ],
        [{ text: "⏳ Offre Limitée", url: links.limited }],
        [
          { text: "🇫🇷 Canal Bons Plans France 🇪🇺", url: CH_FR },
          { text: "🇩🇿 Canal Bons Plans Algérie 🇩🇿", url: CH_DZ },
        ],
        [
          {
            text: "🔄 Partager le bot",
            url: "https://t.me/share/url?url=https://t.me/Alilo07BOT&text=Bot de réduction AliExpress Coins 🪙 Économisez jusqu'à 70% !",
          },
        ],
        [{ text: "🌐 Passer en Arabe 🇩🇿", callback_data: "set_lang_ar" }],
      ],
    };
  } else {
    const priceLine = price
      ? `💵 السعر التقريبي: <b>${price.toFixed(2)}$</b> (~<b>${nf.format(
          Math.round(price * rate)
        )} دج</b>)\n`
      : "";

    text = `🛍️ <b>${safeTitle}</b>
${priceLine}
🛒 <b>الرابط المباشر للمنتج:</b>
🔗 ${links.direct}

🪙 <b>سعر تخفيض العملات (Coins):</b>
🔗 ${links.coin}

📦 <b>عروض الحزم (Bundle Deals):</b>
🔗 ${links.bundle}

⚡ <b>عروض السوبر ديلز (SuperDeals):</b>
🔗 ${links.super}

⏳ <b>العرض المحدود (Limited Offer):</b>
🔗 ${links.limited}

💡 <i>نصيحة: ادخل من رابط العملات واشترِ مباشرة أو أضف المنتج للسلة لتفعيل أكبر نسبة خصم!</i>`;

    markup = {
      inline_keyboard: [
        [
          { text: "🛒 رابط الشراء المباشر", url: links.direct },
          { text: "🪙 شراء بتخفيض العملات", url: links.coin },
        ],
        [
          { text: "📦 عروض Bundle Deals", url: links.bundle },
          { text: "⚡ عروض السوبر ديلز", url: links.super },
        ],
        [{ text: "⏳ العرض المحدود (Limited)", url: links.limited }],
        [
          { text: "📢 قناة صفقات الجزائر 🇩🇿", url: CH_DZ },
          { text: "🇫🇷 قناة صفقات فرنسا 🇪🇺", url: CH_FR },
        ],
        [
          {
            text: "🔄 مشاركة البوت مع أصدقائك",
            url: "https://t.me/share/url?url=https://t.me/Alilo07BOT&text=بوت زيادة تخفيض العملات في علي اكسبرس 🪙🔥 يوفر حتى 70%!",
          },
        ],
        [{ text: "🌐 Passer en Français 🇫🇷", callback_data: "set_lang_fr" }],
      ],
    };
  }

  return {
    text,
    markup,
    title,
    price,
    image: meta.image || null,
    links,
    rate,
  };
}

/* ------------------------------------------------------------------ */
/* Channel publishing (admin only)                                     */
/* ------------------------------------------------------------------ */

async function publishToChannel(pid, rawText, env, deadline) {
  const deal = await generateDeal(pid, rawText, "ar", env, deadline);
  const priceLine = deal.price
    ? `💰 <b>السعر:</b> <b>${deal.price.toFixed(2)}$</b> (~<b>${nf.format(
        Math.round(deal.price * deal.rate)
      )} دج</b>)\n`
    : "";

  const caption = `🔥 <b>${esc(deal.title)}</b>

${priceLine}🪙 <b>خصم العملات (Coins):</b> يصل حتى 70%

👇 <b>اطلب الآن عبر رابط العملات:</b>
${deal.links.coin}

📢 <i>تابع قناتنا لمزيد من الصفقات اليومية:</i> @DzAliexpress0`;

  const markup = {
    inline_keyboard: [
      [{ text: "🪙 فتح بوت تخفيض العملات", url: BOT_URL }],
      [{ text: "📢 قناة الصفقات المعتمدة", url: CH_DZ }],
    ],
  };

  const chatId = env.CHANNEL_ID || "@DzAliexpress0";

  let res;
  if (deal.image) {
    res = await sendPhoto(env, chatId, deal.image, caption, markup, deadline);
    if (!res.ok) {
      res = await sendMsg(env, chatId, caption, markup, deadline);
    }
  } else {
    res = await sendMsg(env, chatId, caption, markup, deadline);
  }

  return {
    ok: res.ok,
    error: res.error,
    messageId: res.result && res.result.message_id,
  };
}

/* ------------------------------------------------------------------ */
/* Keyboards                                                           */
/* ------------------------------------------------------------------ */

const startMarkupAr = () => ({
  inline_keyboard: [
    [{ text: "📖 طريقة استخدام تخفيض العملات", callback_data: "cb_help" }],
    [
      { text: "📢 قناة صفقات الجزائر 🇩🇿", url: CH_DZ },
      { text: "🇫🇷 قناة صفقات فرنسا 🇪🇺", url: CH_FR },
    ],
    [{ text: "🌐 Passer en Français 🇫🇷", callback_data: "set_lang_fr" }],
  ],
});

const startMarkupFr = () => ({
  inline_keyboard: [
    [{ text: "📖 Guide Réduction Pièces (Coins)", callback_data: "cb_help" }],
    [
      { text: "🇫🇷 Canal Bons Plans France 🇪🇺", url: CH_FR },
      { text: "🇩🇿 Canal Bons Plans Algérie 🇩🇿", url: CH_DZ },
    ],
    [{ text: "🌐 Passer en Arabe 🇩🇿", callback_data: "set_lang_ar" }],
  ],
});

/* ------------------------------------------------------------------ */
/* Callback queries                                                    */
/* ------------------------------------------------------------------ */

async function handleCallback(cb, env, deadline) {
  const data = cb.data || "";
  const user = cb.from || {};
  const userId = user.id;
  const msg = cb.message || {};
  const chatId = msg.chat ? msg.chat.id : null;

  await tg(env, "answerCallbackQuery", { callback_query_id: cb.id }, deadline);

  if (!chatId) return { handled: "callback_no_chat" };

  if (data === "set_lang_fr") {
    userLang.set(userId, "fr");
    await sendMsg(env, chatId, "✅ <b>Langue changée en Français !</b>\n\n" + WELCOME_FR, startMarkupFr(), deadline);
    return { handled: "set_lang_fr" };
  }

  if (data === "set_lang_ar") {
    userLang.set(userId, "ar");
    await sendMsg(env, chatId, "✅ <b>تم تغيير اللغة إلى العربية !</b>\n\n" + WELCOME_AR, startMarkupAr(), deadline);
    return { handled: "set_lang_ar" };
  }

  if (data === "cb_help") {
    await sendMsg(env, chatId, getLang(userId) === "fr" ? HELP_FR : HELP_AR, null, deadline);
    return { handled: "cb_help" };
  }

  if (data === "cb_coupons") {
    await sendMsg(env, chatId, COUPONS_AR, null, deadline);
    return { handled: "cb_coupons" };
  }

  if (data.startsWith("admin_pub_")) {
    if (!isAdmin(userId, env)) {
      await sendMsg(env, chatId, "⚠️ عذراً، هذا الإجراء مخصص لمشرف القناة فقط.", null, deadline);
      return { handled: "admin_pub_denied" };
    }
    const pid = data.replace("admin_pub_", "").trim();
    await sendMsg(env, chatId, "⏳ جاري نشر العرض في القناة @DzAliexpress0...", null, deadline);
    const pub = await publishToChannel(pid, "", env, deadline);
    if (pub.ok) {
      await sendMsg(
        env,
        chatId,
        `✅ <b>تم نشر العرض بنجاح في القناة!</b>\n\n🔗 <b>رابط المنشور:</b> <a href="${CH_DZ}/${pub.messageId}">اضغط هنا 👈</a>`,
        null,
        deadline
      );
    } else {
      await sendMsg(env, chatId, `❌ فشل نشر العرض في القناة: ${esc(pub.error || "unknown")}`, null, deadline);
    }
    return { handled: "admin_pub" };
  }

  return { handled: "callback_ignored", data };
}

/* ------------------------------------------------------------------ */
/* Messages                                                            */
/* ------------------------------------------------------------------ */

async function handleMessage(message, env, deadline) {
  const chat = message.chat || {};
  const chatId = chat.id;
  if (!chatId) return { skipped: "no_chat" };

  const chatType = chat.type || "private";
  const isGroup = chatType === "group" || chatType === "supergroup" || chatType === "channel";
  const messageId = message.message_id;
  const from = message.from || {};
  const userId = from.id || chatId;
  const text = (message.text || message.caption || "").trim();
  const lang = getLang(userId);

  /* ---------------- groups ---------------- */
  if (isGroup) {
    if (text.startsWith("/calc") || text.startsWith("/حساب")) {
      const m = text.match(/([0-9]+[.,]?[0-9]*)/);
      if (m) {
        const usd = parseFloat(m[1].replace(",", "."));
        const rate = await getUsdtRate();
        const dzd = Math.round(usd * rate);
        const total = dzd + 130;
        const body =
          `🧮 <b>حاسبة سعر الشراء بالدينار الجزائري 🇩🇿</b>\n\n` +
          `💵 <b>المبلغ:</b> ${usd.toFixed(2)}$ (سعر الصرف: ${rate.toFixed(1)} دج)\n` +
          `▫️ <b>قيمة السلعة:</b> <b>${nf.format(dzd)} دج</b>\n` +
          `▫️ <b>رسوم طرد البريد الجزائري:</b> ~<b>130 دج</b>\n` +
          `💰 <b>التكلفة الإجمالية التقديرية:</b> ~<b>${nf.format(total)} دج</b>`;
        await sendMsg(env, chatId, body, null, deadline, messageId);
        return { handled: "group_calc" };
      }
    }

    if (text.startsWith("/rate") || text.startsWith("/square") || text.startsWith("/سكوار")) {
      const rate = await getUsdtRate();
      const body =
        `📈 <b>سعر صرف الـ USDT الحالي (SquareAlgerie.com):</b>\n\n` +
        `💵 <b>1 USDT</b> ≈ <b>${rate.toFixed(1)} دج</b> 🇩🇿\n\n` +
        `🪙 <i>لحساب أي مبلغ، أرسل: <code>/calc 15.5</code></i>`;
      await sendMsg(env, chatId, body, null, deadline, messageId);
      return { handled: "group_rate" };
    }

    const urls = extractUrls(text);
    const hasAli =
      urls.some((u) => /aliexpress|s\.click/i.test(u)) || Boolean(extractPid(text));
    if (hasAli) {
      const pid = await resolveProductId(text, deadline);
      if (!pid) return { handled: "group_no_pid" };

      const deal = await generateDeal(pid, text, lang, env, deadline);
      const priceInfo = deal.price
        ? `💰 <b>السعر التقريبي:</b> $${deal.price.toFixed(2)} (~<b>${nf.format(
            Math.round(deal.price * deal.rate)
          )} دج</b>)\n`
        : "";

      const body =
        `🪙 <b>تخفيض العملات المباشر للمنتج:</b>\n` +
        `📦 <b>${esc(deal.title).slice(0, 75)}</b>\n` +
        `${priceInfo}\n` +
        `🔗 <b><a href="${deal.links.coin}">اضغط هنا لفتح رابط أقصى تخفيض عملات (Coins) 👈</a></b>`;

      const markup = {
        inline_keyboard: [
          [
            { text: "🪙 شراء بتخفيض العملات (Coins)", url: deal.links.coin },
            { text: "🛒 الرابط المباشر", url: deal.links.direct },
          ],
          [{ text: "📢 قناة الصفقات المعتمدة", url: CH_DZ }],
        ],
      };

      await sendMsg(env, chatId, body, markup, deadline, messageId);
      return { handled: "group_deal", pid, title: deal.title };
    }

    return { handled: "group_ignored" };
  }

  /* ---------------- private: commands ---------------- */

  if (text.startsWith("/myid") || text.startsWith("/id")) {
    const badge = isAdmin(userId, env)
      ? "👑 <b>مشرف معتمد (Admin)</b>"
      : "مستخدم عادي";
    await sendMsg(
      env,
      chatId,
      `🆔 <b>معرف التيليجرام الخاص بك:</b> <code>${userId}</code>\n<b>الرتبة:</b> ${badge}`,
      null,
      deadline
    );
    return { handled: "myid" };
  }

  if (text.startsWith("/start")) {
    const parts = text.split(/\s+/);
    const param = (parts[1] || "").toLowerCase();

    let userLangNow = lang;
    if (param.includes("fr")) {
      userLangNow = "fr";
      userLang.set(userId, "fr");
    } else if (param.includes("ar")) {
      userLangNow = "ar";
      userLang.set(userId, "ar");
    }

    if (["meta", "ad", "fb", "coins", "promo", "deal"].some((k) => param.includes(k))) {
      const adWelcome =
        userLangNow === "fr"
          ? `🇫🇷 <b>Bienvenue sur DealScout Bot via notre promo Réduction Pièces !</b> 🪙🔥\n\n` +
            `Ce bot vous aide à économiser jusqu'à <b>70%</b> sur AliExpress grâce aux pièces (Coins) !\n\n` +
            `📌 <b>Testez en 3 étapes simples :</b>\n` +
            `1️⃣ Ouvrez <b>AliExpress</b> et choisissez un produit.\n` +
            `2️⃣ Cliquez sur <b>Partager</b> puis <b>Copier le lien</b>.\n` +
            `3️⃣ <b>Collez le lien ici dans le chat</b>.\n\n` +
            `⚡ Le bot vous enverra les liens au meilleur prix en Euros !\n\n` +
            `📢 <i>Rejoignez notre canal officiel de bons plans :</i> @francedealsdz`
          : `🇩🇿 <b>مرحباً بك في بوت DealScout DZ عبر إعلان تخفيض العملات!</b> 🪙🔥\n\n` +
            `هذا البوت يساعدك على توفير حتى <b>70%</b> من سعر أي منتج في <b>AliExpress</b> عبر تحويله إلى رابط خصم العملات (Coins) الأقصى!\n\n` +
            `📌 <b>جرّب الآن في 3 خطوات بسيطة:</b>\n` +
            `1️⃣ افتح تطبيق <b>AliExpress</b> واختر أي منتج تريده.\n` +
            `2️⃣ اضغط على زر المشاركة <b>(Share)</b> ثم نسخ الرابط <b>(Copy link)</b>.\n` +
            `3️⃣ <b>ألصق الرابط هنا في هذه المحادثة فوراً</b>.\n\n` +
            `⚡ سيرسل لك البوت روابط الشراء بأقل سعر ممكن بالدينار الجزائري!\n\n` +
            `📢 <i>تابع أيضاً قناتنا الرسمية لأقوى الصفقات اليومية:</i> @DzAliexpress0`;

      await sendMsg(
        env,
        chatId,
        adWelcome,
        userLangNow === "fr" ? startMarkupFr() : startMarkupAr(),
        deadline
      );
      return { handled: "start_ad" };
    }

    await sendMsg(
      env,
      chatId,
      userLangNow === "fr" ? WELCOME_FR : WELCOME_AR,
      userLangNow === "fr" ? startMarkupFr() : startMarkupAr(),
      deadline
    );
    return { handled: "start" };
  }

  if (["/fr", "/french", "francais", "français"].includes(text)) {
    userLang.set(userId, "fr");
    await sendMsg(
      env,
      chatId,
      "✅ <b>La langue a été changée en Français !</b>\n\n" + WELCOME_FR,
      startMarkupFr(),
      deadline
    );
    return { handled: "lang_fr" };
  }

  if (["/ar", "/arabic", "عربي", "العربية"].includes(text)) {
    userLang.set(userId, "ar");
    await sendMsg(
      env,
      chatId,
      "✅ <b>تم تغيير اللغة إلى العربية !</b>\n\n" + WELCOME_AR,
      startMarkupAr(),
      deadline
    );
    return { handled: "lang_ar" };
  }

  if (text.startsWith("/calc") || text.startsWith("/حساب")) {
    const m = text.match(/([0-9]+[.,]?[0-9]*)/);
    if (!m) {
      await sendMsg(
        env,
        chatId,
        "💡 <b>طريقة استخدام الحاسبة:</b>\nأرسل المبلغ بالدولار مع الأمر، مثال:\n<code>/calc 15.5</code>",
        null,
        deadline
      );
      return { handled: "calc_help" };
    }
    const usd = parseFloat(m[1].replace(",", "."));
    const rate = await getUsdtRate();
    const dzd = Math.round(usd * rate);
    const total = dzd + 130;
    const body =
      `🧮 <b>حاسبة سعر الشراء بالدينار الجزائري 🇩🇿</b>\n\n` +
      `💵 <b>المبلغ بالدولار:</b> ${usd.toFixed(2)}$\n` +
      `📈 <b>سعر صرف الـ USDT الحالي:</b> ${rate.toFixed(1)} دج (المصدر: SquareAlgerie.com)\n` +
      `━━━━━━━━━━━━━━━━━\n` +
      `▫️ <b>قيمة السلعة بالدينار:</b> <b>${nf.format(dzd)} دج</b>\n` +
      `▫️ <b>رسوم طرد البريد الجزائري:</b> ~<b>130 دج</b>\n` +
      `💰 <b>التكلفة الإجمالية التقديرية:</b> ~<b>${nf.format(total)} دج</b>\n\n` +
      `💡 <i>نصيحة: استخدم دائماً رابط العملات (Coins) لتخفيض القيمة بالدولار قبل الشراء!</i>`;
    await sendMsg(env, chatId, body, null, deadline);
    return { handled: "calc" };
  }

  if (
    text.startsWith("/rate") ||
    text.startsWith("/square") ||
    text.startsWith("/سكوار") ||
    text.startsWith("سعر السكوار") ||
    text.startsWith("سعر الدولار")
  ) {
    const rate = await getUsdtRate();
    const body =
      `📈 <b>سعر صرف الـ USDT الحالي في السوق الموازي:</b>\n\n` +
      `💵 <b>1 USDT</b> ≈ <b>${rate.toFixed(1)} دج</b> 🇩🇿\n\n` +
      `📊 المصدر المباشر: <a href="https://squarealgerie.com">SquareAlgerie.com</a>\n` +
      `🪙 <i>لحساب تكلفة أي طلب بالدينار أرسل: <code>/calc 20</code></i>`;
    await sendMsg(env, chatId, body, null, deadline);
    return { handled: "rate" };
  }

  if (text.startsWith("/help") || text.includes("كيف") || text.includes("طريقة") || text.toLowerCase().includes("aide")) {
    await sendMsg(env, chatId, lang === "fr" ? HELP_FR : HELP_AR, null, deadline);
    return { handled: "help" };
  }

  if (text.startsWith("/coupons") || text.includes("كوبون") || text.includes("كود")) {
    await sendMsg(env, chatId, COUPONS_AR, null, deadline);
    return { handled: "coupons" };
  }

  if (text.startsWith("/post") || text.startsWith("/publish")) {
    if (!isAdmin(userId, env)) {
      await sendMsg(env, chatId, "⚠️ عذراً، هذا الأمر مخصص لمشرف القناة فقط.", null, deadline);
      return { handled: "post_denied" };
    }
    const sub = text.split(/\s+/).length > 1 ? text.slice(text.indexOf(" ") + 1) : "";
    const pid = await resolveProductId(sub, deadline);
    if (!pid) {
      await sendMsg(
        env,
        chatId,
        "⚠️ يرجى تزويد رابط صحيح للمنتج بعد الأمر، مثال:\n<code>/post https://a.aliexpress.com/_xxxx</code>",
        null,
        deadline
      );
      return { handled: "post_no_pid" };
    }
    await sendMsg(env, chatId, "⏳ جاري تحضير ونشر العرض في القناة @DzAliexpress0...", null, deadline);
    const pub = await publishToChannel(pid, sub, env, deadline);
    await sendMsg(
      env,
      chatId,
      pub.ok
        ? `✅ <b>تم نشر العرض بنجاح في القناة!</b>\n\n🔗 <b>رابط المنشور:</b> <a href="${CH_DZ}/${pub.messageId}">اضغط هنا 👈</a>`
        : `❌ فشل نشر العرض في القناة: ${esc(pub.error || "unknown")}`,
      null,
      deadline
    );
    return { handled: "post", pid, ok: pub.ok };
  }

  /* ---------------- private: the link flow ---------------- */

  const pid = await resolveProductId(text, deadline);
  if (!pid) {
    const helpMsg =
      lang === "fr"
        ? `⚠️ <b>Veuillez envoyer un lien AliExpress valide.</b>\n\n` +
          `📌 <b>Tous les formats de liens sont supportés :</b>\n` +
          `• Liens de l'application : <code>https://a.aliexpress.com/_xxxx</code>\n` +
          `• Liens du navigateur : <code>https://aliexpress.com/item/100500...html</code>\n` +
          `• ID du produit directement : <code>1005007458498882</code>\n\n` +
          `💡 Tapez /help pour voir le guide d'utilisation.`
        : `⚠️ <b>الرجاء إرسال رابط صحيح لمنتج من AliExpress.</b>\n\n` +
          `📌 <b>يدعم البوت جميع الروابط:</b>\n` +
          `• روابط التطبيق: <code>https://a.aliexpress.com/_xxxx</code>\n` +
          `• روابط المتصفح: <code>https://aliexpress.com/item/100500...html</code>\n` +
          `• كود المنتج مباشرة: <code>1005007458498882</code>\n\n` +
          `💡 أو اكتب /calc لحساب الأسعار بالدينار، أو /help لمعرفة كيفية الاستخدام.`;
    await sendMsg(env, chatId, helpMsg, null, deadline);
    return { handled: "no_pid" };
  }

  const limit = checkRateLimit(userId, env);
  if (limit.limited) {
    const waitMin = Math.floor(limit.waitMs / 60000) + 1;
    const body =
      `⏳ <b>عذراً! لقد وصلت إلى الحد الأقصى للطلبات (20 رابط في الساعة).</b>\n\n` +
      `لتفادي الضغط على السيرفرات ولحماية الخدمة للجميع، يرجى الانتظار <b>~${waitMin} دقيقة</b> قبل إرسال روابط جديدة.\n\n` +
      `📢 <i>تابع أحدث الصفقات الحصرية المنشورة مباشرة على قناتنا:</i> @DzAliexpress0`;
    await sendMsg(env, chatId, body, null, deadline);
    return { handled: "rate_limited", pid };
  }

  await tg(env, "sendChatAction", { chat_id: chatId, action: "typing" }, deadline);

  const deal = await generateDeal(pid, text, lang, env, deadline);

  if (isAdmin(userId, env)) {
    deal.markup.inline_keyboard.unshift([
      { text: "📢 نشر هذا العرض في القناة مباشرة 🚀", callback_data: `admin_pub_${pid}` },
    ]);
  }

  let res;
  if (deal.image) {
    res = await sendPhoto(env, chatId, deal.image, deal.text, deal.markup, deadline);
    if (!res.ok) {
      res = await sendMsg(env, chatId, deal.text, deal.markup, deadline);
    }
  } else {
    res = await sendMsg(env, chatId, deal.text, deal.markup, deadline);
  }

  return {
    handled: "deal",
    pid,
    title: deal.title,
    price: deal.price,
    sent: res.ok,
    error: res.error,
  };
}

/* ------------------------------------------------------------------ */
/* Entrypoint                                                          */
/* ------------------------------------------------------------------ */

async function handleUpdate(update, env, deadline) {
  if (!update || typeof update !== "object") return { skipped: "bad_update" };
  if (update.callback_query) return handleCallback(update.callback_query, env, deadline);
  const message = update.message || update.edited_message;
  if (!message) return { skipped: "unsupported_update" };
  return handleMessage(message, env, deadline);
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    if (request.method === "GET") {
      if (url.pathname === "/health") {
        return json({
          ok: true,
          service: "alilo07bot",
          webhook: "/telegram",
          token_configured: Boolean(env.TELEGRAM_BOT_TOKEN),
          time: new Date().toISOString(),
        });
      }
      return new Response("Alilo07BOT webhook worker — POST /telegram", {
        status: 200,
        headers: { "content-type": "text/plain; charset=utf-8" },
      });
    }

    if (request.method !== "POST") {
      return new Response("Method not allowed", { status: 405 });
    }

    if (url.pathname !== "/telegram" && url.pathname !== "/") {
      return new Response("Not found", { status: 404 });
    }

    // Telegram sends the secret in this header when secret_token is set.
    if (env.TELEGRAM_WEBHOOK_SECRET) {
      const got = request.headers.get("x-telegram-bot-api-secret-token");
      if (got !== env.TELEGRAM_WEBHOOK_SECRET) {
        return new Response("Forbidden", { status: 403 });
      }
    }

    let update;
    try {
      update = await request.json();
    } catch (_) {
      return new Response("Bad request", { status: 400 });
    }

    const deadline = Date.now() + WORK_BUDGET_MS;

    try {
      const result = await handleUpdate(update, env, deadline);
      // Debug body only for the operator (requires the webhook secret).
      if (request.headers.get("x-debug") === "1") {
        return json({ ok: true, result });
      }
      return new Response("ok", { status: 200 });
    } catch (e) {
      console.error("update failed", e && e.stack ? e.stack : String(e));
      if (request.headers.get("x-debug") === "1") {
        return json({ ok: false, error: String(e && e.message ? e.message : e) }, 500);
      }
      // Always 200 so Telegram does not hammer us with retries.
      return new Response("ok", { status: 200 });
    }
  },
};

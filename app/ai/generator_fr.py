import re
import hashlib
import html
from typing import Optional, List, Dict
from app.config.settings import settings
from app.utils.logger import logger

class FranceDealCaptionGenerator:
    """
    Generates authentic, high-converting French deal and coupon captions
    for AliExpress France shoppers and the @francedealsdz channel.
    """

    def _select_smart_hook(
        self,
        title: str,
        eur_price: float,
        has_points_discount: bool,
        has_coupon: bool,
        is_price_drop: bool = False,
        is_restock: bool = False
    ) -> str:
        h = int(hashlib.md5(title.encode()).hexdigest(), 16)
        t_lower = title.lower()

        # 1. Restock priority hook
        if is_restock:
            restock_hooks = [
                "🚨 <b>Alerte Restock : De retour en stock en quantité limitée ! 🔥📦</b>",
                "⚡ <b>Retour en stock immédiat.. Faites vite ! 🔥</b>",
                "🔥 <b>Alerte Stock : L'offre vient de réapparaître ! ⚡</b>"
            ]
            return restock_hooks[h % len(restock_hooks)]

        # 2. Price drop arbitrage
        if is_price_drop:
            price_drop_hooks = [
                "💥 <b>Grosse baisse de prix supplémentaire ! 🔥📉</b>",
                "⚡ <b>Le prix vient de chuter.. Foncez avant épuisement ! 🔥</b>",
                "🔥 <b>Réduction supplémentaire exclusive 🔥</b>"
            ]
            return price_drop_hooks[h % len(price_drop_hooks)]

        # 2. Categories
        is_gaming = any(k in t_lower for k in [
            "mouse", "keyboard", "headset", "controller", "gamepad", "gaming", "gamer",
            "attack shark", "ajazz", "aula", "vgn", "rgb", "joystick", "switch", "keycap"
        ])

        is_audio = any(k in t_lower for k in [
            "earphone", "earbuds", "headphone", "tws", "speaker", "soundbar",
            "soundcore", "qcy", "baseus bowie", "lenovo lp", "anc", "bluetooth speaker"
        ])

        is_tech = any(k in t_lower for k in [
            "ssd", "nvme", "m.2", "ram", "ddr4", "ddr5", "phone", "smartphone", "tablet", "pad",
            "xiaomi", "redmi", "poco", "honor", "realme", "charger", "gan", "powerbank"
        ])

        if is_gaming:
            return (
                "🎮 <b>Matériel Gaming à prix cassé 🔥⚡</b>" if (h % 2 == 0)
                else "🕹️ <b>Super deal Gaming à ne pas rater ! 🔥</b>"
            )

        if is_audio:
            return (
                "🎧 <b>Son de qualité & prix imbattable 🔥⚡</b>" if (h % 2 == 0)
                else "🔊 <b>Excellente réduction sur l'audio ⚡</b>"
            )

        if is_tech:
            return (
                "📱 <b>Bon plan Tech & Électronique au meilleur prix 🔥</b>" if (h % 2 == 0)
                else "⚡ <b>Offre exceptionnelle sur la Tech 🔥</b>"
            )

        candidates = [
            "⚡ <b>Super Bon Plan AliExpress France ! 🔥</b>",
            "🔥 <b>Excellente affaire à saisir rapidement !</b>",
            "💥 <b>Grosse promotion disponible dès maintenant 🔥</b>",
            "🎯 <b>Offre spéciale à prix réduit ⚡</b>"
        ]
        return candidates[h % len(candidates)]

    def format_coupon_list(
        self,
        coupon_items: List[Dict[str, str]],
        affiliate_url: str,
        promo_name: Optional[str] = "Party Ready Sale"
    ) -> str:
        """
        Builds French coupon bulletin format for multi-coupon lists.
        """
        lines = [
            f"✨📢 <b>Nouveaux Codes Promo disponibles pour le {promo_name} !</b> 📢✨",
            "",
            "✅ <b>Liste officielle des codes promo :</b>",
            ""
        ]

        for item in coupon_items:
            tier = item.get("tier", "").strip()
            code = item.get("code", "").strip()
            # Clean tier for French presentation
            tier_display = tier.replace("$", "€")
            if tier_display and code:
                lines.append(f"🎟️ <b>Code {tier_display} :</b> <code>{code}</code>")
            elif code:
                lines.append(f"🎟️ <b>Code promo :</b> <code>{code}</code>")

        lines.append("")
        lines.append("⭕️ <b>Tutoriel : Verrouiller tous les codes sur votre compte :</b>")
        lines.append("⚠️ <b>Commencez par les gros codes (-60€, -45€...)</b> puis appliquez les suivants pour les lier à votre compte avant rupture de stock !")
        lines.append("🔹 <b>Appliquez tous les codes sur ce produit (tous les seuils passent) ⤵️</b>")
        lines.append("https://s.click.aliexpress.com/e/_c2QPADRL")
        lines.append("")
        lines.append("🪙 <i>Bot réduction pièces (Coins) : @Alilo07BOT</i>")
        lines.append("📢 <i>Canal de bons plans : @francedealsdz</i>")

        return "\n".join(lines)

    def format_event_campaign(
        self,
        raw_text: str,
        affiliate_url: str
    ) -> str:
        """
        Formats AliExpress official event / warm-up announcements in French.
        """
        clean_lines = []
        for line in raw_text.splitlines():
            line_str = line.strip()
            if not line_str or "http://" in line_str or "https://" in line_str or "t.me/" in line_str:
                continue
            clean_lines.append(line_str)

        main_content = "\n".join(clean_lines).strip()
        if not main_content:
            main_content = "✨ <b>Promotions exclusives et codes de réduction AliExpress France !</b>"

        lines = [
            f"🎉 <b>{main_content}</b>",
            "",
            "🔗 <b>Lien d'accès et activation des offres ⬇️</b>",
            f"{affiliate_url}",
            "",
            "🚚 <i>Livraison directe en France métropolitaine 🇫🇷</i>",
            "📢 <i>Canal officiel : @francedealsdz</i>"
        ]
        return "\n".join(lines)

    def _format_deterministic(
        self,
        title: str,
        eur_price: float,
        usd_price: float,
        affiliate_url: str,
        coupon_code: Optional[str] = None,
        seller_coupon: Optional[str] = None,
        has_points_discount: bool = False,
        is_price_drop: bool = False,
        is_restock: bool = False,
        deal_type: str = "coin",
        country_info: Optional[str] = None,
        raw_text: Optional[str] = None
    ) -> str:
        lines = []

        # 1. Smart French Hook in blockquote
        if deal_type == "bundle":
            h = int(hashlib.md5(title.encode()).hexdigest(), 16)
            if is_restock:
                hook = "🚨 <b>Alerte Restock : De retour en offre Choice Bundle ! 🔥📦</b>"
            else:
                bundle_hooks = [
                    "📦 <b>Offre Choice Bundle : 3 articles à prix cassé ! 🔥</b>",
                    "🛍️ <b>Super deal Choice Bundle à ne pas manquer ! 🔥⚡</b>",
                    "⚡ <b>Sélection Choice Bundle 3 articles au meilleur prix 🔥</b>",
                    "🔥 <b>Bon Plan Choice Bundle exceptionnel dès 3 articles ! 🔥</b>"
                ]
                hook = bundle_hooks[h % len(bundle_hooks)]
        else:
            hook = self._select_smart_hook(
                title=title,
                eur_price=eur_price,
                has_points_discount=has_points_discount,
                has_coupon=bool(coupon_code or seller_coupon),
                is_price_drop=is_price_drop,
                is_restock=is_restock
            )
        clean_hook = re.sub(r'</?b>', '', hook).strip()
        lines.append(f"<blockquote>🔥 <b>{clean_hook}</b></blockquote>")

        # 2. Choice Bundle Alert in blockquote
        if deal_type == "bundle":
            lines.append("<blockquote>📦 <b>Alerte Choice Bundle :</b> Ajoutez 3 articles au panier pour profiter de ce prix et de la livraison gratuite ! 🛍️</blockquote>")

        # 2.5 Restock / Price drop note in blockquote
        if is_restock:
            lines.append("<blockquote>⚡ <b>Alerte Restock :</b> De retour en stock en quantité très limitée.. Faites vite ! 🏃‍♂️💨</blockquote>")
        elif is_price_drop:
            lines.append("<blockquote>📉 <b>Baisse de Prix :</b> Nouveau prix réduit, encore moins cher qu'auparavant ! 🔥</blockquote>")

        # 3. Shipping / Location note in blockquote
        lines.append("<blockquote>🚚 <b>Livraison :</b> France métropolitaine 🇫🇷</blockquote>")

        # 3.5 French retail comparison quote if mentioned in source
        if raw_text:
            p_fr_quote = re.search(
                r'(?:prix\s*(?:constaté\s*(?:ailleurs)?|normal|habituel|conseillé|en\s*france|magasin|ailleurs)|au\s*lieu\s*de|vendu\s*à|vendu|valeur)\s*[:：\-]?\s*([0-9\s\.,]+[€$]|(?:plus\s*de\s*)?[0-9\s\.,]+[€$])',
                raw_text, re.IGNORECASE
            )
            if p_fr_quote:
                matched_q = p_fr_quote.group(0).strip()
                lines.append(f"<blockquote>🏷️ <b>Prix constaté :</b> {html.escape(matched_q)} 🛒</blockquote>")

        lines.append("")

        safe_title = html.escape(title)
        lines.append(f"✅ <b>{safe_title}</b>")
        lines.append("")

        # Price
        if eur_price and eur_price > 0:
            usd_str = f" (${usd_price:.2f})" if usd_price and usd_price > 0 else ""
            lines.append(f"💰 <b>Prix :</b> <b>{eur_price:.2f}€</b>{usd_str} 🔥")
        elif usd_price and usd_price > 0:
            approx_eur = usd_price * (settings.EUR_USD_RATE or 0.92)
            lines.append(f"💰 <b>Prix :</b> <b>{approx_eur:.2f}€</b> (${usd_price:.2f}) 🔥")
        else:
            lines.append("💰 <b>Prix :</b> <b>Prix réduit exceptionnel</b> 🔥")

        if seller_coupon and str(seller_coupon).strip() not in {"0", "0$", "$0", "0€", "None", ""}:
            s_clean = str(seller_coupon).strip()
            # In France, convert dollar coupon markers to EUR
            s_clean = re.sub(r'[\$USDusd\s]', '', s_clean)
            if s_clean and not s_clean.endswith('€'):
                s_clean = f"{s_clean}€"
            lines.append(f"🌷 <b>Coupon vendeur :</b> <code>{html.escape(s_clean)}</code>")

        if coupon_code:
            lines.append(f"🏷️ <b>Code promo :</b> <code>{html.escape(coupon_code)}</code>")

        if deal_type == "bundle":
            lines.append("📦 <b>Offre Choice Bundle — 3 articles minimum</b>")
        elif has_points_discount:
            lines.append("🪙 <b>Réduction pièces (Coins) appliquée via le lien</b>")

        lines.append("")
        if deal_type == "bundle":
            lines.append("🛒 <b>Lien de l'offre Bundle ⤵️</b>")
        else:
            lines.append("🛒 <b>Lien du Bon Plan ⤵️</b>")
        lines.append(f"{affiliate_url}")
        lines.append("")
        lines.append("🤖 <b>Bot Réduction Pièces (Coins) :</b> @Alilo07BOT")
        lines.append("📢 @francedealsdz")

        return "\n".join(lines)

    async def generate(
        self,
        title: str,
        eur_price: Optional[float],
        usd_price: Optional[float],
        affiliate_url: str,
        coupon_code: Optional[str] = None,
        seller_coupon: Optional[str] = None,
        has_points_discount: bool = False,
        coupon_list: Optional[List[Dict[str, str]]] = None,
        is_price_drop: bool = False,
        is_restock: bool = False,
        deal_type: str = "coin",
        country_info: Optional[str] = None,
        raw_text: Optional[str] = None
    ) -> str:
        if not is_restock and raw_text:
            from app.aliexpress.parser import detect_restock_deal
            is_restock = detect_restock_deal(raw_text)

        if not is_price_drop and raw_text:
            from app.aliexpress.parser import detect_price_drop_deal
            is_price_drop = detect_price_drop_deal(raw_text)

        if coupon_list and len(coupon_list) >= 2:
            return self.format_coupon_list(coupon_list, affiliate_url)

        if (not eur_price or eur_price <= 0) and (not usd_price or usd_price <= 0) and raw_text and any(k in raw_text.lower() for k in ["code", "promo", "coupon", "reduction", "party ready", "choice day"]):
            return self.format_event_campaign(raw_text, affiliate_url)

        clean_title = title.strip() if title else "Produit sélectionné sur AliExpress"
        eur_val = eur_price or (round(usd_price * (settings.EUR_USD_RATE or 0.92), 2) if usd_price else 0.0)
        usd_val = usd_price or 0.0

        return self._format_deterministic(
            title=clean_title,
            eur_price=eur_val,
            usd_price=usd_val,
            affiliate_url=affiliate_url,
            coupon_code=coupon_code,
            seller_coupon=seller_coupon,
            has_points_discount=has_points_discount,
            is_price_drop=is_price_drop,
            is_restock=is_restock,
            deal_type=deal_type,
            country_info=country_info,
            raw_text=raw_text
        )

france_caption_generator = FranceDealCaptionGenerator()

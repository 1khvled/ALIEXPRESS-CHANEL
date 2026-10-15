"""
Parcel Tracking Module for DealScout DZ.
Specialized tracking for AliExpress orders shipping to Algeria (Algérie Poste, Cainiao, Sunyou, Yanwen, EMS).
Queries free open carrier endpoints (Cainiao Global) and provides universal multi-carrier tracking integrations.
"""
import re
import html
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
import httpx


CARRIER_PATTERNS = [
    {
        "id": "cainiao",
        "name_ar": "علي إكسبرس تشويس / كاينياو (Cainiao Global)",
        "name_fr": "AliExpress Choice / Cainiao Global",
        "pattern": r"^LP\d{14,16}$",
        "badge_color": "crimson",
        "typical_days": "14-25 يوم",
        "desc_ar": "شحن سريع رسمي لـ AliExpress Choice، يتم تسليمه لبريد الجزائر عند الوصول.",
        "desc_fr": "Expédition officielle AliExpress Choice, remise à Algérie Poste à l'arrivée."
    },
    {
        "id": "algerie_poste",
        "name_ar": "بريد الجزائر (Algérie Poste / EMS)",
        "name_fr": "Algérie Poste / EMS International",
        "pattern": r"^[A-Z]{2}\d{9}DZ$",
        "badge_color": "emerald",
        "typical_days": "1-3 أيام داخل الجزائر",
        "desc_ar": "طرد مسجل لدى بريد الجزائر برقم تتبع وطني ينتهي بـ DZ. يستلم من مكتب البريد المحلي.",
        "desc_fr": "Colis recommandé national Algérie Poste se terminant par DZ. Retrait en agence postale."
    },
    {
        "id": "sunyou",
        "name_ar": "بريد سانيو (SunYou Logistics)",
        "name_fr": "SunYou Special Economy",
        "pattern": r"^SY\d{11,13}$|^SYBAA\d+$",
        "badge_color": "amber",
        "typical_days": "20-35 يوم",
        "desc_ar": "شحن اقتصادي شائع للمنتجات الصغيرة والملحقات، يدخل الجزائر عبر التبادل البريدي الدولي.",
        "desc_fr": "Transporteur économique pour petits accessoires, acheminé via le réseau UPU vers l'Algérie."
    },
    {
        "id": "yanwen",
        "name_ar": "بريد يانوين (Yanwen Express)",
        "name_fr": "Yanwen Economic Air Mail",
        "pattern": r"^[A-Z]{2}\d{9}YP$",
        "badge_color": "sky",
        "typical_days": "18-30 يوم",
        "desc_ar": "خط شحن صيني دولي ينتهي بـ YP، يتحول لرقم تتبع UPU عند دخول التبادل الدولي.",
        "desc_fr": "Courrier aérien économique Yanwen, transféré au bureau postal local en Algérie."
    },
    {
        "id": "singapore_post",
        "name_ar": "بريد سنغافورة (Singapore Post)",
        "name_fr": "Singapore Post Registered",
        "pattern": r"^[A-Z]{2}\d{9}SG$",
        "badge_color": "purple",
        "typical_days": "15-28 يوم",
        "desc_ar": "شحن دولي مسجل عبر بريد سنغافورة، مستخدم للأجهزة التي تحتوي على بطاريات.",
        "desc_fr": "Poste recommandée de Singapour, fréquemment utilisée pour les appareils à batterie."
    },
    {
        "id": "china_post",
        "name_ar": "بريد الصين المسجل (China Post)",
        "name_fr": "China Post Registered Air Mail",
        "pattern": r"^[A-Z]{2}\d{9}CN$",
        "badge_color": "rose",
        "typical_days": "20-40 يوم",
        "desc_ar": "البريد الحكومي الصيني المعتمد، يمكن تتبعه مباشرة حتى وصوله للجمارك الجزائرية.",
        "desc_fr": "Poste nationale chinoise officielle, traçable jusqu'au dédouanement en Algérie."
    },
    {
        "id": "upu_standard",
        "name_ar": "البريد الدولي الموحد (UPU Standard)",
        "name_fr": "Union Postale Universelle (UPU)",
        "pattern": r"^[A-Z]{2}\d{9}[A-Z]{2}$",
        "badge_color": "blue",
        "typical_days": "15-30 يوم",
        "desc_ar": "طرد بريدي مسجل متوافق مع نظام التتبع العالمي لبريد الجزائر.",
        "desc_fr": "Colis postal international standard UPU, traçable dans le système d'Algérie Poste."
    }
]


def sanitize_tracking_number(raw_num: str) -> str:
    """Clean tracking number from whitespace, URL params, or special chars."""
    if not raw_num:
        return ""
    # Strip spaces, dashes, and lowercase to uppercase
    cleaned = re.sub(r"[\s\-_#]+", "", str(raw_num)).strip().upper()
    # If a full tracking URL was pasted, extract the number
    match = re.search(r"(?:nums?|mailNos?|track(?:ing)?(?:_?no)?)[:=]([A-Za-z0-9]+)", cleaned, re.IGNORECASE)
    if match:
        return match.group(1).upper()
    return cleaned


def detect_carrier(num: str) -> Dict[str, Any]:
    """Detect probable carrier based on tracking number format."""
    cleaned = sanitize_tracking_number(num)
    for c in CARRIER_PATTERNS:
        if re.match(c["pattern"], cleaned, re.IGNORECASE):
            return {
                "id": c["id"],
                "name_ar": c["name_ar"],
                "name_fr": c["name_fr"],
                "badge_color": c["badge_color"],
                "typical_days": c["typical_days"],
                "desc_ar": c["desc_ar"],
                "desc_fr": c["desc_fr"],
                "matched": True
            }
    # Fallback generic
    return {
        "id": "generic",
        "name_ar": "طرد دولي / كود تسليم محلي",
        "name_fr": "Colis International / Coursier",
        "badge_color": "zinc",
        "typical_days": "15-30 يوم",
        "desc_ar": "رقم تتبع قياسي للشحنات المتجهة إلى الجزائر، يدعم التتبع العالمي عبر 17Track وCainiao.",
        "desc_fr": "Numéro de suivi standard, compatible avec le traçage universel 17Track et Cainiao.",
        "matched": False
    }


def get_direct_tracking_links(num: str) -> Dict[str, str]:
    """Generate verified direct portal links for deep tracking."""
    cleaned = sanitize_tracking_number(num)
    return {
        "track17": f"https://t.17track.net/en#nums={cleaned}",
        "17track": f"https://t.17track.net/en#nums={cleaned}",
        "cainiao": f"https://global.cainiao.com/detail.html?mailNoList={cleaned}",
        "algerie_poste": f"https://t.17track.net/ar#nums={cleaned}",
        "postal_ninja": f"https://postal.ninja/en/track/{cleaned}"
    }


async def query_cainiao_api(num: str, timeout: float = 5.0) -> Dict[str, Any]:
    """
    Query Cainiao's public free tracking endpoint without API key.
    Endpoint: https://global.cainiao.com/global/detail.json?mailNos={num}
    """
    cleaned = sanitize_tracking_number(num)
    url = f"https://global.cainiao.com/global/detail.json?mailNos={cleaned}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "fr,en-US;q=0.9,ar;q=0.8"
    }
    
    events: List[Dict[str, Any]] = []
    status_label = "in_transit"
    latest_event = None

    try:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            resp = await client.get(url, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("success") and isinstance(data.get("module"), list) and len(data["module"]) > 0:
                    mod = data["module"][0]
                    detail_list = mod.get("detailList") or []
                    for item in detail_list:
                        desc = item.get("desc") or item.get("standerdDesc") or ""
                        time_str = item.get("time") or item.get("timeZone") or ""
                        action = item.get("action") or ""
                        if desc:
                            events.append({
                                "description": html.escape(desc),
                                "time": time_str,
                                "action": action,
                                "location": item.get("address", "")
                            })
                    if events:
                        latest_event = events[0]
                        # Determine high-level stage
                        first_desc = events[0]["description"].lower()
                        if any(w in first_desc for w in ["delivered", "livré", "تم التسليم", "pickup", "pick up"]):
                            status_label = "delivered"
                        elif any(w in first_desc for w in ["customs", "douane", "جمارك", "import clearance"]):
                            status_label = "customs"
                        elif any(w in first_desc for w in ["arrived at destination", "arrivée", "algeria", "alger"]):
                            status_label = "in_destination_country"
                        elif any(w in first_desc for w in ["departed country of origin", "en vol", "handed over"]):
                            status_label = "in_flight"
                        else:
                            status_label = "in_transit"
    except Exception:
        pass

    return {
        "success": len(events) > 0,
        "events_count": len(events),
        "events": events,
        "latest_event": latest_event,
        "status_stage": status_label
    }


async def track_algeria_parcel(raw_num: str) -> Dict[str, Any]:
    """
    Full tracking coordinator for Algerian AliExpress shoppers.
    Returns carrier detection, live checkpoints (if Cainiao), Algerian transit phases,
    and verified 1-click external tracking links.
    """
    cleaned = sanitize_tracking_number(raw_num)
    if not cleaned or len(cleaned) < 5 or len(cleaned) > 40:
        return {
            "ok": False,
            "error_ar": "رقم التتبع غير صالح. يرجى إدخال رقم تتبع صحيح يتراوح بين 5 و35 حرفاً أو رقماً.",
            "error_fr": "Numéro de suivi invalide. Veuillez saisir un numéro valide (5 à 35 caractères)."
        }

    carrier = detect_carrier(cleaned)
    direct_links = get_direct_tracking_links(cleaned)
    cainiao_data = await query_cainiao_api(cleaned, timeout=4.5)

    # Standard Algerian e-commerce delivery workflow stages
    algeria_delivery_stages = [
        {
            "step": 1,
            "title_ar": "تم إرسال الطرد من المستودع (الصين)",
            "title_fr": "Colis expédié de l'entrepôt (Chine)",
            "desc_ar": "تجهيز الشحنة وانطلاقها من مركز فرز Cainiao الدولي.",
            "desc_fr": "Préparation et départ du centre de tri international.",
            "completed": True
        },
        {
            "step": 2,
            "title_ar": "النقل الجوي الدولي نحو الجزائر",
            "title_fr": "Transit aérien international vers l'Algérie",
            "desc_ar": "رحلة الشحن الجوي عبر خطوط التبادل البريدي الدولي.",
            "desc_fr": "Acheminement aérien via le réseau postal mondial.",
            "completed": cainiao_data["status_stage"] in ["in_flight", "in_destination_country", "customs", "delivered"]
        },
        {
            "step": 3,
            "title_ar": "الوصول إلى مركز الفرز (مطار هواري بومدين / CTN الجزائر)",
            "title_fr": "Arrivée au Centre National de Tri (CTN Alger)",
            "desc_ar": "تسجيل الطرد في مركز الفرز البريدي وتوجيهه لمصالح الجمارك.",
            "desc_fr": "Enregistrement au centre postal et transmission aux douanes.",
            "completed": cainiao_data["status_stage"] in ["in_destination_country", "customs", "delivered"]
        },
        {
            "step": 4,
            "title_ar": "المعالجة الجمركية (Dédouanement)",
            "title_fr": "Contrôle et dédouanement douanier",
            "desc_ar": "إعفاء ضريبي كامل للطرود الشخصية غير التجارية وفق القوانين الجزائرية.",
            "desc_fr": "Exonération fiscale totale pour les colis personnels non commerciaux.",
            "completed": cainiao_data["status_stage"] in ["customs", "delivered"]
        },
        {
            "step": 5,
            "title_ar": "التوزيع والاستلام في مكتب بريد بلديتك",
            "title_fr": "Mise à disposition au bureau de poste local",
            "desc_ar": "استلام إشعار SMS أو إشعار ورقي، ثم استلام الطرد بالبطاقة الوطنية.",
            "desc_fr": "Réception du SMS / Avis de passage et retrait avec pièce d'identité.",
            "completed": cainiao_data["status_stage"] == "delivered"
        }
    ]

    return {
        "ok": True,
        "tracking_number": cleaned,
        "carrier": carrier,
        "has_live_checkpoints": cainiao_data["success"],
        "live_checkpoints": cainiao_data["events"],
        "latest_event": cainiao_data["latest_event"],
        "status_stage": cainiao_data["status_stage"],
        "delivery_stages": algeria_delivery_stages,
        "portal_links": direct_links,
        "direct_links": direct_links,
        "checked_at": datetime.now(timezone.utc).isoformat()
    }

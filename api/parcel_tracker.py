"""
Parcel Tracking Module for DealScout DZ.
Specialized, high-precision tracking for AliExpress orders shipping to Algeria.
Handles standard UPU S10 postal codes (CP...AE, RA...CN, RB...SG, etc.),
AliExpress Choice (LP...), Algérie Poste (DZ), SunYou (SY...), Yanwen (YP...), and EMS.
Provides intelligent carrier/origin detection, milestone progression, and direct deep-links.
"""
import re
import html
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
import httpx


UPU_COUNTRY_MAP = {
    "AE": {"name_ar": "الإمارات العربية المتحدة", "name_fr": "Émirats Arabes Unis", "flag": "🇦🇪", "carrier_ar": "بريد الإمارات (Emirates Post)", "carrier_fr": "Emirates Post"},
    "CN": {"name_ar": "الصين", "name_fr": "Chine", "flag": "🇨🇳", "carrier_ar": "بريد الصين (China Post)", "carrier_fr": "China Post"},
    "SG": {"name_ar": "سنغافورة", "name_fr": "Singapour", "flag": "🇸🇬", "carrier_ar": "بريد سنغافورة (Singapore Post)", "carrier_fr": "Singapore Post"},
    "NL": {"name_ar": "هولندا", "name_fr": "Pays-Bas", "flag": "🇳🇱", "carrier_ar": "بريد هولندا (PostNL)", "carrier_fr": "PostNL"},
    "TR": {"name_ar": "تركيا", "name_fr": "Turquie", "flag": "🇹🇷", "carrier_ar": "البريد التركي (PTT Turkey)", "carrier_fr": "PTT Turquie"},
    "MY": {"name_ar": "ماليزيا", "name_fr": "Malaisie", "flag": "🇲🇾", "carrier_ar": "بريد ماليزيا (Pos Malaysia)", "carrier_fr": "Pos Malaysia"},
    "FR": {"name_ar": "فرنسا", "name_fr": "France", "flag": "🇫🇷", "carrier_ar": "البريد الفرنسي (La Poste)", "carrier_fr": "La Poste France"},
    "DE": {"name_ar": "ألمانيا", "name_fr": "Allemagne", "flag": "🇩🇪", "carrier_ar": "البريد الألماني (Deutsche Post)", "carrier_fr": "Deutsche Post"},
    "GB": {"name_ar": "المملكة المتحدة", "name_fr": "Royaume-Uni", "flag": "🇬🇧", "carrier_ar": "البريد الملكي البريطاني (Royal Mail)", "carrier_fr": "Royal Mail"},
    "US": {"name_ar": "الولايات المتحدة", "name_fr": "États-Unis", "flag": "🇺🇸", "carrier_ar": "البريد الأمريكي (USPS)", "carrier_fr": "USPS"},
    "DZ": {"name_ar": "الجزائر", "name_fr": "Algérie", "flag": "🇩🇿", "carrier_ar": "بريد الجزائر (Algérie Poste)", "carrier_fr": "Algérie Poste"},
    "HK": {"name_ar": "هونغ كونغ", "name_fr": "Hong Kong", "flag": "🇭🇰", "carrier_ar": "بريد هونغ كونغ (Hong Kong Post)", "carrier_fr": "Hong Kong Post"},
    "UZ": {"name_ar": "أوزبكستان", "name_fr": "Ouzbékistan", "flag": "🇺🇿", "carrier_ar": "بريد أوزبكستان (Uzbekistan Post)", "carrier_fr": "Uzbekistan Post"},
    "ES": {"name_ar": "إسبانيا", "name_fr": "Espagne", "flag": "🇪🇸", "carrier_ar": "البريد الإسباني (Correos)", "carrier_fr": "Correos Espagne"},
    "IT": {"name_ar": "إيطاليا", "name_fr": "Italie", "flag": "🇮🇹", "carrier_ar": "البريد الإيطالي (Poste Italiane)", "carrier_fr": "Poste Italiane"},
    "BE": {"name_ar": "بلجيكا", "name_fr": "Belgique", "flag": "🇧🇪", "carrier_ar": "البريد البلجيكي (bpost)", "carrier_fr": "bpost Belgique"},
    "TH": {"name_ar": "تايلاند", "name_fr": "Thaïlande", "flag": "🇹🇭", "carrier_ar": "البريد التايلاندي (Thailand Post)", "carrier_fr": "Thailand Post"}
}


def sanitize_tracking_number(raw_num: str) -> str:
    """Clean tracking number from whitespace, URL params, or special chars."""
    if not raw_num:
        return ""
    cleaned = re.sub(r"[\s\-_#]+", "", str(raw_num)).strip().upper()
    match = re.search(r"(?:nums?|mailNos?|track(?:ing)?(?:_?no)?)[:=]([A-Za-z0-9]+)", cleaned, re.IGNORECASE)
    if match:
        return match.group(1).upper()
    return cleaned


def detect_carrier(num: str) -> Dict[str, Any]:
    """Detect carrier, origin country, flag, and service tier from tracking number format."""
    cleaned = sanitize_tracking_number(num)
    
    # 1. AliExpress Choice / Cainiao official (LP...)
    if re.match(r"^LP\d{14,16}$", cleaned, re.IGNORECASE):
        return {
            "id": "cainiao",
            "name_ar": "علي إكسبرس تشويس / كاينياو (Cainiao Global)",
            "name_fr": "AliExpress Choice / Cainiao Global",
            "carrier_code": "CAINIAO",
            "service_type_ar": "شحن سريع رسمي لـ AliExpress Choice",
            "service_type_fr": "Expédition officielle AliExpress Choice",
            "origin_country_ar": "الصين",
            "origin_country_fr": "Chine",
            "origin_flag": "🇨🇳",
            "destination_flag": "🇩🇿",
            "badge_color": "crimson",
            "typical_days": "14 - 25 يوم",
            "desc_ar": "شحن AliExpress Choice المباشر، يتم تسليمه لمركز الفرز CTN بالجزائر ثم مكتب بريد بلديتك.",
            "desc_fr": "Expédition prioritaire AliExpress Choice, remise au CTN Alger puis au bureau de poste local."
        }

    # 2. Algérie Poste / EMS National (DZ suffix)
    if re.match(r"^[A-Z]{2}\d{9}DZ$", cleaned, re.IGNORECASE):
        is_ems = cleaned.startswith("E")
        return {
            "id": "algerie_poste",
            "name_ar": "بريد الجزائر (Algérie Poste / EMS)" if is_ems else "بريد الجزائر الوطني (Algérie Poste)",
            "name_fr": "Algérie Poste / EMS" if is_ems else "Algérie Poste National",
            "carrier_code": "DZPOST",
            "service_type_ar": "بريد سريع EMS جزائري" if is_ems else "طرد مسجل لدى بريد الجزائر",
            "service_type_fr": "Courrier express EMS" if is_ems else "Colis recommandé national",
            "origin_country_ar": "الجزائر",
            "origin_country_fr": "Algérie",
            "origin_flag": "🇩🇿",
            "destination_flag": "🇩🇿",
            "badge_color": "emerald",
            "typical_days": "1 - 3 أيام",
            "desc_ar": "طرد مسجل برقم تتبع وطني ينتهي بـ DZ. يستلم من مكتب البريد المحلي ببطاقة التعريف الوطنية.",
            "desc_fr": "Colis recommandé national sous la responsabilité d'Algérie Poste. Retrait en agence avec pièce d'identité."
        }

    # 3. Yanwen Express (YP suffix, e.g. UJ123456789YP)
    if re.match(r"^[A-Z]{2}\d{9}YP$", cleaned, re.IGNORECASE) or cleaned.endswith("YP"):
        return {
            "id": "yanwen",
            "name_ar": "بريد يانوين (Yanwen Express Air Mail)",
            "name_fr": "Yanwen Economic Air Mail",
            "carrier_code": "YANWEN",
            "service_type_ar": "شحن جوي اقتصادي دولي",
            "service_type_fr": "Courrier aérien économique Yanwen",
            "origin_country_ar": "الصين",
            "origin_country_fr": "Chine",
            "origin_flag": "🇨🇳",
            "destination_flag": "🇩🇿",
            "badge_color": "sky",
            "typical_days": "18 - 30 يوم",
            "desc_ar": "شركة شحن دولية تنقل الطرد إلى مركز الترانزيت ثم تسلمه لبريد الجزائر.",
            "desc_fr": "Opérateur aérien international assurant le transit jusqu'au centre postal d'Alger."
        }

    # 4. SunYou Logistics (SY...)
    if re.match(r"^SY\d{11,13}$|^SYBAA\d+$", cleaned, re.IGNORECASE):
        return {
            "id": "sunyou",
            "name_ar": "بريد سانيو (SunYou Special Economy)",
            "name_fr": "SunYou Logistics Economy",
            "carrier_code": "SUNYOU",
            "service_type_ar": "شحن اقتصادي للمنتجات الصغيرة والملحقات",
            "service_type_fr": "Acheminement économique pour petits articles",
            "origin_country_ar": "الصين",
            "origin_country_fr": "Chine",
            "origin_flag": "🇨🇳",
            "destination_flag": "🇩🇿",
            "badge_color": "amber",
            "typical_days": "20 - 35 يوم",
            "desc_ar": "خط شحن صيني اقتصادي شائع، يدخل الجزائر عبر التبادل البريدي الدولي ويوزع بمكتب البريد المحلي.",
            "desc_fr": "Ligne logistique économique chinoise, remise aux douanes puis à Algérie Poste."
        }

    # 5. Standard UPU International Postal Code (e.g. CP032359951AE, RA123456789CN, RB123456789SG, RR123456789NL)
    upu_match = re.match(r"^([A-Z]{2})\d{9}([A-Z]{2})$", cleaned, re.IGNORECASE)
    if upu_match:
        prefix = upu_match.group(1).upper()
        country_code = upu_match.group(2).upper()
        country_info = UPU_COUNTRY_MAP.get(country_code, {
            "name_ar": f"دولة التصدير ({country_code})",
            "name_fr": f"Pays d'expédition ({country_code})",
            "flag": "🌐",
            "carrier_ar": f"البريد الدولي المعتمد ({country_code})",
            "carrier_fr": f"Poste Internationale ({country_code})"
        })

        if country_code == "SG":
            carrier_id = "singapore_post"
        elif country_code == "CN":
            carrier_id = "china_post"
        elif country_code == "DZ":
            carrier_id = "algerie_poste"
        else:
            carrier_id = "upu_standard"

        # Service type by UPU S10 prefix
        if prefix.startswith("C"):
            service_ar = "طرد بريدي دولي مسجل (Parcel Post - CP)"
            service_fr = "Colis postal international recommandé"
        elif prefix.startswith("E"):
            service_ar = "بريد سريع دولي ممتاز (EMS International Express)"
            service_fr = "Courrier express international EMS"
        elif prefix.startswith("R"):
            service_ar = "بريد جوي مسجل ذو أولوية (Registered Air Mail)"
            service_fr = "Courrier postal recommandé avec accusé"
        elif prefix.startswith("U"):
            service_ar = "طرد بريدي اقتصادي خفيف (Untracked / Economy Packet)"
            service_fr = "Petit paquet économique"
        else:
            service_ar = f"طرد بريدي دولي موحد ({prefix})"
            service_fr = f"Colis postal standard UPU ({prefix})"

        return {
            "id": carrier_id,
            "name_ar": f"{country_info['carrier_ar']} — UPU",
            "name_fr": f"{country_info['carrier_fr']} — UPU",
            "carrier_code": country_code,
            "service_type_ar": service_ar,
            "service_type_fr": service_fr,
            "origin_country_ar": country_info["name_ar"],
            "origin_country_fr": country_info["name_fr"],
            "origin_flag": country_info["flag"],
            "destination_flag": "🇩🇿",
            "badge_color": "blue",
            "typical_days": "15 - 30 يوم",
            "desc_ar": f"شحنة بريدية دولية مسجلة صادرة من {country_info['name_ar']} متجهة إلى الجزائر، تخضع لنظام التتبع الموحد وتستلم عبر بريد الجزائر.",
            "desc_fr": f"Envoi postal international au départ de {country_info['name_fr']} vers l'Algérie, acheminé via le réseau UPU et remis par Algérie Poste."
        }

    # 6. Fallback Generic International Carrier
    return {
        "id": "generic",
        "name_ar": "طرد دولي / كود تسليم بريدي",
        "name_fr": "Colis International / Coursier Postal",
        "carrier_code": "GLOBAL",
        "service_type_ar": "شحنة تجارة إلكترونية دولية",
        "service_type_fr": "Colis d'e-commerce international",
        "origin_country_ar": "دولي",
        "origin_country_fr": "International",
        "origin_flag": "🌐",
        "destination_flag": "🇩🇿",
        "badge_color": "zinc",
        "typical_days": "15 - 30 يوم",
        "desc_ar": "رقم تتبع قياسي للشحنات المتجهة إلى الجزائر، يدعم المتابعة المباشرة عبر محركات التتبع العالمية.",
        "desc_fr": "Numéro de suivi standard compatible avec les plateformes de suivi internationales."
    }


def get_direct_tracking_links(num: str) -> Dict[str, str]:
    """Generate verified direct portal links for deep tracking with 17TRACK and Postal Ninja."""
    cleaned = sanitize_tracking_number(num)
    return {
        "track17": f"https://t.17track.net/ar#nums={cleaned}",
        "track17_en": f"https://t.17track.net/en#nums={cleaned}",
        "postal_ninja": f"https://postal.ninja/ar/track/{cleaned}",
        "postal_ninja_en": f"https://postal.ninja/en/track/{cleaned}",
        "cainiao": f"https://global.cainiao.com/detail.html?mailNoList={cleaned}",
        "parcels_app": f"https://parcelsapp.com/en/tracking/{cleaned}",
        "algerie_poste": f"https://t.17track.net/ar#nums={cleaned}&fc=100071"
    }


async def query_cainiao_api(num: str, timeout: float = 4.0) -> Dict[str, Any]:
    """Query Cainiao's public free tracking endpoint without API key."""
    cleaned = sanitize_tracking_number(num)
    url = f"https://global.cainiao.com/global/detail.json?mailNos={cleaned}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
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
                        first_desc = events[0]["description"].lower()
                        if any(w in first_desc for w in ["delivered", "livré", "تم التسليم", "pickup", "pick up"]):
                            status_label = "delivered"
                        elif any(w in first_desc for w in ["customs", "douane", "جمارك", "import clearance"]):
                            status_label = "customs"
                        elif any(w in first_desc for w in ["arrived at destination", "arrivée", "algeria", "alger", "ctn"]):
                            status_label = "in_destination_country"
                        elif any(w in first_desc for w in ["departed country of origin", "en vol", "handed over", "airline", "flight"]):
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
        "status_stage": status_label if events else "registered_awaiting_scan"
    }


async def track_algeria_parcel(raw_num: str) -> Dict[str, Any]:
    """
    World-class tracking coordinator for Algerian AliExpress shoppers.
    Detects carrier, sending country, postal class, milestones, and provides
    smart reassuring guidance when a parcel was newly issued by seller.
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
    cainiao_data = await query_cainiao_api(cleaned, timeout=3.5)

    status_stage = cainiao_data["status_stage"]

    # If no physical scan recorded yet (like user's freshly created parcel)
    is_fresh_awaiting_scan = not cainiao_data["success"]

    # 5 Milestone Algerian e-commerce delivery journey
    algeria_delivery_stages = [
        {
            "step": 1,
            "title_ar": "انطلاق وتجهيز الشحنة",
            "title_fr": "Expédition de l'entrepôt",
            "desc_ar": "تم إصدار بوليصة الشحن وتجهيز الطرد في مستودع البائع.",
            "desc_fr": "Bordereau créé et colis préparé en entrepôt.",
            "completed": True,
            "active": is_fresh_awaiting_scan or status_stage == "in_transit"
        },
        {
            "step": 2,
            "title_ar": "الشحن الجوي والترانزيت الدولي",
            "title_fr": "Transit aérien international",
            "desc_ar": "رحلة الشحن الجوي عبر شبكة التبادل البريدي الدولي نحو الجزائر.",
            "desc_fr": "Acheminement aérien international vers l'Algérie.",
            "completed": status_stage in ["in_flight", "in_destination_country", "customs", "delivered"],
            "active": status_stage == "in_flight"
        },
        {
            "step": 3,
            "title_ar": "مركز الفرز الوطني CTN الجزائر",
            "title_fr": "Centre National de Tri (CTN Alger)",
            "desc_ar": "وصول الطرد لمطار هواري بومدين وتسجيله بمركز الفرز البريدي.",
            "desc_fr": "Arrivée à l'aéroport Houari Boumediene et tri postal.",
            "completed": status_stage in ["in_destination_country", "customs", "delivered"],
            "active": status_stage == "in_destination_country"
        },
        {
            "step": 4,
            "title_ar": "الرقابة والمعالجة الجمركية",
            "title_fr": "Dédouanement douanier",
            "desc_ar": "فحص الطرد ومعاينته (معفى من الرسوم للطرود الشخصية والعائلية).",
            "desc_fr": "Contrôle douanier (exonéré pour colis personnels non commerciaux).",
            "completed": status_stage in ["customs", "delivered"],
            "active": status_stage == "customs"
        },
        {
            "step": 5,
            "title_ar": "مكتب بريد بلديتك (جاهز للاستلام)",
            "title_fr": "Bureau de poste local (Prêt)",
            "desc_ar": "استلام الطرد من مكتب البريد المحلي ببطاقة التعريف الوطنية.",
            "desc_fr": "Retrait du colis au bureau de poste avec pièce d'identité.",
            "completed": status_stage == "delivered",
            "active": status_stage == "delivered"
        }
    ]

    # Friendly human-readable advice for Algerian buyer
    if is_fresh_awaiting_scan:
        advice_title_ar = "الشحنة مسجلة حديثاً — بانتظار أول فحص فيزيائي لدى الناقل"
        advice_title_fr = "Numéro généré — En attente du premier scan physique"
        advice_body_ar = (
            f"تم حجز بوليصة الشحن بنجاح من قِبل البائع عبر {carrier['name_ar']}. "
            "في التجارة الدولية، يستغرق استلام شركة الشحن للطرد وتسجيل أول محطة فحص فعلية (First Physical Scan) "
            "بين 24 إلى 72 ساعة. لا تقلق، شحنتك تسير وفق المسار الطبيعي."
        )
        advice_body_fr = (
            f"Le numéro d'expédition a été créé par le vendeur via {carrier['name_fr']}. "
            "Le premier enregistrement physique dans le centre de tri apparaît généralement sous 24 à 72 heures."
        )
    elif status_stage == "in_destination_country":
        advice_title_ar = "وصل الطرد إلى الجزائر! 🇩🇿"
        advice_title_fr = "Le colis est arrivé en Algérie ! 🇩🇿"
        advice_body_ar = "الطرد الآن بمركز الفرز الوطني (CTN مطار هواري بومدين) وسيتم تحويله إلى مكتب بريد ولايتك وبلديتك خلال 2-4 أيام عمل."
        advice_body_fr = "Le colis est au Centre National de Tri (CTN Alger). Il sera acheminé vers votre bureau de poste local sous 2 à 4 jours."
    elif status_stage == "delivered":
        advice_title_ar = "الطرد جاهز للاستلام أو تم تسليمه 🎉"
        advice_title_fr = "Colis prêt au retrait ou livré 🎉"
        advice_body_ar = "يمكنك التوجه إلى مكتب بريد بلديتك مصحوباً ببطاقة التعريف الوطنية لدفع الرسم الرمزي واستلام طردك."
        advice_body_fr = "Présentez-vous à votre bureau de poste avec votre pièce d'identité pour retirer le colis."
    else:
        advice_title_ar = "الشحنة في مسار العبور الدولي ✈️"
        advice_title_fr = "Colis en cours d'acheminement international ✈️"
        advice_body_ar = "الطرد في رحلة الترانزيت الجوي وسيمر عبر التبادل البريدي الدولي قبل وصوله إلى الجزائر."
        advice_body_fr = "Le colis est en transit aérien international avant sa remise à Algérie Poste."

    return {
        "ok": True,
        "tracking_number": cleaned,
        "carrier": carrier,
        "is_fresh_awaiting_scan": is_fresh_awaiting_scan,
        "has_live_checkpoints": cainiao_data["success"],
        "live_checkpoints": cainiao_data["events"],
        "latest_event": cainiao_data["latest_event"],
        "status_stage": status_stage,
        "delivery_stages": algeria_delivery_stages,
        "advice": {
            "title_ar": advice_title_ar,
            "title_fr": advice_title_fr,
            "body_ar": advice_body_ar,
            "body_fr": advice_body_fr
        },
        "portal_links": direct_links,
        "direct_links": direct_links,
        "source_provider": {
            "name": "17TRACK & Cainiao Global",
            "name_ar": "17TRACK والشبكة البريدية الدولية",
            "name_fr": "17TRACK & Réseau Postal International",
            "url": "https://t.17track.net/ar",
            "direct_url": direct_links.get("track17"),
            "flag": "🌐"
        },
        "checked_at": datetime.now(timezone.utc).isoformat()
    }

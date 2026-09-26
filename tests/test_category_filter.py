import pytest
from app.aliexpress.parser import is_allowed_category

def test_cables_and_power_allowed():
    """Verify that cables, USB-C, Type-C, chargers, and GaN power are 100% allowed."""
    cases = [
        ("Baseus 100W USB-C to USB-C Fast Charging Cable", "سلك شحن سريع تايب سي"),
        ("Ugreen 65W GaN Charger 3-Port Fast Wall Charger", "شاحن يوجرين جان 65 واط"),
        ("Toocki 1m USB C Cable PD 60W", "كابل يو اس بي تايب سي"),
        ("Anker Power Bank 20000mAh Portable Charger", "باور بانك انكر سعة 20000"),
        ("Baseus 7 in 1 USB C Hub Docking Station HDMI RJ45", "محول هاب وموزع تايب سي"),
    ]
    for title, text in cases:
        allowed, reason = is_allowed_category(title, text)
        assert allowed is True, f"Failed for '{title}': {reason}"

def test_storage_and_drives_allowed():
    """Verify that SSD, HDD, NVMe, SATA, flash drives, and memory cards are 100% allowed."""
    cases = [
        ("SomnAmbulist SATA3 SSD 120GB 240GB 480GB", "قرص صلب اس اس دي ساتا"),
        ("KingSpec NVMe M.2 SSD 1TB PCIe 4.0", "هارد ديسك ان في ام اي"),
        ("SanDisk Micro SD Card 128GB TF Card High Speed", "بطاقة ذاكرة فلاشة"),
        ("Seagate 2TB 2.5 HDD Hard Drive for Laptop", "قرص صلب 2 تيرا للابتوب"),
        ("Netac USB 3.0 Flash Drive 64GB Pen Drive", "فلاش ديسك 64 جيجا"),
    ]
    for title, text in cases:
        allowed, reason = is_allowed_category(title, text)
        assert allowed is True, f"Failed for '{title}': {reason}"

def test_tools_and_drivers_allowed():
    """Verify that screwdrivers, drills, rotary tools, and repair kits are 100% allowed."""
    cases = [
        ("TUNGFULL Cordless Mini Rotary Tool Kit USB Rechargeable Grinder Pen Set For DIY", "دريل ومفك ادوات صيانة"),
        ("Xiaomi Wiha 24 in 1 Precision Screwdriver Set", "طقم مفكات دقيقة شاومي"),
        ("Electric Screwdriver Cordless Power Driver with Bits", "مفك كهربائي لاسلكي"),
        ("Soldering Iron Kit 60W Adjustable Temperature", "كاوية لحام الكترونيات"),
    ]
    for title, text in cases:
        allowed, reason = is_allowed_category(title, text)
        assert allowed is True, f"Failed for '{title}': {reason}"

def test_cooling_and_pc_parts_allowed():
    """Verify that thermal paste, thermal putty, fans, and PC components are 100% allowed."""
    cases = [
        ("Honeywell PTM7950 8.5W/mK Phase Change Thermal Pad", "وسادة حرارية ومعجون"),
        ("Thermalright Peerless Assassin 120 SE CPU Cooler", "مشتت حراري مروحة تبريد"),
        ("CUSU Ram DDR4 8GBx2 3200MHz", "رامات دي دي ار 4 للكمبيوتر"),
        ("Upsiren U6 PRO Thermal Putty 20W", "بوتي حراري للتبريد"),
    ]
    for title, text in cases:
        allowed, reason = is_allowed_category(title, text)
        assert allowed is True, f"Failed for '{title}': {reason}"

def test_monitored_channels_always_accepted():
    """Verify that all 6 monitored channels pass the category filter automatically."""
    monitored = ["pcgamingpart", "bnddeals", "zedstoreonline", "aniscoupons", "ecksdeal", "lodydeals"]
    for ch in monitored:
        allowed, reason = is_allowed_category("Tech item", "Tech description", channel_username=ch)
        assert allowed is True, f"Channel @{ch} should be allowed: {reason}"

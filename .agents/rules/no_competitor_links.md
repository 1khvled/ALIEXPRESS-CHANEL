---
trigger: always_on
description: Absolute rule forbidding any competitor affiliate links, handles, or unauthorized bots on our channels.
---

# NEVER Put a Competitor Link on Our Channels

1. **Channels Protected**: `@DzAliexpress0` and `@francedealsdz`.
2. **Forbidden Competitor Links**:
   - Competitor shortlinks (e.g. `_c38iyTZR` or any shortcode from ESK, Lody, Zed, Anis, etc.).
   - Competitor tracking parameters (`aff_fcid` other than our tracking ID `dzkhvled16`).
   - Competitor Telegram usernames or `t.me` links (`@ECKSDEAL`, `@lodydeals`, `@zedstoreonline`, etc.).
   - Unauthorized external bots (only `@Alilo07BOT` is permitted).
3. **Monetization Requirement**:
   - ALL links published to our channels MUST be generated via Portals API or Direct tracked URL with tracking ID `dzkhvled16`.
4. **Firewall Enforcement**:
   - `check_competitor_contamination()` in `app/aliexpress/urls.py` enforces this rule across validators and publishers.

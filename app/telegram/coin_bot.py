"""
AliExpress Coin & Discount Bot - Unified Integration
Re-exports functionality from api.coin_bot with support for both polling and webhook modes.
"""
from api.coin_bot import (
    handle_update,
    handle_update as handle_telegram_update,
    publish_deal_to_channel,
    generate_coin_discount_response,
    resolve_any_ali_link,
    get_live_usdt_rate,
    is_admin,
    send_msg,
    send_photo,
)

__all__ = [
    "handle_update",
    "handle_telegram_update",
    "publish_deal_to_channel",
    "generate_coin_discount_response",
    "resolve_any_ali_link",
    "get_live_usdt_rate",
    "is_admin",
    "send_msg",
    "send_photo",
]

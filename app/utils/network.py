import socket
import logging

logger = logging.getLogger(__name__)

_ipv4_enforced = False

def enforce_ipv4():
    """
    Forces socket.getaddrinfo to resolve IPv4 addresses first.
    Eliminates Windows and dual-stack ISP connection drops/timeouts when contacting
    Telegram Bot API, GitHub, AliExpress Portals API, and Telegram web scrape targets.
    """
    global _ipv4_enforced
    if _ipv4_enforced:
        return

    old_getaddrinfo = socket.getaddrinfo

    def getaddrinfo_v4(host, port, family=0, type=0, proto=0, flags=0):
        # Force AF_INET (IPv4) instead of AF_UNSPEC / AF_INET6
        return old_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)

    socket.getaddrinfo = getaddrinfo_v4
    _ipv4_enforced = True
    logger.info("Enforced IPv4 networking for robust Telegram and AliExpress API connectivity.")

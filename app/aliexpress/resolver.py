import asyncio
import re
from dataclasses import dataclass
from typing import Optional
import httpx
from app.aliexpress.urls import (
    is_aliexpress_url,
    is_potential_shortener,
    extract_product_id_from_url,
    normalize_aliexpress_url
)
from app.utils.logger import logger
from app.utils.network import enforce_ipv4

enforce_ipv4()

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

@dataclass
class ResolvedUrlResult:
    original_url: str
    final_url: str
    canonical_url: str
    product_id: Optional[str]
    is_valid: bool
    status_code: Optional[int] = None
    error: Optional[str] = None

class UrlResolver:
    def __init__(self, timeout: float = 20.0, max_redirects: int = 8):
        self.timeout = timeout
        self.max_redirects = max_redirects
        self.headers = {
            "User-Agent": DEFAULT_USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
        }

    async def resolve(self, url: str) -> ResolvedUrlResult:
        """
        Follows redirects for short links and resolves canonical product URL and product_id.
        """
        if not url:
            return ResolvedUrlResult(
                original_url=url,
                final_url=url,
                canonical_url=url,
                product_id=None,
                is_valid=False,
                error="Empty URL"
            )

        # Quick check if it's already a direct AliExpress canonical item URL
        product_id = extract_product_id_from_url(url)
        if product_id and not is_potential_shortener(url) and "s.click" not in url and "a.aliexpress" not in url:
            canonical = normalize_aliexpress_url(url, product_id)
            return ResolvedUrlResult(
                original_url=url,
                final_url=url,
                canonical_url=canonical,
                product_id=product_id,
                is_valid=True,
                status_code=200
            )

        # Needs network resolution for short links, redirects, or app share links
        try:
            # 1. Fast-path: probe redirects step-by-step using Location headers (avoids heavy page loads & timeouts)
            async with httpx.AsyncClient(
                headers=self.headers,
                follow_redirects=False,
                timeout=8.0,
                verify=False
            ) as fast_client:
                curr_url = url
                for _ in range(self.max_redirects):
                    try:
                        resp = await fast_client.get(curr_url)
                    except Exception:
                        break
                    loc = resp.headers.get("location") or resp.headers.get("Location")
                    if not loc:
                        break
                    if loc.startswith("/"):
                        from urllib.parse import urljoin
                        loc = urljoin(curr_url, loc)
                    found_id = extract_product_id_from_url(loc)
                    if found_id:
                        canonical = normalize_aliexpress_url(loc, found_id)
                        return ResolvedUrlResult(
                            original_url=url,
                            final_url=loc,
                            canonical_url=canonical,
                            product_id=found_id,
                            is_valid=True,
                            status_code=resp.status_code
                        )
                    curr_url = loc
        except Exception as fast_err:
            logger.debug(f"Fast URL resolution probe for {url}: {fast_err}")

        try:
            async with httpx.AsyncClient(
                headers=self.headers,
                follow_redirects=True,
                max_redirects=self.max_redirects,
                timeout=self.timeout,
                verify=False
            ) as client:
                response = await client.get(url)
                final_url = str(response.url)
                status_code = response.status_code

                # 1. Check all intermediate redirect URLs & Location headers in history
                found_id = None
                for h in response.history:
                    found_id = extract_product_id_from_url(str(h.url))
                    if found_id:
                        break
                    h_loc = h.headers.get("location") or h.headers.get("Location")
                    if h_loc:
                        found_id = extract_product_id_from_url(h_loc)
                        if found_id:
                            break

                # 2. Extract product id from the final destination URL
                if not found_id:
                    found_id = extract_product_id_from_url(final_url)

                # 3. Sometimes AliExpress mobile page contains canonical link in html or JS redirect
                if not found_id and response.text:
                    m_html = re.search(r'href=[\'"][^\'"]*aliexpress\.com/item/(\d{10,18})\.html', response.text[:30000], re.IGNORECASE)
                    if m_html:
                        found_id = m_html.group(1)
                    else:
                        m_json = re.search(r'[\'"]productId[\'"]\s*:\s*[\'"]?(\d{10,18})[\'"]?', response.text[:30000], re.IGNORECASE)
                        if m_json:
                            found_id = m_json.group(1)

                canonical = normalize_aliexpress_url(final_url, found_id) if found_id else final_url
                is_valid = bool(found_id or is_aliexpress_url(final_url))

                return ResolvedUrlResult(
                    original_url=url,
                    final_url=final_url,
                    canonical_url=canonical,
                    product_id=found_id,
                    is_valid=is_valid,
                    status_code=status_code
                )
        except Exception as e:
            logger.warning(f"URL resolution error for {url}: {e}")
            # If resolution timed out or errored, attempt static extraction
            fallback_id = extract_product_id_from_url(url)
            return ResolvedUrlResult(
                original_url=url,
                final_url=url,
                canonical_url=normalize_aliexpress_url(url, fallback_id) if fallback_id else url,
                product_id=fallback_id,
                is_valid=bool(fallback_id or is_aliexpress_url(url)),
                error=str(e)
            )

# Global singleton resolver
url_resolver = UrlResolver()

import secrets
import string
from typing import Optional, Tuple
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.settings import settings
from app.db.models import Deal, RedirectLink, ClickEvent

def generate_short_slug(length: int = 6) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))

class RedirectService:
    async def create_or_get_redirect(
        self,
        session: AsyncSession,
        deal: Deal,
        affiliate_url: str
    ) -> RedirectLink:
        """Creates or retrieves a unique tracking redirect link for a deal."""
        query = select(RedirectLink).where(RedirectLink.deal_id == deal.id)
        result = await session.execute(query)
        existing = result.scalar_one_or_none()
        if existing:
            return existing

        # Generate unique slug
        for _ in range(5):
            slug = generate_short_slug(6)
            slug_check = await session.execute(select(RedirectLink).where(RedirectLink.slug == slug))
            if not slug_check.scalar_one_or_none():
                break

        link = RedirectLink(
            deal_id=deal.id,
            slug=slug,
            target_url=affiliate_url
        )
        session.add(link)
        await session.flush()
        return link

    def get_public_url(self, slug: str) -> str:
        """Returns the public short URL e.g. http://localhost:8000/d/ABC123"""
        base = settings.PUBLIC_BASE_URL.rstrip("/")
        return f"{base}/d/{slug}"

    async def record_click(
        self,
        session: AsyncSession,
        slug: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        referer: Optional[str] = None
    ) -> Optional[str]:
        """
        Increments click counter, records click event metadata, and returns target redirect URL.
        """
        query = select(RedirectLink).where(RedirectLink.slug == slug)
        res = await session.execute(query)
        link = res.scalar_one_or_none()

        if not link:
            return None

        # Log click event
        click = ClickEvent(
            redirect_id=link.id,
            ip_address=ip_address,
            user_agent=user_agent,
            referer=referer
        )
        session.add(click)

        # Increment count
        link.clicks_count += 1
        await session.commit()

        return link.target_url

redirect_service = RedirectService()

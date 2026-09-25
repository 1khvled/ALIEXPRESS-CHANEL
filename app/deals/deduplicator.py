import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.settings import settings
from app.db.models import Deal, SourceMessage
from app.utils.logger import logger

class DeduplicationEngine:
    def __init__(self, cooldown_hours: Optional[int] = None):
        self.cooldown_hours = cooldown_hours or settings.DUPLICATE_COOLDOWN_HOURS

    def make_content_hash(self, title: str, product_id: str) -> str:
        """Computes content hash for title + product_id."""
        normalized = f"{(title or '').lower().strip()}:{(product_id or '').strip()}"
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

    async def is_duplicate(
        self,
        session: AsyncSession,
        product_id: Optional[str],
        normalized_url: Optional[str],
        title: Optional[str] = None
    ) -> Tuple[bool, Optional[str]]:
        """
        Runs multi-layer duplicate checks against past published/approved deals.
        Returns (is_duplicate: bool, reason: str).
        """
        cooldown_cutoff = datetime.now(timezone.utc) - timedelta(hours=self.cooldown_hours)

        # Layer 1: Product ID duplicate within cooldown window
        if product_id:
            query = select(Deal).where(
                and_(
                    Deal.product_id == product_id,
                    Deal.status.in_(["PUBLISHED", "APPROVED", "PENDING_REVIEW"]),
                    Deal.created_at >= cooldown_cutoff
                )
            ).limit(1)
            result = await session.execute(query)
            existing = result.scalar_one_or_none()
            if existing:
                return True, f"Duplicate product_id '{product_id}' posted within {self.cooldown_hours}h (Deal #{existing.id})"

        # Layer 2: Normalized URL duplicate within cooldown window
        if normalized_url:
            query = select(Deal).where(
                and_(
                    Deal.normalized_url == normalized_url,
                    Deal.status.in_(["PUBLISHED", "APPROVED", "PENDING_REVIEW"]),
                    Deal.created_at >= cooldown_cutoff
                )
            ).limit(1)
            result = await session.execute(query)
            existing = result.scalar_one_or_none()
            if existing:
                return True, f"Duplicate normalized URL posted within {self.cooldown_hours}h (Deal #{existing.id})"

        # Layer 3: Title + Product ID match
        if title and product_id:
            # Query similar deals
            query = select(Deal).where(
                and_(
                    Deal.product_id == product_id,
                    Deal.title.ilike(f"%{title[:30]}%"),
                    Deal.created_at >= cooldown_cutoff
                )
            ).limit(1)
            result = await session.execute(query)
            existing = result.scalar_one_or_none()
            if existing:
                return True, f"Duplicate title & product ID found within cooldown window (Deal #{existing.id})"

        return False, None

deduplicator = DeduplicationEngine()

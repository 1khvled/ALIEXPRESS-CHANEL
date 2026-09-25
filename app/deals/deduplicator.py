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
        Enforces global cross-channel deduplication so that if any channel posts
        the same product, it is never repeated.
        """
        conditions_time = []
        if not settings.NEVER_REPEAT_DUPLICATES:
            cooldown_cutoff = datetime.now(timezone.utc) - timedelta(hours=self.cooldown_hours)
            conditions_time.append(Deal.created_at >= cooldown_cutoff)

        active_statuses = ["PUBLISHED", "APPROVED", "PENDING_REVIEW"]

        # Layer 1: Global Product ID duplicate (same product from ANY channel)
        if product_id:
            where_clause = [Deal.product_id == product_id, Deal.status.in_(active_statuses)] + conditions_time
            query = select(Deal).where(and_(*where_clause)).limit(1)
            result = await session.execute(query)
            existing = result.scalar_one_or_none()
            if existing:
                return True, f"Duplicate product_id '{product_id}' already posted from source (Deal #{existing.id})"

        # Layer 2: Global Normalized URL duplicate
        if normalized_url:
            where_clause = [Deal.normalized_url == normalized_url, Deal.status.in_(active_statuses)] + conditions_time
            query = select(Deal).where(and_(*where_clause)).limit(1)
            result = await session.execute(query)
            existing = result.scalar_one_or_none()
            if existing:
                return True, f"Duplicate product URL already exists (Deal #{existing.id})"

        # Layer 3: Title + Product ID match
        if title and product_id:
            where_clause = [
                Deal.product_id == product_id,
                Deal.title.ilike(f"%{title[:30]}%"),
                Deal.status.in_(active_statuses)
            ] + conditions_time
            query = select(Deal).where(and_(*where_clause)).limit(1)
            result = await session.execute(query)
            existing = result.scalar_one_or_none()
            if existing:
                return True, f"Duplicate deal with matching title & product ID (Deal #{existing.id})"

        return False, None

deduplicator = DeduplicationEngine()

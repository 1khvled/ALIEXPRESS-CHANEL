import pytest
import pytest_asyncio
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.db.models import Base, Deal
from app.deals.deduplicator import DeduplicationEngine

@pytest_asyncio.fixture
async def async_test_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with session_maker() as session:
        yield session

    await engine.dispose()

@pytest.mark.asyncio
async def test_deduplication_engine(async_test_session):
    dedup = DeduplicationEngine(cooldown_hours=24)

    # Insert an existing published deal
    existing_deal = Deal(
        product_id="1005009999999",
        original_url="https://aliexpress.com/item/1005009999999.html",
        normalized_url="https://www.aliexpress.com/item/1005009999999.html",
        title="Gaming Headset 7.1",
        status="PUBLISHED",
        created_at=datetime.now(timezone.utc)
    )
    async_test_session.add(existing_deal)
    await async_test_session.commit()

    # Test duplicate product ID
    is_dup, reason = await dedup.is_duplicate(
        session=async_test_session,
        product_id="1005009999999",
        normalized_url="https://www.aliexpress.com/item/1005009999999.html",
        title="Gaming Headset 7.1"
    )
    assert is_dup is True
    assert "1005009999999" in reason

    # Test non-duplicate product ID
    is_not_dup, reason2 = await dedup.is_duplicate(
        session=async_test_session,
        product_id="1005008888888",
        normalized_url="https://www.aliexpress.com/item/1005008888888.html",
        title="Different Product"
    )
    assert is_not_dup is False
    assert reason2 is None

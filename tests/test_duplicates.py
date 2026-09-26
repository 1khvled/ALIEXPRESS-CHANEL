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

@pytest.mark.asyncio
async def test_cross_channel_duplicate_detection():
    """Verifies that deals already posted from another channel are strictly blocked."""
    from app.publisher.state_tracker import is_product_already_published, record_product_published, is_same_deal_title

    # 1. Title matching works across channels
    assert is_same_deal_title("realme P3 5G 8GB+256GB", "Realme P3") is True
    assert is_same_deal_title("Attack Shark X3 Pro 8K", "ماوس Attack Shark X3 Pro") is True
    assert is_same_deal_title("Attack Shark R1", "Attack Shark X3 Pro") is False

    # 2. State-level deduplication blocks reposts
    record_product_published("999111222", "Test Wireless Gaming Mouse X1")
    is_dup, reason = await is_product_already_published("999111222", "Test Wireless Gaming Mouse X1")
    assert is_dup is True
    assert "already in persistent" in reason

    # 3. Different channel posting the same product by title is blocked
    is_dup_title, reason_title = await is_product_already_published("888333444", "ماوس ألعاب Wireless Gaming Mouse X1")
    assert is_dup_title is True
    assert "matches previously published" in reason_title


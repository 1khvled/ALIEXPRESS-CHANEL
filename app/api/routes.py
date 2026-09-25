from datetime import datetime, timezone, timedelta
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel
from sqlalchemy import select, func, desc, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import settings
from app.db.session import get_db, db_context
from app.db.models import (
    Deal,
    Channel,
    SourceMessage,
    GeneratedPost,
    TelegramPost,
    RedirectLink,
    ClickEvent,
    SystemLog
)
from app.deals.processor import deal_processor
from app.aliexpress.product import product_extractor
from app.ai.generator import caption_generator
from app.analytics.redirect import redirect_service
from app.publisher.publisher import telegram_publisher
from app.jobs.monitor import monitor_cycle

api_router = APIRouter()

# -------------------------------------------------------------
# 1. Health Endpoint (Section 50)
# -------------------------------------------------------------
@api_router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    db_status = "ok"
    try:
        await db.execute(select(1))
    except Exception as e:
        db_status = f"error: {e}"

    return {
        "status": "ok" if db_status == "ok" else "degraded",
        "database": db_status,
        "publish_mode": settings.PUBLISH_MODE,
        "target_channel": settings.TARGET_CHANNEL_ID or "unconfigured",
        "poll_interval_seconds": settings.POLL_INTERVAL_SECONDS,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

# -------------------------------------------------------------
# 2. Redirect Tracking Endpoint (Section 13)
# -------------------------------------------------------------
@api_router.get("/d/{slug}")
async def redirect_to_deal(slug: str, request: Request, db: AsyncSession = Depends(get_db)):
    ip = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    referer = request.headers.get("referer")

    target_url = await redirect_service.record_click(
        session=db,
        slug=slug,
        ip_address=ip,
        user_agent=user_agent,
        referer=referer
    )

    if not target_url:
        raise HTTPException(status_code=404, detail="Deal link not found or expired")

    return RedirectResponse(url=target_url, status_code=302)

# -------------------------------------------------------------
# 3. Stats & Metrics Endpoint (Section 25 & 36)
# -------------------------------------------------------------
@api_router.get("/api/stats")
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)):
    now = datetime.now(timezone.utc)
    today_start = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)

    # Today's stats
    total_detected = (await db.execute(
        select(func.count(Deal.id)).where(Deal.created_at >= today_start)
    )).scalar() or 0

    total_published = (await db.execute(
        select(func.count(Deal.id)).where(
            and_(Deal.status == "PUBLISHED", Deal.created_at >= today_start)
        )
    )).scalar() or 0

    pending_review = (await db.execute(
        select(func.count(Deal.id)).where(Deal.status == "PENDING_REVIEW")
    )).scalar() or 0

    total_skipped = (await db.execute(
        select(func.count(Deal.id)).where(
            and_(Deal.status.in_(["SKIPPED", "REJECTED"]), Deal.created_at >= today_start)
        )
    )).scalar() or 0

    total_clicks = (await db.execute(
        select(func.count(ClickEvent.id)).where(ClickEvent.created_at >= today_start)
    )).scalar() or 0

    enabled_channels = (await db.execute(
        select(func.count(Channel.id)).where(Channel.enabled == True)
    )).scalar() or 0

    return {
        "today": {
            "detected": total_detected,
            "published": total_published,
            "pending_review": pending_review,
            "skipped_or_rejected": total_skipped,
            "clicks": total_clicks
        },
        "system": {
            "enabled_channels": enabled_channels,
            "publish_mode": settings.PUBLISH_MODE,
            "cooldown_minutes": settings.COOLDOWN_MINUTES,
            "min_quality_score": settings.MIN_QUALITY_SCORE
        }
    }

# -------------------------------------------------------------
# 4. Deals Management Endpoints
# -------------------------------------------------------------
@api_router.get("/api/deals")
async def list_deals(
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    query = select(Deal).order_by(desc(Deal.id))
    if status and status != "ALL":
        query = query.where(Deal.status == status)

    query = query.offset(offset).limit(limit)
    res = await db.execute(query)
    deals = res.scalars().all()

    items = []
    for d in deals:
        # Load generated caption if exists
        post_q = select(GeneratedPost).where(GeneratedPost.deal_id == d.id).order_by(desc(GeneratedPost.id)).limit(1)
        post = (await db.execute(post_q)).scalar_one_or_none()

        items.append({
            "id": d.id,
            "product_id": d.product_id,
            "title": d.title,
            "current_price": d.current_price,
            "current_price_eur": d.current_price_eur,
            "coupon_code": d.coupon_code,
            "has_points_discount": d.has_points_discount,
            "image_url": d.image_url,
            "quality_score": d.quality_score,
            "status": d.status,
            "rejection_reason": d.rejection_reason,
            "original_url": d.original_url,
            "affiliate_url": d.affiliate_url,
            "caption": post.caption if post else None,
            "created_at": d.created_at.isoformat() if d.created_at else None
        })

    return items

@api_router.post("/api/deals/{deal_id}/approve")
async def approve_deal(deal_id: int, db: AsyncSession = Depends(get_db)):
    deal = (await db.execute(select(Deal).where(Deal.id == deal_id))).scalar_one_or_none()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    # Fetch latest generated post or generate
    post_q = select(GeneratedPost).where(GeneratedPost.deal_id == deal.id).order_by(desc(GeneratedPost.id)).limit(1)
    post = (await db.execute(post_q)).scalar_one_or_none()

    caption = post.caption if post else f"تخفيض لـ {deal.title}\nالسعر : {deal.current_price}$ ({deal.current_price_eur}€)🔥"
    img_path = deal.local_image_path or (post.image_path if post else None)

    from pathlib import Path
    image_file = Path(img_path) if img_path else None

    # Publish forced
    success, err = await telegram_publisher.publish_deal(
        session=db,
        deal=deal,
        caption=caption,
        image_path=image_file,
        force=True
    )

    if not success:
        raise HTTPException(status_code=500, detail=f"Publish failed: {err}")

    deal.status = "PUBLISHED"
    await db.commit()
    return {"status": "ok", "message": f"Deal #{deal_id} approved and published"}

@api_router.post("/api/deals/{deal_id}/reject")
async def reject_deal(deal_id: int, db: AsyncSession = Depends(get_db)):
    deal = (await db.execute(select(Deal).where(Deal.id == deal_id))).scalar_one_or_none()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    deal.status = "REJECTED"
    deal.rejection_reason = "Rejected manually by admin"
    await db.commit()
    return {"status": "ok", "message": f"Deal #{deal_id} marked as rejected"}

@api_router.post("/api/deals/{deal_id}/retry")
async def retry_deal(deal_id: int, db: AsyncSession = Depends(get_db)):
    deal = (await db.execute(select(Deal).where(Deal.id == deal_id))).scalar_one_or_none()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    success = await deal_processor.pipeline_generate_and_publish(db, deal, force_publish=False)
    return {"status": "ok", "success": success, "current_status": deal.status}

# -------------------------------------------------------------
# 5. Live Test Endpoint (Extract & Caption Preview)
# -------------------------------------------------------------
class TestParseRequest(BaseModel):
    text: str

@api_router.post("/api/test-parse")
async def test_parse_message(payload: TestParseRequest):
    extracted = await product_extractor.extract_from_message(payload.text)
    if not extracted:
        return {"success": False, "error": "No AliExpress link or extractable product found in message"}

    preview_caption = await caption_generator.generate(
        title=extracted.title or "Product Title",
        usd_price=extracted.current_price or 0.0,
        eur_price=extracted.current_price_eur or 0.0,
        affiliate_url="https://s.click.aliexpress.com/e/_SAMPLE",
        coupon_code=extracted.coupon_code,
        has_points_discount=extracted.has_points_discount
    )

    return {
        "success": True,
        "product_id": extracted.product_id,
        "title": extracted.title,
        "current_price": extracted.current_price,
        "current_price_eur": extracted.current_price_eur,
        "coupon_code": extracted.coupon_code,
        "has_points_discount": extracted.has_points_discount,
        "image_url": extracted.image_url,
        "canonical_url": extracted.canonical_url,
        "preview_caption": preview_caption
    }

# -------------------------------------------------------------
# 6. Channel & Admin Controls
# -------------------------------------------------------------
@api_router.get("/api/channels")
async def list_channels(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Channel).order_by(desc(Channel.priority)))
    channels = res.scalars().all()
    return [
        {
            "id": c.id,
            "username": c.username,
            "display_name": c.display_name,
            "enabled": c.enabled,
            "priority": c.priority,
            "last_message_id": c.last_message_id,
            "last_checked_at": c.last_checked_at.isoformat() if c.last_checked_at else None
        }
        for c in channels
    ]

@api_router.post("/api/channels/scan-now")
async def trigger_scan_now():
    import asyncio
    asyncio.create_task(monitor_cycle())
    return {"status": "ok", "message": "Manual collection cycle triggered in background"}

class ModeRequest(BaseModel):
    mode: str

@api_router.post("/api/settings/mode")
async def update_publish_mode(payload: ModeRequest):
    target = payload.mode.lower()
    if target not in ["auto", "approval", "dry_run"]:
        raise HTTPException(status_code=400, detail="Invalid mode. Choose: auto, approval, dry_run")
    settings.PUBLISH_MODE = target
    return {"status": "ok", "publish_mode": settings.PUBLISH_MODE}

@api_router.get("/api/logs")
async def get_recent_logs(limit: int = 50, db: AsyncSession = Depends(get_db)):
    q = select(SystemLog).order_by(desc(SystemLog.id)).limit(limit)
    logs = (await db.execute(q)).scalars().all()
    return [
        {
            "id": l.id,
            "level": l.level,
            "component": l.component,
            "message": l.message,
            "details": l.details,
            "created_at": l.created_at.isoformat() if l.created_at else None
        }
        for l in logs
    ]

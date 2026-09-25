from pathlib import Path
from typing import Optional, Tuple
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.settings import settings
from app.db.models import Deal, SourceMessage, GeneratedPost
from app.aliexpress.resolver import url_resolver
from app.aliexpress.affiliate import affiliate_service
from app.aliexpress.product import product_extractor
from app.deals.deduplicator import deduplicator
from app.deals.scorer import deal_scorer
from app.ai.generator import caption_generator
from app.ai.validator import caption_validator
from app.media.downloader import media_downloader
from app.media.renderer import media_renderer
from app.analytics.redirect import redirect_service
from app.publisher.publisher import telegram_publisher
from app.utils.logger import logger, record_system_log

class DealProcessor:
    async def process_source_message(
        self,
        session: AsyncSession,
        source_message: SourceMessage
    ) -> Optional[Deal]:
        """
        Step 1: Analyzes raw incoming message from a source channel.
        Extracts deal data, checks for duplicates, scores quality, and stores deal record.
        """
        raw_text = source_message.raw_text or ""

        # Extract product details
        extracted = await product_extractor.extract_from_message(
            text=raw_text,
            media_path=source_message.media_path
        )

        if not extracted or not extracted.is_valid:
            return None

        # Check multi-layer deduplication
        is_dup, dup_reason = await deduplicator.is_duplicate(
            session=session,
            product_id=extracted.product_id,
            normalized_url=extracted.canonical_url,
            title=extracted.title
        )

        # Calculate quality score
        score = deal_scorer.score(
            url_valid=extracted.is_valid,
            product_id=extracted.product_id,
            current_price=extracted.current_price,
            title=extracted.title,
            image_url=extracted.image_url,
            has_discount=extracted.has_points_discount,
            coupon_code=extracted.coupon_code
        )

        # Convert to our affiliate link
        affiliate_url = await affiliate_service.create_affiliate_link(
            product_url=extracted.canonical_url,
            product_id=extracted.product_id
        )

        initial_status = "DETECTED"
        rejection_reason = None

        if is_dup:
            initial_status = "SKIPPED"
            rejection_reason = dup_reason
        elif not deal_scorer.is_acceptable(score):
            initial_status = "REJECTED"
            rejection_reason = f"Quality score {score} below minimum {deal_scorer.min_score}"

        deal = Deal(
            source_message_id=source_message.id,
            product_id=extracted.product_id,
            original_url=extracted.original_url,
            normalized_url=extracted.canonical_url,
            affiliate_url=affiliate_url,
            title=extracted.title,
            currency="USD",
            current_price=extracted.current_price,
            current_price_eur=extracted.current_price_eur,
            coupon_code=extracted.coupon_code,
            has_points_discount=extracted.has_points_discount,
            image_url=extracted.image_url,
            quality_score=score,
            status=initial_status,
            rejection_reason=rejection_reason
        )

        session.add(deal)
        await session.commit()
        await session.refresh(deal)

        await record_system_log(
            "INFO",
            "processor",
            f"Deal #{deal.id} created ({deal.status}, score: {score}) for product {extracted.product_id}: {deal.title}"
        )

        # If eligible, proceed to generation pipeline
        if initial_status == "DETECTED":
            await self.pipeline_generate_and_publish(session, deal)

        return deal

    async def pipeline_generate_and_publish(
        self,
        session: AsyncSession,
        deal: Deal,
        force_publish: bool = False
    ) -> bool:
        """
        Steps 2-5: Creates tracking URL, generates caption, validates, prepares media,
        and publishes or queues for manual review depending on PUBLISH_MODE and score.
        """
        try:
            # 1. Tracking redirect URL
            redirect = await redirect_service.create_or_get_redirect(
                session, deal, deal.affiliate_url or deal.normalized_url or deal.original_url
            )
            public_deal_url = redirect_service.get_public_url(redirect.slug)

            # 2. Generate exact Arabic post
            caption = await caption_generator.generate(
                title=deal.title or "AliExpress Deal",
                usd_price=deal.current_price or 0.0,
                eur_price=deal.current_price_eur or 0.0,
                affiliate_url=public_deal_url,
                coupon_code=deal.coupon_code,
                has_points_discount=deal.has_points_discount
            )

            # 3. Validate generated caption
            validation = caption_validator.validate(
                caption=caption,
                expected_title=deal.title or "",
                expected_usd_price=deal.current_price or 0.0,
                expected_eur_price=deal.current_price_eur or 0.0,
                expected_affiliate_url=public_deal_url,
                expected_coupon=deal.coupon_code,
                expected_points=deal.has_points_discount
            )

            # 4. Prepare image
            local_img: Optional[Path] = None
            if deal.image_url:
                downloaded = await media_downloader.download_image(deal.image_url, deal.product_id)
                if downloaded:
                    local_img = media_renderer.prepare_post_image(downloaded, deal.product_id, deal.title)
                    deal.local_image_path = str(local_img)

            if not local_img:
                local_img = media_renderer.prepare_post_image(None, deal.product_id, deal.title)
                deal.local_image_path = str(local_img)

            # Save generated post
            gen_post = GeneratedPost(
                deal_id=deal.id,
                title=deal.title,
                caption=caption,
                image_path=str(local_img) if local_img else None,
                image_url=deal.image_url,
                ai_model=settings.AI_MODEL,
                ai_validation_status="APPROVED" if validation.approved else "FAILED",
                validation_errors=", ".join(validation.errors) if validation.errors else None,
                status="VALIDATED" if validation.approved else "NEEDS_FIX"
            )
            session.add(gen_post)
            await session.commit()

            # Determine whether to publish automatically or queue for approval
            mode = settings.PUBLISH_MODE.lower()
            is_auto_eligible = (
                deal_scorer.is_auto_publishable(deal.quality_score) and
                validation.approved
            )

            if force_publish or (mode == "auto" and is_auto_eligible):
                # Publish
                success, err = await telegram_publisher.publish_deal(
                    session=session,
                    deal=deal,
                    caption=caption,
                    image_path=local_img,
                    force=force_publish
                )
                return success
            elif mode == "dry_run":
                success, err = await telegram_publisher.publish_deal(
                    session=session,
                    deal=deal,
                    caption=caption,
                    image_path=local_img
                )
                return success
            else:
                # APPROVAL mode or quality score requires review
                deal.status = "PENDING_REVIEW"
                await session.commit()
                await record_system_log(
                    "INFO",
                    "processor",
                    f"Deal #{deal.id} queued in PENDING_REVIEW (Publish mode: {mode}, score: {deal.quality_score})"
                )
                return True

        except Exception as e:
            deal.status = "FAILED"
            deal.rejection_reason = str(e)
            await session.commit()
            await record_system_log("ERROR", "processor", f"Pipeline failed for deal #{deal.id}: {e}")
            return False

deal_processor = DealProcessor()

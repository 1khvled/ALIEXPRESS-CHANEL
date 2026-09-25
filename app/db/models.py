from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    String,
    Text,
    Boolean,
    Float,
    Numeric,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    Index
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

def utcnow():
    return datetime.now(timezone.utc)

class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_channel_id = Column(BigInteger, unique=True, nullable=True, index=True)
    username = Column(String(255), unique=True, nullable=False, index=True)
    display_name = Column(String(255), nullable=True)
    enabled = Column(Boolean, default=True, nullable=False)
    priority = Column(Integer, default=50, nullable=False)
    last_message_id = Column(BigInteger, nullable=True, default=0)
    last_checked_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    source_messages = relationship("SourceMessage", back_populates="channel", cascade="all, delete-orphan")


class SourceMessage(Base):
    __tablename__ = "source_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(Integer, ForeignKey("channels.id", ondelete="CASCADE"), nullable=False, index=True)
    telegram_message_id = Column(BigInteger, nullable=False)
    message_url = Column(String(500), nullable=True)
    raw_text = Column(Text, nullable=True)
    media_type = Column(String(50), nullable=True)  # photo, video, document, none
    media_path = Column(String(500), nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=True)
    collected_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("channel_id", "telegram_message_id", name="uq_channel_message"),
        Index("idx_channel_message", "channel_id", "telegram_message_id"),
    )

    channel = relationship("Channel", back_populates="source_messages")
    deals = relationship("Deal", back_populates="source_message", cascade="all, delete-orphan")


class Deal(Base):
    __tablename__ = "deals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_message_id = Column(Integer, ForeignKey("source_messages.id", ondelete="SET NULL"), nullable=True, index=True)

    product_id = Column(String(100), nullable=True, index=True)
    original_url = Column(Text, nullable=False)
    normalized_url = Column(Text, nullable=True, index=True)
    affiliate_url = Column(Text, nullable=True)

    title = Column(Text, nullable=True)
    currency = Column(String(10), default="USD", nullable=False)
    current_price = Column(Float, nullable=True)
    current_price_eur = Column(Float, nullable=True)
    original_price = Column(Float, nullable=True)
    discount_percent = Column(Float, nullable=True)

    coupon_code = Column(String(100), nullable=True)
    has_points_discount = Column(Boolean, default=False, nullable=False)

    rating = Column(Float, nullable=True)
    orders_count = Column(BigInteger, nullable=True)

    image_url = Column(Text, nullable=True)
    local_image_path = Column(String(500), nullable=True)

    quality_score = Column(Integer, default=0, nullable=False)
    status = Column(String(50), default="DETECTED", nullable=False, index=True)
    # Statuses: DETECTED, URL_RESOLVED, AFFILIATE_CREATED, AI_GENERATED, AI_VALIDATED,
    #           PENDING_REVIEW, APPROVED, PUBLISHED, REJECTED, SKIPPED, FAILED
    rejection_reason = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    source_message = relationship("SourceMessage", back_populates="deals")
    generated_posts = relationship("GeneratedPost", back_populates="deal", cascade="all, delete-orphan", lazy="selectin")
    telegram_posts = relationship("TelegramPost", back_populates="deal", cascade="all, delete-orphan", lazy="selectin")
    redirect_link = relationship("RedirectLink", back_populates="deal", uselist=False, cascade="all, delete-orphan", lazy="selectin")


class GeneratedPost(Base):
    __tablename__ = "generated_posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    deal_id = Column(Integer, ForeignKey("deals.id", ondelete="CASCADE"), nullable=False, index=True)

    title = Column(Text, nullable=True)
    caption = Column(Text, nullable=False)

    image_path = Column(String(500), nullable=True)
    image_url = Column(Text, nullable=True)

    ai_model = Column(String(100), nullable=True)
    ai_validation_status = Column(String(50), default="PENDING", nullable=False)
    validation_errors = Column(Text, nullable=True)

    status = Column(String(50), default="DRAFT", nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    deal = relationship("Deal", back_populates="generated_posts")


class TelegramPost(Base):
    __tablename__ = "telegram_posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    deal_id = Column(Integer, ForeignKey("deals.id", ondelete="CASCADE"), nullable=False, index=True)

    telegram_media_id = Column(String(255), nullable=True)
    telegram_message_id = Column(BigInteger, nullable=True)
    channel_id = Column(String(100), nullable=True)
    permalink = Column(String(500), nullable=True)

    status = Column(String(50), nullable=False, default="PUBLISHED")  # PUBLISHED, FAILED
    published_at = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    deal = relationship("Deal", back_populates="telegram_posts")


class RedirectLink(Base):
    __tablename__ = "redirect_links"

    id = Column(Integer, primary_key=True, autoincrement=True)
    deal_id = Column(Integer, ForeignKey("deals.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    slug = Column(String(64), unique=True, nullable=False, index=True)
    target_url = Column(Text, nullable=False)
    clicks_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    deal = relationship("Deal", back_populates="redirect_link")
    clicks = relationship("ClickEvent", back_populates="redirect_link", cascade="all, delete-orphan")


class ClickEvent(Base):
    __tablename__ = "click_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    redirect_id = Column(Integer, ForeignKey("redirect_links.id", ondelete="CASCADE"), nullable=False, index=True)
    ip_address = Column(String(100), nullable=True)
    user_agent = Column(Text, nullable=True)
    referer = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    redirect_link = relationship("RedirectLink", back_populates="clicks")


class SystemLog(Base):
    __tablename__ = "system_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    level = Column(String(20), default="INFO", nullable=False)
    component = Column(String(100), nullable=False, index=True)
    message = Column(Text, nullable=False)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False, index=True)

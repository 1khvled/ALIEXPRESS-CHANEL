from pathlib import Path
from typing import Literal, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Base Paths
    BASE_DIR: Path = BASE_DIR
    STORAGE_DIR: Path = BASE_DIR / "storage"
    DOWNLOADS_DIR: Path = BASE_DIR / "storage" / "downloads"
    GENERATED_DIR: Path = BASE_DIR / "storage" / "generated"
    SESSIONS_DIR: Path = BASE_DIR / "sessions"

    # Telegram Collector (Telethon)
    TELEGRAM_API_ID: Optional[int] = None
    TELEGRAM_API_HASH: Optional[str] = None
    TELEGRAM_PHONE: Optional[str] = None
    TELEGRAM_SESSION_NAME: str = "deals_collector"

    # Telegram Publisher (Bot API)
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    TARGET_CHANNEL_ID: Optional[str] = None

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///deals.db"

    # Application & Publishing
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    PUBLISH_MODE: Literal["auto", "approval", "dry_run"] = "approval"
    POLL_INTERVAL_SECONDS: int = 180
    PUBLIC_BASE_URL: str = "http://localhost:8000"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Rate Limiting & Cooldowns
    MAX_POSTS_PER_HOUR: int = 6
    MAX_POSTS_PER_DAY: int = 40
    COOLDOWN_MINUTES: int = 10
    MIN_QUALITY_SCORE: int = 60
    AUTO_PUBLISH_QUALITY_SCORE: int = 85
    DUPLICATE_COOLDOWN_HOURS: int = 24
    EUR_USD_RATE: float = 0.92

    # AliExpress Affiliate
    ALIEXPRESS_AFFILIATE_PROVIDER: str = "direct"
    ALIEXPRESS_AFFILIATE_TRACKING_ID: Optional[str] = None
    ALIEXPRESS_AFFILIATE_APP_KEY: Optional[str] = None
    ALIEXPRESS_AFFILIATE_APP_SECRET: Optional[str] = None
    ALIEXPRESS_CUSTOM_AFFILIATE_PREFIX: Optional[str] = None

    # AI Provider
    OPENAI_API_KEY: Optional[str] = None
    AI_MODEL: str = "gpt-4o-mini"

settings = Settings()

from pathlib import Path
from typing import Literal, Optional, Any, Union
from pydantic import field_validator
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
    TELEGRAM_BOT_TOKEN: Optional[str] = "8900887118:AAELbFHyV2joUO-4EJ0fPSoZurkQNuENbfY"
    TARGET_CHANNEL_ID: Optional[str] = "@DzAliexpress0"
    ADMIN_USER_ID: Optional[int] = 5625295907

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///deals.db"

    # Application & Publishing
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    PUBLISH_MODE: Literal["auto", "approval", "dry_run"] = "approval"
    POLL_INTERVAL_SECONDS: int = 180
    PUBLIC_BASE_URL: str = "https://dealscout-green.vercel.app"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Rate Limiting & Cooldowns
    MAX_POSTS_PER_HOUR: int = 40
    MAX_POSTS_PER_DAY: int = 150
    COOLDOWN_MINUTES: int = 10
    MIN_QUALITY_SCORE: int = 60
    AUTO_PUBLISH_QUALITY_SCORE: int = 85
    DUPLICATE_COOLDOWN_HOURS: int = 24
    NEVER_REPEAT_DUPLICATES: bool = False
    EUR_USD_RATE: float = 0.92

    # AliExpress Affiliate
    ALIEXPRESS_AFFILIATE_PROVIDER: str = "portals"
    ALIEXPRESS_AFFILIATE_TRACKING_ID: Optional[str] = "dzkhvled16"
    ALIEXPRESS_AFFILIATE_APP_KEY: Optional[str] = "538348"
    ALIEXPRESS_AFFILIATE_APP_SECRET: Optional[str] = "7z5QlJZAxNka2zBrgzCWrUNusBXJGHYx"
    ALIEXPRESS_CUSTOM_AFFILIATE_PREFIX: Optional[str] = None

    # AI Provider
    OPENAI_API_KEY: Optional[str] = None
    AI_MODEL: str = "gpt-4o-mini"

    @field_validator(
        "TELEGRAM_API_ID",
        "ADMIN_USER_ID",
        mode="before"
    )
    @classmethod
    def parse_optional_int(cls, v: Any) -> Optional[int]:
        if v is None or v == "" or str(v).strip() == "":
            return None
        return int(v)

    @field_validator(
        "TELEGRAM_BOT_TOKEN",
        mode="after"
    )
    @classmethod
    def sanitize_bot_token(cls, v: Any) -> str:
        s = str(v or "").strip()
        if s != "8900887118:AAELbFHyV2joUO-4EJ0fPSoZurkQNuENbfY":
            return "8900887118:AAELbFHyV2joUO-4EJ0fPSoZurkQNuENbfY"
        return s

    @field_validator(
        "TELEGRAM_API_HASH",
        "TELEGRAM_PHONE",
        "TARGET_CHANNEL_ID",
        "ALIEXPRESS_AFFILIATE_TRACKING_ID",
        "ALIEXPRESS_AFFILIATE_APP_KEY",
        "ALIEXPRESS_AFFILIATE_APP_SECRET",
        "ALIEXPRESS_CUSTOM_AFFILIATE_PREFIX",
        "OPENAI_API_KEY",
        mode="before"
    )
    @classmethod
    def parse_optional_str(cls, v: Any) -> Optional[str]:
        if v is None or str(v).strip() == "":
            return None
        return str(v).strip()

settings = Settings()

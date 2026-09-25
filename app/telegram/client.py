import os
from pathlib import Path
from typing import Optional
from telethon import TelegramClient
from app.config.settings import settings
from app.utils.logger import logger

class TelegramCollectorClient:
    def __init__(self):
        self.api_id = settings.TELEGRAM_API_ID
        self.api_hash = settings.TELEGRAM_API_HASH
        self.session_name = settings.TELEGRAM_SESSION_NAME
        self.sessions_dir = settings.SESSIONS_DIR
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.session_path = str(self.sessions_dir / self.session_name)
        self._client: Optional[TelegramClient] = None

    def get_client(self) -> Optional[TelegramClient]:
        """Returns the Telethon client instance if credentials are configured."""
        if not (self.api_id and self.api_hash):
            return None

        if self._client is None:
            self._client = TelegramClient(
                self.session_path,
                self.api_id,
                self.api_hash
            )
        return self._client

    async def connect(self) -> bool:
        """Starts client session connection."""
        client = self.get_client()
        if client is None:
            logger.warning("Telegram credentials (TELEGRAM_API_ID / TELEGRAM_API_HASH) are not set.")
            return False

        try:
            if not client.is_connected():
                await client.connect()
            is_auth = await client.is_user_authorized()
            if not is_auth:
                logger.warning(
                    f"Telethon session '{self.session_name}' is not authorized. "
                    "Run 'python scripts/auth_telegram.py' to login with your phone/bot."
                )
                return False
            return True
        except Exception as e:
            logger.error(f"Failed to connect Telethon client: {e}")
            return False

    async def disconnect(self):
        if self._client and self._client.is_connected():
            await self._client.disconnect()

telegram_client_manager = TelegramCollectorClient()

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(slots=True)
class TelegramConfig:
    enabled: bool
    bot_token: str
    chat_id: str


@dataclass(slots=True)
class EmailConfig:
    enabled: bool
    smtp_host: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    smtp_from: str
    smtp_to: str
    smtp_use_tls: bool


@dataclass(slots=True)
class AppConfig:
    sigaa_base_url: str
    request_timeout_seconds: int
    check_interval_seconds: int
    max_retries: int
    backoff_seconds: int
    dry_run: bool
    db_path: str
    telegram: TelegramConfig
    email: EmailConfig
    desktop_notifications_enabled: bool



def _env_bool(key: str, default: bool) -> bool:
    value = os.getenv(key)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}



def load_config() -> AppConfig:
    return AppConfig(
        sigaa_base_url=os.getenv("SIGAA_BASE_URL", "https://sigaa.unb.br"),
        request_timeout_seconds=int(os.getenv("REQUEST_TIMEOUT_SECONDS", "15")),
        check_interval_seconds=int(os.getenv("CHECK_INTERVAL_SECONDS", "120")),
        max_retries=int(os.getenv("MAX_RETRIES", "3")),
        backoff_seconds=int(os.getenv("BACKOFF_SECONDS", "2")),
        dry_run=_env_bool("DRY_RUN", True),
        db_path=os.getenv("DB_PATH", "monitor.db"),
        telegram=TelegramConfig(
            enabled=_env_bool("TELEGRAM_ENABLED", False),
            bot_token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
            chat_id=os.getenv("TELEGRAM_CHAT_ID", ""),
        ),
        email=EmailConfig(
            enabled=_env_bool("EMAIL_ENABLED", False),
            smtp_host=os.getenv("SMTP_HOST", ""),
            smtp_port=int(os.getenv("SMTP_PORT", "587")),
            smtp_username=os.getenv("SMTP_USERNAME", ""),
            smtp_password=os.getenv("SMTP_PASSWORD", ""),
            smtp_from=os.getenv("SMTP_FROM", ""),
            smtp_to=os.getenv("SMTP_TO", ""),
            smtp_use_tls=_env_bool("SMTP_USE_TLS", True),
        ),
        desktop_notifications_enabled=_env_bool("DESKTOP_NOTIFICATIONS_ENABLED", False),
    )

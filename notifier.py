from __future__ import annotations

import json
import logging
import platform
import smtplib
import subprocess
from email.message import EmailMessage

import requests

from config import AppConfig

logger = logging.getLogger(__name__)


class BaseNotifier:
    def notify(self, title: str, message: str, dry_run: bool) -> None:
        raise NotImplementedError


class ConsoleNotifier(BaseNotifier):
    def notify(self, title: str, message: str, dry_run: bool) -> None:
        prefix = "[DRY-RUN]" if dry_run else "[ALERTA]"
        print(f"{prefix} {title}: {message}")


class TelegramNotifier(BaseNotifier):
    def __init__(self, token: str, chat_id: str) -> None:
        self.token = token
        self.chat_id = chat_id

    def notify(self, title: str, message: str, dry_run: bool) -> None:
        if dry_run:
            logger.info("Telegram suprimido em dry-run: %s", message)
            return
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {"chat_id": self.chat_id, "text": f"{title}\n{message}"}
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()


class EmailNotifier(BaseNotifier):
    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        smtp_username: str,
        smtp_password: str,
        smtp_from: str,
        smtp_to: str,
        smtp_use_tls: bool,
    ) -> None:
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.smtp_from = smtp_from
        self.smtp_to = smtp_to
        self.smtp_use_tls = smtp_use_tls

    def notify(self, title: str, message: str, dry_run: bool) -> None:
        if dry_run:
            logger.info("E-mail suprimido em dry-run: %s", message)
            return

        msg = EmailMessage()
        msg["Subject"] = title
        msg["From"] = self.smtp_from
        msg["To"] = self.smtp_to
        msg.set_content(message)

        with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=15) as server:
            if self.smtp_use_tls:
                server.starttls()
            if self.smtp_username:
                server.login(self.smtp_username, self.smtp_password)
            server.send_message(msg)


class DesktopNotifier(BaseNotifier):
    def notify(self, title: str, message: str, dry_run: bool) -> None:
        if dry_run:
            logger.info("Desktop notification suprimida em dry-run: %s", message)
            return
        system = platform.system().lower()
        try:
            if "linux" in system:
                subprocess.run(["notify-send", title, message], check=False)
            elif "windows" in system:
                self._notify_windows(title, message)
            else:
                logger.warning("Desktop notification não suportada neste SO: %s", system)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Falha em desktop notification: %s", exc)

    def _notify_windows(self, title: str, message: str) -> None:
        try:
            from win10toast import ToastNotifier  # type: ignore

            ToastNotifier().show_toast(title, message, duration=5, threaded=True)
        except ImportError:
            logger.warning("win10toast não instalado; notificação desktop no Windows indisponível")


class NotifierHub:
    def __init__(self, config: AppConfig) -> None:
        self.notifiers: list[BaseNotifier] = [ConsoleNotifier()]

        if config.telegram.enabled and config.telegram.bot_token and config.telegram.chat_id:
            self.notifiers.append(TelegramNotifier(config.telegram.bot_token, config.telegram.chat_id))
        if config.email.enabled and config.email.smtp_host and config.email.smtp_to and config.email.smtp_from:
            self.notifiers.append(
                EmailNotifier(
                    smtp_host=config.email.smtp_host,
                    smtp_port=config.email.smtp_port,
                    smtp_username=config.email.smtp_username,
                    smtp_password=config.email.smtp_password,
                    smtp_from=config.email.smtp_from,
                    smtp_to=config.email.smtp_to,
                    smtp_use_tls=config.email.smtp_use_tls,
                )
            )
        if config.desktop_notifications_enabled:
            self.notifiers.append(DesktopNotifier())

    def notify_all(self, title: str, message: str, dry_run: bool) -> None:
        for notifier in self.notifiers:
            try:
                notifier.notify(title, message, dry_run=dry_run)
            except Exception as exc:  # noqa: BLE001
                logger.error(
                    "Falha ao enviar notificação via %s: %s",
                    notifier.__class__.__name__,
                    json.dumps(str(exc)),
                )

from __future__ import annotations

import logging
from dataclasses import asdict

import requests

from config import AppConfig
from notifier import NotifierHub
from parser import parse_sigaa_class_status
from storage import ClassState, MonitoredClass, Storage
from utils import RetryConfig, retry_with_backoff

logger = logging.getLogger(__name__)


class SIGAAFetcher:
    def __init__(self, config: AppConfig) -> None:
        self.timeout = config.request_timeout_seconds
        self.retry_config = RetryConfig(config.max_retries, config.backoff_seconds)

    def fetch(self, url: str) -> str:
        def _operation() -> str:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.text

        return retry_with_backoff(
            operation=_operation,
            retry_config=self.retry_config,
            is_retryable=lambda exc: isinstance(exc, requests.RequestException),
            on_retry=lambda exc, attempt, sleep: logger.warning(
                "Falha de conexão (%s). Tentativa %s. Novo retry em %.1fs",
                exc,
                attempt,
                sleep,
            ),
        )


class MonitorService:
    def __init__(self, storage: Storage, fetcher: SIGAAFetcher, notifier: NotifierHub, config: AppConfig) -> None:
        self.storage = storage
        self.fetcher = fetcher
        self.notifier = notifier
        self.config = config

    def check_once(self, monitored_class: MonitoredClass) -> None:
        if monitored_class.id is None:
            raise ValueError("MonitoredClass sem ID persistido")

        html = self.fetcher.fetch(monitored_class.query_url)
        parsed = parse_sigaa_class_status(html)

        current = ClassState(
            total_seats=parsed.get("total_seats"),
            occupied_seats=parsed.get("occupied_seats"),
            available_seats=parsed.get("available_seats"),
            status=parsed.get("status"),
        )

        previous = self.storage.get_latest_state(monitored_class.id)
        changed, summary = self._compare_states(previous, current)
        signature = self._change_signature(current)
        previous_signature = self.storage.get_last_change_signature(monitored_class.id)

        should_alert = changed and signature != previous_signature
        self.storage.save_observation(monitored_class.id, current, changed, summary, signature)

        if should_alert:
            title = f"Mudança detectada: {monitored_class.code} T{monitored_class.class_group}"
            message = f"{summary}. Estado atual: {asdict(current)}"
            logger.info(message)
            self.notifier.notify_all(title, message, dry_run=self.config.dry_run)
        else:
            logger.info(
                "Sem mudança relevante para %s T%s (%s)",
                monitored_class.code,
                monitored_class.class_group,
                monitored_class.term,
            )

    @staticmethod
    def _compare_states(previous: ClassState | None, current: ClassState) -> tuple[bool, str | None]:
        if previous is None:
            return True, "Primeira observação registrada"

        diffs: list[str] = []
        if previous.total_seats != current.total_seats:
            diffs.append(f"total_seats: {previous.total_seats} -> {current.total_seats}")
        if previous.occupied_seats != current.occupied_seats:
            diffs.append(f"occupied_seats: {previous.occupied_seats} -> {current.occupied_seats}")
        if previous.available_seats != current.available_seats:
            diffs.append(f"available_seats: {previous.available_seats} -> {current.available_seats}")
        if previous.status != current.status:
            diffs.append(f"status: {previous.status} -> {current.status}")

        if not diffs:
            return False, None
        return True, "; ".join(diffs)

    @staticmethod
    def _change_signature(state: ClassState) -> str:
        return f"{state.total_seats}|{state.occupied_seats}|{state.available_seats}|{state.status}"

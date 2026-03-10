from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable, TypeVar

T = TypeVar("T")


@dataclass(slots=True)
class RetryConfig:
    max_retries: int
    backoff_seconds: float


def retry_with_backoff(
    operation: Callable[[], T],
    retry_config: RetryConfig,
    is_retryable: Callable[[Exception], bool],
    on_retry: Callable[[Exception, int, float], None],
) -> T:
    """Run an operation with simple linear backoff retry policy."""
    attempt = 0
    while True:
        try:
            return operation()
        except Exception as exc:  # noqa: BLE001
            attempt += 1
            if attempt > retry_config.max_retries or not is_retryable(exc):
                raise
            sleep_seconds = retry_config.backoff_seconds * attempt
            on_retry(exc, attempt, sleep_seconds)
            time.sleep(sleep_seconds)

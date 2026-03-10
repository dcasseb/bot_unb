from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from threading import Event

from monitor import MonitorService
from storage import MonitoredClass, Storage

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class AddClassInput:
    code: str
    class_group: str
    term: str
    query_url: str
    name: str | None = None
    campus: str | None = None


class MonitoringAppService:
    def __init__(self, storage: Storage, monitor_service: MonitorService) -> None:
        self.storage = storage
        self.monitor_service = monitor_service

    def add_class(self, payload: AddClassInput) -> int:
        return self.storage.add_monitored_class(
            MonitoredClass(
                id=None,
                code=payload.code,
                name=payload.name,
                class_group=payload.class_group,
                term=payload.term,
                campus=payload.campus,
                query_url=payload.query_url,
            )
        )

    def list_classes(self) -> list[MonitoredClass]:
        return self.storage.list_monitored_classes()

    def remove_class(self, class_id: int) -> bool:
        return self.storage.remove_monitored_class(class_id)

    def history(self, limit: int = 20) -> list[dict[str, object]]:
        return [dict(row) for row in self.storage.recent_history(limit)]

    def history_for_class(self, class_id: int, limit: int = 20) -> list[dict[str, object]]:
        return [dict(row) for row in self.storage.recent_history_for_class(class_id, limit)]

    def run_cycle(self) -> dict[str, int]:
        classes = self.list_classes()
        if not classes:
            return {"checked": 0, "errors": 0}

        checked = 0
        errors = 0
        for monitored_class in classes:
            try:
                self.monitor_service.check_once(monitored_class)
                checked += 1
            except Exception as exc:  # noqa: BLE001
                errors += 1
                logger.error(
                    "Erro ao verificar %s T%s: %s",
                    monitored_class.code,
                    monitored_class.class_group,
                    exc,
                )
        return {"checked": checked, "errors": errors}

    def run_loop(self, interval: int, stop_event: Event | None = None) -> None:
        stop_signal = stop_event or Event()
        while not stop_signal.is_set():
            self.run_cycle()
            stop_signal.wait(timeout=interval)
            if interval <= 0:
                time.sleep(0)

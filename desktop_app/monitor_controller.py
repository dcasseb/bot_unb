from __future__ import annotations

import logging
import queue
import threading
from dataclasses import dataclass
from typing import Literal

from app_services import MonitoringAppService

logger = logging.getLogger(__name__)

MonitorEventType = Literal["cycle_result", "cycle_error", "stopped"]


@dataclass(slots=True)
class MonitorEvent:
    event_type: MonitorEventType
    payload: dict[str, object]


class MonitorController:
    def __init__(self, service: MonitoringAppService, event_queue: queue.Queue[MonitorEvent]) -> None:
        self._service = service
        self._event_queue = event_queue
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    @property
    def is_running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def start(self, interval: int) -> None:
        if self.is_running:
            return

        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._run_loop, args=(interval,), daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()

    def _run_loop(self, interval: int) -> None:
        try:
            while not self._stop_event.is_set():
                checked = 0
                errors = 0

                for monitored_class in self._service.list_classes():
                    if self._stop_event.is_set():
                        break
                    try:
                        self._service.monitor_service.check_once(monitored_class)
                        checked += 1
                    except Exception as exc:  # noqa: BLE001
                        errors += 1
                        logger.exception(
                            "Erro ao verificar %s T%s",
                            monitored_class.code,
                            monitored_class.class_group,
                        )
                        self._event_queue.put(
                            MonitorEvent(
                                event_type="cycle_error",
                                payload={
                                    "class_id": monitored_class.id,
                                    "code": monitored_class.code,
                                    "class_group": monitored_class.class_group,
                                    "error": str(exc),
                                },
                            )
                        )

                self._event_queue.put(
                    MonitorEvent(
                        event_type="cycle_result",
                        payload={"checked": checked, "errors": errors},
                    )
                )

                if interval <= 0:
                    continue
                self._stop_event.wait(timeout=interval)
        finally:
            self._event_queue.put(MonitorEvent(event_type="stopped", payload={}))

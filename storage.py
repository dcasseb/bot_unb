from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class MonitoredClass:
    id: int | None
    code: str
    name: str | None
    class_group: str
    term: str
    campus: str | None
    query_url: str


@dataclass(slots=True)
class ClassState:
    total_seats: int | None
    occupied_seats: int | None
    available_seats: int | None
    status: str | None


class Storage:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    def _conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self) -> None:
        with self._conn() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS monitored_classes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT NOT NULL,
                    name TEXT,
                    class_group TEXT NOT NULL,
                    term TEXT NOT NULL,
                    campus TEXT,
                    query_url TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS latest_state (
                    class_id INTEGER PRIMARY KEY,
                    total_seats INTEGER,
                    occupied_seats INTEGER,
                    available_seats INTEGER,
                    status TEXT,
                    observed_at TEXT NOT NULL,
                    last_change_signature TEXT,
                    FOREIGN KEY(class_id) REFERENCES monitored_classes(id)
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS state_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    class_id INTEGER NOT NULL,
                    total_seats INTEGER,
                    occupied_seats INTEGER,
                    available_seats INTEGER,
                    status TEXT,
                    observed_at TEXT NOT NULL,
                    changed INTEGER NOT NULL,
                    change_summary TEXT,
                    FOREIGN KEY(class_id) REFERENCES monitored_classes(id)
                )
                """
            )

    def add_monitored_class(self, item: MonitoredClass) -> int:
        now = datetime.utcnow().isoformat()
        with self._conn() as conn:
            cursor = conn.execute(
                """
                INSERT INTO monitored_classes (code, name, class_group, term, campus, query_url, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (item.code, item.name, item.class_group, item.term, item.campus, item.query_url, now),
            )
            return int(cursor.lastrowid)

    def list_monitored_classes(self) -> list[MonitoredClass]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT id, code, name, class_group, term, campus, query_url FROM monitored_classes ORDER BY id"
            ).fetchall()
        return [
            MonitoredClass(
                id=row["id"],
                code=row["code"],
                name=row["name"],
                class_group=row["class_group"],
                term=row["term"],
                campus=row["campus"],
                query_url=row["query_url"],
            )
            for row in rows
        ]

    def remove_monitored_class(self, class_id: int) -> bool:
        with self._conn() as conn:
            deleted = conn.execute("DELETE FROM monitored_classes WHERE id = ?", (class_id,)).rowcount
            conn.execute("DELETE FROM latest_state WHERE class_id = ?", (class_id,))
            return deleted > 0

    def get_latest_state(self, class_id: int) -> ClassState | None:
        with self._conn() as conn:
            row = conn.execute(
                """
                SELECT total_seats, occupied_seats, available_seats, status
                FROM latest_state WHERE class_id = ?
                """,
                (class_id,),
            ).fetchone()
        if not row:
            return None
        return ClassState(
            total_seats=row["total_seats"],
            occupied_seats=row["occupied_seats"],
            available_seats=row["available_seats"],
            status=row["status"],
        )

    def get_last_change_signature(self, class_id: int) -> str | None:
        with self._conn() as conn:
            row = conn.execute(
                "SELECT last_change_signature FROM latest_state WHERE class_id = ?", (class_id,)
            ).fetchone()
        return row["last_change_signature"] if row else None

    def save_observation(
        self,
        class_id: int,
        state: ClassState,
        changed: bool,
        change_summary: str | None,
        signature: str | None,
    ) -> None:
        now = datetime.utcnow().isoformat()
        with self._conn() as conn:
            conn.execute(
                """
                INSERT INTO state_history (
                    class_id, total_seats, occupied_seats, available_seats, status,
                    observed_at, changed, change_summary
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    class_id,
                    state.total_seats,
                    state.occupied_seats,
                    state.available_seats,
                    state.status,
                    now,
                    1 if changed else 0,
                    change_summary,
                ),
            )
            conn.execute(
                """
                INSERT INTO latest_state (
                    class_id, total_seats, occupied_seats, available_seats,
                    status, observed_at, last_change_signature
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(class_id) DO UPDATE SET
                    total_seats=excluded.total_seats,
                    occupied_seats=excluded.occupied_seats,
                    available_seats=excluded.available_seats,
                    status=excluded.status,
                    observed_at=excluded.observed_at,
                    last_change_signature=excluded.last_change_signature
                """,
                (
                    class_id,
                    state.total_seats,
                    state.occupied_seats,
                    state.available_seats,
                    state.status,
                    now,
                    signature,
                ),
            )

    def recent_history(self, limit: int = 20) -> list[sqlite3.Row]:
        with self._conn() as conn:
            return conn.execute(
                """
                SELECT h.id, h.class_id, m.code, m.class_group, m.term,
                       h.total_seats, h.occupied_seats, h.available_seats,
                       h.status, h.observed_at, h.changed, h.change_summary
                FROM state_history h
                JOIN monitored_classes m ON m.id = h.class_id
                ORDER BY h.id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

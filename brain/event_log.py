from __future__ import annotations

from datetime import datetime


class EventLog:
    def __init__(self, limit: int = 200) -> None:
        self.limit = limit
        self.entries: list[dict] = []

    def record(self, category: str, message: str, payload: dict | None = None) -> None:
        entry = {
            "time": datetime.now().isoformat(timespec="seconds"),
            "category": category,
            "message": message,
            "payload": payload or {},
        }
        self.entries.append(entry)
        if len(self.entries) > self.limit:
            self.entries = self.entries[-self.limit:]

    def recent(self, limit: int = 20) -> list[dict]:
        return self.entries[-limit:]

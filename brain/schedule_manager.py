from __future__ import annotations


class ScheduleManager:
    def __init__(self) -> None:
        self.reminders: list[dict] = []

    def add_tick_reminder(self, delay_ticks: int, message: str, current_tick: int) -> dict:
        reminder = {
            "due_tick": current_tick + max(1, delay_ticks),
            "message": message.strip() or "нагадування",
            "done": False,
        }
        self.reminders.append(reminder)
        return reminder

    def due(self, current_tick: int) -> list[dict]:
        due_items = []
        for reminder in self.reminders:
            if not reminder["done"] and reminder["due_tick"] <= current_tick:
                reminder["done"] = True
                due_items.append(reminder)
        return due_items

    def snapshot(self) -> list[dict]:
        return list(self.reminders)

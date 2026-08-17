class ActionQueue:
    def __init__(self) -> None:
        self.queue = []

    def add_actions(self, actions: list[dict]) -> None:
        self.queue.extend(actions)
        print(f"[QUEUE] Added {len(actions)} action(s). Total in queue: {len(self.queue)}")

    def has_actions(self) -> bool:
        return len(self.queue) > 0

    def pop_next(self) -> dict | None:
        if not self.queue:
            return None
        return self.queue.pop(0)

    def clear(self) -> None:
        self.queue.clear()
        print("[QUEUE] Cleared")

    def snapshot(self) -> list[dict]:
        return list(self.queue)
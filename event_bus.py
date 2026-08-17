class EventBus:
    def __init__(self) -> None:
        self.event_history = []

    def emit(self, event_name: str) -> None:
        self.event_history.append(event_name)
        print(f"[EVENT] {event_name}")

    def get_last_event(self) -> str | None:
        if not self.event_history:
            return None
        return self.event_history[-1]
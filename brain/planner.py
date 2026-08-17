EVENT_PRIORITIES = {
    "battery_low": 100,
    "error": 90,
    "wake": 80,
    "voice": 70,
    "voice_greeting": 70,
    "recognized_face": 65,
    "face": 60,
    "think": 50,
    "sad": 40,
    "sleep": 30,
    "no_face": 15,
    "idle": 10,
    "status": 0,
}


class Planner:
    def __init__(self) -> None:
        self.last_priority = -1

    def get_priority(self, event: str) -> int:
        if event.startswith("recognized_face "):
            return EVENT_PRIORITIES["recognized_face"]
        return EVENT_PRIORITIES.get(event, 20)

    def should_handle_event(self, event: str) -> bool:
        priority = self.get_priority(event)
        self.last_priority = priority
        return True

    def get_last_priority(self) -> int:
        return self.last_priority
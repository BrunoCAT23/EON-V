class TimerManager:
    def __init__(self) -> None:
        self.timers = {}

    def set_timer(self, name: str, interval: int, current_tick: int) -> None:
        self.timers[name] = {
            "interval": interval,
            "last_tick": current_tick,
        }

    def is_due(self, name: str, current_tick: int) -> bool:
        if name not in self.timers:
            return False

        timer = self.timers[name]
        return current_tick - timer["last_tick"] >= timer["interval"]

    def reset_timer(self, name: str, current_tick: int) -> None:
        if name in self.timers:
            self.timers[name]["last_tick"] = current_tick

    def snapshot(self) -> dict:
        return dict(self.timers)
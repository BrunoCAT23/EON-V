class LifeState:
    def __init__(self) -> None:
        self.autonomous_enabled = False
        self.tick_count = 0
        self.last_idle_tick = -1

    def enable(self) -> None:
        self.autonomous_enabled = True
        print("[LIFE_STATE] Autonomous mode enabled")

    def disable(self) -> None:
        self.autonomous_enabled = False
        print("[LIFE_STATE] Autonomous mode disabled")

    def is_enabled(self) -> bool:
        return self.autonomous_enabled

    def next_tick(self) -> int:
        self.tick_count += 1
        return self.tick_count

    def get_tick(self) -> int:
        return self.tick_count

    def set_last_idle_tick(self, tick: int) -> None:
        self.last_idle_tick = tick

    def get_last_idle_tick(self) -> int:
        return self.last_idle_tick
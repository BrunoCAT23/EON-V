class PresenceModel:
    def __init__(self) -> None:
        self.current_present_person = None
        self.last_seen_tick = None
        self.last_heard_tick = None
        self.presence_timeout = 6

    def update_visual_presence(self, person_name: str | None, tick: int) -> None:
        self.current_present_person = person_name
        self.last_seen_tick = tick

    def update_audio_presence(self, tick: int) -> None:
        self.last_heard_tick = tick

    def get_current_person(self) -> str | None:
        return self.current_present_person

    def is_person_present(self, current_tick: int) -> bool:
        if self.current_present_person is None:
            return False

        if self.last_seen_tick is None:
            return False

        return (current_tick - self.last_seen_tick) <= self.presence_timeout

    def clear_presence_if_expired(self, current_tick: int) -> bool:
        if self.current_present_person is None:
            return False

        if self.last_seen_tick is None:
            return False

        if (current_tick - self.last_seen_tick) > self.presence_timeout:
            self.current_present_person = None
            self.last_seen_tick = None
            return True

        return False

    def snapshot(self) -> dict:
        return {
            "current_present_person": self.current_present_person,
            "last_seen_tick": self.last_seen_tick,
            "last_heard_tick": self.last_heard_tick,
            "presence_timeout": self.presence_timeout,
        }
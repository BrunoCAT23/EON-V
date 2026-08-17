class ContextManager:
    def __init__(self) -> None:
        self.current_person = None
        self.last_voice_text = None
        self.last_visual_event = None
        self.last_voice_intent = None
        self.last_system_event = None

    def set_current_person(self, person_name: str | None) -> None:
        self.current_person = person_name

    def get_current_person(self) -> str | None:
        return self.current_person

    def set_last_voice_text(self, text: str | None) -> None:
        self.last_voice_text = text

    def get_last_voice_text(self) -> str | None:
        return self.last_voice_text

    def set_last_visual_event(self, event: str | None) -> None:
        self.last_visual_event = event

    def get_last_visual_event(self) -> str | None:
        return self.last_visual_event

    def set_last_voice_intent(self, intent: str | None) -> None:
        self.last_voice_intent = intent

    def get_last_voice_intent(self) -> str | None:
        return self.last_voice_intent

    def set_last_system_event(self, event: str | None) -> None:
        self.last_system_event = event

    def get_last_system_event(self) -> str | None:
        return self.last_system_event

    def snapshot(self) -> dict:
        return {
            "current_person": self.current_person,
            "last_voice_text": self.last_voice_text,
            "last_visual_event": self.last_visual_event,
            "last_voice_intent": self.last_voice_intent,
            "last_system_event": self.last_system_event,
        }
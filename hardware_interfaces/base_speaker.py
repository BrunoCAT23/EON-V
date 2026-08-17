class BaseSpeaker:
    def speak(self, text: str) -> None:
        raise NotImplementedError

    def beep(self, sound_name: str = "default") -> None:
        raise NotImplementedError

    def get_last_spoken_text(self) -> str | None:
        raise NotImplementedError
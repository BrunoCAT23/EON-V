class SpeakerController:
    def __init__(self) -> None:
        self.last_spoken_text = None

    def speak(self, text: str) -> None:
        self.last_spoken_text = text
        print(f"[SPEAKER_CONTROLLER] {text}")

    def beep(self, sound_name: str = "default") -> None:
        print(f"[SPEAKER_CONTROLLER] Beep sound: {sound_name}")

    def get_last_spoken_text(self) -> str | None:
        return self.last_spoken_text
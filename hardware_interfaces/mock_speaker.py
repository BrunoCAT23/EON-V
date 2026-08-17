from hardware_interfaces.base_speaker import BaseSpeaker


class MockSpeaker(BaseSpeaker):
    def __init__(self) -> None:
        self.last_spoken_text = None

    def speak(self, text: str) -> None:
        self.last_spoken_text = text
        print(f"[MOCK_SPEAKER] {text}")

    def beep(self, sound_name: str = "default") -> None:
        print(f"[MOCK_SPEAKER] Beep: {sound_name}")

    def get_last_spoken_text(self) -> str | None:
        return self.last_spoken_text
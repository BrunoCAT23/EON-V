from hardware_interfaces.base_display import BaseDisplay


class MockDisplay(BaseDisplay):
    def __init__(self) -> None:
        self.current_face = "neutral"

    def show_emotion(self, emotion: str) -> None:
        self.current_face = emotion
        print(f"[MOCK_DISPLAY] Showing emotion: {emotion}")

    def show_text(self, text: str) -> None:
        print(f"[MOCK_DISPLAY] Text: {text}")

    def get_current_face(self) -> str:
        return self.current_face
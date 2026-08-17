from config import DEFAULT_EMOTION, AVAILABLE_EMOTIONS


class EmotionEngine:
    def __init__(self) -> None:
        self.current_emotion = DEFAULT_EMOTION

    def set_emotion(self, emotion: str) -> None:
        if emotion not in AVAILABLE_EMOTIONS:
            print(f"[EMOTION] Unknown emotion: {emotion}")
            return

        old_emotion = self.current_emotion
        self.current_emotion = emotion
        print(f"[EMOTION] {old_emotion} -> {self.current_emotion}")

    def get_emotion(self) -> str:
        return self.current_emotion
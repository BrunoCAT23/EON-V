class EmotionalDynamics:
    def __init__(self) -> None:
        self.emotions = {
            "happy": 0.0,
            "curious": 0.0,
            "sad": 0.0,
            "sleepy": 0.0,
            "thinking": 0.0,
        }
        self.decay_rate = 0.1

    def trigger(self, emotion: str, amount: float = 0.4) -> None:
        if emotion in self.emotions:
            self.emotions[emotion] = min(1.0, self.emotions[emotion] + amount)

    def decay(self) -> None:
        for key in self.emotions:
            self.emotions[key] = max(0.0, self.emotions[key] - self.decay_rate)

    def get_levels(self) -> dict:
        return dict(self.emotions)

    def dominant_emotion(self) -> str:
        dominant = max(self.emotions, key=self.emotions.get)
        if self.emotions[dominant] <= 0.05:
            return "neutral"
        return dominant
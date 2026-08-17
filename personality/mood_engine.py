class MoodEngine:
    def derive_mood(self, emotional_levels: dict) -> str:
        happy = emotional_levels.get("happy", 0.0)
        curious = emotional_levels.get("curious", 0.0)
        sad = emotional_levels.get("sad", 0.0)
        sleepy = emotional_levels.get("sleepy", 0.0)
        thinking = emotional_levels.get("thinking", 0.0)

        if sleepy >= 0.5:
            return "low_energy"

        if sad >= 0.45:
            return "melancholic"

        if happy >= 0.55:
            return "playful"

        if curious >= 0.5 or thinking >= 0.5:
            return "inquisitive"

        return "calm"
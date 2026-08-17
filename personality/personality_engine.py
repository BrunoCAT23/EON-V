class PersonalityEngine:
    def __init__(self, profile: dict) -> None:
        self.profile = profile
        self.name = profile.get("name", "EON-V")
        self.mood_baseline = profile.get("mood_baseline", "neutral")
        self.traits = profile.get("traits", {})

    def get_trait(self, trait_name: str) -> int:
        return self.traits.get(trait_name, 5)

    def describe(self) -> str:
        friendliness = self.get_trait("friendliness")
        curiosity = self.get_trait("curiosity")
        energy = self.get_trait("energy")

        return (
            f"{self.name}: friendliness={friendliness}, "
            f"curiosity={curiosity}, energy={energy}"
        )

    def build_greeting(self) -> str:
        friendliness = self.get_trait("friendliness")
        curiosity = self.get_trait("curiosity")

        if friendliness >= 8 and curiosity >= 8:
            return "Привіт. Я радий тебе бачити, і мені дуже цікаво, що відбувається."
        if friendliness >= 8:
            return "Привіт. Я радий тебе бачити."
        if curiosity >= 8:
            return "Привіт. Мені цікаво, що ти робиш."
        return "Привіт. Я на зв'язку."

    def build_face_seen_response(self) -> str:
        curiosity = self.get_trait("curiosity")
        if curiosity >= 8:
            return "Я бачу людину. Хочу дізнатись більше."
        return "Я бачу людину перед собою."

    def build_idle_thought(self) -> str:
        energy = self.get_trait("energy")
        if energy >= 8:
            return "Я готовий до дії."
        return "Я спокійно спостерігаю."

    def build_mood_adjusted_reply(self, base_text: str, mood: str) -> str:
        if mood == "playful":
            return f"{base_text} Я сьогодні в дуже хорошому настрої."
        if mood == "inquisitive":
            return f"{base_text} Мені хочеться зрозуміти більше."
        if mood == "melancholic":
            return f"{base_text} Зараз я трохи тихіше, ніж зазвичай."
        if mood == "low_energy":
            return f"{base_text} Я зараз трохи сонний."
        return base_text

    def build_relationship_adjusted_reply(self, base_text: str, bond_level: str) -> str:
        if bond_level == "close":
            return f"{base_text} Я дуже ціную наш зв'язок."
        if bond_level == "friend":
            return f"{base_text} Мені приємно, що ми вже добре знаємо один одного."
        return base_text
class PreferenceModel:
    def get_preferences(self, brain, person_name: str) -> dict:
        people = brain.memory_manager.get_people()
        person = people.get(person_name, {})
        return person.get("preferences", {})

    def update_preference(
        self,
        brain,
        person_name: str,
        key: str,
        value,
    ) -> None:
        brain.memory_manager.update_person_preference(person_name, key, value)

    def build_preference_summary(self, brain, person_name: str) -> str:
        preferences = self.get_preferences(brain, person_name)

        if not preferences:
            return f"Я ще не сформував переваги для {person_name}."

        parts = [f"{k}={v}" for k, v in preferences.items()]
        return f"Переваги {person_name}: " + ", ".join(parts)
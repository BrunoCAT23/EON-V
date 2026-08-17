class PetModel:
    def get_pets(self, brain) -> dict:
        return brain.memory_manager.get_pets()

    def save_pet(self, brain, name: str, pet_type: str) -> None:
        brain.memory_manager.save_pet(name, pet_type)

    def mark_pet_seen(self, brain, name: str) -> None:
        brain.memory_manager.mark_pet_seen(name)

    def update_pet_trait(self, brain, name: str, key: str, value) -> None:
        brain.memory_manager.update_pet_trait(name, key, value)

    def build_pet_summary(self, brain, name: str) -> str:
        pets = self.get_pets(brain)
        pet = pets.get(name)

        if not pet:
            return f"Я ще не знаю улюбленця {name}."

        return (
            f"Улюбленець {name}: "
            f"type={pet.get('type')}, "
            f"times_seen={pet.get('times_seen')}, "
            f"playfulness={pet.get('traits', {}).get('playfulness', 'unknown')}"
        )
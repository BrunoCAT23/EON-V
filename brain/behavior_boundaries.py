class BehaviorBoundaries:
    def get_context_profile(self, brain) -> dict:
        focused_person = brain.social_context.get_focused_person()
        known_pets = brain.memory_manager.get_pets()

        has_pet_context = len(known_pets) > 0

        return {
            "focused_person": focused_person,
            "has_pet_context": has_pet_context,
            "current_mood": brain.current_mood,
            "state": brain.state_manager.get_state(),
        }

    def should_reduce_intensity(self, brain) -> bool:
        profile = self.get_context_profile(brain)

        if profile["current_mood"] in ["melancholic", "low_energy"]:
            return True

        if profile["has_pet_context"]:
            return True

        return False
class PetBehaviorEngine:
    def build_pet_reaction(self, brain, pet_name: str, pet_type: str, known: bool) -> list[dict]:
        actions = []

        if known:
            actions.append({"type": "show_emotion", "value": "happy"})
            actions.append({"type": "voice_reply", "value": f"Я знову бачу {pet_name}."})
        else:
            actions.append({"type": "show_emotion", "value": "curious"})
            actions.append({"type": "voice_reply", "value": f"Я бачу нового {pet_type}."})

        if pet_type in ["cat", "dog"]:
            actions.append({"type": "track_face"})
            actions.append({"type": "log", "value": f"Tracking pet: {pet_name}"})

        return actions
class PetPlayEngine:
    def build_play_actions(self, brain, pet_name: str, pet_type: str) -> list[dict]:
        actions = []

        if pet_type == "cat":
            actions.append({"type": "gentle_track"})
            actions.append({"type": "set_head_position", "value": "left"})
            actions.append({"type": "set_head_position", "value": "right"})
            actions.append({"type": "voice_reply", "value": f"{pet_name}, хочеш спокійно погратись?"})
            actions.append({"type": "log", "value": f"Soft pet play mode started for cat {pet_name}"})

        elif pet_type == "dog":
            actions.append({"type": "soft_idle"})
            actions.append({"type": "voice_reply", "value": f"{pet_name}, привіт, друже. Давай пограємось спокійно?"})
            actions.append({"type": "log", "value": f"Soft pet play mode started for dog {pet_name}"})

        else:
            actions.append({"type": "voice_reply", "value": "Я бачу домашнього улюбленця. Буду вести себе дуже обережно."})
            actions.append({"type": "log", "value": "Unknown pet soft play mode"})

        return actions
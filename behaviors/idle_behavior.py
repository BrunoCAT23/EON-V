class IdleBehavior:
    def generate(self, brain) -> list[dict]:
        curiosity = brain.personality_engine.get_trait("curiosity")
        energy = brain.personality_engine.get_trait("energy")
        mood = brain.current_mood

        actions = [{"type": "idle_animation"}]

        if mood == "playful":
            actions.append({"type": "gesture", "value": "look_around"})
            actions.append({"type": "voice_reply", "value": "Я в гарному настрої і хочу взаємодіяти."})

        elif mood == "inquisitive":
            actions.append({"type": "gesture", "value": "look_around"})
            actions.append({"type": "log", "value": "Inquisitive idle pattern"})

        elif mood == "melancholic":
            actions.append({"type": "set_head_position", "value": "down"})
            actions.append({"type": "log", "value": "Melancholic idle pattern"})

        elif mood == "low_energy":
            actions.append({"type": "set_head_position", "value": "down"})
            actions.append({"type": "voice_reply", "value": "Я зараз трохи втомлений."})

        else:
            if curiosity >= 8:
                actions.append({"type": "gesture", "value": "look_around"})

            if energy >= 7:
                actions.append({"type": "log", "value": "High-energy idle pattern"})
            else:
                actions.append({"type": "log", "value": "Calm idle pattern"})

        return actions
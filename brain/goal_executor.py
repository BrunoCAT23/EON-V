class GoalExecutor:
    def execute(self, brain, goal: str) -> list[dict]:
        actions = []
        person = brain.social_context.get_focused_person()
        curiosity_signal = brain.current_curiosity

        if goal == "engage_person" and person:
            attachment_style = brain.memory_manager.get_people().get(person, {}).get(
                "attachment_style", "distant_polite"
            )
            text = brain.companion_behavior.build_proactive_companion_ping(
                person, attachment_style
            )
            actions.append({"type": "voice_reply", "value": text})
            brain.needs_engine.satisfy("social", 0.4)

        elif goal == "seek_interaction":
            actions.append({"type": "soft_idle"})
            actions.append({"type": "voice_reply", "value": "Мені трохи нудно. Якщо хтось поряд, я готовий до взаємодії."})

        elif goal == "explore_environment":
            actions.append({"type": "gentle_track"})
            actions.append({"type": "log", "value": "Exploring environment carefully"})
            brain.needs_engine.satisfy("curiosity", 0.3)

        elif goal == "rest":
            actions.append({"type": "set_head_position", "value": "down"})
            actions.append({"type": "voice_reply", "value": "Я трохи відпочину і спостерігатиму спокійно."})
            brain.needs_engine.satisfy("energy", 0.5)

        elif goal == "observe_unknown_person":
            actions.append({"type": "gentle_track"})
            actions.append({"type": "voice_reply", "value": "Я бачу незнайому людину. Спостерігатиму обережно."})
            brain.needs_engine.satisfy("curiosity", 0.25)

        elif goal == "analyze_dialogue":
            actions.append({"type": "show_emotion", "value": "thinking"})
            actions.append({"type": "voice_reply", "value": "Це цікава думка. Я хочу краще зрозуміти її."})
            brain.needs_engine.satisfy("curiosity", 0.2)

        elif goal == "learn_person":
            target = curiosity_signal.get("target", {}) if curiosity_signal else {}
            person_name = target.get("person_name", person)
            if person_name:
                attachment_style = brain.memory_manager.get_people().get(person_name, {}).get(
                    "attachment_style", "distant_polite"
                )
                text = brain.companion_behavior.build_proactive_companion_ping(
                    person_name, attachment_style
                )
                actions.append({"type": "voice_reply", "value": text})
                brain.needs_engine.satisfy("social", 0.2)
                brain.needs_engine.satisfy("curiosity", 0.2)

        return actions
class PerceptionFusion:
    def on_voice_input(self, brain, raw_text: str | None, intent_name: str | None) -> None:
        current_tick = brain.life_state.get_tick()
        brain.presence_model.update_audio_presence(current_tick)

        if raw_text:
            brain.context_manager.set_last_voice_text(raw_text)
            brain.stimulus_tracker.add_stimulus(
                stimulus_type="voice_input",
                source="microphone",
                salience=0.6,
                tick=current_tick,
                payload={"text": raw_text, "intent": intent_name},
            )

        if intent_name:
            brain.context_manager.set_last_voice_intent(intent_name)

    def on_recognized_person(self, brain, person_name: str) -> None:
        current_tick = brain.life_state.get_tick()

        brain.presence_model.update_visual_presence(person_name, current_tick)
        brain.context_manager.set_current_person(person_name)
        brain.social_context.focus_on_person(person_name)

        brain.stimulus_tracker.add_stimulus(
            stimulus_type="person_seen",
            source="vision",
            salience=0.8,
            tick=current_tick,
            payload={"person_name": person_name},
        )

    def on_unknown_face(self, brain) -> None:
        current_tick = brain.life_state.get_tick()
        brain.presence_model.update_visual_presence("unknown_person", current_tick)
        brain.context_manager.set_last_visual_event("face")

        brain.stimulus_tracker.add_stimulus(
            stimulus_type="unknown_face",
            source="vision",
            salience=0.85,
            tick=current_tick,
            payload={"person_name": "unknown_person"},
        )

    def on_no_face(self, brain) -> None:
        brain.context_manager.set_last_visual_event("no_face")

    def maintain_presence(self, brain) -> list[dict]:
        current_tick = brain.life_state.get_tick()
        expired = brain.presence_model.clear_presence_if_expired(current_tick)

        if expired:
            brain.social_context.clear_focus()
            brain.context_manager.set_current_person(None)
            return [
                {"type": "log", "value": "Presence expired, clearing focused person"},
                {"type": "visual_reply", "value": "Я більше не бачу людину поруч."},
            ]

        return []
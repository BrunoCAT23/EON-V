class ReactiveTriggers:
    def evaluate(self, brain) -> list[dict]:
        actions = []

        current_tick = brain.life_state.get_tick()
        focused_person = brain.social_context.get_focused_person()
        state = brain.state_manager.get_state()

        brain.emotional_dynamics.decay()
        brain.current_mood = brain.mood_engine.derive_mood(
            brain.emotional_dynamics.get_levels()
        )

        focus = brain.attention_system.select_focus(brain)
        brain.current_curiosity = brain.curiosity_engine.evaluate(brain)

        if focus:
            actions.append(
                {"type": "log", "value": f"Attention focus: {focus.get('type')} from {focus.get('source')}"}
            )

        if brain.current_curiosity:
            actions.append(
                {"type": "log", "value": f"Curiosity triggered: {brain.current_curiosity.get('curiosity_type')}"}
            )

        if state == "SLEEP":
            return actions

        if brain.timer_manager.is_due("idle_behavior", current_tick):
            actions.append({"type": "log", "value": "Reactive trigger: idle behavior due"})
            brain.timer_manager.reset_timer("idle_behavior", current_tick)
            actions.extend(brain.behavior_engine.generate_idle_behavior(brain))

        if focused_person and brain.timer_manager.is_due("social_ping", current_tick):
            base = f"{focused_person}, я все ще тут поруч."
            text = brain.personality_engine.build_mood_adjusted_reply(
                base, brain.current_mood
            )
            actions.append({"type": "log", "value": f"Reactive trigger: social ping for {focused_person}"})
            actions.append({"type": "voice_reply", "value": text})
            brain.timer_manager.reset_timer("social_ping", current_tick)

        return actions
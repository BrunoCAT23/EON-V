class GoalEngine:
    def decide_goal(self, brain) -> str | None:
        needs = brain.needs_engine.get_needs()
        focused_person = brain.social_context.get_focused_person()
        curiosity_signal = brain.current_curiosity

        if curiosity_signal:
            curiosity_type = curiosity_signal.get("curiosity_type")

            if curiosity_type == "investigate_unknown_person":
                return "observe_unknown_person"

            if curiosity_type == "investigate_complex_dialogue":
                return "analyze_dialogue"

            if curiosity_type == "learn_about_person":
                return "learn_person"

        if needs["social"] < 0.3:
            if focused_person:
                return "engage_person"
            return "seek_interaction"

        if needs["curiosity"] < 0.3:
            return "explore_environment"

        if needs["energy"] < 0.2:
            return "rest"

        return None
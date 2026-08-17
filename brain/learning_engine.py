class LearningEngine:
    def learn_from_dialogue(self, brain, person_name: str | None, text: str) -> None:
        if not person_name:
            return

        normalized = text.strip().lower()

        if len(normalized.split()) > 8:
            brain.preference_model.update_preference(
                brain, person_name, "likes_detailed_dialogue", True
            )

        warm_markers = ["дякую", "клас", "добре", "супер", "друже", "приємно", "радий", "люблю", "окей"]
        if any(marker in normalized for marker in warm_markers):
            brain.preference_model.update_preference(
                brain, person_name, "prefers_warm_style", True
            )

    def learn_from_interaction_type(self, brain, person_name: str | None, interaction_type: str) -> None:
        if not person_name:
            return

        if interaction_type == "voice":
            brain.preference_model.update_preference(
                brain, person_name, "frequent_voice_user", True
            )

        if interaction_type == "vision":
            brain.preference_model.update_preference(
                brain, person_name, "physically_present_often", True
            )
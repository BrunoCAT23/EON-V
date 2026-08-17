class BondEngine:
    def update_from_interaction(self, brain, person_name: str | None, interaction_type: str) -> None:
        if not person_name:
            return

        if interaction_type == "greeting":
            brain.relationship_model.increase_familiarity(brain, person_name, 0.05)

        elif interaction_type == "dialogue":
            brain.relationship_model.increase_trust(brain, person_name, 0.04)
            brain.relationship_model.increase_familiarity(brain, person_name, 0.03)

        elif interaction_type == "recognized_face":
            brain.relationship_model.increase_familiarity(brain, person_name, 0.04)

        elif interaction_type == "remembered_fact":
            brain.relationship_model.increase_trust(brain, person_name, 0.06)

        elif interaction_type == "supportive_exchange":
            brain.relationship_model.increase_trust(brain, person_name, 0.08)
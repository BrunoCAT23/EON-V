class PromptBuilder:
    def build(self, brain, user_text: str) -> dict:
        focused_person = brain.social_context.get_focused_person()
        personality = brain.personality_engine.describe()
        recent_dialogue = brain.dialogue_memory.build_dialogue_summary(brain)
        presence = brain.presence_model.snapshot()

        person_facts = []
        person_preferences = {}
        relationship = {}
        attachment_style = None

        if focused_person:
            person_facts = brain.personal_knowledge.get_person_facts(brain, focused_person)
            person_preferences = brain.preference_model.get_preferences(brain, focused_person)
            relationship = brain.relationship_model.get_relationship(brain, focused_person)
            attachment_style = brain.memory_manager.get_people().get(
                focused_person, {}
            ).get("attachment_style")

        prompt = {
            "system_identity": "You are EON-V, a physical AI companion robot.",
            "personality": personality,
            "focused_person": focused_person,
            "person_facts": person_facts,
            "person_preferences": person_preferences,
            "relationship": relationship,
            "attachment_style": attachment_style,
            "recent_dialogue": recent_dialogue,
            "presence": presence,
            "user_text": user_text,
        }

        return prompt
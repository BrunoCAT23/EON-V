class CuriosityEngine:
    def evaluate(self, brain) -> dict | None:
        focus = brain.attention_system.get_focus()

        if not focus:
            return None

        focus_type = focus.get("type")
        payload = focus.get("payload", {})

        if focus_type == "unknown_face":
            return {
                "curiosity_type": "investigate_unknown_person",
                "target": payload,
            }

        if focus_type == "voice_input":
            text = payload.get("text", "")
            if len(text.split()) > 6:
                return {
                    "curiosity_type": "investigate_complex_dialogue",
                    "target": payload,
                }

        if focus_type == "person_seen":
            person_name = payload.get("person_name")
            facts = brain.personal_knowledge.get_person_facts(brain, person_name) if person_name else []
            if person_name and not facts:
                return {
                    "curiosity_type": "learn_about_person",
                    "target": payload,
                }

        return None
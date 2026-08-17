from skills.base_skill import BaseSkill


class GreetSkill(BaseSkill):
    def __init__(self) -> None:
        super().__init__("greet")

    def execute(self, brain, payload: dict | None = None) -> dict:
        focused_person = brain.social_context.get_focused_person()

        if focused_person:
            text = f"Привіт {focused_person}. Радий взаємодіяти з тобою."
        else:
            text = brain.personality_engine.build_greeting()

        return {
            "success": True,
            "skill": self.name,
            "text": text,
            "actions": [
                {"type": "set_state", "value": "LISTENING"},
                {"type": "show_emotion", "value": "happy"},
                {"type": "voice_reply", "value": text},
            ]
        }
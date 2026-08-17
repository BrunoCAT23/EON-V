from skills.base_skill import BaseSkill


class ThinkSkill(BaseSkill):
    def __init__(self) -> None:
        super().__init__("think")

    def execute(self, brain, payload: dict | None = None) -> dict:
        focused_person = brain.social_context.get_focused_person()

        if focused_person:
            text = f"Я запускаю аналіз ситуації для взаємодії з {focused_person}."
        else:
            text = "Я запускаю аналіз ситуації."

        return {
            "success": True,
            "skill": self.name,
            "text": text,
            "actions": [
                {"type": "set_state", "value": "THINKING"},
                {"type": "show_emotion", "value": "thinking"},
                {"type": "log", "value": "Skill think started"},
                {"type": "voice_reply", "value": text},
            ]
        }
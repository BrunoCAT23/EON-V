from skills.base_skill import BaseSkill


class SleepSkill(BaseSkill):
    def __init__(self) -> None:
        super().__init__("sleep")

    def execute(self, brain, payload: dict | None = None) -> dict:
        text = "Я переходжу в режим сну через skill system."

        return {
            "success": True,
            "skill": self.name,
            "text": text,
            "actions": [
                {"type": "set_state", "value": "SLEEP"},
                {"type": "show_emotion", "value": "sleepy"},
                {"type": "sleep_mode"},
                {"type": "voice_reply", "value": text},
            ]
        }
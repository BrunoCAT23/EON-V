from skills.base_skill import BaseSkill


class StatusSkill(BaseSkill):
    def __init__(self) -> None:
        super().__init__("status")

    def execute(self, brain, payload: dict | None = None) -> dict:
        focused_person = brain.social_context.get_focused_person()

        if focused_person:
            text = (
                f"Мій стан: {brain.state_manager.get_state()}, "
                f"емоція: {brain.emotion_engine.get_emotion()}, "
                f"в фокусі: {focused_person}."
            )
        else:
            text = (
                f"Мій стан: {brain.state_manager.get_state()}, "
                f"емоція: {brain.emotion_engine.get_emotion()}."
            )

        return {
            "success": True,
            "skill": self.name,
            "text": text,
            "actions": [
                {"type": "log", "value": "Status skill prepared response"},
                {"type": "voice_reply", "value": text},
            ]
        }
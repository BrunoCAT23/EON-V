class DialogueMemory:
    def remember_dialogue_turn(
        self,
        brain,
        speaker: str,
        text: str,
        intent: str | None = None,
        person_name: str | None = None,
    ) -> None:
        brain.memory_manager.add_dialogue_turn(
            {
                "speaker": speaker,
                "text": text,
                "intent": intent,
                "person_name": person_name,
            }
        )

    def get_recent_dialogue(self, brain, limit: int = 6) -> list[dict]:
        return brain.memory_manager.get_recent_dialogue(limit)

    def build_dialogue_summary(self, brain, limit: int = 4) -> str:
        dialogue = self.get_recent_dialogue(brain, limit)

        if not dialogue:
            return "Немає недавнього діалогу."

        parts = []
        for turn in dialogue:
            speaker = turn.get("speaker", "unknown")
            text = turn.get("text", "")
            parts.append(f"{speaker}: {text}")

        return " | ".join(parts)
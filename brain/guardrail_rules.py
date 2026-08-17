class GuardrailRules:
    def __init__(self) -> None:
        self.blocked_action_types = {
            "aggressive_move",
            "loud_alarm",
        }

        self.pet_safe_action_replacements = {
            "track_face": "gentle_track",
            "idle_animation": "soft_idle",
        }

        self.max_voice_replies_per_cycle = 2
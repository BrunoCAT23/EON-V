from settings import MAX_MOTOR_SPEED
from brain.guardrail_rules import GuardrailRules
from brain.behavior_boundaries import BehaviorBoundaries


class SafetyLayer:
    def __init__(self) -> None:
        self.rules = GuardrailRules()
        self.boundaries = BehaviorBoundaries()

    def filter_actions(self, brain, actions: list[dict]) -> list[dict]:
        safe_actions = []
        voice_reply_count = 0
        reduce_intensity = self.boundaries.should_reduce_intensity(brain)

        for action in actions:
            action_type = action.get("type")
            value = action.get("value")

            if action_type in self.rules.blocked_action_types:
                print(f"[SAFETY] Blocked action: {action}")
                continue

            if action_type == "voice_reply":
                voice_reply_count += 1
                if voice_reply_count > self.rules.max_voice_replies_per_cycle:
                    print(f"[SAFETY] Too many voice replies, skipping: {action}")
                    continue

            if action_type == "set_head_position" and value not in {"left", "right", "center", "down"}:
                print(f"[SAFETY] Unsafe head position blocked: {value}")
                continue

            if action_type in {"move_forward", "move_backward", "turn_left", "turn_right"}:
                speed = action.get("speed", 50)
                try:
                    action["speed"] = max(0, min(int(MAX_MOTOR_SPEED), int(speed)))
                except (TypeError, ValueError):
                    action["speed"] = 40

            if reduce_intensity:
                if action_type in self.rules.pet_safe_action_replacements:
                    replacement = self.rules.pet_safe_action_replacements[action_type]
                    safe_actions.append({"type": replacement, "value": value})
                    continue

                if action_type == "voice_reply" and isinstance(value, str):
                    safe_actions.append(
                        {
                            "type": "voice_reply",
                            "value": f"{value} Я поводитимуся спокійно.",
                        }
                    )
                    continue

            safe_actions.append(action)

        return safe_actions

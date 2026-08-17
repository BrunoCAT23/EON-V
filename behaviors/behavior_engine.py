from behaviors.animation_library import ANIMATION_LIBRARY
from behaviors.gesture_library import GESTURE_LIBRARY
from behaviors.idle_behavior import IdleBehavior


class BehaviorEngine:
    def __init__(self) -> None:
        self.idle_behavior = IdleBehavior()

    def run_animation(self, animation_name: str, brain) -> list[dict]:
        if animation_name not in ANIMATION_LIBRARY:
            return [
                {"type": "log", "value": f"Unknown animation: {animation_name}"}
            ]

        actions = []

        for action in ANIMATION_LIBRARY[animation_name]:
            if action.get("type") == "gesture":
                gesture_name = action.get("value")
                actions.extend(self.expand_gesture(gesture_name))
            else:
                actions.append(action)

        return actions

    def expand_gesture(self, gesture_name: str) -> list[dict]:
        return GESTURE_LIBRARY.get(
            gesture_name,
            [{"type": "log", "value": f"Unknown gesture: {gesture_name}"}]
        )

    def generate_idle_behavior(self, brain) -> list[dict]:
        actions = self.idle_behavior.generate(brain)

        expanded = []
        for action in actions:
            if action.get("type") == "gesture":
                expanded.extend(self.expand_gesture(action.get("value")))
            else:
                expanded.append(action)

        return expanded
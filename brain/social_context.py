class SocialContext:
    def __init__(self) -> None:
        self.focused_person = None
        self.interaction_mode = "neutral"

    def focus_on_person(self, person_name: str) -> None:
        self.focused_person = person_name
        self.interaction_mode = "social"

    def clear_focus(self) -> None:
        self.focused_person = None
        self.interaction_mode = "neutral"

    def get_focused_person(self) -> str | None:
        return self.focused_person

    def get_interaction_mode(self) -> str:
        return self.interaction_mode

    def snapshot(self) -> dict:
        return {
            "focused_person": self.focused_person,
            "interaction_mode": self.interaction_mode,
        }
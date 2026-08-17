class BaseSkill:
    def __init__(self, name: str) -> None:
        self.name = name

    def execute(self, brain, payload: dict | None = None) -> dict:
        raise NotImplementedError("Skill must implement execute()")
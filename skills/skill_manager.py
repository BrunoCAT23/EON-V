from skills.greet_skill import GreetSkill
from skills.status_skill import StatusSkill
from skills.think_skill import ThinkSkill
from skills.sleep_skill import SleepSkill


class SkillManager:
    def __init__(self) -> None:
        self.skills = {}
        self.register_default_skills()

    def register_default_skills(self) -> None:
        self.register(GreetSkill())
        self.register(StatusSkill())
        self.register(ThinkSkill())
        self.register(SleepSkill())

    def register(self, skill) -> None:
        self.skills[skill.name] = skill

    def has_skill(self, skill_name: str) -> bool:
        return skill_name in self.skills

    def execute_skill(self, skill_name: str, brain, payload: dict | None = None) -> dict:
        if skill_name not in self.skills:
            return {
                "success": False,
                "skill": skill_name,
                "text": f"Skill '{skill_name}' not found.",
                "actions": [
                    {"type": "voice_reply", "value": f"У мене немає навичок {skill_name}."}
                ]
            }

        return self.skills[skill_name].execute(brain, payload)
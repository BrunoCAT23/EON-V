class PersonalKnowledge:
    def get_person_facts(self, brain, person_name: str) -> list[str]:
        people = brain.memory_manager.get_people()
        person = people.get(person_name, {})
        return person.get("facts", [])

    def add_person_fact(self, brain, person_name: str, fact: str) -> None:
        brain.memory_manager.add_person_fact(person_name, fact)

    def build_person_context_line(self, brain, person_name: str) -> str:
        facts = self.get_person_facts(brain, person_name)

        if not facts:
            return f"Я поки що мало знаю про {person_name}."

        last_fact = facts[-1]
        return f"Я пам'ятаю про {person_name} ось що: {last_fact}"
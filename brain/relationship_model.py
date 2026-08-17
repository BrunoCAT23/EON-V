class RelationshipModel:
    def get_relationship(self, brain, person_name: str) -> dict:
        people = brain.memory_manager.get_people()
        person = people.get(person_name, {})
        return person.get(
            "relationship",
            {
                "trust": 0.1,
                "familiarity": 0.1,
                "bond_level": "new",
            },
        )

    def increase_trust(self, brain, person_name: str, amount: float = 0.05) -> None:
        relationship = self.get_relationship(brain, person_name)
        new_value = min(1.0, relationship.get("trust", 0.1) + amount)
        brain.memory_manager.update_person_relationship(person_name, "trust", new_value)
        self._update_bond_level(brain, person_name)

    def increase_familiarity(self, brain, person_name: str, amount: float = 0.05) -> None:
        relationship = self.get_relationship(brain, person_name)
        new_value = min(1.0, relationship.get("familiarity", 0.1) + amount)
        brain.memory_manager.update_person_relationship(person_name, "familiarity", new_value)
        self._update_bond_level(brain, person_name)

    def _update_bond_level(self, brain, person_name: str) -> None:
        relationship = self.get_relationship(brain, person_name)
        trust = relationship.get("trust", 0.1)
        familiarity = relationship.get("familiarity", 0.1)

        avg = (trust + familiarity) / 2

        if avg >= 0.75:
            level = "close"
        elif avg >= 0.45:
            level = "friend"
        else:
            level = "new"

        brain.memory_manager.update_person_relationship(person_name, "bond_level", level)

    def build_relationship_summary(self, brain, person_name: str) -> str:
        relationship = self.get_relationship(brain, person_name)
        return (
            f"Стосунок із {person_name}: "
            f"trust={relationship.get('trust')}, "
            f"familiarity={relationship.get('familiarity')}, "
            f"bond={relationship.get('bond_level')}"
        )
import json
from pathlib import Path
from shutil import copy2
from tempfile import gettempdir

from settings import MEMORY_FILE, MEMORY_SANDBOX, PROJECT_ROOT


MAX_EVENTS = 100
MAX_DIALOGUE_TURNS = 50
MAX_PERSON_CONVERSATIONS = 10


class MemoryManager:
    def __init__(self) -> None:
        if MEMORY_SANDBOX:
            self.memory_file = Path(gettempdir()) / "eon_v_memory_sandbox.json"
        else:
            configured_path = Path(MEMORY_FILE)
            if configured_path.is_absolute():
                self.memory_file = configured_path
            else:
                self.memory_file = PROJECT_ROOT / configured_path

        self.short_term_memory = []
        self.data = self._load_memory()

    def _default_data(self) -> dict:
        return {
            "people": {},
            "pets": {},
            "events": [],
            "dialogue_history": [],
            "robot_profile": {
                "name": "EON-V",
                "mood_baseline": "neutral",
                "traits": {
                    "friendliness": 8,
                    "curiosity": 9,
                    "energy": 7
                }
            },
            "context_memory": {
                "last_person_seen": None,
                "last_interaction_type": None
            }
        }

    def _default_relationship(self) -> dict:
        return {
            "trust": 0.1,
            "familiarity": 0.1,
            "bond_level": "new"
        }

    def _default_person(self, name: str, times_seen: int = 0) -> dict:
        return {
            "name": name,
            "times_seen": times_seen,
            "last_seen": None,
            "facts": [],
            "preferences": {},
            "relationship": self._default_relationship(),
            "attachment_style": "distant_polite",
            "preferred_name": name,
            "important_dates": {},
            "last_conversations": [],
        }

    def _ensure_person_defaults(self, name: str) -> dict:
        if name not in self.data["people"]:
            self.data["people"][name] = self._default_person(name)

        person_data = self.data["people"][name]
        defaults = self._default_person(name)
        for key, value in defaults.items():
            person_data.setdefault(key, value)
        person_data.setdefault("relationship", self._default_relationship())
        return person_data

    def _default_pet(self, name: str, pet_type: str = "unknown_pet") -> dict:
        return {
            "name": name,
            "type": pet_type,
            "times_seen": 0,
            "last_seen": None,
            "traits": {
                "playfulness": "unknown",
                "energy": "unknown",
            }
        }

    def _load_memory(self) -> dict:
        if not self.memory_file.exists():
            default_data = self._default_data()
            self._save_memory_data(default_data)
            return default_data

        try:
            with self.memory_file.open("r", encoding="utf-8") as file:
                loaded = json.load(file)

            default = self._default_data()

            for key, value in default.items():
                if key not in loaded:
                    loaded[key] = value

            for _, person_data in loaded.get("people", {}).items():
                person_data.setdefault("facts", [])
                person_data.setdefault("preferences", {})
                person_data.setdefault("relationship", self._default_relationship())
                person_data.setdefault("attachment_style", "distant_polite")
                person_data.setdefault("preferred_name", person_data.get("name", "friend"))
                person_data.setdefault("important_dates", {})
                person_data.setdefault("last_conversations", [])

            for pet_name, pet_data in loaded.get("pets", {}).items():
                pet_type = pet_data.get("type", "unknown_pet")
                default_pet = self._default_pet(pet_name, pet_type)
                for key, value in default_pet.items():
                    if key not in pet_data:
                        pet_data[key] = value
                pet_data.setdefault("traits", default_pet["traits"])

            return loaded

        except (json.JSONDecodeError, OSError):
            print("[MEMORY] Failed to read memory file. Creating new memory.")
            default_data = self._default_data()
            self._save_memory_data(default_data)
            return default_data

    def _save_memory_data(self, data: dict) -> None:
        self.memory_file.parent.mkdir(parents=True, exist_ok=True)
        if self.memory_file.exists() and not MEMORY_SANDBOX:
            backup_path = self.memory_file.with_suffix(self.memory_file.suffix + ".bak")
            copy2(self.memory_file, backup_path)
        with self.memory_file.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def save(self) -> None:
        self._compact_memory()
        self._save_memory_data(self.data)

    def _compact_memory(self) -> None:
        self.data["events"] = self._dedupe_recent(self.data.get("events", []), MAX_EVENTS)
        self.data["dialogue_history"] = self.data.get("dialogue_history", [])[-MAX_DIALOGUE_TURNS:]
        for person_data in self.data.get("people", {}).values():
            conversations = person_data.get("last_conversations", [])
            person_data["last_conversations"] = conversations[-MAX_PERSON_CONVERSATIONS:]

    def _dedupe_recent(self, values: list[str], limit: int) -> list[str]:
        deduped: list[str] = []
        for value in values:
            if deduped and deduped[-1] == value:
                continue
            deduped.append(value)
        return deduped[-limit:]

    def remember(self, item: str) -> None:
        self.short_term_memory.append(item)
        self.data["events"].append(item)

        self.data["events"] = self._dedupe_recent(self.data["events"], MAX_EVENTS)

        self.save()
        print(f"[MEMORY] Saved: {item}")

    def recall_recent(self, limit: int = 5) -> list[str]:
        return self.short_term_memory[-limit:]

    def recall_persistent_events(self, limit: int = 10) -> list[str]:
        return self.data["events"][-limit:]

    def save_person(self, name: str) -> None:
        if name not in self.data["people"]:
            self.data["people"][name] = self._default_person(name, times_seen=1)
            self.data["people"][name]["last_seen"] = "now"
        else:
            self._ensure_person_defaults(name)
            self.data["people"][name]["times_seen"] += 1
            self.data["people"][name]["last_seen"] = "now"

        self.save()
        print(f"[MEMORY] Person saved: {name}")

    def mark_person_seen(self, name: str) -> None:
        if name in self.data["people"]:
            self._ensure_person_defaults(name)
            self.data["people"][name]["times_seen"] += 1
            self.data["people"][name]["last_seen"] = "now"
        else:
            self.data["people"][name] = self._default_person(name, times_seen=1)
            self.data["people"][name]["last_seen"] = "now"

        self.data["context_memory"]["last_person_seen"] = name
        self.data["context_memory"]["last_interaction_type"] = "visual_recognition"

        self.save()
        print(f"[MEMORY] Person seen: {name}")

    def save_pet(self, name: str, pet_type: str) -> None:
        if name not in self.data["pets"]:
            pet = self._default_pet(name, pet_type)
            pet["times_seen"] = 1
            pet["last_seen"] = "now"
            self.data["pets"][name] = pet
        else:
            self.data["pets"][name]["times_seen"] += 1
            self.data["pets"][name]["last_seen"] = "now"
            self.data["pets"][name]["type"] = pet_type
            self.data["pets"][name].setdefault("traits", self._default_pet(name, pet_type)["traits"])

        self.save()
        print(f"[MEMORY] Pet saved: {name} ({pet_type})")

    def mark_pet_seen(self, name: str) -> None:
        if name in self.data["pets"]:
            self.data["pets"][name]["times_seen"] += 1
            self.data["pets"][name]["last_seen"] = "now"
        else:
            self.data["pets"][name] = self._default_pet(name)
            self.data["pets"][name]["times_seen"] = 1
            self.data["pets"][name]["last_seen"] = "now"

        self.save()
        print(f"[MEMORY] Pet seen: {name}")

    def update_pet_trait(self, name: str, key: str, value) -> None:
        if name not in self.data["pets"]:
            self.data["pets"][name] = self._default_pet(name)

        self.data["pets"][name].setdefault("traits", {})
        self.data["pets"][name]["traits"][key] = value
        self.save()
        print(f"[MEMORY] Updated pet trait for {name}: {key}={value}")

    def add_person_fact(self, name: str, fact: str) -> None:
        self._ensure_person_defaults(name)

        if fact not in self.data["people"][name]["facts"]:
            self.data["people"][name]["facts"].append(fact)
            self.save()
            print(f"[MEMORY] Added fact for {name}: {fact}")

    def update_person_preference(self, name: str, key: str, value) -> None:
        self._ensure_person_defaults(name)
        self.data["people"][name]["preferences"][key] = value
        self.save()
        print(f"[MEMORY] Updated preference for {name}: {key}={value}")

    def update_person_relationship(self, name: str, key: str, value) -> None:
        self._ensure_person_defaults(name)
        self.data["people"][name]["relationship"][key] = value
        self.save()
        print(f"[MEMORY] Updated relationship for {name}: {key}={value}")

    def update_attachment_style(self, name: str, style: str) -> None:
        self._ensure_person_defaults(name)
        self.data["people"][name]["attachment_style"] = style
        self.save()
        print(f"[MEMORY] Updated attachment style for {name}: {style}")

    def update_preferred_name(self, name: str, preferred_name: str) -> None:
        self._ensure_person_defaults(name)
        self.data["people"][name]["preferred_name"] = preferred_name
        self.save()
        print(f"[MEMORY] Updated preferred name for {name}: {preferred_name}")

    def add_important_date(self, name: str, label: str, date_value: str) -> None:
        self._ensure_person_defaults(name)
        self.data["people"][name].setdefault("important_dates", {})
        self.data["people"][name]["important_dates"][label] = date_value
        self.save()
        print(f"[MEMORY] Added important date for {name}: {label}={date_value}")

    def add_person_conversation(self, name: str, text: str) -> None:
        self._ensure_person_defaults(name)
        history = self.data["people"][name].setdefault("last_conversations", [])
        history.append(text)
        self.data["people"][name]["last_conversations"] = history[-MAX_PERSON_CONVERSATIONS:]
        self.save()

    def add_dialogue_turn(self, turn: dict) -> None:
        self.data["dialogue_history"].append(turn)

        self.data["dialogue_history"] = self.data["dialogue_history"][-MAX_DIALOGUE_TURNS:]

        self.save()
        print(f"[MEMORY] Dialogue turn saved: {turn}")

    def get_recent_dialogue(self, limit: int = 6) -> list[dict]:
        return self.data["dialogue_history"][-limit:]

    def save_interaction_context(self, person_name: str | None, interaction_type: str) -> None:
        self.data["context_memory"]["last_person_seen"] = person_name
        self.data["context_memory"]["last_interaction_type"] = interaction_type
        self.save()

    def get_people(self) -> dict:
        return self.data["people"]

    def get_pets(self) -> dict:
        return self.data["pets"]

    def get_robot_profile(self) -> dict:
        return self.data["robot_profile"]

    def get_context_memory(self) -> dict:
        return self.data["context_memory"]

class IntentParser:
    def parse(self, text: str) -> dict:
        normalized = text.strip().lower()

        if not normalized:
            return {"intent": "empty", "entities": {}, "skill": None}

        if "привіт" in normalized or "вітаю" in normalized:
            return {"intent": "greeting", "entities": {}, "skill": "greet"}

        if "спи" in normalized or "сон" in normalized:
            return {"intent": "sleep", "entities": {}, "skill": "sleep"}

        if "прокинься" in normalized or "прокидайся" in normalized:
            return {"intent": "wake", "entities": {}, "skill": None}

        if "статус" in normalized or "стан системи" in normalized:
            return {"intent": "status", "entities": {}, "skill": "status"}

        if "діагност" in normalized or "перевір залізо" in normalized:
            return {"intent": "diagnostics", "entities": {}, "skill": None}

        if "журнал" in normalized or "що сталося" in normalized:
            return {"intent": "event_log", "entities": {}, "skill": None}

        if "безпека" in normalized or "аварійна зупинка" in normalized:
            return {"intent": "safety_status", "entities": {}, "skill": None}

        if (
            "що ми говорили" in normalized
            or "що я казав" in normalized
            or "згадай розмову" in normalized
            or "пам'ятаєш розмову" in normalized
        ):
            return {"intent": "dialogue_summary", "entities": {}, "skill": None}

        if normalized.startswith("познайомся з "):
            name = normalized.replace("познайомся з ", "", 1).strip()
            return {"intent": "meet_person", "entities": {"name": name}, "skill": None}

        if normalized.startswith("запам'ятай що "):
            fact = normalized.replace("запам'ятай що ", "", 1).strip()
            return {"intent": "remember_fact", "entities": {"fact": fact}, "skill": None}

        if normalized.startswith("що ти знаєш про "):
            name = normalized.replace("що ти знаєш про ", "", 1).strip()
            return {"intent": "recall_person_facts", "entities": {"name": name}, "skill": None}

        if normalized.startswith("поверни голову "):
            position = normalized.replace("поверни голову ", "", 1).strip()
            mapping = {
                "ліворуч": "left",
                "вліво": "left",
                "праворуч": "right",
                "вправо": "right",
                "по центру": "center",
                "в центр": "center",
                "вниз": "down",
            }
            return {
                "intent": "head_position",
                "entities": {"position": mapping.get(position, position)},
                "skill": None,
            }

        if normalized.startswith("нагадай через "):
            payload = normalized.replace("нагадай через ", "", 1).strip()
            return {"intent": "remind_in", "entities": {"payload": payload}, "skill": None}

        if normalized.startswith("називай "):
            payload = normalized.replace("називай ", "", 1).strip()
            return {"intent": "profile_set_name", "entities": {"payload": payload}, "skill": None}

        if normalized.startswith("покажи профіль "):
            name = normalized.replace("покажи профіль ", "", 1).strip()
            return {"intent": "profile", "entities": {"name": name}, "skill": None}

        if normalized.startswith("запам'ятай дату "):
            payload = normalized.replace("запам'ятай дату ", "", 1).strip()
            return {"intent": "profile_add_date", "entities": {"payload": payload}, "skill": None}

        if normalized.startswith("навчись "):
            payload = normalized.replace("навчись ", "", 1).strip()
            return {"intent": "teach", "entities": {"payload": payload}, "skill": None}

        if "бачиш мене" in normalized:
            return {"intent": "face_check", "entities": {}, "skill": None}

        if "подумай" in normalized or "думай" in normalized:
            return {"intent": "think", "entities": {}, "skill": "think"}

        return {
            "intent": "free_dialogue",
            "entities": {"raw_text": normalized},
            "skill": None,
        }

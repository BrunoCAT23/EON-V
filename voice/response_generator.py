class ResponseGenerator:
    def generate(self, intent_data: dict) -> dict:
        intent = intent_data.get("intent")
        entities = intent_data.get("entities", {})

        if intent == "greeting":
            return {"event": "voice_greeting", "text": "Привіт. Я тут і готовий допомагати."}

        if intent == "sleep":
            return {"event": "sleep", "text": "Добре. Я переходжу в режим сну."}

        if intent == "wake":
            return {"event": "wake", "text": "Я прокинувся і знову активний."}

        if intent == "status":
            return {"event": "status", "text": "Показую поточний стан."}

        if intent == "dialogue_summary":
            return {"event": "dialogue_summary", "text": "Зараз згадаю останню розмову."}

        if intent == "meet_person":
            name = entities.get("name", "").strip()
            return {"event": f"meet {name}", "text": f"Добре. Я запам'ятаю {name}."}

        if intent == "remember_fact":
            fact = entities.get("fact", "").strip()
            return {"event": f"remember_fact {fact}", "text": "Добре. Я спробую це запам'ятати."}

        if intent == "recall_person_facts":
            name = entities.get("name", "").strip()
            return {"event": f"recall_person_facts {name}", "text": f"Зараз скажу, що я знаю про {name}."}

        if intent == "face_check":
            return {"event": "face", "text": "Я активую режим візуального контакту."}

        if intent == "think":
            return {"event": "think", "text": "Запускаю аналіз."}

        if intent == "diagnostics":
            return {"event": "diagnostics", "text": "Запускаю діагностику."}

        if intent == "event_log":
            return {"event": "event_log", "text": "Показую журнал подій."}

        if intent == "safety_status":
            return {"event": "safety_status", "text": "Перевіряю стан безпеки."}

        if intent == "head_position":
            position = entities.get("position", "").strip()
            return {"event": f"head {position}", "text": f"Повертаю голову: {position}."}

        if intent == "remind_in":
            payload = entities.get("payload", "").strip()
            return {"event": f"remind_in {payload}", "text": "Добре, створюю нагадування."}

        if intent == "profile_set_name":
            payload = entities.get("payload", "").strip()
            return {"event": f"profile_set_name {payload}", "text": "Запам'ятовую звертання."}

        if intent == "profile":
            name = entities.get("name", "").strip()
            return {"event": f"profile {name}", "text": f"Показую профіль {name}."}

        if intent == "profile_add_date":
            payload = entities.get("payload", "").strip()
            return {"event": f"profile_add_date {payload}", "text": "Запам'ятовую важливу дату."}

        if intent == "teach":
            payload = entities.get("payload", "").strip()
            return {"event": f"teach {payload}", "text": "Записую нове знання."}

        if intent == "free_dialogue":
            raw_text = entities.get("raw_text", "")
            return {"event": f"free_dialogue {raw_text}", "text": "Я думаю над відповіддю."}

        if intent == "empty":
            return {"event": None, "text": "Я нічого не чув."}

        return {"event": None, "text": "Я поки не розумію цю голосову команду."}

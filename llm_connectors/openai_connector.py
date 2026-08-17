from llm_connectors.connector_config import (
    OPENAI_ENABLED,
    OPENAI_API_KEY,
    OPENAI_BASE_URL,
    OPENAI_MODEL,
)


class OpenAIConnector:
    def generate(self, prompt: dict) -> str | None:
        if not OPENAI_ENABLED:
            return None

        if not OPENAI_API_KEY.strip():
            print("[OPENAI_CONNECTOR] API key is missing")
            return None

        try:
            import requests
        except ImportError:
            print("[OPENAI_CONNECTOR] requests not installed")
            return None

        try:
            response = requests.post(
                f"{OPENAI_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": OPENAI_MODEL,
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                f"{prompt.get('system_identity')}\n"
                                f"Personality: {prompt.get('personality')}\n"
                                f"Focused person: {prompt.get('focused_person')}\n"
                                f"Person facts: {prompt.get('person_facts')}\n"
                                f"Recent dialogue: {prompt.get('recent_dialogue')}\n"
                                f"Presence: {prompt.get('presence')}\n"
                                "You are EON-V, a warm physical AI companion robot."
                            ),
                        },
                        {
                            "role": "user",
                            "content": prompt.get("user_text"),
                        },
                    ],
                    "temperature": 0.7,
                },
                timeout=25,
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as exc:
            print(f"[OPENAI_CONNECTOR] Error: {exc}")
            return None
from llm_connectors.connector_config import (
    OLLAMA_ENABLED,
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
)


class OllamaConnector:
    def generate(self, prompt: dict) -> str | None:
        if not OLLAMA_ENABLED:
            return None

        try:
            import requests
        except ImportError:
            print("[OLLAMA_CONNECTOR] requests not installed")
            return None

        try:
            response = requests.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": self._build_prompt_text(prompt),
                    "stream": False,
                },
                timeout=20,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("response")
        except Exception as exc:
            print(f"[OLLAMA_CONNECTOR] Error: {exc}")
            return None

    def _build_prompt_text(self, prompt: dict) -> str:
        return (
            f"System identity: {prompt.get('system_identity')}\n"
            f"Personality: {prompt.get('personality')}\n"
            f"Focused person: {prompt.get('focused_person')}\n"
            f"Person facts: {prompt.get('person_facts')}\n"
            f"Recent dialogue: {prompt.get('recent_dialogue')}\n"
            f"Presence: {prompt.get('presence')}\n"
            f"User text: {prompt.get('user_text')}\n"
            "Reply as EON-V, a warm physical AI companion."
        )
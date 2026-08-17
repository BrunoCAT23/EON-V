from llm_connectors.connector_config import (
    OLLAMA_ENABLED,
    OPENAI_ENABLED,
    OPENAI_API_KEY,
)


def get_connector_status() -> dict:
    return {
        "ollama_enabled": OLLAMA_ENABLED,
        "openai_enabled": OPENAI_ENABLED,
        "openai_key_present": bool(OPENAI_API_KEY.strip()),
    }
from llm_connectors.ollama_connector import OllamaConnector
from llm_connectors.fallback_connector import FallbackConnector


class LocalLLM:
    def __init__(self) -> None:
        self.ollama = OllamaConnector()
        self.fallback = FallbackConnector()

    def generate(self, prompt: dict) -> str:
        result = self.ollama.generate(prompt)

        if result:
            return result

        return self.fallback.generate(prompt, route="local")
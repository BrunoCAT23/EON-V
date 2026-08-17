from llm_connectors.openai_connector import OpenAIConnector
from llm_connectors.fallback_connector import FallbackConnector


class CloudLLM:
    def __init__(self) -> None:
        self.openai = OpenAIConnector()
        self.fallback = FallbackConnector()

    def generate(self, prompt: dict) -> str:
        result = self.openai.generate(prompt)

        if result:
            return result

        return self.fallback.generate(prompt, route="cloud")
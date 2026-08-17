from llm.llm_config import LLM_MODE
from llm.prompt_builder import PromptBuilder
from llm.local_llm import LocalLLM
from llm.cloud_llm import CloudLLM
from llm.hybrid_router import HybridRouter
from llm_connectors.connector_status import get_connector_status


class LLMManager:
    def __init__(self) -> None:
        self.mode = LLM_MODE
        self.prompt_builder = PromptBuilder()
        self.local_llm = LocalLLM()
        self.cloud_llm = CloudLLM()
        self.hybrid_router = HybridRouter()
        self.connector_status = get_connector_status()

    def generate_reply(self, brain, user_text: str) -> dict:
        prompt = self.prompt_builder.build(brain, user_text)

        if self.mode == "local":
            route = "local"
        elif self.mode == "cloud":
            route = "cloud"
        else:
            route = self.hybrid_router.choose_route(user_text)

        if route == "cloud":
            text = self.cloud_llm.generate(prompt)
        else:
            text = self.local_llm.generate(prompt)

        return {
            "route": route,
            "prompt": prompt,
            "text": text,
            "connector_status": self.connector_status,
        }
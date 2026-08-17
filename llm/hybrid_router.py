class HybridRouter:
    def choose_route(self, user_text: str) -> str:
        normalized = user_text.strip().lower()

        complex_markers = [
            "чому",
            "поясни",
            "розкажи",
            "як ти думаєш",
            "що буде",
            "проаналізуй",
        ]

        if any(marker in normalized for marker in complex_markers):
            return "cloud"

        if len(normalized.split()) > 8:
            return "cloud"

        return "local"
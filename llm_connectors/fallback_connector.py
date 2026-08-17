class FallbackConnector:
    def generate(self, prompt: dict, route: str) -> str:
        user_text = prompt.get("user_text", "")
        focused_person = prompt.get("focused_person")

        if focused_person:
            return (
                f"[FALLBACK {route.upper()}] "
                f"{focused_person}, я поки що працюю в безпечному резервному режимі. "
                f"Твій запит: {user_text}"
            )

        return (
            f"[FALLBACK {route.upper()}] "
            f"Я поки що працюю в безпечному резервному режимі. "
            f"Твій запит: {user_text}"
        )
class CompanionBehavior:
    def build_companion_reply(self, base_text: str, attachment_style: str) -> str:
        if attachment_style == "secure_close":
            return f"{base_text} Я радий, що ми з тобою добре знайомі."

        if attachment_style == "warm_social":
            return f"{base_text} Мені завжди приємно з тобою взаємодіяти."

        if attachment_style == "careful_opening":
            return f"{base_text} Я поступово краще за тебе дізнаюся."

        return base_text

    def build_proactive_companion_ping(self, person_name: str, attachment_style: str) -> str:
        if attachment_style == "secure_close":
            return f"{person_name}, я поряд. Мені важлива наша взаємодія."

        if attachment_style == "warm_social":
            return f"{person_name}, я радий, що ти тут."

        if attachment_style == "careful_opening":
            return f"{person_name}, мені цікаво продовжити наше знайомство."

        return f"{person_name}, я тут і готовий до взаємодії."
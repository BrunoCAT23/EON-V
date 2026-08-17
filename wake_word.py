WAKE_WORDS = ["еон", "йон", "іон", "е он", "і он"]

def is_wake_word(text):
    text = text.lower()

    # точне спрацювання
    if len(text) <= 10:
        for word in WAKE_WORDS:
            if word in text:
                return True

    # fallback
    if len(text) <= 6 and any(x in text for x in ["он", "ео", "іо"]):
        return True

    return False


def clean_command(text):
    text = text.lower()

    for word in WAKE_WORDS:
        text = text.replace(word, "")

    return text.strip()
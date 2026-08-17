import random

MOODS = ["happy", "curious", "sleepy", "excited"]

def get_mood():
    return random.choice(MOODS)


def add_emotion(text, mood):
    if mood == "happy":
        return f"*біп-біп!* 😄 {text}"

    elif mood == "curious":
        return f"*вжж?* 🤔 {text}"

    elif mood == "sleepy":
        return f"*пік...* 😴 {text}"

    elif mood == "excited":
        return f"*БІП-БІП!!!* 🤖 {text}"

    return text
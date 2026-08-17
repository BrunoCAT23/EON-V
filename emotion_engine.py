import random
import time

current_emotion = "neutral"

emotion_data = {
    "neutral": {
        "responses": [
            "Я слухаю.",
            "Гаразд.",
            "Добре."
        ],
    "speed": 1.0
   },

    "happy": {
        "responses": [
            "Мені подобається!",
            "Це круто 😄",
            "Я радий тебе чути!"
        ],
        "speed": 1.2
    },

    "curious": {
        "responses": [
            "Хмм...",
            "Цікаво 🤔",
            "Я аналізую..."
        ],
        "speed": 0.9
    },

    "sleepy": {
        "responses": [
            "Я трохи втомився...",
            "Ммм...",
            "Хочу спати 😴"
        ],
        "speed": 0.7
    },

    "angry": {
        "responses": [
            "Мені це не подобається.",
            "Хмм.",
            "Не роби так 😠"
        ],
        "speed": 1.4
    },

    "sad": {
        "responses": [
            "Мені сумно...",
            "Не знаю...",
            "😔"
        ],
        "speed": 0.6
    },

    "excited": {
        "responses": [
            "Ооо!",
            "Це дуже цікаво!",
            "Вау ⚡"
        ],
        "speed": 1.5
    }
}


# 🎭 ВСТАНОВЛЕННЯ ЕМОЦІЇ
def set_emotion(emotion):
    global current_emotion

    if emotion in emotion_data:
        current_emotion = emotion
        print(f"🎭 Emotion → {emotion}")


# 📖 ОТРИМАТИ ПОТОЧНУ ЕМОЦІЮ
def get_emotion():
    return current_emotion


# 💬 ВИПАДКОВА ФРАЗА
def get_emotion_response():
    data = emotion_data[current_emotion]
    return random.choice(data["responses"])


# ⚡ ШВИДКІСТЬ ГОЛОСУ
def get_voice_speed():
    data = emotion_data[current_emotion]
    return data["speed"]


# 🧠 ПРОСТИЙ AI АНАЛІЗ ЕМОЦІЇ
def analyze_emotion(text):
    text = text.lower()

    if any(word in text for word in ["клас", "супер", "дякую"]):
        set_emotion("happy")

    elif any(word in text for word in ["цікаво", "що це"]):
        set_emotion("curious")

    elif any(word in text for word in ["дурень", "бісить"]):
        set_emotion("angry")

    elif any(word in text for word in ["сумно", "погано"]):
        set_emotion("sad")

    else:
        # випадкова idle емоція
        set_emotion(random.choice([
            "happy",
            "curious",
            "neutral"
        ]))
import requests
from personality.eon_personality import get_mood, add_emotion

def ask_ai(text):
    mood = get_mood()

    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "llama3:8b",
        "prompt": f"""
    Ти робот EON-V.
    Говори тільки українською.
    Коротко і емоційно.

    Користувач: {text}
    EON:
    """,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)

        data = response.json()

        # 🔥 перевірка відповіді
        if "response" not in data:
            print("❌ Ollama відповів дивно:", data)
            return "Хмм... *біп* щось не думаю..."

        result = data["response"]

        final = add_emotion(result, mood)

        return final

    except Exception as e:
        print("❌ ПОМИЛКА OLLAMA:", e)
        return "Я завис... *пік*"
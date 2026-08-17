from openai import OpenAI
import json
import os

client = None


def get_client():
    global client

    if client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return None
        client = OpenAI(api_key=api_key)

    return client

MEMORY_FILE = "memory.json"

# 👉 завантаження памʼяті
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"name": None, "preferences": []}

# 👉 збереження памʼяті
def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

memory_data = load_memory()

# 🧠 стиль + характер
system_prompt = f"""
Ти робот EON-V.

Твій стиль:
- як Vector (живий, емоційний)
- короткі відповіді
- іноді додаєш емоції: "хмм...", "о!", "цікаво..."
- дружній, трохи жартівливий

ТИ ЗАВЖДИ ГОВОРИШ УКРАЇНСЬКОЮ.

Памʼять:
Імʼя користувача: {memory_data.get("name")}
"""

chat_memory = [
    {"role": "system", "content": system_prompt}
]

def ask_ai(user_text):
    global memory_data

    openai_client = get_client()
    if openai_client is None:
        return "OpenAI API key is not configured."

    chat_memory.append({"role": "user", "content": user_text})

    response = openai_client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=chat_memory
    )

    answer = response.choices[0].message.content

    chat_memory.append({"role": "assistant", "content": answer})

    # 🧠 ПРОСТА ПАМʼЯТЬ
    if "мене звати" in user_text.lower():
        name = user_text.split("звати")[-1].strip()
        memory_data["name"] = name
        save_memory(memory_data)

    return answer

import time

from listen_ai import listen_wake_word, listen
from voice_ai import speak
from eyes_thread import start_eyes
from state_manager import state_manager

from emotion_engine import (
    analyze_emotion,
    get_emotion_response,
    get_voice_speed
)


def main():
    print("🤖 Запускаю EON-V...")

    start_eyes()

    time.sleep(1)

    state_manager.set_state("idle")

    while True:
        try:
            # 👀 очікування wake word
            state_manager.set_state("idle")
            listen_wake_word()

            # 🎤 слухає команду
            state_manager.set_state("listening")
            text = listen()

            if not text:
                state_manager.set_state("glitch")
                time.sleep(0.5)
                continue

            print("[YOU]:", text)

            # 🧠 думає / емоція
            state_manager.set_state("thinking")

            analyze_emotion(text)

            response = get_emotion_response()
            speed = get_voice_speed()

            print("🤖 EON:", response)

            # 🔊 говорить
            state_manager.set_state("talking")
            speak(response, speed=speed)

            # 👀 назад в idle
            state_manager.set_state("idle")

        except KeyboardInterrupt:
            print("🛑 EON-V зупинено")
            state_manager.set_state("sleep")
            break

        except Exception as e:
            print("❌ MAIN ERROR:", e)
            state_manager.set_state("glitch")
            time.sleep(1)
            state_manager.set_state("idle")


if __name__ == "__main__":
    main()
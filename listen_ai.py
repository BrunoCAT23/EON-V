from vosk import Model, KaldiRecognizer
import sounddevice as sd
import json

model = Model("models/vosk")
recognizer = KaldiRecognizer(model, 16000)

WAKE_WORDS = ["еон", "йон", "іон", "eon"]

def is_wake_word(text):
    text = text.lower()
    return any(word in text for word in WAKE_WORDS)


def listen_wake_word():
    print("🟡 Чекаю 'Еон'...")

    with sd.RawInputStream(
        samplerate=16000,
        blocksize=8000,
        dtype="int16",
        channels=1
    ) as stream:

        while True:
            data = stream.read(4000)[0]
            data = bytes(data)

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")

                if text:
                    print("🧠 Чую:", text)

                    if is_wake_word(text):
                        print("⚡ WAKE WORD DETECTED!")
                        return True


def listen():
    print("🎤 Слухаю команду...")

    with sd.RawInputStream(
        samplerate=16000,
        blocksize=8000,
        dtype="int16",
        channels=1
    ) as stream:

        while True:
            data = stream.read(4000)[0]
            data = bytes(data)

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")

                if text:
                    return text
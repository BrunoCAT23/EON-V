import sounddevice as sd
import soundfile as sf
import os

def play_sound(path):
    if not os.path.exists(path):
        print(f"❌ Файл не знайдено: {path}")
        return

    data, samplerate = sf.read(path, dtype='float32')
    sd.play(data, samplerate)
    sd.wait()


def emotion_sound(emotion):
    sounds = {
        "happy": "sounds/happy.wav",
        "sad": "sounds/sad.wav",
        "angry": "sounds/angry.wav",
        "thinking": "sounds/thinking.wav"
    }

    if emotion in sounds:
        play_sound(sounds[emotion])
import math
import wave
from pathlib import Path

from settings import (
    PROJECT_ROOT,
    STARTUP_SOUND_ENABLED,
    STARTUP_SOUND_PATH,
    STARTUP_SOUND_VOLUME,
)


SAMPLE_RATE = 22050


def _resolve_sound_path() -> Path:
    path = Path(STARTUP_SOUND_PATH)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def _clamp_sample(value: float) -> int:
    value = max(-1.0, min(1.0, value))
    return int(value * 32767)


def _envelope(t: float, duration: float, attack: float = 0.04, release: float = 0.2) -> float:
    if t < attack:
        return t / attack
    if t > duration - release:
        return max(0.0, (duration - t) / release)
    return 1.0


def _tone(t: float, freq: float, duration: float, gain: float) -> float:
    return math.sin(2.0 * math.pi * freq * t) * gain * _envelope(t, duration)


def generate_startup_sound(path: Path | None = None) -> Path:
    output_path = path or _resolve_sound_path()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    duration = 2.4
    total_samples = int(SAMPLE_RATE * duration)
    samples = []

    for index in range(total_samples):
        t = index / SAMPLE_RATE

        # Original cinematic robot boot sound: low power-on pulse, servo texture,
        # then a clean confirmation chime. This is not copied from any film.
        low_pulse = 0.0
        if t < 1.3:
            sweep_freq = 52.0 + (t / 1.3) * 42.0
            low_pulse = math.sin(2.0 * math.pi * sweep_freq * t) * 0.34
            low_pulse += math.sin(2.0 * math.pi * (sweep_freq * 0.5) * t) * 0.22
            low_pulse *= _envelope(t, 1.3, attack=0.08, release=0.25)

        servo_texture = 0.0
        if 0.35 <= t <= 1.65:
            local_t = t - 0.35
            texture_freq = 180.0 + math.sin(local_t * 18.0) * 65.0
            gate = 0.5 + 0.5 * math.sin(local_t * 46.0)
            servo_texture = math.sin(2.0 * math.pi * texture_freq * local_t) * gate * 0.08
            servo_texture *= _envelope(local_t, 1.3, attack=0.03, release=0.18)

        chime = 0.0
        if 1.25 <= t:
            local_t = t - 1.25
            chime += _tone(local_t, 392.0, 1.15, 0.16)
            chime += _tone(local_t, 587.33, 1.15, 0.12)
            chime += _tone(local_t, 783.99, 1.15, 0.08)

        mechanical_click = 0.0
        for click_time in [0.18, 0.62, 1.08]:
            distance = abs(t - click_time)
            if distance < 0.015:
                mechanical_click += (1.0 - distance / 0.015) * 0.18 * math.sin(2.0 * math.pi * 1200.0 * t)

        sample = (low_pulse + servo_texture + chime + mechanical_click) * STARTUP_SOUND_VOLUME
        samples.append(_clamp_sample(sample))

    with wave.open(str(output_path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(b"".join(sample.to_bytes(2, byteorder="little", signed=True) for sample in samples))

    return output_path


def ensure_startup_sound() -> Path:
    path = _resolve_sound_path()
    if not path.exists():
        return generate_startup_sound(path)
    return path


def play_startup_sound(force: bool = False) -> None:
    if not STARTUP_SOUND_ENABLED and not force:
        return

    path = ensure_startup_sound()

    try:
        import sounddevice as sd
        import soundfile as sf

        data, sample_rate = sf.read(str(path), dtype="float32")
        sd.play(data, sample_rate)
        sd.wait()
        return
    except Exception as exc:
        print(f"[STARTUP_SOUND] sounddevice playback failed: {exc}")

    try:
        import winsound

        winsound.PlaySound(str(path), winsound.SND_FILENAME)
    except Exception as exc:
        print(f"[STARTUP_SOUND] winsound playback failed: {exc}")

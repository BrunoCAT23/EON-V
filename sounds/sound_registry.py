from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from settings import (
    PROJECT_ROOT,
    SOUND_EFFECTS_DIR,
    SOUND_EFFECTS_ENABLED,
    SOUND_EFFECTS_VOLUME,
)
from sounds.startup_sound import ensure_startup_sound


SUPPORTED_AUDIO = {".wav", ".mp3", ".ogg", ".flac", ".aiff", ".aif"}


EVENT_ALIASES = {
    "startup": "eon_startup.wav",
    "boot": "eon_startup.wav",
    "power_on": "eon_startup.wav",
    "robot": "freesound_community-robot-6282.wav",
    "wake_ack": "freesound_community-robot-6282.wav",
    "voice_greeting": "freesound_community-robot-6282.wav",
    "thinking": "freesound_community-robot-6282.wav",
    "think": "freesound_community-robot-6282.wav",
    "face_detected": "freesound_community-robot-6282.wav",
    "face": "freesound_community-robot-6282.wav",
    "pet_detected": "freesound_community-robot-6282.wav",
    "recognized_pet": "freesound_community-robot-6282.wav",
    "recognized_face": "freesound_community-robot-6282.wav",
    "error": "freesound_community-robot-6282.wav",
    "battery_low": "freesound_community-robot-6282.wav",
    "sleep": "eon_startup.wav",
}


@dataclass(frozen=True)
class SoundEntry:
    name: str
    path: Path
    source: str


def _sound_dir() -> Path:
    path = Path(SOUND_EFFECTS_DIR)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def _normalize_name(name: str) -> str:
    return name.strip().lower().replace(" ", "_")


def _resolve_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return PROJECT_ROOT / candidate


def list_sounds() -> dict[str, SoundEntry]:
    sounds: dict[str, SoundEntry] = {}

    startup_path = ensure_startup_sound()
    if startup_path.exists():
        sounds["startup"] = SoundEntry("startup", startup_path, "generated")

    directory = _sound_dir()
    if directory.exists():
        for path in sorted(directory.iterdir()):
            if not path.is_file() or path.suffix.lower() not in SUPPORTED_AUDIO:
                continue

            key = _normalize_name(path.stem)
            sounds[key] = SoundEntry(key, path, "file")

    for alias, filename in EVENT_ALIASES.items():
        path = _resolve_path(Path(SOUND_EFFECTS_DIR) / filename)
        if path.exists():
            sounds[_normalize_name(alias)] = SoundEntry(_normalize_name(alias), path, "alias")

    return sounds


def resolve_sound(name: str) -> SoundEntry | None:
    if not name:
        return None

    normalized = _normalize_name(name)
    sounds = list_sounds()

    if normalized in sounds:
        return sounds[normalized]

    for alias in sorted(EVENT_ALIASES, key=len, reverse=True):
        normalized_alias = _normalize_name(alias)
        if normalized == normalized_alias or normalized.startswith(f"{normalized_alias}_"):
            return sounds.get(normalized_alias)

    event_prefix = normalized.split(":", 1)[0]
    return sounds.get(event_prefix)


def play_sound(name: str, force: bool = False) -> bool:
    if not SOUND_EFFECTS_ENABLED and not force:
        return False

    entry = resolve_sound(name)
    if entry is None:
        print(f"[SOUND] Unknown sound: {name}")
        return False

    path = entry.path

    try:
        import sounddevice as sd
        import soundfile as sf

        data, sample_rate = sf.read(str(path), dtype="float32")
        data = data * max(0.0, min(1.0, SOUND_EFFECTS_VOLUME))
        sd.play(data, sample_rate)
        sd.wait()
        return True
    except Exception as exc:
        print(f"[SOUND] sounddevice playback failed: {exc}")

    if path.suffix.lower() != ".wav":
        print(f"[SOUND] winsound fallback supports only WAV files: {path}")
        return False

    try:
        import winsound

        winsound.PlaySound(str(path), winsound.SND_FILENAME)
        return True
    except Exception as exc:
        print(f"[SOUND] winsound playback failed: {exc}")
        return False


def play_event_sound(event: str | None) -> bool:
    if not event:
        return False

    return play_sound(event)

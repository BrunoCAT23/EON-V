import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
ENV_FILE = PROJECT_ROOT / ".env"


def load_dotenv(path: Path = ENV_FILE) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key and key not in os.environ:
            os.environ[key] = value


def env_str(name: str, default: str) -> str:
    return os.getenv(name, default).strip()


def env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default

    try:
        return int(value)
    except ValueError:
        return default


def env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None:
        return default

    try:
        return float(value)
    except ValueError:
        return default


def env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default

    return value.strip().lower() in {"1", "true", "yes", "on"}


load_dotenv()

ROBOT_NAME = env_str("ROBOT_NAME", "EON-V")
RUNTIME_MODE = env_str("RUNTIME_MODE", "simulation")

MIC_MODE = env_str("MIC_MODE", "stub")
SPEAKER_MODE = env_str("SPEAKER_MODE", "stub")
STT_MODE = env_str("STT_MODE", "fallback")
TTS_MODE = env_str("TTS_MODE", "fallback")

CAMERA_MODE = env_str("CAMERA_MODE", "stub")
DETECTOR_MODE = env_str("DETECTOR_MODE", "stub")
OPENCV_CAMERA_INDEX = env_int("OPENCV_CAMERA_INDEX", 0)
YOLO_MODEL_PATH = env_str("YOLO_MODEL_PATH", "models/yolo_placeholder.onnx")

HARDWARE_MODE = env_str("HARDWARE_MODE", "mock")
ARDUINO_PORT = env_str("ARDUINO_PORT", "COM5")
ARDUINO_BAUDRATE = env_int("ARDUINO_BAUDRATE", 115200)
ARDUINO_TIMEOUT = env_float("ARDUINO_TIMEOUT", 1.0)

OLLAMA_ENABLED = env_bool("OLLAMA_ENABLED", False)
OLLAMA_BASE_URL = env_str("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = env_str("OLLAMA_MODEL", "llama3.1")

OPENAI_ENABLED = env_bool("OPENAI_ENABLED", False)
OPENAI_API_KEY = env_str("OPENAI_API_KEY", "")
OPENAI_BASE_URL = env_str("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL = env_str("OPENAI_MODEL", "gpt-4.1-mini")

RUNTIME_TICK_DELAY = env_float("RUNTIME_TICK_DELAY", 1.0)

MEMORY_FILE = env_str("MEMORY_FILE", "memory/data.json")
MEMORY_SANDBOX = env_bool("MEMORY_SANDBOX", False)

VOICE_PROFILE = env_str("VOICE_PROFILE", "eon_default")
VOICE_STYLE = env_str("VOICE_STYLE", "warm_ukrainian_companion")
VOICE_RATE = env_float("VOICE_RATE", 1.0)
VOICE_PITCH = env_float("VOICE_PITCH", 1.0)
WAKE_WORDS = env_str("WAKE_WORDS", "eon,eon-v,еон,еон-ві,йон,іон,єон,e on")
WAKE_WORD_FUZZY = env_bool("WAKE_WORD_FUZZY", True)
WAKE_WORD_MAX_DISTANCE = env_int("WAKE_WORD_MAX_DISTANCE", 1)
WAKE_ACK_SOUND = env_str("WAKE_ACK_SOUND", "wake_ack")
WAKE_FOLLOWUP_CAPTURE = env_bool("WAKE_FOLLOWUP_CAPTURE", True)
WAKE_REPLY_TEXT = env_str("WAKE_REPLY_TEXT", "Так?")
DO_NOT_DISTURB = env_bool("DO_NOT_DISTURB", False)
MIC_SAMPLE_RATE = env_int("MIC_SAMPLE_RATE", 16000)
MIC_RECORD_SECONDS = env_float("MIC_RECORD_SECONDS", 4.0)
MIC_CAPTURE_MODE = env_str("MIC_CAPTURE_MODE", "vad")
VAD_FRAME_MS = env_int("VAD_FRAME_MS", 30)
VAD_MAX_RECORD_SECONDS = env_float("VAD_MAX_RECORD_SECONDS", 6.0)
VAD_MIN_SPEECH_SECONDS = env_float("VAD_MIN_SPEECH_SECONDS", 0.25)
VAD_SILENCE_MS = env_int("VAD_SILENCE_MS", 700)
VAD_PREROLL_MS = env_int("VAD_PREROLL_MS", 300)
VAD_CALIBRATION_MS = env_int("VAD_CALIBRATION_MS", 300)
VAD_ENERGY_THRESHOLD = env_int("VAD_ENERGY_THRESHOLD", 350)
VAD_NOISE_MULTIPLIER = env_float("VAD_NOISE_MULTIPLIER", 2.5)
VOSK_MODEL_PATH = env_str("VOSK_MODEL_PATH", "models/vosk")
PIPER_EXE_PATH = env_str("PIPER_EXE_PATH", "tools/piper/piper.exe")
PIPER_VOICE_PATH = env_str("PIPER_VOICE_PATH", "tools/piper/voices/uk_UA-ukrainian_tts-medium.onnx")

MAX_MOTOR_SPEED = env_float("MAX_MOTOR_SPEED", 60.0)
MIN_SERVO_ANGLE = env_float("MIN_SERVO_ANGLE", 25.0)
MAX_SERVO_ANGLE = env_float("MAX_SERVO_ANGLE", 155.0)
MOTION_ENABLED = env_bool("MOTION_ENABLED", True)
MOTION_DRY_RUN = env_bool("MOTION_DRY_RUN", HARDWARE_MODE == "mock")
MOTION_COMMAND_TIMEOUT = env_float("MOTION_COMMAND_TIMEOUT", 3.0)

STARTUP_SOUND_ENABLED = env_bool("STARTUP_SOUND_ENABLED", True)
STARTUP_SOUND_PATH = env_str("STARTUP_SOUND_PATH", "sounds/eon_startup.wav")
STARTUP_SOUND_VOLUME = env_float("STARTUP_SOUND_VOLUME", 0.7)
SOUND_EFFECTS_ENABLED = env_bool("SOUND_EFFECTS_ENABLED", True)
SOUND_EFFECTS_VOLUME = env_float("SOUND_EFFECTS_VOLUME", 0.8)
SOUND_EFFECTS_DIR = env_str("SOUND_EFFECTS_DIR", "sounds")

LIVE_VOICE_INTERVAL = env_float("LIVE_VOICE_INTERVAL", 4.0)
LIVE_VISION_INTERVAL = env_float("LIVE_VISION_INTERVAL", 2.0)
LIVE_RUNTIME_INTERVAL = env_float("LIVE_RUNTIME_INTERVAL", 1.0)
LIVE_MAX_CYCLES = env_int("LIVE_MAX_CYCLES", 0)
LAST_FRAME_PATH = env_str("LAST_FRAME_PATH", "logs/last_frame.jpg")
VOICE_TEST_PHRASE = env_str("VOICE_TEST_PHRASE", "Привіт. Я EON-V. Голосова система працює.")

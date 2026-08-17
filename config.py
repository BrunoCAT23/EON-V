ROBOT_NAME = "EON-V"

DEFAULT_STATE = "IDLE"

AVAILABLE_STATES = [
    "BOOTING",
    "IDLE",
    "LISTENING",
    "THINKING",
    "TALKING",
    "TRACKING_PERSON",
    "SLEEP",
    "ERROR",
    # Legacy lowercase states used by the older main_test.py flow.
    "idle",
    "listening",
    "thinking",
    "talking",
    "sleep",
    "glitch",
    "happy",
    "curious",
    "angry",
    "charging",
]

DEFAULT_EMOTION = "neutral"

AVAILABLE_EMOTIONS = [
    "neutral",
    "happy",
    "curious",
    "thinking",
    "sleepy",
    "sad",
]

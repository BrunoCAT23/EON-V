ANIMATION_LIBRARY = {
    "greet_animation": [
        {"type": "show_emotion", "value": "happy"},
        {"type": "gesture", "value": "small_wave"},
        {"type": "voice_reply", "value": "Привіт. Я радий тебе бачити."},
    ],
    "thinking_animation": [
        {"type": "show_emotion", "value": "thinking"},
        {"type": "gesture", "value": "head_tilt"},
        {"type": "log", "value": "Thinking animation started"},
    ],
    "sleep_animation": [
        {"type": "show_emotion", "value": "sleepy"},
        {"type": "gesture", "value": "head_down"},
        {"type": "sleep_mode"},
    ],
    "wake_animation": [
        {"type": "show_emotion", "value": "happy"},
        {"type": "gesture", "value": "look_up"},
        {"type": "voice_reply", "value": "Я знову активний."},
    ],
}
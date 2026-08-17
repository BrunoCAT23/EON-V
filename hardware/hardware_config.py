from settings import (
    ARDUINO_BAUDRATE,
    ARDUINO_PORT,
    ARDUINO_TIMEOUT,
    HARDWARE_MODE,
)

LEFT_MOTOR_PINS = {
    "in1": 17,
    "in2": 18,
    "enable": 12,
}

RIGHT_MOTOR_PINS = {
    "in1": 22,
    "in2": 23,
    "enable": 13,
}

HEAD_SERVO_PIN = 19

DISPLAY_CONFIG = {
    "width": 320,
    "height": 240,
    "type": "2inch_ips",
}

AUDIO_CONFIG = {
    "output_device": "default_speaker",
}

ARDUINO_CONFIG = {
    "port": ARDUINO_PORT,
    "baudrate": ARDUINO_BAUDRATE,
    "timeout": ARDUINO_TIMEOUT,
}

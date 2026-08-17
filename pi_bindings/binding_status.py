from pi_bindings.pi_env import is_raspberry_pi, safe_import


def get_binding_status() -> dict:
    return {
        "is_raspberry_pi": is_raspberry_pi(),
        "gpiozero_available": safe_import("gpiozero"),
        "rpi_gpio_available": safe_import("RPi.GPIO"),
        "board_available": safe_import("board"),
        "busio_available": safe_import("busio"),
        "adafruit_pca9685_available": safe_import("adafruit_pca9685"),
    }
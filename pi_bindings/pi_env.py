import platform


def is_raspberry_pi() -> bool:
    machine = platform.machine().lower()
    return "arm" in machine or "aarch" in machine


def safe_import(module_name: str) -> bool:
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False
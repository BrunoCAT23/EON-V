import threading
from eyes_system import run_eyes


def start_eyes():
    thread = threading.Thread(
        target=run_eyes,
        daemon=True
    )
    thread.start()
    return thread
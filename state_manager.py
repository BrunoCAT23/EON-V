from config import DEFAULT_STATE, AVAILABLE_STATES
import threading


class StateManager:
    def __init__(self) -> None:
        self.current_state = DEFAULT_STATE
        self.lock = threading.Lock()

    def set_state(self, new_state: str) -> None:
        if new_state not in AVAILABLE_STATES:
            print(f"[STATE] Unknown state: {new_state}")
            return

        with self.lock:
            old_state = self.current_state
            self.current_state = new_state

        print(f"[STATE] {old_state} -> {new_state}")

    def get_state(self) -> str:
        with self.lock:
            return self.current_state

    def is_state(self, state_name: str) -> bool:
        return self.get_state() == state_name


state_manager = StateManager()
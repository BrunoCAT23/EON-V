class Scheduler:
    def __init__(self, action_executor, action_queue) -> None:
        self.action_executor = action_executor
        self.action_queue = action_queue

    def run_next(self) -> None:
        next_action = self.action_queue.pop_next()

        if not next_action:
            print("[SCHEDULER] No actions to run")
            return

        print(f"[SCHEDULER] Running action: {next_action}")
        self.action_executor.execute([next_action])

    def run_all(self) -> None:
        if not self.action_queue.has_actions():
            print("[SCHEDULER] Queue is empty")
            return

        while self.action_queue.has_actions():
            self.run_next()
class AutonomousLoop:
    def __init__(self) -> None:
        self.idle_interval = 3

    def tick(self, brain) -> None:
        tick_number = brain.life_state.next_tick()
        print(f"[AUTO_LOOP] Tick: {tick_number}")

        if brain.action_queue.has_actions():
            print("[AUTO_LOOP] Queue has actions, running next action")
            brain.run_next_action()
            return

        if brain.state_manager.get_state() == "SLEEP":
            print("[AUTO_LOOP] Robot is sleeping, skipping idle behavior")
            return

        last_idle_tick = brain.life_state.get_last_idle_tick()

        if tick_number - last_idle_tick >= self.idle_interval:
            print("[AUTO_LOOP] Triggering autonomous idle behavior")
            actions = brain.behavior_engine.generate_idle_behavior(brain)
            brain.enqueue_actions(actions)
            brain.life_state.set_last_idle_tick(tick_number)
        else:
            print("[AUTO_LOOP] No autonomous action this tick")
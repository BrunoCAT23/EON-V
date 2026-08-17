class RuntimeOrchestrator:
    def __init__(self) -> None:
        pass

    def step(self, brain) -> None:
        if not brain.life_state.is_enabled():
            print("[RUNTIME] Autonomous mode OFF")
            return

        brain.life_state.next_tick()
        tick = brain.life_state.get_tick()

        print(f"\n[RUNTIME] ===== TICK {tick} =====")

        # 1. Needs update
        brain.needs_engine.update()

        # 2. Consume synchronized perception
        voice_packet, vision_packet = brain.perception_sync.consume()
        fused_stimuli = brain.stimulus_fusion.fuse(voice_packet, vision_packet)

        self.process_fused_stimuli(brain, fused_stimuli)

        # 3. Presence / perception maintenance
        presence_actions = brain.perception_fusion.maintain_presence(brain)

        # 4. Reactive triggers
        reactive_actions = brain.reactive_triggers.evaluate(brain)

        # 5. Goal selection
        goal = brain.goal_engine.decide_goal(brain)
        brain.current_goal = goal

        goal_actions = []
        if goal:
            print(f"[RUNTIME] Goal selected: {goal}")
            goal_actions = brain.goal_executor.execute(brain, goal)

        # 6. Combine actions
        actions = []
        actions.extend(presence_actions)
        actions.extend(reactive_actions)
        actions.extend(goal_actions)

        if not actions:
            print("[RUNTIME] No actions generated")
            return

        brain.enqueue_actions(actions)

        # 7. Execute a limited number each tick
        self.execute_limited(brain)

    def process_fused_stimuli(self, brain, fused_stimuli: list[dict]) -> None:
        if not fused_stimuli:
            print("[RUNTIME] No fused stimuli")
            return

        print(f"[RUNTIME] Fused stimuli count: {len(fused_stimuli)}")

        top = fused_stimuli[0]
        print(f"[RUNTIME] Top focus channel: {top['channel']}")

        for item in fused_stimuli:
            channel = item["channel"]
            data = item["data"]

            if channel == "voice":
                response = data.get("response", {})
                event = response.get("event")
                if event:
                    brain.process_event(event)

            elif channel == "vision":
                response = data.get("response", {})
                event = response.get("event")
                if event:
                    brain.process_event(event)

    def execute_limited(self, brain, max_actions: int = 2) -> None:
        count = 0

        while brain.action_queue.has_actions() and count < max_actions:
            brain.run_next_action()
            count += 1
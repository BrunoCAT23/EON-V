class AttentionSystem:
    def __init__(self) -> None:
        self.current_focus = None

    def select_focus(self, brain) -> dict | None:
        stimuli = brain.stimulus_tracker.recent_stimuli(limit=8)

        if not stimuli:
            self.current_focus = None
            return None

        scored = []

        for stimulus in stimuli:
            score = stimulus["salience"]

            if stimulus["type"] == "person_seen":
                score += 0.4

            if stimulus["type"] == "voice_input":
                score += 0.3

            if stimulus["type"] == "unknown_face":
                score += 0.35

            if stimulus["type"] == "new_fact":
                score += 0.2

            scored.append((score, stimulus))

        scored.sort(key=lambda item: item[0], reverse=True)
        self.current_focus = scored[0][1]
        return self.current_focus

    def get_focus(self) -> dict | None:
        return self.current_focus
class StimulusTracker:
    def __init__(self) -> None:
        self.stimuli = []

    def add_stimulus(
        self,
        stimulus_type: str,
        source: str,
        salience: float,
        tick: int,
        payload: dict | None = None,
    ) -> None:
        self.stimuli.append(
            {
                "type": stimulus_type,
                "source": source,
                "salience": salience,
                "tick": tick,
                "payload": payload or {},
            }
        )

        if len(self.stimuli) > 30:
            self.stimuli = self.stimuli[-30:]

    def recent_stimuli(self, limit: int = 10) -> list[dict]:
        return self.stimuli[-limit:]

    def snapshot(self) -> list[dict]:
        return list(self.stimuli)
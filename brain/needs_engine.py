class NeedsEngine:
    def __init__(self) -> None:
        self.needs = {
            "social": 0.5,
            "curiosity": 0.5,
            "energy": 1.0,
        }

        self.decay_rates = {
            "social": 0.03,
            "curiosity": 0.02,
            "energy": 0.01,
        }

    def update(self) -> None:
        for need, rate in self.decay_rates.items():
            self.needs[need] = max(0.0, self.needs[need] - rate)

    def satisfy(self, need: str, amount: float = 0.3) -> None:
        if need in self.needs:
            self.needs[need] = min(1.0, self.needs[need] + amount)

    def get_needs(self) -> dict:
        return dict(self.needs)

    def most_urgent_need(self) -> str:
        return min(self.needs, key=self.needs.get)
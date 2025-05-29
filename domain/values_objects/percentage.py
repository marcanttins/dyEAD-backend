# backend/domain/value_objects/percentage.py
class Percentage:
    def __init__(self, value: float):
        if not (0.0 <= value <= 100.0):
            raise ValueError("Percentage deve estar entre 0 e 100")
        self._value = float(value)

    @property
    def value(self) -> float:
        return self._value

    def __eq__(self, other):
        return isinstance(other, Percentage) and self.value == other.value

    def __str__(self):
        return f"{self.value:.2f}%"

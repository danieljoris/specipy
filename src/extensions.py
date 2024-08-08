from src.base import Specification


class GreaterThanSpecification(Specification[int]):
    def __init__(self, threshold: int):
        self.threshold = threshold

    def is_satisfied_by(self, candidate: int) -> bool:
        return candidate > self.threshold


class LessThanSpecification(Specification[int]):
    def __init__(self, threshold: int):
        self.threshold = threshold

    def is_satisfied_by(self, candidate: int) -> bool:
        return candidate < self.threshold


class BetweenSpecification(Specification[int]):
    def __init__(self, lower: int, upper: int):
        self.lower = lower
        self.upper = upper

    def is_satisfied_by(self, candidate: int) -> bool:
        return self.lower <= candidate <= self.upper


class MinLengthSpecification(Specification[str]):
    def __init__(self, min_length: int):
        self.min_length = min_length

    def is_satisfied_by(self, candidate: str) -> bool:
        return len(candidate) >= self.min_length


class MaxLengthSpecification(Specification[str]):
    def __init__(self, max_length: int):
        self.max_length = max_length

    def is_satisfied_by(self, candidate: str) -> bool:
        return len(candidate) <= self.max_length
